"""Codex exec の cwd、schema 保存先、permission profile 結合を検証する。

根拠:
- <work-root>/oracle/doc/app_spec/codex_exec_rule.md
- <work-root>/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
"""

import json
from multiprocessing import Barrier, Pipe, Process
from pathlib import Path

import pytest
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from config.cmoc_config import CmocConfig

from _codex_support import codex_override_config, codex_parameter, setup_codex_home
from _command_support import write_python_executable
from _git_support import make_repo, run_git
from commons.runtime_codex import run_codex_exec
from commons.runtime_paths import _reserve_timestamped_path


def reserve_fixed_codex_path(
    directory: Path, barrier: Barrier, connection: object
) -> None:
    """同じ初回 timestamp を使う別 process の予約を再現する。"""
    attempts = 0

    def timestamp_factory() -> str:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            barrier.wait(timeout=5)
            return "2099-01-01_00-00_00_000000000"
        return f"2099-01-01_00-00_00_000000000_retry_{attempts}"

    _, path = _reserve_timestamped_path(directory, "_call.json", timestamp_factory)
    connection.send(path.name)
    connection.close()


def test_timestamped_path_reservation_is_process_safe(tmp_path: Path) -> None:
    """同一 timestamp の並列予約でもログ path を共有しない。"""
    log_dir = tmp_path / "codex"
    log_dir.mkdir()
    barrier = Barrier(2)
    channels = [Pipe() for _ in range(2)]
    processes = [
        Process(
            target=reserve_fixed_codex_path,
            args=(log_dir, barrier, child),
        )
        for _parent, child in channels
    ]
    for process in processes:
        process.start()

    names = [parent.recv() for parent, _child in channels]
    for process in processes:
        process.join(5)

    assert all(process.exitcode == 0 for process in processes)
    assert len(set(names)) == 2
    assert all((log_dir / name).is_file() for name in names)


def test_run_codex_exec_uses_parameter_cwd_independent_of_pure_oracle_read(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """パラメータの cwd と pure-oracle read の権限境界を検証する。

    正本仕様:
        <work-root>/oracle/doc/app_spec/codex_exec_rule.md
        <work-root>/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
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

    run_codex_exec(
        codex_parameter(FileAccessMode.PURE_ORACLE_READ),
        root=root,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )

    record = json.loads(recorder.read_text())
    work_root = str(root.resolve())
    assert record["args"][record["args"].index("--cd") + 1] == work_root
    assert record["cwd"] == work_root
    override_config = codex_override_config(record["args"])
    assert "--sandbox" not in record["args"]
    assert "sandbox_workspace_write" not in override_config
    assert override_config["default_permissions"] == "cmoc"
    assert override_config["permissions"]["cmoc"]["filesystem"] == {
        str((root / "oracle").resolve()): "read"
    }


def test_run_codex_exec_stores_schema_state_under_repo_root(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """リンク済み worktree の出力 schema を repo root 配下へ保存することを検証する。

    正本仕様:
        <work-root>/oracle/doc/app_spec/codex_exec_rule.md
    """
    root = make_repo(tmp_path)
    linked = root / ".cmoc" / "local" / "worktree" / "linked"
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
    assert schema_arg.parent == root / ".cmoc" / "local" / "schema"
    assert not (linked / ".cmoc" / "local" / "schema").exists()


def test_run_codex_exec_allows_repo_local_read_from_linked_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """リンク済み worktree から repo-local の追加 read path を許可することを検証する。

    正本仕様:
        <work-root>/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
    """
    root = make_repo(tmp_path)
    linked = root / ".cmoc" / "local" / "worktree" / "linked-exec-log"
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
        extra_read_paths=[root / ".cmoc" / "local" / "report" / "review" / "report.md"],
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )

    record = json.loads(recorder.read_text())
    assert record["cwd"] == str(linked.resolve())
    assert record["args"][record["args"].index("--cd") + 1] == str(linked.resolve())
    # <work-root>/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
    filesystem = codex_override_config(record["args"])["permissions"]["cmoc"][
        "filesystem"
    ]
    assert filesystem[str((root / ".cmoc" / "local").resolve())] == "read"


def test_run_codex_exec_overrides_do_not_open_agents_tree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """権限 override が `.agents` tree を write 対象として開かないことを検証する。

    正本仕様:
        <work-root>/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
    """
    root = make_repo(tmp_path)
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
    filesystem = codex_override_config(args)["permissions"]["cmoc"]["filesystem"]
    agents = (root / ".agents").resolve()
    assert not any(
        access == "write" and agents.is_relative_to(Path(path))
        for path, access in filesystem.items()
    )
    assert "--profile" not in args
