"""`cmoc indexing` の CLI、preflight、commit lifecycle を検証する。

CLI の事前条件、doctor、worktree、INDEX.md 更新、Codex 呼び出し、commit 条件を
外部挙動として確認する。仕様根拠は
`{{work-root}}/oracle/doc/app_spec/indexing.md` と
`{{work-root}}/oracle/doc/app_spec/sub_command/indexing.md`。
Structured Output schema の根拠は
`{{work-root}}/oracle/src/oracle/acp_builder/indexing/index_entry.json`。
"""

from collections.abc import Callable, Iterator
from pathlib import Path

import pytest
from _cli_support import runner
from _git_support import make_repo, run_git
from _ollama_support import run_doctor
from oracle.other.cmoc_config import CodexModelSpec

import cmoc_runtime
import commons.indexing as indexing_common
import commons.runtime_codex_preflight as codex_preflight_module
import sub_commands.indexing as indexing_module
from basic.acp import AgentCallParameter, ModelClass
from commons.runtime_results import CommandResult
from main import app


@pytest.fixture(autouse=True)
def reset_indexing_preflight() -> Iterator[None]:
    """各テスト前後に indexing preflight の有効状態を初期化する。"""
    codex_preflight_module.disable_indexing_preflight()
    yield
    codex_preflight_module.disable_indexing_preflight()


