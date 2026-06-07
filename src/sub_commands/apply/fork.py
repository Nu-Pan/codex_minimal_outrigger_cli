"""`cmoc apply` の本体処理。"""

import fcntl
import json
import os
import re
from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from contextvars import copy_context
from dataclasses import dataclass
from inspect import Parameter, signature
from pathlib import Path
from time import sleep
from typing import Literal

from commons.codex import (
    COMMIT_MESSAGE_MODEL,
    COMMIT_MESSAGE_REASONING_EFFORT,
    COST_PERFORMANCE_MODEL,
    COST_PERFORMANCE_REASONING_EFFORT,
    FRONTIER_HIGH_REASONING_EFFORT,
    FRONTIER_MODEL,
    FRONTIER_REASONING_EFFORT,
    parse_json_object,
    run_codex_exec,
)
from commons.command_runner import run_command
from commons.errors import CmocError
from commons.indexing import find_index_inconsistencies
from commons.indexing import is_maintained_index_path
from commons.indexing import maintain_indexes
from commons.report_files import write_timestamped_report
from commons.subcommand_log import write_console_block
from commons.repo import (
    APPLY_BRANCH_PREFIX,
    assert_no_uncommitted_changes,
    changed_paths,
    clear_apply_process_id,
    current_branch,
    ensure_cmoc_ignored_and_committed,
    filter_apply_implementation_file_paths,
    filter_apply_implementation_file_paths_at_commit,
    filter_oracle_file_paths,
    filter_oracle_file_paths_at_commit,
    git_name_only_paths,
    git_name_status_entries,
    git_status_paths,
    head_commit,
    is_session_branch,
    read_session_state,
    read_session_start_commit,
    run_git,
    session_id_from_branch,
    session_state_root,
    write_session_state,
    write_apply_process_id,
)
from commons.timing import StepTimer, start_step
from commons.timing import StepIndexPath
from commons.timestamps import make_timestamp

ApplyScope = Literal["rolling", "session", "full"]
_APPLY_SCOPES = {"rolling", "session", "full"}
APPLY_FORK_EXIT_CODE_SUCCESS = 0
APPLY_FORK_EXIT_CODE_CONVERGED = APPLY_FORK_EXIT_CODE_SUCCESS
# 未収束はエラーではないが、呼び出し元が収束と判別できる終了コードにする。
APPLY_FORK_EXIT_CODE_UNCONVERGED = 10


@dataclass(frozen=True)
class _InvestigationTarget:
    """不整合調査を開始する repo 内 path と存在状態。"""

    path: Path
    exists_at_snapshot: bool = True
    exists_in_worktree: bool = True

    @property
    def deleted_at_snapshot(self) -> bool:
        """snapshot にも現在 worktree にもない履歴調査対象かを返す。"""
        return not self.exists_at_snapshot and not self.exists_in_worktree


@dataclass(frozen=True)
class _ApplyWorktreePlan:
    """1 回の apply worktree 作成試行で使う識別子一式。"""

    apply_run_id: str
    apply_branch: str
    apply_worktree: Path


class _ApplyWorktreeCreationError(RuntimeError):
    """apply worktree 作成失敗時に、最後に実試行した候補を保持する。"""

    def __init__(self, message: str, last_plan: _ApplyWorktreePlan) -> None:
        """復旧表示で参照する最後の worktree 作成計画を例外へ添付する。"""
        super().__init__(message)
        self.last_plan = last_plan


@dataclass(frozen=True)
class _InvestigationJob:
    """file 起点調査として並列実行する Codex CLI 呼び出し単位。"""

    kind: str
    index: int
    total: int
    target: _InvestigationTarget


_DISCREPANCY_OUTPUT_SCHEMA: dict[str, object] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["git_head_commit_hash", "fixing_points"],
    "properties": {
        "git_head_commit_hash": {
            "type": ["string", "null"],
            "description": (
                "要修正点を発見した時点での git HEAD commit hash。"
                "後で機械的にフィルされるので AI による出力は null で良い。"
            ),
        },
        "fixing_points": {
            "type": "array",
            "description": "実装に対する要修正点のリスト。空配列の場合のみ要修正点なしとみなす。",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "title",
                    "evidences",
                    "oracle_requirement",
                    "observed_implementation",
                    "reason",
                    "suggested_fix",
                ],
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "要修正点の短い見出し。",
                    },
                    "evidences": {
                        "type": "array",
                        "description": (
                            "要修正点の根拠となる文言の位置情報。"
                            "仕様ファイル・実装ファイルのどちらかが必ず 1 つは"
                            "根拠として存在するはずであるから空配列は想定しない。"
                        ),
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "required": [
                                "path",
                                "line_start",
                                "line_end",
                                "summary",
                            ],
                            "properties": {
                                "path": {
                                    "type": "string",
                                    "description": "要修正点の根拠となるファイルの絶対パス。",
                                },
                                "line_start": {
                                    "type": ["integer", "null"],
                                    "description": (
                                        "要修正点の根拠となる記述の開始行。"
                                        "行番号を特定できない場合は null。"
                                    ),
                                },
                                "line_end": {
                                    "type": ["integer", "null"],
                                    "description": (
                                        "要修正点の根拠となる記述の終了行。"
                                        "行番号を特定できない場合は null。"
                                    ),
                                },
                                "summary": {
                                    "type": "string",
                                    "description": (
                                        "該当箇所の短い要約。位置情報がズレた場合に"
                                        "それを検知するための冗長情報。"
                                    ),
                                },
                            },
                        },
                    },
                    "oracle_requirement": {
                        "type": "string",
                        "description": (
                            "仕様ファイルが要求している仕様。実装のみから発見した"
                            "要修正点であったとしても必ず関係する仕様を記載する。"
                        ),
                    },
                    "observed_implementation": {
                        "type": "string",
                        "description": "調査時点の実装が実際にどうなっているか。",
                    },
                    "reason": {
                        "type": "string",
                        "description": (
                            "なぜ、明確に問題があり修正が必要であると言えるのか。"
                            "推測や未確認事項は含めない。"
                        ),
                    },
                    "suggested_fix": {
                        "type": "string",
                        "description": "問題を解決するために必要な実装修正の方針。",
                    },
                },
            },
        }
    },
}

_CHANGE_SUMMARY_OUTPUT_SCHEMA: dict[str, object] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["changes"],
    "properties": {
        "changes": {
            "type": "array",
            "description": (
                "`<oracle-snapshot-commit>` から `<cmoc-apply-branch>` の "
                "HEAD までの差分を、変更内容の意味論に基づいてカテゴリ分け"
                "した要約。空配列は想定しない。"
            ),
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["category", "summary", "changed_paths"],
                "properties": {
                    "category": {
                        "type": "string",
                        "description": (
                            "変更内容の意味論に基づくカテゴリ名。"
                            "例: 実行制御、レポート生成、テスト、ルーティング文書。"
                        ),
                    },
                    "summary": {
                        "type": "string",
                        "description": (
                            "このカテゴリで行った変更内容の人間向け要約。"
                            "何をどう変えたかを書く。"
                        ),
                    },
                    "changed_paths": {
                        "type": "array",
                        "description": (
                            "このカテゴリに属する主な変更ファイルのリポジトリ"
                            "相対パス。"
                        ),
                        "items": {"type": "string"},
                    },
                },
            },
        }
    },
}


