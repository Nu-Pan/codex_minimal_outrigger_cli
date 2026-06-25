from _support import (
    AgentCallParameter,
    CmocError,
    FileAccessMode,
    ModelClass,
    Path,
    ReasoningEffort,
    json,
    make_repo,
)
from commons.runtime_codex import run_codex_exec

def test_run_codex_exec_uses_default_codex_home_when_env_unset(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    home = tmp_path / "home"
    codex_home = home / ".codex"
    codex_home.mkdir(parents=True)
    (codex_home / "auth.json").write_text("{}\n")
    monkeypatch.delenv("CODEX_HOME", raising=False)
    monkeypatch.setattr(Path, "home", lambda: home)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "record.json"
    fake_codex = bin_dir / "codex"
    fake_codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
                "import json, os, pathlib",
                f"record = pathlib.Path({str(recorder)!r})",
                "args = __import__('sys').argv[1:]",
                "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
                "output.write_text('done\\n')",
                "record.write_text(json.dumps({'codex_home': os.environ.get('CODEX_HOME'), 'args': args}))",
                "print(json.dumps({'type': 'turn.completed'}))",
            ]
        )
        + "\n"
    )
    fake_codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )

    result = run_codex_exec(parameter, root=root, capacity_initial_sleep_sec=0)

    recorded = json.loads(recorder.read_text())
    assert recorded["codex_home"] == str(codex_home)
    assert recorded["args"][2] == result.profile_name
    assert result.codex_home == codex_home
    assert result.profile_path.parent == codex_home


def test_run_codex_exec_preserves_configured_codex_home_env_value(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    codex_home = root / "relative_codex_home"
    codex_home.mkdir()
    (codex_home / "auth.json").write_text("{}\n")
    monkeypatch.setenv("CODEX_HOME", "relative_codex_home")
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    recorder = tmp_path / "record.json"
    fake_codex = bin_dir / "codex"
    fake_codex.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
                "import json, os, pathlib",
                f"record = pathlib.Path({str(recorder)!r})",
                "args = __import__('sys').argv[1:]",
                "output = pathlib.Path(args[args.index('--output-last-message') + 1])",
                "output.write_text('done\\n')",
                "record.write_text(json.dumps({'codex_home': os.environ.get('CODEX_HOME'), 'args': args}))",
                "print(json.dumps({'type': 'turn.completed'}))",
            ]
        )
        + "\n"
    )
    fake_codex.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}:{Path('/usr/bin')}")
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )

    result = run_codex_exec(parameter, root=root, capacity_initial_sleep_sec=0)

    recorded = json.loads(recorder.read_text())
    assert recorded["codex_home"] == "relative_codex_home"
    assert result.codex_home == codex_home
    assert result.profile_path.parent == codex_home
    call_log = json.loads(result.call_log_path.read_text())
    assert call_log["codex_home"] == str(codex_home)


def test_run_codex_exec_fails_before_codex_when_codex_home_missing(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
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
        run_codex_exec(parameter, root=root, capacity_initial_sleep_sec=0)
    except CmocError as exc:
        error = exc
    else:
        raise AssertionError("run_codex_exec should fail before invoking Codex CLI")

    assert error.summary == "Codex home が存在しません。"
    assert str(missing_home) in error.detail
    assert "Codex CLI の通常利用環境を初期化してください。" in error.next_actions


def test_run_codex_exec_fails_before_codex_when_codex_home_is_file(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
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
        run_codex_exec(parameter, root=root, capacity_initial_sleep_sec=0)
    except CmocError as exc:
        error = exc
    else:
        raise AssertionError("run_codex_exec should fail before invoking Codex CLI")

    assert error.summary == "Codex home がディレクトリではありません。"
    assert str(codex_home) in error.detail
    assert "CODEX_HOME のファイル種別を確認してください。" in error.next_actions


def test_run_codex_exec_fails_before_codex_when_auth_json_missing(
    tmp_path: Path, monkeypatch
) -> None:
    root = make_repo(tmp_path)
    codex_home = tmp_path / "codex_home"
    codex_home.mkdir()
    monkeypatch.setenv("CODEX_HOME", str(codex_home))
    parameter = AgentCallParameter(
        ModelClass.EFFICIENCY,
        ReasoningEffort.LOW,
        FileAccessMode.READONLY,
        "prompt",
        None,
    )

    try:
        run_codex_exec(parameter, root=root, capacity_initial_sleep_sec=0)
    except CmocError as exc:
        error = exc
    else:
        raise AssertionError("run_codex_exec should fail before invoking Codex CLI")

    assert error.summary == "Codex CLI 認証情報が存在しません。"
    assert str(codex_home / "auth.json") in error.detail
    assert "既存の Codex home を指すように CODEX_HOME を設定してください。" in error.next_actions
