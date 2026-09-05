"""Feedback publication 後の cleanup と明示 join/abandon の境界を扱う。

根拠: {{work-root}}/oracle/doc/app_spec/feedback_state.md の
「正常 report の atomic publication」と「run lifecycle との整合」。
"""

from pathlib import Path
from typing import Any

from cmoc_runtime import (
    RunPart,
    TerminalResult,
    branch_exists,
    head_commit,
    load_state_for_branch,
    require_clean_worktree,
    run_git,
    write_state,
)
from commons.runtime_feedback_run_state import new_run_record, read_run_artifact
from commons.runtime_feedback_state import (
    _durable_unlink,
    _read_canonical_object,
    _require_exact_fields,
    artifact_reference,
    cleanup_published_report,
    discard_report_cut,
    feedback_writer_lock,
    load_active_state,
    load_report_cut,
    recover_report_cut_checkpoint_references,
    validate_feedback_state,
)
from commons.runtime_feedback_store import feedback_root, write_immutable_json
from commons.runtime_logging import current_subcommand_logger
from commons.runtime_primary_report import update_primary_report_fields
from commons.runtime_run import (
    delete_run_process_id,
    expected_run_worktree,
    run_lifecycle_lock,
    worktree_for_branch,
)
from commons.runtime_run_lifecycle import EditingRunContext
from sub_commands.run.join import _cleanup_joined_run


def finish_feedback_run(
    context: EditingRunContext, manifest: dict[str, Any], result: TerminalResult
) -> TerminalResult:
    """work artifact を削除する前に最小の recovery journal を durable 保存する。"""
    from .remediation import _failure

    if result.primary_report is None:
        raise _failure("feedback finalization に durable report がありません。")
    completion = read_run_artifact(context.repo, manifest["run"]["completion"])
    merged = read_run_artifact(context.repo, manifest["run"]["merged"])
    path = feedback_root(context.repo) / "finalization.json"
    journal = {
        "schema_version": 1,
        "identity": manifest["run"]["identity"],
        "report_cut_id": manifest["report_cut_id"],
        "report": artifact_reference(context.repo, result.primary_report),
        "current": load_active_state(context.repo).current,
        "completion": completion,
        "merged": merged,
        "result": result.result,
    }
    write_immutable_json(path, journal)
    return _finish_from_journal(context.repo, journal, path)


def recover_finalization(repo: Path, session_branch: str) -> TerminalResult | None:
    """publication 後の cleanup を同じ報告書と join tree から再開する。"""
    path = feedback_root(repo) / "finalization.json"
    if not path.exists() and not path.is_symlink():
        return None
    journal = _read_canonical_object(path, "feedback finalization journal")
    context = _journal_context(repo, journal)
    if context.session_branch != session_branch:
        from .remediation import _failure

        raise _failure(
            "別 session の feedback finalization が未完了です。",
            [
                f"{context.session_branch} で `cmoc feedback report` を実行してください。"
            ],
        )
    from .remediation import _indivisible_finalization

    with _indivisible_finalization():
        return _finish_from_journal(repo, journal, path)


def _journal_context(repo: Path, journal: dict[str, Any]) -> EditingRunContext:
    """journal の保存先を active session と managed run の正規 path へ照合する。"""
    from .remediation import _failure

    path = feedback_root(repo) / "finalization.json"
    _require_exact_fields(
        journal,
        {
            "schema_version",
            "identity",
            "report_cut_id",
            "report",
            "current",
            "completion",
            "merged",
            "result",
        },
        path,
        "feedback finalization journal",
    )
    if (
        type(journal["schema_version"]) is not int
        or journal["schema_version"] != 1
        or journal["result"] not in {"ok", "attention", "incomplete"}
    ):
        raise _failure("feedback finalization journal の version/result が不正です。")
    identity = _require_exact_fields(
        journal["identity"],
        set(EditingRunContext.__dataclass_fields__),
        path,
        "feedback run identity",
    )
    converted = dict(identity)
    for field in ("repo", "session_worktree", "state_path", "run_worktree"):
        if not isinstance(identity[field], str):
            raise _failure("feedback finalization identity の path が不正です。")
        converted[field] = Path(identity[field])
    context = EditingRunContext(**converted)
    session_id, state_path, session = load_state_for_branch(
        repo, context.session_branch
    )
    if (
        context.repo != repo.resolve()
        or context.kind != "feedback_report"
        or context.session_id != session_id
        or context.state_path != state_path
        or context.run_worktree != expected_run_worktree(repo, context.run_branch)
        or context.session_worktree != worktree_for_branch(repo, context.session_branch)
        or session.session.state != "active"
        or session.session.session_fork_commit != context.session_fork_commit
    ):
        raise _failure(
            "feedback finalization journal と session identity が一致しません。"
        )
    if session.run.state != "ready" and (
        session.run.branch != context.run_branch
        or session.run.kind != context.kind
        or session.run.fork_commit != context.run_fork_commit
    ):
        raise _failure("feedback finalization の対象とは異なる active run があります。")
    return context


