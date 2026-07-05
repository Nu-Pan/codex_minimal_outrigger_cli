import json
from pathlib import Path

import pytest
from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
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


def test_run_codex_exec_does_not_post_validate_file_access_violations(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    (root / "src").mkdir()
    (root / "src" / "app.py").write_text("")
    run_git(root, "add", "src")
    run_git(root, "commit", "-m", "add src")
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
            "blocked = pathlib.Path('oracle/blocked.md')",
            "blocked.write_text('blocked\\n')",
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
    assert (root / "oracle" / "blocked.md").read_text() == "blocked\n"


@pytest.mark.parametrize("blocked_name", ["a b.md", 'quoted " name.md'])
def test_run_codex_exec_does_not_post_validate_quoted_oracle_path_file_access_violations(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, blocked_name: str
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    counter = tmp_path / "count.txt"
    blocked_path = Path("oracle") / blocked_name
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, pathlib, sys",
            f"counter = pathlib.Path({str(counter)!r})",
            f"blocked = pathlib.Path({str(blocked_path)!r})",
            "count = int(counter.read_text()) if counter.exists() else 0",
            "counter.write_text(str(count + 1))",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "blocked.write_text('blocked\\n')",
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
    assert (root / blocked_path).read_text() == "blocked\n"


def test_run_codex_exec_does_not_post_validate_git_directory_file_access_violation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    counter = tmp_path / "count.txt"
    saved_config = tmp_path / "git_config.txt"
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, pathlib, sys",
            f"counter = pathlib.Path({str(counter)!r})",
            f"saved_config = pathlib.Path({str(saved_config)!r})",
            "count = int(counter.read_text()) if counter.exists() else 0",
            "counter.write_text(str(count + 1))",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "config = pathlib.Path('.git/config')",
            "saved_config.write_text(config.read_text())",
            "config.write_text(config.read_text() + '\\n[cmoc-test]\\n\\tvalue = true\\n')",
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

    assert counter.read_text() == "1"
    assert "[cmoc-test]" in (root / ".git" / "config").read_text()


def test_run_codex_exec_does_not_post_validate_file_access_violations_before_nonzero_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
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
            "blocked = pathlib.Path('oracle/blocked.md')",
            "blocked.write_text('blocked\\n')",
            "print(json.dumps({'type': 'error', 'message': 'boom'}))",
            "raise SystemExit(7)",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    with pytest.raises(CmocError, match="Codex CLI 呼び出しが失敗しました"):
        run_codex_exec(
            codex_parameter(FileAccessMode.REALIZATION_WRITE),
            root=root,
            capacity_initial_sleep_sec=0,
            config=CmocConfig(),
        )

    assert counter.read_text() == "1"
    assert (root / "oracle" / "blocked.md").read_text() == "blocked\n"


def test_run_codex_exec_does_not_post_validate_file_access_violations_before_schema_retry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    counter = tmp_path / "count.txt"
    schema = tmp_path / "schema.json"
    schema.write_text(
        json.dumps(
            {
                "type": "object",
                "properties": {"ok": {"type": "boolean"}},
                "required": ["ok"],
                "additionalProperties": False,
            }
        )
    )
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, pathlib, sys",
            f"counter = pathlib.Path({str(counter)!r})",
            "count = int(counter.read_text()) if counter.exists() else 0",
            "counter.write_text(str(count + 1))",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "blocked = pathlib.Path('oracle/blocked.md')",
            "if count == 0:",
            "    blocked.write_text('blocked\\n')",
            "    output.write_text('{}\\n')",
            "else:",
            "    output.write_text(json.dumps({'ok': True}) + '\\n')",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")

    result = run_codex_exec(
        AgentCallParameter(
            ModelClass.EFFICIENCY,
            ReasoningEffort.LOW,
            FileAccessMode.REALIZATION_WRITE,
            "prompt",
            schema,
        ),
        root=root,
        capacity_initial_sleep_sec=0,
        config=CmocConfig(),
    )

    assert counter.read_text() == "2"
    assert (root / "oracle" / "blocked.md").read_text() == "blocked\n"
    assert result.output_json == {"ok": True}


def test_run_codex_exec_allows_root_readme_realization_diff(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
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
            "pathlib.Path('README.md').write_text('# updated\\n')",
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
    assert (root / "README.md").read_text() == "# updated\n"


def test_run_codex_exec_ignores_preexisting_forbidden_diff(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    target = root / "oracle" / "spec.md"
    target.write_text("base\n")
    run_git(root, "add", "oracle/spec.md")
    run_git(root, "commit", "-m", "add oracle spec")
    target.write_text("preexisting\n")
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
    assert target.read_text() == "preexisting\n"


def test_run_codex_exec_leaves_modified_preexisting_forbidden_diff(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    target = root / "oracle" / "spec.md"
    target.write_text("base\n")
    run_git(root, "add", "oracle/spec.md")
    run_git(root, "commit", "-m", "add oracle spec")
    target.write_text("preexisting\n")
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
            "target = pathlib.Path('oracle/spec.md')",
            "if count == 0:",
            "    target.write_text('agent changed\\n')",
            "else:",
            "    target.write_text('preexisting\\n')",
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
    assert target.read_text() == "agent changed\n"


def test_run_codex_exec_does_not_post_validate_session_join_conflict_targets(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = make_repo(tmp_path)
    setup_codex_home(tmp_path, monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    counter = tmp_path / "count.txt"
    target = root / "oracle" / "spec.md"
    other = root / "oracle" / "other.md"
    write_python_executable(
        bin_dir / "codex",
        [
            "import json, pathlib, sys",
            f"counter = pathlib.Path({str(counter)!r})",
            "count = int(counter.read_text()) if counter.exists() else 0",
            "counter.write_text(str(count + 1))",
            "args = sys.argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "if count == 0:",
            "    pathlib.Path('oracle/spec.md').write_text('resolved\\n')",
            "    pathlib.Path('oracle/other.md').write_text('blocked\\n')",
            "else:",
            "    pathlib.Path('oracle/other.md').unlink(missing_ok=True)",
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
        extra_writable_paths=[target],
        allow_oracle_conflict_writes=True,
    )

    assert counter.read_text() == "1"
    assert target.read_text() == "resolved\n"
    assert other.read_text() == "blocked\n"

