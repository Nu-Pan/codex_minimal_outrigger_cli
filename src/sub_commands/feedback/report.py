"""`cmoc feedback report` の publication／diagnostic pipeline。

この module は固定済み report cut に対する deterministic processing、必要最小限の
normalization、全 candidate の verification、正常 publication、および incomplete
診断を一つの transaction として扱う。各段階を分散すると中断後の checkpoint 再利用と
固定入力の対応を重複管理するため、サブコマンド固有の状態機械としてまとめる。

対応する oracle file:
- `{{work-root}}/oracle/doc/app_spec/feedback_state.md`
- `{{work-root}}/oracle/doc/app_spec/sub_command/feedback_report.md`
"""

import hashlib
import html
import json
import os
from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from inspect import getsourcefile
from pathlib import Path
from typing import Any

from jsonschema import validators
from jsonschema.exceptions import SchemaError
from oracle.other.struct_doc import render_sd_node_as_markdown

from acp.builder.feedback.normalize_issue import (
    build_feedback_normalize_issue_parameter,
)
from acp.builder.feedback.remediate_issue import (
    build_feedback_remediate_issue_parameter,
)
from cmoc_runtime import (
    CmocError,
    TerminalResult,
    current_branch,
    mark_current_subcommand_interrupted,
    run_cli_subcommand,
    run_codex_exec,
)
from commons.indexing import enable_indexing_preflight
from commons.runtime_feedback_state import (
    ActiveState,
    agent_canonical_key,
    artifact_reference,
    current_generation_artifacts,
    current_pointer_path,
    generation_artifacts,
    issue_id,
    load_active_state,
    machine_aggregate_id,
    machine_canonical_key,
    normalization_checkpoint_path,
    publish_current_pointer,
    publish_generation_artifacts,
    validate_observation_envelope,
    write_checkpoint,
    write_report_cut_manifest,
)
from commons.runtime_feedback_store import (
    _has_symlink_component,
    canonical_json_bytes,
    feedback_root,
    iter_observation_paths,
    mask_feedback_text,
    observation_path,
    parse_rfc3339,
    read_json_object,
    rfc3339_now,
    sha256_bytes,
    write_immutable_bytes,
)
from commons.runtime_logging import current_subcommand_logger
from commons.runtime_paths import reports_dir, timestamp
from commons.runtime_primary_report import update_primary_report_fields
from commons.runtime_results import StructuredOutputValidationIssue

_JsonObject = dict[str, Any]
_REFERENCE_CONTENT_LIMIT = 16 * 1024
_MACHINE_WINDOW_DAYS = 30
_MACHINE_DIGEST_LIMIT = 64


def cmoc_feedback_report_impl() -> None:
    """CLI runtime を通して current feedback report を publication する。"""
    enable_indexing_preflight()
    run_cli_subcommand(
        _cmoc_feedback_report_body,
        command_name="feedback report",
        command_argv=["cmoc", "feedback", "report"],
        # {{work-root}}/oracle/doc/app_spec/subcommand_interruption.md
        interruptible=True,
        doctor_preprocess=False,
        total_steps=7,
    )


def _cmoc_feedback_report_body() -> TerminalResult:
    """self-joining remediation run と publication を実行する。"""
    from .remediation import run_feedback_report

    return run_feedback_report()


def _pending_observations(
    repo: Path,
) -> tuple[list[_JsonObject], dict[str, _JsonObject]]:
    """raw store の全 pending file を canonical validation して固定入力へ変換する。"""
    root = feedback_root(repo) / "observation" / "v1"
    # {{work-root}}/oracle/doc/app_spec/feedback_state.md
    # dangling symlink と symlink 化された親 directory も、空の初期 state と
    # 誤認して publication しない。
    if _has_symlink_component(root) or (root.exists() and not root.is_dir()):
        raise CmocError(
            "feedback observation root が通常 directory ではありません。",
            ["raw observation store を人間が確認してください。"],
            str(root),
        )
    if root.is_dir():
        for path in root.rglob("*"):
            if path.is_dir() and not path.is_symlink():
                continue
            if (
                path.is_symlink()
                or not path.is_file()
                or path.suffix != ".json"
                or not path.name.startswith("fbo_")
            ):
                raise CmocError(
                    "feedback raw store に未定義 artifact があります。",
                    ["raw observation path を人間が確認してください。"],
                    str(path),
                )

    entries: list[_JsonObject] = []
    observations: dict[str, _JsonObject] = {}
    hashes_by_id: dict[str, str] = {}
    validation_errors: list[str] = []
    for path in iter_observation_paths(repo):
        try:
            content = path.read_bytes()
            observation = read_json_object(path)
        except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
            validation_errors.append(f"{path}: {exc}")
            continue
        try:
            canonical_content = canonical_json_bytes(observation)
        except (TypeError, UnicodeError, ValueError) as exc:
            validation_errors.append(
                f"{path}: canonical JSON object ではありません: {exc}"
            )
            continue
        if canonical_content != content:
            validation_errors.append(f"{path}: canonical JSON object ではありません")
            continue
        observation_id_value = observation.get("observation_id")
        observed_at = observation.get("observed_at")
        errors = validate_observation_envelope(observation, expected_repo_root=repo)
        if (
            not isinstance(observation_id_value, str)
            or path.stem != observation_id_value
        ):
            errors.append("/observation_id: file name and payload differ")
        if isinstance(observation_id_value, str) and isinstance(observed_at, str):
            try:
                if observation_path(repo, observation_id_value, observed_at) != path:
                    errors.append("/: observation path does not match observed_at")
            except ValueError as exc:
                errors.append(f"/: {exc}")
        if errors:
            validation_errors.append(f"{path}: {'; '.join(errors)}")
            continue
        digest = sha256_bytes(content)
        previous = hashes_by_id.setdefault(str(observation_id_value), digest)
        if previous != digest:
            validation_errors.append(
                f"{path}: 同じ observation ID に異なる SHA256 があります"
            )
            continue
        observations.setdefault(str(observation_id_value), observation)
        entries.append(
            {
                "observation_id": observation_id_value,
                "path": path.resolve().relative_to(repo.resolve()).as_posix(),
                "sha256": digest,
            }
        )
    if validation_errors:
        raise CmocError(
            "feedback report cut の raw observation validation に失敗しました。",
            [
                "表示された raw observation を修復せず、人間が保存領域を確認してください。"
            ],
            "\n".join(validation_errors),
        )
    entries.sort(key=lambda item: (str(item["observation_id"]), str(item["path"])))
    return entries, observations


def _active_state_input(repo: Path, state: ActiveState) -> _JsonObject | None:
    """cut 開始時の current generation を path/hash reference で固定する。"""
    if state.current is None or state.generation_manifest is None:
        return None
    pointer_path = current_pointer_path(repo)
    issue_references = state.generation_manifest.get("issues")
    aggregate_references = state.generation_manifest.get("machine_aggregates")
    if not isinstance(issue_references, list) or not isinstance(
        aggregate_references, list
    ):
        raise ValueError("validated generation references are missing")
    return {
        "pointer": {
            "value": state.current,
            **artifact_reference(repo, pointer_path),
        },
        "generation_manifest": {
            "path": state.current["generation_manifest_path"],
            "sha256": state.current["generation_manifest_sha256"],
        },
        "issues": issue_references,
        "machine_aggregates": aggregate_references,
    }


def _capture_report_cut_references(
    repo: Path,
    observations: dict[str, _JsonObject],
    active_issues: dict[str, _JsonObject],
) -> list[_JsonObject]:
    """agent に許可する observation と current repository reference を固定する。"""
    references: dict[str, _JsonObject] = {}
    path_subjects: dict[Path, set[str]] = {}

    # raw observation 自体は current verdict の根拠ではない別種 reference とする。
    for observation_id_value, observation in sorted(observations.items()):
        payload = observation.get("payload")
        summary = payload.get("summary") if isinstance(payload, dict) else None
        evidence = payload.get("evidence") if isinstance(payload, dict) else []
        reference_id = f"obs:{observation_id_value}"
        references[reference_id] = {
            "reference_id": reference_id,
            "kind": "observation",
            "subjects": [observation_id_value],
            "observation_id": observation_id_value,
            "summary": summary if isinstance(summary, str) else "",
            "evidence": evidence if isinstance(evidence, list) else [],
        }
        for path in _observation_reference_paths(repo, observation):
            path_subjects.setdefault(path, set()).add(observation_id_value)

    # active issue が保持する stable target を今回の cut で再取得する。
    for current_issue_id, issue in sorted(active_issues.items()):
        targets = issue.get("reference_targets")
        if not isinstance(targets, list):
            continue
        for target in targets:
            if not isinstance(target, dict) or not isinstance(target.get("path"), str):
                continue
            candidate = _repository_path(repo, target["path"])
            if candidate is not None:
                path_subjects.setdefault(candidate, set()).add(current_issue_id)
        verification = issue.get("verification")
        current_evidence = (
            verification.get("current_evidence")
            if isinstance(verification, dict)
            else None
        )
        if isinstance(current_evidence, list):
            for evidence in current_evidence:
                if not isinstance(evidence, dict) or not isinstance(
                    evidence.get("path"), str
                ):
                    continue
                candidate = _repository_path(repo, evidence["path"])
                if candidate is not None:
                    path_subjects.setdefault(candidate, set()).add(current_issue_id)

    # path ごとに一度だけ current state を取得し、複数 candidate の subject を共有する。
    for path, subjects in sorted(path_subjects.items(), key=lambda item: str(item[0])):
        reference = _capture_repository_reference(repo, path, sorted(subjects))
        references[str(reference["reference_id"])] = reference
    return [references[key] for key in sorted(references)]


def _observation_reference_paths(repo: Path, observation: _JsonObject) -> list[Path]:
    """raw observation が既に拘束した repository 内 current target を返す。"""
    paths: set[Path] = set()
    fingerprints = observation.get("evidence_fingerprints")
    if isinstance(fingerprints, list):
        for fingerprint in fingerprints:
            if isinstance(fingerprint, dict) and isinstance(
                fingerprint.get("normalized_path"), str
            ):
                candidate = _repository_path(repo, fingerprint["normalized_path"])
                if candidate is not None:
                    paths.add(candidate)
    source_event = observation.get("source_event")
    if isinstance(source_event, dict) and isinstance(source_event.get("log_path"), str):
        candidate = _repository_path(repo, source_event["log_path"])
        if candidate is not None:
            paths.add(candidate)
    return sorted(paths)