def _finish_from_journal(
    repo: Path, journal: dict[str, Any], path: Path
) -> TerminalResult:
    """raw/work cleanup、ready 遷移、隔離資源回収を idempotent に確定する。"""
    from .remediation import _failure

    context = _journal_context(repo, journal)
    report_reference = journal["report"]
    report_path = repo / report_reference["path"]
    if (
        not report_path.resolve().is_relative_to(repo / ".cmoc/gu/ar/report/feedback")
        or artifact_reference(repo, report_path) != report_reference
    ):
        raise _failure("feedback finalization report の path/hash が不正です。")
    completion = journal["completion"]
    if (
        completion.get("report_cut_id") != journal["report_cut_id"]
        or completion.get("checks")
        != {"reachability": True, "paths": True, "clean": True}
        or journal["merged"].get("sealed") != completion.get("sealed")
    ):
        raise _failure("feedback finalization の join evidence が不正です。")
    with run_lifecycle_lock(repo, context.session_id):
        try:
            require_clean_worktree(context.session_worktree)
            if head_commit(context.session_worktree) != completion["session_commit"]:
                raise _failure(
                    "feedback finalization の session tree が変更されています。"
                )
            if (
                run_git(
                    [
                        "merge-base",
                        "--is-ancestor",
                        completion["run_head"],
                        context.session_branch,
                    ],
                    repo,
                    check=False,
                ).returncode
                != 0
            ):
                raise _failure("feedback finalization の run commit が到達不能です。")
            if load_active_state(repo).current != journal["current"]:
                raise _failure(
                    "feedback finalization 中に current pointer が変更されました。"
                )
            if context.run_worktree.exists():
                require_clean_worktree(context.run_worktree)
                if head_commit(context.run_worktree) != completion["run_head"]:
                    raise _failure(
                        "feedback finalization の run tree が変更されています。"
                    )
            state = validate_feedback_state(repo)
            work = load_report_cut(repo)
            if work is not None:
                manifest, manifest_path = work
                if (
                    manifest["report_cut_id"] != journal["report_cut_id"]
                    or manifest["run"]["identity"] != journal["identity"]
                ):
                    raise _failure(
                        "feedback finalization の cleanup 対象が一致しません。"
                    )
                if journal["result"] == "incomplete":
                    if (
                        manifest["processing"]["status"] != "incomplete"
                        or manifest["diagnostic"]["report"] != report_reference
                    ):
                        raise _failure(
                            "feedback incomplete report の確定状態が不正です。"
                        )
                    discard_report_cut(repo, manifest, manifest_path)
                else:
                    if (
                        state.current is None
                        or state.current["report_cut_id"] != journal["report_cut_id"]
                    ):
                        raise _failure("feedback publication point を確認できません。")
                    cleanup_published_report(repo)
            # work artifact の cleanup が完了してから state と隔離資源を回収する。
            _, _, session = load_state_for_branch(repo, context.session_branch)
            session.run = RunPart()
            write_state(context.state_path, session)
            warnings: list[str] = []
            if branch_exists(repo, context.run_branch):
                cleanup = _cleanup_joined_run(context, warnings)
                if cleanup != "completed":
                    raise _failure(
                        "feedback run の隔離資源 cleanup に失敗しました。",
                        detail="\n".join(warnings),
                    )
            elif context.run_worktree.exists() or context.run_worktree.is_symlink():
                raise _failure(
                    "feedback run branch がない状態で worktree が残っています。"
                )
            delete_run_process_id(repo, context.session_id)
            _durable_unlink(path)
        except BaseException:
            _, _, session = load_state_for_branch(repo, context.session_branch)
            session.run = RunPart(
                state="error",
                kind=context.kind,
                branch=context.run_branch,
                fork_commit=context.run_fork_commit,
            )
            write_state(context.state_path, session)
            raise
    update_primary_report_fields(
        state_after="ready",
        cleanup="completed",
        run_join_commit=journal["merged"]["run_join_commit"],
    )
    return TerminalResult(
        primary_report=report_path,
        primary_report_role="incomplete feedback diagnostic report"
        if journal["result"] == "incomplete"
        else "feedback report",
        result=journal["result"],
        details=(
            ("run_kind", "feedback_report"),
            ("run_join_commit", journal["merged"]["run_join_commit"]),
            ("cleanup", "completed"),
        ),
    )


def require_manual_feedback_run(context: EditingRunContext) -> None:
    """自動 join 済み feedback run を明示 join/abandon で破棄させない。"""
    from .remediation import _failure, _is_ancestor, _validate_context

    if context.kind != "feedback_report":
        return
    if (feedback_root(context.repo) / "finalization.json").exists():
        raise _failure(
            "feedback run は自動 join 済みです。",
            [
                "`cmoc feedback report` で publication または cleanup を再開してください。"
            ],
        )
    work = load_report_cut(context.repo)
    if work is None:
        return
    manifest, _ = work
    _validate_context(context, manifest)
    run = manifest["run"]
    joined = run["merged"] is not None
    if not joined and run["join_intent"] is not None:
        intent = read_run_artifact(context.repo, run["join_intent"])
        joined = _is_ancestor(context, intent["run_head"])
    if joined:
        raise _failure(
            "feedback run は自動 join 済みです。",
            [
                "`cmoc feedback report` で publication または cleanup を再開してください。"
            ],
        )


def finish_manual_feedback_run(context: EditingRunContext, operation: str) -> None:
    """明示終了した run の結果を監査記録へ移し、raw/current を維持して work を除く。"""
    if context.kind != "feedback_report":
        return
    with feedback_writer_lock(context.repo):
        work = load_report_cut(context.repo)
        if work is None:
            return
        manifest, path = work
        from .remediation import _validate_context

        _validate_context(context, manifest)
        recover_report_cut_checkpoint_references(context.repo, manifest, path)
        logger = current_subcommand_logger()
        if logger is not None:
            logger.event(
                "feedback_run_manual_completion",
                operation=operation,
                run_identity=new_run_record(context)["identity"],
                session_commit=head_commit(context.session_worktree),
                publication=False,
                checkpoints=[
                    read_run_artifact(
                        context.repo,
                        {key: reference[key] for key in ("path", "sha256")},
                    )
                    for reference in manifest["processing"]["remediation_checkpoints"]
                ],
            )
        discard_report_cut(context.repo, manifest, path)
