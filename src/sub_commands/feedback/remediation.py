"""Feedback issue の逐次修復から自動 join、publication までを制御する。

根拠: {{work-root}}/oracle/doc/app_spec/sub_command/feedback_report.md。
観測の集約と表示は report、永続 artifact の検査は runtime_feedback_run_state に委譲する。
"""

import json
import signal
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import replace
from pathlib import Path
from typing import Any

from oracle.acp_builder.feedback.remediate_issue import (
    build_feedback_remediate_issue_parameter,
)

from cmoc_runtime import (
    CmocError,
    TerminalResult,
    current_branch,
    head_commit,
    load_state_for_branch,
    repo_root,
    require_clean_worktree,
    run_git,
    work_root,
    write_state,
)
from commons.indexing import run_indexing_preflight
from commons.runtime_feedback_intake import capture_high_watermark
from commons.runtime_feedback_run_state import (
    new_run_record,
    read_run_artifact,
    save_run_artifact,
    validate_remediation_checkpoint,
)
from commons.runtime_feedback_state import (
    ActiveState,
    artifact_reference,
    feedback_writer_lock,
    load_report_cut,
    new_generation_id,
    new_report_cut_id,
    remediation_checkpoint_path,
    validate_feedback_state,
    write_checkpoint,
    write_report_cut_manifest,
)
from commons.runtime_feedback_store import (
    canonical_json_bytes,
    rfc3339_now,
    sha256_bytes,
    write_immutable_json,
)
from commons.runtime_logging import current_subcommand_logger
from commons.runtime_primary_report import update_primary_report_fields
from commons.runtime_primary_report_render import execution_record_markdown
from commons.runtime_refactor import sync_refactor_state
from commons.runtime_results import StructuredOutputValidationIssue
from commons.runtime_run import (
    delete_run_process_id,
    run_lifecycle_lock,
    run_process_tracking,
    stop_tracked_codex_children,
)
from commons.runtime_run_lifecycle import (
    EditingRunContext,
    GitChange,
    commit_work_unit,
    recover_started_run,
    refresh_indexes,
    resolve_active_run,
    set_run_state,
    start_editing_run,
    tree_changes,
    unexpected_agent_paths,
    unexpected_run_paths,
    worktree_change_paths,
)
from sub_commands.run.join import (
    _doctor_preprocess_for_join,
    merge_run,
    validate_run_join,
)

from . import report


