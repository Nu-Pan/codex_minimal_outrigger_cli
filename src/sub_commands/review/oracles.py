"""`cmoc review oracles` の本体処理。"""

from concurrent.futures import Future, ThreadPoolExecutor
from contextvars import copy_context
from dataclasses import dataclass
import json
from pathlib import Path
import shutil
import sys
import tempfile
from time import sleep
from typing import Literal

from commons.codex import (
    FRONTIER_HIGH_REASONING_EFFORT,
    FRONTIER_MODEL,
    parse_json_object,
    run_codex_exec,
)
from commons.command_runner import run_command
from commons.errors import CmocError
from commons.indexing import maintain_indexes
from commons.report_files import write_timestamped_report
from commons.repo import (
    REVIEW_BRANCH_PREFIX,
    assert_no_uncommitted_changes,
    changed_oracle_files,
    current_branch,
    ensure_cmoc_ignored_and_committed,
    has_deleted_oracle_files,
    head_commit,
    is_cmoc_branch,
    is_session_branch,
    list_oracle_files,
    read_session_state,
    read_session_start_commit,
    session_id_from_branch,
    session_state_root,
    run_git,
)
from commons.timing import StepTimer, start_step
from commons.timestamps import make_timestamp

_SEVERITY_ORDER = ["fatal", "inconclusive", "warning"]
_ISSUE_ID_PREFIXES = {
    "fatal": "FATAL",
    "inconclusive": "INCONCLUSIVE",
    "warning": "WARN",
}
ReviewOraclesScope = Literal["session", "full"]
_REPORT_COMMAND = "cmoc review oracles"
_REPORT_DIR_NAME = "review_oracles"
_REVIEW_ORACLES_TMP_DIR = Path(".cmoc") / "tmp"
_DEFAULT_REVIEW_ORACLES_LOOP = 3
_DEFAULT_REPEAT_IMPROVE_ISSUES_LIST = _DEFAULT_REVIEW_ORACLES_LOOP
_CMOC_ROOT = Path(__file__).resolve().parents[3]
_REVIEW_ORACLES_SCHEMA_ROOT = (
    _CMOC_ROOT / "oracles" / "schemas" / "structured_output" / "review" / "oracles"
)


def _load_review_oracles_output_schema(file_name: str) -> dict[str, object]:
    """review oracles の正本 Structured Output schema を読む。"""
    schema = json.loads(
        (_REVIEW_ORACLES_SCHEMA_ROOT / file_name).read_text(encoding="utf-8")
    )
    if not isinstance(schema, dict):
        raise TypeError(f"{file_name} must contain a JSON object schema.")
    return schema


def _schema_string_enum(schema: dict[str, object], keys: tuple[str, ...]) -> list[str]:
    """正本 schema 内の string enum を Python 側処理順にも使う。"""
    current: object = schema
    for key in keys:
        if not isinstance(current, dict):
            raise TypeError(f"schema path {'.'.join(keys)} is not an object.")
        current = current[key]
    if not isinstance(current, dict):
        raise TypeError(f"schema path {'.'.join(keys)} is not an object.")
    values = current["enum"]
    if not isinstance(values, list) or not all(
        isinstance(value, str) for value in values
    ):
        raise TypeError(f"schema path {'.'.join(keys)} must contain a string enum.")
    return values


_ENUMERATE_FINDINGS_OUTPUT_SCHEMA = _load_review_oracles_output_schema(
    "enumerate_findings.json"
)
_MERGE_FINDINGS_OUTPUT_SCHEMA = _load_review_oracles_output_schema(
    "merge_findings.json"
)
_VALIDATE_FINDINGS_CHALLENGER_OUTPUT_SCHEMA = _load_review_oracles_output_schema(
    "validate_findings_challenger.json"
)
_VALIDATE_FINDINGS_ADVOCATE_OUTPUT_SCHEMA = _load_review_oracles_output_schema(
    "validate_findings_advocate.json"
)
_JUDGE_FINDINGS_OUTPUT_SCHEMA = _load_review_oracles_output_schema(
    "judge_findings.json"
)
_FINDING_SEVERITY_ORDER = _schema_string_enum(
    _ENUMERATE_FINDINGS_OUTPUT_SCHEMA,
    ("properties", "findings", "items", "properties", "severity"),
)
_FINDING_VERDICT_ORDER = _schema_string_enum(
    _JUDGE_FINDINGS_OUTPUT_SCHEMA,
    ("properties", "verdict"),
)
_SPECULATIVE_REASON_PHRASES = [
    "かもしれない",
    "可能性がある",
]
_ISSUE_OUTPUT_SCHEMA: dict[str, object] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "severity",
        "title",
        "oracle_path",
        "oracle_line_start",
        "oracle_line_end",
        "referenced_paths",
        "affected_workflow",
        "requirement",
        "problem",
        "reason",
        "suggested_oracle_change",
        "specification_only_basis",
    ],
    "properties": {
        "severity": {
            "type": "string",
            "enum": ["fatal", "warning", "inconclusive"],
            "description": "問題点の分類。",
        },
        "title": {
            "type": "string",
            "description": "問題点の短い見出し。",
        },
        "oracle_path": {
            "type": "string",
            "description": "問題点の根拠となる仕様ファイルの絶対パス。",
        },
        "oracle_line_start": {
            "anyOf": [
                {"type": "integer", "minimum": 1},
                {"type": "null"},
            ],
            "description": (
                "問題点の根拠となる仕様記述の開始行。"
                "特定できない場合は null。"
            ),
        },
        "oracle_line_end": {
            "anyOf": [
                {"type": "integer", "minimum": 1},
                {"type": "null"},
            ],
            "description": (
                "問題点の根拠となる仕様記述の終了行。"
                "特定できない場合は null。"
            ),
        },
        "referenced_paths": {
            "type": "array",
            "description": (
                "この問題点の評価時に参照した仕様ファイルまたは INDEX.md の絶対パス。"
            ),
            "items": {"type": "string"},
        },
        "affected_workflow": {
            "type": "string",
            "description": (
                "影響を受ける workflow / subcommand / concept。"
                "例: apply fork, review, overall。"
            ),
        },
        "requirement": {
            "type": "string",
            "description": "仕様ファイルが要求している、または要求すべき仕様。",
        },
        "problem": {
            "type": "string",
            "description": "仕様上の問題点。",
        },
        "reason": {
            "type": "string",
            "description": (
                "なぜその severity と判断したのか。fatal の場合は"
                "致命的問題の定義との対応を明示する。"
            ),
        },
        "suggested_oracle_change": {
            "type": "string",
            "description": "仕様ファイルをどう修正すべきか。",
        },
        "specification_only_basis": {
            "type": "string",
            "description": (
                "この問題点の評価が仕様ファイルと INDEX.md だけに"
                "基づくことの説明。"
            ),
        },
    },
}
_EVALUATION_OUTPUT_SCHEMA: dict[str, object] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["issues"],
    "properties": {
        "issues": {
            "type": "array",
            "description": "検出した問題点。問題がない場合は空配列。",
            "items": _ISSUE_OUTPUT_SCHEMA,
        },
    },
}


@dataclass(frozen=True)
class _OracleEvaluationSnapshot:
    """review 開始時点の oracles tree を評価用に固定した copy。"""

    original_repo_root: Path
    original_oracle_root: Path
    snapshot_root: Path
    snapshot_oracle_root: Path
    oracle_files: frozenset[Path]
    reference_files: frozenset[Path]


@dataclass(frozen=True)
class _ReviewWorktreePlan:
    """review run 用 branch/worktree 作成計画。"""

    review_run_id: str
    review_branch: str
    review_worktree: Path


@dataclass
class _Finding:
    """review oracles の所見処理 pipeline で扱う所見。"""

    finding_id: str
    severity: Literal["fatal", "minor"]
    title: str
    oracle_path: str
    reason: str
    challenger_reasons: list[str]
    advocate_reasons: list[str]
    judge_verdict: Literal["accept", "reject"] | None = None
    judge_reason: str = ""


@dataclass
class _FindingIdAllocator:
    """所見 pipeline 全体で finding_id の再利用を防ぐ採番状態。"""

    next_index: int = 1

    @classmethod
    def from_findings(cls, findings: list[_Finding]) -> "_FindingIdAllocator":
        """既存所見の最大 FINDING number より後ろから採番する。"""
        max_index = 0
        for finding in findings:
            parsed_index = _parse_finding_id_index(finding.finding_id)
            if parsed_index is not None:
                max_index = max(max_index, parsed_index)
        return cls(max_index + 1)

    def allocate(self) -> int:
        """次に使用する finding number を返し、内部状態を進める。"""
        index = self.next_index
        self.next_index += 1
        return index


