import json
from pathlib import Path

from basic.acp import AgentCallParameter, FileAccessMode, ModelClass, ReasoningEffort
from cmoc_runtime import CmocError
from config.cmoc_config import CmocConfig
import pytest

from _codex_support import stub_codex_overrides
from _command_support import write_python_executable
from _git_support import make_repo
from commons.runtime_codex import run_codex_exec
import commons.runtime_codex_exec as runtime_codex_exec


# <work-root>/oracle/doc/app_spec/codex_exec_rule.md
def _spy_codex_subprocess(
    monkeypatch: pytest.MonkeyPatch,
) -> list[tuple[tuple[object, ...], dict[str, object]]]:
    """Record Codex subprocess calls so preflight failures prove zero starts."""
    calls: list[tuple[tuple[object, ...], dict[str, object]]] = []

    def record_call(*args: object, **kwargs: object) -> None:
        """Record a Codex subprocess invocation without starting it."""
        calls.append((args, kwargs))

    monkeypatch.setattr(runtime_codex_exec, "run_codex_subprocess", record_call)
    return calls


def test_run_codex_exec_uses_default_codex_home_when_env_unset(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Uses the default home and passes it to the Codex subprocess."""
    root = make_repo(tmp_path)
    home = tmp_path / "home"
    codex_home = home / ".codex"
    codex_home.mkdir(parents=True)
    (codex_home / "auth.json").write_text("{}\n")
    monkeypatch.delenv("CODEX_HOME", raising=False)
    monkeypatch.setattr(Path, "home", lambda: home)
    stub_codex_overrides(monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "record.json"
    fake_codex = bin_dir / "codex"
    write_python_executable(
        fake_codex,
        [
            "import json, os, pathlib",
            f"record = pathlib.Path({str(recorder)!r})",
            "args = __import__('sys').argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "output.write_text('done\\n')",
            "record.write_text(json.dumps({'codex_home': os.environ.get('CODEX_HOME'), 'args': args}))",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )

    result = run_codex_exec(
        parameter, root=root, capacity_initial_sleep_sec=0, config=CmocConfig()
    )

    recorded = json.loads(recorder.read_text())
    assert recorded["codex_home"] == str(codex_home)
    assert result.codex_home == codex_home


def test_run_codex_exec_preserves_configured_codex_home_env_value(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Preserves a configured home value and records its resolved path."""
    root = make_repo(tmp_path)
    codex_home = root / "relative_codex_home"
    codex_home.mkdir()
    (codex_home / "auth.json").write_text("{}\n")
    monkeypatch.setenv("CODEX_HOME", "relative_codex_home")
    stub_codex_overrides(monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "record.json"
    fake_codex = bin_dir / "codex"
    write_python_executable(
        fake_codex,
        [
            "import json, os, pathlib",
            f"record = pathlib.Path({str(recorder)!r})",
            "args = __import__('sys').argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "output.write_text('done\\n')",
            "record.write_text(json.dumps({'codex_home': os.environ.get('CODEX_HOME'), 'args': args}))",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )

    result = run_codex_exec(
        parameter, root=root, capacity_initial_sleep_sec=0, config=CmocConfig()
    )

    recorded = json.loads(recorder.read_text())
    assert recorded["codex_home"] == "relative_codex_home"
    assert result.codex_home == codex_home
    call_log = json.loads(result.call_log_path.read_text())
    assert call_log["codex_home"] == str(codex_home)


def test_run_codex_exec_validates_relative_codex_home_from_codex_cwd(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Resolves a relative home from the Codex subprocess working directory."""
    root = make_repo(tmp_path)
    codex_home = root / "relative_codex_home"
    codex_home.mkdir()
    (codex_home / "auth.json").write_text("{}\n")
    monkeypatch.setenv("CODEX_HOME", "relative_codex_home")
    stub_codex_overrides(monkeypatch)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "record.json"
    fake_codex = bin_dir / "codex"
    write_python_executable(
        fake_codex,
        [
            "import json, os, pathlib",
            f"record = pathlib.Path({str(recorder)!r})",
            "args = __import__('sys').argv[1:]",
            "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
            "output.write_text('done\\n')",
            "home = pathlib.Path(os.environ['CODEX_HOME'])",
            "record.write_text(json.dumps({",
            "    'codex_home': os.environ['CODEX_HOME'],",
            "    'resolved_home': str(home.resolve()),",
            "    'cwd': os.getcwd(),",
            "}))",
            "print(json.dumps({'type': 'turn.completed'}))",
        ],
    )
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.PURE_ORACLE_READ,
        "prompt",
        None,
    )

    result = run_codex_exec(
        parameter, root=root, capacity_initial_sleep_sec=0, config=CmocConfig()
    )

    recorded = json.loads(recorder.read_text())
    assert recorded["codex_home"] == "relative_codex_home"
    assert Path(recorded["cwd"]) == root
    assert Path(recorded["resolved_home"]) == codex_home
    assert result.codex_home == codex_home


def test_run_codex_exec_fails_before_codex_when_codex_home_missing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Rejects a missing home before starting the Codex subprocess."""
    root = make_repo(tmp_path)
    codex_calls = _spy_codex_subprocess(monkeypatch)
    missing_home = tmp_path / "missing_codex_home"
    monkeypatch.setenv("CODEX_HOME", str(missing_home))
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )

    try:
        run_codex_exec(
            parameter, root=root, capacity_initial_sleep_sec=0, config=CmocConfig()
        )
    except CmocError as exc:
        error = exc
    else:
        raise AssertionError("run_codex_exec should fail before invoking Codex CLI")

    assert error.summary == "Codex home が存在しません。"
    assert str(missing_home) in error.detail
    assert "Codex CLI の通常利用環境を初期化してください。" in error.next_actions
    assert codex_calls == []


def test_run_codex_exec_fails_before_codex_when_codex_home_is_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Rejects a file-valued home before starting the Codex subprocess."""
    root = make_repo(tmp_path)
    codex_calls = _spy_codex_subprocess(monkeypatch)
    codex_home = tmp_path / "codex_home_file"
    codex_home.write_text("not a directory\n")
    monkeypatch.setenv("CODEX_HOME", str(codex_home))
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )

    try:
        run_codex_exec(
            parameter, root=root, capacity_initial_sleep_sec=0, config=CmocConfig()
        )
    except CmocError as exc:
        error = exc
    else:
        raise AssertionError("run_codex_exec should fail before invoking Codex CLI")

    assert error.summary == "Codex home がディレクトリではありません。"
    assert str(codex_home) in error.detail
    assert "CODEX_HOME のファイル種別を確認してください。" in error.next_actions
    assert codex_calls == []


@pytest.mark.parametrize("auth_json_is_directory", [False, True])
def test_run_codex_exec_fails_before_codex_when_auth_json_is_not_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    auth_json_is_directory: bool,
) -> None:
    """Rejects missing or non-file auth.json before starting Codex."""
    root = make_repo(tmp_path)
    codex_home = tmp_path / "codex_home"
    codex_home.mkdir()
    auth_path = codex_home / "auth.json"
    if auth_json_is_directory:
        auth_path.mkdir()
    monkeypatch.setenv("CODEX_HOME", str(codex_home))
    codex_calls = _spy_codex_subprocess(monkeypatch)
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )

    try:
        run_codex_exec(
            parameter, root=root, capacity_initial_sleep_sec=0, config=CmocConfig()
        )
    except CmocError as exc:
        error = exc
    else:
        raise AssertionError("run_codex_exec should fail before invoking Codex CLI")

    assert codex_calls == []

    assert error.summary == "Codex CLI 認証情報が存在しません。"
    assert str(codex_home / "auth.json") in error.detail
    assert "既存の Codex home を指すように CODEX_HOME を設定してください。" in error.next_actions
