"""`cmoc feedback report` の repository-local 増分 normalization と report 生成。

この file は 16,000 文字を超えるが、snapshot 固定、normalization unit、checkpoint、
unit manifest、state snapshot、および最終 report record は、一つの
中断可能 transaction の順序を構成する。分割すると確定済み unit と deferred
observation の境界を module 間で重複管理するため、report command の状態機械として
一箇所に保つ。

対応する oracle file:
`{{work-root}}/oracle/doc/app_spec/sub_command/feedback_report.md`。
"""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import typer
from jsonschema import validators
from jsonschema.exceptions import SchemaError

from acp.builder.feedback.normalize_issue import (
    build_feedback_normalize_issue_parameter,
)
from cmoc_runtime import (
    CmocError,
    current_branch,
    load_state_for_branch,
    repo_root,
    run_cli_subcommand,
    run_codex_exec,
    start_subcommand_step,
    work_root,
)
from commons.runtime_feedback_state import (
    IssueView,
    agent_canonical_key,
    assessment_record,
    build_state_snapshot,
    effective_ingestion_receipts,
    feedback_writer_lock,
    identity_record,
    ingestion_record,
    issue_id,
    load_effective_feedback_state,
    load_issue_views,
    load_issue_views_from_snapshot,
    machine_canonical_key,
    new_report_id,
    normalization_unit_id,
    normalizer_version,
    occurrence_record,
    prepare_report_publication,
    previous_state_snapshot_id,
    previous_successful_report_id,
    publish_normalization_unit,
    publish_report_record,
    recover_normalization_units,
    recover_report_publications,
    report_record,
    revision_record,
    validate_feedback_state,
    validate_observation_envelope,
)
from commons.runtime_feedback_store import (
    canonical_json_bytes,
    feedback_root,
    iter_observation_paths,
    normalization_checkpoint_root,
    observation_path,
    parse_rfc3339,
    recover_immutable_bytes_from_temporary,
    report_snapshot_root,
    rfc3339_now,
    sha256_bytes,
    write_immutable_bytes,
    write_immutable_json,
)
from commons.runtime_logging import current_subcommand_logger
from commons.runtime_paths import reports_dir, timestamp
from commons.runtime_results import StructuredOutputValidationIssue


def cmoc_feedback_report_impl(
    show_all: bool = False,
) -> None:
    """CLI runtime を通して feedback report を実行する。"""
    run_cli_subcommand(
        _cmoc_feedback_report_body,
        show_all,
        command_name="feedback report",
        command_argv=[
            "cmoc",
            "feedback",
            "report",
            *(["--all"] if show_all else []),
        ],
        total_steps=6,
    )


def _cmoc_feedback_report_body(
    show_all: bool,
) -> int:
    """snapshot 内の未処理 observation を unit ごとに確定する。"""
    repo = repo_root()
    worktree = work_root()
    start_subcommand_step(
        2, "feedback report の事前条件を確認", "validate feedback report preconditions"
    )
    _validate_preconditions(repo, worktree)
    with feedback_writer_lock(repo):
        start_subcommand_step(
            3,
            "feedback state の整合性を確認",
            "validate feedback state",
        )
        recovered_units = recover_normalization_units(repo)
        recover_report_publications(repo)
        validate_feedback_state(repo, require_no_orphans=True)
        return _cmoc_feedback_report_locked(repo, worktree, show_all, recovered_units)