def _repository_path(repo: Path, value: str) -> Path | None:
    """absolute／repository-relative value を repository 内の path へ制限する。"""
    repository = repo.resolve(strict=False)
    raw = Path(value)
    candidate = (
        Path(os.path.abspath(raw))
        if raw.is_absolute()
        else Path(os.path.abspath(repository / raw))
    )
    if candidate != repository and repository not in candidate.parents:
        return None
    try:
        resolved = candidate.resolve(strict=False)
    except (OSError, RuntimeError, ValueError):
        return None
    if resolved != repository and repository not in resolved.parents:
        return None
    return candidate


def _capture_repository_reference(
    repo: Path, path: Path, subjects: list[str]
) -> _JsonObject:
    """repository path の content または typed fingerprint を secret-safe に固定する。"""
    relative = path.relative_to(repo.resolve(strict=False)).as_posix()
    reference_id = f"ref:{hashlib.sha256(relative.encode('utf-8')).hexdigest()[:24]}"
    base: _JsonObject = {
        "reference_id": reference_id,
        "subjects": subjects,
        "path": relative,
    }
    try:
        if path.is_symlink():
            return {
                **base,
                "kind": "current_fingerprint",
                "state": "unreadable",
                "sha256": None,
            }
        if not path.exists():
            return {
                **base,
                "kind": "current_fingerprint",
                "state": "missing",
                "sha256": None,
            }
        if not path.is_file():
            return {
                **base,
                "kind": "current_fingerprint",
                "state": "not_file",
                "sha256": None,
            }
        content = path.read_bytes()
    except OSError:
        return {
            **base,
            "kind": "current_fingerprint",
            "state": "unreadable",
            "sha256": None,
        }
    digest = sha256_bytes(content)
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        return {
            **base,
            "kind": "current_fingerprint",
            "state": "hashed",
            "sha256": digest,
        }
    masked_text = mask_feedback_text(text)
    return {
        **base,
        "kind": "repository_content",
        "state": "hashed",
        "sha256": digest,
        # {{work-root}}/oracle/doc/app_spec/feedback_state.md
        # private key block が capture 上限をまたいでも、先に全体を mask して
        # report cut の bounded content へ secret の断片を保存しない。
        "content": masked_text[:_REFERENCE_CONTENT_LIMIT],
        "truncated": len(text) > _REFERENCE_CONTENT_LIMIT,
    }


def _processing_versions() -> _JsonObject:
    """builder、schema、および deterministic processing rule の content hash を返す。"""
    normalize_builder = _builder_source_path(build_feedback_normalize_issue_parameter)
    verify_builder = _builder_source_path(build_feedback_remediate_issue_parameter)
    # 動的 code fence を構築する canonical renderer も checkpoint version に含める。
    prompt_renderer = _builder_source_path(render_sd_node_as_markdown)
    normalize_schema = normalize_builder.with_suffix(".json")
    verify_schema = verify_builder.with_suffix(".json")
    module_path = Path(__file__)
    state_path = module_path.parents[2] / "commons" / "runtime_feedback_state.py"
    return {
        "normalization_builder": _builder_version_hash(
            normalize_builder,
            (prompt_renderer,),
        ),
        "normalization_schema": sha256_bytes(normalize_schema.read_bytes()),
        "remediation_builder": _builder_version_hash(
            verify_builder,
            (prompt_renderer,),
        ),
        "remediation_schema": sha256_bytes(verify_schema.read_bytes()),
        "deterministic_processing": _combined_file_hash(
            [
                module_path,
                state_path,
                module_path.with_name("remediation.py"),
                module_path.with_name("recovery.py"),
                state_path.with_name("runtime_feedback_run_state.py"),
                state_path.with_name("runtime_feedback_intake.py"),
            ]
        ),
    }


def _builder_source_path(builder: Callable[..., object]) -> Path:
    """builder の実装 file path を検証用 hash の入力として返す。"""
    source = getsourcefile(builder)
    if source is None:
        raise ValueError("builder source path is unavailable")
    return Path(source)


def _builder_version_hash(
    source: Path,
    dependency_sources: tuple[Path, ...] = (),
) -> str:
    """builder と prompt 構築依存の変更を checkpoint version へ反映する。"""
    sources = {source, *dependency_sources}
    if len(sources) == 1:
        return sha256_bytes(source.read_bytes())
    return _combined_file_hash(list(sources))