def test_indexing_uses_codex_index_entry_builder_and_commits(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Codex 生成結果を INDEX.md に反映し、更新を commit する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    calls: list[str] = []

    class FakeCodexResult:
        """Codex の structured output を返すテスト用 fake。"""

        output_json = {
            "summary": ["generated summary"],
            "read_this_when": ["generated read condition"],
            "do_not_read_this_when": ["generated skip condition"],
        }

    def fake_run_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """固定された INDEX エントリーを返す fake。"""
        calls.append(kwargs["purpose"])
        assert parameter.structured_output_schema_path.name == "index_entry.json"
        return FakeCodexResult()

    monkeypatch.setattr(indexing_module, "run_codex_exec", fake_run_codex_exec)

    result = runner.invoke(app, ["indexing"], catch_exceptions=False)

    assert result.exit_code == 0
    assert calls
    root_index = root / "INDEX.md"
    assert root_index.is_file()
    rendered = root_index.read_text()
    assert "generated summary" in rendered
    assert "generated read condition" in rendered
    assert "generated skip condition" in rendered
    assert run_git(root, "status", "--short").stdout.strip() == ""
    assert "cmoc indexing" in run_git(root, "log", "--oneline", "-1").stdout


def test_indexing_uninitialized_clean_repo_runs_doctor_and_generates_config(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """未初期化の clean repository でも doctor が config を生成して続行する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)

    class FakeCodexResult:
        """index entry用の固定Structured Outputを返すdouble。"""

        output_json = {
            "summary": ["summary"],
            "read_this_when": ["read"],
            "do_not_read_this_when": ["skip"],
        }

    monkeypatch.setattr(
        indexing_module,
        "run_codex_exec",
        lambda parameter, **kwargs: FakeCodexResult(),
    )

    result = runner.invoke(app, ["indexing"], catch_exceptions=False)

    assert result.exit_code == 0
    assert "/.cmoc/gu/" in (root / ".gitignore").read_text()
    assert (root / ".agents" / ".gitkeep").is_file()
    assert (root / ".cmoc" / "gt" / "ar" / "config.json").is_file()
    assert (root / "INDEX.md").is_file()
    assert (root / ".cmoc" / "gu" / "ar" / "log" / "sub_command").is_dir()
    assert run_git(root, "status", "--short").stdout.strip() == ""


def test_indexing_targets_current_linked_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """現在の linked worktree だけを indexing 対象にして commit する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    main_head = run_git(root, "rev-parse", "HEAD").stdout.strip()
    linked = root / ".cmoc" / "gu" / "worktree" / "indexing"
    run_git(root, "worktree", "add", "-b", "linked-indexing", str(linked), "HEAD")

    class FakeCodexResult:
        """Codex の structured output を返すテスト用 fake。"""

        output_json = {
            "summary": ["linked summary"],
            "read_this_when": ["linked read condition"],
            "do_not_read_this_when": ["linked skip condition"],
        }

    def fake_run_codex_exec(
        _parameter: AgentCallParameter, **_kwargs: object
    ) -> FakeCodexResult:
        """linked worktree 用に固定された INDEX エントリーを返す。"""
        return FakeCodexResult()

    monkeypatch.setattr(indexing_module, "run_codex_exec", fake_run_codex_exec)
    monkeypatch.chdir(linked)

    result = runner.invoke(app, ["indexing"], catch_exceptions=False)

    assert result.exit_code == 0
    assert (linked / "INDEX.md").is_file()
    assert not (root / "INDEX.md").exists()
    assert run_git(linked, "log", "-1", "--pretty=%s").stdout.strip() == "cmoc indexing"
    assert run_git(root, "rev-parse", "HEAD").stdout.strip() == main_head
    assert run_git(linked, "status", "--short").stdout.strip() == ""


def test_indexing_rejects_dirty_current_linked_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """dirty linked worktree では INDEX 更新を開始せずに拒否する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    linked = root / ".cmoc" / "gu" / "worktree" / "dirty-indexing"
    run_git(root, "worktree", "add", "-b", "dirty-indexing", str(linked), "HEAD")
    (linked / "README.md").write_text("# repo\n\nlinked change\n")
    head_before = run_git(linked, "rev-parse", "HEAD").stdout.strip()

    def fail_update_indexes(
        update_root: Path, codex_exec: Callable[..., object] | None = None
    ) -> list[Path]:
        """更新へ進んだ場合にテストを失敗させる fake。"""
        raise AssertionError("dirty linked worktree must stop before indexing")

    monkeypatch.setattr(indexing_module, "update_indexes", fail_update_indexes)
    monkeypatch.chdir(linked)

    result = runner.invoke(app, ["indexing"], catch_exceptions=False)

    assert result.exit_code != 0
    assert "git 未コミット差分が存在します。" in result.stdout
    assert run_git(root, "status", "--short").stdout.strip() == ""
    assert run_git(linked, "rev-parse", "HEAD").stdout.strip() == head_before
    assert not (linked / "INDEX.md").exists()
    assert run_git(linked, "status", "--short").stdout == " M README.md\n"


def test_indexing_preflight_in_apply_worktree_uses_worktree_config(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """apply worktree の preflight がその worktree の Codex 設定を使う。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    config = cmoc_runtime.sync_config(root)
    custom_model = CodexModelSpec("codex", "CUSTOM-INDEXING-EFFICIENCY")
    config.codex.model[ModelClass.EFFICIENCY] = custom_model
    cmoc_runtime.write_config(
        root / ".cmoc" / "gt" / "ar" / "config.json",
        config,
    )
    run_git(root, "add", ".cmoc/gt/ar/config.json")
    run_git(root, "commit", "-m", "customize indexing model")
    apply_worktree = root / ".cmoc" / "gu" / "worktree" / "session" / "run"
    run_git(
        root,
        "worktree",
        "add",
        "-b",
        "apply-indexing-config",
        str(apply_worktree),
        "HEAD",
    )
    seen_models: list[CodexModelSpec] = []

    class FakeCodexResult:
        """Codex の structured output を返すテスト用 fake。"""

        output_json = {
            "summary": ["summary"],
            "read_this_when": ["read"],
            "do_not_read_this_when": ["skip"],
        }

    def fake_codex_exec(
        parameter: AgentCallParameter, **kwargs: object
    ) -> FakeCodexResult:
        """Codex 実行へ渡された設定を記録して固定結果を返す fake。"""
        seen_models.append(kwargs["config"].codex.model[ModelClass.EFFICIENCY])
        assert kwargs["root"] == root
        assert kwargs["cwd"] == apply_worktree
        return FakeCodexResult()

    indexing_common.run_indexing_preflight(apply_worktree, fake_codex_exec)

    assert seen_models
    assert set(seen_models) == {custom_model}
    assert (apply_worktree / "INDEX.md").is_file()
    assert (apply_worktree / ".cmoc" / "gt" / "ar" / "config.json").exists()


def test_indexing_skips_codex_when_existing_hashes_are_fresh(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """hash が fresh な INDEX.md の再生成と Codex 呼び出しを省略する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0

    class FakeCodexResult:
        """Codex の structured output を返すテスト用 fake。"""

        output_json = {
            "summary": ["generated summary"],
            "read_this_when": ["generated read condition"],
            "do_not_read_this_when": ["generated skip condition"],
        }

    def fake_run_codex_exec(
        _parameter: AgentCallParameter, **_kwargs: object
    ) -> FakeCodexResult:
        """初回 indexing 用に固定された INDEX エントリーを返す。"""
        return FakeCodexResult()

    monkeypatch.setattr(indexing_module, "run_codex_exec", fake_run_codex_exec)
    first = runner.invoke(app, ["indexing"], catch_exceptions=False)
    assert first.exit_code == 0
    root_index_before = (root / "INDEX.md").read_text()
    head_before = run_git(root, "rev-parse", "HEAD").stdout.strip()

    calls: list[str] = []

    def fail_if_called(parameter: AgentCallParameter, **kwargs: object) -> None:
        """呼び出されるべきでない Codex 実行を検出する fake。"""
        calls.append(kwargs["purpose"])
        raise AssertionError("fresh INDEX.md should not require Codex")

    monkeypatch.setattr(indexing_module, "run_codex_exec", fail_if_called)
    second = runner.invoke(app, ["indexing"], catch_exceptions=False)

    assert second.exit_code == 0
    assert calls == []
    assert (root / "INDEX.md").read_text() == root_index_before
    assert run_git(root, "rev-parse", "HEAD").stdout.strip() == head_before
    assert run_git(root, "status", "--short").stdout.strip() == ""


def test_commit_index_updates_commits_only_index_paths(tmp_path: Path) -> None:
    """INDEX 更新の commit に INDEX.md 以外を含めない。"""
    root = make_repo(tmp_path)
    index_path = root / "INDEX.md"
    index_path.write_text("# generated\n")
    (root / ".gitignore").write_text("/.cmoc/gu/\n")

    indexing_common.commit_index_updates(root, [index_path])

    committed_paths = run_git(
        root, "show", "--name-only", "--pretty=", "HEAD"
    ).stdout.strip()
    assert committed_paths == "INDEX.md"
    assert run_git(root, "status", "--short").stdout.strip() == "?? .gitignore"


def test_commit_index_updates_rejects_git_diff_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """git diff の異常終了を成功扱いしない。

    根拠: {{work-root}}/oracle/doc/app_spec/indexing.md
    """
    root = make_repo(tmp_path)
    calls: list[tuple[list[str], bool]] = []

    def fake_run_git(args: list[str], cwd: Path, check: bool = True) -> CommandResult:
        """index commitのGit結果を固定し、diff失敗を再現する。"""
        calls.append((args, check))
        if args[0] == "add":
            return CommandResult(0, "", "")
        return CommandResult(2, "", "fatal: diff failed")

    monkeypatch.setattr(indexing_common, "run_git", fake_run_git)

    with pytest.raises(
        cmoc_runtime.CmocError, match="INDEX.md 差分の確認に失敗しました"
    ):
        indexing_common.commit_index_updates(root, [root / "INDEX.md"])

    assert calls == [
        (["add", "--", "INDEX.md"], True),
        (["diff", "--cached", "--quiet", "--", "INDEX.md"], False),
    ]


def test_indexing_rejects_existing_non_index_diff_without_index_commit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """既存の非 INDEX 差分がある通常 indexing を開始前に拒否する。"""
    root = make_repo(tmp_path)
    monkeypatch.chdir(root)
    assert run_doctor(root).exit_code == 0
    (root / "README.md").write_text("# repo\n\nchanged\n")
    head_before = run_git(root, "rev-parse", "HEAD").stdout.strip()
    calls: list[Path] = []

    def fake_update_indexes(
        update_root: Path, codex_exec: Callable[..., object] | None = None
    ) -> list[Path]:
        """INDEX.md の更新結果を固定する fake。"""
        calls.append(update_root)
        raise AssertionError("dirty cmoc indexing must stop before updating INDEX.md")

    monkeypatch.setattr(indexing_common, "update_indexes", fake_update_indexes)

    result = runner.invoke(app, ["indexing"], catch_exceptions=False)

    assert result.exit_code != 0
    assert "git 未コミット差分が存在します。" in result.stdout
    assert "git 未コミット差分が存在します。" not in result.stderr
    assert calls == []
    assert run_git(root, "rev-parse", "HEAD").stdout.strip() == head_before
    assert not (root / "INDEX.md").exists()
    assert run_git(root, "status", "--short").stdout == " M README.md\n"


def test_indexing_preflight_allows_existing_non_index_diff_and_commits_only_index(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """preflight が既存差分を保持しつつ INDEX.md だけを commit する。"""
    root = make_repo(tmp_path)
    index_path = root / "INDEX.md"
    (root / "README.md").write_text("# repo\n\nchanged\n")

    def fake_update_indexes(
        update_root: Path, codex_exec: Callable[..., object] | None = None
    ) -> list[Path]:
        """INDEX.md の更新結果を固定する fake。"""
        assert update_root == root
        index_path.write_text("# generated\n")
        return [index_path]

    monkeypatch.setattr(indexing_common, "update_indexes", fake_update_indexes)

    def fake_codex_exec(_parameter: AgentCallParameter, **_kwargs: object) -> None:
        """INDEX 更新では呼び出されない Codex callback の fake。"""

    indexing_common.run_indexing_preflight(root, fake_codex_exec)

    committed_paths = run_git(
        root, "show", "--name-only", "--pretty=", "HEAD"
    ).stdout.splitlines()
    assert committed_paths == ["INDEX.md"]
    assert run_git(root, "status", "--short").stdout == " M README.md\n"