def _cmoc_feedback_report_locked(
    repo: Path,
    worktree: Path,
    show_all: bool,
    recovered_unit_ids: list[str],
) -> int:
    """repository-level writer lock 保持中に report transaction を完了する。"""
    previous_views = _previous_normal_issue_views(repo)

    report_id = new_report_id()
    generated_at = rfc3339_now()
    start_subcommand_step(
        4, "raw observation snapshot を保存", "snapshot raw observations"
    )
    snapshot, snapshot_sha256 = _write_snapshot(repo, report_id, generated_at)
    entries = snapshot["observations"]
    assert isinstance(entries, list)
    observation_map = _read_snapshot_observations(entries)

    # 既存 receipt の hash 一致を先に検査し、corruption を unit 処理へ混ぜない。
    pending, _, normalization_unit_ids = _pending_entries(repo, entries)
    normalization_unit_ids[:0] = recovered_unit_ids
    invalid_count = 0
    normalization_agent_call_count = 0
    processed_count = 0
    result = "ok"
    partial_error: BaseException | None = None
    start_subcommand_step(
        5, "observation を増分 normalization", "normalize feedback observations"
    )
    try:
        # schema 不正 record は改変せず invalid receipt だけを確定する。
        valid_pending: list[dict[str, Any]] = []
        for entry in pending:
            observation_id = str(entry["observation_id"])
            observation = observation_map.get(observation_id)
            errors = (
                ["raw observation is not valid JSON object"]
                if observation is None
                else validate_observation_envelope(
                    observation,
                    expected_repo_root=repo,
                )
            )
            if (
                observation is not None
                and observation.get("observation_id") != observation_id
            ):
                errors.append("/observation_id: file name and payload differ")
            if errors:
                unit_id = _publish_invalid_observation(
                    repo, entry, errors, generated_at
                )
                normalization_unit_ids.append(unit_id)
                invalid_count += 1
                processed_count += 1
            else:
                valid_pending.append(entry)

        # machine observation は canonical key 完全一致の集合を一 unit にする。
        machine_groups: dict[str, list[dict[str, Any]]] = {}
        agent_entries: list[dict[str, Any]] = []
        for entry in valid_pending:
            observation = observation_map[str(entry["observation_id"])]
            if observation.get("source") == "machine_rule":
                key = machine_canonical_key(observation)
                machine_groups.setdefault(key, []).append(entry)
            else:
                agent_entries.append(entry)
        for canonical_key, group in sorted(machine_groups.items()):
            _issue, unit_id = _integrate_machine_group(
                repo,
                canonical_key,
                group,
                observation_map,
                generated_at,
            )
            normalization_unit_ids.append(unit_id)
            processed_count += len(group)

        # agent observation は一件ずつ候補を絞り込み、曖昧な場合だけ agent を使う。
        for entry in sorted(
            agent_entries, key=lambda item: str(item["observation_id"])
        ):
            _issue, unit_id, agent_used = _integrate_agent_observation(
                repo,
                worktree,
                entry,
                observation_map,
                generated_at,
            )
            normalization_unit_ids.append(unit_id)
            normalization_agent_call_count += int(agent_used)
            processed_count += 1

        # 新規 observation がなくても、既存 evidence の現在 fingerprint が変われば
        # machine assessment を独立 unit として追加する。
        for view in load_issue_views(repo).values():
            assessment_unit_id = _refresh_issue_assessment(
                repo,
                view,
                observation_map,
                generated_at,
            )
            if assessment_unit_id is not None:
                normalization_unit_ids.append(assessment_unit_id)
    except KeyboardInterrupt:
        processed_count, invalid_count = _effective_observation_counts(repo, entries)
        _, _, committed_unit_ids = _pending_entries(repo, entries)
        normalization_unit_ids.extend(committed_unit_ids)
        result = "interrupted"
        _record_feedback_interruption()
    except BaseException as exc:
        processed_count, invalid_count = _effective_observation_counts(repo, entries)
        _, _, committed_unit_ids = _pending_entries(repo, entries)
        normalization_unit_ids.extend(committed_unit_ids)
        result = "partial"
        partial_error = exc

    validate_feedback_state(repo, require_no_orphans=True)

    # 確定済み unit manifest だけから report を作り、未処理 entry は deferred とする。
    start_subcommand_step(
        6, "feedback report と state snapshot を保存", "write feedback report"
    )
    views = load_issue_views(repo)
    changed_issue_ids, disposition_changed_issue_ids = _issue_changes(
        previous_views,
        views,
    )
    deferred_count = _deferred_count(repo, entries)
    default_visible, suppressed = _visible_issues(
        views,
        observation_map,
        changed_issue_ids,
        disposition_changed_issue_ids,
        False,
    )
    visible = (
        _visible_issues(
            views,
            observation_map,
            changed_issue_ids,
            disposition_changed_issue_ids,
            True,
        )[0]
        if show_all
        else default_visible
    )
    needs_revalidation_count = sum(
        view.assessment is not None
        and view.assessment.get("freshness") == "needs_revalidation"
        for view in views.values()
    )
    recurrent_open_count = sum(
        _is_recurrent_open(view, observation_map) for view in views.values()
    )
    if result == "ok" and (default_visible or invalid_count):
        result = "attention"
    normalization_unit_ids = list(dict.fromkeys(normalization_unit_ids))
    state_snapshot, _state_snapshot_sha256 = build_state_snapshot(
        repo, created_at=generated_at
    )
    state_snapshot_id = str(state_snapshot["state_snapshot_id"])
    predecessor_id = previous_successful_report_id(repo)
    report_path, report_sha256, report_content = _write_report(
        repo=repo,
        worktree=worktree,
        report_id=report_id,
        generated_at=generated_at,
        snapshot_sha256=snapshot_sha256,
        snapshot_count=len(entries),
        processed_count=processed_count,
        deferred_count=deferred_count,
        invalid_count=invalid_count,
        normalization_agent_call_count=normalization_agent_call_count,
        changed_issue_ids=changed_issue_ids,
        disposition_changed_issue_ids=disposition_changed_issue_ids,
        recurrent_open_count=recurrent_open_count,
        needs_revalidation_count=needs_revalidation_count,
        suppressed_count=len(suppressed),
        show_all=show_all,
        normalization_unit_ids=normalization_unit_ids,
        state_snapshot_id=state_snapshot_id,
        previous_successful_report_id=predecessor_id,
        result=result,
        visible=visible,
        observations=observation_map,
        partial_error=partial_error,
    )
    report_state = report_record(
        report_id=report_id,
        generated_at=generated_at,
        report_snapshot_sha256=snapshot_sha256,
        report_snapshot_observation_count=len(entries),
        processed_observation_count=processed_count,
        deferred_observation_count=deferred_count,
        report_path=report_path,
        report_sha256=report_sha256,
        result=result,
        normalization_unit_ids=normalization_unit_ids,
        state_snapshot_id=state_snapshot_id,
        previous_successful_report_id=predecessor_id,
    )
    prepare_report_publication(repo, report_state)
    write_immutable_bytes(report_path, report_content)
    report_record_path = publish_report_record(repo, report_state)
    validate_feedback_state(repo, require_no_orphans=True)
    logger = current_subcommand_logger()
    if logger is not None:
        logger.event(
            "feedback_report_committed",
            report_id=report_id,
            normalization_unit_ids=normalization_unit_ids,
            state_snapshot_id=state_snapshot_id,
            report_record_path=str(report_record_path),
        )
    typer.echo(f"- feedback report: `{report_path}`")
    for unit_id in normalization_unit_ids:
        typer.echo(f"- feedback normalization unit: `{unit_id}`")
    typer.echo(f"- feedback state snapshot: `{state_snapshot_id}`")
    typer.echo(f"- feedback report record: `{report_record_path}`")
    if result == "partial":
        return 2
    if result == "error":
        return 1
    return 0


def _validate_preconditions(repo: Path, worktree: Path) -> None:
    """main worktree、active session branch、ready run state を検査する。"""
    if repo.resolve() != worktree.resolve():
        raise CmocError(
            "feedback report は main worktree 上で実行してください。",
            ["active session branch の main worktree へ移動してください。"],
            f"repo_root: {repo}\nwork_root: {worktree}",
        )
    branch = current_branch(worktree)
    if not branch.startswith("cmoc/session/"):
        raise CmocError(
            "feedback report は active session branch 上で実行してください。",
            ["`cmoc session fork` 後の branch で再実行してください。"],
            branch,
        )
    _, state_path, state = load_state_for_branch(repo, branch)
    if state.session.state != "active" or state.run.state != "ready":
        raise CmocError(
            "feedback report の session/run state が事前条件を満たしません。",
            ["active session の editing run を join または abandon してください。"],
            f"state: {state_path}\n{json.dumps(state.to_dict(), ensure_ascii=False)}",
        )


def _write_snapshot(
    repo: Path, report_id: str, generated_at: str
) -> tuple[dict[str, Any], str]:
    """raw observation の path、ID、SHA256 を固定した manifest を保存する。"""
    observations = [
        {
            "path": str(path.resolve()),
            "observation_id": path.stem,
            "sha256": sha256_bytes(path.read_bytes()),
        }
        for path in iter_observation_paths(repo)
    ]
    manifest: dict[str, Any] = {
        "schema_version": 1,
        "report_id": report_id,
        "generated_at": generated_at,
        "observations": observations,
    }
    path = report_snapshot_root(repo) / f"{report_id}.json"
    digest = write_immutable_json(path, manifest)
    return manifest, digest