def cmoc_apply_impl(
    repo_root: Path | None = None,
    *,
    repeat_investigate_and_fix: int = 5,
    repeat_improove_fixing_list: int = 3,
    scope: ApplyScope = "rolling",
) -> int | None:
    """oracle と実装の不整合を Codex CLI へ追従させる。"""
    # 直接呼び出し時は共通 runner で repo root 解決とエラー整形を行う。
    if repo_root is None:
        run_command(
            lambda resolved_repo_root: cmoc_apply_impl(
                resolved_repo_root,
                repeat_investigate_and_fix=repeat_investigate_and_fix,
                repeat_improove_fixing_list=(
                    repeat_improove_fixing_list
                ),
                scope=scope,
            ),
            command_path="cmoc apply fork",
            non_error_exit_codes={APPLY_FORK_EXIT_CODE_UNCONVERGED},
        )
        return None

    # apply は session branch 上で開始し、専用 worktree でだけ実装を変更する。
    timer = StepTimer("apply")
    session_branch = current_branch(repo_root)
    if not is_session_branch(session_branch):
        raise CmocError(
            "`cmoc apply` は session branch 上で実行してください。",
            [
                "先に `cmoc session fork` を実行してください。",
                "既存の session branch を checkout してください。",
            ],
            f"現在の branch: {session_branch or '(detached HEAD)'}",
        )

    session_id = session_id_from_branch(session_branch)
    state_root = session_state_root(repo_root)
    _validate_repeat_options(
        repeat_investigate_and_fix,
        repeat_improove_fixing_list,
    )
    _validate_apply_scope(scope)

    start_step(timer, 1, 6, "session 状態検証")
    state = read_session_state(state_root, session_id)
    session_start_commit = _validate_apply_fork_state(
        state,
        session_branch,
    )
    assert_no_uncommitted_changes(repo_root)

    start_step(timer, 2, 6, ".cmoc ignore 確認")
    ensure_cmoc_ignored_and_committed(repo_root)
    assert_no_uncommitted_changes(repo_root)
    session_head_at_apply_start = ""
    oracle_snapshot_commit = ""

    failed_stage = "apply worktree 作成"
    apply_run_id = ""
    apply_branch = ""
    apply_worktree = state_root / ".cmoc" / "worktrees" / session_id
    discrepancy_counts: list[int] = []
    apply_start_needs_error_record = False
    apply_error_recorded = False
    try:
        with _locked_apply_start(state_root, session_id):
            state = read_session_state(state_root, session_id)
            session_start_commit = _validate_apply_fork_state(
                state,
                session_branch,
            )
            investigation_base_commit = _scope_base_commit(
                state,
                session_start_commit,
                scope,
            )
            assert_no_uncommitted_changes(repo_root)
            session_head_at_apply_start = head_commit(repo_root)
            oracle_snapshot_commit = session_head_at_apply_start

            failed_stage = "apply worktree 作成"
            start_step(timer, 3, 6, "apply worktree 作成")
            apply_start_needs_error_record = True
            apply_plan = _plan_apply_worktree(state_root, session_id)
            apply_run_id = apply_plan.apply_run_id
            apply_branch = apply_plan.apply_branch
            apply_worktree = apply_plan.apply_worktree
            try:
                apply_plan = _create_apply_worktree(
                    state_root,
                    session_id,
                    oracle_snapshot_commit,
                    apply_plan,
                )
                apply_run_id = apply_plan.apply_run_id
                apply_branch = apply_plan.apply_branch
                apply_worktree = apply_plan.apply_worktree
                _mark_apply_running(
                    state_root,
                    session_id,
                    state,
                    apply_branch,
                    oracle_snapshot_commit,
                )
            except _ApplyWorktreeCreationError as error:
                apply_run_id = error.last_plan.apply_run_id
                apply_branch = error.last_plan.apply_branch
                apply_worktree = error.last_plan.apply_worktree
                _mark_apply_error(
                    state_root,
                    session_id,
                    state,
                    apply_branch=apply_branch,
                    oracle_snapshot_commit=oracle_snapshot_commit,
                )
                apply_error_recorded = True
                raise
            except Exception:
                _mark_apply_error(
                    state_root,
                    session_id,
                    state,
                    apply_branch=apply_branch,
                    oracle_snapshot_commit=oracle_snapshot_commit,
                )
                apply_error_recorded = True
                raise

        # ユーザー向けステップとして INDEX.md を明示メンテナンスする。
        failed_stage = "INDEX.md メンテナンス"
        start_step(timer, 4, 6, "INDEX.md メンテナンス")
        before_index_head = head_commit(apply_worktree)
        _maintain_apply_indexes(apply_worktree)
        _assert_forbidden_paths_unchanged_since(
            apply_worktree,
            before_index_head,
            allow_maintained_index_paths=True,
        )

        # 不整合調査と追従作業を指定回数まで反復する。
        failed_stage = "要修正点調査・適用"
        start_step(timer, 5, 6, "要修正点調査・適用")
        completed = False
        dirty_oracle_paths: set[Path] | None = None
        dirty_implementation_paths: set[Path] | None = None
        for loop_index in range(1, repeat_investigate_and_fix + 1):
            loop_step_path = (
                (5, 6),
                (loop_index, repeat_investigate_and_fix),
            )
            start_step(
                timer,
                loop_step_path,
                None,
                "調査・修正ループ",
            )
            discrepancies = _investigate_discrepancies(
                apply_worktree,
                investigation_base_commit,
                oracle_snapshot_commit,
                improvement_base_commit=oracle_snapshot_commit,
                timer=timer,
                step_path=loop_step_path,
                repeat_improove_fixing_list=repeat_improove_fixing_list,
                scope=scope,
                dirty_oracle_paths=dirty_oracle_paths,
                dirty_implementation_paths=dirty_implementation_paths,
            )
            next_dirty_oracle_paths = _dirty_oracle_paths_from_discrepancies(
                apply_worktree,
                discrepancies,
            )
            next_dirty_implementation_paths = (
                _dirty_implementation_paths_from_discrepancies(
                    apply_worktree,
                    discrepancies,
                )
            )
            # 要修正点が残る反復では、空集合も「全候補 dirty=false」
            # という有効な dirty フラグ状態として次ループへ渡す。
            found_dirty_evidences = bool(discrepancies)
            dirty_oracle_paths = (
                next_dirty_oracle_paths if found_dirty_evidences else None
            )
            dirty_implementation_paths = next_dirty_implementation_paths
            discrepancy_counts.append(len(discrepancies))
            print(
                "実装反復 "
                f"({loop_index}/{repeat_investigate_and_fix}) 要修正点: "
                f"{len(discrepancies)}"
            )
            if not discrepancies:
                completed = True
                break

            _apply_discrepancies(
                apply_worktree,
                discrepancies,
                timer=timer,
                step_path=(*loop_step_path, (5, 5)),
                dirty_implementation_paths=dirty_implementation_paths,
            )
            if not found_dirty_evidences and not dirty_implementation_paths:
                dirty_implementation_paths = None

        # 要修正点 0 件の経路も含め、apply run 中に生じた差分を確定する。
        _assert_forbidden_paths_clean(
            apply_worktree,
            allow_maintained_index_paths=True,
        )
        _commit_all_changes(apply_worktree)

        session_head_at_apply_finish = _session_branch_head_for_report(
            repo_root,
            session_branch,
        )
        # 実行結果を人間向け report に変換する。
        failed_stage = "report 書き込み"
        start_step(timer, 6, 6, "report 書き込み")
        report_path = _write_apply_report(
            apply_worktree,
            state_root,
            session_id,
            apply_run_id,
            session_branch,
            apply_branch,
            apply_worktree,
            session_start_commit,
            oracle_snapshot_commit,
            session_head_at_apply_start,
            session_head_at_apply_finish,
            completed,
            discrepancy_counts,
        )
        failed_stage = "final output 書き込み"
        print(f"apply run id: {apply_run_id}")
        print(str(report_path))
        failed_stage = "apply 完了記録"
        _mark_apply_completed(
            state_root,
            session_id,
            state,
        )
        apply_start_needs_error_record = False
        if completed:
            return APPLY_FORK_EXIT_CODE_CONVERGED
        return APPLY_FORK_EXIT_CODE_UNCONVERGED
    except Exception as error:
        if not apply_start_needs_error_record:
            raise
        if not apply_error_recorded:
            _mark_apply_error(
                state_root,
                session_id,
                state,
                apply_branch=apply_branch,
                oracle_snapshot_commit=oracle_snapshot_commit,
            )
        try:
            session_head_at_apply_finish = _session_branch_head_for_report(
                repo_root,
                session_branch,
            )
            report_path = _write_apply_error_report(
                state_root,
                session_id,
                apply_run_id,
                session_branch,
                apply_branch,
                apply_worktree,
                session_start_commit,
                oracle_snapshot_commit,
                session_head_at_apply_start,
                session_head_at_apply_finish,
                failed_stage,
                error,
                discrepancy_counts,
            )
        except Exception as report_error:
            error.add_note(
                "apply error report generation also failed: "
                f"{type(report_error).__name__}: {report_error}"
            )
        else:
            print(f"apply run id: {apply_run_id}")
            print(str(report_path))
        raise


def _session_branch_head_for_report(repo_root: Path, session_branch: str) -> str:
    """apply report 用に session branch の現在 HEAD を取得する。"""
    result = run_git(
        repo_root,
        ["rev-parse", "--verify", f"refs/heads/{session_branch}^{{commit}}"],
        check=False,
    )
    value = result.stdout.strip()
    if result.returncode == 0 and value:
        return value
    detail = result.stderr.strip() or "git rev-parse returned no commit"
    return f"unknown: failed to resolve {session_branch}: {detail}"


