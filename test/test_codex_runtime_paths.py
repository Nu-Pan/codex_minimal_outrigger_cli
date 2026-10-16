"""Codex exec の cwd、schema 保存先、sandbox argv を検証する。

根拠:
- {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
- {{work-root}}/oracle/src/oracle/prompt_builder/policy/file_access.py
"""

import json
from dataclasses import replace
from multiprocessing import Barrier, Pipe, Process
from multiprocessing.connection import Connection
from multiprocessing.synchronize import Barrier as BarrierType
from pathlib import Path

import oracle.other.path_model as path_model_module
import pytest
from _codex_support import (
    codex_override_config,
    codex_parameter,
    script_codex_calls,
    setup_codex_home,
)
from _command_support import write_python_executable
from _git_support import run_git

from basic.acp import FileAccessMode
from commons.runtime_codex import run_codex_exec
from commons.runtime_ids import is_common_id, new_id
from config.cmoc_config import CmocConfig

_FIXED_CODEX_TIMESTAMP = "2099-01-01_00-00-00_000"


def run_fixed_codex_exec(
    root: Path, barrier: BarrierType, connection: Connection
) -> None:
    """同時刻の Codex 呼び出しを別 process で実行する。"""
    import commons.runtime_codex_exec as exec_module

    def timestamp_factory() -> str:
        """両 process に同じ生成時刻を与えて path の独立性を確かめる。"""
        return _FIXED_CODEX_TIMESTAMP

    def resolve_test_roots(agent_call_cwd: Path) -> tuple[Path, Path]:
        assert agent_call_cwd == root
        return root, root

    try:
        with pytest.MonkeyPatch.context() as monkeypatch:
            monkeypatch.setattr(exec_module, "timestamp", timestamp_factory)
            # Git からの導出は後続の cwd・linked worktree test に残す。
            # 採番と log の検査では探索結果だけを固定し、実 context は使う。
            monkeypatch.setattr(
                path_model_module, "_resolve_git_worktree_roots", resolve_test_roots
            )
            # subprocess の cwd・env は後続の Fake CLI test に残す。
            # ここでは 2 process の実採番と log 保存だけを通し、孫 process を起動しない。
            script_codex_calls(
                monkeypatch,
                [(0, '{"type": "turn.completed"}\n', "done\n")] * 2,
            )
            # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
            # 発行前に同期し、記録日時が一致しても各 log が分離されることを調べる。
            barrier.wait(timeout=5)
            records = []
            for _ in range(2):
                result = run_codex_exec(
                    codex_parameter(agent_call_cwd=root),
                    root=root,
                    transient_poll_interval_sec=0,
                    config=CmocConfig(),
                )
                records.append(
                    {
                        "call_log_path": str(result.call_log_path),
                        "prompt_log_path": str(result.prompt_log_path),
                        "stdout_log_path": str(result.stdout_log_path),
                        "stderr_log_path": str(result.stderr_log_path),
                        "output_path": str(result.output_path),
                    }
                )
        connection.send(records)
    except BaseException as exc:
        connection.send([{"error": f"{type(exc).__name__}: {exc}"}])
    finally:
        connection.close()