def _read_snapshot_observations(
    entries: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """snapshot path の raw JSON object を ID ごとに best effort で読む。"""
    observations: dict[str, dict[str, Any]] = {}
    for entry in entries:
        observation_id = entry.get("observation_id")
        path = entry.get("path")
        if not isinstance(observation_id, str) or not isinstance(path, str):
            continue
        try:
            raw_path = Path(path)
            content = raw_path.read_bytes()
            if sha256_bytes(content) != entry.get("sha256"):
                raise CmocError(
                    "snapshot 後に raw feedback observation が変化しました。",
                    ["raw observation store の corruption を確認してください。"],
                    str(raw_path),
                )
            value = json.loads(content)
            if not isinstance(value, dict):
                continue
            observations[observation_id] = value
        except CmocError:
            raise
        except (OSError, UnicodeError, ValueError, json.JSONDecodeError):
            continue
    return observations


def _pending_entries(
    repo: Path, entries: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], int, list[str]]:
    """receipt と hash が一致する entry を除き、corruption を拒否する。"""
    pending: list[dict[str, Any]] = []
    processed = 0
    reused_unit_ids: list[str] = []
    seen: dict[str, str] = {}
    state = load_effective_feedback_state(repo)
    receipts = {
        str(record["observation_id"]): record
        for relative, record in state.records.items()
        if relative.startswith("ingestion/")
    }
    for entry in entries:
        observation_id = str(entry.get("observation_id"))
        digest = str(entry.get("sha256"))
        previous_digest = seen.get(observation_id)
        if previous_digest is not None:
            if previous_digest != digest:
                raise CmocError(
                    "同じ observation ID に異なる SHA256 があります。",
                    ["raw observation store の corruption を確認してください。"],
                    f"observation_id: {observation_id}",
                )
            continue
        seen[observation_id] = digest
        receipt = receipts.get(observation_id)
        if receipt is None:
            pending.append(entry)
            continue
        if receipt.get("observation_sha256") != digest:
            raise CmocError(
                "ingestion receipt と raw observation の SHA256 が一致しません。",
                [
                    "raw observation と effective receipt の corruption を確認してください。"
                ],
                f"observation_id: {observation_id}",
            )
        processed += 1
        unit_id = receipt.get("normalization_unit_id")
        if isinstance(unit_id, str) and unit_id in state.unit_manifests:
            reused_unit_ids.append(unit_id)
    return pending, processed, reused_unit_ids


def _record_feedback_interruption() -> None:
    """ユーザー中断を正常な report 終了理由として console と log に残す。"""
    typer.echo(
        "# ユーザー中断要求を受け付けました\n"
        "- 確定済みの normalization unit で feedback report を完了します。"
    )
    logger = current_subcommand_logger()
    if logger is not None:
        logger.event(
            "user_interruption",
            command="feedback report",
            result="interrupted",
        )


def _previous_normal_issue_views(repo: Path) -> dict[str, IssueView]:
    """正常 report 連鎖の直前 state snapshot から issue view を返す。"""
    snapshot_id = previous_state_snapshot_id(repo)
    return (
        load_issue_views_from_snapshot(repo, snapshot_id)
        if snapshot_id is not None
        else {}
    )


def _issue_changes(
    previous: dict[str, IssueView],
    current: dict[str, IssueView],
) -> tuple[set[str], set[str]]:
    """直前の正常 state snapshot からの revision/disposition 差分を返す。"""
    changed: set[str] = set()
    disposition_changed: set[str] = set()
    for current_issue_id, view in current.items():
        old = previous.get(current_issue_id)
        if old is None or old.revision.get("revision_id") != view.revision.get(
            "revision_id"
        ):
            changed.add(current_issue_id)
        old_decision = (
            old.disposition.get("decision_id")
            if old is not None and old.disposition is not None
            else None
        )
        current_decision = (
            view.disposition.get("decision_id")
            if view.disposition is not None
            else None
        )
        if old is not None and old_decision != current_decision:
            disposition_changed.add(current_issue_id)
    return changed, disposition_changed


def _publish_invalid_observation(
    repo: Path,
    entry: dict[str, Any],
    errors: list[str],
    processed_at: str,
) -> str:
    """schema 不正 observation の invalid receipt を一 unit で確定する。"""
    observation_id = str(entry["observation_id"])
    version = normalizer_version(False)
    unit_id = normalization_unit_id([observation_id], [], version)
    receipt = ingestion_record(
        observation_id,
        str(entry["sha256"]),
        processed_at,
        unit_id,
        version,
        "invalid",
        [],
        errors,
    )
    return publish_normalization_unit(
        repo,
        normalization_unit_id_value=unit_id,
        observations=[
            {
                "observation_id": observation_id,
                "observation_sha256": str(entry["sha256"]),
            }
        ],
        candidate_revision_ids=[],
        normalizer_schema_sha256=version,
        normalizer_version_value=version,
        records=[("ingestion", receipt)],
        checkpoint_sha256=None,
    )


def _integrate_machine_group(
    repo: Path,
    canonical_key: str,
    entries: list[dict[str, Any]],
    observations: dict[str, dict[str, Any]],
    processed_at: str,
) -> tuple[str, str]:
    """同じ machine canonical key の observation を一 issue へ統合する。"""
    current_issue_id = issue_id(canonical_key)
    views = load_issue_views(repo)
    existing = views.get(current_issue_id)
    first = observations[str(entries[0]["observation_id"])]
    payload = first["payload"]
    assert isinstance(payload, dict)
    records: list[tuple[str, dict[str, Any]]] = []
    if existing is None:
        records.append(
            (
                "identity",
                identity_record(
                    current_issue_id,
                    canonical_key,
                    "machine_rule",
                    str(first["observation_id"]),
                    str(first["observed_at"]),
                ),
            )
        )
    elif existing.identity.get("canonical_key") != canonical_key:
        raise CmocError(
            "feedback issue ID collision を検出しました。",
            ["canonical key と issue directory を人間が確認してください。"],
            current_issue_id,
        )
    source_ids = {
        str(record.get("observation_id"))
        for record in (existing.occurrences if existing is not None else [])
    }
    source_ids.update(str(entry["observation_id"]) for entry in entries)
    records.append(
        (
            "revision",
            revision_record(
                current_issue_id,
                processed_at,
                sorted(source_ids),
                str(payload["category"]),
                str(payload["summary"]),
                str(payload["human_action"]),
                str(payload["impact"]),
                {"certainty": "supported", "description": "allowlist rule matched"},
                [],
            ),
        )
    )
    for entry in entries:
        observation = observations[str(entry["observation_id"])]
        records.append(
            (
                "occurrence",
                occurrence_record(current_issue_id, observation, str(entry["sha256"])),
            )
        )
    records.append(
        (
            "assessment",
            assessment_record(
                current_issue_id,
                processed_at,
                "unknown",
                "unavailable",
                "fingerprint_unavailable",
                "machine event に現在状態の file fingerprint がないため再検証できない。",
                [],
            ),
        )
    )
    version = normalizer_version(False)
    unit_id = normalization_unit_id(
        [str(entry["observation_id"]) for entry in entries], [], version
    )
    for entry in entries:
        records.append(
            (
                "ingestion",
                ingestion_record(
                    str(entry["observation_id"]),
                    str(entry["sha256"]),
                    processed_at,
                    unit_id,
                    version,
                    "integrated",
                    [current_issue_id],
                    [],
                ),
            )
        )
    published = publish_normalization_unit(
        repo,
        normalization_unit_id_value=unit_id,
        observations=[
            {
                "observation_id": str(entry["observation_id"]),
                "observation_sha256": str(entry["sha256"]),
            }
            for entry in entries
        ],
        candidate_revision_ids=[],
        normalizer_schema_sha256=version,
        normalizer_version_value=version,
        records=records,
        checkpoint_sha256=None,
    )
    return current_issue_id, published


