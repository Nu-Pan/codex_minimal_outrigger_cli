"""Codex home の起動前検査を検証する。

正常時の既定 home は test_codex_runtime_exec.py、相対 home と cwd は
test_codex_runtime_paths.py の Fake CLI 起動にまとめる。
"""

from collections.abc import Callable
from pathlib import Path

import pytest
from oracle.other import path_model as path_model_module

import commons.runtime_codex_exec as runtime_codex_exec
from basic.acp import AgentCallParameter, FileAccessMode
from cmoc_runtime import CmocError
from commons.runtime_codex import run_codex_exec, run_codex_tui
from commons.runtime_codex_profile import validate_codex_home
from config.cmoc_config import CmocConfig


@pytest.fixture
def codex_call_directory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """home 検証では Git discovery を解決済みとして扱う。"""
    # Git/cwd の結合は test_codex_runtime_paths.py と test_basic_runtime.py に残す。
    root = tmp_path / "repo"
    root.mkdir()
    monkeypatch.setattr(
        path_model_module,
        "_resolve_git_worktree_roots",
        lambda _start_path=None: (root, root),
    )
    return root


# {{work-root}}/oracle/doc/app_spec/codex_exec_rule.md
def _spy_codex_startup(
    monkeypatch: pytest.MonkeyPatch,
) -> list[tuple[tuple[object, ...], dict[str, object]]]:
    """exec・TUI・version probe の起動境界を、実行せず記録する。"""
    calls: list[tuple[tuple[object, ...], dict[str, object]]] = []

    def record_call(*args: object, **kwargs: object) -> None:
        """Codex subprocess invocation を起動せずに記録する。"""
        calls.append((args, kwargs))

    monkeypatch.setattr(runtime_codex_exec, "run_codex_subprocess", record_call)
    return calls


@pytest.mark.parametrize(
    "codex_runner", [run_codex_exec, run_codex_tui], ids=["exec", "tui"]
)
@pytest.mark.parametrize(
    ("codex_home_is_file", "summary", "next_action"),
    [
        pytest.param(
            False,
            "Codex home が存在しません。",
            "Codex CLI の通常利用環境を初期化してください。",
            id="missing",
        ),
        pytest.param(
            True,
            "Codex home がディレクトリではありません。",
            "CODEX_HOME のファイル種別を確認してください。",
            id="file",
        ),
    ],
)
def test_invalid_codex_home_fails_before_startup_and_log_preparation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    codex_call_directory: Path,
    codex_runner: Callable[..., object],
    codex_home_is_file: bool,
    summary: str,
    next_action: str,
) -> None:
    """欠落・通常 file の home を、Codex 起動と採番・log 作成より前に拒否する。"""
    root = codex_call_directory
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    codex_calls = _spy_codex_startup(monkeypatch)
    codex_home = tmp_path / "codex_home"
    if codex_home_is_file:
        codex_home.write_text("not a directory\n")
    monkeypatch.setenv("CODEX_HOME", str(codex_home))
    parameter = AgentCallParameter(
        "build_feedback_normalize_issue_parameter",
        FileAccessMode.READONLY,
        "prompt",
        None,
        root,
    )

    with pytest.raises(CmocError) as caught:
        codex_runner(parameter, root=root, config=CmocConfig())

    error = caught.value
    assert error.summary == summary
    assert str(codex_home) in error.detail
    assert next_action in error.next_actions
    assert codex_calls == []
    assert list(root.iterdir()) == []


@pytest.mark.parametrize("auth_json_is_directory", [False, True])
def test_codex_home_validation_does_not_assume_provider_auth_schema(
    tmp_path: Path,
    auth_json_is_directory: bool,
) -> None:
    """auth.json の欠落・種別を model provider 非依存の preflight に含めない。"""
    codex_home = tmp_path / "codex_home"
    codex_home.mkdir()
    auth_path = codex_home / "auth.json"
    if auth_json_is_directory:
        auth_path.mkdir()

    validate_codex_home(codex_home)