def cmoc_review_oracles_impl(
    repo_root: Path | None = None,
    *,
    scope: ReviewOraclesScope = "session",
    enumerate_findings_loop: int = _DEFAULT_REVIEW_ORACLES_LOOP,
    merge_findings_loop: int = _DEFAULT_REVIEW_ORACLES_LOOP,
    refine_findings_loop: int = _DEFAULT_REVIEW_ORACLES_LOOP,
    full: bool | None = None,
    repeat_improve_issues_list: int | None = None,
) -> None:
    """oracle 断片を Codex CLI で評価し、レポートを作る。"""
    scope = _normalize_review_oracles_scope(scope, full)
    if repeat_improve_issues_list is not None:
        refine_findings_loop = repeat_improve_issues_list

    # 直接呼び出し時は共通 runner で repo root 解決とエラー整形を行う。
    if repo_root is None:
        run_command(
            lambda resolved_repo_root: cmoc_review_oracles_impl(
                resolved_repo_root,
                scope=scope,
                enumerate_findings_loop=enumerate_findings_loop,
                merge_findings_loop=merge_findings_loop,
                refine_findings_loop=refine_findings_loop,
            ),
            command_path="cmoc review oracles",
        )
        return
    _validate_review_oracles_loop(
        enumerate_findings_loop,
        "--enumerate-findings-loop",
    )
    _validate_review_oracles_loop(merge_findings_loop, "--merge-findings-loop")
    _validate_review_oracles_loop(refine_findings_loop, "--refine-findings-loop")

    timer = StepTimer("review oracles")
    mode = None
    branch_name = None
    cmoc_branch = None
    base_commit = None
    session_fork_commit = None
    review_start_commit = None
    review_fork_commit = None
    review_join_commit = None
    deleted_oracles = None
    all_oracle_files: list[Path] = []
    all_oracle_files_known = False
    oracle_files: list[Path] = []
    evaluations = []
    failed_stage = "review oracles 初期化"
    review_plan: _ReviewWorktreePlan | None = None
    try:
        branch_name = _validate_review_oracles_preconditions(repo_root)

        session_fork_commit = read_session_start_commit(repo_root, branch_name)

        # 評価前に `.cmoc` の ignore 保証を済ませる。
        failed_stage = ".cmoc ignore 確認"
        start_step(timer, 1, 6, ".cmoc ignore 確認")
        ensure_cmoc_ignored_and_committed(repo_root)
        assert_no_uncommitted_changes(repo_root)

        session_id = session_id_from_branch(branch_name)
        state_root = session_state_root(repo_root)
        review_start_commit = head_commit(repo_root)

        failed_stage = "review worktree 作成"
        review_plan = _create_review_worktree(
            state_root,
            session_id,
            review_start_commit,
        )
        review_repo_root = review_plan.review_worktree
        review_fork_commit = head_commit(review_repo_root)

        # branch 状態と scope から、部分評価か全体評価かを決める。
        failed_stage = "oracle ファイル選定"
        start_step(timer, 2, 6, "oracle ファイル選定")
        cmoc_branch = is_cmoc_branch(branch_name)
        session_branch = is_session_branch(branch_name)
        partial = session_branch and scope == "session"
        mode = "partial" if partial else "full"
        if partial:
            base_commit = session_fork_commit
            deleted_oracles = has_deleted_oracle_files(review_repo_root, base_commit)
        else:
            deleted_oracles = False

        # 評価モードに応じて Codex CLI に渡す oracle ファイル一覧を作る。
        all_review_oracle_files = list_oracle_files(review_repo_root)
        all_oracle_files = [
            _owner_path_for_worktree_path(repo_root, review_repo_root, path)
            for path in all_review_oracle_files
        ]
        all_oracle_files_known = True
        if enumerate_findings_loop == 0:
            oracle_files = []
        elif partial:
            assert base_commit is not None
            changed_files = {
                _owner_path_for_worktree_path(repo_root, review_repo_root, path)
                for path in changed_oracle_files(review_repo_root, base_commit)
            }
            oracle_files = [
                path for path in all_oracle_files if path in changed_files
            ]
        else:
            oracle_files = all_oracle_files

        failed_stage = "oracle snapshot 作成"
        backup_parent_dir = _review_oracles_backup_parent_dir(review_repo_root)
        with tempfile.TemporaryDirectory(
            prefix="cmoc-review-oracles-backup-",
            dir=backup_parent_dir,
        ) as backup_dir:
            # Codex CLI に読ませる内容を review worktree 内の oracles に固定する。
            backup_snapshot = _create_oracle_evaluation_snapshot(
                review_repo_root,
                all_review_oracle_files,
                Path(backup_dir),
                display_repo_root=repo_root,
            )

            failed_stage = "INDEX.md メンテナンス"
            start_step(timer, 3, 6, "INDEX.md メンテナンス")
            _maintain_indexes_after_oracle_snapshot(review_repo_root)
            _restore_oracle_snapshot_to_review_worktree(
                review_repo_root,
                backup_snapshot,
            )
            oracle_snapshot = _create_worktree_oracle_evaluation_snapshot(
                review_repo_root,
                all_review_oracle_files,
                display_repo_root=repo_root,
            )

            # oracle ファイルごとに所見を列挙し、所見単位で検証・判定する。
            failed_stage = "oracle ファイル評価"
            start_step(timer, 4, 6, "所見リスト処理")
            for index, oracle_file in enumerate(oracle_files, start=1):
                print(
                    f"oracle 所見列挙 ({index}/{len(oracle_files)}) "
                    f"{oracle_file}"
                )
            evaluations = _run_findings_pipeline(
                review_repo_root,
                repo_root,
                oracle_files,
                enumerate_findings_loop,
                merge_findings_loop,
                refine_findings_loop,
                oracle_snapshot,
                progress_evaluations=evaluations,
            )

            failed_stage = "review branch merge"
            start_step(timer, 5, 6, "review branch merge")
            _merge_review_branch_into_session(repo_root, branch_name, review_plan)
            review_join_commit = head_commit(repo_root)

            # 評価結果を 1 つの Markdown レポートとして保存する。
            failed_stage = "report 書き込み"
            start_step(timer, 6, 6, "report 書き込み")
            report_path = _write_report(
                state_root,
                mode,
                scope == "full",
                branch_name,
                cmoc_branch,
                base_commit,
                session_fork_commit,
                deleted_oracles,
                len(all_oracle_files),
                oracle_files,
                evaluations,
                scope,
                review_plan.review_branch,
                review_fork_commit,
                review_join_commit,
            )
    except Exception as error:
        try:
            report_path = _write_error_report(
                session_state_root(repo_root),
                mode,
                scope == "full",
                branch_name,
                cmoc_branch,
                base_commit,
                session_fork_commit,
                deleted_oracles,
                len(all_oracle_files) if all_oracle_files_known else None,
                oracle_files,
                evaluations,
                scope,
                review_plan.review_branch if review_plan is not None else None,
                review_fork_commit,
                review_join_commit,
                failed_stage,
                error,
            )
        except Exception as report_error:
            error.add_note(
                "review oracles error report generation also failed: "
                f"{type(report_error).__name__}: {report_error}"
            )
            _print_error_report_fallback(
                repo_root,
                mode,
                full,
                branch_name,
                cmoc_branch,
                base_commit,
                review_start_commit,
                deleted_oracles,
                len(all_oracle_files) if all_oracle_files_known else None,
                oracle_files,
                evaluations,
                failed_stage,
                error,
                report_error,
            )
        else:
            print(str(report_path))
        raise
    print(str(report_path))


def _normalize_review_oracles_scope(
    scope: ReviewOraclesScope,
    full: bool | None,
) -> ReviewOraclesScope:
    """正式 scope と旧 `--full` alias を 1 つの scope 値へ正規化する。"""
    if scope not in {"session", "full"}:
        raise ValueError("--scope must be one of: session, full.")
    if full is True:
        return "full"
    return scope


def _validate_review_oracles_preconditions(repo_root: Path) -> str:
    """review oracles の session / clean worktree 前提条件を検証する。"""
    branch_name = current_branch(repo_root)
    if not is_session_branch(branch_name):
        raise CmocError(
            "`cmoc review oracles` は session branch 上で実行してください。",
            [
                "`cmoc session fork` で作成した branch へ移動してから再実行してください。",
                "通常 branch や apply branch 上では、先に対象 session branch へ切り替えてください。",
            ],
            f"現在の branch: {branch_name or '(detached HEAD)'}",
        )

    session_id = session_id_from_branch(branch_name)
    state = read_session_state(session_state_root(repo_root), session_id)
    session = state.get("session")
    if not isinstance(session, dict):
        raise CmocError(
            "session state ファイルの形式が不正です。",
            [
                "state JSON の session セクションを確認して復旧してください。",
                "復旧できない場合は、現在の session を使わず新しい session を開始してください。",
            ],
            f"現在の branch: {branch_name}",
        )
    if session.get("state") != "active":
        raise CmocError(
            "active な session ではありません。",
            [
                "対象 session の state を確認してください。",
                "既に join または abandon 済みの場合は、新しい session を開始してください。",
            ],
            f"session.state: {session.get('state')}",
        )

    assert_no_uncommitted_changes(repo_root)
    return branch_name


def _validate_review_oracles_loop(value: int, option_name: str) -> None:
    """review oracles の各ループ回数が非負整数か検証する。"""
    if value < 0:
        raise ValueError(f"{option_name} must be greater than or equal to 0.")


def _validate_repeat_improve_issues_list(value: int) -> None:
    """旧 option 名の問題点リスト改善回数を互換検証する。"""
    _validate_review_oracles_loop(value, "--repeat-improve-issues-list")


def _create_review_worktree(
    repo_root: Path,
    session_id: str,
    session_head_commit: str,
) -> _ReviewWorktreePlan:
    """session HEAD から review branch と専用 worktree を作成する。"""
    last_plan = _plan_review_worktree(repo_root, session_id)
    for attempt in range(1, 11):
        plan = (
            last_plan
            if attempt == 1
            else _plan_review_worktree(repo_root, session_id)
        )
        last_plan = plan
        print(
            "review worktree 作成試行 "
            f"({attempt}/10) {plan.review_branch}"
        )
        branch_result = run_git(
            repo_root,
            ["branch", plan.review_branch, session_head_commit],
            check=False,
        )
        if branch_result.returncode != 0:
            sleep(0.001)
            continue
        worktree_result = run_git(
            repo_root,
            ["worktree", "add", str(plan.review_worktree), plan.review_branch],
            check=False,
        )
        if worktree_result.returncode == 0:
            return plan
        cleanup_result = run_git(
            repo_root,
            ["branch", "-D", plan.review_branch],
            check=False,
        )
        if cleanup_result.returncode != 0:
            raise RuntimeError(
                "\n".join(
                    [
                        "review worktree 作成失敗後の branch cleanup に失敗しました。",
                        f"review_branch: {plan.review_branch}",
                        f"review_worktree: {plan.review_worktree}",
                        "worktree add failure:",
                        _format_git_failure(worktree_result),
                        "branch cleanup failure:",
                        _format_git_failure(cleanup_result),
                    ]
                )
            )
        sleep(0.001)
    raise RuntimeError(
        "\n".join(
            [
                "リトライ後も一意な review worktree を作成できませんでした。",
                f"last_review_branch: {last_plan.review_branch}",
                f"last_review_worktree: {last_plan.review_worktree}",
            ]
        )
    )


def _plan_review_worktree(repo_root: Path, session_id: str) -> _ReviewWorktreePlan:
    """次に作成を試みる review run id、branch、worktree path を組み立てる。"""
    review_run_id = make_timestamp()
    review_branch = f"{REVIEW_BRANCH_PREFIX}{session_id}/{review_run_id}"
    review_worktree = repo_root / ".cmoc" / "worktrees" / session_id / review_run_id
    return _ReviewWorktreePlan(review_run_id, review_branch, review_worktree)


def _merge_review_branch_into_session(
    repo_root: Path,
    session_branch: str,
    review_plan: _ReviewWorktreePlan,
) -> None:
    """review branch の INDEX.md 更新を session branch へ自動 merge する。"""
    assert_no_uncommitted_changes(repo_root)
    assert_no_uncommitted_changes(review_plan.review_worktree)
    run_git(repo_root, ["switch", session_branch])
    merge_result = run_git(
        repo_root,
        ["merge", "--no-ff", review_plan.review_branch],
        check=False,
    )
    if merge_result.returncode == 0:
        return

    unmerged = _unmerged_paths(repo_root)
    index_conflicts = [path for path in unmerged if _is_index_path(path)]
    non_index_conflicts = [path for path in unmerged if not _is_index_path(path)]
    if index_conflicts:
        _resolve_index_conflicts_with_session_side(repo_root, index_conflicts)
        unmerged = _unmerged_paths(repo_root)
        non_index_conflicts = [
            path for path in unmerged if not _is_index_path(path)
        ]
    if non_index_conflicts or not index_conflicts:
        detail = _unmerged_paths_detail(repo_root, unmerged)
        if not detail:
            detail = merge_result.stderr.strip()
        raise CmocError(
            "review branch の merge で conflict が発生しました。",
            [
                "cmoc は review branch の INDEX.md conflict だけを自動解消します。",
                "git status を確認し、手動で merge 状態を解消してください。",
            ],
            detail,
        )

    commit_result = run_git(repo_root, ["commit", "--no-edit"], check=False)
    if commit_result.returncode != 0:
        detail = "\n".join(
            [
                merge_result.stderr.strip(),
                commit_result.stderr.strip(),
            ]
        ).strip()
        raise CmocError(
            "INDEX.md conflict 解消後の review merge commit に失敗しました。",
            [
                "git status を確認し、merge 状態を手動で完了してください。",
                "不要な merge 状態であれば `git merge --abort` で戻してください。",
            ],
            detail,
        )


def _resolve_index_conflicts_with_session_side(
    repo_root: Path,
    paths: list[str],
) -> None:
    """INDEX.md conflict を session branch 側の内容で解消する。"""
    for path in sorted(paths):
        run_git(repo_root, ["checkout", "--ours", "--", path], check=False)
    run_git(repo_root, ["add", "--", *sorted(paths)])


def _unmerged_paths(repo_root: Path) -> list[str]:
    """unmerged path を git から取得する。"""
    result = run_git(repo_root, ["diff", "--name-only", "-z", "--diff-filter=U"])
    return [path for path in result.stdout.split("\0") if path]


def _unmerged_paths_detail(repo_root: Path, unmerged: list[str]) -> str:
    """unmerged path detail をユーザー表示用に整形する。"""
    return "\n".join(str((repo_root / path).resolve()) for path in unmerged)


def _is_index_path(path: str) -> bool:
    """cmoc が再生成可能な INDEX.md path か判定する。"""
    return Path(path).name == "INDEX.md"


def _format_git_failure(result: object) -> str:
    """git 失敗時の診断情報をユーザー向け detail に載せる。"""
    return "\n".join(
        [
            f"returncode: {getattr(result, 'returncode', '')}",
            f"stdout: {getattr(result, 'stdout', '').strip()}",
            f"stderr: {getattr(result, 'stderr', '').strip()}",
        ]
    )


def _owner_path_for_worktree_path(
    owner_repo_root: Path,
    worktree_root: Path,
    path: Path,
) -> Path:
    """review worktree 内 path に対応する呼び出し元 repo path を返す。"""
    return (
        owner_repo_root / path.resolve().relative_to(worktree_root.resolve())
    ).resolve()