def _integrate_agent_observation(
    repo: Path,
    worktree: Path,
    entry: dict[str, Any],
    observations: dict[str, dict[str, Any]],
    processed_at: str,
) -> tuple[str, str, bool]:
    """一 agent observation を exact match または normalization agent で統合する。"""
    observation_id = str(entry["observation_id"])
    observation = observations[observation_id]
    views = load_issue_views(repo)
    exact, candidates = _candidate_issues(observation, views, observations)
    requires_agent = exact is None and bool(candidates)
    agent_called = False
    normalized: dict[str, Any]
    selected: IssueView | None = exact
    related_ids: list[str] = []
    checkpoint_path: Path | None = None
    candidate_revision_ids = [str(view.revision["revision_id"]) for view in candidates]
    version = normalizer_version(requires_agent)
    schema_sha256 = version

    if requires_agent:
        output, checkpoint_path, unit_id, agent_called, schema_sha256 = (
            _normalize_with_agent(
                repo,
                worktree,
                observation,
                str(entry["sha256"]),
                candidates,
                version,
            )
        )
        decision = output.get("decision")
        if decision == "existing":
            selected_id = output.get("existing_issue_id")
            selected = views.get(str(selected_id))
            if selected is None or selected not in candidates:
                raise CmocError(
                    "normalization agent が候補外 issue を選択しました。",
                    [
                        "normalization checkpoint と Structured Output を確認してください。"
                    ],
                    str(selected_id),
                )
        normalized_value = output.get("normalized_issue")
        if not isinstance(normalized_value, dict):
            raise ValueError("normalized_issue must be an object")
        normalized = normalized_value
        related = output.get("related_issue_ids", [])
        related_ids = (
            [str(value) for value in related] if isinstance(related, list) else []
        )
    else:
        unit_id = normalization_unit_id(
            [observation_id], candidate_revision_ids, version
        )
        normalized = _deterministic_normalized_issue(observation, selected)

    if selected is None:
        canonical_key = agent_canonical_key(observation_id)
        current_issue_id = issue_id(canonical_key)
        category = str(observation["payload"]["category"])
    else:
        canonical_key = str(selected.identity["canonical_key"])
        current_issue_id = selected.issue_id
        category = str(selected.revision["category"])
    records: list[tuple[str, dict[str, Any]]] = []
    if selected is None:
        records.append(
            (
                "identity",
                identity_record(
                    current_issue_id,
                    canonical_key,
                    "agent_report",
                    observation_id,
                    str(observation["observed_at"]),
                ),
            )
        )
    existing_source_ids = {
        str(record.get("observation_id"))
        for record in (selected.occurrences if selected is not None else [])
    }
    existing_source_ids.add(observation_id)
    cause = normalized.get("cause_assessment")
    if not isinstance(cause, dict):
        cause = {"certainty": "unknown", "description": "原因を評価できない。"}
    records.extend(
        [
            (
                "revision",
                revision_record(
                    current_issue_id,
                    processed_at,
                    sorted(existing_source_ids),
                    category,
                    str(normalized["summary"]),
                    str(normalized["human_action"]),
                    str(normalized["impact"]),
                    {
                        "certainty": str(cause["certainty"]),
                        "description": str(cause["description"]),
                    },
                    related_ids,
                ),
            ),
            (
                "occurrence",
                occurrence_record(current_issue_id, observation, str(entry["sha256"])),
            ),
        ]
    )
    assessment = _assessment_for_observation(
        current_issue_id,
        processed_at,
        observation,
        normalized.get("presence_assessment") if requires_agent else None,
    )
    records.append(("assessment", assessment))
    records.append(
        (
            "ingestion",
            ingestion_record(
                observation_id,
                str(entry["sha256"]),
                processed_at,
                unit_id,
                version,
                "integrated",
                [current_issue_id],
                [],
            ),
        )
    )
    checkpoint_sha256 = (
        sha256_bytes(checkpoint_path.read_bytes())
        if checkpoint_path is not None
        else None
    )
    published = publish_normalization_unit(
        repo,
        normalization_unit_id_value=unit_id,
        observations=[
            {
                "observation_id": observation_id,
                "observation_sha256": str(entry["sha256"]),
            }
        ],
        candidate_revision_ids=candidate_revision_ids,
        normalizer_schema_sha256=schema_sha256,
        normalizer_version_value=version,
        records=records,
        checkpoint_sha256=checkpoint_sha256,
    )
    return current_issue_id, published, agent_called