def test_codex_call_ids_are_process_safe_on_same_timestamp(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """並行・連続発行とログ分離、終了・ログ削除後の通番維持を検査する。"""
    root = tmp_path / "repo"
    root.mkdir()
    setup_codex_home(tmp_path, monkeypatch)
    monkeypatch.setenv("PATH", "/usr/bin")
    barrier = Barrier(2)
    channels = [Pipe() for _ in range(2)]
    processes = [
        Process(
            target=run_fixed_codex_exec,
            args=(root, barrier, child),
        )
        for _parent, child in channels
    ]
    records = []
    started_processes = []
    try:
        for process in processes:
            process.start()
            started_processes.append(process)

        for parent, _child in channels:
            assert parent.poll(10)
            records.extend(parent.recv())
        for process in started_processes:
            process.join(10)

        assert all(process.exitcode == 0 for process in started_processes)
        assert all("error" not in record for record in records), records
        assert len(records) == 4
        all_log_paths = []
        cc_sequences = []
        for record in records:
            call_path = Path(record["call_log_path"])
            call_log = json.loads(call_path.read_text())
            assert call_log["timestamp"] == _FIXED_CODEX_TIMESTAMP
            codex_call_id = call_log["codex_call_id"]
            assert is_common_id(codex_call_id, "cc")
            cc_sequences.append(int(codex_call_id.split("_")[1], 36))
            assert is_common_id(call_log["execution_id"], "exec")
            assert call_path.parent.name == call_log["execution_id"]
            assert call_path.name == f"{codex_call_id}_call.json"
            related_paths = [
                call_path,
                *(
                    Path(call_log[key])
                    for key in (
                        "prompt_log_path",
                        "stdout_log_path",
                        "stderr_log_path",
                        "output_path",
                    )
                ),
            ]
            assert all(path.is_file() for path in related_paths)
            assert all(path.parent == call_path.parent for path in related_paths)
            assert all(
                path.name.startswith(f"{codex_call_id}_") for path in related_paths
            )
            assert {
                Path(record[key])
                for key in (
                    "call_log_path",
                    "prompt_log_path",
                    "stdout_log_path",
                    "stderr_log_path",
                    "output_path",
                )
            }.issubset(related_paths)
            all_log_paths.extend(related_paths)

        assert len(all_log_paths) == len(set(all_log_paths))
        assert sorted(cc_sequences) == list(range(4))
        # 子の終了・実ログの削除後の非再利用を、同じ起動で検査する。
        for path in all_log_paths:
            path.unlink()
        assert new_id(root, "cc").startswith("cc_000004_")
    finally:
        for process in started_processes:
            if process.is_alive():
                process.terminate()
        for process in started_processes:
            process.join()
        for parent, child in channels:
            parent.close()
            child.close()


# 実採番と log の結合は上の並行 test に残す。以下の cwd・home・schema の検査では
# nonpersistent_codex_ids を使い、採番のたびの SQLite transaction と同期を省く。
@pytest.mark.parametrize(
    "agent_call_cwd_relative",
    [".", "oracle"],
    ids=["work_root", "nested_directory"],
)
def test_run_codex_exec_uses_agent_call_cwd_independent_of_pure_oracle_read(
    cli_repository: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    nonpersistent_codex_ids: None,
    agent_call_cwd_relative: str,
) -> None:
    """パラメータの cwd と pure-oracle read の権限境界を検証する。

    正本仕様:
        {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
        {{work-root}}/oracle/src/oracle/prompt_builder/policy/file_access.py
    """
    # oracle の存在による cwd の自動変更を検出し、Git 履歴の準備だけを省く。
    root = cli_repository
    (root / "oracle").mkdir()
    (root / "oracle" / "spec.md").write_text("# spec\n")
    agent_call_cwd = root / agent_call_cwd_relative
    # 相対 home の値・子の cwd 基準の解決・log 保存も同じ起動で検査する。
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    codex_home = agent_call_cwd / "relative_codex_home"
    codex_home.mkdir()
    monkeypatch.setenv("CODEX_HOME", "relative_codex_home")
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "record.json"
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, os, pathlib, sys",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "output.write_text('done\\n')",
            f"pathlib.Path({str(recorder)!r}).write_text(json.dumps({{",
            "    'args': args,",
            "    'cwd': os.getcwd(),",
            "    'codex_home': os.environ['CODEX_HOME'],",
            "    'resolved_home': str(pathlib.Path(os.environ['CODEX_HOME']).resolve()),",
            "}))",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    result = run_codex_exec(
        codex_parameter(
            FileAccessMode.PURE_ORACLE_READ,
            agent_call_cwd=agent_call_cwd,
        ),
        root=root,
        transient_poll_interval_sec=0,
        config=CmocConfig(),
    )

    record = json.loads(recorder.read_text())
    expected_cwd = agent_call_cwd.resolve()
    assert record["args"][record["args"].index("--cd") + 1] == str(expected_cwd)
    assert record["cwd"] == str(expected_cwd)
    assert record["codex_home"] == "relative_codex_home"
    assert Path(record["resolved_home"]) == codex_home
    assert result.codex_home == codex_home
    call_log = json.loads(result.call_log_path.read_text())
    assert call_log["codex_home"] == str(codex_home)
    override_config = codex_override_config(record["args"])
    assert record["args"][record["args"].index("--sandbox") + 1] == "workspace-write"
    assert override_config["sandbox_workspace_write"] == {"exclude_slash_tmp": False}
    assert "features" not in override_config
    assert "default_permissions" not in override_config
    assert "permissions" not in override_config


def test_run_codex_exec_uses_linked_worktree_context(
    committed_repository: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    nonpersistent_codex_ids: None,
) -> None:
    """linked worktree の cwd・sandbox と main repository の schema 保存先を検証する。

    正本仕様:
        {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    """
    # cwd・sandbox・schema の境界には実 linked metadata と HEAD だけを用意する。
    root = committed_repository
    linked = root / ".cmoc" / "gu" / "worktree" / "linked"
    linked.parent.mkdir(parents=True)
    run_git(root, "worktree", "add", "-b", "linked-exec", str(linked), "HEAD")
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "record.json"
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, os, pathlib, sys",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "output.write_text(json.dumps({'ok': True}))",
            f"pathlib.Path({str(recorder)!r}).write_text(json.dumps({{",
            "    'args': args,",
            "    'cwd': os.getcwd(),",
            "}))",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    schema_source = tmp_path / "schema.json"
    schema_source.write_text(
        json.dumps(
            {
                "type": "object",
                "required": ["ok"],
                "properties": {"ok": {"type": "boolean"}},
            }
        )
    )
    parameter = replace(
        codex_parameter(FileAccessMode.PURE_ORACLE_READ, agent_call_cwd=linked),
        structured_output_schema_path=schema_source,
    )

    result = run_codex_exec(
        parameter,
        root=root,
        transient_poll_interval_sec=0,
        config=CmocConfig(),
    )

    record = json.loads(recorder.read_text())
    schema_arg = Path(record["args"][record["args"].index("--output-schema") + 1])
    assert record["cwd"] == str(linked.resolve())
    assert record["args"][record["args"].index("--cd") + 1] == str(linked.resolve())
    assert record["args"][record["args"].index("--sandbox") + 1] == "workspace-write"
    override_config = codex_override_config(record["args"])
    assert "permissions" not in override_config
    assert "default_permissions" not in override_config
    assert result.schema_path == schema_arg
    assert schema_arg.parent == root / ".cmoc" / "gu" / "schema"
    assert not (linked / ".cmoc" / "gu" / "schema").exists()
