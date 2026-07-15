"""Codex exec の cwd、schema 保存先、sandbox argv を検証する。

根拠:
- {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
- {{work-root}}/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
"""

import json
from multiprocessing import Barrier, Pipe, Process
from pathlib import Path

import pytest
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from config.cmoc_config import CmocConfig

from _codex_support import (
    codex_override_config,
    codex_parameter,
    setup_codex_home,
)
from _command_support import write_python_executable
from _git_support import make_repo, run_git
from commons.runtime_codex import run_codex_exec


_FIXED_CODEX_TIMESTAMP = "2099-01-01_00-00_00_000000000"


def run_fixed_codex_exec(root: Path, barrier: Barrier, connection: object) -> None:
    """同じ初回 timestamp の実運用 Codex 呼び出しを別 process で実行する。"""
    import commons.runtime_codex_exec as exec_module

    attempts = 0

    def timestamp_factory() -> str:
        """初回は共有 timestamp を返し、再試行では一意な suffix を付けて返す。"""
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            barrier.wait(timeout=5)
            return _FIXED_CODEX_TIMESTAMP
        return f"{_FIXED_CODEX_TIMESTAMP}_retry_{attempts}"

    # {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    # Force both production calls through the same initial timestamp so the
    # reservation is exercised at the run_codex_exec boundary.
    exec_module.timestamp = timestamp_factory
    try:
        result = run_codex_exec(
            codex_parameter(),
            root=root,
            capacity_initial_sleep_sec=0,
            config=CmocConfig(),
        )
        connection.send(
            {
                "call_log_path": str(result.call_log_path),
                "prompt_log_path": str(result.prompt_log_path),
                "stdout_log_path": str(result.stdout_log_path),
                "stderr_log_path": str(result.stderr_log_path),
                "output_path": str(result.output_path),
            }
        )
    except BaseException as exc:
        connection.send({"error": f"{type(exc).__name__}: {exc}"})
    finally:
        connection.close()