def run_feedback_report() -> TerminalResult:
    """事前条件を検査し、同一 run の join 後 recovery または新規修復を行う。"""
    from .recovery import finish_feedback_run, recover_finalization

    repository, session_worktree = repo_root(), work_root()
    context: EditingRunContext | None = None
    manifest: dict[str, Any] | None = None
    manifest_path: Path | None = None
    finalizing = False
    starting = False
    try:
        # doctor と必要な INDEX 更新を完了してから clean を判定する。
        _doctor_preprocess_for_join()
        feedback_directory = repository / ".cmoc/gu/ar/feedback"
        if (
            not (feedback_directory / "work").exists()
            and not (feedback_directory / "finalization.json").exists()
        ):
            run_indexing_preflight(repository, report.run_codex_exec)
        branch = current_branch(session_worktree)
        update_primary_report_fields(session_branch=branch)
        if not branch.startswith("cmoc/session/"):
            raise _failure(
                "feedback report は active session branch 上で実行してください。"
            )
        _, _, session = load_state_for_branch(repository, branch)
        if session.session.state != "active":
            raise _failure("feedback report の session は active ではありません。")
        require_clean_worktree(session_worktree)
        with feedback_writer_lock(repository):
            recovered = recover_finalization(repository, branch)
            if recovered is not None:
                return recovered
            state = validate_feedback_state(repository)
            existing = load_report_cut(repository)
            if existing is not None:
                manifest, manifest_path = existing
                candidate_context, _ = resolve_active_run({"error", "joinable"})
                _validate_context(candidate_context, manifest)
                if manifest["run"]["join_intent"] is None:
                    raise _failure(
                        "未 join の feedback run が残っています。",
                        [
                            "`cmoc run join` または `cmoc run abandon` で run を終了してください。"
                        ],
                    )
                # 同じ run の wave loop は再開しない。join 成功を証明できる場合だけ再開する。
                context = candidate_context
                finalizing = True
                with _indivisible_finalization():
                    _recover_join(context, manifest)
                    result = _publish(context, manifest, manifest_path, state)
                    return finish_feedback_run(context, manifest, result)
            if session.run.state != "ready":
                raise _failure(
                    "active editing run があるため feedback run を開始できません。",
                    ["既存 run を join または abandon してください。"],
                )
            starting = True
            context = start_editing_run("feedback_report")
            manifest = _new_manifest(context, state)
            manifest_path, _ = write_report_cut_manifest(repository, manifest)
            _update_progress(context, manifest, "running")
            with run_process_tracking(repository, context.session_id):
                candidates, aggregates = _wave_loop(context, manifest, state)
                stop_tracked_codex_children(repository, context.session_id)
            # 自動 join に必要な doctor の機械更新を seal 前に確定する。
            ignored = _doctor_preprocess_for_join()
            warnings: list[str] = []
            validate_run_join(context, warnings, session_ignored_paths=ignored)
            _seal(context, manifest, candidates, aggregates)
            set_run_state(context, "joinable")
            _update_progress(context, manifest, "joinable")
            with _indivisible_finalization():
                finalizing = True
                save_run_artifact(
                    repository,
                    manifest,
                    "join_intent",
                    {
                        "report_cut_id": manifest["report_cut_id"],
                        "sealed": manifest["run"]["sealed"],
                        "session_head_before": head_commit(context.session_worktree),
                        "run_head": head_commit(context.run_worktree),
                    },
                )
                with run_lifecycle_lock(repository, context.session_id):
                    _, _, current = load_state_for_branch(
                        repository, context.session_branch
                    )
                    validate_run_join(context, warnings, session_ignored_paths=ignored)
                    before = head_commit(context.session_worktree)

                    def merged(commit: str | None) -> None:
                        """post-join より先に merge 成功を durable に確定する。"""
                        assert context is not None
                        _record_merge(context, manifest, commit)

                    merge_run(context, current, warnings, before, on_merged=merged)
                    _complete_join(context, manifest)
                result = _publish(context, manifest, manifest_path, state)
                return finish_feedback_run(context, manifest, result)
    except KeyboardInterrupt:
        if context is None and starting:
            context = recover_started_run("feedback_report")
        if finalizing:
            if context is not None:
                _set_error(context)
            raise _failure(
                "feedback の自動 join または publication が中断されました。"
            ) from None
        if context is not None:
            stop_tracked_codex_children(repository, context.session_id)
            set_run_state(context, "joinable")
            if manifest is not None:
                report._set_processing_state(repository, manifest, "interrupted", None)
                _update_progress(context, manifest, "joinable")
        return report._record_feedback_interruption(manifest, manifest_path)
    except BaseException as exc:
        if context is None and starting:
            context = recover_started_run("feedback_report")
        if context is not None:
            _set_error(context)
            if manifest is not None:
                _update_progress(context, manifest, "error")
        logger = current_subcommand_logger()
        if logger is not None:
            logger.event(
                "feedback_remediation_failed", error=repr(exc), finalizing=finalizing
            )
        raise


def _new_manifest(context: EditingRunContext, state: ActiveState) -> dict[str, Any]:
    """可変な run 進行記録を作り、report cut は wave 終了後まで作らない。"""
    return {
        "schema_version": 1,
        "report_cut_id": new_report_cut_id(),
        "cut_at": rfc3339_now(),
        "inputs": {
            "observations": [],
            "current": report._active_state_input(context.repo, state),
            "references": [],
            "versions": report._processing_versions(),
        },
        "processing": {
            "status": "ready",
            "normalization_checkpoints": [],
            "remediation_checkpoints": [],
            "failure": None,
        },
        "publication": None,
        "diagnostic": None,
        "run": new_run_record(context),
    }


