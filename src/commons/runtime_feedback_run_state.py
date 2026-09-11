"""Feedback run の immutable wave、issue checkpoint、seal と join 記録を検証する。

根拠: {{work-root}}/oracle/doc/app_spec/feedback_state.md の
「checkpoint と report cut」と「run lifecycle との整合」。
"""

import json
import re
from dataclasses import asdict
from importlib import resources
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .runtime_feedback_state import (
    _corruption,
    _read_canonical_object,
    _require_exact_fields,
    _validate_report_cut_artifact_reference,
    artifact_reference,
    write_report_cut_manifest,
)
from .runtime_feedback_store import (
    canonical_json_bytes,
    sha256_bytes,
    write_immutable_json,
)
from .runtime_logging import current_subcommand_logger
from .runtime_run_lifecycle import EditingRunContext


def new_run_record(context: EditingRunContext) -> dict[str, Any]:
    """run identity と未処理の artifact reference を作る。"""
    logger = current_subcommand_logger()
    return {
        "invocation_log": str(logger.path.relative_to(context.repo))
        if logger
        else None,
        "identity": {
            key: str(value) if isinstance(value, Path) else value
            for key, value in asdict(context).items()
        },
        "waves": [],
        "high_watermark": 0,
        "sealed": None,
        "join_intent": None,
        "merged": None,
        "completion": None,
        "execution_record": None,
        "targets": None,
    }


