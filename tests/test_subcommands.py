"""サブコマンド本体の決定論的な制御ロジックのテスト。"""

import inspect
import subprocess
import sys
from pathlib import Path

import pytest
from pytest import MonkeyPatch

from commons.errors import CmocError
from sub_commands.apply import cmoc_apply_impl
from sub_commands.apply import _DISCREPANCY_OUTPUT_SCHEMA
from sub_commands.apply import _commit_all_changes
from sub_commands.apply import _validate_discrepancy_payload
from sub_commands.branch import cmoc_branch_impl
from sub_commands.eval_oracles import cmoc_eval_oracles_impl
from sub_commands.eval_oracles import _evaluation_prompt
from sub_commands.init import cmoc_init_impl
from sub_commands.merge import cmoc_merge_impl
from sub_commands.merge import _conflict_prompt
from sub_commands.merge import _files_with_conflict_markers


def test_init_adds_cmoc_ignore_and_commits_it(tmp_path: Path) -> None:
    """`cmoc init` は `.cmoc` ignore ルールを commit する。"""
    repo = _init_repo(tmp_path)

    cmoc_init_impl(repo)

    assert ".cmoc" in (repo / ".gitignore").read_text(encoding="utf-8")
    assert _git(repo, "status", "--porcelain").stdout == ""
    assert (
        _git(repo, "log", "-1", "--pretty=%s").stdout.strip()
        == "Initialize cmoc"
    )


def test_init_untracks_existing_cmoc_file_and_commits_it(
    tmp_path: Path,
) -> None:
    """`cmoc init` は tracked `.cmoc` ファイルの追跡解除も commit する。"""
    repo = _init_repo(tmp_path)
    cmoc_file = repo / ".cmoc" / "logs" / "tracked.log"
    cmoc_file.parent.mkdir(parents=True)
    cmoc_file.write_text("tracked\n", encoding="utf-8")
    _git(repo, "add", "-f", ".cmoc/logs/tracked.log")
    _git(repo, "commit", "-m", "track cmoc")

    cmoc_init_impl(repo)

    assert _git(repo, "ls-files", "--", ".cmoc").stdout == ""
    assert cmoc_file.exists()
    assert _git(repo, "status", "--porcelain").stdout == ""
    last_commit_paths = _git(
        repo,
        "show",
        "--name-only",
        "--pretty=format:",
        "HEAD",
    ).stdout
    assert ".gitignore" in last_commit_paths
    assert ".cmoc/logs/tracked.log" in last_commit_paths


def test_init_allows_existing_gitignore_changes(tmp_path: Path) -> None:
    """`cmoc init` は `.gitignore` 差分を追加の事前条件にしない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("user-rule\n", encoding="utf-8")

    cmoc_init_impl(repo)

    assert "/.cmoc/" in (repo / ".gitignore").read_text(encoding="utf-8")
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == (
        "Initialize cmoc"
    )


def test_branch_creates_cmoc_branch_and_records_base_commit(
    tmp_path: Path,
) -> None:
    """`cmoc branch` は branch 作成と base commit 記録を行う。"""
    repo = _init_repo(tmp_path)
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    cmoc_branch_impl(repo)

    branch_name = _git(repo, "branch", "--show-current").stdout.strip()
    record_path = repo / ".cmoc" / "branch" / f"{branch_name}.txt"
    assert branch_name.startswith("cmoc_")
    assert record_path.read_text(encoding="utf-8").strip() == base_commit


def test_eval_oracles_writes_report_with_fake_codex(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """`cmoc eval-oracles --full` は oracle 評価レポートを保存する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")

    monkeypatch.setattr(
        "sub_commands.eval_oracles.maintain_indexes",
        lambda repo_root: False,
    )
    monkeypatch.setattr(
        "sub_commands.eval_oracles.run_codex_exec",
        lambda *args, **kwargs: "no fatal problems",
    )

    cmoc_eval_oracles_impl(repo, full=True)

    reports = list((repo / ".cmoc" / "reports" / "eval-oracles").glob("*.md"))
    assert len(reports) == 1
    assert "mode: full" in reports[0].read_text(encoding="utf-8")
    assert "no fatal problems" in reports[0].read_text(encoding="utf-8")


def test_eval_oracles_body_uses_pep8_module_name() -> None:
    """`eval-oracles` の本体は import 可能な underscore module に置く。"""
    repo_root = Path(__file__).resolve().parents[1]

    body = repo_root / "src" / "sub_commands" / "eval-oracles.py"
    module = repo_root / "src" / "sub_commands" / "eval_oracles.py"
    assert not body.exists()
    assert "def cmoc_eval_oracles_impl" in module.read_text(encoding="utf-8")


def test_eval_oracles_prompt_forbids_implementation_references() -> None:
    """評価 prompt は仕様だけから致命的問題を判断させる。"""
    prompt = _evaluation_prompt(Path("/repo"), Path("/repo/oracles/spec.md"))

    assert "実装・テスト・設定ファイルは参照禁止です。" in prompt
    assert "仕様だけから判断・実装したとき" in prompt


