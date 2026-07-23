"""`cmoc realization refactor fork` の full-cycle workload。

この file は 16,000 文字を超えるが、target 選択、処理単位の確定、current fork
だけの unresolved 管理、完了判定、および report は同じ進捗状態を共有する。
分割すると、この一時状態と完了不変条件を複数 file 間で受け渡す必要があるため、
単一 workload の lifecycle として保つ。
"""

from pathlib import Path

import typer

from acp.builder.realization.refactor.fork.change_summary import (
    build_realization_refactor_fork_change_summary_parameter,
)
from acp.builder.realization.refactor.fork.file_review_and_fix import (
    build_realization_refactor_fork_file_review_and_fix_parameter,
)
from cmoc_runtime import (
    CmocError,
    file_sha256,
    load_config,
    pushd,
    refactor_state_path,
    run_cli_subcommand,
    run_codex_exec,
    run_git,
    start_subcommand_step,
    timestamp,
)
from commons.indexing import enable_indexing_preflight
from commons.runtime_refactor import (
    RefactorState,
    load_refactor_state,
    mark_all_refactor_targets_required,
    select_refactor_target,
    sync_refactor_state,
    write_refactor_state,
)
from commons.runtime_run import run_process_tracking
from sub_commands.run.lifecycle import (
    EditingRunContext,
    GitChange,
    commit_work_unit,
    flattened_change_paths,
    refresh_indexes,
    resolve_active_run,
    rollback_work_unit,
    set_run_state,
    start_editing_run,
    tree_changes,
    unexpected_agent_paths,
    unexpected_run_paths,
    worktree_change_paths,
)
from sub_commands.run.report import write_fork_report

_UnresolvedFinding = tuple[str, str, Path]


def cmoc_realization_refactor_fork_impl() -> None:
    """CLI runtime を通して realization refactor fork を実行する。"""
    enable_indexing_preflight()
    run_cli_subcommand(
        _cmoc_realization_refactor_fork_body,
        command_name="realization refactor fork",
        command_argv=["cmoc", "realization", "refactor", "fork"],
        total_steps=6,
    )


def _cmoc_realization_refactor_fork_body() -> None:
    context: EditingRunContext | None = None
    units: list[tuple[str, int]] = []
    unresolved_findings: dict[str, list[_UnresolvedFinding]] = {}
    try:
        start_subcommand_step(2, "realization refactor run を作成", "create run")
        context = start_editing_run("realization_refactor")
        start_subcommand_step(3, "full refactor cycle を初期化", "initialize cycle")
        _initialize_cycle(context)
        start_subcommand_step(4, "file 単位の調査と修正を実行", "run refactor loop")
        with run_process_tracking(context.repo, context.session_id):
            while target := select_refactor_target(
                load_refactor_state(context.run_worktree), unresolved_findings
            ):
                unit_target, finding_count, unresolved = _run_refactor_unit(
                    context, target
                )
                units.append((unit_target, finding_count))
                if unresolved:
                    # {{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md
                    # commit 済みの対象だけを current fork 内で保留し、次の対象へ進む。
                    unresolved_findings[target] = unresolved
            reason = _completion_reason(context.run_worktree, unresolved_findings)
            summary = _completion_change_summary(context)
        start_subcommand_step(5, "run を joinable に更新", "publish joinable")
        set_run_state(context, "joinable")
        start_subcommand_step(6, "fork report を保存", "write fork report")
        report = _write_refactor_report(
            context,
            "joinable",
            reason,
            units,
            unresolved_findings,
            summary=summary,
        )
        typer.echo(_completion_log(reason, unresolved_findings, report))
    except KeyboardInterrupt:
        if context is None:
            context = _recover_started_run()
            if context is None:
                raise
        rollback_work_unit(context.run_worktree)
        set_run_state(context, "joinable")
        report = _write_refactor_report(
            context,
            "joinable",
            "user_interruption",
            units,
            unresolved_findings,
            summary=None,
        )
        typer.echo(_completion_log("user_interruption", unresolved_findings, report))
        return
    except BaseException as exc:
        if context is None:
            context = _recover_started_run()
            if context is None:
                raise
        cleanup_errors: list[str] = []
        try:
            rollback_work_unit(context.run_worktree)
        except BaseException as cleanup_error:
            cleanup_errors.append(f"rollback failed: {cleanup_error!r}")
        try:
            set_run_state(context, "error")
        except BaseException as state_error:
            cleanup_errors.append(f"state update failed: {state_error!r}")
        report = _write_refactor_report(
            context,
            "error",
            "error",
            units,
            unresolved_findings,
            summary=None,
            error=exc,
            cleanup_errors=cleanup_errors,
        )
        error = CmocError(
            "realization refactor fork は error state で停止しました。",
            [
                "確定済み成果物を取り込む場合は `cmoc run join` を実行してください。",
                "run 全体を破棄する場合は `cmoc run abandon` を実行してください。",
            ],
            f"report: {report}\nerror: {exc!r}",
        )
        setattr(
            error, "cmoc_stdout", _completion_log("error", unresolved_findings, report)
        )
        raise error from exc