def _validate_apply_fork_state(
    state: dict[str, object],
    session_branch: str,
) -> str:
    """apply fork の state 前提条件を検証し、session start commit を返す。"""
    session = state.get("session")
    apply = state.get("apply")
    if not isinstance(session, dict) or not isinstance(apply, dict):
        raise CmocError(
            "session state ファイルの形式が不正です。",
            [
                "state JSON の session/apply セクションを確認して復旧してください。",
                "復旧できない場合は、現在の session を使わず新しい session を開始してください。",
            ],
            f"現在の branch: {session_branch}",
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
    if apply.get("state") != "ready":
        raise CmocError(
            "apply run を開始できる状態ではありません。",
            [
                "`cmoc apply join` または `cmoc apply abandon` を完了してから再実行してください。",
                "session state の apply.state を確認してください。",
            ],
            f"apply.state: {apply.get('state')}",
        )
    start_commit = session.get("session_start_commit")
    if not isinstance(start_commit, str) or not start_commit:
        raise CmocError(
            "session start commit が session state に記録されていません。",
            [
                "session state の session.session_start_commit を確認して復旧してください。",
                "復旧できない場合は、現在の session を使わず新しい session を開始してください。",
            ],
            f"現在の branch: {session_branch}",
        )
    return start_commit


def _validate_repeat_options(
    repeat_investigate_and_fix: int,
    repeat_improove_fixing_list: int,
) -> None:
    """apply fork の repeat 系オプションを副作用前に検証する。"""
    if repeat_investigate_and_fix < 0:
        raise CmocError(
            "調査・修正ループ回数に負の値は指定できません。",
            [
                "`--apply-loop` には 0 以上の整数を指定してください。",
                "既定の上限を使う場合は `--apply-loop` を省略してください。",
            ],
            f"repeat_investigate_and_fix: {repeat_investigate_and_fix}",
        )
    if repeat_improove_fixing_list < 0:
        raise CmocError(
            "要修正点リスト改善ループ回数に負の値は指定できません。",
            [
                "`--improove-fixing-list-loop` には 0 以上の整数を指定してください。",
                "既定の上限を使う場合は `--improove-fixing-list-loop` を省略してください。",
            ],
            f"repeat_improove_fixing_list: {repeat_improove_fixing_list}",
        )


def _validate_apply_scope(scope: str) -> None:
    """apply fork の scope オプション値を検証する。"""
    if scope in _APPLY_SCOPES:
        return
    raise CmocError(
        "`cmoc apply fork --scope` の値が不正です。",
        [
            "`rolling`, `session`, `full` のいずれかを指定してください。",
            "既定の rolling scope を使う場合は `--scope` を省略してください。",
        ],
        f"--scope: {scope}",
    )


def _scope_base_commit(
    state: dict[str, object],
    session_start_commit: str,
    scope: ApplyScope,
) -> str:
    """scope に応じて差分調査の base commit を返す。"""
    if scope == "session" or scope == "full":
        return session_start_commit
    session = state.get("session")
    if not isinstance(session, dict):
        raise CmocError(
            "session state ファイルの形式が不正です。",
            [
                "state JSON の session セクションを確認して復旧してください。",
                "復旧できない場合は、現在の session を使わず新しい session を開始してください。",
            ],
        )
    last_joined = session.get("last_joined_apply_oracle_snapshot_commit")
    if last_joined is None:
        return session_start_commit
    if not isinstance(last_joined, str) or not last_joined:
        raise CmocError(
            "session state ファイルの形式が不正です。",
            [
                "session.last_joined_apply_oracle_snapshot_commit を確認して復旧してください。",
                "復旧できない場合は、現在の session を使わず新しい session を開始してください。",
            ],
            f"last_joined_apply_oracle_snapshot_commit: {last_joined}",
        )
    return last_joined


def _create_apply_worktree(
    repo_root: Path,
    session_id: str,
    oracle_snapshot_commit: str,
    initial_plan: _ApplyWorktreePlan,
) -> _ApplyWorktreePlan:
    """snapshot から apply branch と専用 worktree を作成する。"""
    # timestamp 衝突に備えて短い sleep を挟みながら最大 10 回リトライする。
    last_plan = initial_plan
    for attempt in range(1, 11):
        plan = (
            initial_plan
            if attempt == 1
            else _plan_apply_worktree(repo_root, session_id)
        )
        last_plan = plan
        print(
            "apply worktree 作成試行 "
            f"({attempt}/10) {plan.apply_branch}"
        )
        branch_result = run_git(
            repo_root,
            ["branch", plan.apply_branch, oracle_snapshot_commit],
            check=False,
        )
        if branch_result.returncode != 0:
            sleep(0.001)
            continue
        worktree_result = run_git(
            repo_root,
            ["worktree", "add", str(plan.apply_worktree), plan.apply_branch],
            check=False,
        )
        if worktree_result.returncode == 0:
            return plan
        cleanup_result = run_git(
            repo_root,
            ["branch", "-D", plan.apply_branch],
            check=False,
        )
        if cleanup_result.returncode != 0:
            raise _ApplyWorktreeCreationError(
                "\n".join(
                    [
                        "apply worktree 作成失敗後の branch cleanup に失敗しました。",
                        f"apply_branch: {plan.apply_branch}",
                        f"apply_worktree: {plan.apply_worktree}",
                        "worktree add failure:",
                        _format_git_failure(worktree_result),
                        "branch cleanup failure:",
                        _format_git_failure(cleanup_result),
                    ]
                ),
                plan,
            )
        sleep(0.001)
    raise _ApplyWorktreeCreationError(
        "リトライ後も一意な apply worktree を作成できませんでした。",
        last_plan,
    )


def _format_git_failure(result: object) -> str:
    """git 失敗時の診断情報をユーザー向け detail に載せる。"""
    return "\n".join(
        [
            f"returncode: {getattr(result, 'returncode', '')}",
            f"stdout: {getattr(result, 'stdout', '').strip()}",
            f"stderr: {getattr(result, 'stderr', '').strip()}",
        ]
    )


@contextmanager
def _locked_apply_start(
    state_root: Path,
    session_id: str,
) -> Iterator[None]:
    """apply 開始時の ready 判定、artifact 作成、state 永続化を直列化する。"""
    lock_dir = state_root / ".cmoc" / "locks"
    lock_dir.mkdir(parents=True, exist_ok=True)
    lock_path = lock_dir / f"apply-fork-{session_id}.lock"
    with lock_path.open("a+", encoding="utf-8") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def _plan_apply_worktree(
    repo_root: Path,
    session_id: str,
) -> _ApplyWorktreePlan:
    """次に作成を試みる apply run id、branch、worktree path を組み立てる。"""
    apply_run_id = make_timestamp()
    apply_branch = f"{APPLY_BRANCH_PREFIX}{session_id}/{apply_run_id}"
    apply_worktree = repo_root / ".cmoc" / "worktrees" / session_id / apply_run_id
    return _ApplyWorktreePlan(apply_run_id, apply_branch, apply_worktree)


def _mark_apply_running(
    repo_root: Path,
    session_id: str,
    state: dict[str, object],
    apply_branch: str,
    oracle_snapshot_commit: str,
) -> None:
    """session state の apply セクションを running に更新する。"""
    apply = _mutable_apply_section(state)
    apply["state"] = "running"
    apply["apply_branch"] = apply_branch
    apply["oracle_snapshot_commit"] = oracle_snapshot_commit
    write_session_state(repo_root, session_id, state)
    write_apply_process_id(repo_root, session_id, os.getpid(), apply_branch)


def _mark_apply_completed(
    repo_root: Path,
    session_id: str,
    state: dict[str, object],
) -> None:
    """session state の apply セクションを completed に更新する。"""
    apply = _mutable_apply_section(state)
    apply["state"] = "completed"
    write_session_state(repo_root, session_id, state)
    clear_apply_process_id(repo_root, session_id)


def _mark_apply_error(
    repo_root: Path,
    session_id: str,
    state: dict[str, object],
    *,
    apply_branch: str | None = None,
    oracle_snapshot_commit: str | None = None,
) -> None:
    """開始済み apply run を error として永続化する。"""
    apply = _mutable_apply_section(state)
    changed = apply.get("state") != "error"
    apply["state"] = "error"
    if apply_branch:
        changed = changed or apply.get("apply_branch") != apply_branch
        apply["apply_branch"] = apply_branch
    if oracle_snapshot_commit:
        changed = (
            changed
            or apply.get("oracle_snapshot_commit") != oracle_snapshot_commit
        )
        apply["oracle_snapshot_commit"] = oracle_snapshot_commit
    if changed:
        write_session_state(repo_root, session_id, state)
    clear_apply_process_id(repo_root, session_id)


def _mutable_apply_section(
    state: dict[str, object],
) -> dict[str, object]:
    """session state から更新可能な apply セクションを取り出す。"""
    apply = state.get("apply")
    if not isinstance(apply, dict):
        raise CmocError(
            "session state ファイルの形式が不正です。",
            [
                "state JSON の apply セクションを確認して復旧してください。",
                "復旧できない場合は、現在の session を使わず新しい session を開始してください。",
            ],
        )
    return apply


def _investigate_discrepancies(
    repo_root: Path,
    investigation_base_commit: str,
    oracle_snapshot_commit: str,
    *,
    improvement_base_commit: str | None = None,
    timer: StepTimer,
    step_path: StepIndexPath,
    repeat_improove_fixing_list: int,
    scope: ApplyScope,
    dirty_oracle_paths: set[Path] | None = None,
    dirty_implementation_paths: set[Path] | None = None,
) -> list[dict[str, object]]:
    """oracle ファイル・実装ファイルごとに不整合調査を実行する。"""
    # ループごとに scope と調査対象を再評価する。
    discrepancies: list[dict[str, object]] = []
    partial = scope != "full"
    start_step(
        timer,
        (*step_path, (1, 5)),
        None,
        "調査対象選定",
    )
    oracle_targets = _target_oracle_files(
        repo_root,
        investigation_base_commit,
        oracle_snapshot_commit,
        partial,
        dirty_paths=dirty_oracle_paths,
    )
    implementation_targets = _target_implementation_files(
        repo_root,
        investigation_base_commit,
        oracle_snapshot_commit,
        partial,
        dirty_paths=dirty_implementation_paths,
    )

    jobs = [
        _InvestigationJob("oracle", index, len(oracle_targets), target)
        for index, target in enumerate(oracle_targets, start=1)
    ]
    jobs.extend(
        _InvestigationJob(
            "implementation",
            index,
            len(implementation_targets),
            target,
        )
        for index, target in enumerate(implementation_targets, start=1)
    )
    start_step(
        timer,
        (*step_path, (2, 5)),
        None,
        "ファイル別調査を並列実行",
    )
    for job in jobs:
        label = (
            "oracle 調査"
            if job.kind == "oracle"
            else "実装調査"
        )
        write_console_block(
            f"{label} ({job.index}/{job.total}) {job.target.path}"
        )
    if jobs:
        with ThreadPoolExecutor(max_workers=len(jobs)) as executor:
            futures = [
                executor.submit(
                    copy_context().run,
                    _run_investigation_job,
                    repo_root,
                    job,
                )
                for job in jobs
            ]
            for future in futures:
                discrepancies.extend(future.result())

    return _improove_fixing_list(
        repo_root,
        discrepancies,
        improvement_base_commit or oracle_snapshot_commit,
        repeat_improove_fixing_list,
        timer=timer,
        step_path=(*step_path, (4, 5)),
    )


def _run_investigation_job(
    repo_root: Path,
    job: _InvestigationJob,
) -> list[dict[str, object]]:
    """1 file 起点の不整合調査を実行し、fixing_points を返す。"""
    if job.kind == "oracle":
        prompt = _investigation_prompt(repo_root, job.target)
        purpose = f"oracle 調査 {job.target.path.relative_to(repo_root)}"
    else:
        prompt = _implementation_investigation_prompt(repo_root, job.target)
        purpose = (
            "実装調査 "
            f"{job.target.path.relative_to(repo_root)}"
        )
    payload = parse_json_object(
        run_codex_exec(
            repo_root,
            prompt,
            purpose=purpose,
            read_only=True,
            expect_json=True,
            output_schema=_DISCREPANCY_OUTPUT_SCHEMA,
            json_validator=_validate_discrepancy_payload,
            model=FRONTIER_MODEL,
            reasoning_effort=FRONTIER_REASONING_EFFORT,
            index_excluded_roots=_apply_index_excluded_roots(repo_root),
        )
    )
    return _fixing_points_with_head_commit_hash(repo_root, payload)


def _target_oracle_files(
    repo_root: Path,
    base_commit: str,
    oracle_snapshot_commit: str,
    partial: bool,
    *,
    dirty_paths: set[Path] | None = None,
) -> list[_InvestigationTarget]:
    """適用モードに応じた oracle 調査対象を返す。"""
    # apply run 開始時の snapshot に調査対象を固定する。
    all_files = _oracle_files_at_commit(repo_root, oracle_snapshot_commit)
    snapshot_paths = set(all_files)
    if dirty_paths is not None:
        return [
            _InvestigationTarget(
                path,
                exists_at_snapshot=path in snapshot_paths,
                exists_in_worktree=path.exists(),
            )
            for path in sorted(dirty_paths)
        ]
    if not partial:
        return [_InvestigationTarget(path) for path in all_files]
    changed = set(
        _changed_oracle_files_at_commit(
            repo_root,
            base_commit,
            oracle_snapshot_commit,
        )
    )
    return [
        _InvestigationTarget(path)
        for path in sorted(changed)
        if path in snapshot_paths
    ]


def _target_implementation_files(
    repo_root: Path,
    base_commit: str,
    oracle_snapshot_commit: str,
    partial: bool,
    *,
    dirty_paths: set[Path] | None = None,
) -> list[_InvestigationTarget]:
    """適用モードに応じた実装調査対象を返す。"""
    # apply run 開始時の snapshot に調査対象を固定する。
    all_files = _implementation_files_at_commit(
        repo_root,
        oracle_snapshot_commit,
    )
    snapshot_paths = set(all_files)
    if dirty_paths is not None:
        return [
            _InvestigationTarget(
                path,
                exists_at_snapshot=path in snapshot_paths,
                exists_in_worktree=path.exists(),
            )
            for path in sorted(dirty_paths)
        ]
    if not partial:
        return [_InvestigationTarget(path) for path in all_files]
    changed = set(
        _changed_implementation_files_at_commit(
            repo_root,
            base_commit,
            oracle_snapshot_commit,
        )
    )
    return [
        _InvestigationTarget(path)
        for path in sorted(changed)
        if path in snapshot_paths
    ]


def _oracle_files_at_commit(repo_root: Path, commit_hash: str) -> list[Path]:
    """指定 commit に存在する oracle ファイルを列挙する。"""
    paths = _tracked_files_at_commit(repo_root, commit_hash, "oracles")
    return [
        repo_root / path
        for path in filter_oracle_file_paths_at_commit(
            repo_root,
            commit_hash,
            paths,
        )
    ]


def _implementation_files_at_commit(
    repo_root: Path,
    commit_hash: str,
) -> list[Path]:
    """指定 commit に存在する実装ファイルを列挙する。"""
    paths = _tracked_files_at_commit(repo_root, commit_hash, ".")
    return [
        repo_root / path
        for path in _filter_implementation_file_paths_at_commit(
            repo_root,
            commit_hash,
            paths,
        )
    ]


def _changed_oracle_files_at_commit(
    repo_root: Path,
    base_commit: str,
    commit_hash: str,
) -> list[Path]:
    """指定 commit 範囲で変更された oracle ファイルを列挙する。"""
    return [
        repo_root / path
        for path in filter_oracle_file_paths_at_commit(
            repo_root,
            commit_hash,
            _changed_files_between_commits(
                repo_root,
                base_commit,
                commit_hash,
                "oracles",
            ),
        )
    ]


def _changed_implementation_files_at_commit(
    repo_root: Path,
    base_commit: str,
    commit_hash: str,
) -> list[Path]:
    """指定 commit 範囲で変更された実装ファイルを列挙する。"""
    return [
        repo_root / path
        for path in _filter_implementation_file_paths_at_commit(
            repo_root,
            commit_hash,
            _changed_files_between_commits(
                repo_root,
                base_commit,
                commit_hash,
                ".",
            ),
        )
    ]


def _filter_implementation_file_paths(
    repo_root: Path,
    relative_paths: list[str],
) -> list[str]:
    """root 相対 path から apply fork の実装調査対象だけを返す。"""
    return filter_apply_implementation_file_paths(repo_root, relative_paths)


def _filter_implementation_file_paths_at_commit(
    repo_root: Path,
    commit_hash: str,
    relative_paths: list[str],
) -> list[str]:
    """指定 commit の root `.gitignore` で apply 実装調査対象だけを返す。"""
    return filter_apply_implementation_file_paths_at_commit(
        repo_root,
        commit_hash,
        relative_paths,
    )


def _tracked_files_at_commit(
    repo_root: Path,
    commit_hash: str,
    pathspec: str,
) -> list[str]:
    """指定 commit の tracked file 一覧を repo 相対 path で返す。"""
    result = run_git(
        repo_root,
        ["ls-tree", "-r", "-z", "--name-only", commit_hash, "--", pathspec],
    )
    return sorted(git_name_only_paths(result.stdout))


def _changed_files_between_commits(
    repo_root: Path,
    base_commit: str,
    commit_hash: str,
    pathspec: str,
    *,
    include_deleted: bool = False,
) -> list[str]:
    """指定 commit 範囲で変更された path を返す。

    既定では削除差分は対象外にし、rename/copy は変更後 path だけを返す。
    include_deleted=True では削除 path と rename 前 path も返す。
    """
    result = run_git(
        repo_root,
        [
            "log",
            "--name-status",
            "-z",
            "-M",
            "--format=",
            f"{base_commit}..{commit_hash}",
            "--",
            pathspec,
        ],
    )
    paths: set[str] = set()
    for status, status_paths in git_name_status_entries(result.stdout):
        status_kind = status[:1]
        if status_kind not in {"A", "C", "D", "M", "R", "T"}:
            continue
        if status_kind == "D":
            if include_deleted and status_paths:
                paths.add(status_paths[0])
            continue
        if status_kind in {"C", "R"}:
            if len(status_paths) >= 2:
                if include_deleted and status_kind == "R":
                    paths.add(status_paths[0])
                paths.add(status_paths[1])
            continue
        if status_paths:
            paths.add(status_paths[0])
    return sorted(paths)


def _improove_fixing_list(
    repo_root: Path,
    discrepancies: list[dict[str, object]],
    base_commit: str,
    repeat_improove_fixing_list: int,
    *,
    timer: StepTimer,
    step_path: StepIndexPath,
) -> list[dict[str, object]]:
    """要修正点リストを最大指定回数まで Codex CLI に改善させる。"""
    if not discrepancies:
        return []

    # 空リストまたは前回と同一の改善結果を、収束として早期終了する。
    improved = discrepancies
    for loop_index in range(1, repeat_improove_fixing_list + 1):
        start_step(
            timer,
            (*step_path, (loop_index, repeat_improove_fixing_list)),
            None,
            "要修正点リスト改善",
        )
        next_improved = _organize_discrepancies(
            repo_root,
            improved,
            base_commit,
        )
        write_console_block(
            "要修正点リスト改善ループ "
            f"({loop_index}/{repeat_improove_fixing_list}) 要修正点: "
            f"{len(next_improved)}"
        )
        if not next_improved:
            return []
        if next_improved == improved:
            break
        improved = next_improved
    return improved


def _organize_discrepancies(
    repo_root: Path,
    discrepancies: list[dict[str, object]],
    base_commit: str | None = None,
) -> list[dict[str, object]]:
    """連結した不整合リストを Codex CLI に整理させる。"""
    # 整理結果も同じ Structured Output schema で受け取って検証する。
    branch_name = current_branch(repo_root)
    if base_commit is None:
        base_commit = read_session_start_commit(repo_root, branch_name)
    head_commit_hash = head_commit(repo_root)
    payload = parse_json_object(
        run_codex_exec(
            repo_root,
            _organize_prompt(
                repo_root,
                discrepancies,
                branch_name,
                base_commit,
                head_commit_hash,
            ),
            purpose="要修正点整理",
            read_only=True,
            expect_json=True,
            output_schema=_DISCREPANCY_OUTPUT_SCHEMA,
            json_validator=_validate_discrepancy_payload,
            index_excluded_roots=_apply_index_excluded_roots(repo_root),
            model=FRONTIER_MODEL,
            reasoning_effort=FRONTIER_HIGH_REASONING_EFFORT,
        )
    )
    return _fixing_points_with_head_commit_hash(repo_root, payload)


def _fixing_points_with_head_commit_hash(
    repo_root: Path,
    payload: dict[str, object],
) -> list[dict[str, object]]:
    """Structured Output の要修正点へ発見時 HEAD commit hash を付与する。"""
    # AI 出力の git_head_commit_hash は信用せず、cmoc 側で現在の HEAD を記録する。
    commit_hash = head_commit(repo_root)
    values = payload.get("fixing_points")
    if not isinstance(values, list):
        return []
    fixing_points: list[dict[str, object]] = []
    for value in values:
        if not isinstance(value, dict):
            continue
        fixing_point = dict(value)
        fixing_point["git_head_commit_hash"] = commit_hash
        fixing_points.append(fixing_point)
    return fixing_points


def _dirty_oracle_paths_from_discrepancies(
    repo_root: Path,
    discrepancies: list[dict[str, object]],
) -> set[Path]:
    """最終要修正点リストの根拠から次回調査する oracle path を返す。"""
    return {
        repo_root / path
        for path in filter_oracle_file_paths(
            repo_root,
            _evidence_relative_paths(repo_root, discrepancies),
        )
    }


def _dirty_implementation_paths_from_discrepancies(
    repo_root: Path,
    discrepancies: list[dict[str, object]],
) -> set[Path]:
    """最終要修正点リストの根拠から次回調査する実装 path を返す。"""
    return {
        repo_root / path
        for path in _filter_implementation_file_paths(
            repo_root,
            _evidence_relative_paths(repo_root, discrepancies),
        )
    }


def _evidence_relative_paths(
    repo_root: Path,
    discrepancies: list[dict[str, object]],
) -> list[str]:
    """要修正点 evidence の path を repo 相対 path に正規化する。"""
    paths: set[str] = set()
    for discrepancy in discrepancies:
        evidences = discrepancy.get("evidences")
        if not isinstance(evidences, list):
            continue
        for evidence in evidences:
            if not isinstance(evidence, dict):
                continue
            value = evidence.get("path")
            if not isinstance(value, str) or not value:
                continue
            relative_path = _repo_relative_path(repo_root, value)
            if relative_path is not None:
                paths.add(relative_path)
    return sorted(paths)


def _repo_relative_path(repo_root: Path, value: str) -> str | None:
    """絶対・相対どちらの evidence path も repo 相対 path に変換する。"""
    path = Path(value)
    try:
        if path.is_absolute():
            return path.resolve().relative_to(repo_root.resolve()).as_posix()
        return path.as_posix()
    except ValueError:
        return None


def _changed_implementation_files_since(
    repo_root: Path,
    base_commit: str,
    commit_hash: str,
) -> set[Path]:
    """指定 commit 範囲で変更された実装 path を絶対 path 集合で返す。"""
    return {
        repo_root / path
        for path in _filter_implementation_file_paths_at_commit(
            repo_root,
            commit_hash,
            _changed_files_between_commits(
                repo_root,
                base_commit,
                commit_hash,
                ".",
                include_deleted=True,
            ),
        )
    }


def _apply_discrepancies(
    repo_root: Path,
    discrepancies: list[dict[str, object]],
    *,
    timer: StepTimer,
    step_path: StepIndexPath,
    dirty_implementation_paths: set[Path] | None = None,
) -> None:
    """Codex CLI に不整合追従作業を依頼する。"""
    # 不整合 1 件ごとに修正、禁止領域検査、commit までを完結させる。
    for index, discrepancy in enumerate(discrepancies, start=1):
        start_step(
            timer,
            (*step_path, (index, len(discrepancies))),
            None,
            "要修正点適用",
        )
        write_console_block(
            f"要修正点適用 ({index}/{len(discrepancies)})"
        )
        before_head = head_commit(repo_root)
        run_codex_exec(
            repo_root,
            _apply_prompt(repo_root, discrepancy),
            purpose=f"要修正点適用 {index}/{len(discrepancies)}",
            read_only=False,
            expect_json=False,
            index_excluded_roots=_apply_index_excluded_roots(repo_root),
        )
        _assert_forbidden_paths_unchanged_since(
            repo_root,
            before_head,
            allow_maintained_index_paths=True,
        )
        _assert_forbidden_paths_clean(
            repo_root,
            allow_maintained_index_paths=True,
        )
        _commit_all_changes(repo_root)
        after_head = head_commit(repo_root)
        if dirty_implementation_paths is not None and after_head != before_head:
            dirty_implementation_paths.update(
                _changed_implementation_files_since(
                    repo_root,
                    before_head,
                    after_head,
                )
            )


def _commit_all_changes(repo_root: Path) -> None:
    """未コミット差分を Codex 生成メッセージで commit する。"""
    # 差分が無ければ commit message 生成も git commit も行わない。
    if not changed_paths(repo_root):
        return

    # 実装差分によって INDEX.md が古くなった場合は commit 前に更新する。
    before_index_head = head_commit(repo_root)
    _maintain_apply_indexes(repo_root)
    _assert_forbidden_paths_unchanged_since(
        repo_root,
        before_index_head,
        allow_maintained_index_paths=True,
    )
    _assert_forbidden_paths_clean(
        repo_root,
        allow_maintained_index_paths=True,
    )
    if not changed_paths(repo_root):
        return

    # Codex に 1 行 commit message を生成させ、空なら既定値を使う。
    message = run_codex_exec(
        repo_root,
        _commit_message_prompt(repo_root),
        purpose="commit message 生成",
        read_only=True,
        expect_json=False,
        model=COMMIT_MESSAGE_MODEL,
        reasoning_effort=COMMIT_MESSAGE_REASONING_EFFORT,
        index_excluded_roots=_apply_index_excluded_roots(repo_root),
    ).strip()
    if not message:
        message = "Apply oracle implementation changes"

    # 最終的な全差分を 1 commit にまとめる。
    run_git(repo_root, ["add", "--all"])
    run_git(repo_root, ["commit", "-m", message])


def _maintain_apply_indexes(repo_root: Path) -> bool:
    """apply worktree 上で cmoc 管理 INDEX.md を保守する。"""
    excluded_roots = _apply_index_excluded_roots(repo_root)
    _assert_excluded_indexes_current(repo_root, excluded_roots)
    if _maintain_indexes_accepts_excluded_roots():
        return maintain_indexes(
            repo_root,
            excluded_index_roots=excluded_roots,
        )
    return maintain_indexes(repo_root)


def _maintain_indexes_accepts_excluded_roots() -> bool:
    """テスト用 monkeypatch も考慮して除外 root 引数の有無を判定する。"""
    parameters = signature(maintain_indexes).parameters.values()
    for parameter in parameters:
        if parameter.name == "excluded_index_roots":
            return True
        if parameter.kind == Parameter.VAR_KEYWORD:
            return True
    return False


def _apply_index_excluded_roots(repo_root: Path) -> list[Path]:
    """apply worktree の INDEX メンテナンス除外 root 群を返す。"""
    return [repo_root / "oracles"]


def _assert_excluded_indexes_current(
    repo_root: Path,
    excluded_roots: list[Path],
) -> None:
    """編集禁止 root の INDEX 不整合を、更新せずに事前検出する。"""
    indexed_roots = [
        root
        for root in excluded_roots
        if root.exists() and any(root.rglob("INDEX.md"))
    ]
    if not indexed_roots:
        return
    inconsistencies = find_index_inconsistencies(
        repo_root,
        index_roots=indexed_roots,
    )
    if not inconsistencies:
        return
    raise CmocError(
        "編集禁止パス配下の INDEX.md が実在ファイル構成と一致していません。",
        [
            "編集禁止パスは apply では自動更新できないため、先に INDEX.md を整備してください。",
            "整備後に `cmoc apply` を再実行してください。",
        ],
        "\n".join(inconsistencies),
    )


def _assert_forbidden_paths_clean(
    repo_root: Path,
    *,
    allow_maintained_index_paths: bool = False,
) -> None:
    """Codex CLI が編集禁止領域を変更していないことを確認する。"""
    # prompt 上の禁止領域に差分があれば、commit 前に中断する。
    forbidden = [
        path
        for path in _changed_paths_for_forbidden_check(repo_root)
        if _is_forbidden_changed_path(path)
        and not _is_allowed_maintained_index_path_in_forbidden_check(
            repo_root,
            path,
            allow_maintained_index_paths,
        )
    ]
    if forbidden:
        raise CmocError(
            "実装作業により編集禁止パスが変更されました。",
            [
                "編集禁止パスの変更を確認し、手動で解消してください。",
                "作業ツリーが許容できる状態になってから `cmoc apply` を再実行してください。",
            ],
            "\n".join(forbidden),
        )


def _assert_forbidden_paths_unchanged_since(
    repo_root: Path,
    before_commit: str,
    *,
    allow_maintained_index_paths: bool = False,
) -> None:
    """Codex CLI 中の commit 済み禁止 path 変更を検出する。"""
    forbidden = [
        path
        for path in _changed_paths_since_for_forbidden_check(
            repo_root,
            before_commit,
        )
        if _is_forbidden_changed_path(path)
        and not _is_allowed_maintained_index_path_in_forbidden_check(
            repo_root,
            path,
            allow_maintained_index_paths,
        )
    ]
    if forbidden:
        raise CmocError(
            "実装作業により編集禁止パスが変更されました。",
            [
                "編集禁止パスの変更を確認し、手動で解消してください。",
                "作業ツリーが許容できる状態になってから `cmoc apply` を再実行してください。",
            ],
            "\n".join(forbidden),
        )


def _is_allowed_maintained_index_path_in_forbidden_check(
    repo_root: Path,
    relative_path: str,
    allow_maintained_index_paths: bool,
) -> bool:
    """cmoc 管理 INDEX.md の自動差分だけ禁止 path 検査で許可する。"""
    return (
        allow_maintained_index_paths
        and is_maintained_index_path(
            repo_root,
            relative_path,
            excluded_index_roots=_apply_index_excluded_roots(repo_root),
        )
    )


def _changed_paths_for_forbidden_check(repo_root: Path) -> list[str]:
    """禁止 path 検査用に未追跡ディレクトリ内の file path まで展開する。"""
    result = run_git(
        repo_root,
        ["status", "--porcelain=v1", "-z", "--untracked-files=all"],
    )
    return [path for _status, path in git_status_paths(result.stdout)]


def _changed_paths_since_for_forbidden_check(
    repo_root: Path,
    before_commit: str,
) -> list[str]:
    """禁止 path 検査用に commit 範囲内の変更 path を列挙する。"""
    result = run_git(
        repo_root,
        [
            "diff",
            "--name-status",
            "-z",
            "-M",
            "-C",
            "--find-copies-harder",
            f"{before_commit}..HEAD",
            "--",
        ],
    )
    paths: list[str] = []
    for status, entry_paths in git_name_status_entries(result.stdout):
        if status.startswith("R"):
            paths.extend(entry_paths)
        elif entry_paths:
            paths.append(entry_paths[-1])
    return paths


def _is_forbidden_changed_path(relative_path: str) -> bool:
    """workspace-write prompt で禁止した変更 path か判定する。"""
    return (
        relative_path == "README.md"
        or relative_path == "AGENTS.md"
        or relative_path == "oracles"
        or relative_path.startswith("oracles/")
        or relative_path == ".cmoc"
        or relative_path.startswith(".cmoc/")
        or relative_path == ".agents"
        or relative_path.startswith(".agents/")
        or relative_path == "memo"
        or relative_path.startswith("memo/")
    )


def _write_apply_report(
    repo_root: Path,
    report_repo_root: Path,
    session_id: str,
    apply_run_id: str,
    session_branch: str,
    branch_name: str,
    apply_worktree: Path,
    session_fork_commit: str,
    oracle_snapshot_commit: str,
    session_head_at_apply_start: str,
    session_head_at_apply_finish: str,
    completed: bool,
    discrepancy_counts: list[int],
) -> Path:
    """作業レポートを cmoc 側で組み立て、変更要約だけ Codex CLI に依頼する。"""
    report_dir = report_repo_root / ".cmoc" / "reports" / "apply" / "fork"

    result_label = "収束" if completed else "未収束"
    change_summary = _generate_change_summary(
        repo_root,
        branch_name,
        oracle_snapshot_commit,
    )

    def build_report(generated_at: str) -> str:
        """同一内容の report を一貫した front matter 付きで再生成する。"""
        report = _apply_report_with_front_matter(
            report_body=_render_apply_report_body(
                apply_branch=branch_name,
                result_label=result_label,
                completed=completed,
                discrepancy_counts=discrepancy_counts,
                change_summary=change_summary,
            ),
            generated_at=generated_at,
            session_id=session_id,
            apply_run_id=apply_run_id,
            session_branch=session_branch,
            apply_branch=branch_name,
            apply_worktree=apply_worktree,
            session_fork_commit=session_fork_commit,
            oracle_snapshot_commit=oracle_snapshot_commit,
            session_head_at_apply_start=session_head_at_apply_start,
            session_head_at_apply_finish=session_head_at_apply_finish,
            result_label=result_label,
            discrepancy_counts=discrepancy_counts,
        )
        _validate_apply_report(
            report,
            branch_name,
            result_label,
            completed,
            discrepancy_counts,
            require_front_matter=True,
        )
        return report

    try:
        return write_timestamped_report(report_dir, build_report)
    except ValueError as error:
        raise CmocError(
            "apply report の生成に必要な変更要約が不足しています。",
            [
                "Codex CLI の変更要約出力を確認してから再実行してください。",
                "問題が続く場合は apply branch の差分を確認してください。",
            ],
            str(error),
        ) from error


def _generate_change_summary(
    repo_root: Path,
    branch_name: str,
    oracle_snapshot_commit: str,
) -> list[dict[str, object]]:
    """apply branch の変更内容を Structured Output でカテゴリ別要約にする。"""
    changed_paths = _changed_paths_on_apply_branch(
        repo_root,
        oracle_snapshot_commit,
        branch_name,
    )
    if not changed_paths:
        return [
            {
                "category": "変更なし",
                "summary": (
                    "この apply run では、対象範囲に保存すべき実装差分は"
                    "発生しませんでした。"
                ),
                "changed_paths": [],
            }
        ]
    prompt = "\n".join(
        [
            "あなたはソフトウェア変更内容の要約担当です。",
            f"`{repo_root}` のブランチ `{branch_name}` の変更内容をカテゴリ別に要約してください。",
            "完了条件は Structured Output schema に従い、changes 配列だけを返すことです。",
            f"具体的には `{oracle_snapshot_commit}` から `{branch_name}` の HEAD までの差分と、"
            "working tree / staging area に残っている未コミット差分を対象にしてください。",
            "対象変更 path の機械的な収集結果は次の JSON 配列です。",
            json.dumps(changed_paths, ensure_ascii=False),
            "変更内容の意味論に基づいてカテゴリ分けしてください。",
            "changed_paths は repo 相対パスで、要約の根拠になる主要ファイルだけを列挙してください。",
            f"`{repo_root / 'oracles'}` と `{repo_root / '.agents'}` は編集禁止です。",
            f"`{repo_root / 'memo'}` は読み書き禁止です。",
            "ファイル編集は禁止です。",
        ]
    )
    payload = parse_json_object(
        run_codex_exec(
            repo_root,
            prompt,
            purpose="apply 変更要約",
            read_only=True,
            expect_json=True,
            output_schema=_CHANGE_SUMMARY_OUTPUT_SCHEMA,
            json_validator=_validate_change_summary_payload,
            model=COST_PERFORMANCE_MODEL,
            reasoning_effort=COST_PERFORMANCE_REASONING_EFFORT,
            index_excluded_roots=_apply_index_excluded_roots(repo_root),
        )
    )
    changes = payload.get("changes")
    if not isinstance(changes, list):
        return []
    return [change for change in changes if isinstance(change, dict)]


def _changed_paths_on_apply_branch(
    repo_root: Path,
    base_commit: str,
    branch_name: str,
) -> list[str]:
    """apply branch 上の commit 済み/未コミット変更 path を集約する。"""
    collected: set[str] = set()
    commands = [
        [
            "diff",
            "--name-status",
            "-z",
            "-M",
            "--diff-filter=ACDMRT",
            f"{base_commit}..{branch_name}",
            "--",
        ],
        [
            "diff",
            "--name-status",
            "-z",
            "-M",
            "--diff-filter=ACDMRT",
            "HEAD",
            "--",
        ],
        [
            "diff",
            "--cached",
            "--name-status",
            "-z",
            "-M",
            "--diff-filter=ACDMRT",
            "--",
        ],
    ]
    for command in commands:
        result = run_git(repo_root, command, check=False)
        if result.returncode not in (0, 1):
            continue
        for status, paths in git_name_status_entries(result.stdout):
            if status[:1] in {"A", "C", "D", "M", "R", "T"} and paths:
                collected.add(paths[-1])

    status_result = run_git(
        repo_root,
        ["status", "--porcelain=v1", "-z", "--untracked-files=all", "--"],
        check=False,
    )
    if status_result.returncode in (0, 1):
        for status, path in git_status_paths(status_result.stdout):
            if status == "??" or "D" in status:
                collected.add(path)
    return sorted(collected)


def _validate_change_summary_payload(value: object) -> None:
    """変更要約 Structured Output の意味的な最低条件を検査する。"""
    if not isinstance(value, dict):
        raise ValueError("change summary payload must be object.")
    changes = value.get("changes")
    if not isinstance(changes, list) or not changes:
        raise ValueError("changes must be a non-empty array.")
    for index, change in enumerate(changes, start=1):
        if not isinstance(change, dict):
            raise ValueError(f"changes[{index}] must be object.")
        for key in ("category", "summary"):
            if not isinstance(change.get(key), str) or not change[key].strip():
                raise ValueError(f"changes[{index}].{key} must be non-empty string.")
        paths = change.get("changed_paths")
        if not isinstance(paths, list) or any(
            not isinstance(path, str) or not path for path in paths
        ):
            raise ValueError(f"changes[{index}].changed_paths must be string array.")


def _render_apply_report_body(
    *,
    apply_branch: str,
    result_label: str,
    completed: bool,
    discrepancy_counts: list[int],
    change_summary: list[dict[str, object]],
) -> str:
    """cmoc が持つ確定情報と変更要約から Markdown report 本文を作る。"""
    count_lines = [
        f"- {index} 回目: {count} 件"
        for index, count in enumerate(discrepancy_counts, start=1)
    ]
    if not count_lines:
        count_lines = ["- 記録された調査ループはありません。"]
    if result_label == "未収束" and not completed:
        count_lines.append(
            "- 定型文: 回数上限に達したため、まだ要修正点が残っている可能性があります。"
        )

    lines = [
        "## 作業結果",
        result_label,
        "",
        "## 要修正点件数の推移",
        *count_lines,
        "",
        f"## ブランチ {apply_branch} 上の全変更内容",
    ]
    _append_change_summary_lines(lines, change_summary)
    return "\n".join(lines).strip()


def _append_change_summary_lines(
    lines: list[str],
    change_summary: list[dict[str, object]],
) -> None:
    """変更要約 Structured Output を Markdown 行へ追加する。"""
    for change in change_summary:
        category = str(change.get("category", "")).strip()
        summary = str(change.get("summary", "")).strip()
        paths = change.get("changed_paths")
        if not isinstance(paths, list):
            paths = []
        lines.extend(
            [
                f"### カテゴリ: {category}",
                summary,
            ]
        )
        if paths:
            lines.append("")
            lines.append("主な変更ファイル:")
            lines.extend(f"- `{path}`" for path in paths if isinstance(path, str))
        lines.append("")


def _best_effort_change_summary(
    repo_root: Path,
    branch_name: str,
    oracle_snapshot_commit: str,
) -> list[dict[str, object]]:
    """エラーレポート用に、可能な限り apply branch の変更要約を返す。"""
    try:
        change_summary = _generate_change_summary(
            repo_root,
            branch_name,
            oracle_snapshot_commit,
        )
        _validate_change_summary_payload({"changes": change_summary})
        return change_summary
    except Exception as error:
        return _fallback_change_summary_from_git(
            repo_root,
            branch_name,
            oracle_snapshot_commit,
            error,
        )


def _fallback_change_summary_from_git(
    repo_root: Path,
    branch_name: str,
    oracle_snapshot_commit: str,
    error: BaseException,
) -> list[dict[str, object]]:
    """Codex CLI 要約が使えない場合、git から取得できる範囲を report に残す。"""
    try:
        changed_paths = _changed_paths_on_apply_branch(
            repo_root,
            oracle_snapshot_commit,
            branch_name,
        )
    except Exception as diff_error:
        return [
            {
                "category": "変更要約生成失敗",
                "summary": (
                    "Codex CLI による変更内容要約に失敗し、git diff による"
                    "変更ファイル一覧の取得にも失敗しました。"
                    f"要約生成エラー: {type(error).__name__}: {error} / "
                    f"diff 取得エラー: {type(diff_error).__name__}: {diff_error}"
                ),
                "changed_paths": [],
            }
        ]
    if not changed_paths:
        return [
            {
                "category": "変更なし",
                "summary": (
                    "Codex CLI による変更内容要約には失敗しましたが、"
                    "git で確認できる apply branch 上の commit 済み変更と"
                    "未コミット変更のファイルはありませんでした。"
                    f"要約生成エラー: {type(error).__name__}: {error}"
                ),
                "changed_paths": [],
            }
        ]
    return [
        {
            "category": "変更ファイル一覧",
            "summary": (
                "Codex CLI による意味論的カテゴリ別要約には失敗しました。"
                "代替情報として、oracle snapshot commit から apply branch の"
                "HEAD までの変更と、working tree / staging area に残っている"
                "未コミット変更のファイル一覧を記録します。"
                f"要約生成エラー: {type(error).__name__}: {error}"
            ),
            "changed_paths": changed_paths,
        }
    ]


def _write_apply_error_report(
    report_repo_root: Path,
    session_id: str,
    apply_run_id: str,
    session_branch: str,
    apply_branch: str,
    apply_worktree: Path,
    session_fork_commit: str,
    oracle_snapshot_commit: str,
    session_head_at_apply_start: str,
    session_head_at_apply_finish: str,
    failed_stage: str,
    error: BaseException,
    discrepancy_counts: list[int],
) -> Path:
    """例外終了時の apply レポートを cmoc 側で保存する。"""
    report_dir = report_repo_root / ".cmoc" / "reports" / "apply" / "fork"

    count_lines = [
        f"- {index} 回目: {count} 件"
        for index, count in enumerate(discrepancy_counts, start=1)
    ]
    if not count_lines:
        count_lines = ["- エラー発生前に記録済みの要修正点件数はありません。"]

    summary_repo_root = (
        apply_worktree
        if apply_worktree.exists()
        else report_repo_root
    )
    change_summary = _best_effort_change_summary(
        summary_repo_root,
        apply_branch,
        oracle_snapshot_commit,
    )
    body_lines = [
        "## 作業結果",
        "エラー",
        "",
        "`cmoc apply fork` は途中でエラーが起きたため、"
        "調査・修正ループを正常に終了できませんでした。",
        "",
        "## エラー詳細",
        f"- Failed stage: `{failed_stage}`",
        f"- Exception type: `{type(error).__name__}`",
        f"- Exception message: `{error}`",
        "",
        "## 要修正点件数の推移",
        *count_lines,
        "",
        f"## ブランチ {apply_branch} 上の全変更内容",
    ]
    _append_change_summary_lines(body_lines, change_summary)
    body = "\n".join(body_lines).strip()

    def build_report(generated_at: str) -> str:
        """エラー終了 report を衝突回避後の生成時刻で再生成する。"""
        report = _apply_report_with_front_matter(
            report_body=body,
            generated_at=generated_at,
            session_id=session_id,
            apply_run_id=apply_run_id,
            session_branch=session_branch,
            apply_branch=apply_branch,
            apply_worktree=apply_worktree,
            session_fork_commit=session_fork_commit,
            oracle_snapshot_commit=oracle_snapshot_commit,
            session_head_at_apply_start=session_head_at_apply_start,
            session_head_at_apply_finish=session_head_at_apply_finish,
            result_label="エラー",
            discrepancy_counts=discrepancy_counts,
        )
        _validate_apply_report(
            report,
            apply_branch,
            "エラー",
            completed=False,
            discrepancy_counts=discrepancy_counts,
            require_front_matter=True,
        )
        return report

    return write_timestamped_report(report_dir, build_report)


def _validate_apply_report(
    report: str,
    branch_name: str,
    result_label: str,
    completed: bool,
    discrepancy_counts: list[int],
    *,
    require_front_matter: bool = False,
) -> None:
    """保存前の apply レポートが必須内容を持つことを機械的に確認する。"""
    # Markdown の完全な意味解釈ではなく、必須セクションと既知値の対応を検査する。
    missing: list[str] = []
    body = report
    if require_front_matter:
        front_matter, body = _split_yaml_front_matter(report)
        required_metadata = [
            "cmoc_session_id",
            "cmoc_apply_run_id",
            "cmoc_session_branch",
            "cmoc_session_fork_commit",
            "cmoc_apply_branch",
            "cmoc_apply_fork_commit",
            "apply_worktree_path",
            "oracle_snapshot_commit",
            "session_head_at_apply_start",
            "session_head_at_apply_finish",
            "result",
            "generated_at",
        ]
        for key in required_metadata:
            if key not in front_matter:
                missing.append(f"YAML Front Matter {key}")
        if front_matter.get("cmoc_apply_branch") != branch_name:
            missing.append("YAML Front Matter cmoc_apply_branch")
        if front_matter.get("result") != result_label:
            missing.append("YAML Front Matter result")

    sections = _markdown_sections(body)
    result_section = sections.get("作業結果")
    counts_section = sections.get("要修正点件数の推移")
    all_changes_section = _find_markdown_section(sections, "全変更内容")

    if result_section is None or result_label not in result_section.content:
        missing.append("作業結果の区分")

    if counts_section is None:
        missing.append("要修正点件数の推移")
    else:
        for index, count in enumerate(discrepancy_counts, start=1):
            if not _section_has_loop_count(counts_section, index, count):
                missing.append(f"要修正点件数の推移 loop {index}")
        if (
            result_label == "未収束"
            and not completed
            and "まだ要修正点が残っている可能性" not in counts_section.content
        ):
            missing.append("未収束時の残存可能性")

    if (
        all_changes_section is None
        or branch_name not in all_changes_section.heading
        or not _section_has_categorized_summary(all_changes_section.content)
    ):
        missing.append("ブランチ上の全変更内容の意味論的カテゴリ別要約")

    # 不完全な Codex 出力をそのまま保存せず、共通エラーとして中断する。
    if missing:
        raise ValueError(
            "Codex CLI が生成した apply report に必須内容がありません:\n"
            + "\n".join(missing)
        )


@dataclass(frozen=True)
class _MarkdownSection:
    """apply report の Markdown heading と本文を保持する。"""

    heading: str
    content: str


def _markdown_sections(markdown: str) -> dict[str, _MarkdownSection]:
    """Markdown を heading 単位の section に分ける。"""
    sections: dict[str, _MarkdownSection] = {}
    current_heading: str | None = None
    current_level: int | None = None
    current_lines: list[str] = []

    for line in markdown.splitlines():
        heading_match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if heading_match is not None:
            level = len(heading_match.group(1))
            if (
                current_heading is not None
                and current_level is not None
                and level <= current_level
            ):
                sections[current_heading] = _MarkdownSection(
                    heading=current_heading,
                    content="\n".join(current_lines).strip(),
                )
                current_heading = heading_match.group(2).strip()
                current_level = level
                current_lines = []
                continue
            if current_heading is None:
                current_heading = heading_match.group(2).strip()
                current_level = level
                current_lines = []
                continue
        if current_heading is not None:
            current_lines.append(line)

    if current_heading is not None:
        sections[current_heading] = _MarkdownSection(
            heading=current_heading,
            content="\n".join(current_lines).strip(),
        )
    return sections


def _find_markdown_section(
    sections: dict[str, _MarkdownSection],
    heading_keyword: str,
) -> _MarkdownSection | None:
    """heading に keyword を含む section を返す。"""
    for heading, section in sections.items():
        if heading_keyword in heading:
            return section
    return None


def _section_has_loop_count(section: _MarkdownSection, index: int, count: int) -> bool:
    """同じ行に loop 番号と件数が対応して書かれているかを返す。"""
    index_pattern = rf"(?<!\d){index}(?!\d)\s*(回目|ループ|loop)"
    count_pattern = rf"(?<!\d){count}(?!\d)\s*件"
    for line in section.content.splitlines():
        if re.search(index_pattern, line) and re.search(count_pattern, line):
            return True
    return False


def _section_has_categorized_summary(content: str) -> bool:
    """全変更内容 section にカテゴリ付き要約本文があるかを返す。"""
    meaningful_lines = [
        line.strip()
        for line in content.splitlines()
        if line.strip() and not set(line.strip()) <= {"-", "|", ":", " "}
    ]
    category_lines = [
        line for line in meaningful_lines if _line_declares_category(line)
    ]
    if not category_lines:
        return False
    non_category_lines = [
        line for line in meaningful_lines if not _line_declares_category(line)
    ]
    return bool(non_category_lines)


def _line_declares_category(line: str) -> bool:
    """行がカテゴリ名またはカテゴリ列を宣言しているかを返す。"""
    return re.search(r"カテゴリ\s*[:：|]", line) is not None


def _apply_report_with_front_matter(
    *,
    report_body: str,
    generated_at: str,
    session_id: str,
    apply_run_id: str,
    session_branch: str,
    apply_branch: str,
    apply_worktree: Path,
    session_fork_commit: str,
    oracle_snapshot_commit: str,
    session_head_at_apply_start: str,
    session_head_at_apply_finish: str,
    result_label: str,
    discrepancy_counts: list[int],
) -> str:
    """cmoc が確定できる apply report metadata を YAML Front Matter にする。"""
    front_matter = [
        "---",
        f"generated_at: {_yaml_string(generated_at)}",
        f"cmoc_session_id: {_yaml_string(session_id)}",
        f"cmoc_apply_run_id: {_yaml_string(apply_run_id)}",
        f"cmoc_session_branch: {_yaml_string(session_branch)}",
        f"cmoc_session_fork_commit: {_yaml_string(session_fork_commit)}",
        f"cmoc_apply_branch: {_yaml_string(apply_branch)}",
        f"cmoc_apply_fork_commit: {_yaml_string(oracle_snapshot_commit)}",
        f"apply_worktree_path: {_yaml_string(str(apply_worktree))}",
        f"oracle_snapshot_commit: {_yaml_string(oracle_snapshot_commit)}",
        f"session_head_at_apply_start: {_yaml_string(session_head_at_apply_start)}",
        f"session_head_at_apply_finish: {_yaml_string(session_head_at_apply_finish)}",
        f"result: {_yaml_string(result_label)}",
        f"discrepancy_counts: {json.dumps(discrepancy_counts)}",
        "---",
    ]
    return "\n".join([*front_matter, "", report_body.strip(), ""])


def _yaml_string(value: str) -> str:
    """単純な文字列 metadata を YAML double quoted scalar として出力する。"""
    return json.dumps(value, ensure_ascii=False)


def _split_yaml_front_matter(report: str) -> tuple[dict[str, str], str]:
    """apply report の YAML Front Matter を軽量に取り出す。"""
    if not report.startswith("---\n"):
        return {}, report
    front_matter_end = report.find("\n---\n", 4)
    if front_matter_end == -1:
        return {}, report

    front_matter: dict[str, str] = {}
    for line in report[4:front_matter_end].splitlines():
        if ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        value = raw_value.strip()
        if value.startswith('"') and value.endswith('"'):
            try:
                loaded = json.loads(value)
            except json.JSONDecodeError:
                loaded = value[1:-1]
            if isinstance(loaded, str):
                front_matter[key.strip()] = loaded
                continue
        front_matter[key.strip()] = value

    return front_matter, report[front_matter_end + len("\n---\n") :]


def _investigation_prompt(
    repo_root: Path,
    oracle_target: _InvestigationTarget,
) -> str:
    """不整合調査用 prompt を組み立てる。"""
    # Structured Output schema と禁止事項を prompt 上で明示する。
    target_note = _investigation_target_note(oracle_target)
    return "\n".join(
        [
            "あなたはソフトウェア実装の監査担当です。",
            f"`{oracle_target.path}` を起点に `{repo_root}` の要修正点を調査してください。",
            "完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです。",
            target_note,
            f"要修正点には、`{repo_root / 'oracles'}` 配下の仕様ファイルと"
            "実装との明確な不整合だけでなく、",
            "実装だけから見た成果物品質上の致命的な問題も含めてください。",
            "実装のみから発見した要修正点でも、関係する仕様要求を "
            "oracle_requirement に記載してください。",
            "指定ファイルは調査の起点であり、必要なら他の仕様ファイル・実装ファイルも読んでください。",
            "各要修正点には title、evidences、oracle_requirement、",
            "observed_implementation、reason、suggested_fix を含めてください。",
            "evidences には path、line_start、line_end、summary を含めてください。",
            "top-level の git_head_commit_hash は必ず含め、値は null で構いません。",
            "明確な要修正点がない場合だけ fixing_points に空配列を返してください。",
            f"`{repo_root / 'memo'}` は読み書き禁止です。",
            "ファイル編集は禁止です。",
        ]
    )


def _implementation_investigation_prompt(
    repo_root: Path,
    implementation_target: _InvestigationTarget,
) -> str:
    """実装ファイル起点の不整合調査用 prompt を組み立てる。"""
    # 指定ファイルは調査起点であり、必要な関連ファイル参照は許可する。
    target_note = _investigation_target_note(implementation_target)
    return "\n".join(
        [
            "あなたはソフトウェア実装の監査担当です。",
            f"`{implementation_target.path}` を起点に、",
            f"`{repo_root}` の要修正点を調査してください。",
            "完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです。",
            target_note,
            f"要修正点には、`{repo_root / 'oracles'}` 配下の仕様ファイルと"
            "実装との明確な不整合だけでなく、",
            "実装だけから見た成果物品質上の致命的な問題も含めてください。",
            "実装のみから発見した要修正点でも、関係する仕様要求を "
            "oracle_requirement に記載してください。",
            "指定ファイルは調査の起点であり、必要なら他の仕様ファイル・実装ファイルも読んでください。",
            "各要修正点には title、evidences、oracle_requirement、",
            "observed_implementation、reason、suggested_fix を含めてください。",
            "evidences には path、line_start、line_end、summary を含めてください。",
            "top-level の git_head_commit_hash は必ず含め、値は null で構いません。",
            "明確な要修正点がない場合だけ fixing_points に空配列を返してください。",
            f"`{repo_root / 'memo'}` は読み書き禁止です。",
            "ファイル編集は禁止です。",
        ]
    )


def _investigation_target_note(target: _InvestigationTarget) -> str:
    """target の存在状態に応じた調査観点を prompt に明示する。"""
    if target.exists_at_snapshot:
        if target.exists_in_worktree:
            return "この起点 path は調査対象として固定された commit 時点に存在するファイルです。"
        return (
            "この起点 path は調査対象として固定された commit 時点には存在し、"
            "現在の worktree には存在しません。"
            "前回までの修正で削除されたファイルとして、"
            "削除差分や履歴上の変更内容を確認して調査してください。"
        )
    if target.exists_in_worktree:
        return (
            "この起点 path は調査対象として固定された commit 時点では存在せず、"
            "現在の worktree には存在します。"
            "前回までの修正で新規作成されたファイルとして、"
            "現在の worktree の内容を確認して調査してください。"
        )
    else:
        return (
            "この起点 path は調査対象として固定された commit 時点では存在しません。"
            "削除差分や履歴上の変更内容を確認して調査してください。"
        )


def _organize_prompt(
    repo_root: Path,
    discrepancies: list[dict[str, object]],
    branch_name: str,
    base_commit: str,
    head_commit_hash: str,
) -> str:
    """不整合リスト整理用 prompt を組み立てる。"""
    # 個別調査結果の重複や矛盾を整理し、同じ schema で返させる。
    structured_discrepancies = _discrepancies_for_structured_output(
        discrepancies
    )
    return "\n".join(
        [
            "あなたはソフトウェア監査結果の整理担当です。",
            f"`{repo_root}` の要修正点リストを整理してください。",
            "完了条件は、指定された Structured Output schema に一致する JSON だけを返すことです。",
            "要修正点の内容の品質に明確な問題がない状態を目指してください。",
            (
                "重複する要修正点は 1 件にマージし、"
                "矛盾する修正方針は矛盾しない内容に調整してください。"
            ),
            (
                f"git ブランチ `{branch_name}` の "
                f"`{base_commit}..{head_commit_hash}` "
                "に含まれる過去の修正内容を確認し、その内容を考慮してください。"
            ),
            "False-Positive と判断できる要修正点は除外してください。",
            "要修正点を先頭から順番に対応した時に、作業順序として適切になるよう並べ替えてください。",
            "改善過程で発見した漏れがあれば、要修正点リストに追加してください。",
            "実装のみから発見した要修正点でも、関係する仕様要求を "
            "oracle_requirement に記載してください。",
            "改善点がない場合は入力と同じ要修正点リストを返してください。",
            "top-level の git_head_commit_hash は必ず含め、値は null で構いません。",
            "明確な要修正点がない場合だけ fixing_points に空配列を返してください。",
            "連結済み要修正点リスト: "
            f"{json.dumps(structured_discrepancies, ensure_ascii=False)}",
            f"`{repo_root / 'memo'}` は読み書き禁止です。",
            "ファイル編集は禁止です。",
        ]
    )


def _discrepancies_for_structured_output(
    discrepancies: list[dict[str, object]],
) -> list[dict[str, object]]:
    """cmoc 内部メタデータを Structured Output 用の要修正点から除外する。"""
    # fixing_points item は schema 上 additionalProperties false なので内部キーを出さない。
    return [
        {
            key: value
            for key, value in discrepancy.items()
            if key != "git_head_commit_hash"
        }
        for discrepancy in discrepancies
    ]


def _apply_prompt(
    repo_root: Path,
    discrepancy: dict[str, object],
) -> str:
    """不整合追従作業用 prompt を組み立てる。"""
    # workspace-write 実行用に編集禁止領域を無条件で明示する。
    return "\n".join(
        [
            "あなたはソフトウェア実装担当です。",
            f"`{repo_root}` の実装を、要修正点情報に記載された仕様要求に"
            "追従するようベストエフォートで更新してください。",
            "完了条件は、必要と判断した実装修正とテスト更新を終え、変更内容と残課題を報告することです。",
            "作業が必要と判断できる場合は、実装修正と必要なテスト更新を行ってください。",
            "以下の要修正点情報は作業のためのヒントです。",
            "絶対に従わなければならない指示書としては扱わないでください。",
            "実装状況や仕様ファイルを確認した結果として不適切なら、"
            "この要修正点情報は無視してかまいません。",
            "作業目的は、要修正点が指摘している問題の修正を試みることです。",
            "要修正点本文への逐語的追従や、要修正点で述べている目的を達成した保証は不要です。",
            f"要修正点: {json.dumps(discrepancy, ensure_ascii=False)}",
            f"`{repo_root / 'oracles'}` は編集禁止です。",
            f"`{repo_root / 'README.md'}` は編集禁止です。",
            f"`{repo_root / 'AGENTS.md'}` は編集禁止です。",
            f"`{repo_root / '.cmoc'}` は編集禁止です。",
            f"`{repo_root / '.agents'}` は編集禁止です。",
            f"`{repo_root / 'memo'}` は読み書き禁止です。",
        ]
    )


def _commit_message_prompt(repo_root: Path) -> str:
    """commit message 生成用 prompt を組み立てる。"""
    # read-only 実行で commit message の文字列だけを要求する。
    return "\n".join(
        [
            "あなたは git commit message の作成担当です。",
            f"`{repo_root}` の現在の変更に対する簡潔な commit message を 1 行で書いてください。",
            "完了条件は、commit message だけを出力することです。",
            f"`{repo_root / 'memo'}` は読み書き禁止です。",
            "ファイル編集は禁止です。",
        ]
    )


def _validate_discrepancy_payload(value: object) -> None:
    """不整合調査 Structured Output の schema を検査する。"""
    # top-level は git_head_commit_hash と fixing_points に限定する。
    if not isinstance(value, dict):
        raise ValueError("Expected JSON object.")
    required_keys = {"git_head_commit_hash", "fixing_points"}
    if set(value) != required_keys:
        raise ValueError("Expected git_head_commit_hash and fixing_points keys.")
    commit_hash = value.get("git_head_commit_hash")
    if commit_hash is not None and not isinstance(commit_hash, str):
        raise ValueError("git_head_commit_hash must be a string or null.")
    fixing_points = value.get("fixing_points")
    if not isinstance(fixing_points, list):
        raise ValueError("fixing_points must be a list.")

    # 各 fixing point item の required keys を完全一致で検査する。
    required_keys = {
        "title",
        "evidences",
        "oracle_requirement",
        "observed_implementation",
        "reason",
        "suggested_fix",
    }
    for index, item in enumerate(fixing_points):
        # item ごとに型と各プロパティの型を検査する。
        if not isinstance(item, dict):
            raise ValueError(f"fixing_points[{index}] must be an object.")
        if set(item) != required_keys:
            raise ValueError(
                f"fixing_points[{index}] keys do not match schema."
            )
        _require_string(item, "title", index)
        _validate_evidences(item["evidences"], index)
        for key in [
            "oracle_requirement",
            "observed_implementation",
            "reason",
            "suggested_fix",
        ]:
            _require_string(item, key, index)


def _require_string(item: dict[str, object], key: str, index: int) -> None:
    """schema 上 string の項目を検査する。"""
    # 対象 key が Python str であることを保証する。
    if not isinstance(item[key], str):
        raise ValueError(f"fixing_points[{index}].{key} must be a string.")


def _validate_evidences(value: object, item_index: int) -> None:
    """schema 上 evidences の項目を検査する。"""
    # evidence は根拠位置の構造化情報として完全一致で検査する。
    if not isinstance(value, list) or not value:
        raise ValueError(
            f"fixing_points[{item_index}].evidences must be a non-empty list."
        )
    required_keys = {"path", "line_start", "line_end", "summary"}
    for evidence_index, evidence in enumerate(value):
        if not isinstance(evidence, dict):
            raise ValueError(
                "fixing_points"
                f"[{item_index}].evidences[{evidence_index}] "
                "must be an object."
            )
        if set(evidence) != required_keys:
            raise ValueError(
                "fixing_points"
                f"[{item_index}].evidences[{evidence_index}] "
                "keys do not match schema."
            )
        _require_evidence_string(evidence, "path", item_index, evidence_index)
        _require_evidence_absolute_path(evidence, item_index, evidence_index)
        _require_evidence_nullable_int(
            evidence,
            "line_start",
            item_index,
            evidence_index,
        )
        _require_evidence_nullable_int(
            evidence,
            "line_end",
            item_index,
            evidence_index,
        )
        _require_evidence_string(
            evidence,
            "summary",
            item_index,
            evidence_index,
        )


def _require_evidence_string(
    item: dict[object, object],
    key: str,
    item_index: int,
    evidence_index: int,
) -> None:
    """schema 上 evidence 内 string の項目を検査する。"""
    if not isinstance(item[key], str):
        raise ValueError(
            "fixing_points"
            f"[{item_index}].evidences[{evidence_index}].{key} "
            "must be a string."
        )


def _require_evidence_absolute_path(
    item: dict[object, object],
    item_index: int,
    evidence_index: int,
) -> None:
    """schema 上 evidence path が絶対パスであることを検査する。"""
    path = item["path"]
    if not isinstance(path, str) or not Path(path).is_absolute():
        raise ValueError(
            "fixing_points"
            f"[{item_index}].evidences[{evidence_index}].path "
            "must be an absolute path."
        )


def _require_evidence_nullable_int(
    item: dict[object, object],
    key: str,
    item_index: int,
    evidence_index: int,
) -> None:
    """schema 上 evidence 内 integer|null の項目を検査する。"""
    if (
        item[key] is not None
        and (not isinstance(item[key], int) or isinstance(item[key], bool))
    ):
        raise ValueError(
            "fixing_points"
            f"[{item_index}].evidences[{evidence_index}].{key} "
            "must be integer or null."
        )