def test_apply_returns_complete_when_no_discrepancies(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """`cmoc apply` は不整合なし JSON で完了扱いのレポートを保存する。"""
    repo = _init_repo(tmp_path)
    _git(repo, "checkout", "-b", "cmoc_2026-05-10_22-21_10_123")
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")

    monkeypatch.setattr(
        "sub_commands.apply.maintain_indexes",
        lambda repo_root: False,
    )
    codex_kwargs: list[dict[str, object]] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査なら不整合なし JSON、レポートなら Markdown を返す。"""
        codex_kwargs.append(kwargs)
        if kwargs.get("expect_json") is True:
            return '{"discrepancies": []}'
        return "complete report"

    monkeypatch.setattr("sub_commands.apply.run_codex_exec", fake_codex)

    exit_code = cmoc_apply_impl(repo)

    reports = list((repo / ".cmoc" / "reports" / "apply").glob("*.md"))
    assert exit_code == 0
    assert len(reports) == 1
    assert reports[0].read_text(encoding="utf-8") == "complete report"
    assert codex_kwargs[0]["output_schema"] == _DISCREPANCY_OUTPUT_SCHEMA


def test_apply_uses_repeat_option_for_loop_limit(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """`cmoc apply` は指定 repeat 回数をループ上限と表示に使う。"""
    repo = _init_repo(tmp_path)
    _git(repo, "checkout", "-b", "cmoc_2026-05-10_22-21_10_123")
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "oracle")

    monkeypatch.setattr(
        "sub_commands.apply.maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """常に不整合を返し、指定回数で incomplete になることを見やすくする。"""
        if kwargs.get("expect_json") is True:
            return (
                '{"discrepancies": [{"oracle_path": "/repo/oracles/spec.md", '
                '"oracle_line_start": 1, "oracle_line_end": 1, '
                '"implementation_paths": [], "title": "t", '
                '"oracle_requirement": "r", "observed_implementation": "o", '
                '"reason": "x", "suggested_fix": "f"}]}'
            )
        return "incomplete report"

    monkeypatch.setattr("sub_commands.apply.run_codex_exec", fake_codex)

    exit_code = cmoc_apply_impl(repo, repeat=2)

    assert exit_code == 2
    assert (
        "implementation loop (2/2) discrepancies: 1"
        in capsys.readouterr().out
    )


def test_apply_rejects_non_cmoc_branch(tmp_path: Path) -> None:
    """`cmoc apply` は cmoc ブランチ外では仕様通り CmocError にする。"""
    repo = _init_repo(tmp_path)

    with pytest.raises(CmocError) as error:
        cmoc_apply_impl(repo)

    assert "cmoc apply must be run on a cmoc branch." in error.value.message


def test_apply_rejects_non_oracle_changes_before_cmoc_guarantee(
    tmp_path: Path,
) -> None:
    """`cmoc apply` はユーザー由来の oracle 外差分を先に拒否する。"""
    repo = _init_repo(tmp_path)
    _git(repo, "checkout", "-b", "cmoc_2026-05-10_22-21_10_123")
    (repo / "app.py").write_text("changed\n", encoding="utf-8")

    with pytest.raises(CmocError):
        cmoc_apply_impl(repo)

    assert not (repo / ".gitignore").exists()


def test_apply_commits_cmoc_guarantee_before_oracle_changes(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """`cmoc apply` は `.cmoc` 保証差分を oracle commit 前に処理する。"""
    repo = _init_repo(tmp_path)
    _git(repo, "checkout", "-b", "cmoc_2026-05-10_22-21_10_123")
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")

    monkeypatch.setattr(
        "sub_commands.apply.maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査なら不整合なし JSON、レポートなら Markdown を返す。"""
        if kwargs.get("expect_json") is True:
            return '{"discrepancies": []}'
        return "complete report"

    monkeypatch.setattr("sub_commands.apply.run_codex_exec", fake_codex)

    assert cmoc_apply_impl(repo) == 0

    commit_subjects = _git(
        repo,
        "log",
        "--pretty=%s",
        "-3",
    ).stdout.splitlines()
    assert commit_subjects[:2] == [
        "Update oracle files",
        "Ensure cmoc directory is ignored",
    ]
    assert _git(repo, "status", "--porcelain", "--", "oracles").stdout == ""


def test_commit_all_changes_rechecks_forbidden_paths_after_index_update(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """INDEX メンテナンス後に禁止領域差分が出た場合は commit 前に止める。"""
    repo = _init_repo(tmp_path)
    (repo / "app.py").write_text("changed\n", encoding="utf-8")

    def fake_maintain_indexes(repo_root: Path) -> bool:
        """INDEX メンテナンス時に禁止領域差分を作る fake。"""
        oracle_index = repo_root / "oracles" / "INDEX.md"
        oracle_index.parent.mkdir()
        oracle_index.write_text("forbidden\n", encoding="utf-8")
        return True

    monkeypatch.setattr(
        "sub_commands.apply.maintain_indexes",
        fake_maintain_indexes,
    )

    with pytest.raises(CmocError):
        _commit_all_changes(repo)

    assert _git(repo, "status", "--porcelain").stdout


def test_apply_discrepancy_schema_rejects_incomplete_items() -> None:
    """不整合調査 JSON は仕様 schema の必須項目不足を意味的失敗として扱う。"""
    with pytest.raises(ValueError):
        _validate_discrepancy_payload(
            {
                "discrepancies": [
                    {
                        "oracle_path": "/repo/oracles/spec.md",
                        "title": "missing fields",
                    }
                ]
            }
        )


def test_apply_discrepancy_schema_rejects_near_miss_keys() -> None:
    """似た名前のキーでも不整合調査 schema と一致しなければ拒否する。"""
    with pytest.raises(ValueError):
        _validate_discrepancy_payload(
            {
                "discrepancies": [
                    {
                        "oracle_path": "/repo/oracles/spec.md",
                        "oracle_lines": "10-12",
                        "implementation_paths": ["/repo/src/app.py"],
                        "title": "near miss",
                        "expected_by_oracle": "requirement",
                        "observed_implementation": "observed",
                        "reason": "reason",
                        "suggested_fix": "fix",
                    }
                ]
            }
        )


def test_merge_merges_explicit_cmoc_branch_and_deletes_it(
    tmp_path: Path,
) -> None:
    """`cmoc merge <branch>` は clean tree で merge し、安全なら branch を消す。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")
    target_branch = _git(repo, "branch", "--show-current").stdout.strip()
    _git(repo, "checkout", "-b", "cmoc_2026-05-10_22-21_10_123")
    (repo / "feature.txt").write_text("feature\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "feature")
    _git(repo, "checkout", target_branch)

    cmoc_merge_impl(repo, "cmoc_2026-05-10_22-21_10_123")

    branches = _git(
        repo,
        "branch",
        "--format=%(refname:short)",
    ).stdout.splitlines()
    assert (repo / "feature.txt").read_text(encoding="utf-8") == "feature\n"
    assert "cmoc_2026-05-10_22-21_10_123" not in branches


def test_merge_auto_resolve_failure_does_not_print_manual_resolution(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """merge 開始前の自動解決失敗では merge state 手動解決を案内しない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("/.cmoc/\n", encoding="utf-8")
    _git(repo, "add", ".gitignore")
    _git(repo, "commit", "-m", "ignore cmoc")

    with pytest.raises(CmocError):
        cmoc_merge_impl(repo, None)

    captured = capsys.readouterr()
    assert "Manual resolution is required" not in captured.err


def test_main_typer_functions_delegate_only_to_impls() -> None:
    """Typer 対応関数は共通 runner ではなく対応する impl 呼び出しだけを持つ。"""
    import main

    source = inspect.getsource(main)

    assert "def _run_command" not in source
    assert "_run_command(" not in source
    assert "cmoc_init_impl()" in source
    assert "cmoc_branch_impl()" in source
    assert "cmoc_eval_oracles_impl(full=full)" in source
    assert "cmoc_apply_impl(repeat=repeat)" in source
    assert "cmoc_merge_impl(cmoc_branch=cmoc_branch)" in source


def test_cmoc_help_uses_cmoc_command_name() -> None:
    """PATH 経由の `cmoc --help` は Usage に cmoc を表示する。"""
    repo_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "-m", "main", "--help"],
        cwd=repo_root,
        env={"PYTHONPATH": str(repo_root / "src")},
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert "Usage: cmoc [OPTIONS] COMMAND [ARGS]..." in result.stdout


def test_merge_conflict_prompt_always_forbids_oracles_edit() -> None:
    """workspace-write の conflict 解消 prompt でも oracles は常に編集禁止にする。"""
    repo = Path("/repo")

    prompt = _conflict_prompt(repo, ["app.py"])

    assert "`/repo/oracles` は編集禁止です。" in prompt
    assert "既に conflict がある場合を除いて" not in prompt


def test_files_with_conflict_markers_uses_fixed_conflict_targets(
    tmp_path: Path,
) -> None:
    """marker 検査は現在の unmerged path ではなく渡された対象一覧を見る。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    conflicted = repo / "conflicted.txt"
    conflicted.write_text(
        "<<<<<<< HEAD\nleft\n=======\nright\n>>>>>>> branch\n",
        encoding="utf-8",
    )

    assert _files_with_conflict_markers(repo, ["conflicted.txt"]) == [
        "conflicted.txt"
    ]


def _init_repo(tmp_path: Path) -> Path:
    """テスト用 git repo を作り、初期 commit を置く。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test User")
    (repo / "README.md").write_text("test\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "initial")
    return repo


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """git をテスト repo で実行する。"""
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