def _maintain_indexes_after_oracle_snapshot(repo_root: Path) -> bool:
    """評価 snapshot とは分離して INDEX.md をメンテナンスする。"""
    return maintain_indexes(repo_root)


def _review_oracles_backup_parent_dir(review_repo_root: Path) -> Path:
    """review run 中の一時退避先を review worktree 内に閉じ込める。"""
    parent_dir = review_repo_root / _REVIEW_ORACLES_TMP_DIR
    parent_dir.mkdir(parents=True, exist_ok=True)
    return parent_dir


def _create_oracle_evaluation_snapshot(
    repo_root: Path,
    oracle_files: list[Path],
    snapshot_root: Path,
    *,
    display_repo_root: Path | None = None,
) -> _OracleEvaluationSnapshot:
    """開始時点の oracles tree を一時 copy として固定する。"""
    display_root = (display_repo_root or repo_root).resolve()
    original_oracle_root = (repo_root / "oracles").resolve()
    display_oracle_root = (display_root / "oracles").resolve()
    snapshot_oracle_root = snapshot_root / "oracles"
    if original_oracle_root.exists():
        _copy_oracles_tree_snapshot(original_oracle_root, snapshot_oracle_root)
    else:
        snapshot_oracle_root.mkdir(parents=True)

    reference_files = {path.resolve() for path in oracle_files}
    if display_root != repo_root.resolve():
        reference_files = {
            _owner_path_for_worktree_path(display_root, repo_root, path)
            for path in reference_files
        }
    reference_files.update(
        _original_path_for_snapshot_path(
            display_root,
            snapshot_oracle_root,
            index_path,
        )
        for index_path in snapshot_oracle_root.rglob("INDEX.md")
        if index_path.is_file()
    )
    return _OracleEvaluationSnapshot(
        original_repo_root=display_root,
        original_oracle_root=display_oracle_root,
        snapshot_root=snapshot_root.resolve(),
        snapshot_oracle_root=snapshot_oracle_root.resolve(),
        oracle_files=frozenset(reference_files - {
            _original_path_for_snapshot_path(
                display_root,
                snapshot_oracle_root,
                index_path,
            )
            for index_path in snapshot_oracle_root.rglob("INDEX.md")
            if index_path.is_file()
        }),
        reference_files=frozenset(reference_files),
    )


def _create_worktree_oracle_evaluation_snapshot(
    repo_root: Path,
    oracle_files: list[Path],
    *,
    display_repo_root: Path | None = None,
) -> _OracleEvaluationSnapshot:
    """review worktree の oracles tree を Codex CLI の読み取り対象にする。"""
    display_root = (display_repo_root or repo_root).resolve()
    worktree_root = repo_root.resolve()
    worktree_oracle_root = (worktree_root / "oracles").resolve()
    display_oracle_root = (display_root / "oracles").resolve()

    reference_files = {path.resolve() for path in oracle_files}
    if display_root != worktree_root:
        reference_files = {
            _owner_path_for_worktree_path(display_root, worktree_root, path)
            for path in reference_files
        }
    if worktree_oracle_root.exists():
        reference_files.update(
            _owner_path_for_worktree_path(display_root, worktree_root, index_path)
            for index_path in worktree_oracle_root.rglob("INDEX.md")
            if index_path.is_file()
        )

    index_files = {
        path
        for path in reference_files
        if path.name == "INDEX.md"
    }
    return _OracleEvaluationSnapshot(
        original_repo_root=display_root,
        original_oracle_root=display_oracle_root,
        snapshot_root=worktree_root,
        snapshot_oracle_root=worktree_oracle_root,
        oracle_files=frozenset(reference_files - index_files),
        reference_files=frozenset(reference_files),
    )


def _restore_oracle_snapshot_to_review_worktree(
    repo_root: Path,
    snapshot: _OracleEvaluationSnapshot,
) -> None:
    """開始時点の oracle 本文とメンテナンス後 INDEX.md を worktree へ固定する。"""
    original_oracle_root = (repo_root / "oracles").resolve()
    maintained_indexes = _read_maintained_index_files(original_oracle_root)

    if original_oracle_root.exists():
        shutil.rmtree(original_oracle_root)
    if snapshot.snapshot_oracle_root.exists():
        _copy_oracles_tree_snapshot(
            snapshot.snapshot_oracle_root,
            original_oracle_root,
        )
    else:
        original_oracle_root.mkdir(parents=True)

    for index_path in original_oracle_root.rglob("INDEX.md"):
        if not index_path.is_file():
            continue
        relative_path = index_path.relative_to(original_oracle_root)
        if relative_path not in maintained_indexes:
            index_path.unlink()
    for relative_path, content in maintained_indexes.items():
        index_path = original_oracle_root / relative_path
        index_path.parent.mkdir(parents=True, exist_ok=True)
        index_path.write_bytes(content)

    status = run_git(
        repo_root,
        ["status", "--porcelain", "--", "oracles"],
    ).stdout
    if not status:
        return
    run_git(repo_root, ["add", "-A", "--", "oracles"])
    run_git(
        repo_root,
        ["commit", "-m", "Restore review oracle evaluation snapshot"],
    )


def _read_maintained_index_files(oracle_root: Path) -> dict[Path, bytes]:
    """メンテナンス後の INDEX.md 内容を oracle root 相対 path で読む。"""
    if not oracle_root.exists():
        return {}
    return {
        index_path.relative_to(oracle_root): index_path.read_bytes()
        for index_path in oracle_root.rglob("INDEX.md")
        if index_path.is_file()
    }


def _copy_oracles_tree_snapshot(source_root: Path, destination_root: Path) -> None:
    """oracles tree の file 内容を symlink 参照先も含めて固定 copy する。"""
    destination_root.mkdir(parents=True)
    for source_path in source_root.rglob("*"):
        relative_path = source_path.relative_to(source_root)
        destination_path = destination_root / relative_path
        if source_path.is_dir():
            destination_path.mkdir(exist_ok=True)
            continue
        if not source_path.is_file():
            continue
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, destination_path, follow_symlinks=True)


def _original_path_for_snapshot_path(
    repo_root: Path,
    snapshot_oracle_root: Path,
    snapshot_path: Path,
) -> Path:
    """snapshot 内 path に対応する元 repo 側の絶対 path を返す。"""
    return (
        repo_root
        / "oracles"
        / snapshot_path.relative_to(snapshot_oracle_root)
    ).resolve()


def _snapshot_path_for_original_path(
    snapshot: _OracleEvaluationSnapshot,
    original_path: Path,
) -> Path:
    """元 repo 側 oracle path に対応する snapshot 側 path を返す。"""
    return (
        snapshot.snapshot_oracle_root
        / original_path.resolve().relative_to(snapshot.original_oracle_root)
    ).resolve()


def _run_findings_pipeline(
    execution_repo_root: Path,
    display_repo_root: Path,
    oracle_files: list[Path],
    enumerate_findings_loop: int,
    merge_findings_loop: int,
    refine_findings_loop: int,
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
    progress_evaluations: list[dict[str, object]] | None = None,
) -> list[dict[str, object]]:
    """仕様どおりの所見 list pipeline を実行し、既存 report 形式へ変換する。"""
    findings: list[_Finding] = []
    finding_ids = _FindingIdAllocator.from_findings(findings)
    dirty_files = {str(path.resolve()): True for path in oracle_files}

    for _ in range(enumerate_findings_loop):
        targets = [
            path for path in oracle_files if dirty_files.get(str(path.resolve()), False)
        ]
        if not targets:
            break
        legacy_evaluations: list[dict[str, object]] = []
        legacy_payload_seen = False
        with ThreadPoolExecutor(max_workers=len(targets)) as executor:
            futures = [
                executor.submit(
                    copy_context().run,
                    _enumerate_oracle_findings,
                    execution_repo_root,
                    display_repo_root,
                    oracle_file,
                    findings,
                    oracle_snapshot,
                )
                for oracle_file in targets
            ]
            for oracle_file, future in zip(targets, futures):
                new_findings = future.result()
                legacy_items = _legacy_issues_from_enumerate_result(new_findings)
                if legacy_items is not None:
                    legacy_payload_seen = True
                    record = _evaluation_payload_to_record(
                        {"issues": legacy_items},
                        display_repo_root,
                        oracle_file,
                    )
                    legacy_evaluations.append(record)
                    if progress_evaluations is not None:
                        progress_evaluations.append(record)
                    if not legacy_items:
                        dirty_files[str(oracle_file.resolve())] = False
                    continue
                if new_findings:
                    _append_new_findings(findings, new_findings, finding_ids)
                else:
                    dirty_files[str(oracle_file.resolve())] = False
        if legacy_payload_seen:
            return _improve_evaluations(
                execution_repo_root,
                display_repo_root,
                legacy_evaluations,
                refine_findings_loop,
                oracle_snapshot,
            )
        if not any(dirty_files.values()):
            break
        findings = _merge_findings_loop(
            execution_repo_root,
            display_repo_root,
            findings,
            finding_ids,
            merge_findings_loop,
            oracle_snapshot,
        )

    findings = _validate_findings_loop(
        execution_repo_root,
        display_repo_root,
        findings,
        refine_findings_loop,
        oracle_snapshot,
    )
    findings = _judge_findings(
        execution_repo_root,
        display_repo_root,
        findings,
        oracle_snapshot,
    )
    return _findings_to_evaluations(display_repo_root, oracle_files, findings)