def _wave_loop(
    context: EditingRunContext, manifest: dict[str, Any], state: ActiveState
) -> tuple[dict[str, Any], dict[str, Any]]:
    """保存順境界内の新規 identity がなくなるまで immutable wave を逐次処理する。"""
    candidates: dict[str, Any] | None = None
    aggregates: dict[str, Any] | None = None
    processed: set[str] = set()
    while True:
        after = manifest["run"]["high_watermark"]
        # 未定義 artifact と invalid input を publication 前に拒否する。
        report._pending_observations(context.repo)
        watermark, entries = capture_high_watermark(context.repo, after)
        inputs = manifest["inputs"]
        delta = {**manifest, "inputs": {**inputs, "observations": entries}}
        observations = report._read_cut_observations(context.repo, delta)
        captured_at = rfc3339_now()
        references = report._capture_report_cut_references(
            context.repo,
            observations,
            state.issues if candidates is None else {},
        )
        intake_number = len(manifest["run"]["waves"]) + 1
        for reference in references:
            reference["reference_id"] += f":intake{intake_number}"
        inputs["observations"] = sorted(
            [*inputs["observations"], *entries],
            key=lambda item: (item["observation_id"], item["path"]),
        )
        inputs["references"] = sorted(
            [*inputs["references"], *references], key=lambda item: item["reference_id"]
        )
        manifest["run"]["high_watermark"] = watermark
        write_report_cut_manifest(context.repo, manifest)
        candidates, aggregates = report._build_candidates(
            context.repo,
            context.run_worktree,
            manifest,
            observations,
            state,
            previous_candidates=candidates,
            previous_aggregates=aggregates,
            observed_at=captured_at,
        )
        pending = {
            identity: candidate
            for identity, candidate in sorted(candidates.items())
            if identity not in processed
        }
        if manifest["run"]["waves"] and not pending:
            return candidates, aggregates
        sequence = len(manifest["run"]["waves"]) + 1
        wave = {
            "sequence": sequence,
            "after": after,
            "high_watermark": watermark,
            "inputs": {
                "observations": entries,
                "current": inputs["current"] if sequence == 1 else None,
                "versions": inputs["versions"],
                "captured_at": captured_at,
                "reporter_compatibility": "v1-raw-to-v2-view",
            },
            "candidates": pending,
        }
        wave_path = (
            context.repo
            / ".cmoc/gu/ar/feedback/work"
            / manifest["report_cut_id"]
            / "wave"
            / str(sequence)
            / "input.json"
        )
        write_immutable_json(wave_path, wave)
        wave_reference = artifact_reference(context.repo, wave_path)
        manifest["run"]["waves"].append(wave_reference)
        write_report_cut_manifest(context.repo, manifest)
        for identity, candidate in pending.items():
            _remediate_issue(context, manifest, wave_reference, candidate)
            processed.add(identity)
        # run_codex_exec は各 call の reporter を close/drain してから戻る。
        # 次の capture は、全 call の終了後に collector と同じ lock を取得する。
        _update_progress(context, manifest, "running")


def _remediation_output_issues(
    output: Any,
    changed_paths: frozenset[str],
    identity: str,
) -> tuple[StructuredOutputValidationIssue, ...]:
    """issue ID、正規化 path 集合と検証記録を実差分へ照合する。"""
    if not isinstance(output, dict) or not isinstance(output.get("result"), dict):
        return ()  # schema validator が構造違反を扱う。
    result = output["result"]
    issues: list[StructuredOutputValidationIssue] = []

    def mismatch(name: str, expected: object, actual: object) -> None:
        """決定論的な差を既存 Structured Output correction へ返す。"""
        issues.append(
            StructuredOutputValidationIssue(
                name, f"$.result.{name}", str(expected), str(actual)
            )
        )

    if result.get("issue_id") != identity:
        mismatch("issue_id", identity, result.get("issue_id"))
    paths = result.get("changed_paths")
    if not isinstance(paths, list) or any(not isinstance(path, str) for path in paths):
        return tuple(issues)
    if len(paths) != len(set(paths)) or set(paths) != set(changed_paths):
        mismatch("changed_paths", sorted(changed_paths), paths)
    for path in paths:
        if (
            not path
            or Path(path).is_absolute()
            or ".." in Path(path).parts
            or Path(path).as_posix() != path
            or path == "."
        ):
            mismatch("changed_paths", "normalized work-root relative paths", path)
    status = result.get("status")
    if status == "fixed" and not changed_paths:
        mismatch("status", "fixed requires an actual change", status)
    if (
        status in {"already_resolved", "not_actionable", "inconclusive"}
        and changed_paths
    ):
        mismatch("changed_paths", [], sorted(changed_paths))
    if changed_paths:
        verification = result.get("verification")
        if (
            not isinstance(verification, list)
            or not verification
            or any(
                not isinstance(item, dict) or item.get("status") != "passed"
                for item in verification
            )
        ):
            mismatch(
                "verification", "successful post-change verification", verification
            )
    for field in ("reason", "human_action"):
        value = result.get(field)
        if isinstance(value, str) and not value.strip():
            mismatch(field, "non-whitespace text", value)
    for field, names in (
        ("verification", ("method", "summary")),
        ("current_evidence", ("path", "location", "finding")),
    ):
        for item in result.get(field, []):
            if isinstance(item, dict) and any(
                isinstance(item.get(name), str) and not item[name].strip()
                for name in names
            ):
                mismatch(field, "concrete non-whitespace records", item)
    return tuple(issues)