def test_timestamped_path_reservation_is_process_safe(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """並列 run_codex_exec が同一 timestamp でもログ path を共有しない。"""
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, pathlib, sys",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "output.write_text('done\\n')",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    barrier = Barrier(2)
    channels = [Pipe() for _ in range(2)]
    processes = [
        Process(
            target=run_fixed_codex_exec,
            args=(root, barrier, child),
        )
        for _parent, child in channels
    ]
    for process in processes:
        process.start()

    records = []
    for parent, _child in channels:
        assert parent.poll(10)
        records.append(parent.recv())
    for process in processes:
        process.join(10)

    assert all(process.exitcode == 0 for process in processes)
    assert all("error" not in record for record in records), records
    all_log_paths = []
    for record in records:
        call_path = Path(record["call_log_path"])
        call_log = json.loads(call_path.read_text())
        timestamp = call_log["timestamp"]
        assert timestamp.startswith(_FIXED_CODEX_TIMESTAMP)
        assert call_path.name == f"{timestamp}_call.json"
        related_paths = [
            call_path,
            *(
                Path(call_log[key])
                for key in (
                    "prompt_log_path",
                    "stdout_log_path",
                    "stderr_log_path",
                    "output_path",
                    "output_jsonl_log_path",
                )
            ),
        ]
        assert all(path.is_file() for path in related_paths)
        assert all(path.name.startswith(f"{timestamp}_") for path in related_paths)
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


@pytest.mark.parametrize(
    "parameter_cwd",
    [None, "oracle"],
    ids=["fallback_to_work_root", "parameter_cwd"],
)
def test_run_codex_exec_uses_parameter_cwd_independent_of_pure_oracle_read(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, parameter_cwd: str | None
) -> None:
    """パラメータの cwd と pure-oracle read の権限境界を検証する。

    正本仕様:
        {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
        {{work-root}}/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
    """
    root = make_repo(tmp_path)
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
            "output.write_text('done\\n')",
            f"pathlib.Path({str(recorder)!r}).write_text(json.dumps({{",
            "    'args': args,",
            "    'cwd': os.getcwd(),",
            "}))",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    target_cwd = root / parameter_cwd if parameter_cwd is not None else None
    run_codex_exec(
        codex_parameter(FileAccessMode.PURE_ORACLE_READ, cwd=target_cwd),
        root=root,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )

    record = json.loads(recorder.read_text())
    expected_cwd = (target_cwd or root).resolve()
    assert record["args"][record["args"].index("--cd") + 1] == str(expected_cwd)
    assert record["cwd"] == str(expected_cwd)
    override_config = codex_override_config(record["args"])
    assert record["args"][record["args"].index("--sandbox") + 1] == "read-only"
    assert "sandbox_workspace_write" not in override_config
    assert "default_permissions" not in override_config
    assert "permissions" not in override_config


def test_run_codex_exec_stores_schema_state_under_repo_root(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """リンク済み worktree の出力 schema を repo root 配下へ保存することを検証する。

    正本仕様:
        {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
    """
    root = make_repo(tmp_path)
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
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.REPO_WRITE,
        "prompt",
        schema_source,
    )

    result = run_codex_exec(
        parameter,
        root=root,
        cwd=linked,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )

    record = json.loads(recorder.read_text())
    schema_arg = Path(record["args"][record["args"].index("--output-schema") + 1])
    assert record["cwd"] == str(linked.resolve())
    assert result.schema_path == schema_arg
    assert schema_arg.parent == root / ".cmoc" / "gu" / "ar" / "schema"
    assert not (linked / ".cmoc" / "gu" / "ar" / "schema").exists()


def test_run_codex_exec_uses_readonly_sandbox_from_linked_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """linked worktree でも PURE_ORACLE_READ を専用 sandbox 引数へ変換する。

    正本仕様:
        {{work-root}}/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
    """
    root = make_repo(tmp_path)
    linked = root / ".cmoc" / "gu" / "worktree" / "linked-exec-log"
    linked.parent.mkdir(parents=True)
    run_git(root, "worktree", "add", "-b", "linked-exec-log", str(linked), "HEAD")
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
            "output.write_text('done\\n')",
            f"pathlib.Path({str(recorder)!r}).write_text(json.dumps({{",
            "    'args': args,",
            "    'cwd': os.getcwd(),",
            "}))",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    run_codex_exec(
        codex_parameter(FileAccessMode.PURE_ORACLE_READ),
        root=root,
        cwd=linked,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )

    record = json.loads(recorder.read_text())
    assert record["cwd"] == str(linked.resolve())
    assert record["args"][record["args"].index("--cd") + 1] == str(linked.resolve())
    assert record["args"][record["args"].index("--sandbox") + 1] == "read-only"
    override_config = codex_override_config(record["args"])
    assert "permissions" not in override_config
    assert "default_permissions" not in override_config


def test_run_codex_exec_does_not_inject_agents_path_permissions(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`.agents` の実在 path を sandbox の個別設定へ変換しないことを検証する。

    正本仕様:
        {{work-root}}/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
    """
    root = make_repo(tmp_path)
    agents_file = root / ".agents" / "nested" / "instructions.md"
    agents_file.parent.mkdir(parents=True)
    agents_file.write_text("agent instructions\n")
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "record.json"
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, pathlib, sys",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            f"pathlib.Path({str(recorder)!r}).write_text(json.dumps(args))",
            "output.write_text(json.dumps({'ok': True}))",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    run_codex_exec(
        codex_parameter(FileAccessMode.REPO_WRITE),
        root=root,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )

    args = json.loads(recorder.read_text())
    assert args[args.index("--sandbox") + 1] == "workspace-write"
    override_config = codex_override_config(args)
    assert "permissions" not in override_config
    assert "default_permissions" not in override_config
    assert all(str(agents_file.resolve()) not in arg for arg in args)
    assert "--profile" not in args