def _recover_started_run() -> EditingRunContext | None:
    """start 後の context 代入前に公開された run を cleanup 対象として回収する。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md
    try:
        context, _state = resolve_active_run({"running", "error"})
    except CmocError:
        return None
    return context if context.kind == "realization_refactor" else None


def _initialize_cycle(context: EditingRunContext) -> None:
    state = sync_refactor_state(context.run_worktree)
    if not any(entry["investigation_required"] for entry in state.values()):
        mark_all_refactor_targets_required(state)
        write_refactor_state(context.run_worktree, state)
    refresh_indexes(context.run_worktree, commit=False)
    commit_work_unit(
        context.run_worktree,
        "cmoc realization refactor cycle",
        allow_empty=True,
    )


def _run_refactor_unit(
    context: EditingRunContext,
    target: str,
) -> tuple[str, int, list[_UnresolvedFinding]]:
    target_path = context.run_worktree / target
    if not (target_path.is_file() or target_path.is_symlink()):
        sync_refactor_state(context.run_worktree)
        commit_work_unit(
            context.run_worktree,
            f"cmoc realization refactor sync {target}",
        )
        return target, 0, []
    investigated_hash = file_sha256(target_path)
    with pushd(context.run_worktree):
        parameter = build_realization_refactor_fork_file_review_and_fix_parameter(
            target_path
        )
        result = run_codex_exec(
            parameter,
            root=context.repo,
            cwd=context.run_worktree,
            config=load_config(context.run_worktree),
            purpose=f"realization refactor: {target}",
        )
    if result.returncode != 0:
        raise CmocError(
            "refactor agent が正常終了しませんでした。",
            ["Codex call log を確認してください。"],
            f"target: {target}\nreturncode: {result.returncode}",
        )
    findings = _validated_findings(result.output_json, target)
    changed_realization = worktree_change_paths(
        context.run_worktree,
        include_rename_sources=True,
    )
    unexpected = unexpected_agent_paths(context, changed_realization)
    if unexpected:
        raise CmocError(
            "refactor agent が想定外 path を変更しました。",
            ["run report を確認し、run を join または abandon してください。"],
            "\n".join(unexpected),
        )
    if not findings and changed_realization:
        raise CmocError(
            "所見が空の refactor agent call に差分があります。",
            ["Codex call log と run worktree の差分を確認してください。"],
            "\n".join(changed_realization),
        )
    unresolved = [
        finding
        for finding in findings
        if finding.get("resolution", {}).get("status") == "unresolved"
    ]
    if findings and not changed_realization and not unresolved:
        raise CmocError(
            "fixed 所見に対応する realization 差分がありません。",
            ["Codex call log と Structured Output を確認してください。"],
            f"target: {target}",
        )
    _update_refactor_state(
        context,
        target,
        investigated_hash,
        bool(findings),
        changed_realization,
    )
    refresh_indexes(context.run_worktree, commit=False)
    all_unit_paths = worktree_change_paths(
        context.run_worktree,
        include_rename_sources=True,
    )
    unexpected = unexpected_run_paths(
        context,
        # {{work-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md
        # status と tree diff の分類は path 単位で同じなので一時 change として扱う。
        [_status_change(path) for path in all_unit_paths],
    )
    if unexpected:
        raise CmocError(
            "refactor 処理単位に想定外差分があります。",
            ["run worktree の差分を確認してください。"],
            "\n".join(unexpected),
        )
    commit_work_unit(
        context.run_worktree,
        f"cmoc realization refactor {target}",
    )
    unresolved_details = [
        (
            str(finding.get("title", "")),
            str(finding.get("resolution", {}).get("summary", "")),
            result.call_log_path.resolve(),
        )
        for finding in unresolved
    ]
    return target, len(findings), unresolved_details


def _status_change(path: str) -> GitChange:
    """未 commit path を共通の差分分類へ渡す最小 GitChange にする。"""
    return GitChange("M", (path,))


def _update_refactor_state(
    context: EditingRunContext,
    target: str,
    investigated_hash: str,
    has_findings: bool,
    changed_realization: list[str],
) -> None:
    state = load_refactor_state(context.run_worktree)
    entry = state.get(target)
    if entry is None:
        raise CmocError(
            "refactor target の state entry がありません。",
            ["refactor state を同期してから新しい run を開始してください。"],
            target,
        )
    entry["last_investigated_sha256"] = investigated_hash
    entry["last_investigated_at"] = timestamp()
    entry["last_investigation_result"] = "findings" if has_findings else "no_findings"
    entry["investigation_required"] = has_findings
    write_refactor_state(context.run_worktree, state)
    state = sync_refactor_state(context.run_worktree)
    for changed in changed_realization:
        if changed in state:
            state[changed]["investigation_required"] = True
    write_refactor_state(context.run_worktree, state)


def _validated_findings(output: object, target: str) -> list[dict]:
    if not isinstance(output, dict) or set(output) != {"findings"}:
        raise CmocError(
            "refactor agent の Structured Output が不正です。",
            ["Codex call log と output schema を確認してください。"],
            f"target: {target}\noutput: {output!r}",
        )
    findings = output["findings"]
    if not isinstance(findings, list) or any(
        not isinstance(finding, dict) for finding in findings
    ):
        raise CmocError(
            "refactor findings が配列ではありません。",
            ["Codex call log と output schema を確認してください。"],
            f"target: {target}\noutput: {output!r}",
        )
    return findings


def _completion_reason(
    root: Path,
    unresolved_findings: dict[str, list[_UnresolvedFinding]],
) -> str:
    """loop 完了時の state 不変条件を検査して完了理由を返す。"""
    required = {
        path
        for path, entry in load_refactor_state(root).items()
        if entry["investigation_required"]
    }
    unresolved_targets = set(unresolved_findings)
    if required != unresolved_targets:
        raise CmocError(
            "realization refactor の完了状態が不正です。",
            ["run report と refactor state を確認してください。"],
            f"investigation_required: {sorted(required)}\n"
            f"unresolved targets: {sorted(unresolved_targets)}",
        )
    return "completed_with_unresolved" if unresolved_targets else "natural_completion"


def _completion_change_summary(context: EditingRunContext) -> list[dict] | None:
    """正常完了した refactor fork の tree 差分を要約する。"""
    diff = run_git(
        ["diff", "--binary", context.run_fork_commit, "HEAD"],
        context.run_worktree,
    ).stdout
    if not diff:
        return None
    with pushd(context.run_worktree):
        result = run_codex_exec(
            build_realization_refactor_fork_change_summary_parameter(diff),
            root=context.repo,
            cwd=context.run_worktree,
            config=load_config(context.run_worktree),
            purpose="realization refactor change summary",
        )
    output = result.output_json
    if (
        result.returncode != 0
        or not isinstance(output, dict)
        or set(output) != {"changes"}
        or not isinstance(output["changes"], list)
    ):
        raise CmocError(
            "refactor change summary を生成できません。",
            ["Codex call log と output schema を確認してください。"],
            repr(output),
        )
    return output["changes"]


def _write_refactor_report(
    context: EditingRunContext,
    state_after: str,
    reason: str,
    units: list[tuple[str, int]],
    unresolved_findings: dict[str, list[_UnresolvedFinding]],
    *,
    summary: list[dict] | None,
    error: BaseException | None = None,
    cleanup_errors: list[str] | None = None,
) -> Path:
    state = _safe_refactor_state(context.run_worktree)
    counts = _state_counts(state)
    changes = tree_changes(context.run_worktree, context.run_fork_commit)
    unresolved_targets = set(unresolved_findings)
    uninvestigated_targets = sum(
        entry["investigation_required"] and path not in unresolved_targets
        for path, entry in state.items()
    )
    body = [
        "## Current fork",
        f"- processed targets: {len({target for target, _count in units})}",
        f"- uninvestigated targets: {uninvestigated_targets}",
        "## Processing units",
        *(
            [f"- `{target}`: {count} finding(s)" for target, count in units]
            or ["- none"]
        ),
        "## Unresolved targets",
        f"- count: {len(unresolved_targets)}",
        "- paths:",
        *([f"  - `{target}`" for target in sorted(unresolved_targets)] or ["  - none"]),
        "## Unresolved findings",
        *_render_unresolved_findings(unresolved_findings),
        "## Refactor state",
        f"- entries: {counts['entries']}",
        f"- investigation_required: {counts['required']}",
        f"- not_investigated: {counts['not_investigated']}",
        f"- no_findings: {counts['no_findings']}",
        f"- findings: {counts['findings']}",
        "## Change summary",
        *_render_summary(summary, flattened_change_paths(changes)),
    ]
    if error is not None:
        body.extend(["## Error", repr(error)])
    body.extend(
        [
            "## Cleanup warnings",
            *(
                [f"- {item}" for item in cleanup_errors]
                if cleanup_errors
                else ["- none"]
            ),
        ]
    )
    return write_fork_report(
        context,
        "realization/refactor/fork",
        state_after=state_after,
        completion_reason=reason,
        changed_paths=flattened_change_paths(changes),
        extra_fields={
            "refactor_state_path": refactor_state_path(context.run_worktree).resolve()
        },
        body_lines=body,
    )


def _safe_refactor_state(root: Path) -> RefactorState:
    try:
        return load_refactor_state(root)
    except BaseException:
        return {}


def _state_counts(state: RefactorState) -> dict[str, int]:
    return {
        "entries": len(state),
        "required": sum(entry["investigation_required"] for entry in state.values()),
        "not_investigated": sum(
            entry["last_investigation_result"] == "not_investigated"
            for entry in state.values()
        ),
        "no_findings": sum(
            entry["last_investigation_result"] == "no_findings"
            for entry in state.values()
        ),
        "findings": sum(
            entry["last_investigation_result"] == "findings" for entry in state.values()
        ),
    }


def _render_summary(
    summary: list[dict] | None,
    changed_paths: list[str],
) -> list[str]:
    if summary is not None:
        # {{work-root}}/oracle/doc/app_spec/misc_spec.md
        # Structured Output の path は、実際の managed branch 差分の変更対象に限定する。
        changed_path_set = set(changed_paths)
        lines = []
        for change in summary:
            category = change.get("category", "change")
            description = change.get("summary", "")
            paths = change.get("changed_paths", [])
            lines.append(f"- {category}: {description}")
            lines.extend(
                f"  - `{path}`"
                for path in paths
                if isinstance(path, str) and path in changed_path_set
            )
        return lines or ["- none"]
    if not changed_paths:
        return ["- none"]
    return [f"- committed path: `{path}`" for path in changed_paths]


def _render_unresolved_findings(
    unresolved_findings: dict[str, list[_UnresolvedFinding]],
) -> list[str]:
    """unresolved 所見の理由と追跡可能な Codex call log を表示する。"""
    lines = []
    for target in sorted(unresolved_findings):
        for title, summary, call_log_path in unresolved_findings[target]:
            lines.extend(
                [
                    f"- `{target}`: {title}",
                    f"  - resolution.summary: {summary}",
                    f"  - Codex call log: `{call_log_path}`",
                ]
            )
    return lines or ["- none"]


def _completion_log(
    reason: str,
    unresolved_findings: dict[str, list[_UnresolvedFinding]],
    report: Path,
) -> str:
    """fork 固有の完了理由、unresolved 件数、report path を出力する。"""
    return "\n".join(
        [
            f"- completion_reason: `{reason}`",
            f"- unresolved targets: `{len(unresolved_findings)}`",
            f"- fork report: `{report}`",
        ]
    )
