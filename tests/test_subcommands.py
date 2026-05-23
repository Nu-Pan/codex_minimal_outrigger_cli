"""サブコマンド本体の決定論的な制御ロジックのテスト。"""

import inspect
import json
import subprocess
import sys
from pathlib import Path

import pytest
import typer
from pytest import MonkeyPatch

from commons.command_runner import run_command
from commons.errors import CmocError
from commons.errors import format_error_report
from commons.repo import branch_base_commit_path
from commons.timing import StepTimer, start_step
from sub_commands import eval_oracles as eval_oracles_module
from sub_commands.apply import cmoc_apply_impl
from sub_commands.apply import _DISCREPANCY_OUTPUT_SCHEMA
from sub_commands.apply import _commit_all_changes
from sub_commands.apply import _organize_prompt
from sub_commands.apply import _use_partial_mode
from sub_commands.apply import _validate_discrepancy_payload
from sub_commands.branch import cmoc_branch_impl
from sub_commands.eval_oracles import cmoc_eval_oracles_impl
from sub_commands.eval_oracles import _evaluation_prompt
from sub_commands.init import cmoc_init_impl
from sub_commands.merge import cmoc_merge_impl
from sub_commands.merge import _conflict_prompt
from sub_commands.merge import _files_with_conflict_markers