def _candidate_issues(
    observation: dict[str, Any],
    views: dict[str, IssueView],
    observations: dict[str, dict[str, Any]],
) -> tuple[IssueView | None, list[IssueView]]:
    """category、evidence path、fingerprint で normalization 候補を絞る。"""
    payload = observation["payload"]
    assert isinstance(payload, dict)
    category = payload.get("category")
    deduplication_hint = payload.get("deduplication_hint")
    fingerprints = observation.get("evidence_fingerprints", [])
    current_by_path = {
        item.get("normalized_path"): item.get("sha256")
        for item in fingerprints
        if isinstance(item, dict) and isinstance(item.get("normalized_path"), str)
    }
    current_fingerprint_pairs = [
        (item.get("normalized_path"), item.get("sha256"))
        for item in fingerprints
        if isinstance(item, dict) and isinstance(item.get("normalized_path"), str)
    ]
    current_fingerprints_hashed = bool(current_fingerprint_pairs) and all(
        isinstance(path, str) and isinstance(digest, str)
        for path, digest in current_fingerprint_pairs
    )
    exact: list[IssueView] = []
    candidates: list[IssueView] = []
    for view in views.values():
        if view.revision.get("category") != category:
            continue
        path_match = False
        hash_match = False
        hint_match = False
        for occurrence in view.occurrences:
            previous = observations.get(str(occurrence.get("observation_id")))
            if previous is None:
                continue
            previous_payload = previous.get("payload")
            if (
                isinstance(deduplication_hint, str)
                and isinstance(previous_payload, dict)
                and previous_payload.get("deduplication_hint") == deduplication_hint
            ):
                # agent hint は候補検索だけに使い、完全一致や issue key には使わない。
                hint_match = True
            previous_fingerprints = previous.get("evidence_fingerprints", [])
            previous_fingerprint_pairs: list[tuple[object, object]] = []
            previous_fingerprints_hashed = True
            for item in previous_fingerprints:
                if not isinstance(item, dict):
                    previous_fingerprints_hashed = False
                    continue
                path = item.get("normalized_path")
                if path in current_by_path:
                    path_match = True
                if isinstance(path, str):
                    digest = item.get("sha256")
                    previous_fingerprint_pairs.append((path, digest))
                    if not isinstance(digest, str):
                        previous_fingerprints_hashed = False
            if (
                current_fingerprints_hashed
                and previous_fingerprints_hashed
                and sorted(previous_fingerprint_pairs)
                == sorted(current_fingerprint_pairs)
            ):
                hash_match = True
        if path_match or hint_match:
            candidates.append(view)
        if hash_match:
            exact.append(view)
    return (exact[0] if len(exact) == 1 else None), candidates


def _normalize_with_agent(
    repo: Path,
    worktree: Path,
    observation: dict[str, Any],
    observation_sha256: str,
    candidates: list[IssueView],
    version: str,
) -> tuple[dict[str, Any], Path, str, bool, str]:
    """checkpoint を再利用し、必要な場合だけ normalization agent を呼ぶ。"""
    observation_id = str(observation["observation_id"])
    candidate_payload = [
        {
            "issue_id": view.issue_id,
            "identity": view.identity,
            "effective_revision": view.revision,
            "effective_assessment": view.assessment,
            "effective_disposition": view.disposition,
        }
        for view in candidates
    ]
    reference_paths: list[Path] = []
    for item in observation.get("evidence_fingerprints", []):
        if not isinstance(item, dict) or not isinstance(
            item.get("normalized_path"), str
        ):
            continue
        reference = _current_repo_path(Path(item["normalized_path"]), repo)
        if reference is not None and reference.exists():
            reference_paths.append(reference)
    parameter = build_feedback_normalize_issue_parameter(
        json.dumps(observation, ensure_ascii=False, sort_keys=True),
        json.dumps(candidate_payload, ensure_ascii=False, sort_keys=True),
        reference_paths,
        worktree,
    )
    schema_path = parameter.structured_output_schema_path
    assert schema_path is not None
    schema_sha256 = sha256_bytes(schema_path.read_bytes())
    unit_id = normalization_unit_id(
        [observation_id],
        [str(view.revision["revision_id"]) for view in candidates],
        schema_sha256,
    )
    checkpoint_path = normalization_checkpoint_root(repo) / f"{unit_id}.json"
    allowed = {view.issue_id for view in candidates}
    checkpoint, checkpoint_content = _recoverable_checkpoint(checkpoint_path)
    if checkpoint is not None:
        expected_candidate_ids = sorted(
            str(view.revision["revision_id"]) for view in candidates
        )
        if (
            checkpoint.get("schema_version") == 1
            and checkpoint.get("normalization_unit_id") == unit_id
            and checkpoint.get("observation_sha256") == observation_sha256
            and checkpoint.get("schema_sha256") == schema_sha256
            and checkpoint.get("candidate_revision_ids") == expected_candidate_ids
            and checkpoint.get("normalizer_version") == version
            and isinstance(checkpoint.get("structured_output"), dict)
            and _normalization_output_matches_contract(
                checkpoint["structured_output"], schema_path, allowed
            )
        ):
            assert checkpoint_content is not None
            recover_immutable_bytes_from_temporary(
                checkpoint_path,
                sha256_bytes(checkpoint_content),
            )
            return (
                checkpoint["structured_output"],
                checkpoint_path,
                unit_id,
                False,
                schema_sha256,
            )
        raise CmocError(
            "feedback normalization checkpoint が入力と一致しません。",
            ["checkpoint の corruption を確認し、手動対応してください。"],
            str(checkpoint_path),
        )

    def postcondition(
        output: Any, changed_paths: frozenset[str]
    ) -> tuple[StructuredOutputValidationIssue, ...]:
        """候補外 issue ID と existing/related 重複を拒否する。"""
        del changed_paths
        return _normalization_candidate_issues(output, allowed)

    result = run_codex_exec(
        parameter,
        root=repo,
        purpose="feedback issue normalization",
        structured_output_postcondition=postcondition,
    )
    if not isinstance(result.output_json, dict):
        raise ValueError("normalization output must be an object")
    checkpoint = {
        "schema_version": 1,
        "normalization_unit_id": unit_id,
        "observation_sha256": observation_sha256,
        "candidate_revision_ids": [
            str(view.revision["revision_id"])
            for view in sorted(
                candidates,
                key=lambda item: str(item.revision["revision_id"]),
            )
        ],
        "schema_sha256": schema_sha256,
        "normalizer_version": version,
        "structured_output": result.output_json,
    }
    write_immutable_json(checkpoint_path, checkpoint)
    return result.output_json, checkpoint_path, unit_id, True, schema_sha256