def _remediate_issue(
    context: EditingRunContext,
    manifest: dict[str, Any],
    wave: dict[str, Any],
    candidate: dict[str, Any],
) -> None:
    """issue 1 件を commit と正式 checkpoint まで確定し、未確定単位を rollback する。"""
    identity = candidate["candidate_id"]
    before = head_commit(context.run_worktree)
    require_clean_worktree(context.run_worktree)
    payload = report._remediation_candidate_payload(candidate)
    payload["issue_id"] = payload.pop("candidate_id")
    parameter = build_feedback_remediate_issue_parameter(
        json.dumps(payload, ensure_ascii=False, sort_keys=True), context.run_worktree
    )
    schema = parameter.structured_output_schema_path
    assert schema is not None
    checkpoint_saved = False
    try:

        def postcondition(
            output: Any, changed: frozenset[str]
        ) -> tuple[StructuredOutputValidationIssue, ...]:
            """runtime が算出した論理 call の net 差分を照合する。"""
            return _remediation_output_issues(output, changed, identity)

        result = report.run_codex_exec(
            parameter,
            root=context.repo,
            purpose=f"feedback issue remediation ({identity})",
            structured_output_postcondition=postcondition,
        )
        stop_tracked_codex_children(context.repo, context.session_id)
        if result.returncode != 0 or head_commit(context.run_worktree) != before:
            raise _failure("feedback remediation call の終了または HEAD が不正です。")
        if (
            run_git(
                ["diff", "--cached", "--quiet"], context.run_worktree, check=False
            ).returncode
            != 0
        ):
            raise _failure("feedback remediation agent が Git index を変更しました。")
        actual = worktree_change_paths(
            context.run_worktree, include_rename_sources=True
        )
        unexpected = unexpected_agent_paths(
            replace(context, run_fork_commit=before), actual
        )
        if unexpected:
            raise _failure(
                "feedback remediation が realization file 以外を変更しました。",
                detail="\n".join(unexpected),
            )
        if not report._structured_output_matches_schema(
            result.output_json, schema
        ) or _remediation_output_issues(
            result.output_json, frozenset(actual), identity
        ):
            raise _failure(
                "feedback remediation output と実差分または verification が一致しません。"
            )
        if actual:
            sync_refactor_state(context.run_worktree)
            refresh_indexes(context.run_worktree, commit=False)
            stop_tracked_codex_children(context.repo, context.session_id)
        all_paths = worktree_change_paths(
            context.run_worktree, include_rename_sources=True
        )
        if head_commit(context.run_worktree) != before or unexpected_run_paths(
            context, [GitChange("M", (path,)) for path in all_paths]
        ):
            raise _failure("feedback issue 処理単位に想定外差分があります。")
        commit = commit_work_unit(
            context.run_worktree, f"cmoc feedback remediation {identity}"
        )
        after = head_commit(context.run_worktree)
        require_clean_worktree(context.run_worktree)
        input_value = {"issue": payload, "wave": wave, "before_commit": before}
        call_log = result.call_log_path
        checkpoint = {
            "schema_version": 1,
            "kind": "remediation",
            "report_cut_id": manifest["report_cut_id"],
            "candidate_id": identity,
            "input": input_value,
            "input_sha256": sha256_bytes(canonical_json_bytes(input_value)),
            "builder_sha256": manifest["inputs"]["versions"]["remediation_builder"],
            "schema_sha256": sha256_bytes(schema.read_bytes()),
            "structured_output": result.output_json,
            "output_sha256": sha256_bytes(canonical_json_bytes(result.output_json)),
            "audit": {
                "wave": wave,
                "before_commit": before,
                "after_commit": after,
                "commit": commit,
                "changed_paths": actual,
                "diff_sha256": _diff_hash(context.run_worktree, before, after),
                "call_log": artifact_reference(context.repo, call_log),
                "mechanical_checks": {
                    "changed_paths": True,
                    "allowed_paths": True,
                    "verification": True,
                },
            },
        }
        path = remediation_checkpoint_path(
            context.repo, manifest["report_cut_id"], identity
        )
        validate_remediation_checkpoint(checkpoint, path)
        reference = write_checkpoint(context.repo, path, checkpoint)
        checkpoint_saved = True
        logger = current_subcommand_logger()
        if logger is not None:
            logger.event(
                "feedback_issue_committed",
                issue_id=identity,
                result=result.output_json["result"],
                audit=checkpoint["audit"],
            )
        report._record_checkpoint(
            context.repo,
            manifest,
            "remediation_checkpoints",
            "candidate_id",
            identity,
            reference,
        )
    except BaseException:
        if not checkpoint_saved:
            stop_tracked_codex_children(context.repo, context.session_id)
            run_git(["reset", "--hard", before], context.run_worktree)
            run_git(["clean", "-fd"], context.run_worktree)
            require_clean_worktree(context.run_worktree)
            update_primary_report_fields(
                rollback={"issue_id": identity, "commit": before}
            )
        raise