def run_artifact_references(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    """manifest が所有する immutable run artifact だけを列挙する。"""
    run = manifest["run"]
    return sorted(
        [
            *run["waves"],
            *[
                run[name]
                for name in ("sealed", "join_intent", "merged", "completion")
                if run[name] is not None
            ],
        ],
        key=lambda item: item["path"],
    )


def save_run_artifact(
    repo: Path, manifest: dict[str, Any], name: str, content: dict[str, Any]
) -> dict[str, Any]:
    """immutable artifact を先に保存し、検証済み reference を manifest へ登録する。"""
    directory = repo / ".cmoc/gu/feedback/work" / manifest["report_cut_id"]
    relative = {
        "sealed": "report_cut.json",
        "join_intent": "join_intent.json",
        "merged": "merge_completion.json",
        "completion": "publication_completion.json",
    }[name]
    path = directory / relative
    write_immutable_json(path, content)
    reference = artifact_reference(repo, path)
    manifest["run"][name] = reference
    write_report_cut_manifest(repo, manifest)
    return reference


def read_run_artifact(repo: Path, reference: dict[str, Any]) -> dict[str, Any]:
    """run 内の reference と canonical hash を検証して artifact を読む。"""
    path = _validate_report_cut_artifact_reference(
        repo,
        reference,
        expected_root=repo / ".cmoc/gu/feedback/work",
        description="feedback run artifact",
        allow_missing=False,
    )
    return _read_canonical_object(path, "feedback run artifact")


def selected_remediation_checkpoints(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    """各 issue の最後の論理 call を publication 用に選ぶ。履歴は削除しない。"""
    selected: dict[str, dict[str, Any]] = {}
    for reference in sorted(
        manifest["processing"]["remediation_checkpoints"],
        key=lambda item: int(Path(item["path"]).stem.split(".")[1]),
    ):
        selected[reference["candidate_id"]] = reference
    return [selected[identity] for identity in sorted(selected)]


def validate_decision_basis(
    value: object, path: Path, *, compact: bool = False
) -> None:
    """判定条件の hash と、検査条件・結果の自己完結した記録を検査する。"""
    basis = _require_exact_fields(
        value,
        {"scope", "verification", "current_evidence", "cycle_states"}
        | ({"state_sha256"} if compact else {"state"}),
        path,
        "decision basis",
    )
    if basis["scope"] != "repository-inputs-v1":
        raise _corruption("feedback 判定根拠の scope が不正です。", path)
    digests = []
    if compact:
        digests.append(basis["state_sha256"])
    else:
        state = _require_exact_fields(
            basis["state"], {"files", "evidence_sha256"}, path, "decision state"
        )
        if not isinstance(state["files"], dict):
            raise _corruption("feedback 判定根拠の file 集合が不正です。", path)
        for name in state["files"]:
            if (
                not isinstance(name, str)
                or not name
                or Path(name).is_absolute()
                or ".." in Path(name).parts
                or Path(name).as_posix() != name
            ):
                raise _corruption("feedback 判定根拠の path が不正です。", path)
        digests.extend(state["files"].values())
        digests.append(state["evidence_sha256"])
    if not isinstance(basis["cycle_states"], list):
        raise _corruption("feedback 循環診断の状態集合が不正です。", path)
    digests.extend(basis["cycle_states"])
    if any(
        not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None
        for value in digests
    ):
        raise _corruption("feedback 判定根拠の hash が不正です。", path)
    if (
        not isinstance(basis["verification"], list)
        or not basis["verification"]
        or not isinstance(basis["current_evidence"], list)
    ):
        raise _corruption("feedback 判定根拠の検査記録が不正です。", path)
    if basis["cycle_states"] != sorted(set(basis["cycle_states"])):
        raise _corruption(
            "feedback 循環診断の状態が一意な hash 順ではありません。", path
        )
    if compact:
        schema = json.loads(
            resources.files("oracle.acp_builder.feedback")
            .joinpath("remediate_issue.json")
            .read_text()
        )
        for field, definition in (
            ("verification", "verifications"),
            ("current_evidence", "current_evidence_required"),
        ):
            if not Draft202012Validator(
                {"$defs": schema["$defs"], "$ref": f"#/$defs/{definition}"}
            ).is_valid(basis[field]):
                raise _corruption(
                    "active issue の判定根拠が検査記録 schema に適合しません。", path
                )
        if basis["cycle_states"]:
            raise _corruption("循環診断を active issue に変換できません。", path)


def recover_run_artifact_references(
    repo: Path, manifest: dict[str, Any], path: Path
) -> None:
    """artifact 保存と manifest 更新の間の停止を、固定 path から読み取り回復する。"""
    if (
        manifest.get("publication") is not None
        or manifest.get("diagnostic") is not None
    ):
        return
    run = manifest.get("run")
    if not isinstance(run, dict) or not isinstance(run.get("waves"), list):
        return  # 正式 validator が構造違反を報告する。
    next_wave = path.parent / "wave" / str(len(run["waves"]) + 1) / "input.json"
    if next_wave.exists() or next_wave.is_symlink():
        if run.get("sealed") is not None:
            raise _corruption("封印後に未列挙 wave があります。", next_wave)
        run["waves"].append(artifact_reference(repo, next_wave))
    for name, filename in (
        ("sealed", "report_cut.json"),
        ("join_intent", "join_intent.json"),
        ("merged", "merge_completion.json"),
        ("completion", "publication_completion.json"),
    ):
        target = path.parent / filename
        if run.get(name) is None and (target.exists() or target.is_symlink()):
            content = _read_canonical_object(target, f"feedback {name}")
            if name == "sealed":
                run["targets"] = content.get("targets")
            run[name] = artifact_reference(repo, target)


def validate_manifest_update(
    previous: dict[str, Any], current: dict[str, Any], path: Path
) -> None:
    """append-only な intake と、一度だけ封印する publication 入力を保つ。"""
    old_run, new_run = previous["run"], current["run"]
    old_inputs, new_inputs = previous["inputs"], current["inputs"]
    if (
        old_run["identity"] != new_run["identity"]
        or old_run["invocation_log"] != new_run["invocation_log"]
        or previous["cut_at"] != current["cut_at"]
    ):
        raise _corruption("feedback run identity を変更できません。", path)
    for key in ("current", "versions"):
        if old_inputs[key] != new_inputs[key]:
            raise _corruption("feedback run の開始時入力を変更できません。", path)
    if old_run["sealed"] is not None and old_inputs != new_inputs:
        raise _corruption("封印済み report cut の入力を変更できません。", path)
    for key in ("observations", "references"):
        new_values = {canonical_json_bytes(item) for item in new_inputs[key]}
        if any(
            canonical_json_bytes(item) not in new_values for item in old_inputs[key]
        ):
            raise _corruption("feedback intake の既存入力を変更できません。", path)
    if (
        new_run["waves"][: len(old_run["waves"])] != old_run["waves"]
        or new_run["high_watermark"] < old_run["high_watermark"]
    ):
        raise _corruption(
            "feedback wave または high-watermark が逆行しています。", path
        )
    for key in (
        "sealed",
        "join_intent",
        "merged",
        "completion",
        "execution_record",
        "targets",
    ):
        if old_run[key] is not None and new_run[key] != old_run[key]:
            raise _corruption(f"feedback run の確定済み {key} を変更できません。", path)
    if old_run["sealed"] is not None:
        for key in ("waves", "high_watermark"):
            if old_run[key] != new_run[key]:
                raise _corruption("封印済み intake を変更できません。", path)
    for key in ("normalization_checkpoints", "remediation_checkpoints"):
        new_values = {canonical_json_bytes(item) for item in current["processing"][key]}
        if any(
            canonical_json_bytes(item) not in new_values
            for item in previous["processing"][key]
        ):
            raise _corruption("正式 checkpoint を変更できません。", path)


def validate_run_artifacts(
    repo: Path, manifest: dict[str, Any], path: Path, *, allow_missing: bool
) -> None:
    """run identity、ordered wave、seal と join evidence の hash 対応を検査する。"""
    run = _require_exact_fields(
        manifest.get("run"),
        {
            "identity",
            "invocation_log",
            "waves",
            "high_watermark",
            "sealed",
            "join_intent",
            "merged",
            "completion",
            "execution_record",
            "targets",
        },
        path,
        "feedback run",
    )
    identity = _require_exact_fields(
        run["identity"],
        set(EditingRunContext.__dataclass_fields__),
        path,
        "feedback run identity",
    )
    if identity["kind"] != "feedback_report" or identity["repo"] != str(repo.resolve()):
        raise _corruption("feedback run の repository または kind が不正です。", path)
    log = run["invocation_log"]
    if not isinstance(log, str) or not (repo / log).resolve().is_relative_to(
        repo / ".cmoc/gu/log/sub_command"
    ):
        raise _corruption("feedback invocation log の path が不正です。", path)
    if (
        not isinstance(run["waves"], list)
        or type(run["high_watermark"]) is not int
        or run["high_watermark"] < 0
    ):
        raise _corruption("feedback intake の境界が不正です。", path)
    if run["execution_record"] is not None and not isinstance(
        run["execution_record"], str
    ):
        raise _corruption("feedback 実行記録が不正です。", path)
    expected_paths = {
        "sealed": path.parent / "report_cut.json",
        "join_intent": path.parent / "join_intent.json",
        "merged": path.parent / "merge_completion.json",
        "completion": path.parent / "publication_completion.json",
    }
    last_watermark = 0
    missing_wave_artifact = False
    for sequence, reference in enumerate(run["waves"], 1):
        target = _validate_report_cut_artifact_reference(
            repo,
            reference,
            expected_root=path.parent / "wave",
            description="feedback intake wave",
            allow_missing=allow_missing,
        )
        if target != path.parent / "wave" / str(sequence) / "input.json":
            raise _corruption("feedback wave の順序または path が不正です。", path)
        if not target.exists():
            # Cleanup removes work artifacts in manifest order and may stop
            # after an earlier wave.  Once that happens, a later wave's
            # `after` value cannot be checked because the preceding boundary
            # is no longer available.  The current-pointer path explicitly
            # opts into this missing-artifact state; retain structural/path
            # validation while deferring cross-wave continuity until the
            # manifest itself is removed.
            missing_wave_artifact = True
            continue
        if missing_wave_artifact and allow_missing:
            continue
        wave = _read_canonical_object(target, "feedback intake wave")
        _require_exact_fields(
            wave,
            {"sequence", "after", "high_watermark", "inputs", "candidates"},
            target,
            "intake wave",
        )
        if (
            wave["sequence"] != sequence
            or type(wave["after"]) is not int
            or type(wave["high_watermark"]) is not int
            # A larger `after` would skip durable receipts between waves.
            or wave["after"] != last_watermark
            or not wave["after"] <= wave["high_watermark"] <= run["high_watermark"]
        ):
            raise _corruption("feedback wave の high-watermark が不正です。", target)
        if not isinstance(wave["candidates"], dict):
            raise _corruption("feedback wave の candidate 集合が不正です。", target)
        last_watermark = wave["high_watermark"]
    for name, expected in expected_paths.items():
        reference = run[name]
        if reference is None:
            continue
        target = _validate_report_cut_artifact_reference(
            repo,
            reference,
            expected_root=path.parent,
            description=f"feedback {name}",
            allow_missing=allow_missing,
        )
        if target != expected:
            raise _corruption("feedback run artifact の path が不正です。", target)
        if not target.exists():
            continue
        value = _read_canonical_object(target, f"feedback {name}")
        if value.get("report_cut_id") != manifest["report_cut_id"]:
            raise _corruption("feedback run artifact の identity が不正です。", target)
        if name == "sealed":
            for key, expected_value in (
                ("inputs", manifest["inputs"]),
                ("waves", run["waves"]),
                ("high_watermark", run["high_watermark"]),
                ("targets", run["targets"]),
                ("checkpoints", manifest["processing"]["remediation_checkpoints"]),
                ("selected_checkpoints", selected_remediation_checkpoints(manifest)),
            ):
                if value.get(key) != expected_value:
                    raise _corruption(
                        f"report cut の {key} が封印入力と一致しません。", target
                    )
        elif value.get("sealed") != run["sealed"] or run["sealed"] is None:
            raise _corruption("join 記録と report cut が一致しません。", target)
    if (run["completion"] is not None and run["merged"] is None) or (
        run["merged"] is not None and run["sealed"] is None
    ):
        raise _corruption("feedback join の先行 artifact がありません。", path)
    if (
        manifest["publication"] is not None or manifest["diagnostic"] is not None
    ) and run["completion"] is None:
        raise _corruption(
            "join 後検査前に feedback publication を開始できません。", path
        )


def validate_remediation_checkpoint(checkpoint: dict[str, Any], path: Path) -> None:
    """canonical schema と issue commit の機械検査記録が正式結果に一致するか検査する。"""
    checkpoint = _require_exact_fields(
        checkpoint,
        {
            "schema_version",
            "kind",
            "report_cut_id",
            "candidate_id",
            "input",
            "input_sha256",
            "builder_sha256",
            "schema_sha256",
            "structured_output",
            "output_sha256",
            "audit",
        },
        path,
        "remediation checkpoint",
    )
    if (
        type(checkpoint["schema_version"]) is not int
        or checkpoint["schema_version"] != 1
        or checkpoint["kind"] != "remediation"
    ):
        raise _corruption("remediation checkpoint identity が不正です。", path)
    for field in ("input_sha256", "builder_sha256", "schema_sha256", "output_sha256"):
        value = checkpoint[field]
        if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None:
            raise _corruption(f"remediation checkpoint {field} が不正です。", path)
    input_value = checkpoint["input"]
    if (
        not isinstance(input_value, dict)
        or sha256_bytes(canonical_json_bytes(input_value)) != checkpoint["input_sha256"]
    ):
        raise _corruption("remediation checkpoint の入力 hash が不正です。", path)
    _require_exact_fields(
        input_value,
        {"issue", "wave", "before_commit", "decision_state"},
        path,
        "remediation input",
    )
    if not isinstance(input_value["issue"], dict):
        raise _corruption("remediation issue input が不正です。", path)
    output = checkpoint["structured_output"]
    schema = json.loads(
        resources.files("oracle.acp_builder.feedback")
        .joinpath("remediate_issue.json")
        .read_text()
    )
    if not Draft202012Validator(schema).is_valid(output):
        raise _corruption(
            "remediation checkpoint output が schema に適合しません。", path
        )
    if sha256_bytes(canonical_json_bytes(output)) != checkpoint["output_sha256"]:
        raise _corruption("remediation checkpoint output hash が一致しません。", path)
    result = output["result"]
    audit = _require_exact_fields(
        checkpoint.get("audit"),
        {
            "wave",
            "before_commit",
            "after_commit",
            "commit",
            "changed_paths",
            "diff_sha256",
            "call_log",
            "mechanical_checks",
            "decision_basis",
        },
        path,
        "remediation audit",
    )
    for reference, description in (
        (audit["wave"], "remediation audit wave"),
        (audit["call_log"], "remediation audit call log"),
    ):
        reference = _require_exact_fields(
            reference, {"path", "sha256"}, path, description
        )
        reference_path = reference["path"]
        reference_hash = reference["sha256"]
        if (
            not isinstance(reference_path, str)
            or not reference_path
            or Path(reference_path).is_absolute()
            or ".." in Path(reference_path).parts
            or Path(reference_path).as_posix() != reference_path
            or not isinstance(reference_hash, str)
            or re.fullmatch(r"[0-9a-f]{64}", reference_hash) is None
        ):
            raise _corruption(f"{description} が不正です。", path)
    validate_decision_basis(audit["decision_basis"], path)
    basis = audit["decision_basis"]
    if (
        basis["verification"] != result["verification"]
        or basis["current_evidence"] != result["current_evidence"]
        or (basis["cycle_states"] and result["status"] != "inconclusive")
    ):
        raise _corruption("feedback 判定根拠と正式な検査記録が一致しません。", path)
    issue = input_value["issue"]
    if not isinstance(input_value["decision_state"], dict) or issue.get(
        "decision_state_sha256"
    ) != sha256_bytes(canonical_json_bytes(input_value["decision_state"])):
        raise _corruption("feedback call の開始時判定条件がありません。", path)
    validate_decision_basis({**basis, "state": input_value["decision_state"]}, path)
    recheck = issue.get("reconfirmation")
    if recheck is not None:
        recheck = _require_exact_fields(
            recheck,
            {
                "previous_checkpoint",
                "previous_result",
                "previous_basis",
                "changes",
                "history",
                "cycle_states",
                "cycle_reason",
            },
            path,
            "feedback reconfirmation",
        )
        history = recheck["history"]
        if not isinstance(history, list) or not history:
            raise _corruption("feedback 再確認の先行 checkpoint が不正です。", path)
        for reference in history:
            reference = _require_exact_fields(
                reference,
                {"candidate_id", "path", "sha256"},
                path,
                "feedback reconfirmation checkpoint reference",
            )
            if (
                not isinstance(reference["candidate_id"], str)
                or not isinstance(reference["path"], str)
                or not reference["path"]
                or Path(reference["path"]).is_absolute()
                or ".." in Path(reference["path"]).parts
                or Path(reference["path"]).as_posix() != reference["path"]
                or not isinstance(reference["sha256"], str)
                or re.fullmatch(r"[0-9a-f]{64}", reference["sha256"]) is None
                or reference["candidate_id"] != checkpoint["candidate_id"]
            ):
                raise _corruption("feedback 再確認の先行 checkpoint が不正です。", path)
        previous_checkpoint = _require_exact_fields(
            recheck["previous_checkpoint"],
            {"candidate_id", "path", "sha256"},
            path,
            "feedback reconfirmation previous checkpoint",
        )
        if history[-1] != previous_checkpoint:
            raise _corruption("feedback 再確認の先行 checkpoint が不正です。", path)
    expected_cycle = (
        recheck["cycle_states"]
        if recheck and result["status"] == "inconclusive"
        else []
    )
    if basis["cycle_states"] != expected_cycle:
        raise _corruption("feedback 循環診断と再確認入力が一致しません。", path)
    wave_sequence = Path(audit["wave"]["path"]).parent.name
    if (
        not wave_sequence.isdecimal()
        or path.stem != f"{checkpoint['candidate_id']}.{int(wave_sequence):08d}"
    ):
        raise _corruption("feedback checkpoint の論理 call identity が不正です。", path)
    if (
        result["issue_id"] != checkpoint["candidate_id"]
        or input_value.get("issue", {}).get("issue_id") != checkpoint["candidate_id"]
        or input_value.get("wave") != audit["wave"]
        or input_value.get("before_commit") != audit["before_commit"]
        or sorted(result["changed_paths"]) != audit["changed_paths"]
        or len(set(result["changed_paths"])) != len(result["changed_paths"])
    ):
        raise _corruption("remediation output と実差分の記録が一致しません。", path)
    for field in ("before_commit", "after_commit"):
        if (
            not isinstance(audit[field], str)
            or re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", audit[field]) is None
        ):
            raise _corruption("remediation commit ID が不正です。", path)
    if audit["mechanical_checks"] != {
        "changed_paths": True,
        "allowed_paths": True,
        "verification": True,
    }:
        raise _corruption("remediation の機械検査が完了していません。", path)
    if audit["commit"] is not None and audit["commit"] != audit["after_commit"]:
        raise _corruption("remediation issue commit が終了 tree と一致しません。", path)
    if audit["commit"] is None and audit["before_commit"] != audit["after_commit"]:
        raise _corruption("commit なしの remediation が HEAD を変更しています。", path)
    if (
        not isinstance(audit["diff_sha256"], str)
        or re.fullmatch(r"[0-9a-f]{64}", audit["diff_sha256"]) is None
    ):
        raise _corruption("remediation 差分 hash が不正です。", path)
    for changed_path in audit["changed_paths"]:
        if (
            not changed_path
            or Path(changed_path).is_absolute()
            or ".." in Path(changed_path).parts
            or Path(changed_path).as_posix() != changed_path
        ):
            raise _corruption("remediation の変更 path が正規化されていません。", path)
    if result["status"] == "fixed" and (
        not audit["changed_paths"] or audit["commit"] is None
    ):
        raise _corruption("fixed checkpoint に issue commit がありません。", path)
    if audit["changed_paths"] and any(
        item["status"] != "passed" for item in result["verification"]
    ):
        raise _corruption(
            "修正を残す checkpoint の verification が成功していません。", path
        )
