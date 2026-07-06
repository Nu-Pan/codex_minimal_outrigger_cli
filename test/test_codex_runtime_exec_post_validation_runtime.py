import json
import tomllib
from pathlib import Path

import pytest
from basic.acp import FileAccessMode
from cmoc_runtime import CmocError
from config.cmoc_config import CmocConfig
from _support import (
    codex_parameter,
    make_repo,
    run_git,
    setup_codex_home,
    write_python_executable,
)
from commons.runtime_codex import run_codex_exec


def test_run_codex_exec_allows_ignored_untracked_realization_write_diff(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    (root / ".gitignore").write_text("/build/\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "commit", "-m", "ignore build")
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    counter = tmp_path / "count.txt"
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, pathlib, sys",
            f"counter = pathlib.Path({str(counter)!r})",
            "count = int(counter.read_text()) if counter.exists() else 0",
            "counter.write_text(str(count + 1))",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "artifact = pathlib.Path('build/artifact.txt')",
            "artifact.parent.mkdir(exist_ok=True)",
            "artifact.write_text('ignored\\n')",
            "output.write_text('{}\\n')",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    run_codex_exec(
        codex_parameter(FileAccessMode.REALIZATION_WRITE),
        root=root,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )

    assert counter.read_text() == "1"
    assert (root / "build" / "artifact.txt").read_text() == "ignored\n"


def test_run_codex_exec_allows_realization_write_temporary_cache_diff(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    (root / ".gitignore").write_text("/.pytest_cache/\n__pycache__/\n*.pyc\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "commit", "-m", "ignore python caches")
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    counter = tmp_path / "count.txt"
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, pathlib, sys",
            f"counter = pathlib.Path({str(counter)!r})",
            "count = int(counter.read_text()) if counter.exists() else 0",
            "counter.write_text(str(count + 1))",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "cache = pathlib.Path('.pytest_cache')",
            "cache.mkdir(exist_ok=True)",
            "(cache / 'state').write_text('temporary\\n')",
            "pycache = pathlib.Path('oracle/__pycache__')",
            "pycache.mkdir(exist_ok=True)",
            "(pycache / 'spec.cpython-313.pyc').write_bytes(b'cache')",
            "output.write_text('{}\\n')",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    run_codex_exec(
        codex_parameter(FileAccessMode.REALIZATION_WRITE),
        root=root,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )

    assert counter.read_text() == "1"
    assert (root / ".pytest_cache" / "state").read_text() == "temporary\n"
    assert (root / "oracle" / "__pycache__" / "spec.cpython-313.pyc").is_file()


def test_run_codex_exec_allows_venv_diff_without_post_call_file_access_check(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    (root / ".gitignore").write_text("/.venv/\n")
    venv_python = root / ".venv" / "bin" / "python3"
    venv_python.parent.mkdir(parents=True)
    venv_python.write_text("before\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "commit", "-m", "ignore venv")
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    counter = tmp_path / "count.txt"
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, pathlib, sys",
            f"counter = pathlib.Path({str(counter)!r})",
            "count = int(counter.read_text()) if counter.exists() else 0",
            "counter.write_text(str(count + 1))",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "pathlib.Path('.venv/bin/python3').write_text(f'touched {count}\\n')",
            "output.write_text('{}\\n')",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    run_codex_exec(
        codex_parameter(FileAccessMode.READONLY),
        root=root,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )

    assert counter.read_text() == "1"
    assert venv_python.read_text() == "touched 0\n"


def test_run_codex_exec_allows_readonly_temporary_pytest_cache_diff(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
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
            "cache = pathlib.Path('.pytest_cache')",
            "cache.mkdir(exist_ok=True)",
            "(cache / 'state').write_text('temporary\\n')",
            "pycache = pathlib.Path('oracle/__pycache__')",
            "pycache.mkdir(exist_ok=True)",
            "(pycache / 'spec.cpython-313.pyc').write_bytes(b'cache')",
            "output.write_text('{}\\n')",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    run_codex_exec(
        codex_parameter(FileAccessMode.READONLY),
        root=root,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )

    assert (root / ".pytest_cache" / "state").read_text() == "temporary\n"
    assert (root / "oracle" / "__pycache__" / "spec.cpython-313.pyc").is_file()


@pytest.mark.parametrize("blocked_dir", [".agents", ".codex", ".git", "memo"])
def test_run_codex_exec_allows_readonly_temporary_cache_under_blocked_root(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, blocked_dir: str
) -> None:
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
            f"pycache = pathlib.Path({blocked_dir!r}) / '__pycache__'",
            "pycache.mkdir(parents=True, exist_ok=True)",
            "(pycache / 'blocked.cpython-313.pyc').write_bytes(b'cache')",
            "output.write_text('{}\\n')",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    run_codex_exec(
        codex_parameter(FileAccessMode.READONLY),
        root=root,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )

    assert (root / blocked_dir / "__pycache__" / "blocked.cpython-313.pyc").is_file()


def test_run_codex_exec_rejects_readonly_realization_diff_after_call(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
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
            "pathlib.Path('src').mkdir(exist_ok=True)",
            "pathlib.Path('src/changed.py').write_text('changed\\n')",
            "output.write_text('{}\\n')",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    with pytest.raises(CmocError, match="禁止差分"):
        run_codex_exec(
            codex_parameter(FileAccessMode.READONLY),
            root=root,
            capacity_initial_sleep_sec=0,
            config=CmocConfig(),
        )

    assert (root / "src" / "changed.py").read_text() == "changed\n"


def test_run_codex_exec_profile_does_not_open_agents_tree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, os, pathlib, sys, tomllib",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "profile = args[args.index('--profile') + 1]",
            "home = pathlib.Path(os.environ['CODEX_HOME'])",
            "profile_path = home / f'{profile}.config.toml'",
            "roots = tomllib.loads(profile_path.read_text())",
            "roots = roots['sandbox_workspace_write']['writable_roots']",
            "agents = pathlib.Path('.agents').resolve()",
            "assert not any(agents.is_relative_to(pathlib.Path(root)) for root in roots)",
            "output.write_text(json.dumps({'ok': True}))",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    run_codex_exec(
        codex_parameter(),
        root=root,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )

    profile_path = next(tmp_path.glob("codex_home/cmoc_*.config.toml"))
    writable_roots = tomllib.loads(profile_path.read_text())["sandbox_workspace_write"][
        "writable_roots"
    ]
    agents = (root / ".agents").resolve()
    assert not any(agents.is_relative_to(Path(path)) for path in writable_roots)


def test_run_codex_exec_allows_agent_created_cmoc_log_diff(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    (root / ".gitignore").write_text("/.cmoc/local/\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "commit", "-m", "ignore cmoc")
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, pathlib, sys",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "agent_log = pathlib.Path('.cmoc/local/log/codex/agent-created.txt')",
            "agent_log.parent.mkdir(parents=True, exist_ok=True)",
            "agent_log.write_text('agent\\n')",
            "output.write_text('{}\\n')",
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

    assert (root / ".cmoc" / "local" / "log" / "codex" / "agent-created.txt").read_text() == (
        "agent\n"
    )


def test_run_codex_exec_allows_agent_modified_previous_cmoc_log_diff(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    counter = tmp_path / "count.txt"
    previous_log_ref = tmp_path / "previous_log.txt"
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, pathlib, sys",
            f"counter = pathlib.Path({str(counter)!r})",
            f"previous_log_ref = pathlib.Path({str(previous_log_ref)!r})",
            "count = int(counter.read_text()) if counter.exists() else 0",
            "counter.write_text(str(count + 1))",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "if count >= 1:",
            "    pathlib.Path(previous_log_ref.read_text()).write_text('agent\\n')",
            "output.write_text('{}\\n')",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    first_result = run_codex_exec(
        codex_parameter(FileAccessMode.REPO_WRITE),
        root=root,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )
    previous_log_ref.write_text(str(first_result.call_log_path))

    run_codex_exec(
        codex_parameter(FileAccessMode.REPO_WRITE),
        root=root,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )

    assert first_result.call_log_path.read_text() == "agent\n"


@pytest.mark.parametrize(
    ("blocked_dir", "mode"),
    [
        (".agents", FileAccessMode.READONLY),
        ("memo", FileAccessMode.REPO_WRITE),
    ],
)
def test_run_codex_exec_allows_empty_blocked_runtime_dir_after_call(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    blocked_dir: str,
    mode: FileAccessMode,
) -> None:
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
            "output.write_text(json.dumps({'ok': True}))",
            f"pathlib.Path({blocked_dir!r}).mkdir(exist_ok=True)",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    run_codex_exec(
        codex_parameter(mode),
        root=root,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )

    assert (root / blocked_dir).is_dir()
    assert not any((root / blocked_dir).iterdir())


def test_run_codex_exec_allows_repo_write_blocked_diffs_after_call(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    (root / ".gitignore").write_text("memo/\n")
    run_git(root, "add", ".gitignore")
    run_git(root, "commit", "-m", "ignore memo")
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, pathlib, sys",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "output.write_text(json.dumps({'ok': True}))",
            "pathlib.Path('memo').mkdir(exist_ok=True)",
            "pathlib.Path('memo/blocked.md').write_text('blocked\\n')",
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

    assert (root / "memo" / "blocked.md").read_text() == "blocked\n"