def _diff_hash(worktree: Path, before: str, after: str) -> str:
    """commit 間の binary を含む net 差分を監査用 hash にする。"""
    return sha256_bytes(
        run_git(
            ["diff", "--binary", "--no-ext-diff", before, after], worktree
        ).stdout.encode("utf-8")
    )


def _seal(
    context: EditingRunContext,
    manifest: dict[str, Any],
    candidates: dict[str, Any],
    aggregates: dict[str, Any],
) -> None:
    """wave loop の自然完了後に publication 入力と merge 対象を一度だけ封印する。"""
    manifest["run"]["targets"] = {
        "generated_at": rfc3339_now(),
        "generation_id": new_generation_id(),
        "report": report._new_report_path(context.repo)
        .relative_to(context.repo)
        .as_posix(),
        "incomplete_report": report._new_report_path(context.repo, incomplete=True)
        .relative_to(context.repo)
        .as_posix(),
    }
    save_run_artifact(
        context.repo,
        manifest,
        "sealed",
        {
            "report_cut_id": manifest["report_cut_id"],
            "inputs": manifest["inputs"],
            "waves": manifest["run"]["waves"],
            "high_watermark": manifest["run"]["high_watermark"],
            "targets": manifest["run"]["targets"],
            "checkpoints": manifest["processing"]["remediation_checkpoints"],
            "candidates": candidates,
            "machine_aggregates": aggregates,
            "run_head": head_commit(context.run_worktree),
            "session_head_before": head_commit(context.session_worktree),
        },
    )


def _record_merge(
    context: EditingRunContext, manifest: dict[str, Any], commit: str | None
) -> None:
    """merge/no-op 成功を seal と結び付け、publication failure で巻き戻さない。"""
    save_run_artifact(
        context.repo,
        manifest,
        "merged",
        {
            "report_cut_id": manifest["report_cut_id"],
            "sealed": manifest["run"]["sealed"],
            "run_join_commit": commit,
            "session_commit": head_commit(context.session_worktree),
        },
    )