def _combined_file_hash(paths: list[Path]) -> str:
    """path と content の canonical 順序から処理実装 version を返す。"""
    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: str(item)):
        digest.update(str(path).encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _read_cut_observations(repo: Path, manifest: _JsonObject) -> dict[str, _JsonObject]:
    """cut manifest が固定した raw byte 列を再検証し、完全一致 duplicate を除く。"""
    inputs = manifest.get("inputs")
    entries = inputs.get("observations") if isinstance(inputs, dict) else None
    if not isinstance(entries, list):
        raise ValueError("report cut observations must be an array")
    observations: dict[str, _JsonObject] = {}
    hashes: dict[str, str] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("report cut observation entry must be an object")
        path = repo / str(entry.get("path"))
        content = path.read_bytes()
        digest = sha256_bytes(content)
        if digest != entry.get("sha256"):
            raise CmocError(
                "feedback report cut の raw observation hash が変化しました。",
                ["raw observation と report cut manifest を人間が確認してください。"],
                str(path),
            )
        observation = read_json_object(path)
        if canonical_json_bytes(observation) != content:
            raise CmocError(
                "feedback report cut の raw observation が canonical JSON ではありません。",
                ["raw observation を人間が確認してください。"],
                str(path),
            )
        errors = validate_observation_envelope(observation, expected_repo_root=repo)
        observation_id_value = str(entry.get("observation_id"))
        if observation.get("observation_id") != observation_id_value:
            errors.append("/observation_id: manifest and payload differ")
        observed_at = observation.get("observed_at")
        if isinstance(observed_at, str):
            try:
                if observation_path(repo, observation_id_value, observed_at) != path:
                    errors.append("/: observation path does not match observed_at")
            except ValueError as exc:
                errors.append(f"/: {exc}")
        if errors:
            raise CmocError(
                "feedback report cut の raw observation schema が不正です。",
                [
                    "raw observation を処理済みにせず、人間が保存領域を確認してください。"
                ],
                f"path: {path}\n" + "\n".join(errors),
            )
        previous_hash = hashes.setdefault(observation_id_value, digest)
        if previous_hash != digest:
            raise CmocError(
                "同じ feedback observation ID に異なる内容があります。",
                ["重複 raw observation を人間が確認してください。"],
                observation_id_value,
            )
        observations.setdefault(observation_id_value, observation)
    return observations


def _build_candidates(
    repo: Path,
    worktree: Path,
    manifest: _JsonObject,
    observations: dict[str, _JsonObject],
    state: ActiveState,
    *,
    previous_candidates: dict[str, _JsonObject] | None = None,
    previous_aggregates: dict[str, _JsonObject] | None = None,
    observed_at: str | None = None,
) -> tuple[dict[str, _JsonObject], dict[str, _JsonObject]]:
    """deterministic processing と必要な同一性判断だけで candidate 集合を作る。"""
    candidates = (
        previous_candidates
        if previous_candidates is not None
        else {
            current_issue_id: _candidate_from_active(issue)
            for current_issue_id, issue in state.issues.items()
        }
    )
    inputs = manifest["inputs"]
    assert isinstance(inputs, dict)

    # machine observation は canonical key と recurrence rule だけで先に集約する。
    machine_observations: dict[str, list[_JsonObject]] = {}
    agent_observations: list[_JsonObject] = []
    for observation in observations.values():
        if observation.get("source") == "machine_rule":
            machine_observations.setdefault(
                machine_canonical_key(observation), []
            ).append(observation)
        else:
            agent_observations.append(observation)
    machine_aggregates = _process_machine_observations(
        repo,
        {**manifest, "cut_at": observed_at or manifest["cut_at"]},
        candidates,
        previous_aggregates
        if previous_aggregates is not None
        else state.machine_aggregates,
        machine_observations,
    )

    # agent observation は observed_at と ID の canonical order で一件ずつ処理する。
    for observation in sorted(
        agent_observations,
        key=lambda item: (
            parse_rfc3339(str(item["observed_at"])),
            str(item["observation_id"]),
        ),
    ):
        exact, comparison = _agent_comparison_candidates(
            observation,
            candidates,
            current_cut_fingerprint_pairs=_report_cut_fingerprint_pairs(
                repo, manifest, observation
            ),
        )
        selected: _JsonObject | None = exact
        if selected is None and comparison:
            selected_id = _normalize_issue_identity(
                repo, worktree, manifest, observation, comparison
            )
            if selected_id is not None:
                selected = candidates[selected_id]
        if selected is None:
            observation_id_value = str(observation["observation_id"])
            canonical_key = agent_canonical_key(observation_id_value)
            selected = _new_candidate(observation, canonical_key)
            _insert_candidate(candidates, selected)
        _merge_observation(repo, selected, observation)

    # candidate ごとに許可する cut reference を固定済み subject から機械選択する。
    references = inputs.get("references")
    assert isinstance(references, list)
    for candidate in candidates.values():
        subjects = {
            str(candidate["candidate_id"]),
            *[str(value) for value in candidate.get("source_observation_ids", [])],
        }
        candidate["reference_ids"] = sorted(
            str(reference["reference_id"])
            for reference in references
            if isinstance(reference, dict)
            and isinstance(reference.get("subjects"), list)
            and subjects.intersection(str(value) for value in reference["subjects"])
        )
    return candidates, machine_aggregates


def _candidate_from_active(issue: _JsonObject) -> _JsonObject:
    """active issue record を今回再検証する transient candidate へ変換する。"""
    return {
        "schema_version": 1,
        "candidate_id": issue["issue_id"],
        "origin": issue["origin"],
        "canonical_key": issue["canonical_key"],
        "category": issue["category"],
        "summary": issue["summary"],
        "impact": issue["impact"],
        "occurrence_count": issue["occurrence_count"],
        "affected_session_count": issue["affected_session_count"],
        "session_digest": issue["session_digest"],
        "first_observed_at": issue["first_observed_at"],
        "last_observed_at": issue["last_observed_at"],
        "representative_evidence": issue["representative_evidence"],
        "reference_targets": issue["reference_targets"],
        "latest_fingerprints": issue["latest_fingerprints"],
        "machine_state": issue["machine_state"],
        "source_observation_ids": [],
        "deduplication_hints": [],
        "reference_ids": [],
    }


def _new_candidate(observation: _JsonObject, canonical_key: str) -> _JsonObject:
    """一 observation から未集約の transient candidate を作る。"""
    payload = observation["payload"]
    assert isinstance(payload, dict)
    return {
        "schema_version": 1,
        "candidate_id": issue_id(canonical_key),
        "origin": observation["source"],
        "canonical_key": canonical_key,
        "category": payload["category"],
        "summary": payload["summary"],
        "impact": payload["impact"],
        "occurrence_count": 0,
        "affected_session_count": 0,
        "session_digest": {"values": [], "saturated": False},
        "first_observed_at": observation["observed_at"],
        "last_observed_at": observation["observed_at"],
        "representative_evidence": [],
        "reference_targets": [],
        "latest_fingerprints": [],
        "machine_state": None,
        "source_observation_ids": [],
        "deduplication_hints": [],
        "reference_ids": [],
    }


def _insert_candidate(
    candidates: dict[str, _JsonObject], candidate: _JsonObject
) -> None:
    """異なる canonical key の issue ID collision を publication 前に停止する。"""
    candidate_id_value = candidate.get("candidate_id")
    canonical_key = candidate.get("canonical_key")
    if not isinstance(candidate_id_value, str) or not isinstance(canonical_key, str):
        raise ValueError("candidate identity is malformed")
    previous = candidates.get(candidate_id_value)
    if previous is not None and previous.get("canonical_key") != canonical_key:
        raise CmocError(
            "feedback issue ID collision を検出しました。",
            [
                "異なる canonical key に同じ issue ID を割り当てず、report を停止しました。"
            ],
            f"issue_id: {candidate_id_value}\n"
            f"existing canonical_key: {previous.get('canonical_key')!r}\n"
            f"new canonical_key: {canonical_key!r}",
        )
    candidates[candidate_id_value] = candidate


def _merge_observation(
    repo: Path, candidate: _JsonObject, observation: _JsonObject
) -> None:
    """一意な raw observation を compact candidate aggregate へ統合する。"""
    observation_id_value = str(observation["observation_id"])
    source_ids = candidate.setdefault("source_observation_ids", [])
    assert isinstance(source_ids, list)
    if observation_id_value in source_ids:
        return
    source_ids.append(observation_id_value)
    source_ids.sort()
    candidate["occurrence_count"] = int(candidate["occurrence_count"]) + 1
    observed_at = str(observation["observed_at"])
    observed_time = parse_rfc3339(observed_at)
    if observed_time < parse_rfc3339(str(candidate["first_observed_at"])):
        candidate["first_observed_at"] = observed_at
    is_latest_observation = observed_time >= parse_rfc3339(
        str(candidate["last_observed_at"])
    )
    if is_latest_observation:
        candidate["last_observed_at"] = observed_at
        payload = observation["payload"]
        assert isinstance(payload, dict)
        candidate["summary"] = payload["summary"]
        candidate["impact"] = payload["impact"]

    # session digest と evidence は canonical order／fixed bound だけで保持対象を決める。
    context = observation.get("context")
    session_id_value = (
        context.get("cmoc_session_id") if isinstance(context, dict) else None
    )
    if isinstance(session_id_value, str):
        digest = hashlib.sha256(session_id_value.encode("utf-8")).hexdigest()
        session_digest = candidate["session_digest"]
        assert isinstance(session_digest, dict)
        values = session_digest["values"]
        assert isinstance(values, list)
        if digest not in values:
            if len(values) < 64:
                values.append(digest)
                values.sort()
            else:
                session_digest["saturated"] = True
        candidate["affected_session_count"] = max(
            int(candidate["affected_session_count"]), len(values)
        )
    payload = observation.get("payload")
    if isinstance(payload, dict):
        evidence = payload.get("evidence")
        if isinstance(evidence, list):
            candidate["representative_evidence"] = _bounded_objects(
                [
                    *candidate.get("representative_evidence", []),
                    *[item for item in evidence if isinstance(item, dict)],
                ],
                5,
            )
        hint = payload.get("deduplication_hint")
        if isinstance(hint, str):
            hints = candidate.setdefault("deduplication_hints", [])
            assert isinstance(hints, list)
            if hint not in hints:
                hints.append(hint)
                hints.sort()
    candidate["reference_targets"] = _bounded_objects(
        [
            *candidate.get("reference_targets", []),
            *_observation_reference_targets(repo, observation),
        ],
        5,
    )
    fingerprints = observation.get("evidence_fingerprints")
    if is_latest_observation and isinstance(fingerprints, list):
        candidate["latest_fingerprints"] = _bounded_objects(
            [item for item in fingerprints if isinstance(item, dict)], 5
        )


def _observation_reference_targets(
    repo: Path, observation: _JsonObject
) -> list[_JsonObject]:
    """次回 cut で再取得できる stable repository target を抽出する。"""
    targets: list[_JsonObject] = []
    payload = observation.get("payload")
    if isinstance(payload, dict) and isinstance(payload.get("evidence"), list):
        for evidence in payload["evidence"]:
            if not isinstance(evidence, dict) or not isinstance(
                evidence.get("path"), str
            ):
                continue
            candidate = _repository_path(repo, evidence["path"])
            if candidate is not None:
                targets.append(
                    {
                        "path": candidate.relative_to(repo.resolve()).as_posix(),
                        "kind": evidence.get("kind"),
                        "location": evidence.get("location"),
                    }
                )
    source_event = observation.get("source_event")
    if isinstance(source_event, dict) and isinstance(source_event.get("log_path"), str):
        candidate = _repository_path(repo, source_event["log_path"])
        if candidate is not None:
            targets.append(
                {
                    "path": candidate.relative_to(repo.resolve()).as_posix(),
                    "kind": "log",
                    "location": source_event.get("event_id"),
                }
            )
    return targets


def _bounded_objects(values: list[_JsonObject], limit: int) -> list[_JsonObject]:
    """object を canonical byte 列で deduplicate し固定上限へ収める。"""
    by_content = {canonical_json_bytes(value): value for value in values}
    return [by_content[key] for key in sorted(by_content)[:limit]]


def _agent_comparison_candidates(
    observation: _JsonObject,
    candidates: dict[str, _JsonObject],
    *,
    current_cut_fingerprint_pairs: list[tuple[str, str, str | None]] | None = None,
) -> tuple[_JsonObject | None, list[_JsonObject]]:
    """category、evidence subject、fingerprint、hint で比較候補を機械的に絞る。"""
    payload = observation["payload"]
    assert isinstance(payload, dict)
    category = payload.get("category")
    hint = payload.get("deduplication_hint")
    current_fingerprints = _fingerprint_pairs(observation.get("evidence_fingerprints"))
    current_cut_matches_observation = (
        current_cut_fingerprint_pairs is not None
        and len(current_cut_fingerprint_pairs) == len(current_fingerprints)
        and all(
            state == "hashed" for _path, state, _sha256 in current_cut_fingerprint_pairs
        )
        and [(path, sha256) for path, _state, sha256 in current_cut_fingerprint_pairs]
        == current_fingerprints
    )
    current_subjects = _observation_evidence_subjects(observation)
    exact: list[_JsonObject] = []
    comparison: list[_JsonObject] = []
    for candidate in candidates.values():
        if candidate.get("category") != category:
            continue
        previous_fingerprints = _fingerprint_pairs(candidate.get("latest_fingerprints"))
        previous_subjects = _candidate_evidence_subjects(candidate)
        exact_match = (
            bool(current_fingerprints)
            and all(digest is not None for _path, digest in current_fingerprints)
            and current_fingerprints == previous_fingerprints
            and current_cut_matches_observation
            and bool(current_subjects)
            and current_subjects.issubset(previous_subjects)
        )
        hint_match = isinstance(hint, str) and hint in candidate.get(
            "deduplication_hints", []
        )
        if exact_match:
            exact.append(candidate)
        if current_subjects.intersection(previous_subjects) or hint_match:
            comparison.append(candidate)
    return (exact[0] if len(exact) == 1 else None), comparison


def _report_cut_fingerprint_pairs(
    repo: Path, manifest: _JsonObject, observation: _JsonObject
) -> list[tuple[str, str, str | None]]:
    """observation subject に紐付く report cut current fingerprint を返す。"""
    inputs = manifest.get("inputs")
    references = inputs.get("references") if isinstance(inputs, dict) else None
    observation_id_value = observation.get("observation_id")
    if not isinstance(references, list) or not isinstance(observation_id_value, str):
        return []
    current: dict[str, tuple[str, str | None]] = {}
    for reference in references:
        if not isinstance(reference, dict) or reference.get("kind") not in {
            "repository_content",
            "current_fingerprint",
        }:
            continue
        subjects = reference.get("subjects")
        path = reference.get("path")
        state = reference.get("state")
        sha256 = reference.get("sha256")
        if (
            not isinstance(subjects, list)
            or observation_id_value not in subjects
            or not isinstance(path, str)
            or not isinstance(state, str)
            or (sha256 is not None and not isinstance(sha256, str))
        ):
            continue
        candidate = _repository_path(repo, path)
        if candidate is None:
            continue
        current[str(candidate)] = (state, sha256)

    fingerprints = observation.get("evidence_fingerprints")
    if not isinstance(fingerprints, list):
        return []
    result: list[tuple[str, str, str | None]] = []
    for fingerprint in fingerprints:
        if not isinstance(fingerprint, dict):
            continue
        path = fingerprint.get("normalized_path")
        state = fingerprint.get("state")
        sha256 = fingerprint.get("sha256")
        if (
            not isinstance(path, str)
            or not isinstance(state, str)
            or (sha256 is not None and not isinstance(sha256, str))
        ):
            continue
        candidate = _repository_path(repo, path)
        if candidate is None:
            continue
        current_value = current.get(str(candidate))
        if current_value is not None:
            result.append((str(candidate), current_value[0], current_value[1]))
    return sorted(set(result))


def _observation_evidence_subjects(
    observation: _JsonObject,
) -> set[tuple[str, str]]:
    """observation の path evidence を subject type と repository-relative path へ揃える。"""
    payload = observation.get("payload")
    context = observation.get("context")
    fingerprints = observation.get("evidence_fingerprints")
    if (
        not isinstance(payload, dict)
        or not isinstance(payload.get("evidence"), list)
        or not isinstance(context, dict)
        or not isinstance(context.get("repo_root"), str)
        or not isinstance(fingerprints, list)
    ):
        return set()
    repo_root = Path(str(context["repo_root"]))
    evidence = payload["evidence"]
    subjects: set[tuple[str, str]] = set()
    for fingerprint in fingerprints:
        if not isinstance(fingerprint, dict):
            continue
        index = fingerprint.get("evidence_index")
        normalized_path = fingerprint.get("normalized_path")
        if (
            type(index) is not int
            or not isinstance(normalized_path, str)
            or index < 0
            or index >= len(evidence)
        ):
            continue
        evidence_item = evidence[index]
        if not isinstance(evidence_item, dict) or not isinstance(
            evidence_item.get("kind"), str
        ):
            continue
        try:
            relative_path = Path(normalized_path).relative_to(repo_root).as_posix()
        except ValueError:
            relative_path = normalized_path
        subjects.add((relative_path, evidence_item["kind"]))
    return subjects


def _candidate_evidence_subjects(candidate: _JsonObject) -> set[tuple[str, str]]:
    """candidate が保持する stable target から subject type と path を返す。"""
    targets = candidate.get("reference_targets")
    if not isinstance(targets, list):
        return set()
    return {
        (str(target["path"]), str(target["kind"]))
        for target in targets
        if isinstance(target, dict)
        and isinstance(target.get("path"), str)
        and isinstance(target.get("kind"), str)
    }


def _fingerprint_pairs(value: object) -> list[tuple[str, str | None]]:
    """fingerprint array を path/hash の canonical pair へ変換する。"""
    if not isinstance(value, list):
        return []
    pairs = [
        (str(item["normalized_path"]), item.get("sha256"))
        for item in value
        if isinstance(item, dict) and isinstance(item.get("normalized_path"), str)
    ]
    return sorted(set(pairs))


def _normalize_issue_identity(
    repo: Path,
    worktree: Path,
    manifest: _JsonObject,
    observation: _JsonObject,
    candidates: list[_JsonObject],
) -> str | None:
    """曖昧な agent observation の同一性だけを checkpoint 付きで判断する。"""
    candidate_payload = [
        {
            key: candidate[key]
            for key in (
                "candidate_id",
                "origin",
                "category",
                "summary",
                "impact",
                "representative_evidence",
                "reference_targets",
                "latest_fingerprints",
            )
        }
        for candidate in sorted(candidates, key=lambda item: str(item["candidate_id"]))
    ]
    # {{work-root}}/oracle/doc/app_spec/sub_command/feedback_report.md
    # deduplication hint は候補検索だけで使い、issue identity の根拠として
    # normalization agent へ渡さない。
    from commons.runtime_feedback_store import reporter_payload_view

    normalization_observation = {
        **observation,
        "compatibility": {
            "source_schema_version": observation["payload"]["schema_version"],
            "view_schema_version": 2,
            "rule": "reporter-input-v1-to-v2"
            if observation["payload"]["schema_version"] == 1
            else "identity",
        },
        "payload": {
            key: value
            for key, value in reporter_payload_view(observation["payload"]).items()
            if key != "deduplication_hint"
        },
    }
    parameter = build_feedback_normalize_issue_parameter(
        json.dumps(normalization_observation, ensure_ascii=False, sort_keys=True),
        json.dumps(candidate_payload, ensure_ascii=False, sort_keys=True),
        worktree,
    )
    schema_path = parameter.structured_output_schema_path
    assert schema_path is not None
    allowed = {str(candidate["candidate_id"]) for candidate in candidates}
    input_value = {
        "observation": normalization_observation,
        "candidates": candidate_payload,
    }
    input_sha256 = sha256_bytes(canonical_json_bytes(input_value))
    observation_id_value = str(observation["observation_id"])

    def postcondition(
        output: Any, changed_paths: frozenset[str]
    ) -> tuple[StructuredOutputValidationIssue, ...]:
        """候補外 issue ID を deterministic correction 対象にする。"""
        del changed_paths
        return _normalization_output_issues(output, allowed)

    result = run_codex_exec(
        parameter,
        root=repo,
        purpose="feedback issue identity normalization",
        structured_output_postcondition=postcondition,
    )
    if (
        not isinstance(result.output_json, dict)
        or not _structured_output_matches_schema(result.output_json, schema_path)
        or _normalization_output_issues(result.output_json, allowed)
    ):
        raise ValueError("normalization output does not satisfy its contract")
    output_sha256 = sha256_bytes(canonical_json_bytes(result.output_json))
    checkpoint = {
        "schema_version": 1,
        "kind": "normalization",
        "report_cut_id": manifest["report_cut_id"],
        "candidate_id": observation_id_value,
        "input_sha256": input_sha256,
        "builder_sha256": manifest["inputs"]["versions"]["normalization_builder"],
        "schema_sha256": sha256_bytes(schema_path.read_bytes()),
        "structured_output": result.output_json,
        "output_sha256": output_sha256,
    }
    path = normalization_checkpoint_path(
        repo, str(manifest["report_cut_id"]), observation_id_value
    )
    reference = write_checkpoint(repo, path, checkpoint)
    _record_checkpoint(
        repo,
        manifest,
        "normalization_checkpoints",
        "observation_id",
        observation_id_value,
        reference,
    )
    structured_output = checkpoint.get("structured_output")
    if not isinstance(structured_output, dict):
        raise ValueError("normalization checkpoint output must be an object")
    result_value = structured_output.get("result")
    if not isinstance(result_value, dict):
        raise ValueError("normalization result must be an object")
    return (
        str(result_value["existing_issue_id"])
        if result_value.get("decision") == "existing"
        else None
    )


def _normalization_output_issues(
    output: object, allowed: set[str]
) -> tuple[StructuredOutputValidationIssue, ...]:
    """normalization result が入力 candidate だけを選ぶか検査する。"""
    if not isinstance(output, dict) or not isinstance(output.get("result"), dict):
        return ()
    result = output["result"]
    assert isinstance(result, dict)
    existing_id = result.get("existing_issue_id")
    if result.get("decision") == "existing" and existing_id not in allowed:
        return (
            StructuredOutputValidationIssue(
                "candidate issue ID",
                "$.result.existing_issue_id",
                f"one of {sorted(allowed)!r}",
                repr(existing_id),
            ),
        )
    return ()


def _record_checkpoint(
    repo: Path,
    manifest: _JsonObject,
    list_name: str,
    id_name: str,
    id_value: str,
    reference: _JsonObject,
) -> None:
    """formal checkpoint reference を manifest へ canonical order で追加する。"""
    processing = manifest["processing"]
    assert isinstance(processing, dict)
    entries = processing[list_name]
    assert isinstance(entries, list)
    entry = {id_name: id_value, **reference}
    if not any(
        isinstance(item, dict) and item.get(id_name) == id_value for item in entries
    ):
        entries.append(entry)
        entries.sort(key=lambda item: str(item[id_name]))
    write_report_cut_manifest(repo, manifest)


def _structured_output_matches_schema(output: _JsonObject, schema_path: Path) -> bool:
    """checkpoint output を正本 Structured Output schema で再検証する。"""
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        validator_class = validators.validator_for(schema)
        validator_class.check_schema(schema)
        return not tuple(validator_class(schema).iter_errors(output))
    except (OSError, UnicodeError, json.JSONDecodeError, SchemaError, TypeError):
        return False


def _process_machine_observations(
    repo: Path,
    manifest: _JsonObject,
    candidates: dict[str, _JsonObject],
    previous_aggregates: dict[str, _JsonObject],
    observation_groups: dict[str, list[_JsonObject]],
) -> dict[str, _JsonObject]:
    """recurrence window／threshold を適用し、candidate と bounded aggregate を分ける。"""
    active_by_key = {
        str(candidate["canonical_key"]): candidate
        for candidate in candidates.values()
        if candidate.get("origin") == "machine_rule"
    }
    aggregates: dict[str, _JsonObject] = {}
    all_keys = sorted(
        set(previous_aggregates) | set(observation_groups) | set(active_by_key)
    )
    for canonical_key in all_keys:
        active_candidate = active_by_key.get(canonical_key)
        previous = previous_aggregates.get(canonical_key)
        if (
            previous is None
            and active_candidate is not None
            and isinstance(active_candidate.get("machine_state"), dict)
        ):
            previous = active_candidate["machine_state"]
        observations = sorted(
            observation_groups.get(canonical_key, []),
            key=lambda item: (
                parse_rfc3339(str(item["observed_at"])),
                str(item["observation_id"]),
            ),
        )
        aggregate = _merge_machine_aggregate(
            repo,
            previous,
            observations,
            str(manifest["cut_at"]),
            canonical_key,
        )
        if aggregate is None:
            # current active issue は新しい report cut でも必ず verification する。
            # window 外になった state は次の aggregate として保存せず、active issue
            # の最後の threshold state は verification 中も表現可能なまま保持する。
            continue
        threshold_met = _machine_threshold_met(aggregate)
        if active_candidate is not None:
            if not threshold_met:
                # 部分的に window 外となった aggregate も threshold 未満 state として
                # active issue へ上書きせず、unresolved の再検証結果だけを反映する。
                continue
            for observation in observations:
                _merge_observation(repo, active_candidate, observation)
            _apply_machine_aggregate_to_candidate(active_candidate, aggregate)
            continue
        if threshold_met:
            if not observations:
                raise ValueError(
                    "threshold aggregate without an issue candidate source"
                )
            candidate = _new_candidate(observations[0], canonical_key)
            for observation in observations:
                _merge_observation(repo, candidate, observation)
            _apply_machine_aggregate_to_candidate(candidate, aggregate)
            _insert_candidate(candidates, candidate)
            continue
        aggregates[canonical_key] = aggregate
    return aggregates


def _merge_machine_aggregate(
    repo: Path,
    previous: _JsonObject | None,
    observations: list[_JsonObject],
    cut_at: str,
    canonical_key: str,
) -> _JsonObject | None:
    """30 日 window 内の machine recurrence を daily bounded buckets へ集約する。"""
    cut_time = parse_rfc3339(cut_at).astimezone(timezone.utc)
    cutoff = cut_time - timedelta(days=_MACHINE_WINDOW_DAYS)
    buckets_by_day: dict[str, _JsonObject] = {}
    representative: list[_JsonObject] = []
    fingerprints: list[_JsonObject] = []
    metadata: _JsonObject = {}
    previous_buckets_truncated = False
    if previous is not None:
        metadata = dict(previous)
        previous_buckets = previous.get("time_buckets")
        if not isinstance(previous_buckets, list):
            raise ValueError("machine aggregate time_buckets must be an array")
        for bucket in previous_buckets:
            if not isinstance(bucket, dict) or not isinstance(bucket.get("day"), str):
                raise ValueError("machine aggregate bucket is malformed")
            first = bucket.get("first_observed_at")
            last = bucket.get("last_observed_at")
            if not isinstance(first, str) or not isinstance(last, str):
                raise ValueError("machine aggregate bucket timestamps are malformed")
            if parse_rfc3339(first) >= cutoff and parse_rfc3339(last) <= cut_time:
                copied = json.loads(json.dumps(bucket, ensure_ascii=False))
                assert isinstance(copied, dict)
                copied.setdefault("scope_saturated", False)
                copied.setdefault("agent_call_saturated", False)
                buckets_by_day[str(bucket["day"])] = copied
            else:
                # A daily bucket that straddles the moving boundary cannot be
                # split without retaining individual occurrences.  Drop the
                # whole bucket so expired occurrences are never counted.
                previous_buckets_truncated = True
        if not previous_buckets_truncated:
            representative.extend(
                item
                for item in previous.get("representative_evidence", [])
                if isinstance(item, dict)
            )
            fingerprints.extend(
                item
                for item in previous.get("latest_fingerprints", [])
                if isinstance(item, dict)
            )

    # 新しい occurrence を日単位 bucket へ加え、個別 occurrence record は残さない。
    for observation in observations:
        observed_at = str(observation["observed_at"])
        occurred = parse_rfc3339(observed_at).astimezone(timezone.utc)
        if occurred < cutoff or occurred > cut_time:
            continue
        payload = observation["payload"]
        context = observation["context"]
        assert isinstance(payload, dict) and isinstance(context, dict)
        metadata = {
            "rule_id": payload["rule_id"],
            "category": payload["category"],
            "summary": payload["summary"],
            "impact": payload["impact"],
            "human_action": payload["human_action"],
        }
        day = occurred.strftime("%Y-%m-%d")
        bucket = buckets_by_day.setdefault(
            day,
            {
                "day": day,
                "count": 0,
                "first_observed_at": observed_at,
                "last_observed_at": observed_at,
                "scope_digest": [],
                "agent_call_digest": [],
                "scope_saturated": False,
                "agent_call_saturated": False,
            },
        )
        bucket["count"] = int(bucket["count"]) + 1
        if occurred < parse_rfc3339(str(bucket["first_observed_at"])):
            bucket["first_observed_at"] = observed_at
        if occurred > parse_rfc3339(str(bucket["last_observed_at"])):
            bucket["last_observed_at"] = observed_at
        scope = context.get("cmoc_session_id") or context.get(
            "subcommand_invocation_id"
        )
        if isinstance(scope, str):
            if _update_dimension_digest(bucket["scope_digest"], scope, observed_at):
                bucket["scope_saturated"] = True
        agent_call_id = context.get("agent_call_id")
        if isinstance(agent_call_id, str):
            if _update_dimension_digest(
                bucket["agent_call_digest"], agent_call_id, observed_at
            ):
                bucket["agent_call_saturated"] = True
        evidence = payload.get("event_fields")
        if isinstance(evidence, dict):
            representative.append(
                {
                    "kind": "machine_event",
                    "text": str(payload["summary"]),
                    "event_fields": evidence,
                }
            )
        raw_fingerprints = observation.get("evidence_fingerprints")
        if isinstance(raw_fingerprints, list):
            fingerprints.extend(
                item for item in raw_fingerprints if isinstance(item, dict)
            )
    if not buckets_by_day:
        return None
    if not all(
        name in metadata
        for name in ("rule_id", "category", "summary", "impact", "human_action")
    ):
        raise ValueError("machine aggregate metadata is incomplete")

    # bucket 間の distinct dimension を bounded digest へ再集約する。
    buckets = [buckets_by_day[key] for key in sorted(buckets_by_day)]
    scope_digest, scope_saturated = _merge_dimension_digests(
        [bucket["scope_digest"] for bucket in buckets],
        cutoff,
        any(bool(bucket.get("scope_saturated")) for bucket in buckets),
    )
    agent_digest, agent_call_saturated = _merge_dimension_digests(
        [bucket["agent_call_digest"] for bucket in buckets],
        cutoff,
        any(bool(bucket.get("agent_call_saturated")) for bucket in buckets),
    )
    first = min(
        (str(bucket["first_observed_at"]) for bucket in buckets), key=parse_rfc3339
    )
    last = max(
        (str(bucket["last_observed_at"]) for bucket in buckets), key=parse_rfc3339
    )
    occurrence_count = sum(int(bucket["count"]) for bucket in buckets)
    return {
        "schema_version": 1,
        "aggregate_id": machine_aggregate_id(canonical_key),
        "rule_id": metadata["rule_id"],
        "canonical_key": canonical_key,
        "category": metadata["category"],
        "summary": metadata["summary"],
        "impact": metadata["impact"],
        "human_action": metadata["human_action"],
        "window_start": cutoff.isoformat().replace("+00:00", "Z"),
        "window_end": cut_time.isoformat().replace("+00:00", "Z"),
        "occurrence_count": occurrence_count,
        "affected_session_count": len(scope_digest),
        "threshold_counts": {
            "recurrence_scope": len(scope_digest),
            "agent_call": len(agent_digest),
        },
        "time_buckets": buckets,
        "scope_digest": scope_digest,
        "agent_call_digest": agent_digest,
        "scope_saturated": scope_saturated,
        "agent_call_saturated": agent_call_saturated,
        "first_observed_at": first,
        "last_observed_at": last,
        "representative_evidence": _bounded_objects(representative, 5),
        "latest_fingerprints": _bounded_objects(fingerprints, 5),
    }


def _update_dimension_digest(
    digest: list[_JsonObject], raw_value: str, observed_at: str
) -> bool:
    """threshold 判定に必要な distinct value と最終時刻だけを bounded 保存する。"""
    value = hashlib.sha256(raw_value.encode("utf-8")).hexdigest()
    for entry in digest:
        if entry.get("value") == value:
            if parse_rfc3339(observed_at) > parse_rfc3339(
                str(entry["last_observed_at"])
            ):
                entry["last_observed_at"] = observed_at
            return False
    if len(digest) < _MACHINE_DIGEST_LIMIT:
        digest.append({"value": value, "last_observed_at": observed_at})
        digest.sort(key=lambda item: str(item["value"]))
        return False
    return True


def _merge_dimension_digests(
    groups: list[object], cutoff: datetime, previously_saturated: bool
) -> tuple[list[_JsonObject], bool]:
    """bucket の dimension digest を固定上限へ統合する。"""
    unique: dict[str, _JsonObject] = {}
    for group in groups:
        if not isinstance(group, list):
            continue
        for item in group:
            if (
                not isinstance(item, dict)
                or not isinstance(item.get("value"), str)
                or not isinstance(item.get("last_observed_at"), str)
                or parse_rfc3339(item["last_observed_at"]) < cutoff
            ):
                continue
            key = str(item["value"])
            previous = unique.get(key)
            if previous is None or parse_rfc3339(
                str(item["last_observed_at"])
            ) > parse_rfc3339(str(previous["last_observed_at"])):
                unique[key] = dict(item)
    ordered = [unique[key] for key in sorted(unique)]
    return (
        ordered[:_MACHINE_DIGEST_LIMIT],
        previously_saturated or len(ordered) > _MACHINE_DIGEST_LIMIT,
    )


def _machine_threshold_met(aggregate: _JsonObject) -> bool:
    """初期 allowlist rule の distinct recurrence threshold を判定する。"""
    counts = aggregate.get("threshold_counts")
    if not isinstance(counts, dict):
        return False
    scope_count = counts.get("recurrence_scope")
    agent_count = counts.get("agent_call")
    if aggregate.get("rule_id") == "feedback.reporter_unavailable.v1":
        return isinstance(scope_count, int) and scope_count >= 2
    if aggregate.get("rule_id") == "codex.structured_output_validation_exhausted.v1":
        return (
            isinstance(scope_count, int)
            and scope_count >= 2
            and isinstance(agent_count, int)
            and agent_count >= 2
        )
    raise ValueError(f"unknown machine feedback rule: {aggregate.get('rule_id')!r}")


def _apply_machine_aggregate_to_candidate(
    candidate: _JsonObject, aggregate: _JsonObject
) -> None:
    """window-scoped machine aggregate を active candidate の compact field へ反映する。"""
    candidate["origin"] = "machine_rule"
    candidate["category"] = aggregate["category"]
    candidate["summary"] = aggregate["summary"]
    candidate["impact"] = aggregate["impact"]
    candidate["occurrence_count"] = aggregate["occurrence_count"]
    candidate["affected_session_count"] = aggregate["affected_session_count"]
    candidate["session_digest"] = {
        "values": [str(item["value"]) for item in aggregate["scope_digest"]],
        "saturated": aggregate["scope_saturated"],
    }
    candidate["first_observed_at"] = aggregate["first_observed_at"]
    candidate["last_observed_at"] = aggregate["last_observed_at"]
    candidate["representative_evidence"] = aggregate["representative_evidence"]
    candidate["latest_fingerprints"] = aggregate["latest_fingerprints"]
    candidate["machine_state"] = aggregate


def _remediation_candidate_payload(candidate: _JsonObject) -> _JsonObject:
    """verification agent に渡す機械集約済み candidate field だけを返す。"""
    names = (
        "schema_version",
        "candidate_id",
        "origin",
        "category",
        "summary",
        "impact",
        "occurrence_count",
        "affected_session_count",
        "first_observed_at",
        "last_observed_at",
        "representative_evidence",
        "reference_targets",
        "latest_fingerprints",
        "reference_ids",
    )
    return {name: candidate[name] for name in names}


def _publish_report(
    repo: Path,
    worktree: Path,
    manifest: _JsonObject,
    manifest_path: Path,
    candidates: dict[str, _JsonObject],
    machine_aggregates: dict[str, _JsonObject],
    verdicts: dict[str, _JsonObject],
    current_state: ActiveState,
) -> TerminalResult:
    """generation と report を準備し、manifest hash を固定して pointer を切り替える。"""
    unresolved_ids = sorted(
        candidate_id_value
        for candidate_id_value, verdict in verdicts.items()
        if verdict.get("status") == "human_required"
    )
    result = "attention" if unresolved_ids else "ok"
    publication = manifest.get("publication")
    if publication is None:
        targets = manifest["run"]["targets"]
        generated_at = targets["generated_at"]
        generation_id_value = targets["generation_id"]
        report_path = repo / targets["report"]
    elif isinstance(publication, dict):
        generated_at = str(publication["generated_at"])
        generation_id_value = str(publication["generation_id"])
        report_reference = publication.get("report")
        if not isinstance(report_reference, dict):
            raise ValueError("staged report reference must be an object")
        report_path = repo / str(report_reference["path"])
        if publication.get("result") != result:
            raise CmocError(
                "staged feedback publication result が固定入力の再計算結果と一致しません。",
                ["report cut manifest と正式 checkpoint を人間が確認してください。"],
                str(manifest_path),
            )
    else:
        raise ValueError("report cut publication must be an object or null")

    references_by_id = _report_cut_references_by_id(manifest)
    machine_aggregates = _next_machine_aggregates(
        candidates, verdicts, machine_aggregates
    )
    active_issues = {
        candidate_id_value: _active_issue_record(
            manifest,
            candidates[candidate_id_value],
            verdicts[candidate_id_value],
            references_by_id,
            generated_at,
        )
        for candidate_id_value in unresolved_ids
    }
    generation_manifest, generation_files, generation_reference = generation_artifacts(
        repo,
        generation_id=generation_id_value,
        report_cut_id=str(manifest["report_cut_id"]),
        created_at=generated_at,
        session_commit=_joined_session_commit(repo, manifest),
        issues=active_issues,
        machine_aggregates=machine_aggregates,
    )
    generation_references = [
        {
            "path": path.resolve(strict=False)
            .relative_to(repo.resolve(strict=False))
            .as_posix(),
            "sha256": sha256_bytes(content),
        }
        for path, content in generation_files
    ]
    report_content = _render_feedback_report(
        repo,
        worktree,
        manifest,
        generation_id_value,
        generated_at,
        result,
        active_issues,
    ).encode("utf-8")
    report_reference = {
        "path": report_path.resolve(strict=False)
        .relative_to(repo.resolve(strict=False))
        .as_posix(),
        "sha256": sha256_bytes(report_content),
    }
    cleanup = {
        "observations": _observation_cleanup_references(manifest),
        "old_generation": current_generation_artifacts(repo, current_state),
        "work_artifacts": _checkpoint_cleanup_references(manifest),
    }
    expected_publication: _JsonObject = {
        "generation_id": generation_id_value,
        "generation_manifest": generation_reference,
        "generation_artifacts": generation_references,
        "report": report_reference,
        "generated_at": generated_at,
        "result": result,
        "cleanup": cleanup,
    }
    if publication is not None and publication != expected_publication:
        raise CmocError(
            "staged feedback publication が固定入力の再計算結果と一致しません。",
            ["report cut manifest と staged artifact を人間が確認してください。"],
            str(manifest_path),
        )

    manifest["publication"] = expected_publication
    _set_processing_state(repo, manifest, "staging", None)
    publish_generation_artifacts(repo, generation_manifest, generation_files)
    write_immutable_bytes(report_path, report_content)
    if artifact_reference(repo, report_path) != report_reference:
        raise CmocError(
            "feedback Markdown report の保存後 hash が一致しません。",
            ["staged report artifact を人間が確認してください。"],
            str(report_path),
        )

    # publication_ready manifest の byte hash が current pointer の cleanup manifest ID になる。
    processing = manifest["processing"]
    assert isinstance(processing, dict)
    processing["status"] = "publication_ready"
    processing["failure"] = None
    _path, manifest_sha256 = write_report_cut_manifest(repo, manifest)
    publish_current_pointer(
        repo,
        generation_id=generation_id_value,
        generation_manifest=generation_reference,
        report_cut_id=str(manifest["report_cut_id"]),
        report_cut_manifest_sha256=manifest_sha256,
        report=report_reference,
        published_at=rfc3339_now(),
        result=result,
    )
    _record_publication_event(
        repo,
        manifest,
        generation_reference,
        report_reference,
        result,
        len(active_issues),
    )
    return _published_terminal_result(
        repo / str(report_reference["path"]),
        result,
    )


def _publish_incomplete_report(
    repo: Path,
    worktree: Path,
    manifest: _JsonObject,
    manifest_path: Path,
    candidates: dict[str, _JsonObject],
    verdicts: dict[str, _JsonObject],
) -> TerminalResult:
    """全 verdict を materialize し、正常 publication と独立して保存する。"""
    # {{work-root}}/oracle/doc/app_spec/feedback_state.md
    # {{work-root}}/oracle/doc/app_spec/sub_command/feedback_report.md
    unresolved_count = sum(
        verdict.get("status") == "human_required" for verdict in verdicts.values()
    )
    inconclusive_count = sum(
        verdict.get("status") == "inconclusive" for verdict in verdicts.values()
    )
    if inconclusive_count == 0:
        raise ValueError("incomplete report requires an inconclusive verdict")

    diagnostic = manifest.get("diagnostic")
    if diagnostic is None:
        targets = manifest["run"]["targets"]
        generated_at = targets["generated_at"]
        report_path = repo / targets["incomplete_report"]
    elif isinstance(diagnostic, dict):
        generated_at = str(diagnostic["generated_at"])
        report_reference = diagnostic.get("report")
        if not isinstance(report_reference, dict):
            raise ValueError("staged diagnostic report reference must be an object")
        report_path = repo / str(report_reference["path"])
    else:
        raise ValueError("report cut diagnostic must be an object or null")

    report_content = _render_incomplete_report(
        repo,
        worktree,
        manifest,
        generated_at,
        candidates,
        verdicts,
    ).encode("utf-8")
    report_reference = {
        "path": report_path.resolve(strict=False)
        .relative_to(repo.resolve(strict=False))
        .as_posix(),
        "sha256": sha256_bytes(report_content),
    }
    expected_diagnostic: _JsonObject = {
        "report": report_reference,
        "generated_at": generated_at,
        "result": "incomplete",
    }
    if diagnostic is not None and diagnostic != expected_diagnostic:
        raise CmocError(
            "staged incomplete 診断が正式 checkpoint の再計算結果と一致しません。",
            ["report cut manifest と正式 checkpoint を人間が確認してください。"],
            str(manifest_path),
        )
    if manifest.get("publication") is not None:
        raise CmocError(
            "正常 publication と incomplete 診断を同じ report cut に保存できません。",
            ["report cut manifest を人間が確認してください。"],
            str(manifest_path),
        )

    manifest["diagnostic"] = expected_diagnostic
    _set_processing_state(repo, manifest, "diagnostic_staging", None)
    write_immutable_bytes(report_path, report_content)
    if artifact_reference(repo, report_path) != report_reference:
        raise CmocError(
            "incomplete 診断 report の保存後 hash が一致しません。",
            ["診断 report artifact を人間が確認してください。"],
            str(report_path),
        )

    processing = manifest["processing"]
    assert isinstance(processing, dict)
    processing["status"] = "incomplete"
    processing["failure"] = None
    write_report_cut_manifest(repo, manifest)
    _record_incomplete_event(
        repo,
        manifest,
        report_reference,
        unresolved_count,
        inconclusive_count,
    )
    return TerminalResult(
        primary_report=report_path,
        primary_report_role="incomplete feedback diagnostic report",
        result="incomplete",
        next_actions=(
            "`inconclusive` の原因を修正した後に `cmoc feedback report` を再実行してください。",
        ),
    )


def _next_machine_aggregates(
    candidates: dict[str, _JsonObject],
    verdicts: dict[str, _JsonObject],
    aggregates: dict[str, _JsonObject],
) -> dict[str, _JsonObject]:
    """active から外れる machine issue の threshold 未満 state を引き継ぐ。"""
    result = dict(aggregates)
    for candidate_id_value, candidate in candidates.items():
        machine_state = candidate.get("machine_state")
        verdict = verdicts.get(candidate_id_value)
        if (
            candidate.get("origin") != "machine_rule"
            or not isinstance(machine_state, dict)
            or not isinstance(verdict, dict)
            or verdict.get("status") == "human_required"
            or _machine_threshold_met(machine_state)
        ):
            continue
        canonical_key = candidate.get("canonical_key")
        if not isinstance(canonical_key, str):
            raise ValueError("machine candidate canonical key is missing")
        result[canonical_key] = machine_state
    return result


def _resume_publication(
    repo: Path, manifest: _JsonObject, manifest_path: Path
) -> TerminalResult:
    """成果物保存後・pointer 切替前に止まった publication を hash から再開する。"""
    publication = manifest.get("publication")
    if not isinstance(publication, dict):
        raise CmocError(
            "publication_ready な feedback report cut に成果物参照がありません。",
            ["report cut manifest を人間が確認してください。"],
            str(manifest_path),
        )
    current_state = load_active_state(repo)
    if current_state.current is None or current_state.current.get(
        "report_cut_id"
    ) != manifest.get("report_cut_id"):
        if _active_state_input(repo, current_state) != manifest["inputs"].get(
            "current"
        ):
            raise CmocError(
                "feedback publication 再開前に current active state が変化しています。",
                ["current pointer と report cut manifest を人間が確認してください。"],
                str(manifest_path),
            )
        publish_current_pointer(
            repo,
            generation_id=str(publication["generation_id"]),
            generation_manifest=_artifact_object(
                publication.get("generation_manifest"), "generation manifest"
            ),
            report_cut_id=str(manifest["report_cut_id"]),
            report_cut_manifest_sha256=sha256_bytes(manifest_path.read_bytes()),
            report=_artifact_object(publication.get("report"), "Markdown report"),
            published_at=rfc3339_now(),
            result=str(publication["result"]),
        )
    _record_publication_event(
        repo,
        manifest,
        _artifact_object(publication.get("generation_manifest"), "generation manifest"),
        _artifact_object(publication.get("report"), "Markdown report"),
        str(publication["result"]),
        None,
    )
    return _published_terminal_result(
        repo / str(publication["report"]["path"]),
        str(publication["result"]),
    )


def _active_issue_record(
    manifest: _JsonObject,
    candidate: _JsonObject,
    verdict: _JsonObject,
    references_by_id: dict[str, _JsonObject],
    verified_at: str,
) -> _JsonObject:
    """unresolved candidate と最新 verification を compact active record にする。"""
    if verdict.get("status") != "human_required":
        raise ValueError("only unresolved candidates can become active issues")
    evidence = verdict.get("current_evidence")
    if not isinstance(evidence, list):
        raise ValueError("unresolved verdict current_evidence must be an array")
    materialized = [
        _materialize_current_evidence(item, references_by_id)
        for item in evidence[:5]
        if isinstance(item, dict)
    ]
    evidence_targets = [
        {
            "path": item["path"],
            "kind": item.get("kind"),
            "location": item.get("location"),
        }
        for item in materialized
        if isinstance(item.get("path"), str)
    ]
    return {
        "schema_version": 1,
        "issue_id": candidate["candidate_id"],
        "origin": candidate["origin"],
        "canonical_key": candidate["canonical_key"],
        "category": mask_feedback_text(str(candidate["category"])),
        "summary": mask_feedback_text(str(candidate["summary"])),
        "impact": mask_feedback_text(str(candidate["impact"])),
        "occurrence_count": candidate["occurrence_count"],
        "affected_session_count": candidate["affected_session_count"],
        "session_digest": _masked_json_object(candidate["session_digest"]),
        "first_observed_at": candidate["first_observed_at"],
        "last_observed_at": candidate["last_observed_at"],
        "representative_evidence": _masked_object_list(
            candidate.get("representative_evidence"), 5
        ),
        "reference_targets": _masked_object_list(
            _bounded_objects(
                [
                    *candidate.get("reference_targets", []),
                    *evidence_targets,
                ],
                5,
            ),
            5,
        ),
        "latest_fingerprints": _masked_object_list(
            candidate.get("latest_fingerprints"), 5
        ),
        "verification": {
            "report_cut_id": manifest["report_cut_id"],
            "verified_at": verified_at,
            "reason": mask_feedback_text(str(verdict["reason"])),
            "current_evidence": materialized,
            "human_action": mask_feedback_text(str(verdict["human_action"])),
        },
        "machine_state": (
            _masked_json_object(candidate["machine_state"])
            if isinstance(candidate.get("machine_state"), dict)
            else None
        ),
    }


def _materialize_current_evidence(
    evidence: _JsonObject, references_by_id: dict[str, _JsonObject]
) -> _JsonObject:
    """cut-scoped ID を削除予定 artifact に依存しない compact evidence へ解決する。"""
    del references_by_id
    return {
        "kind": "repository_content",
        "path": mask_feedback_text(str(evidence["path"])),
        "location": mask_feedback_text(str(evidence["location"])),
        "finding": mask_feedback_text(str(evidence["finding"])),
    }


def _report_cut_references_by_id(manifest: _JsonObject) -> dict[str, _JsonObject]:
    """固定済み reference を ID で引く。"""
    inputs = manifest.get("inputs")
    references = inputs.get("references") if isinstance(inputs, dict) else None
    if not isinstance(references, list):
        raise ValueError("report cut references must be an array")
    return {
        str(reference["reference_id"]): reference
        for reference in references
        if isinstance(reference, dict)
        and isinstance(reference.get("reference_id"), str)
    }


def _render_feedback_report(
    repo: Path,
    worktree: Path,
    manifest: _JsonObject,
    generation_id_value: str,
    generated_at: str,
    result: str,
    issues: dict[str, _JsonObject],
) -> str:
    """正常 publication 用の current unresolved issue 一覧だけを描画する。"""
    fields = (
        ("command", "cmoc feedback report"),
        ("generated_at", generated_at),
        ("repo_root", str(repo)),
        ("session_branch", current_branch(worktree)),
        *_run_report_fields(manifest),
        ("report_cut_id", manifest["report_cut_id"]),
        ("report_cut_at", manifest["cut_at"]),
        ("active_generation_id", generation_id_value),
        ("remediation_issue_count", _remediation_candidate_count(manifest)),
        ("human_required_issue_count", len(issues)),
        ("result", result),
    )
    lines = [
        "---",
        *[f"{name}: {_yaml_scalar(value)}" for name, value in fields],
        "---",
    ]
    lines.extend(["# cmoc feedback report", "", "## Issues", ""])
    if not issues:
        lines.extend(["人間対応が必要な issue はありません。", ""])
        return "\n".join([*lines, manifest["run"]["execution_record"] or ""])
    for issue_id_value, issue in sorted(issues.items()):
        verification = issue["verification"]
        assert isinstance(verification, dict)
        session_count = str(issue["affected_session_count"])
        session_digest = issue.get("session_digest")
        if isinstance(session_digest, dict) and session_digest.get("saturated") is True:
            session_count += "+"
        lines.extend(
            [
                f"### {_markdown_text(issue_id_value)}",
                "",
                f"- Category: {_markdown_text(issue['category'])}",
                f"- Summary: {_markdown_text(issue['summary'])}",
                f"- Impact: {_markdown_text(issue['impact'])}",
                f"- Human action: {_markdown_text(verification['human_action'])}",
                f"- Occurrences: {issue['occurrence_count']}",
                f"- Affected sessions: {session_count}",
                f"- First observed: {_markdown_text(issue['first_observed_at'])}",
                f"- Last observed: {_markdown_text(issue['last_observed_at'])}",
                "- Current evidence:",
            ]
        )
        for current_evidence in verification["current_evidence"]:
            assert isinstance(current_evidence, dict)
            target = (
                current_evidence.get("path")
                or current_evidence.get("probe_id")
                or current_evidence.get("observation_id", "unknown")
            )
            lines.append(
                "  - "
                f"{_markdown_text(target)} / "
                f"{_markdown_text(current_evidence.get('location', ''))}: "
                f"{_markdown_text(current_evidence.get('finding', ''))}"
            )
        lines.append("- Representative evidence:")
        representative = issue.get("representative_evidence")
        if isinstance(representative, list) and representative:
            for evidence in representative:
                lines.append(
                    f"  - {_markdown_text(json.dumps(evidence, ensure_ascii=False, sort_keys=True))}"
                )
        else:
            lines.append("  - none")
        lines.append("")
    return "\n".join([*lines, manifest["run"]["execution_record"] or ""])


def _render_incomplete_report(
    repo: Path,
    worktree: Path,
    manifest: _JsonObject,
    generated_at: str,
    candidates: dict[str, _JsonObject],
    verdicts: dict[str, _JsonObject],
) -> str:
    """未 publication の確定 verdict と判定不能理由を単独で読める形にする。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/feedback_report.md
    unresolved_ids = sorted(
        candidate_id_value
        for candidate_id_value, verdict in verdicts.items()
        if verdict.get("status") == "human_required"
    )
    inconclusive_ids = sorted(
        candidate_id_value
        for candidate_id_value, verdict in verdicts.items()
        if verdict.get("status") == "inconclusive"
    )
    fields = (
        ("command", "cmoc feedback report"),
        ("generated_at", generated_at),
        ("repo_root", str(repo)),
        ("session_branch", current_branch(worktree)),
        *_run_report_fields(manifest),
        ("report_cut_id", manifest["report_cut_id"]),
        ("report_cut_at", manifest["cut_at"]),
        ("remediation_issue_count", len(verdicts)),
        ("human_required_issue_count", len(unresolved_ids)),
        ("inconclusive_candidate_count", len(inconclusive_ids)),
        ("result", "incomplete"),
    )
    lines = [
        "---",
        *[f"{name}: {_yaml_scalar(value)}" for name, value in fields],
        "---",
        "# cmoc feedback report: incomplete",
        "",
        "この診断 report は正常 publication ではありません。",
        "新しい active generation と current pointer は publication されていません。",
        "直前の正常 publication が存在する場合は、その publication が current のままです。",
        "",
        "## 確定済みだが今回未 publication の human_required issue",
        "",
        "以下の verdict は診断情報であり、今回の active generation へ publication されていません。",
        "直前の正常 active generation に同じ issue が含まれる可能性とは区別してください。",
        "",
    ]
    references_by_id = _report_cut_references_by_id(manifest)
    if not unresolved_ids:
        lines.extend(["該当 candidate はありません。", ""])
    for candidate_id_value in unresolved_ids:
        candidate = candidates[candidate_id_value]
        verdict = verdicts[candidate_id_value]
        lines.extend(
            [
                f"### {_markdown_text(candidate_id_value)}",
                "",
                f"- Origin: {_markdown_text(mask_feedback_text(str(candidate['origin'])))}",
                f"- Category: {_markdown_text(mask_feedback_text(str(candidate['category'])))}",
                f"- Summary: {_markdown_text(mask_feedback_text(str(candidate['summary'])))}",
                f"- Impact: {_markdown_text(mask_feedback_text(str(candidate['impact'])))}",
                f"- Verification reason: {_markdown_text(mask_feedback_text(str(verdict['reason'])))}",
                f"- Human action: {_markdown_text(mask_feedback_text(str(verdict['human_action'])))}",
                "- Current evidence:",
            ]
        )
        _append_diagnostic_current_evidence(
            lines,
            verdict.get("current_evidence"),
            references_by_id,
        )
        lines.append("")

    lines.extend(["## inconclusive issue", ""])
    for candidate_id_value in inconclusive_ids:
        candidate = candidates[candidate_id_value]
        verdict = verdicts[candidate_id_value]
        lines.extend(
            [
                f"### {_markdown_text(candidate_id_value)}",
                "",
                f"- Summary: {_markdown_text(mask_feedback_text(str(candidate['summary'])))}",
                f"- Reason: {_markdown_text(mask_feedback_text(str(verdict['reason'])))}",
                "- Current evidence:",
            ]
        )
        _append_diagnostic_current_evidence(
            lines,
            verdict.get("current_evidence"),
            references_by_id,
        )
        lines.append("")
    return "\n".join([*lines, manifest["run"]["execution_record"] or ""])


def _append_diagnostic_current_evidence(
    lines: list[str],
    evidence: object,
    references_by_id: dict[str, _JsonObject],
) -> None:
    """cut reference を診断 report 内の自己完結した current evidence にする。"""
    values = evidence if isinstance(evidence, list) else []
    materialized = [
        _materialize_current_evidence(item, references_by_id)
        for item in values
        if isinstance(item, dict)
    ]
    if not materialized:
        lines.append("  - 確認できた current evidence はありません。")
        return
    for item in materialized:
        target = (
            item.get("path")
            or item.get("probe_id")
            or item.get("observation_id", "unknown")
        )
        lines.append(
            "  - "
            f"{_markdown_text(target)} / "
            f"{_markdown_text(item.get('location', ''))}: "
            f"{_markdown_text(item.get('finding', ''))}"
        )


def _remediation_candidate_count(manifest: _JsonObject) -> int:
    """正式 remediation checkpoint 数を front matter の candidate 件数にする。"""
    processing = manifest.get("processing")
    checkpoints = (
        processing.get("remediation_checkpoints")
        if isinstance(processing, dict)
        else None
    )
    if not isinstance(checkpoints, list):
        raise ValueError("remediation checkpoints must be an array")
    return len(checkpoints)


def _new_report_path(repo: Path, *, incomplete: bool = False) -> Path:
    """正常／診断 report の既存 artifact を上書きしない path を選ぶ。"""
    directory = reports_dir(repo, "feedback")
    if incomplete:
        directory /= "incomplete"
    while True:
        path = directory / f"{timestamp()}.md"
        if not path.exists() and not path.is_symlink():
            return path


def _yaml_scalar(value: object) -> str:
    """YAML 1.2 と互換な JSON scalar を返す。"""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if value is None:
        return "null"
    return json.dumps(str(value), ensure_ascii=False)


def _markdown_text(value: object) -> str:
    """外部入力が Markdown の行構造を変更しない compact text を返す。"""
    return html.escape(str(value).replace("\r", " ").replace("\n", " "), quote=False)


def _masked_json_value(value: Any) -> Any:
    """永続 compact state に含める文字列へ feedback secret masking を再適用する。"""
    if isinstance(value, str):
        return mask_feedback_text(value)
    if isinstance(value, list):
        return [_masked_json_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _masked_json_value(item) for key, item in value.items()}
    return value


def _masked_json_object(value: object) -> _JsonObject:
    """JSON object を deep copy しながら文字列を mask する。"""
    if not isinstance(value, dict):
        raise ValueError("expected JSON object")
    masked = _masked_json_value(value)
    assert isinstance(masked, dict)
    return masked


def _masked_object_list(value: object, limit: int) -> list[_JsonObject]:
    """bounded object array を deep copy しながら文字列を mask する。"""
    if not isinstance(value, list):
        raise ValueError("expected JSON object array")
    result = [_masked_json_object(item) for item in value if isinstance(item, dict)]
    return result[:limit]


def _observation_cleanup_references(manifest: _JsonObject) -> list[_JsonObject]:
    """cut に含まれる全 raw file を publication 後 cleanup target にする。"""
    inputs = manifest.get("inputs")
    entries = inputs.get("observations") if isinstance(inputs, dict) else None
    if not isinstance(entries, list):
        raise ValueError("report cut observations must be an array")
    return [
        {"path": entry["path"], "sha256": entry["sha256"]}
        for entry in entries
        if isinstance(entry, dict)
    ]


def _checkpoint_cleanup_references(manifest: _JsonObject) -> list[_JsonObject]:
    """正式 checkpoint file を manifest 自体より先に削除する一覧へまとめる。"""
    processing = manifest.get("processing")
    if not isinstance(processing, dict):
        raise ValueError("report cut processing must be an object")
    references: list[_JsonObject] = []
    for name in ("normalization_checkpoints", "remediation_checkpoints"):
        values = processing.get(name)
        if not isinstance(values, list):
            raise ValueError(f"{name} must be an array")
        references.extend(
            {"path": item["path"], "sha256": item["sha256"]}
            for item in values
            if isinstance(item, dict)
        )
    from commons.runtime_feedback_run_state import run_artifact_references

    references.extend(run_artifact_references(manifest))
    return sorted(references, key=lambda item: str(item["path"]))


def _artifact_object(value: object, description: str) -> _JsonObject:
    """publication section の path/hash object を型付きで返す。"""
    if not isinstance(value, dict) or set(value) != {"path", "sha256"}:
        raise ValueError(f"{description} reference is malformed")
    return value


def _full_log_path(repo: Path, value: object) -> str | None:
    """subcommand log に記録する artifact path をフルパスへ変換する。"""
    # {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
    if not isinstance(value, str):
        return None
    path = Path(value)
    if not path.is_absolute():
        path = repo / path
    return str(path.resolve(strict=False))


def _record_publication_event(
    repo: Path,
    manifest: _JsonObject,
    generation_reference: _JsonObject,
    report_reference: _JsonObject,
    result: str,
    unresolved_count: int | None,
) -> None:
    """publication point を subcommand log から一意に確認できるようにする。"""
    logger = current_subcommand_logger()
    if logger is not None:
        logger.event(
            "feedback_report_published",
            report_cut_id=manifest.get("report_cut_id"),
            active_generation_id=manifest.get("publication", {}).get("generation_id"),
            generation_manifest_path=_full_log_path(
                repo, generation_reference.get("path")
            ),
            report_path=_full_log_path(repo, report_reference.get("path")),
            result=result,
            unresolved_issue_count=unresolved_count,
        )


def _record_incomplete_event(
    repo: Path,
    manifest: _JsonObject,
    report_reference: _JsonObject,
    unresolved_count: int,
    inconclusive_count: int,
) -> None:
    """正常 publication 不成立と durable な診断 report を log に記録する。"""
    logger = current_subcommand_logger()
    if logger is not None:
        logger.event(
            "feedback_report_incomplete",
            report_cut_id=manifest.get("report_cut_id"),
            report_path=_full_log_path(repo, report_reference.get("path")),
            result="incomplete",
            verification_candidate_count=_remediation_candidate_count(manifest),
            unresolved_candidate_count=unresolved_count,
            inconclusive_candidate_count=inconclusive_count,
            normal_publication=False,
        )


def _set_processing_state(
    repo: Path, manifest: _JsonObject, status: str, failure: str | None
) -> None:
    """固定入力を変えず processing status/failure だけを atomic update する。"""
    processing = manifest.get("processing")
    if not isinstance(processing, dict):
        raise ValueError("report cut processing must be an object")
    processing["status"] = status
    processing["failure"] = failure
    write_report_cut_manifest(repo, manifest)


def _record_feedback_interruption(
    manifest: _JsonObject | None, manifest_path: Path | None
) -> TerminalResult:
    """中断を正常系として subcommand state と log へ記録する。"""
    _update_feedback_progress_fields(manifest)
    mark_current_subcommand_interrupted()
    logger = current_subcommand_logger()
    if logger is not None:
        logger.event(
            "feedback_report_interrupted",
            report_cut_id=(manifest.get("report_cut_id") if manifest else None),
            report_cut_manifest_path=(str(manifest_path) if manifest_path else None),
        )
    details: tuple[tuple[str, object], ...] = ()
    next_actions: tuple[str, ...] = ()
    if manifest_path is not None:
        details = (("保持した feedback run", manifest_path),)
        next_actions = (
            "`cmoc run join` で確定済み修正を取り込むか、`cmoc run abandon` で破棄してください。",
        )
    return TerminalResult(details=details, next_actions=next_actions)


def _update_feedback_progress_fields(manifest: _JsonObject | None) -> None:
    """invocation summary 用に durable checkpoint の確定件数だけを保持する。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/feedback_report.md
    if manifest is None:
        update_primary_report_fields(
            normalization_checkpoint_count=None,
            remediation_checkpoint_count=None,
            partial_result_count=None,
            processing_status=None,
        )
        return
    processing = manifest.get("processing")
    normalization = (
        processing.get("normalization_checkpoints")
        if isinstance(processing, dict)
        else None
    )
    verification = (
        processing.get("remediation_checkpoints")
        if isinstance(processing, dict)
        else None
    )
    normalization_count = (
        len(normalization) if isinstance(normalization, list) else None
    )
    verification_count = len(verification) if isinstance(verification, list) else None
    partial_result_count = (
        normalization_count + verification_count
        if normalization_count is not None and verification_count is not None
        else None
    )
    update_primary_report_fields(
        normalization_checkpoint_count=normalization_count,
        remediation_checkpoint_count=verification_count,
        partial_result_count=partial_result_count,
        processing_status=(
            processing.get("status") if isinstance(processing, dict) else None
        ),
    )


def _published_terminal_result(report_path: Path, result: str) -> TerminalResult:
    """確定済み publication を run finalization へ渡す。"""
    return TerminalResult(
        primary_report=report_path,
        primary_report_role="feedback report",
        result=result,
    )


def _joined_session_commit(repo: Path, manifest: _JsonObject) -> str:
    """公開 generation の根拠となる検査済み session commit を読む。"""
    from commons.runtime_feedback_run_state import read_run_artifact

    return str(read_run_artifact(repo, manifest["run"]["completion"])["session_commit"])


def _run_report_fields(manifest: _JsonObject) -> tuple[tuple[str, object], ...]:
    """self-joining run の identity と finalization の確定情報を掲載する。"""
    run = manifest["run"]
    identity = run["identity"]
    from commons.runtime_feedback_run_state import read_run_artifact

    merged = read_run_artifact(Path(identity["repo"]), run["merged"])
    return (
        ("feedback_run_id", identity["run_branch"].rsplit("/", 1)[-1]),
        ("run_kind", identity["kind"]),
        ("run_branch", identity["run_branch"]),
        ("run_fork_commit", identity["run_fork_commit"]),
        ("run_worktree", identity["run_worktree"]),
        ("run_join_commit", merged["run_join_commit"]),
        ("final_high_watermark", run["high_watermark"]),
        ("wave_count", len(run["waves"])),
    )
