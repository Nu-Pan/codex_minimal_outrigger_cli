"""session branch を home branch へ merge し、conflict 解消を検証する。"""

# {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md
import json
from pathlib import Path
from typing import Callable

from acp.builder.session.join.conflict_resolution import (
    build_session_join_conflict_resolution_parameter,
)
from cmoc_runtime import (
    CmocError,
    CommandResult,
    TerminalResult,
    current_branch,
    head_commit,
    load_state_for_branch,
    repo_root,
    require_clean_worktree,
    run_cli_subcommand,
    run_codex_exec,
    run_git,
    session_fork_lock,
    start_subcommand_step,
    work_root,
    write_state,
)
from commons.runtime_document_search_scope import oracle_doc_scope
from commons.runtime_merge_conflict import resolve_merge_conflicts, unmerged_paths
from commons.runtime_primary_report import update_primary_report_fields
from commons.runtime_results import CodexExecCallable

_CodexExec = CodexExecCallable
_GitRun = Callable[..., CommandResult]


def cmoc_session_join_impl() -> None:
    """CLI runtime を通して session join を実行する。"""
    run_cli_subcommand(
        _cmoc_session_join_body,
        run_codex_exec,
        run_git,
        command_name="session join",
        command_argv=["cmoc", "session", "join"],
        total_steps=4,
        use_work_root_runtime=True,
    )


def _cmoc_session_join_body(
    codex_exec: _CodexExec, git: _GitRun = run_git
) -> TerminalResult:
    """active session branch を session home branch へ merge する。"""
    root = repo_root()
    # {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md
    # conflict resolution agent call は session branch/worktree を直接編集するため、
    # fork・join・abandon を同じ repository lock で直列化する。
    with session_fork_lock(root):
        work = work_root()
        branch = current_branch(work)
        update_primary_report_fields(
            session_branch=branch,
            session_state_before=None,
            session_state_after=None,
        )
        start_subcommand_step(2, "事前条件を確認", "validate preconditions")
        session_id, path, state = load_state_for_branch(root, branch)
        home = state.session.session_home_branch
        update_primary_report_fields(
            home_branch=home,
            session_state_before=state.session.state,
        )
        if not branch.startswith("cmoc/session/"):
            raise CmocError(
                "session join は session branch 上で実行してください。", [], branch
            )
        if state.session.state != "active" or state.run.state != "ready":
            raise CmocError(
                "session join の事前条件を満たしていません。",
                ["session.state と run.state を確認してください。"],
                json.dumps(state.to_dict(), ensure_ascii=False, indent=2),
            )
        require_clean_worktree(work)
        if not home:
            raise CmocError("session home branch を特定できません。", [], str(path))
        session_head_before_merge = head_commit(work)
        update_primary_report_fields(
            session_branch_head_before_merge=session_head_before_merge,
        )
        start_subcommand_step(3, "session branch を merge", "merge session branch")
        update_primary_report_fields(
            branch_switch_status="started",
            merge_status="started",
        )
        # {{work-root}}/oracle/doc/app_spec/session_state.md:
        # session_home_branch は local branch なので、同名 remote-tracking branch を
        # Git に推測させて別の merge target を作らない。
        run_git(["switch", "--no-guess", home], work)
        update_primary_report_fields(branch_switch_status="completed")
        home_head_before_merge = head_commit(work)
        update_primary_report_fields(
            home_branch_head_before_merge=home_head_before_merge
        )
        merge = git(["merge", "--no-ff", branch], work, check=False)
        if merge.returncode != 0:
            resolve_session_join_conflict(
                work,
                session_head_before_merge,
                home_head_before_merge,
                codex_exec,
            )
        update_primary_report_fields(merge_status="completed")
        head_after_merge = head_commit(work)
        merge_commit = (
            head_after_merge if head_after_merge != home_head_before_merge else None
        )
        update_primary_report_fields(merge_commit=merge_commit)
        state.session.state = "joined"
        start_subcommand_step(
            4, "後始末と terminal result を確定", "finish session join"
        )
        update_primary_report_fields(state_update_status="started")
        write_state(path, state)
        update_primary_report_fields(
            session_state_after="joined",
            state_update_status="completed",
            session_branch_cleanup_status="started",
        )
        # {{work-root}}/oracle/doc/app_spec/sub_command/session_join.md:
        # 削除するのは local session branch 自体が merge target HEAD から到達可能な場合だけ。
        # remote-tracking ref で安全性を証明してはならない。
        reachable = (
            git(
                ["merge-base", "--is-ancestor", branch, "HEAD"],
                work,
                check=False,
            ).returncode
            == 0
        )
        if reachable:
            delete_result = git(["branch", "-d", branch], work, check=False)
        else:
            delete_result = CommandResult(
                1, "", f"session branch is not merged: {branch}"
            )
        warnings: list[str] = []
        if delete_result.returncode != 0:
            warnings.append(f"session branch was not deleted: {branch}")
            update_primary_report_fields(session_branch_cleanup_status="warning")
        else:
            update_primary_report_fields(session_branch_cleanup_status="completed")
        return TerminalResult(
            details=(
                ("session_id", session_id),
                ("joined_to", home),
                ("deleted_session_branch", delete_result.returncode == 0),
            ),
            warnings=tuple(warnings),
        )


def resolve_session_join_conflict(
    root: Path,
    session_head_commit: str,
    home_head_commit: str,
    codex_exec: _CodexExec,
) -> None:
    """両 HEAD を渡して内容解消を依頼し、管理物と merge commit を確定する。"""
    start_subcommand_step("3/4", "競合を統合", "resolve merge conflicts")
    update_primary_report_fields(
        conflict_paths=[str(root / path) for path in unmerged_paths(root)],
        conflict_resolution_status="started",
        conflict_resolution_result="not_confirmed",
    )
    resolution = resolve_merge_conflicts(
        root,
        build_session_join_conflict_resolution_parameter(
            session_head_commit,
            home_head_commit,
            root,
            document_search_scope=oracle_doc_scope(),
        ),
        codex_exec=codex_exec,
        purpose="session join conflict resolution",
    )
    update_primary_report_fields(
        conflict_paths=[str(root / path) for path in resolution["initial_conflicts"]],
        conflict_resolution_status=resolution["agent_status"],
        conflict_resolution_result="confirmed",
        conflict_agent_report=resolution["agent_report"],
        conflict_incidental_paths=resolution["incidental_paths"],
        conflict_call_log=resolution["call_log"],
    )