def _complete_join(context: EditingRunContext, manifest: dict[str, Any]) -> None:
    """最終 session tree に対する commit 到達可能性と path/hash を確認する。"""
    seal = read_run_artifact(context.repo, manifest["run"]["sealed"])
    require_clean_worktree(context.run_worktree)
    require_clean_worktree(context.session_worktree)
    if head_commit(context.run_worktree) != seal["run_head"] or not _is_ancestor(
        context, seal["run_head"]
    ):
        raise _failure("feedback run HEAD が join 後 session tree から到達できません。")
    paths: set[str] = set()
    for reference in manifest["processing"]["remediation_checkpoints"]:
        checkpoint = read_run_artifact(
            context.repo, {key: reference[key] for key in ("path", "sha256")}
        )
        validate_remediation_checkpoint(checkpoint, context.repo / reference["path"])
        audit = checkpoint["audit"]
        if audit["wave"] not in manifest["run"]["waves"]:
            raise _failure("feedback issue checkpoint の wave が一致しません。")
        call_log = audit["call_log"]
        if not isinstance(call_log, dict) or not isinstance(call_log.get("path"), str):
            raise _failure("feedback issue の call log reference が不正です。")
        call_path = context.repo / call_log["path"]
        if (
            not call_path.resolve().is_relative_to(context.repo / ".cmoc/gu/ar/log")
            or artifact_reference(context.repo, call_path) != call_log
        ):
            raise _failure("feedback issue の call log hash が一致しません。")
        if (
            not _is_ancestor(context, audit["after_commit"])
            or _diff_hash(
                context.session_worktree, audit["before_commit"], audit["after_commit"]
            )
            != audit["diff_sha256"]
        ):
            raise _failure(
                "feedback issue commit または net 差分 hash を確認できません。"
            )
        paths.update(audit["changed_paths"])
        result = checkpoint["structured_output"]["result"]
        if result["status"] == "human_required":
            evidence_paths = {item["path"] for item in result["current_evidence"]}
            changed_evidence = {
                path
                for change in tree_changes(
                    context.session_worktree, audit["after_commit"]
                )
                for path in change.paths
            }.intersection(evidence_paths)
            if changed_evidence:
                raise _failure(
                    "human_required の evidence が修復時から変更されています。",
                    detail="\n".join(sorted(changed_evidence)),
                )
            paths.update(evidence_paths)
    # 後続 issue が同じ path を編集できるため、最終 run tree と session tree を比較する。
    different = {
        path
        for change in tree_changes(context.session_worktree, seal["run_head"])
        for path in change.paths
    }
    if paths.intersection(different):
        raise _failure(
            "join 後の realization tree が正式な issue commit の最終 tree と一致しません。",
            detail="\n".join(sorted(paths.intersection(different))),
        )
    completion = {
        "report_cut_id": manifest["report_cut_id"],
        "sealed": manifest["run"]["sealed"],
        "session_commit": head_commit(context.session_worktree),
        "run_head": seal["run_head"],
        "checked_paths": sorted(paths),
        "checks": {"reachability": True, "paths": True, "clean": True},
    }
    if manifest["run"]["completion"] is None:
        save_run_artifact(context.repo, manifest, "completion", completion)
    elif read_run_artifact(context.repo, manifest["run"]["completion"]) != completion:
        raise _failure("feedback join の確定済み検査結果と現在 tree が一致しません。")
    if manifest["run"]["execution_record"] is None:
        logger = current_subcommand_logger()
        original_log = context.repo / manifest["run"]["invocation_log"]
        saved_events = (
            tuple(json.loads(line) for line in original_log.read_text().splitlines())
            if logger is None or original_log != logger.path
            else ()
        )
        manifest["run"]["execution_record"] = execution_record_markdown(
            logger,
            saved_events=saved_events,
        )
        write_report_cut_manifest(context.repo, manifest)


def _is_ancestor(context: EditingRunContext, commit: str) -> bool:
    """commit の session branch からの到達可能性を Git で検査する。"""
    return (
        run_git(
            ["merge-base", "--is-ancestor", commit, context.session_branch],
            context.repo,
            check=False,
        ).returncode
        == 0
    )


def _recover_join(context: EditingRunContext, manifest: dict[str, Any]) -> None:
    """封印済み run の join 成功だけを回復し、新しい call を開始しない。"""
    seal = read_run_artifact(context.repo, manifest["run"]["sealed"])
    if manifest["run"]["merged"] is None:
        head = head_commit(context.session_worktree)
        parents = (
            run_git(["show", "-s", "--format=%P", head], context.repo)
            .stdout.strip()
            .split()
        )
        if head == seal["session_head_before"] and _is_ancestor(
            context, seal["run_head"]
        ):
            _record_merge(context, manifest, None)
        elif parents == [seal["session_head_before"], seal["run_head"]]:
            _record_merge(context, manifest, head)
        else:
            raise _failure(
                "feedback run の自動 join 成功を一意に確認できません。",
                [
                    "未 join の run は `cmoc run join` または `cmoc run abandon` で終了してください。"
                ],
            )
    merged = read_run_artifact(context.repo, manifest["run"]["merged"])
    if not _is_ancestor(context, merged["session_commit"]):
        raise _failure(
            "feedback run の join commit が session tree から到達できません。"
        )
    if manifest["run"]["completion"] is not None:
        completion = read_run_artifact(context.repo, manifest["run"]["completion"])
        if head_commit(context.session_worktree) != completion["session_commit"]:
            raise _failure(
                "feedback publication recovery の session tree が変更されています。"
            )
    else:
        # merge 後、機械的 state 同期だけが未完了の場合は Codex を使わず再実行する。
        require_clean_worktree(context.session_worktree)
        sync_refactor_state(context.session_worktree)
        commit_work_unit(
            context.session_worktree, "cmoc refactor state sync after feedback join"
        )
    _complete_join(context, manifest)