def _recoverable_checkpoint(path: Path) -> tuple[dict[str, Any] | None, bytes | None]:
    """final file または同一 byte 列の sibling temporary から checkpoint を読む。"""
    temporaries: list[Path] = []
    if path.parent.is_dir():
        prefix = f".{path.name}."
        temporaries = [
            candidate
            for candidate in path.parent.iterdir()
            if candidate.name.startswith(prefix) and candidate.name.endswith(".tmp")
        ]
    if path.exists() or path.is_symlink():
        if path.is_symlink() or not path.is_file():
            raise CmocError(
                "feedback normalization checkpoint path が通常 file ではありません。",
                ["checkpoint path を人間が確認してください。"],
                str(path),
            )
        candidates = [path, *temporaries]
    else:
        candidates = temporaries
    if not candidates:
        return None, None
    contents: list[bytes] = []
    for candidate in candidates:
        if candidate.is_symlink() or not candidate.is_file():
            raise CmocError(
                "feedback normalization checkpoint temporary file が不正です。",
                ["checkpoint path を人間が確認してください。"],
                str(candidate),
            )
        contents.append(candidate.read_bytes())
    if any(content != contents[0] for content in contents[1:]):
        raise CmocError(
            "feedback normalization checkpoint temporary file の byte 列が一致しません。",
            ["異なる checkpoint 候補を人間が確認してください。"],
            str(path),
        )
    try:
        checkpoint = json.loads(contents[0])
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise CmocError(
            "feedback normalization checkpoint temporary file が JSON ではありません。",
            ["checkpoint path を人間が確認してください。"],
            str(path),
        ) from exc
    if (
        not isinstance(checkpoint, dict)
        or canonical_json_bytes(checkpoint) != contents[0]
    ):
        raise CmocError(
            "feedback normalization checkpoint temporary file が canonical JSON object ではありません。",
            ["checkpoint path を人間が確認してください。"],
            str(path),
        )
    return checkpoint, contents[0]


def _normalization_output_matches_contract(
    output: dict[str, Any],
    schema_path: Path,
    allowed: set[str],
) -> bool:
    """checkpoint の Structured Output schema と決定論的事後条件を再検証する。"""
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        validator_class = validators.validator_for(schema)
        validator_class.check_schema(schema)
        if tuple(validator_class(schema).iter_errors(output)):
            return False
    except (OSError, UnicodeError, json.JSONDecodeError, SchemaError, TypeError):
        return False
    return not _normalization_candidate_issues(output, allowed)


def _normalization_candidate_issues(
    output: object,
    allowed: set[str],
) -> tuple[StructuredOutputValidationIssue, ...]:
    """normalization output が入力候補 ID だけを参照するか検査する。"""
    if not isinstance(output, dict):
        return ()
    issues: list[StructuredOutputValidationIssue] = []
    existing_id = output.get("existing_issue_id")
    related = output.get("related_issue_ids", [])
    if existing_id is not None and existing_id not in allowed:
        issues.append(
            StructuredOutputValidationIssue(
                "candidate issue ID",
                "$.existing_issue_id",
                f"one of {sorted(allowed)!r}",
                repr(existing_id),
            )
        )
    if isinstance(related, list):
        invalid = [value for value in related if value not in allowed]
        if invalid:
            issues.append(
                StructuredOutputValidationIssue(
                    "related candidate issue IDs",
                    "$.related_issue_ids",
                    f"subset of {sorted(allowed)!r}",
                    repr(invalid),
                )
            )
        if existing_id in related:
            issues.append(
                StructuredOutputValidationIssue(
                    "existing issue is not related duplicate",
                    "$.related_issue_ids",
                    "must not contain $.existing_issue_id",
                    repr(related),
                )
            )
    return tuple(issues)


def _deterministic_normalized_issue(
    observation: dict[str, Any], selected: IssueView | None
) -> dict[str, Any]:
    """新規 agent report または exact match の revision 内容を決める。"""
    if selected is not None:
        return {
            "summary": selected.revision["summary"],
            "human_action": selected.revision["human_action"],
            "impact": selected.revision["impact"],
            "cause_assessment": selected.revision["cause_assessment"],
        }
    payload = observation["payload"]
    assert isinstance(payload, dict)
    cause = payload.get("cause")
    assert isinstance(cause, dict)
    # agent 自己申告の known は機械的に裏付けられないため supported へ昇格しない。
    certainty = (
        "suspected" if cause.get("certainty") in {"known", "suspected"} else "unknown"
    )
    return {
        "summary": payload["summary"],
        "human_action": payload["human_action_reason"],
        "impact": payload["impact"],
        "cause_assessment": {
            "certainty": certainty,
            "description": cause["description"],
        },
    }


def _assessment_for_observation(
    current_issue_id: str,
    assessed_at: str,
    observation: dict[str, Any],
    agent_assessment: object,
) -> dict[str, Any]:
    """normalizer 判断または fingerprint 比較から assessment を構築する。"""
    compared: list[dict[str, Any]] = []
    unavailable = False
    changed = False
    context = observation.get("context")
    repo_value = context.get("repo_root") if isinstance(context, dict) else None
    repository = Path(repo_value) if isinstance(repo_value, str) else None
    for item in observation.get("evidence_fingerprints", []):
        if not isinstance(item, dict) or not isinstance(
            item.get("normalized_path"), str
        ):
            continue
        path = Path(item["normalized_path"])
        current_state = "missing"
        current_hash: str | None = None
        try:
            current_path = (
                _current_repo_path(path, repository) if repository is not None else None
            )
            if current_path is None:
                current_state = "unreadable"
            elif current_path.is_file():
                current_hash = sha256_bytes(current_path.read_bytes())
                current_state = "hashed"
            elif current_path.exists():
                current_state = "not_file"
        except OSError:
            current_state = "unreadable"
        compared.append(
            {
                "path": str(path),
                "old_sha256": item.get("sha256"),
                "current_sha256": current_hash,
                "state": current_state,
            }
        )
        unavailable |= current_state != "hashed" or item.get("state") != "hashed"
        changed |= item.get("sha256") != current_hash
    if isinstance(agent_assessment, dict):
        if unavailable or not compared:
            freshness = "unavailable"
        elif changed:
            freshness = "needs_revalidation"
        else:
            freshness = "current"
        return assessment_record(
            current_issue_id,
            assessed_at,
            str(agent_assessment.get("presence", "unknown")),
            freshness,
            "normalizer_assessment",
            str(agent_assessment.get("reason", "normalizer assessment")),
            compared,
        )
    if unavailable or not compared:
        values = (
            "unknown",
            "unavailable",
            "fingerprint_unavailable",
            "現在の fingerprint を取得できない。",
        )
    elif changed:
        values = (
            "unknown",
            "needs_revalidation",
            "fingerprint_changed",
            "observation 時点から fingerprint が変化した。",
        )
    else:
        values = (
            "likely_present",
            "current",
            "observation_matches_current",
            "observation と現在の fingerprint が一致する。",
        )
    return assessment_record(
        current_issue_id,
        assessed_at,
        values[0],
        values[1],
        values[2],
        values[3],
        compared,
    )


def _current_repo_path(path: Path, repository: Path) -> Path | None:
    """現在解決される path が repository 内なら resolved path を返す。"""
    try:
        root = repository.resolve(strict=False)
        resolved = path.resolve(strict=False)
    except OSError:
        return None
    if resolved == root or root in resolved.parents:
        return resolved
    return None