def _enumerate_oracle_findings(
    execution_repo_root: Path,
    display_repo_root: Path,
    oracle_file: Path,
    existing_findings: list[_Finding],
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> list[dict[str, object]]:
    """1 oracle ファイルから新規所見を列挙する。"""
    payload = parse_json_object(
        run_codex_exec(
            execution_repo_root,
            _enumerate_findings_prompt(
                display_repo_root,
                oracle_file,
                existing_findings,
                oracle_snapshot,
            ),
            purpose=f"oracle 評価 {oracle_file.relative_to(display_repo_root)}",
            read_only=True,
            expect_json=True,
            output_schema=_ENUMERATE_FINDINGS_OUTPUT_SCHEMA,
            json_validator=lambda value: _validate_enumerate_findings_payload(
                value,
                display_repo_root,
                oracle_snapshot,
            ),
        )
    )
    if "issues" in payload:
        return [{"__legacy_issues": payload["issues"]}]
    findings = payload["findings"]
    if not isinstance(findings, list):
        raise ValueError("findings must be a list.")
    return [finding for finding in findings if isinstance(finding, dict)]


def _append_new_findings(
    findings: list[_Finding],
    payloads: list[dict[str, object]],
    finding_ids: _FindingIdAllocator,
) -> None:
    """新規所見に安定 ID を付与して所見 list へ追加する。"""
    for payload in payloads:
        findings.append(_finding_from_payload(payload, finding_ids.allocate()))


def _merge_findings_loop(
    execution_repo_root: Path,
    display_repo_root: Path,
    findings: list[_Finding],
    finding_ids: _FindingIdAllocator,
    merge_findings_loop: int,
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> list[_Finding]:
    """Codex CLI の編集操作を所見 list に反映する。"""
    if not findings:
        return findings
    current = list(findings)
    for index in range(merge_findings_loop):
        payload = parse_json_object(
            run_codex_exec(
                execution_repo_root,
                _merge_findings_prompt(display_repo_root, current, oracle_snapshot),
                purpose=f"oracle 所見リストマージ {index + 1}",
                read_only=True,
                expect_json=True,
                output_schema=_MERGE_FINDINGS_OUTPUT_SCHEMA,
                model=FRONTIER_MODEL,
                reasoning_effort=FRONTIER_HIGH_REASONING_EFFORT,
                json_validator=lambda value: _validate_merge_findings_payload(
                    value,
                    display_repo_root,
                    {finding.finding_id for finding in current},
                    oracle_snapshot,
                ),
            )
        )
        if "issues" in payload:
            current = [
                _finding_from_payload(_issue_to_finding_payload(issue), item_index)
                for item_index, issue in enumerate(payload["issues"], start=1)
                if isinstance(issue, dict)
            ]
            finding_ids.next_index = _FindingIdAllocator.from_findings(
                current
            ).next_index
            break
        operations = payload["operations"]
        if not isinstance(operations, list):
            raise ValueError("operations must be a list.")
        if not operations:
            break
        current = _apply_merge_operations(current, operations, finding_ids)
    return current


def _validate_findings_loop(
    execution_repo_root: Path,
    display_repo_root: Path,
    findings: list[_Finding],
    refine_findings_loop: int,
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> list[_Finding]:
    """各所見の challenger / advocate reason を反復収集する。"""
    dirty = {finding.finding_id: True for finding in findings}
    for _ in range(refine_findings_loop):
        targets = [finding for finding in findings if dirty.get(finding.finding_id)]
        if not targets:
            break
        with ThreadPoolExecutor(max_workers=len(targets) * 2) as executor:
            futures: list[tuple[_Finding, str, Future[list[str]]]] = []
            for finding in targets:
                futures.append(
                    (
                        finding,
                        "challenger",
                        executor.submit(
                            copy_context().run,
                            _validate_finding_reasons,
                            execution_repo_root,
                            display_repo_root,
                            finding,
                            "challenger",
                            oracle_snapshot,
                        ),
                    )
                )
                futures.append(
                    (
                        finding,
                        "advocate",
                        executor.submit(
                            copy_context().run,
                            _validate_finding_reasons,
                            execution_repo_root,
                            display_repo_root,
                            finding,
                            "advocate",
                            oracle_snapshot,
                        ),
                    )
                )
            changed = {finding.finding_id: False for finding in targets}
            for finding, role, future in futures:
                reasons = future.result()
                if role == "challenger":
                    added = _extend_unique(finding.challenger_reasons, reasons)
                else:
                    added = _extend_unique(finding.advocate_reasons, reasons)
                changed[finding.finding_id] = changed[finding.finding_id] or added
            for finding in targets:
                if not changed[finding.finding_id]:
                    dirty[finding.finding_id] = False
        if not any(dirty.values()):
            break
    return findings


def _validate_finding_reasons(
    execution_repo_root: Path,
    display_repo_root: Path,
    finding: _Finding,
    role: Literal["challenger", "advocate"],
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> list[str]:
    """1 所見について advocate/challenger reason を取得する。"""
    if role == "challenger":
        schema = _VALIDATE_FINDINGS_CHALLENGER_OUTPUT_SCHEMA
        purpose_role = "不採用理由"
    else:
        schema = _VALIDATE_FINDINGS_ADVOCATE_OUTPUT_SCHEMA
        purpose_role = "採用理由"
    payload = parse_json_object(
        run_codex_exec(
            execution_repo_root,
            _validate_finding_prompt(display_repo_root, finding, role, oracle_snapshot),
            purpose=f"oracle 所見検証 {purpose_role} {finding.finding_id}",
            read_only=True,
            expect_json=True,
            output_schema=schema,
            model=FRONTIER_MODEL,
            reasoning_effort=FRONTIER_HIGH_REASONING_EFFORT,
            json_validator=_validate_reasons_payload,
        )
    )
    if "issues" in payload:
        return []
    reasons = payload["reasons"]
    if not isinstance(reasons, list):
        raise ValueError("reasons must be a list.")
    return [reason for reason in reasons if isinstance(reason, str)]


def _judge_findings(
    execution_repo_root: Path,
    display_repo_root: Path,
    findings: list[_Finding],
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> list[_Finding]:
    """各所見を人間に提示すべきか判定する。"""
    for finding in findings:
        payload = parse_json_object(
            run_codex_exec(
                execution_repo_root,
                _judge_finding_prompt(display_repo_root, finding, oracle_snapshot),
                purpose=f"oracle 所見判定 {finding.finding_id}",
                read_only=True,
                expect_json=True,
                output_schema=_JUDGE_FINDINGS_OUTPUT_SCHEMA,
                model=FRONTIER_MODEL,
                reasoning_effort=FRONTIER_HIGH_REASONING_EFFORT,
                json_validator=_validate_judge_findings_payload,
            )
        )
        if "issues" in payload:
            finding.judge_verdict = "accept"
            finding.judge_reason = "旧 issues payload 互換入力のため採用扱いにしました。"
            continue
        finding.judge_verdict = payload["verdict"]  # type: ignore[assignment]
        finding.judge_reason = str(payload["reason"])
    return findings


def _enumerate_findings_prompt(
    repo_root: Path,
    oracle_file: Path,
    existing_findings: list[_Finding],
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> str:
    """新規所見列挙用 prompt を組み立てる。"""
    concrete_repo_root = repo_root.resolve()
    concrete_oracle_root = (concrete_repo_root / "oracles").resolve()
    readable_oracle_file = oracle_file.resolve()
    readable_oracle_root = concrete_oracle_root
    readable_oracle_index = (concrete_oracle_root / "INDEX.md").resolve()
    if oracle_snapshot is not None:
        readable_oracle_file = _snapshot_path_for_original_path(
            oracle_snapshot,
            oracle_file,
        )
        readable_oracle_root = oracle_snapshot.snapshot_oracle_root
        readable_oracle_index = (
            oracle_snapshot.snapshot_oracle_root / "INDEX.md"
        ).resolve()
    relevant_findings = [
        _finding_to_payload(finding)
        for finding in existing_findings
        if _finding_may_relate_to_oracle(finding, oracle_file)
    ]
    return "\n".join(
        [
            "あなたはソフトウェア仕様のレビュー担当です。",
            f"`{concrete_repo_root}` 内の仕様ファイル `{oracle_file.resolve()}` から新規所見を列挙してください。",
            "完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです。",
            "所見は fatal または minor だけを対象にしてください。",
            "fatal は仕様断片同士の明確な矛盾、または実装者の裁量では解消不能な問題です。",
            "minor は誤字、脱字、助詞抜け、用語不統一、表記揺れ、typo などの単純な問題です。",
            "oracles ファイルだけから問題と言い切れないものは所見にしないでください。",
            f"評価時に読む対象ファイルは、開始時点の内容を固定したコピー `{readable_oracle_file}` です。",
            f"`{readable_oracle_root}` 配下の仕様ファイルと INDEX.md だけを読んでください。",
            f"`{readable_oracle_index}` から始まる INDEX.md の Summary /",
            "Read this when / Do not read this when を根拠に、",
            "関連する仕様ファイルを選定してください。",
            f"`{concrete_oracle_root}` は path 変換のためにだけ使い、読まないでください。",
            f"出力する oracle_path は `{concrete_oracle_root}` 配下の絶対パスにしてください。",
            "既知所見と内容的に重複する所見は返さないでください。",
            "既知所見:",
            json.dumps(relevant_findings, ensure_ascii=False, indent=2),
            f"`{concrete_repo_root / 'memo'}` は読み書き禁止です。",
            "ファイル編集は禁止です。",
        ]
    )


def _merge_findings_prompt(
    repo_root: Path,
    findings: list[_Finding],
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> str:
    """所見 list merge 用 prompt を組み立てる。"""
    concrete_repo_root = repo_root.resolve()
    concrete_oracle_root = (concrete_repo_root / "oracles").resolve()
    readable_oracle_root = (
        oracle_snapshot.snapshot_oracle_root
        if oracle_snapshot is not None
        else concrete_oracle_root
    )
    return "\n".join(
        [
            "あなたはソフトウェア仕様レビュー結果の整理担当です。",
            "所見リストの重複と矛盾を解消する編集操作を返してください。",
            "完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです。",
            "変更不要なら operations: [] を返してください。",
            "operation は finding_id を target_ids で参照してください。",
            f"必要に応じて `{readable_oracle_root}` 配下の仕様ファイルと INDEX.md だけを読んでください。",
            f"`{concrete_oracle_root}` は path 変換のためにだけ使い、読まないでください。",
            "現状の所見リスト:",
            json.dumps(
                [_finding_to_payload(finding) for finding in findings],
                ensure_ascii=False,
                indent=2,
            ),
            f"`{concrete_repo_root / 'memo'}` は読み書き禁止です。",
            "ファイル編集は禁止です。",
        ]
    )


def _validate_finding_prompt(
    repo_root: Path,
    finding: _Finding,
    role: Literal["challenger", "advocate"],
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> str:
    """所見検証用 prompt を組み立てる。"""
    concrete_repo_root = repo_root.resolve()
    concrete_oracle_root = (concrete_repo_root / "oracles").resolve()
    readable_oracle_root = (
        oracle_snapshot.snapshot_oracle_root
        if oracle_snapshot is not None
        else concrete_oracle_root
    )
    if role == "challenger":
        task = "その所見が妥当ではない理由を新規に列挙してください。"
        existing = finding.challenger_reasons
        opposite = finding.advocate_reasons
    else:
        task = "その所見が妥当である理由を新規に列挙してください。"
        existing = finding.advocate_reasons
        opposite = finding.challenger_reasons
    return "\n".join(
        [
            "あなたはソフトウェア仕様レビュー所見の検証担当です。",
            task,
            "完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです。",
            "理由には具体的な根拠を必ず含めてください。",
            "「かもしれない」「可能性がある」などの推測だけを根拠にした理由は返さないでください。",
            "反対側の既存理由がある場合は、対応する反対側理由への反論を含めてください。",
            "既存理由と重複する理由は返さないでください。",
            f"`{readable_oracle_root}` 配下の仕様ファイルと INDEX.md だけを読んでください。",
            f"`{concrete_oracle_root}` は path 変換のためにだけ使い、読まないでください。",
            "対象所見:",
            json.dumps(_finding_to_payload(finding), ensure_ascii=False, indent=2),
            "既存理由:",
            json.dumps(existing, ensure_ascii=False, indent=2),
            "反対側の既存理由:",
            json.dumps(opposite, ensure_ascii=False, indent=2),
            f"`{concrete_repo_root / 'memo'}` は読み書き禁止です。",
            "ファイル編集は禁止です。",
        ]
    )


def _judge_finding_prompt(
    repo_root: Path,
    finding: _Finding,
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> str:
    """所見判定用 prompt を組み立てる。"""
    concrete_repo_root = repo_root.resolve()
    concrete_oracle_root = (concrete_repo_root / "oracles").resolve()
    readable_oracle_root = (
        oracle_snapshot.snapshot_oracle_root
        if oracle_snapshot is not None
        else concrete_oracle_root
    )
    return "\n".join(
        [
            "あなたはソフトウェア仕様レビュー所見の判定担当です。",
            "この所見を人間に提示すべきなら accept、提示すべきでないなら reject を返してください。",
            "完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです。",
            f"`{readable_oracle_root}` 配下の仕様ファイルと INDEX.md だけを読んでください。",
            f"`{concrete_oracle_root}` は path 変換のためにだけ使い、読まないでください。",
            "対象所見:",
            json.dumps(_finding_to_payload(finding), ensure_ascii=False, indent=2),
            "妥当ではない理由:",
            json.dumps(finding.challenger_reasons, ensure_ascii=False, indent=2),
            "妥当である理由:",
            json.dumps(finding.advocate_reasons, ensure_ascii=False, indent=2),
            f"`{concrete_repo_root / 'memo'}` は読み書き禁止です。",
            "ファイル編集は禁止です。",
        ]
    )


def _validate_enumerate_findings_payload(
    value: object,
    repo_root: Path,
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> None:
    """enumerate_findings の payload を検査する。"""
    if not isinstance(value, dict):
        raise ValueError("Expected JSON object.")
    if set(value) == {"issues"}:
        _validate_evaluation_issues(value["issues"], repo_root, oracle_snapshot)
        return
    if set(value) != {"findings"}:
        raise ValueError("Enumerate findings payload keys do not match schema.")
    _validate_finding_payloads(value["findings"], repo_root, oracle_snapshot)


def _validate_merge_findings_payload(
    value: object,
    repo_root: Path,
    known_finding_ids: set[str],
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> None:
    """merge_findings の payload を検査する。"""
    if not isinstance(value, dict):
        raise ValueError("Expected JSON object.")
    if set(value) == {"issues"}:
        _validate_evaluation_issues(value["issues"], repo_root, oracle_snapshot)
        return
    if set(value) != {"operations"}:
        raise ValueError("Merge findings payload keys do not match schema.")
    operations = value["operations"]
    if not isinstance(operations, list):
        raise ValueError("operations must be a list.")
    for index, operation in enumerate(operations):
        if not isinstance(operation, dict):
            raise ValueError(f"operations[{index}] must be an object.")
        if set(operation) != {"kind", "target_ids", "finding"}:
            raise ValueError(f"operations[{index}] keys do not match schema.")
        if operation["kind"] not in {"delete", "replace", "merge"}:
            raise ValueError(f"operations[{index}].kind is invalid.")
        target_ids = operation["target_ids"]
        if not isinstance(target_ids, list) or not target_ids:
            raise ValueError(f"operations[{index}].target_ids is invalid.")
        for target_id in target_ids:
            if target_id not in known_finding_ids:
                raise ValueError(f"operations[{index}].target_ids is unknown.")
        if operation["kind"] == "delete":
            if operation["finding"] is not None:
                raise ValueError(f"operations[{index}].finding must be null.")
        else:
            _validate_finding_payloads([operation["finding"]], repo_root, oracle_snapshot)


def _validate_finding_payloads(
    findings: object,
    repo_root: Path,
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> None:
    """finding item の Python 側の最小検査を行う。"""
    if not isinstance(findings, list):
        raise ValueError("findings must be a list.")
    for index, finding in enumerate(findings):
        if not isinstance(finding, dict):
            raise ValueError(f"findings[{index}] must be an object.")
        if set(finding) != {"severity", "title", "oracle_path", "reason"}:
            raise ValueError(f"findings[{index}] keys do not match schema.")
        if finding["severity"] not in set(_FINDING_SEVERITY_ORDER):
            raise ValueError(f"findings[{index}].severity is invalid.")
        _require_absolute_oracle_file(
            finding["oracle_path"],
            repo_root,
            f"findings[{index}].oracle_path",
            oracle_snapshot,
        )
        for key in ["title", "reason"]:
            if not isinstance(finding[key], str) or not str(finding[key]).strip():
                raise ValueError(f"findings[{index}].{key} must be a non-empty string.")


def _validate_reasons_payload(value: object) -> None:
    """validate_findings_* の payload を検査する。"""
    if not isinstance(value, dict):
        raise ValueError("Expected JSON object.")
    if set(value) == {"issues"}:
        return
    if set(value) != {"reasons"}:
        raise ValueError("Reasons payload keys do not match schema.")
    if not isinstance(value["reasons"], list):
        raise ValueError("reasons must be a list.")
    for index, reason in enumerate(value["reasons"]):
        if not isinstance(reason, str):
            raise ValueError(f"reasons[{index}] must be a string.")
        if not reason.strip():
            raise ValueError(f"reasons[{index}] must be a non-empty string.")
        if _contains_speculative_reason_phrase(reason):
            raise ValueError(f"reasons[{index}] contains speculative wording.")


def _contains_speculative_reason_phrase(reason: str) -> bool:
    """理由の根拠として禁止する推測表現を最小限に検出する。"""
    return any(phrase in reason for phrase in _SPECULATIVE_REASON_PHRASES)


def _validate_judge_findings_payload(value: object) -> None:
    """judge_findings の payload を検査する。"""
    if not isinstance(value, dict):
        raise ValueError("Expected JSON object.")
    if set(value) == {"issues"}:
        return
    if set(value) != {"verdict", "reason"}:
        raise ValueError("Judge findings payload keys do not match schema.")
    if value["verdict"] not in set(_FINDING_VERDICT_ORDER):
        raise ValueError("verdict is invalid.")
    if not isinstance(value["reason"], str):
        raise ValueError("reason must be a string.")


def _finding_from_payload(payload: dict[str, object], index: int) -> _Finding:
    """schema payload から stable finding_id 付き Finding を作る。"""
    return _Finding(
        finding_id=f"FINDING-{index:04d}",
        severity=payload["severity"],  # type: ignore[arg-type]
        title=str(payload["title"]),
        oracle_path=str(Path(str(payload["oracle_path"])).resolve()),
        reason=str(payload["reason"]),
        challenger_reasons=[],
        advocate_reasons=[],
    )


def _parse_finding_id_index(finding_id: str) -> int | None:
    """FINDING-0001 形式の ID から number を取り出す。"""
    prefix = "FINDING-"
    if not finding_id.startswith(prefix):
        return None
    suffix = finding_id[len(prefix) :]
    if len(suffix) != 4 or not suffix.isdigit():
        return None
    return int(suffix)


def _finding_to_payload(finding: _Finding) -> dict[str, object]:
    """Codex CLI に渡す所見 payload を作る。"""
    return {
        "finding_id": finding.finding_id,
        "severity": finding.severity,
        "title": finding.title,
        "oracle_path": finding.oracle_path,
        "reason": finding.reason,
        "challenger_reasons": finding.challenger_reasons,
        "advocate_reasons": finding.advocate_reasons,
        "judge_verdict": finding.judge_verdict,
        "judge_reason": finding.judge_reason,
    }


def _legacy_issues_from_enumerate_result(
    findings: list[dict[str, object]],
) -> list[object] | None:
    """旧 issues payload 互換用 marker から issues を取り出す。"""
    if len(findings) != 1:
        return None
    marker = findings[0]
    if set(marker) != {"__legacy_issues"}:
        return None
    issues = marker["__legacy_issues"]
    if not isinstance(issues, list):
        raise ValueError("issues must be a list.")
    return issues


def _issue_to_finding_payload(issue: dict[str, object]) -> dict[str, object]:
    """旧 issues payload を enumerate_findings payload 相当に変換する。"""
    severity = "fatal" if issue.get("severity") == "fatal" else "minor"
    return {
        "severity": severity,
        "title": str(issue.get("title") or "Untitled finding"),
        "oracle_path": str(issue.get("oracle_path") or ""),
        "reason": str(issue.get("reason") or issue.get("problem") or ""),
    }


def _apply_merge_operations(
    findings: list[_Finding],
    operations: list[object],
    finding_ids: _FindingIdAllocator | None = None,
) -> list[_Finding]:
    """merge_findings operations を所見 list に適用する。"""
    current = list(findings)
    allocator = finding_ids or _FindingIdAllocator.from_findings(current)
    by_id = {finding.finding_id: finding for finding in current}
    for operation in operations:
        if not isinstance(operation, dict):
            continue
        target_ids = [
            target_id
            for target_id in operation.get("target_ids", [])
            if isinstance(target_id, str)
        ]
        target_positions = [
            index
            for index, finding in enumerate(current)
            if finding.finding_id in set(target_ids)
        ]
        if not target_positions:
            continue
        if operation["kind"] == "delete":
            current = [
                finding for finding in current if finding.finding_id not in target_ids
            ]
            continue
        payload = operation.get("finding")
        if not isinstance(payload, dict):
            continue
        if operation["kind"] == "replace" and len(target_ids) == 1:
            replacement = _finding_from_payload(payload, 1)
            replacement.finding_id = target_ids[0]
        else:
            replacement = _finding_from_payload(payload, allocator.allocate())
        for target_id in target_ids:
            old = by_id.get(target_id)
            if old is None:
                continue
            _extend_unique(replacement.challenger_reasons, old.challenger_reasons)
            _extend_unique(replacement.advocate_reasons, old.advocate_reasons)
        first_position = min(target_positions)
        current = [
            finding for finding in current if finding.finding_id not in target_ids
        ]
        current.insert(min(first_position, len(current)), replacement)
        by_id = {finding.finding_id: finding for finding in current}
    return current


def _findings_to_evaluations(
    repo_root: Path,
    oracle_files: list[Path],
    findings: list[_Finding],
) -> list[dict[str, object]]:
    """判定済み所見 list を report 用 evaluation list に変換する。"""
    result = [
        {
            "target_oracle_path": str(path.resolve()),
            "referenced_paths": [],
            "specification_only_basis": "",
            "issues": [],
        }
        for path in oracle_files
    ]
    if not result:
        return []
    target_to_index = {
        str(evaluation["target_oracle_path"]): index
        for index, evaluation in enumerate(result)
    }
    for finding in findings:
        issue = _finding_to_issue(repo_root, finding)
        index = target_to_index.get(str(Path(finding.oracle_path).resolve()), 0)
        result[index]["issues"].append(issue)
    return [_refresh_evaluation_metadata(evaluation) for evaluation in result]


def _finding_to_issue(repo_root: Path, finding: _Finding) -> dict[str, object]:
    """Finding を report renderer の issue 互換形式へ変換する。"""
    severity = "fatal" if finding.severity == "fatal" else "warning"
    judge_verdict = finding.judge_verdict or "accept"
    reason_parts = [finding.reason]
    if finding.advocate_reasons:
        reason_parts.append(
            "採用理由: " + " / ".join(finding.advocate_reasons)
        )
    if finding.challenger_reasons:
        reason_parts.append(
            "不採用理由: " + " / ".join(finding.challenger_reasons)
        )
    if finding.judge_reason:
        reason_parts.append(f"判定理由: {finding.judge_reason}")
    return {
        "severity": severity,
        "title": f"{finding.finding_id}: {finding.title}",
        "oracle_path": finding.oracle_path,
        "oracle_line_start": None,
        "oracle_line_end": None,
        "referenced_paths": [finding.oracle_path],
        "affected_workflow": "cmoc review oracles",
        "requirement": "oracles ファイルは fatal/minor の所見としてレビュー可能であること。",
        "problem": finding.reason,
        "reason": "\n".join(reason_parts),
        "suggested_oracle_change": "人間が該当 oracle 断片を確認してください。",
        "specification_only_basis": (
            f"`{repo_root / 'oracles'}` 配下の仕様ファイルと INDEX.md だけに基づく所見です。"
        ),
        "finding_id": finding.finding_id,
        "finding_severity": finding.severity,
        "judge_verdict": judge_verdict,
    }


def _finding_may_relate_to_oracle(finding: _Finding, oracle_file: Path) -> bool:
    """列挙 prompt に渡す既知所見を対象ファイル中心に絞る。"""
    try:
        return Path(finding.oracle_path).resolve() == oracle_file.resolve()
    except OSError:
        return False


def _extend_unique(target: list[str], values: list[str]) -> bool:
    """文字列 list に未登録値だけを追加し、追加有無を返す。"""
    changed = False
    seen = set(target)
    for value in values:
        if value in seen:
            continue
        target.append(value)
        seen.add(value)
        changed = True
    return changed


def _evaluate_oracle_file(
    execution_repo_root: Path,
    display_repo_root: Path,
    oracle_file: Path,
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> dict[str, object]:
    """1 oracle ファイルの評価を実行し、report 用レコードを返す。"""
    payload = parse_json_object(
        run_codex_exec(
            execution_repo_root,
            _evaluation_prompt(display_repo_root, oracle_file, oracle_snapshot),
            purpose=f"oracle 評価 {oracle_file.relative_to(display_repo_root)}",
            read_only=True,
            expect_json=True,
            output_schema=_EVALUATION_OUTPUT_SCHEMA,
            json_validator=lambda value: _validate_evaluation_payload(
                value,
                display_repo_root,
                oracle_file,
                oracle_snapshot,
            ),
        )
    )
    return _evaluation_payload_to_record(payload, display_repo_root, oracle_file)


def _append_evaluation_records_in_order(
    futures: list[Future[dict[str, object]]],
    evaluations: list[dict[str, object]],
) -> None:
    """並列評価結果を dispatch 時の順序で回収する。"""
    for future in futures:
        evaluations.append(future.result())


def _evaluation_prompt(
    repo_root: Path,
    oracle_file: Path,
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> str:
    """oracle 評価用 prompt を組み立てる。"""
    # Codex CLI には prompt だけで解釈できる具体的な絶対パスを渡す。
    concrete_repo_root = repo_root.resolve()
    concrete_oracle_file = oracle_file.resolve()
    concrete_oracle_root = (concrete_repo_root / "oracles").resolve()
    concrete_oracle_index = (concrete_oracle_root / "INDEX.md").resolve()
    readable_oracle_file = concrete_oracle_file
    readable_oracle_root = concrete_oracle_root
    readable_oracle_index = concrete_oracle_index
    if oracle_snapshot is not None:
        readable_oracle_file = _snapshot_path_for_original_path(
            oracle_snapshot,
            concrete_oracle_file,
        )
        readable_oracle_root = oracle_snapshot.snapshot_oracle_root
        readable_oracle_index = (
            oracle_snapshot.snapshot_oracle_root / "INDEX.md"
        ).resolve()

    # 仕様の構成順序に従い、完了条件を詳細指示より前に置く。
    lines = [
        "あなたはソフトウェア仕様のレビュー担当です。",
        f"`{concrete_repo_root}` 内の仕様ファイル "
        f"`{concrete_oracle_file}` を評価してください。",
        "完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです。",
        "issues には検出した問題点を入れ、問題がない場合は空配列を返してください。",
    ]
    if oracle_snapshot is not None:
        lines.append(
            "評価時に読む対象ファイルは、開始時点の内容を固定したコピー "
            f"`{readable_oracle_file}` です。"
        )
    lines.extend(
        [
            "問題がある場合、各 issue の referenced_paths には参照した仕様ファイル",
            "または INDEX.md に対応する元リポジトリ側の絶対パスをすべて返してください。",
            f"出力する oracle_path / referenced_paths は `{concrete_oracle_root}` "
            "配下の絶対パスにしてください。",
            "INDEX.md は自動生成されるため評価対象ではありません。",
            "INDEX.md は関連ファイル選定・参照根拠としてだけ読んでください。",
            "各 issue の specification_only_basis には、評価が仕様ファイルと",
            "INDEX.md だけに基づくことの説明を書いてください。",
            "対象仕様ファイル、関連する仕様ファイル、関連判断に必要な",
            f"`{readable_oracle_root}` 配下の INDEX.md だけを読んでください。",
            f"`{readable_oracle_index}` から始まる INDEX.md の Summary /",
            "Read this when / Do not read this when を根拠に、",
            "関連する仕様ファイルを選定してください。",
            f"`{readable_oracle_root}` 外のファイルは一切参照禁止です。",
            "実装ファイル、テストファイル、設定ファイル、ビルド成果物も参照禁止です。",
            "致命的な問題とは、実装を参照せずに仕様だけから判断・実装したとき、",
            "主要ワークフローを壊す、完了判定を妨げる、または中核目的を",
            "満たしたと判断できなくする問題です。",
            f"`{concrete_repo_root / 'memo'}` は読み書き禁止です。",
            "ファイル編集は禁止です。",
        ]
    )
    if oracle_snapshot is not None:
        lines.insert(
            lines.index("実装ファイル、テストファイル、設定ファイル、ビルド成果物も参照禁止です。"),
            f"`{concrete_oracle_root}` は path 変換のためにだけ使い、読まないでください。",
        )
    return "\n".join(lines)


def _improve_evaluations(
    execution_repo_root: Path,
    display_repo_root: Path,
    evaluations: list[dict[str, object]],
    repeat_improve_issues_list: int,
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> list[dict[str, object]]:
    """結合済み issue list を Codex CLI で反復改善する。"""
    if repeat_improve_issues_list == 0:
        return evaluations
    issues = _all_issues(evaluations)
    if not issues:
        return evaluations

    current_payload = {"issues": issues}
    for index in range(repeat_improve_issues_list):
        previous_payload_text = json.dumps(
            current_payload,
            ensure_ascii=False,
            sort_keys=True,
        )
        payload = parse_json_object(
            run_codex_exec(
                execution_repo_root,
                _improvement_prompt(
                    display_repo_root,
                    current_payload,
                    oracle_snapshot,
                ),
                purpose=f"oracle 問題点リスト改善 {index + 1}",
                read_only=True,
                expect_json=True,
                output_schema=_EVALUATION_OUTPUT_SCHEMA,
                model=FRONTIER_MODEL,
                reasoning_effort=FRONTIER_HIGH_REASONING_EFFORT,
                json_validator=lambda value: _validate_issues_payload(
                    value,
                    display_repo_root,
                    _target_oracle_paths(evaluations),
                    oracle_snapshot,
                ),
            )
        )
        current_payload = payload
        current_payload_text = json.dumps(
            current_payload,
            ensure_ascii=False,
            sort_keys=True,
        )
        if current_payload_text == previous_payload_text:
            break

    return _redistribute_improved_issues(evaluations, current_payload["issues"])


def _improvement_prompt(
    repo_root: Path,
    issue_payload: dict[str, object],
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> str:
    """問題点リスト改善用 prompt を組み立てる。"""
    concrete_repo_root = repo_root.resolve()
    concrete_oracle_root = (concrete_repo_root / "oracles").resolve()
    concrete_oracle_index = (concrete_oracle_root / "INDEX.md").resolve()
    readable_oracle_root = concrete_oracle_root
    readable_oracle_index = concrete_oracle_index
    if oracle_snapshot is not None:
        readable_oracle_root = oracle_snapshot.snapshot_oracle_root
        readable_oracle_index = (
            oracle_snapshot.snapshot_oracle_root / "INDEX.md"
        ).resolve()
    payload_text = json.dumps(issue_payload, ensure_ascii=False, indent=2)
    lines = [
        "あなたはソフトウェア仕様レビュー結果の整理担当です。",
        f"`{concrete_repo_root}` の仕様評価で得られた問題点リストを改善してください。",
        "完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです。",
    ]
    if oracle_snapshot is not None:
        lines.append(
            "必要に応じて読む仕様ファイル群は、開始時点の内容を固定したコピー "
            f"`{readable_oracle_root}` です。"
        )
    lines.extend(
        [
            "入力 issues を意味論的に統合・改善し、重複、矛盾、False-Positive を",
            "ベストエフォートで減らしてください。",
            "問題点がない場合は issues: [] を返してください。",
            "必要に応じて仕様ファイル、関連する仕様ファイル、関連判断に必要な",
            f"`{readable_oracle_root}` 配下の INDEX.md だけを読んでください。",
            f"`{readable_oracle_index}` から始まる INDEX.md の Summary /",
            "Read this when / Do not read this when を根拠に、",
            "関連する仕様ファイルを選定してください。",
            f"`{readable_oracle_root}` 外のファイルは一切参照禁止です。",
            f"出力する oracle_path / referenced_paths は `{concrete_oracle_root}` "
            "配下の絶対パスにしてください。",
            "実装ファイル、テストファイル、設定ファイル、ビルド成果物も参照禁止です。",
            f"`{concrete_repo_root / 'memo'}` は読み書き禁止です。",
            "ファイル編集は禁止です。",
            "入力問題点リスト:",
            payload_text,
        ]
    )
    if oracle_snapshot is not None:
        lines.insert(
            lines.index("実装ファイル、テストファイル、設定ファイル、ビルド成果物も参照禁止です。"),
            f"`{concrete_oracle_root}` は path 変換のためにだけ使い、読まないでください。",
        )
    return "\n".join(lines)


def _redistribute_improved_issues(
    evaluations: list[dict[str, object]],
    issues: object,
) -> list[dict[str, object]]:
    """改善後 issue を既存 report 集計形式へ戻す。"""
    if not isinstance(issues, list):
        raise ValueError("issues must be a list.")
    result = [
        {
            "target_oracle_path": evaluation["target_oracle_path"],
            "referenced_paths": [],
            "specification_only_basis": "",
            "issues": [],
        }
        for evaluation in evaluations
    ]
    target_to_index = {
        str(evaluation["target_oracle_path"]): index
        for index, evaluation in enumerate(result)
    }
    for issue in issues:
        if not isinstance(issue, dict):
            raise ValueError("issues item must be an object.")
        target = str(Path(str(issue["oracle_path"])).resolve())
        index = target_to_index.get(target, 0)
        result[index]["issues"].append(issue)
    return [_refresh_evaluation_metadata(evaluation) for evaluation in result]


def _evaluation_payload_to_record(
    value: object,
    repo_root: Path,
    oracle_file: Path,
) -> dict[str, object]:
    """Structured Output を report 用の評価レコードへ正規化する。"""
    if not isinstance(value, dict):
        raise ValueError("Expected JSON object.")
    if set(value) != {"issues"}:
        raise ValueError("Evaluation payload keys do not match schema.")
    return _refresh_evaluation_metadata(
        {
            "target_oracle_path": str(oracle_file.resolve()),
            "issues": value["issues"],
        }
    )


def _refresh_evaluation_metadata(
    evaluation: dict[str, object],
) -> dict[str, object]:
    """issue 単位の metadata から evaluation 単位の補助 metadata を再構成する。"""
    issues = _evaluation_issues(evaluation)
    referenced_paths = _unique_strings(
        [
            path
            for issue in issues
            for path in _string_list(issue.get("referenced_paths", []))
        ]
    )
    bases = _unique_strings(
        [
            str(issue["specification_only_basis"])
            for issue in issues
            if issue.get("specification_only_basis")
        ]
    )
    basis = " / ".join(bases)
    return {
        "target_oracle_path": str(
            Path(str(evaluation["target_oracle_path"])).resolve()
        ),
        "referenced_paths": referenced_paths,
        "specification_only_basis": basis,
        "issues": issues,
    }


def _validate_evaluation_payload(
    value: object,
    repo_root: Path,
    oracle_file: Path,
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> None:
    """oracle 評価 Structured Output の schema と意味制約を検査する。"""
    # run_codex_exec の schema 検査に加え、Python 側でも後段で扱う型を保証する。
    if not isinstance(value, dict):
        raise ValueError("Expected JSON object.")
    if set(value) != {"issues"}:
        raise ValueError("Evaluation payload keys do not match schema.")
    _validate_evaluation_issues(value["issues"], repo_root, oracle_snapshot)


def _validate_issues_payload(
    value: object,
    repo_root: Path,
    target_oracle_paths: set[Path],
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> None:
    """改善済み issue list の Structured Output を検査する。"""
    if not isinstance(value, dict):
        raise ValueError("Expected JSON object.")
    if set(value) != {"issues"}:
        raise ValueError("Issues payload keys do not match schema.")
    _validate_evaluation_issues(value["issues"], repo_root, oracle_snapshot)


def _target_oracle_paths(evaluations: list[dict[str, object]]) -> set[Path]:
    """評価済み target_oracle_path の集合を返す。"""
    return {
        Path(str(evaluation["target_oracle_path"])).resolve()
        for evaluation in evaluations
    }


def _write_report(
    repo_root: Path,
    mode: str,
    full_requested: bool,
    branch_name: str,
    cmoc_branch: bool,
    base_commit: str | None,
    session_fork_commit: str,
    deleted_oracles: bool,
    oracle_count_total: int,
    oracle_files: list[Path],
    evaluations: list[dict[str, object]],
    scope: ReviewOraclesScope,
    review_branch: str | None,
    review_fork_commit: str | None,
    review_join_commit: str | None,
) -> Path:
    """評価結果を `.cmoc/reports/review_oracles` に保存する。"""
    report_dir = repo_root / ".cmoc" / "reports" / _REPORT_DIR_NAME
    generated_at = "__CMOC_REPORT_GENERATED_AT__"
    finding_records = _finding_records(evaluations)
    finding_counts = _finding_counts(finding_records)
    result = _evaluation_result(len(oracle_files), finding_counts)

    lines = [
        "---",
        f"command: {_yaml_string(_REPORT_COMMAND)}",
        f"generated_at: {_yaml_string(generated_at)}",
        f"repo_root: {_yaml_string(str(repo_root.resolve()))}",
        f"scope: {_yaml_string(scope)}",
        f"session_branch: {_yaml_string(branch_name)}",
        f"session_fork_commit: {_yaml_string(session_fork_commit)}",
        f"review_branch: {_yaml_nullable(review_branch)}",
        f"review_fork_commit: {_yaml_nullable(review_fork_commit)}",
        f"review_join_commit: {_yaml_nullable(review_join_commit)}",
        f"oracle_count_total: {oracle_count_total}",
        f"oracle_count_evaluated: {len(oracle_files)}",
        f"fatal_findings_accepted_count: {finding_counts['fatal']['accept']}",
        f"minor_findings_accepted_count: {finding_counts['minor']['accept']}",
        f"fatal_findings_rejected_count: {finding_counts['fatal']['reject']}",
        f"minor_findings_rejected_count: {finding_counts['minor']['reject']}",
        f"result: {_yaml_string(result)}",
        "---",
        "",
        f"# {_REPORT_COMMAND} report",
        "",
        "## Verdict",
        "",
        _verdict_text(result),
        "",
        f"- Scope: `{scope}`",
        f"- Evaluated oracle files: `{len(oracle_files)}`",
        f"- Accepted fatal findings: `{finding_counts['fatal']['accept']}`",
        f"- Accepted minor findings: `{finding_counts['minor']['accept']}`",
        f"- Rejected fatal findings: `{finding_counts['fatal']['reject']}`",
        f"- Rejected minor findings: `{finding_counts['minor']['reject']}`",
        "",
        "## Evaluated oracle files",
        "",
        "| No. | Oracle file | Findings |",
        "|---:|---|---:|",
    ]
    finding_count_by_target = _finding_count_by_target(evaluations)
    for index, oracle_file in enumerate(oracle_files, start=1):
        target = str(oracle_file.resolve())
        lines.append(
            f"| {index} | `{_display_path(repo_root, str(oracle_file))}` | "
            f"{finding_count_by_target.get(target, 0)} |"
        )
    lines.extend([""])
    lines.extend(_finding_sections_lines(repo_root, finding_records))
    lines.extend(["## Referenced files", ""])
    referenced_path_rows = _referenced_path_rows(repo_root, evaluations)
    if referenced_path_rows:
        lines.extend(
            [
                "| No. | Referenced file |",
                "|---:|---|",
            ]
        )
        lines.extend(referenced_path_rows)
    else:
        lines.append("No referenced files.")
    report = "\n".join(lines)
    return write_timestamped_report(
        report_dir,
        lambda timestamp: report.replace(generated_at, timestamp),
    )


def _write_error_report(
    repo_root: Path,
    mode: str | None,
    full_requested: bool,
    branch_name: str | None,
    cmoc_branch: bool | None,
    base_commit: str | None,
    session_fork_commit: str | None,
    deleted_oracles: bool | None,
    oracle_count_total: int | None,
    oracle_files: list[Path],
    evaluations: list[dict[str, object]],
    scope: ReviewOraclesScope | None,
    review_branch: str | None,
    review_fork_commit: str | None,
    review_join_commit: str | None,
    failed_stage: str,
    error: Exception,
) -> Path:
    """評価処理失敗時の `result: error` レポートを best effort で保存する。"""
    report_dir = repo_root / ".cmoc" / "reports" / _REPORT_DIR_NAME
    generated_at = "__CMOC_REPORT_GENERATED_AT__"
    finding_records = _finding_records(evaluations)
    finding_counts = _finding_counts(finding_records)
    result = "error"
    lines = [
        "---",
        f"command: {_yaml_string(_REPORT_COMMAND)}",
        f"generated_at: {_yaml_string(generated_at)}",
        f"repo_root: {_yaml_string(str(repo_root.resolve()))}",
        f"scope: {_yaml_nullable(scope)}",
        f"session_branch: {_yaml_nullable(branch_name)}",
        f"session_fork_commit: {_yaml_nullable(session_fork_commit)}",
        f"review_branch: {_yaml_nullable(review_branch)}",
        f"review_fork_commit: {_yaml_nullable(review_fork_commit)}",
        f"review_join_commit: {_yaml_nullable(review_join_commit)}",
        f"oracle_count_total: {_yaml_int_nullable(oracle_count_total)}",
        f"oracle_count_evaluated: {len(evaluations)}",
        f"fatal_findings_accepted_count: {finding_counts['fatal']['accept']}",
        f"minor_findings_accepted_count: {finding_counts['minor']['accept']}",
        f"fatal_findings_rejected_count: {finding_counts['fatal']['reject']}",
        f"minor_findings_rejected_count: {finding_counts['minor']['reject']}",
        f"result: {_yaml_string(result)}",
        "---",
        "",
        f"# {_REPORT_COMMAND} report",
        "",
        "## Verdict",
        "",
        _verdict_text(result),
        "",
        f"- Scope: `{scope or 'unknown'}`",
        f"- Failed stage: `{failed_stage}`",
        f"- Exception type: `{type(error).__name__}`",
        f"- Exception message: `{str(error)}`",
        "",
        "## Evaluated oracle files",
        "",
        "| No. | Oracle file | Evaluation status | Findings |",
        "|---:|---|---|---:|",
    ]
    finding_count_by_target = _finding_count_by_target(evaluations)
    evaluated_files = _evaluated_oracle_files(evaluations)
    for index, oracle_file in enumerate(evaluated_files, start=1):
        target = str(oracle_file)
        lines.append(
            f"| {index} | `{_display_path(repo_root, str(oracle_file))}` | "
            f"evaluated | {finding_count_by_target.get(target, 0)} |"
        )
    not_evaluated_files = _not_evaluated_oracle_files(
        repo_root,
        oracle_files,
        evaluations,
    )
    for index, oracle_file in enumerate(
        not_evaluated_files,
        start=len(evaluated_files) + 1,
    ):
        lines.append(
            f"| {index} | `{_display_path(repo_root, str(oracle_file))}` | "
            "not_evaluated | - |"
        )
    if not evaluated_files and not not_evaluated_files:
        lines.append("| - | No requested oracle files. | - | - |")
    lines.extend([""])
    lines.extend(_finding_sections_lines(repo_root, finding_records))
    lines.extend(["## Referenced files", ""])
    referenced_path_rows = _referenced_path_rows(repo_root, evaluations)
    if referenced_path_rows:
        lines.extend(
            [
                "| No. | Referenced file |",
                "|---:|---|",
            ]
        )
        lines.extend(referenced_path_rows)
    else:
        lines.append("No referenced files.")
    report = "\n".join(lines)
    return write_timestamped_report(
        report_dir,
        lambda timestamp: report.replace(generated_at, timestamp),
    )


def _print_error_report_fallback(
    repo_root: Path,
    mode: str | None,
    full_requested: bool,
    branch_name: str | None,
    cmoc_branch: bool | None,
    base_commit: str | None,
    review_start_commit: str | None,
    deleted_oracles: bool | None,
    oracle_count_total: int | None,
    oracle_files: list[Path],
    evaluations: list[dict[str, object]],
    failed_stage: str,
    error: Exception,
    report_error: Exception,
) -> None:
    """error report 保存失敗時に一次失敗情報だけは stderr へ残す。"""
    lines = [
        f"{_REPORT_COMMAND} error report generation failed.",
        "Fallback diagnostic:",
        f"- result: error",
        f"- repo_root: {repo_root.resolve()}",
        f"- mode: {mode or 'unknown'}",
        f"- full_requested: {str(full_requested).lower()}",
        f"- branch: {_yaml_nullable(branch_name)}",
        f"- is_cmoc_branch: {_yaml_bool_nullable(cmoc_branch)}",
        f"- base_commit: {_yaml_nullable(base_commit)}",
        f"- head_commit: {_yaml_nullable(review_start_commit)}",
        f"- deleted_oracles_detected: {_yaml_bool_nullable(deleted_oracles)}",
        f"- oracle_count_total: {_yaml_int_nullable(oracle_count_total)}",
        f"- oracle_count_requested: {len(oracle_files)}",
        f"- oracle_count_evaluated: {len(evaluations)}",
        f"- failed_stage: {failed_stage}",
        f"- exception: {type(error).__name__}: {error}",
        f"- report_exception: {type(report_error).__name__}: {report_error}",
    ]
    print("\n".join(lines), file=sys.stderr)


def _validate_referenced_paths(
    value: object,
    repo_root: Path,
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> set[Path]:
    """referenced_paths を絶対 oracle / INDEX ファイル配列として検査する。"""
    if not isinstance(value, list):
        raise ValueError("referenced_paths must be a list.")
    paths = set()
    for index, item in enumerate(value):
        paths.add(
            _require_absolute_oracle_reference_path(
                item,
                repo_root,
                f"referenced_paths[{index}]",
                oracle_snapshot,
            )
        )
    return paths


def _validate_evaluation_issues(
    value: object,
    repo_root: Path,
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> None:
    """issues 配列の item schema を検査する。"""
    if not isinstance(value, list):
        raise ValueError("issues must be a list.")
    required_keys = {
        "severity",
        "title",
        "oracle_path",
        "oracle_line_start",
        "oracle_line_end",
        "referenced_paths",
        "affected_workflow",
        "requirement",
        "problem",
        "reason",
        "suggested_oracle_change",
        "specification_only_basis",
    }
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise ValueError(f"issues[{index}] must be an object.")
        if set(item) != required_keys:
            raise ValueError(f"issues[{index}] keys do not match schema.")
        if item["severity"] not in _SEVERITY_ORDER:
            raise ValueError(f"issues[{index}].severity is invalid.")
        _require_issue_string(item, "title", index)
        _require_issue_oracle_path_string(item["oracle_path"], index)
        _validate_issue_lines(item, index)
        _validate_referenced_paths(
            item["referenced_paths"],
            repo_root,
            oracle_snapshot,
        )
        for key in [
            "affected_workflow",
            "requirement",
            "problem",
            "reason",
            "suggested_oracle_change",
        ]:
            _require_issue_string(item, key, index)
        _require_issue_string(
            item,
            "specification_only_basis",
            index,
            allow_empty=True,
        )


def _require_issue_oracle_path_string(value: object, index: int) -> None:
    """issues[].oracle_path は後処理で必要な最小限だけ検査する。"""
    if not isinstance(value, str):
        raise ValueError(f"issues[{index}].oracle_path must be a string.")
    stripped_value = value.strip()
    if not stripped_value:
        raise ValueError(f"issues[{index}].oracle_path must not be empty.")


def _require_absolute_oracle_file(
    value: object,
    repo_root: Path,
    label: str,
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> Path:
    """JSON 値を oracles ファイル path として検査する。"""
    resolved_path = _require_absolute_oracles_file(
        value,
        repo_root,
        label,
        require_current_existence=oracle_snapshot is None,
    )
    if oracle_snapshot is not None:
        if resolved_path not in oracle_snapshot.oracle_files:
            raise ValueError(f"{label} must be an oracle file.")
        return resolved_path

    oracle_files = {path.resolve() for path in list_oracle_files(repo_root)}
    if resolved_path not in oracle_files:
        raise ValueError(f"{label} must be an oracle file.")
    return resolved_path


def _require_absolute_oracle_reference_path(
    value: object,
    repo_root: Path,
    label: str,
    oracle_snapshot: _OracleEvaluationSnapshot | None = None,
) -> Path:
    """JSON 値を参照可能な oracle / INDEX file path として検査する。"""
    resolved_path = _require_absolute_oracles_file(
        value,
        repo_root,
        label,
        require_current_existence=oracle_snapshot is None,
    )
    if oracle_snapshot is not None:
        if resolved_path not in oracle_snapshot.reference_files:
            raise ValueError(f"{label} must be an oracle file or INDEX.md.")
        return resolved_path
    if resolved_path.name == "INDEX.md":
        return resolved_path

    oracle_files = {path.resolve() for path in list_oracle_files(repo_root)}
    if resolved_path not in oracle_files:
        raise ValueError(f"{label} must be an oracle file or INDEX.md.")
    return resolved_path


def _require_absolute_oracles_file(
    value: object,
    repo_root: Path,
    label: str,
    *,
    require_current_existence: bool,
) -> Path:
    """JSON 値を oracles 配下の絶対 file path として検査する。"""
    if not isinstance(value, str):
        raise ValueError(f"{label} must be a string.")
    path = Path(value)
    if not path.is_absolute():
        raise ValueError(f"{label} must be an absolute path.")
    resolved_path = path.resolve()
    oracle_root = (repo_root / "oracles").resolve()
    try:
        resolved_path.relative_to(oracle_root)
    except ValueError as error:
        raise ValueError(f"{label} must be under oracles.") from error
    if require_current_existence:
        if not resolved_path.exists():
            raise ValueError(f"{label} must exist.")
        if not resolved_path.is_file():
            raise ValueError(f"{label} must be a file.")
    return resolved_path


def _require_issue_string(
    item: dict[object, object],
    key: str,
    index: int,
    *,
    allow_empty: bool = False,
) -> None:
    """issue item の string 項目を検査する。"""
    if not isinstance(item[key], str):
        raise ValueError(f"issues[{index}].{key} must be a string.")
    if not allow_empty and not item[key].strip():
        raise ValueError(f"issues[{index}].{key} must not be empty.")


def _validate_issue_lines(item: dict[object, object], index: int) -> None:
    """issue item の行番号項目を検査する。"""
    start = item["oracle_line_start"]
    end = item["oracle_line_end"]
    if start is not None and not isinstance(start, int):
        raise ValueError(f"issues[{index}].oracle_line_start is invalid.")
    if end is not None and not isinstance(end, int):
        raise ValueError(f"issues[{index}].oracle_line_end is invalid.")
    if isinstance(start, int) and start < 1:
        raise ValueError(f"issues[{index}].oracle_line_start is invalid.")
    if isinstance(end, int) and end < 1:
        raise ValueError(f"issues[{index}].oracle_line_end is invalid.")
    if isinstance(start, int) and isinstance(end, int) and start > end:
        raise ValueError(f"issues[{index}] line range is invalid.")


def _issue_counts(
    evaluations: list[dict[str, object]],
) -> dict[str, int]:
    """severity ごとの issue 件数を数える。"""
    counts = {severity: 0 for severity in _SEVERITY_ORDER}
    for issue in _all_issues(evaluations):
        severity = str(issue["severity"])
        counts[severity] += 1
    return counts


def _finding_records(
    evaluations: list[dict[str, object]],
) -> list[dict[str, object]]:
    """evaluation 内 issue を仕様上の finding record に正規化する。"""
    records = []
    for issue in _all_issues(evaluations):
        records.append(
            {
                "severity": _finding_severity_for_issue(issue),
                "verdict": _finding_verdict_for_issue(issue),
                "issue": issue,
            }
        )
    return records


def _finding_severity_for_issue(issue: dict[str, object]) -> str:
    """旧 issue severity を fatal/minor に畳む。"""
    finding_severity = issue.get("finding_severity")
    if finding_severity in _FINDING_SEVERITY_ORDER:
        return str(finding_severity)
    return "fatal" if issue.get("severity") == "fatal" else "minor"


def _finding_verdict_for_issue(issue: dict[str, object]) -> str:
    """issue metadata から accept/reject を返す。旧 issue は accept 扱い。"""
    judge_verdict = issue.get("judge_verdict")
    if judge_verdict in _FINDING_VERDICT_ORDER:
        return str(judge_verdict)
    return "accept"


def _finding_counts(
    finding_records: list[dict[str, object]],
) -> dict[str, dict[str, int]]:
    """fatal/minor と accept/reject ごとの finding 件数を数える。"""
    counts = {
        severity: {verdict: 0 for verdict in _FINDING_VERDICT_ORDER}
        for severity in _FINDING_SEVERITY_ORDER
    }
    for record in finding_records:
        severity = str(record["severity"])
        verdict = str(record["verdict"])
        counts[severity][verdict] += 1
    return counts


def _evaluation_result(
    oracle_count: int,
    issue_counts: dict[str, object],
) -> str:
    """件数から仕様上許可されたレポート result を決める。"""
    if oracle_count == 0:
        return "no_targets"
    if _count_value(issue_counts, "fatal") > 0:
        return "fatal"
    if (
        _count_value(issue_counts, "minor") > 0
        or _count_value(issue_counts, "warning") > 0
        or _count_value(issue_counts, "inconclusive") > 0
    ):
        return "minor"
    return "ok"


def _count_value(counts: dict[str, object], key: str) -> int:
    """plain count と verdict 別 count の両方から検出件数を読む。"""
    value = counts.get(key, 0)
    if isinstance(value, dict):
        return sum(count for count in value.values() if isinstance(count, int))
    return value if isinstance(value, int) else 0


def _verdict_text(result: str) -> str:
    """result ごとの Verdict 本文を返す。"""
    if result == "ok":
        return (
            "今回評価した範囲では問題点が検出されませんでした。"
            "ただし、問題点の不存在を完全保証するものではありません。"
        )
    if result == "fatal":
        return (
            "oracle スナップショットには、仕様だけから判断して主要ワークフロー、"
            "完了判定、または中核目的を壊しうる問題があります。"
        )
    if result == "minor":
        return "致命的ではありませんが、oracles ファイルに細かな問題があります。"
    if result == "no_targets":
        return "評価対象 oracle が 0 件だったため、問題点の評価は行われませんでした。"
    if result == "error":
        return (
            "評価処理またはレポート生成に失敗したため、成功評価ではありません。"
            "ログと例外情報を確認し、必要な修正または再実行を判断してください。"
        )
    return (
        "未知の result のため、評価状態を成功として扱えません。"
        "ログとレポート生成処理を確認してください。"
    )


def _issue_count_by_target(
    evaluations: list[dict[str, object]],
) -> dict[str, int]:
    """評価対象ファイルごとの issue 件数を返す。"""
    result = {}
    for evaluation in evaluations:
        issues = _evaluation_issues(evaluation)
        target = Path(str(evaluation["target_oracle_path"])).resolve()
        result[str(target)] = len(issues)
    return result


def _finding_count_by_target(
    evaluations: list[dict[str, object]],
) -> dict[str, int]:
    """評価対象ファイルごとの finding 件数を返す。"""
    result = {}
    for evaluation in evaluations:
        target = Path(str(evaluation["target_oracle_path"])).resolve()
        result[str(target)] = len(_evaluation_issues(evaluation))
    return result


def _evaluated_oracle_files(evaluations: list[dict[str, object]]) -> list[Path]:
    """完了した評価結果に含まれる対象 oracle ファイルを返す。"""
    return [
        Path(str(evaluation["target_oracle_path"])).resolve()
        for evaluation in evaluations
    ]


def _not_evaluated_oracle_files(
    repo_root: Path,
    oracle_files: list[Path],
    evaluations: list[dict[str, object]],
) -> list[Path]:
    """依頼対象のうち評価完了していない oracle ファイルを返す。"""
    evaluated = set(_evaluated_oracle_files(evaluations))
    return [
        oracle_file.resolve()
        for oracle_file in oracle_files
        if oracle_file.resolve() not in evaluated
    ]


def _issues_for_severity(
    evaluations: list[dict[str, object]],
    severity: str,
) -> list[dict[str, object]]:
    """指定 severity の issue を評価順・issue 順で返す。"""
    return [
        issue
        for issue in _all_issues(evaluations)
        if issue["severity"] == severity
    ]


def _numbered_issues(
    severity: str,
    issues: list[dict[str, object]],
) -> list[tuple[str, dict[str, object]]]:
    """severity ごとに report-local id を付ける。"""
    prefix = _ISSUE_ID_PREFIXES[severity]
    return [
        (f"{prefix}-{index:03d}", issue)
        for index, issue in enumerate(issues, start=1)
    ]


def _issue_lines(
    repo_root: Path,
    issue_id: str,
    issue: dict[str, object],
) -> list[str]:
    """issue 1 件を Markdown 行へ変換する。"""
    return [
        f"### {issue_id}: {issue['title']}",
        "",
        f"- Oracle file: `{_display_path(repo_root, str(issue['oracle_path']))}`",
        f"- Lines: `{_line_range(issue)}`",
        f"- Affected workflow: `{issue['affected_workflow']}`",
        "- Requirement:",
        f"  - {issue['requirement']}",
        "- Problem:",
        f"  - {issue['problem']}",
        "- Reason:",
        f"  - {issue['reason']}",
        "- Suggested oracle change:",
        f"  - {issue['suggested_oracle_change']}",
        "- Specification-only basis:",
        f"  - {issue['specification_only_basis']}",
        "",
    ]


def _finding_sections_lines(
    repo_root: Path,
    finding_records: list[dict[str, object]],
) -> list[str]:
    """仕様順の finding セクション行を返す。"""
    lines = []
    for verdict, severity, heading in [
        ("accept", "fatal", "## Fatal findings"),
        ("accept", "minor", "## Minor findings"),
        ("reject", "fatal", "## Rejected fatal findings"),
        ("reject", "minor", "## Rejected minor findings"),
    ]:
        lines.extend([heading, ""])
        lines.extend(
            _finding_group_lines(repo_root, finding_records, verdict, severity)
        )
    return lines


def _finding_group_lines(
    repo_root: Path,
    finding_records: list[dict[str, object]],
    verdict: str,
    severity: str,
) -> list[str]:
    """指定 verdict/severity の finding 行を返す。"""
    lines = []
    records = [
        record
        for record in finding_records
        if record["severity"] == severity and record["verdict"] == verdict
    ]
    if not records:
        lines.extend(["No findings.", ""])
        return lines
    for finding_id, record in _numbered_finding_records(severity, records):
        issue = record["issue"]
        if isinstance(issue, dict):
            lines.extend(_issue_lines(repo_root, finding_id, issue))
    return lines


def _numbered_finding_records(
    severity: str,
    records: list[dict[str, object]],
) -> list[tuple[str, dict[str, object]]]:
    """finding severity ごとに report-local id を付ける。"""
    prefix = "FATAL" if severity == "fatal" else "MINOR"
    return [
        (f"{prefix}-{index:03d}", record)
        for index, record in enumerate(records, start=1)
    ]


def _line_range(issue: dict[str, object]) -> str:
    """issue の行範囲を Markdown 表示用文字列にする。"""
    start = issue["oracle_line_start"]
    end = issue["oracle_line_end"]
    if start is None or end is None:
        return "unknown"
    if start == end:
        return str(start)
    return f"{start}-{end}"


def _referenced_path_rows(
    repo_root: Path,
    evaluations: list[dict[str, object]],
) -> list[str]:
    """全評価結果の referenced_paths を重複排除した表示行を返す。"""
    referenced_paths = _unique_strings(
        [
            path
            for evaluation in evaluations
            for path in _string_list(evaluation["referenced_paths"])
        ]
    )
    result = []
    for index, path in enumerate(referenced_paths, start=1):
        result.append(
            f"| {index} | `{_display_path(repo_root, path)}` |"
        )
    return result


def _all_issues(
    evaluations: list[dict[str, object]],
) -> list[dict[str, object]]:
    """全評価結果の issues を評価順に連結する。"""
    result = []
    for evaluation in evaluations:
        result.extend(_evaluation_issues(evaluation))
    return result


def _evaluation_issues(
    evaluation: dict[str, object],
) -> list[dict[str, object]]:
    """検証済み evaluation から issues を取り出す。"""
    issues = evaluation["issues"]
    if not isinstance(issues, list):
        raise ValueError("issues must be a list.")
    return [issue for issue in issues if isinstance(issue, dict)]


def _string_list(value: object) -> list[str]:
    """JSON 値を文字列配列として検査する。"""
    if not isinstance(value, list) or not all(
        isinstance(item, str) for item in value
    ):
        raise ValueError("Expected list[str].")
    return value


def _yaml_nullable(value: str | None) -> str:
    """YAML frontmatter 用に nullable scalar を返す。"""
    if value is None:
        return "null"
    return _yaml_string(value)


def _yaml_string(value: str) -> str:
    """YAML frontmatter 用に double quoted scalar を返す。"""
    return json.dumps(value, ensure_ascii=False)


def _yaml_bool_nullable(value: bool | None) -> str:
    """YAML frontmatter 用に nullable bool を返す。"""
    if value is None:
        return "null"
    return str(value).lower()


def _yaml_int_nullable(value: int | None) -> str:
    """YAML frontmatter 用に nullable int を返す。"""
    if value is None:
        return "null"
    return str(value)


def _unique_strings(values: list[str]) -> list[str]:
    """文字列配列を順序維持で重複排除する。"""
    result = []
    seen = set()
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def _display_path(repo_root: Path, path_text: str) -> str:
    """path_text をレポート向けの絶対パスにする。"""
    path = Path(path_text)
    if not path.is_absolute():
        path = repo_root / path
    return str(path.resolve())