def _publish(
    context: EditingRunContext,
    manifest: dict[str, Any],
    manifest_path: Path,
    state: ActiveState,
) -> TerminalResult:
    """join 後の封印済み候補と正式 checkpoint だけを publication に渡す。"""
    seal = read_run_artifact(context.repo, manifest["run"]["sealed"])
    verdicts = {}
    for reference in manifest["processing"]["remediation_checkpoints"]:
        checkpoint = read_run_artifact(
            context.repo, {key: reference[key] for key in ("path", "sha256")}
        )
        verdicts[reference["candidate_id"]] = checkpoint["structured_output"]["result"]
    if set(verdicts) != set(seal["candidates"]):
        raise _failure("feedback report cut に未処理の issue があります。")
    if manifest["processing"]["status"] == "publication_ready":
        return report._resume_publication(context.repo, manifest, manifest_path)
    if any(value["status"] == "inconclusive" for value in verdicts.values()):
        return report._publish_incomplete_report(
            context.repo,
            context.session_worktree,
            manifest,
            manifest_path,
            seal["candidates"],
            verdicts,
        )
    return report._publish_report(
        context.repo,
        context.session_worktree,
        manifest,
        manifest_path,
        seal["candidates"],
        seal["machine_aggregates"],
        verdicts,
        state,
    )


def _validate_context(context: EditingRunContext, manifest: dict[str, Any]) -> None:
    """別 run の成果物を recovery へ流用しない。"""
    identity = manifest["run"]["identity"]
    expected = new_run_record(context)["identity"]
    if any(
        identity[key] != value
        for key, value in expected.items()
        if key != "state_before"
    ):
        raise _failure("feedback manifest と active run identity が一致しません。")


def _set_error(context: EditingRunContext) -> None:
    """同一 active run だけを error にし、確定済み merge と資源を保持する。"""
    with run_lifecycle_lock(context.repo, context.session_id):
        _, _, state = load_state_for_branch(context.repo, context.session_branch)
        if state.run.branch == context.run_branch:
            state.run.state = "error"
            write_state(context.state_path, state)
            delete_run_process_id(context.repo, context.session_id)


def _update_progress(
    context: EditingRunContext, manifest: dict[str, Any], state: str
) -> None:
    """中断・エラー時に必要な確定情報を invocation report に残す。"""
    report._update_feedback_progress_fields(manifest)
    logger = current_subcommand_logger()
    committed = [
        {"issue_id": event["issue_id"], "commit": event["audit"]["commit"]}
        for event in (logger.event_records() if logger else ())
        if event.get("event") == "feedback_issue_committed"
    ]
    update_primary_report_fields(
        report_cut_id=manifest["report_cut_id"],
        report_cut_at=manifest["cut_at"],
        run_kind=context.kind,
        run_branch=context.run_branch,
        run_fork_commit=context.run_fork_commit,
        run_worktree=context.run_worktree,
        state_before=context.state_before,
        state_after=state,
        confirmed_issue_commits=committed,
        wave_count=len(manifest["run"]["waves"]),
        final_high_watermark=manifest["run"]["high_watermark"],
        processed_issues=[
            item["candidate_id"]
            for item in manifest["processing"]["remediation_checkpoints"]
        ],
    )


@contextmanager
def _indivisible_finalization() -> Iterator[None]:
    """SIGINT を finalization 中だけ保留し、merge と publication を整合した境界まで進める。"""
    previous = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, lambda _signum, _frame: None)
    try:
        yield
    finally:
        signal.signal(signal.SIGINT, previous)


def _failure(
    summary: str, next_actions: list[str] | tuple[str, ...] = (), detail: str = ""
) -> CmocError:
    """feedback failure の共通回復案と具体情報を既存エラー型に載せる。"""
    return CmocError(
        summary,
        list(next_actions) or ["invocation report と run state を確認してください。"],
        detail,
    )