def _refresh_issue_assessment(
    repo: Path,
    view: IssueView,
    observations: dict[str, dict[str, Any]],
    assessed_at: str,
) -> str | None:
    """現在 fingerprint が前 assessment から変わった issue を再評価する。"""
    available = [
        (occurrence, observations.get(str(occurrence.get("observation_id"))))
        for occurrence in view.occurrences
    ]
    available = [
        (occurrence, observation)
        for occurrence, observation in available
        if observation is not None
    ]
    if not available:
        return None
    occurrence, observation = max(
        available,
        key=lambda item: (
            _parse_time(item[0].get("observed_at"))
            or datetime.min.replace(tzinfo=timezone.utc),
            str(item[0].get("observation_id", "")),
        ),
    )
    assert observation is not None
    candidate = _assessment_for_observation(
        view.issue_id,
        assessed_at,
        observation,
        None,
    )
    previous_fingerprints = (
        view.assessment.get("compared_fingerprints")
        if view.assessment is not None
        else None
    )
    if previous_fingerprints == candidate["compared_fingerprints"]:
        return None
    observation_id = str(occurrence["observation_id"])
    version = normalizer_version(False)
    schema_sha256 = sha256_bytes(
        canonical_json_bytes(
            {
                "kind": "feedback-assessment-v1",
                "compared_fingerprints": candidate["compared_fingerprints"],
            }
        )
    )
    unit_id = normalization_unit_id(
        [observation_id],
        [str(view.revision["revision_id"])],
        schema_sha256,
    )
    return publish_normalization_unit(
        repo,
        normalization_unit_id_value=unit_id,
        observations=[
            {
                "observation_id": observation_id,
                "observation_sha256": str(occurrence["observation_sha256"]),
            }
        ],
        candidate_revision_ids=[str(view.revision["revision_id"])],
        normalizer_schema_sha256=schema_sha256,
        normalizer_version_value=version,
        records=[("assessment", candidate)],
        checkpoint_sha256=None,
    )


def _effective_observation_counts(
    repo: Path,
    entries: list[dict[str, Any]],
) -> tuple[int, int]:
    """effective ingestion receipt から確定済み observation 数を再計算する。"""
    processed = 0
    invalid = 0
    seen: set[str] = set()
    receipts = effective_ingestion_receipts(repo)
    for entry in entries:
        observation_id = str(entry["observation_id"])
        if observation_id in seen:
            continue
        seen.add(observation_id)
        receipt = receipts.get(observation_id)
        if receipt is None:
            continue
        processed += 1
        invalid += int(receipt.get("status") == "invalid")
    return processed, invalid


def _deferred_count(repo: Path, entries: list[dict[str, Any]]) -> int:
    """snapshot 内で effective ingestion receipt がない observation 数を返す。"""
    receipts = effective_ingestion_receipts(repo)
    return sum(str(entry["observation_id"]) not in receipts for entry in entries)


def _is_open(view: IssueView) -> bool:
    """effective disposition が未決定または open/acknowledged か判定する。"""
    if view.disposition is None:
        return True
    return view.disposition.get("state") in {"open", "acknowledged"}


def _is_recurrent_open(
    view: IssueView,
    observations: dict[str, dict[str, Any]],
) -> bool:
    """既定表示上の再発中かつ未終結 issue かを返す。"""
    if not _is_open(view):
        return False
    if view.identity.get("origin") == "machine_rule":
        return _machine_threshold_met(view, observations)
    sessions = {
        occurrence.get("cmoc_session_id")
        for occurrence in view.occurrences
        if isinstance(occurrence.get("cmoc_session_id"), str)
    }
    return len(sessions) >= 2


def _parse_time(value: object) -> datetime | None:
    """RFC 3339 timestamp を UTC datetime として best effort で読む。"""
    if not isinstance(value, str):
        return None
    try:
        return parse_rfc3339(value)
    except ValueError:
        return None


def _machine_threshold_met(
    view: IssueView, observations: dict[str, dict[str, Any]]
) -> bool:
    """初期 allowlist rule の recurrence threshold を型付き context で判定する。"""
    if view.identity.get("origin") != "machine_rule":
        return True
    cutoff = datetime.now(timezone.utc) - timedelta(days=30)
    scopes: set[str] = set()
    agent_calls: set[str] = set()
    rule_id: str | None = None
    for occurrence in view.occurrences:
        observation = observations.get(str(occurrence.get("observation_id")))
        if observation is None:
            continue
        observed_at = _parse_time(observation.get("observed_at"))
        if observed_at is None or observed_at.astimezone(timezone.utc) < cutoff:
            continue
        payload = observation.get("payload")
        context = observation.get("context")
        if not isinstance(payload, dict) or not isinstance(context, dict):
            continue
        rule_id = str(payload.get("rule_id"))
        scope = context.get("cmoc_session_id") or context.get(
            "subcommand_invocation_id"
        )
        if isinstance(scope, str):
            scopes.add(scope)
        agent_call = context.get("agent_call_id")
        if isinstance(agent_call, str):
            agent_calls.add(agent_call)
    if rule_id == "codex.structured_output_validation_exhausted.v1":
        return len(scopes) >= 2 and len(agent_calls) >= 2
    return len(scopes) >= 2


def _visible_issues(
    views: dict[str, IssueView],
    observations: dict[str, dict[str, Any]],
    changed: set[str],
    disposition_changed: set[str],
    show_all: bool,
) -> tuple[list[IssueView], list[IssueView]]:
    """既定 notification boundary に従って表示・抑制 issue を分ける。"""
    visible: list[IssueView] = []
    suppressed: list[IssueView] = []
    for view in views.values():
        threshold = _machine_threshold_met(view, observations)
        if show_all:
            visible.append(view)
        elif view.identity.get("origin") == "machine_rule" and not threshold:
            suppressed.append(view)
        elif (
            view.issue_id in changed
            or _is_recurrent_open(view, observations)
            or (
                view.assessment is not None
                and view.assessment.get("freshness") == "needs_revalidation"
            )
            or view.issue_id in disposition_changed
        ):
            visible.append(view)
    visible.sort(
        key=lambda view: (
            view.issue_id not in changed,
            not _is_recurrent_open(view, observations),
            not (
                view.assessment is not None
                and view.assessment.get("freshness") == "needs_revalidation"
            ),
            view.issue_id not in disposition_changed,
            view.issue_id,
        )
    )
    return visible, suppressed