def test_run_command_tees_subcommand_output_and_summary(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """共通入口はサブコマンド呼び出しログを stdout とファイルへ tee する。"""
    repo = _init_repo(tmp_path)
    monkeypatch.chdir(repo)

    def handler(resolved_repo: Path) -> int:
        assert resolved_repo == repo
        timer = StepTimer("sample")
        start_step(timer, 1, 1, "first step")
        return 2

    with pytest.raises(typer.Exit) as exit_info:
        run_command(handler)

    captured = capsys.readouterr()
    log_files = list((repo / "logs" / "sub_commands").glob("*.log"))
    log_content = log_files[0].read_text(encoding="utf-8")
    assert exit_info.value.exit_code == 2
    assert captured.err == ""
    assert len(log_files) == 1
    assert "(1/1) first step" in captured.out
    assert "sample (1/1) first step" not in captured.out
    assert "(1/1) first step" in log_content
    assert "sample (1/1) first step" not in log_content
    assert "sample step timings:" in log_content
    assert "- first step:" in log_content
    assert "subcommand total elapsed:" in log_content
    assert "subcommand quota wait elapsed:" in log_content
    assert "subcommand return code: 2" in log_content
    assert "/logs/" in (repo / ".git" / "info" / "exclude").read_text(
        encoding="utf-8"
    )
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_run_command_logs_summary_on_exception(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """例外終了時も可能な範囲の経過時間と戻り値をログに残す。"""
    repo = _init_repo(tmp_path)
    monkeypatch.chdir(repo)

    def handler(_repo: Path) -> None:
        timer = StepTimer("sample")
        start_step(timer, 1, 1, "failing step")
        raise RuntimeError("boom")

    with pytest.raises(typer.Exit) as exit_info:
        run_command(handler)

    log_content = next(
        (repo / "logs" / "sub_commands").glob("*.log")
    ).read_text(encoding="utf-8")
    assert exit_info.value.exit_code == 1
    assert "ERROR" in log_content
    assert "boom" in log_content
    assert "(1/1) failing step" in log_content
    assert "sample (1/1) failing step" not in log_content
    assert "sample step timings:" in log_content
    assert "- failing step:" in log_content
    assert "subcommand return code: 1" in log_content


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


def test_init_does_not_commit_existing_gitignore_changes(
    tmp_path: Path,
) -> None:
    """`cmoc init` は既存 `.gitignore` 差分を初期化 commit に混ぜない。"""
    repo = _init_repo(tmp_path)
    (repo / ".gitignore").write_text("user-rule\n", encoding="utf-8")

    cmoc_init_impl(repo)

    gitignore = (repo / ".gitignore").read_text(encoding="utf-8")
    committed_gitignore = _git(repo, "show", "HEAD:.gitignore").stdout
    assert gitignore == "user-rule\n/.cmoc/\n"
    assert committed_gitignore == "/.cmoc/\n"
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == (
        "Initialize cmoc"
    )
    assert _git(repo, "status", "--porcelain").stdout == " M .gitignore\n"


def test_init_does_not_commit_preexisting_staged_changes(
    tmp_path: Path,
) -> None:
    """`cmoc init` は実行前から stage 済みの別差分を commit に混ぜない。"""
    repo = _init_repo(tmp_path)
    staged_file = repo / "feature.txt"
    staged_file.write_text("user staged\n", encoding="utf-8")
    _git(repo, "add", "feature.txt")

    cmoc_init_impl(repo)

    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == (
        "Initialize cmoc"
    )
    last_commit_paths = _git(
        repo,
        "show",
        "--name-only",
        "--pretty=format:",
        "HEAD",
    ).stdout.splitlines()
    assert last_commit_paths == [".gitignore"]
    assert _git(repo, "diff", "--cached", "--name-only").stdout == (
        "feature.txt\n"
    )


def test_init_does_not_restore_preexisting_staged_cmoc_changes(
    tmp_path: Path,
) -> None:
    """実行前に stage 済みの `.cmoc` 差分も最終的に追跡対象外にする。"""
    repo = _init_repo(tmp_path)
    cmoc_file = repo / ".cmoc" / "logs" / "staged.log"
    cmoc_file.parent.mkdir(parents=True)
    cmoc_file.write_text("user staged\n", encoding="utf-8")
    _git(repo, "add", "-f", ".cmoc/logs/staged.log")

    cmoc_init_impl(repo)

    assert _git(repo, "ls-files", "--", ".cmoc").stdout == ""
    assert _git(
        repo,
        "check-ignore",
        "-q",
        "--",
        ".cmoc/.__cmoc_ignore_probe__",
    ).returncode == 0
    assert ".cmoc" not in _git(
        repo,
        "diff",
        "--cached",
        "--name-only",
    ).stdout
    assert cmoc_file.exists()


def test_init_can_create_first_commit(tmp_path: Path) -> None:
    """`cmoc init` は unborn HEAD のリポジトリでも初期化 commit を作る。"""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test User")

    cmoc_init_impl(repo)

    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == (
        "Initialize cmoc"
    )
    assert _git(repo, "status", "--porcelain").stdout == ""


def test_branch_creates_cmoc_branch_and_records_base_commit(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """`cmoc branch` は branch 作成と base commit 記録を行う。"""
    repo = _init_repo(tmp_path)
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()

    cmoc_branch_impl(repo)

    branch_name = _git(repo, "branch", "--show-current").stdout.strip()
    record_path = repo / ".cmoc" / "branch" / f"{branch_name}.txt"
    assert branch_name.startswith("cmoc_")
    assert record_path.read_text(encoding="utf-8").strip() == base_commit
    output = capsys.readouterr().out
    assert "(1/3) create cmoc branch" in output
    assert "branch (1/3) create cmoc branch" not in output
    assert "create cmoc branch attempt (1/10)" in output


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
        eval_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )
    codex_kwargs: list[dict[str, object]] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        codex_kwargs.append(kwargs)
        return json.dumps(
            {
                "target_oracle_path": str((oracle_root / "spec.md").resolve()),
                "referenced_paths": [
                    str((oracle_root / "spec.md").resolve()),
                ],
                "specification_only_basis": "oracles 配下の仕様だけを参照しました。",
                "issues": [],
            },
            ensure_ascii=False,
        )

    monkeypatch.setattr(eval_oracles_module, "run_codex_exec", fake_codex)

    cmoc_eval_oracles_impl(repo, full=True)

    reports = list((repo / ".cmoc" / "reports" / "eval-oracles").glob("*.md"))
    assert len(reports) == 1
    report = reports[0].read_text(encoding="utf-8")
    assert codex_kwargs[0]["expect_json"] is True
    assert codex_kwargs[0]["output_schema"] == (
        eval_oracles_module._EVALUATION_OUTPUT_SCHEMA
    )
    assert "json_validator" in codex_kwargs[0]
    assert "mode: full" in report
    assert "result: ok" in report
    assert "## Fatal issues" in report
    assert "No issues." in report


def test_eval_oracles_report_aggregates_issues_by_severity(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """レポートはファイル単位ではなく issue 単位で severity 順に集約する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    oracle_a = oracle_root / "a.md"
    oracle_b = oracle_root / "b.md"
    oracle_index = oracle_root / "INDEX.md"
    oracle_a.write_text("a\n", encoding="utf-8")
    oracle_b.write_text("b\n", encoding="utf-8")
    oracle_index.write_text("index\n", encoding="utf-8")

    monkeypatch.setattr(
        eval_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        purpose = str(kwargs["purpose"])
        if "oracles/a.md" in purpose:
            return json.dumps(
                {
                    "target_oracle_path": str(oracle_a.resolve()),
                    "referenced_paths": [
                        str(oracle_a.resolve()),
                        str(oracle_index.resolve()),
                        str(oracle_a.resolve()),
                    ],
                    "specification_only_basis": "oracles 配下の仕様だけを参照しました。",
                    "issues": [
                        _eval_oracle_issue(
                            "warning",
                            "A warning",
                            oracle_a,
                            3,
                            4,
                        ),
                        _eval_oracle_issue(
                            "fatal",
                            "A fatal",
                            oracle_a,
                            5,
                            5,
                        ),
                    ],
                },
                ensure_ascii=False,
            )
        return json.dumps(
            {
                "target_oracle_path": str(oracle_b.resolve()),
                "referenced_paths": [
                    str(oracle_b.resolve()),
                    str(oracle_index.resolve()),
                ],
                "specification_only_basis": "oracles 配下の仕様だけを参照しました。",
                "issues": [
                    _eval_oracle_issue(
                        "inconclusive",
                        "B inconclusive",
                        oracle_b,
                        None,
                        None,
                    ),
                    _eval_oracle_issue(
                        "fatal",
                        "B fatal",
                        oracle_b,
                        8,
                        9,
                    ),
                    _eval_oracle_issue(
                        "warning",
                        "B warning",
                        oracle_b,
                        10,
                        10,
                    ),
                ],
            },
            ensure_ascii=False,
        )

    monkeypatch.setattr(eval_oracles_module, "run_codex_exec", fake_codex)

    cmoc_eval_oracles_impl(repo, full=True)

    report = next(
        (repo / ".cmoc" / "reports" / "eval-oracles").glob("*.md")
    ).read_text(encoding="utf-8")
    for field in [
        "schema_version: 1",
        "command: cmoc eval-oracles",
        "generated_at:",
        f"repo_root: {repo.resolve()}",
        f"oracle_root: {oracle_root.resolve()}",
        "mode: full",
        "full_requested: true",
        "branch:",
        "is_cmoc_branch: false",
        "base_commit: null",
        "head_commit:",
        "deleted_oracles_detected: false",
        "oracle_count_total: 2",
        "oracle_count_evaluated: 2",
        "fatal_issue_count: 2",
        "warning_issue_count: 2",
        "inconclusive_issue_count: 1",
        "result: fatal",
    ]:
        assert field in report

    expected_sections = [
        "# cmoc eval-oracles report",
        "## Summary",
        "## Verdict",
        "## Evaluated oracle files",
        "## Fatal issues",
        "## Inconclusive issues",
        "## Warnings",
        "## Referenced files",
    ]
    assert [report.index(section) for section in expected_sections] == sorted(
        report.index(section) for section in expected_sections
    )
    assert report.index("### FATAL-001: A fatal") < report.index(
        "### FATAL-002: B fatal"
    )
    assert report.index("### FATAL-002: B fatal") < report.index(
        "### INCONCLUSIVE-001: B inconclusive"
    )
    assert report.index("### INCONCLUSIVE-001: B inconclusive") < report.index(
        "### WARN-001: A warning"
    )
    assert report.index("### WARN-001: A warning") < report.index(
        "### WARN-002: B warning"
    )
    assert "| 1 | `oracles/a.md` | 2 |" in report
    assert "| 2 | `oracles/b.md` | 3 |" in report
    assert "| `oracles/a.md` | `oracles/a.md`<br>`oracles/INDEX.md` |" in report
    assert "| `oracles/b.md` | `oracles/b.md`<br>`oracles/INDEX.md` |" in report


def test_eval_oracles_result_precedence() -> None:
    """result は評価対象数と severity 件数から機械的に決まる。"""
    assert eval_oracles_module._evaluation_result(
        0,
        {"fatal": 0, "inconclusive": 0, "warning": 0},
    ) == "no_targets"
    assert eval_oracles_module._evaluation_result(
        1,
        {"fatal": 1, "inconclusive": 1, "warning": 1},
    ) == "fatal"
    assert eval_oracles_module._evaluation_result(
        1,
        {"fatal": 0, "inconclusive": 1, "warning": 1},
    ) == "inconclusive"
    assert eval_oracles_module._evaluation_result(
        1,
        {"fatal": 0, "inconclusive": 0, "warning": 1},
    ) == "warning"
    assert eval_oracles_module._evaluation_result(
        1,
        {"fatal": 0, "inconclusive": 0, "warning": 0},
    ) == "ok"


def test_eval_oracles_stays_partial_when_oracle_was_deleted(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """削除済み oracle があっても `--full` なしの cmoc branch は部分評価する。"""
    repo = _init_repo(tmp_path)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    changed_oracle = oracle_root / "changed.md"
    unchanged_oracle = oracle_root / "unchanged.md"
    deleted_oracle = oracle_root / "deleted.md"
    changed_oracle.write_text("before\n", encoding="utf-8")
    unchanged_oracle.write_text("unchanged\n", encoding="utf-8")
    deleted_oracle.write_text("deleted\n", encoding="utf-8")
    _git(repo, "add", "oracles")
    _git(repo, "commit", "-m", "add oracles")
    _checkout_cmoc_branch(repo)
    changed_oracle.write_text("after\n", encoding="utf-8")
    deleted_oracle.unlink()

    evaluated_prompts: list[str] = []
    monkeypatch.setattr(
        eval_oracles_module,
        "maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        evaluated_prompts.append(str(args[1]))
        return json.dumps(
            {
                "target_oracle_path": str(changed_oracle.resolve()),
                "referenced_paths": [str(changed_oracle.resolve())],
                "specification_only_basis": "oracles 配下の仕様だけを参照しました。",
                "issues": [],
            },
            ensure_ascii=False,
        )

    monkeypatch.setattr(eval_oracles_module, "run_codex_exec", fake_codex)

    cmoc_eval_oracles_impl(repo, full=False)

    reports = list((repo / ".cmoc" / "reports" / "eval-oracles").glob("*.md"))
    report = reports[0].read_text(encoding="utf-8")
    assert len(evaluated_prompts) == 1
    assert str(changed_oracle) in evaluated_prompts[0]
    assert str(unchanged_oracle) not in evaluated_prompts[0]
    assert "mode: partial" in report
    assert "deleted_oracles_detected: true" in report
    assert "oracle_count: 1" in report


def test_eval_oracles_body_uses_subcommand_file_name() -> None:
    """`eval-oracles` の本体は PEP 8 の module 名に置く。"""
    repo_root = Path(__file__).resolve().parents[1]

    body = repo_root / "src" / "sub_commands" / "eval_oracles.py"
    legacy = repo_root / "src" / "sub_commands" / "eval-oracles.py"
    body_text = body.read_text(encoding="utf-8")
    assert "def cmoc_eval_oracles_impl" in body_text
    assert "spec_from_file_location" not in body_text
    assert not legacy.exists()


def test_eval_oracles_prompt_forbids_implementation_references() -> None:
    """評価 prompt は仕様だけから致命的問題を判断させる。"""
    prompt = _evaluation_prompt(Path("/repo"), Path("/repo/oracles/spec.md"))

    assert "`/repo/oracles` 外のファイルは一切参照禁止です。" in prompt
    assert "`/repo/oracles/INDEX.md` から始まる INDEX.md" in prompt
    assert "`oracles` 外のファイルは一切参照禁止です。" not in prompt
    assert "`oracles/INDEX.md`" not in prompt
    assert "実装ファイル、テストファイル、設定ファイル、ビルド成果物も参照禁止です。" in prompt
    assert "referenced_paths には参照した oracle / INDEX ファイルの絶対パス" in prompt
    assert "Structured Output schema に一致する JSON" in prompt
    assert "仕様だけから判断・実装したとき" in prompt


def test_eval_oracles_prompt_orders_completion_before_details() -> None:
    """評価 prompt はロール、作業、完了条件、詳細指示の順にする。"""
    prompt = _evaluation_prompt(Path("/repo"), Path("/repo/oracles/spec.md"))
    lines = prompt.splitlines()

    assert lines[0] == "あなたはソフトウェア仕様のレビュー担当です。"
    assert lines[1] == (
        "`/repo` 内の oracle ファイル `/repo/oracles/spec.md` を評価してください。"
    )
    assert lines[2] == (
        "完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです。"
    )
    assert lines.index(
        "target_oracle_path には評価対象 oracle ファイルの絶対パスを返してください。"
    ) > 2


def test_apply_returns_complete_when_no_discrepancies(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """`cmoc apply` は不整合なし JSON で完了扱いのレポートを保存する。"""
    repo = _init_repo(tmp_path)
    _checkout_cmoc_branch(repo)
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
    codex_prompts: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査なら不整合なし JSON、レポートなら Markdown を返す。"""
        codex_kwargs.append(kwargs)
        codex_prompts.append(str(args[1]))
        if kwargs.get("expect_json") is True:
            return '{"fixing_points": []}'
        return "\n".join(
            [
                "## 作業結果",
                "収束",
                "## 不整合件数の推移",
                "1 回目: 0 件",
                "## ブランチ cmoc_2026-05-10_22-21_10_123 上の全変更内容",
                "カテゴリ: oracle 整備",
            ]
        )

    monkeypatch.setattr("sub_commands.apply.run_codex_exec", fake_codex)

    exit_code = cmoc_apply_impl(repo)

    reports = list((repo / ".cmoc" / "reports" / "apply").glob("*.md"))
    assert exit_code == 0
    assert len(reports) == 1
    report_text = reports[0].read_text(encoding="utf-8")
    assert "## 作業結果" in report_text
    assert "## 不整合件数の推移" in report_text
    assert "全変更内容" in report_text
    assert codex_kwargs[0]["output_schema"] == _DISCREPANCY_OUTPUT_SCHEMA
    assert "fixing_points" in codex_prompts[0]
    assert "実装だけから見た成果物品質上の致命的な問題" in codex_prompts[0]
    assert "oracle_requirement" in codex_prompts[0]
    assert "作業結果区分: 収束" in codex_prompts[-1]
    assert "変更内容の意味論に基づき" in codex_prompts[-1]
    assert "「カテゴリ」という語" in codex_prompts[-1]
    assert "<cmoc-branch>" not in codex_prompts[-1]


def test_apply_uses_investigate_repeat_option_for_loop_limit(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """`cmoc apply` は指定された調査・修正ループ回数を上限に使う。"""
    repo = _init_repo(tmp_path)
    _checkout_cmoc_branch(repo)
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
    codex_prompts: list[str] = []

    def fake_codex(*args: object, **kwargs: object) -> str:
        """常に不整合を返し、指定回数で incomplete になることを見やすくする。"""
        codex_prompts.append(str(args[1]))
        if kwargs.get("expect_json") is True:
            return _discrepancy_json("f")
        return "\n".join(
            [
                "## 作業結果",
                "未収束",
                "## 不整合件数の推移",
                "1 回目: 1 件",
                "2 回目: 1 件",
                "まだ不整合が残っている可能性があります。",
                "## ブランチ cmoc_2026-05-10_22-21_10_123 上の全変更内容",
                "カテゴリ: 実装修正",
            ]
        )

    monkeypatch.setattr("sub_commands.apply.run_codex_exec", fake_codex)

    exit_code = cmoc_apply_impl(repo, repeat_investigate_and_fix=2)

    assert exit_code == 2
    assert (
        "implementation loop (2/2) discrepancies: 1"
        in capsys.readouterr().out
    )
    reports = list((repo / ".cmoc" / "reports" / "apply").glob("*.md"))
    report_text = reports[0].read_text(encoding="utf-8")
    assert "作業結果区分: 未収束" in codex_prompts[-1]
    assert "まだ不整合が残っている可能性" in codex_prompts[-1]
    assert "まだ不整合が残っている可能性" in report_text


def test_apply_improoves_fixing_list_until_same_result_or_limit(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """要修正点リスト改善ループは上限内で同一結果まで繰り返す。"""
    repo = _init_repo(tmp_path)
    _checkout_cmoc_branch(repo)
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
    organize_prompts: list[str] = []
    apply_prompts: list[str] = []
    organize_results = [
        _discrepancy_json("first improvement"),
        _discrepancy_json("second improvement"),
        _discrepancy_json("second improvement"),
    ]

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査、改善、修正、レポートの呼び出しを purpose で分岐する。"""
        purpose = str(kwargs.get("purpose"))
        if purpose.startswith("investigate"):
            return _discrepancy_json("initial")
        if purpose == "organize discrepancies":
            organize_prompts.append(str(args[1]))
            return organize_results.pop(0)
        if purpose.startswith("apply discrepancy"):
            apply_prompts.append(str(args[1]))
            return ""
        if purpose == "write apply report":
            return "\n".join(
                [
                    "## 作業結果",
                    "未収束",
                    "## 不整合件数の推移",
                    "1 回目: 1 件",
                    "まだ不整合が残っている可能性があります。",
                    "## ブランチ cmoc_2026-05-10_22-21_10_123 上の全変更内容",
                    "カテゴリ: 実装修正",
                ]
            )
        return ""

    monkeypatch.setattr("sub_commands.apply.run_codex_exec", fake_codex)

    exit_code = cmoc_apply_impl(
        repo,
        repeat_investigate_and_fix=1,
        repeat_improove_fixing_list=3,
    )

    output = capsys.readouterr().out
    assert exit_code == 2
    assert len(organize_prompts) == 3
    assert "fixing list improvement loop (3/3) discrepancies: 1" in output
    assert "second improvement" in apply_prompts[0]
    assert "initial" in organize_prompts[0]
    assert "first improvement" in organize_prompts[1]


def test_apply_mode_depends_only_on_full_option() -> None:
    """`cmoc apply` の部分・全体適用モードは --full の有無だけで決まる。"""
    assert _use_partial_mode(False) is True
    assert _use_partial_mode(True) is False


def test_organize_prompt_includes_fixing_list_quality_requirements(
    tmp_path: Path,
) -> None:
    """要修正点リスト改善 prompt は oracle の品質観点を明示する。"""
    prompt = _organize_prompt(
        tmp_path,
        json.loads(_discrepancy_json("fix"))["fixing_points"],
    )

    assert "内容の品質に明確な問題がない" in prompt
    assert "重複する要修正点は 1 件にマージ" in prompt
    assert "矛盾する修正方針は矛盾しない内容に調整" in prompt
    assert "`<cmoc-branch>` 上の過去の修正内容を確認" in prompt
    assert "False-Positive と判断できる要修正点は除外" in prompt
    assert "作業順序として適切になるよう並べ替えてください" in prompt
    assert "改善過程で発見した漏れがあれば" in prompt


def test_apply_rejects_incomplete_report_from_codex(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """必須内容を欠く apply レポートは保存せずエラーにする。"""
    repo = _init_repo(tmp_path)
    _checkout_cmoc_branch(repo)
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
        """調査は収束、レポートは必須項目不足にする。"""
        if kwargs.get("expect_json") is True:
            return '{"fixing_points": []}'
        return "収束\ncomplete report"

    monkeypatch.setattr("sub_commands.apply.run_codex_exec", fake_codex)

    with pytest.raises(CmocError):
        cmoc_apply_impl(repo)

    report_dir = repo / ".cmoc" / "reports" / "apply"
    assert not report_dir.exists() or list(report_dir.glob("*.md")) == []


def test_apply_rejects_non_cmoc_branch(tmp_path: Path) -> None:
    """`cmoc apply` は cmoc ブランチ外では仕様通り CmocError にする。"""
    repo = _init_repo(tmp_path)

    with pytest.raises(CmocError) as error:
        cmoc_apply_impl(repo)

    assert "`cmoc apply` は cmoc branch 上で実行してください。" in error.value.message


def test_apply_rejects_non_oracle_changes_after_cmoc_guarantee(
    tmp_path: Path,
) -> None:
    """`cmoc apply` は `.cmoc` 保証後にユーザー由来の oracle 外差分を拒否する。"""
    repo = _init_repo(tmp_path)
    _checkout_cmoc_branch(repo)
    (repo / "app.py").write_text("changed\n", encoding="utf-8")

    with pytest.raises(CmocError):
        cmoc_apply_impl(repo)

    assert ".cmoc" in (repo / ".gitignore").read_text(encoding="utf-8")
    assert _git(repo, "log", "-1", "--pretty=%s").stdout.strip() == (
        "Ensure cmoc directory is ignored"
    )


def test_apply_does_not_commit_preexisting_gitignore_changes(
    tmp_path: Path,
) -> None:
    """`.cmoc` 保証 commit は既存 `.gitignore` 差分を混ぜない。"""
    repo = _init_repo(tmp_path)
    _checkout_cmoc_branch(repo)
    (repo / ".gitignore").write_text("user-rule\n", encoding="utf-8")

    with pytest.raises(CmocError):
        cmoc_apply_impl(repo)

    assert _git(repo, "show", "HEAD:.gitignore").stdout == "/.cmoc/\n"
    assert _git(repo, "status", "--porcelain", "--", ".gitignore").stdout == (
        " M .gitignore\n"
    )


def test_apply_commits_cmoc_guarantee_before_oracle_changes(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """`cmoc apply` は `.cmoc` 保証差分を oracle commit 前に処理する。"""
    repo = _init_repo(tmp_path)
    _checkout_cmoc_branch(repo)
    cmoc_log = repo / ".cmoc" / "logs" / "poll.log"
    cmoc_log.parent.mkdir(parents=True)
    cmoc_log.write_text("local log\n", encoding="utf-8")
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
            return '{"fixing_points": []}'
        return "\n".join(
            [
                "## 作業結果",
                "収束",
                "## 不整合件数の推移",
                "1 回目: 0 件",
                "## ブランチ cmoc_2026-05-10_22-21_10_123 上の全変更内容",
                "カテゴリ: oracle 整備",
            ]
        )

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
    assert _git(repo, "status", "--porcelain", "--", ".cmoc").stdout == ""


def test_apply_does_not_mix_preexisting_staged_oracles_into_cmoc_commit(
    tmp_path: Path,
    monkeypatch: MonkeyPatch,
) -> None:
    """事前 stage 済み oracle 差分も `.cmoc` 保証 commit へ混ぜない。"""
    repo = _init_repo(tmp_path)
    _checkout_cmoc_branch(repo)
    oracle_root = repo / "oracles"
    oracle_root.mkdir()
    (oracle_root / "spec.md").write_text("spec\n", encoding="utf-8")
    _git(repo, "add", "oracles/spec.md")

    monkeypatch.setattr(
        "sub_commands.apply.maintain_indexes",
        lambda repo_root: False,
    )

    def fake_codex(*args: object, **kwargs: object) -> str:
        """調査なら不整合なし JSON、レポートなら Markdown を返す。"""
        if kwargs.get("expect_json") is True:
            return '{"fixing_points": []}'
        return "\n".join(
            [
                "## 作業結果",
                "収束",
                "## 不整合件数の推移",
                "1 回目: 0 件",
                "## ブランチ cmoc_2026-05-10_22-21_10_123 上の全変更内容",
                "カテゴリ: oracle 整備",
            ]
        )

    monkeypatch.setattr("sub_commands.apply.run_codex_exec", fake_codex)

    assert cmoc_apply_impl(repo) == 0

    cmoc_commit_paths = _git(
        repo,
        "show",
        "--name-only",
        "--pretty=format:",
        "HEAD~1",
    ).stdout.splitlines()
    oracle_commit_paths = _git(
        repo,
        "show",
        "--name-only",
        "--pretty=format:",
        "HEAD",
    ).stdout.splitlines()
    assert cmoc_commit_paths == [".gitignore"]
    assert oracle_commit_paths == ["oracles/spec.md"]
    assert _git(repo, "status", "--porcelain").stdout == ""


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
                "fixing_points": [
                    {
                        "title": "missing fields",
                    }
                ]
            }
        )


def test_apply_discrepancy_schema_accepts_fixing_points() -> None:
    """要修正点 JSON は fixing_points と evidences 形式を受け付ける。"""
    _validate_discrepancy_payload(json.loads(_discrepancy_json("fix")))


def test_apply_discrepancy_schema_rejects_near_miss_keys() -> None:
    """似た名前のキーでも不整合調査 schema と一致しなければ拒否する。"""
    with pytest.raises(ValueError):
        _validate_discrepancy_payload(
            {
                "fixing_points": [
                    {
                        "title": "near miss",
                        "evidence": [
                            {
                                "path": "/repo/src/app.py",
                                "line_start": 10,
                                "line_end": 12,
                                "summary": "summary",
                            }
                        ],
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
    _checkout_cmoc_branch(repo)
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
    eval_oracles_source = inspect.getsource(main.eval_oracles_command)

    assert "def _run_command" not in source
    assert "_run_command(" not in source
    assert "cmoc_init_impl()" in source
    assert "cmoc_branch_impl()" in source
    assert (
        "from sub_commands.eval_oracles import cmoc_eval_oracles_impl"
        in source
    )
    assert "from sub_commands.eval_oracles" not in eval_oracles_source
    assert "cmoc_eval_oracles_impl(full=full)" in source
    assert "repeat_investigate_and_fix=repeat_investigate_and_fix" in source
    assert "repeat_improove_fixing_list=repeat_improove_fixing_list" in source
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


def test_cmoc_apply_help_exposes_oracle_repeat_options() -> None:
    """`cmoc apply --help` は oracle で定義された正式オプションを表示する。"""
    repo_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "-m", "main", "apply", "--help"],
        cwd=repo_root,
        env={"PYTHONPATH": str(repo_root / "src")},
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert "--repeat-investigate-and-fix" in result.stdout
    assert "--repeat-improove-fixing-list" in result.stdout
    assert "--full" in result.stdout


def test_main_returns_nonzero_for_subcommand_error() -> None:
    """サブコマンド内エラーはプロセス終了コードへ反映される。"""
    repo_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "main",
            "apply",
            "--repeat-investigate-and-fix",
            "-1",
        ],
        cwd=repo_root,
        env={"PYTHONPATH": str(repo_root / "src")},
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 1
    assert result.stderr == ""
    assert "ERROR" in result.stdout
    assert "Summary:" in result.stdout


def test_main_reports_no_args_error_with_non_empty_detail() -> None:
    """引数なし起動も詳細説明を含む共通エラーレポートにする。"""
    repo_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "-m", "main"],
        cwd=repo_root,
        env={"PYTHONPATH": str(repo_root / "src")},
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 2
    assert result.stderr == ""
    assert "ERROR" in result.stdout
    assert "Summary:\nコマンドが指定されていません。" in result.stdout
    assert "Next actions:" in result.stdout
    assert "- 利用可能なコマンドを確認するには `cmoc --help` を実行してください。" in result.stdout
    assert "Detail:\ncmoc がサブコマンドなしで起動されました。" in result.stdout
    assert "Call stack:" in result.stdout


def test_format_error_report_fills_empty_generic_detail() -> None:
    """通常例外の文字列表現が空でも Detail を空欄にしない。"""
    error = Exception()

    report = format_error_report(error)

    assert "Summary:\nException" in report
    assert (
        "- 入力値が誤っている場合は、コマンド引数を修正してから cmoc を再実行してください。"
        in report
    )
    assert (
        "- リポジトリ状態が原因の場合は、Detail と Call stack を確認して作業ツリーや設定を修正してください。"
        in report
    )
    assert "Detail:\nbuiltins.Exception がメッセージなしで発生しました。" in report
    assert "Call stack:" in report


def test_user_facing_error_text_does_not_keep_known_english_phrases() -> None:
    """共通エラーレポートに渡す説明・次アクションを日本語方針で固定する。"""
    repo_root = Path(__file__).resolve().parents[1]
    target_paths = [
        repo_root / "src" / "commons" / "errors.py",
        repo_root / "src" / "commons" / "repo.py",
        repo_root / "src" / "sub_commands" / "apply.py",
        repo_root / "src" / "sub_commands" / "merge.py",
    ]
    forbidden_fragments = [
        "Git repository root was not found.",
        "Move into a git-managed repository.",
        "Uncommitted changes exist.",
        "Commit or stash",
        "cmoc apply must be run on a cmoc branch.",
        "Run `cmoc branch` first.",
        "Failed to resolve cmoc branch automatically.",
        "Pass the cmoc branch name explicitly.",
        "Inspect git status manually.",
        "Resolve remaining conflict markers manually.",
        "Manual resolution is required.",
    ]
    source_text = "\n".join(
        path.read_text(encoding="utf-8") for path in target_paths
    )

    for fragment in forbidden_fragments:
        assert fragment not in source_text


def test_bin_cmoc_requires_venv_python() -> None:
    """ランチャーは system python3 へフォールバックしない。"""
    repo_root = Path(__file__).resolve().parents[1]
    launcher = (repo_root / "bin" / "cmoc").read_text(encoding="utf-8")

    assert launcher.startswith("#!/bin/sh")
    assert "#!/usr/bin/env python3" not in launcher
    assert 'exec "$venv_python"' in launcher
    assert "} >&2" not in launcher


def test_bin_cmoc_reports_missing_venv_to_stdout(tmp_path: Path) -> None:
    """仮想環境が無い場合も共通エラーレポートを stdout へ出す。"""
    repo_root = Path(__file__).resolve().parents[1]
    launcher = tmp_path / "repo" / "bin" / "cmoc"
    launcher.parent.mkdir(parents=True)
    launcher.write_text(
        (repo_root / "bin" / "cmoc").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    launcher.chmod(0o755)

    result = subprocess.run(
        [str(launcher), "--help"],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert result.returncode == 1
    assert result.stderr == ""
    assert "ERROR" in result.stdout
    assert "Summary:" in result.stdout
    assert "Next actions:" in result.stdout
    assert "Detail:" in result.stdout
    assert "Call stack:" in result.stdout
    assert "仮想環境 Python" in result.stdout
    assert "at print_missing_venv_error" in result.stdout
    assert "at require_venv_python" in result.stdout
    assert "at main" in result.stdout
    assert "仮想環境 Python の実行可能性チェック" not in result.stdout


def test_merge_conflict_prompt_always_forbids_oracles_edit() -> None:
    """workspace-write の conflict 解消 prompt でも oracles は常に編集禁止にする。"""
    repo = Path("/repo")

    prompt = _conflict_prompt(repo, ["app.py"])

    assert "`/repo/oracles` は編集禁止です。" in prompt
    assert "解消してください: ['/repo/app.py']" in prompt
    assert "解消してください: ['app.py']" not in prompt
    assert "既に conflict がある場合を除いて" not in prompt
    assert "解決内容と未解決ファイルの有無を報告" in prompt


def test_files_with_conflict_markers_checks_all_tracked_files(
    tmp_path: Path,
) -> None:
    """marker 検査は渡された対象一覧に限定せず git 管理対象全体を見る。"""
    repo = _init_repo(tmp_path)
    conflicted = repo / "conflicted.txt"
    unrelated = repo / "unrelated.txt"
    conflicted.write_text("resolved\n", encoding="utf-8")
    unrelated.write_text(
        "<<<<<<< HEAD\nleft\n=======\nright\n>>>>>>> branch\n",
        encoding="utf-8",
    )
    _git(repo, "add", "conflicted.txt", "unrelated.txt")
    _git(repo, "commit", "-m", "add tracked files")

    assert _files_with_conflict_markers(repo, ["conflicted.txt"]) == [
        "unrelated.txt"
    ]


def _discrepancy_json(suggested_fix: str) -> str:
    """テスト用の valid な不整合 JSON を返す。"""
    return json.dumps(
        {
            "git_head_commit_hash": None,
            "fixing_points": [
                {
                    "title": "t",
                    "evidences": [
                        {
                            "path": "/repo/oracles/spec.md",
                            "line_start": 1,
                            "line_end": 1,
                            "summary": "spec",
                        }
                    ],
                    "oracle_requirement": "r",
                    "observed_implementation": "o",
                    "reason": "x",
                    "suggested_fix": suggested_fix,
                }
            ]
        }
    )


def _eval_oracle_issue(
    severity: str,
    title: str,
    oracle_path: Path,
    line_start: int | None,
    line_end: int | None,
) -> dict[str, object]:
    """テスト用の valid な eval-oracles issue item を返す。"""
    return {
        "severity": severity,
        "title": title,
        "oracle_path": str(oracle_path.resolve()),
        "oracle_line_start": line_start,
        "oracle_line_end": line_end,
        "affected_workflow": "cmoc eval-oracles",
        "requirement": f"{title} requirement",
        "problem": f"{title} problem",
        "reason": f"{title} reason",
        "suggested_oracle_change": f"{title} change",
    }


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


def _checkout_cmoc_branch(repo: Path) -> None:
    """テスト用 cmoc branch に移動し、base commit 記録を作る。"""
    branch_name = "cmoc_2026-05-10_22-21_10_123"
    base_commit = _git(repo, "rev-parse", "HEAD").stdout.strip()
    _git(repo, "checkout", "-b", branch_name)
    path = branch_base_commit_path(repo, branch_name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(base_commit, encoding="utf-8")
    exclude = repo / ".git" / "info" / "exclude"
    exclude.write_text(f"{exclude.read_text(encoding='utf-8')}\n.cmoc/\n")


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