def _write_report(
    *,
    repo: Path,
    worktree: Path,
    report_id: str,
    generated_at: str,
    snapshot_sha256: str,
    snapshot_count: int,
    processed_count: int,
    deferred_count: int,
    invalid_count: int,
    normalization_agent_call_count: int,
    changed_issue_ids: set[str],
    disposition_changed_issue_ids: set[str],
    recurrent_open_count: int,
    needs_revalidation_count: int,
    suppressed_count: int,
    show_all: bool,
    normalization_unit_ids: list[str],
    state_snapshot_id: str,
    previous_successful_report_id: str | None,
    result: str,
    visible: list[IssueView],
    observations: dict[str, dict[str, Any]],
    partial_error: BaseException | None,
) -> tuple[Path, str, bytes]:
    """deterministic issue view の Markdown publication 内容を準備する。"""
    directory = reports_dir(repo, "feedback")
    directory.mkdir(parents=True, exist_ok=True)
    timestamp_value = timestamp()
    path = directory / f"{timestamp_value}.md"
    if path.exists():
        path = directory / f"{timestamp_value}_{report_id}.md"
    fields: dict[str, object] = {
        "command": "cmoc feedback report",
        "generated_at": generated_at,
        "repo_root": str(repo.resolve()),
        "session_branch": current_branch(worktree),
        "report_snapshot_sha256": snapshot_sha256,
        "report_snapshot_observation_count": snapshot_count,
        "processed_observation_count": processed_count,
        "deferred_observation_count": deferred_count,
        "invalid_observation_count": invalid_count,
        "normalization_agent_call_count": normalization_agent_call_count,
        "new_or_changed_issue_count": len(changed_issue_ids),
        "recurrent_open_issue_count": recurrent_open_count,
        "needs_revalidation_issue_count": needs_revalidation_count,
        "disposition_change_count": len(disposition_changed_issue_ids),
        "suppressed_machine_issue_count": suppressed_count,
        "all": show_all,
        "normalization_unit_ids": normalization_unit_ids,
        "state_snapshot_id": state_snapshot_id,
        "previous_successful_report_id": previous_successful_report_id,
        "result": result,
    }
    lines = [
        "---",
        *[f"{key}: {_yaml(value)}" for key, value in fields.items()],
        "---",
        "# cmoc feedback report",
        "",
    ]
    if partial_error is not None:
        lines.extend(["## Processing warning", "", repr(partial_error), ""])
    if not visible:
        lines.extend(["既定表示の対象 issue はありません。", ""])
    for view in visible:
        observed = sorted(
            (str(item.get("observed_at")) for item in view.occurrences),
            key=lambda value: (
                _parse_time(value) or datetime.min.replace(tzinfo=timezone.utc)
            ),
        )
        assessment = view.assessment or {}
        disposition = (
            str(view.disposition.get("state"))
            if view.disposition is not None
            else "not_disposed"
        )
        sessions = {
            item.get("cmoc_session_id")
            for item in view.occurrences
            if item.get("cmoc_session_id") is not None
        }
        latest_occurrence = max(
            view.occurrences,
            key=lambda item: (
                _parse_time(item.get("observed_at"))
                or datetime.min.replace(tzinfo=timezone.utc),
                str(item.get("observation_id", "")),
            ),
            default={},
        )
        latest_observation = observations.get(
            str(latest_occurrence.get("observation_id", "")), {}
        )
        raw_reference = "unknown"
        latest_observation_id = latest_observation.get("observation_id")
        latest_observed_at = latest_observation.get("observed_at")
        if isinstance(latest_observation_id, str) and isinstance(
            latest_observed_at, str
        ):
            try:
                raw_reference = str(
                    observation_path(repo, latest_observation_id, latest_observed_at)
                )
            except ValueError:
                pass
        representative_evidence = _representative_evidence(latest_observation)
        log_paths = latest_occurrence.get("log_paths", [])
        log_reference = (
            str(log_paths[0])
            if isinstance(log_paths, list) and log_paths
            else "unknown"
        )
        lines.extend(
            [
                f"## {view.issue_id}: {view.revision.get('summary', '')}",
                "",
                f"- 人間の対応候補: {view.revision.get('human_action', '')}",
                f"- occurrence 数: {len(view.occurrences)}",
                f"- affected cmoc session 数: {len(sessions)}",
                f"- 最初の観測日時: {observed[0] if observed else 'unknown'}",
                f"- 最後の観測日時: {observed[-1] if observed else 'unknown'}",
                f"- machine assessment: {assessment.get('presence', 'unknown')} / {assessment.get('freshness', 'unavailable')}",
                f"- human disposition: {disposition}",
                f"- 代表的な evidence: {representative_evidence}",
                f"- issue directory: `{feedback_root(repo) / 'issue' / view.issue_id}`",
                f"- raw observation: `{raw_reference}`",
                f"- log: `{log_reference}`",
                *(
                    ["- 直前の正常 report 後に human disposition が変更されています。"]
                    if view.issue_id in disposition_changed_issue_ids
                    else []
                ),
                "",
            ]
        )
        if show_all:
            lines.extend(
                [
                    "```json",
                    json.dumps(
                        {
                            "identity": view.identity,
                            "revisions": view.revisions,
                            "assessments": view.assessments,
                            "dispositions": view.dispositions,
                            "occurrences": view.occurrences,
                        },
                        ensure_ascii=False,
                        sort_keys=True,
                        indent=2,
                    ),
                    "```",
                    "",
                ]
            )
    content = ("\n".join(lines) + "\n").encode("utf-8")
    return path.resolve(), sha256_bytes(content), content


def _representative_evidence(observation: dict[str, Any]) -> str:
    """report 先頭に載せる一件の evidence を短く整形する。"""
    payload = observation.get("payload")
    if isinstance(payload, dict):
        evidence = payload.get("evidence")
        if isinstance(evidence, list):
            for item in evidence:
                if not isinstance(item, dict):
                    continue
                parts = [str(item.get("kind", "other")), str(item.get("text", ""))]
                if isinstance(item.get("path"), str):
                    parts.append(str(item["path"]))
                if isinstance(item.get("location"), str):
                    parts.append(str(item["location"]))
                return " / ".join(part for part in parts if part)
        summary = payload.get("summary")
        if isinstance(summary, str):
            return summary
    source_event = observation.get("source_event")
    if isinstance(source_event, dict) and isinstance(source_event.get("event_id"), str):
        return f"event {source_event['event_id']}"
    return "unknown"


def _yaml(value: object) -> str:
    """front matter value を YAML 1.2 互換 JSON scalar/flow style にする。"""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(value, ensure_ascii=False, sort_keys=True)
