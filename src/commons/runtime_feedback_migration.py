"""tracked feedback state を repository-local state へ一回限りで移行する。

対応する oracle file:
`{{work-root}}/oracle/doc/app_spec/feedback_state.md`。
"""

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .runtime_errors import CmocError
from .runtime_feedback_state import (
    legacy_feedback_root,
    migration_receipt_path,
    validate_legacy_feedback_state,
    validate_migration_artifacts,
    write_state_snapshot_from_records,
)
from .runtime_feedback_store import (
    canonical_json_bytes,
    feedback_root,
    migration_root,
    parse_rfc3339,
    report_snapshot_root,
    rfc3339_now,
    sha256_bytes,
    write_immutable_bytes,
    write_immutable_json,
)
from .runtime_git import current_branch, require_clean_worktree, run_git

_LEGACY_PREFIX = ".cmoc/gt/ar/feedback"


@dataclass(frozen=True)
class LegacyCandidate:
    """local branch tip から固定した legacy feedback tree。"""

    branch: str
    commit: str
    tree: str
    files: dict[str, bytes]


def ensure_feedback_migration(
    repo: Path,
    *,
    migration_source: str | None,
) -> None:
    """normalized state を読み書きする前に migration receipt を確定する。"""
    # {{work-root}}/oracle/doc/app_spec/feedback_state.md
    receipt_path = migration_receipt_path(repo)
    prepared_path = migration_root(repo) / "prepared.json"
    if receipt_path.is_file():
        if migration_source is not None:
            raise CmocError(
                "--migration-source は feedback state 移行の完了後に指定できません。",
                ["option を外して再実行してください。"],
                str(receipt_path),
            )
        receipt = _read_canonical_object(receipt_path, "migration receipt")
        validate_migration_artifacts(repo, receipt, source_path=receipt_path)
        _remove_reappeared_legacy_state(repo, receipt)
        return

    if prepared_path.is_file():
        prepared = _read_canonical_object(prepared_path, "prepared migration")
        _validate_prepared_artifacts(repo, prepared)
        _remove_archived_legacy_state(repo, prepared)
        _write_receipt(repo, receipt_path, prepared)
        return

    branch = current_branch(repo)
    if migration_source is not None and migration_source != branch:
        raise CmocError(
            "--migration-source は現在 checkout 中の active session branch と一致しません。",
            ["現在 branch を移行元として選択するか、option を外してください。"],
            f"current: {branch}\nrequested: {migration_source}",
        )
    candidates = _local_legacy_candidates(repo)
    selected = next((item for item in candidates if item.branch == branch), None)
    if selected is None and candidates:
        raise _divergence_error(
            "active session branch に旧 feedback state がなく、別の local branch に存在します。",
            candidates,
            selected,
        )
    divergent = [
        item
        for item in candidates
        if selected is not None and item.files != selected.files
    ]
    if divergent and migration_source is None:
        raise _divergence_error(
            "local branch 間で旧 feedback state が分岐しています。",
            candidates,
            selected,
        )
    if migration_source is not None and not divergent:
        raise CmocError(
            "--migration-source は divergent な旧 feedback state がある場合だけ指定できます。",
            ["option を外して再実行してください。"],
            migration_source,
        )

    if selected is None:
        empty_receipt = _empty_receipt(branch)
        _write_receipt(repo, receipt_path, empty_receipt)
        return

    require_clean_worktree(repo)
    validate_legacy_feedback_state(repo)
    candidate_records = [_archive_candidate(repo, item) for item in candidates]
    selected_archive = next(
        item for item in candidate_records if item["branch"] == selected.branch
    )
    migrated_records, legacy_reports = _copy_selected_records(
        repo, selected, selected_archive
    )
    baseline = _build_legacy_baseline(repo, selected, legacy_reports)
    migration_receipt: dict[str, Any] = {
        "schema_version": 1,
        "migration_version": 1,
        "completed_at": rfc3339_now(),
        "source_branch": selected.branch,
        "source_commit": selected.commit,
        "source_tree": selected.tree,
        "candidates": candidate_records,
        "records": migrated_records,
        "legacy_reports": legacy_reports,
        "baseline": baseline,
    }
    # deletion 後の receipt 保存失敗からも同じ byte 列で再開できる。
    write_immutable_json(prepared_path, migration_receipt)
    _validate_prepared_artifacts(repo, migration_receipt)
    _remove_archived_legacy_state(repo, migration_receipt)
    _write_receipt(repo, receipt_path, migration_receipt)


def _empty_receipt(branch: str) -> dict[str, Any]:
    """旧 state がない repository の完了 receipt を返す。"""
    return {
        "schema_version": 1,
        "migration_version": 1,
        "completed_at": rfc3339_now(),
        "source_branch": branch,
        "source_commit": None,
        "source_tree": None,
        "candidates": [],
        "records": [],
        "legacy_reports": [],
        "baseline": None,
    }


def _local_legacy_candidates(repo: Path) -> list[LegacyCandidate]:
    """全 local branch tip にある legacy tree を commit と byte 列で固定する。"""
    lines = run_git(
        ["for-each-ref", "--format=%(refname:short)%09%(objectname)", "refs/heads"],
        repo,
    ).stdout.splitlines()
    pairs = [tuple(line.split("\t", 1)) for line in lines if "\t" in line]
    candidates: list[LegacyCandidate] = []
    for branch, commit in pairs:
        tree_result = run_git(
            ["rev-parse", "--verify", f"{commit}:{_LEGACY_PREFIX}"],
            repo,
            check=False,
        )
        if tree_result.returncode != 0:
            continue
        tree = tree_result.stdout.strip()
        if run_git(["cat-file", "-t", tree], repo).stdout.strip() != "tree":
            continue
        files = _legacy_tree_files(repo, commit)
        candidates.append(LegacyCandidate(branch, commit, tree, files))
    return sorted(candidates, key=lambda item: item.branch)


def _legacy_tree_files(repo: Path, commit: str) -> dict[str, bytes]:
    """commit 上の legacy tree を root 相対 byte 列で読む。"""
    names = run_git(
        ["ls-tree", "-r", "-z", "--name-only", commit, "--", _LEGACY_PREFIX],
        repo,
    ).stdout.split("\0")
    files: dict[str, bytes] = {}
    prefix = f"{_LEGACY_PREFIX}/"
    for name in names:
        if not name:
            continue
        if not name.startswith(prefix):
            raise CmocError("legacy feedback tree の path が不正です。", [], name)
        relative = name.removeprefix(prefix)
        # legacy record は UTF-8 JSON であり、run_git の text 変換後も byte 列が一致する。
        files[relative] = run_git(["show", f"{commit}:{name}"], repo).stdout.encode(
            "utf-8"
        )
    return files


def _divergence_error(
    summary: str,
    candidates: list[LegacyCandidate],
    selected: LegacyCandidate | None,
) -> CmocError:
    """branch、commit、tree、差分 path を含む移行停止 error を返す。"""
    selected_files = selected.files if selected is not None else {}
    lines: list[str] = []
    for candidate in candidates:
        different = sorted(
            path
            for path in candidate.files.keys() | selected_files.keys()
            if candidate.files.get(path) != selected_files.get(path)
        )
        lines.extend(
            [
                f"branch: {candidate.branch}",
                f"commit: {candidate.commit}",
                f"tree: {candidate.tree}",
                f"different_paths: {different}",
            ]
        )
    return CmocError(
        summary,
        [
            "branch の join/abandon で候補を整理するか、active session branch を `--migration-source` で明示してください。"
        ],
        "\n".join(lines),
    )


def _archive_candidate(repo: Path, candidate: LegacyCandidate) -> dict[str, Any]:
    """candidate tree の全 byte 列を repository-local audit archive へ保存する。"""
    branch_key = hashlib.sha256(candidate.branch.encode("utf-8")).hexdigest()
    root = migration_root(repo) / "archive" / branch_key / candidate.tree / "tree"
    references: list[dict[str, str]] = []
    for relative, content in sorted(candidate.files.items()):
        path = root / relative
        digest = write_immutable_bytes(path, content)
        references.append(
            {
                "legacy_path": relative,
                "archive_path": path.relative_to(feedback_root(repo)).as_posix(),
                "sha256": digest,
            }
        )
    return {
        "branch": candidate.branch,
        "commit": candidate.commit,
        "tree": candidate.tree,
        "files": references,
    }


def _copy_selected_records(
    repo: Path,
    selected: LegacyCandidate,
    archive_candidate: dict[str, Any],
) -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    """選択 tree の normalized record を新 root へ取り込み、旧 report は archive 参照にする。"""
    records: list[dict[str, str]] = []
    reports: list[dict[str, Any]] = []
    archive_by_path = {
        item["legacy_path"]: item
        for item in archive_candidate["files"]
        if isinstance(item, dict)
    }
    for relative, content in sorted(selected.files.items()):
        if relative.startswith("issue/") or relative.startswith("ingestion/"):
            destination = feedback_root(repo) / relative
            digest = write_immutable_bytes(destination, content)
            records.append({"path": relative, "sha256": digest})
            continue
        if not relative.startswith("report/"):
            raise CmocError(
                "legacy feedback state に未定義 path があります。",
                ["schema 違反 path を確認してください。"],
                relative,
            )
        record = json.loads(content)
        if not isinstance(record, dict):
            raise CmocError(
                "legacy report record が JSON object ではありません。", [], relative
            )
        report_id = str(record.get("report_id", ""))
        snapshot_path = report_snapshot_root(repo) / f"{report_id}.json"
        report_path_value = Path(str(record.get("report_path", "")))
        if (
            snapshot_path.is_symlink()
            or not snapshot_path.is_file()
            or sha256_bytes(snapshot_path.read_bytes())
            != record.get("snapshot_manifest_sha256")
            or report_path_value.is_symlink()
            or not report_path_value.is_file()
            or sha256_bytes(report_path_value.read_bytes())
            != record.get("report_sha256")
        ):
            raise CmocError(
                "legacy report artifact の参照整合性を検証できません。",
                [
                    "report record、report snapshot、Markdown report を確認してください。"
                ],
                relative,
            )
        archive = archive_by_path[relative]
        reports.append(
            {
                "report_id": report_id,
                "source_branch": selected.branch,
                "source_commit": selected.commit,
                "legacy_path": relative,
                "archive_path": archive["archive_path"],
                "sha256": archive["sha256"],
            }
        )
    return records, reports


def _build_legacy_baseline(
    repo: Path,
    selected: LegacyCandidate,
    legacy_reports: list[dict[str, Any]],
) -> dict[str, str] | None:
    """直前の正常 legacy report 時点を immutable state snapshot へ変換する。"""
    normal: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for metadata in legacy_reports:
        content = selected.files[str(metadata["legacy_path"])]
        record = json.loads(content)
        if isinstance(record, dict) and record.get("result") in {"ok", "attention"}:
            normal.append((metadata, record))
    if not normal:
        return None
    metadata, report = max(
        normal,
        key=lambda item: (
            parse_rfc3339(str(item[1]["generated_at"])),
            str(item[1]["report_id"]),
        ),
    )
    legacy_path = f"{_LEGACY_PREFIX}/{metadata['legacy_path']}"
    commits = run_git(
        [
            "log",
            "--format=%H",
            "--diff-filter=A",
            selected.commit,
            "--",
            legacy_path,
        ],
        repo,
    ).stdout.splitlines()
    if not commits:
        raise CmocError(
            "legacy report を最初に含む commit tree を特定できません。",
            ["legacy report の Git history を確認してください。"],
            legacy_path,
        )
    baseline_files = _legacy_tree_files(repo, commits[-1])
    records: dict[str, dict[str, Any]] = {}
    for relative, content in baseline_files.items():
        if not (relative.startswith("issue/") or relative.startswith("ingestion/")):
            continue
        destination = feedback_root(repo) / relative
        if not destination.is_file() or destination.read_bytes() != content:
            raise CmocError(
                "legacy baseline record を新 state から再構築できません。",
                ["source commit と migrated record を確認してください。"],
                relative,
            )
        value = json.loads(content)
        if not isinstance(value, dict):
            raise CmocError(
                "legacy baseline record が JSON object ではありません。", [], relative
            )
        records[relative] = value
    snapshot, _digest = write_state_snapshot_from_records(
        repo,
        records=records,
        normalization_unit_ids=[],
        created_at=str(report["generated_at"]),
    )
    return {
        "legacy_report_id": str(report["report_id"]),
        "state_snapshot_id": str(snapshot["state_snapshot_id"]),
    }


def _remove_reappeared_legacy_state(repo: Path, receipt: dict[str, Any]) -> None:
    """移行後に再度見えた legacy tree を archive 一致時だけ削除する。"""
    if not legacy_feedback_root(repo).exists():
        return
    _remove_archived_legacy_state(repo, receipt)


def _remove_archived_legacy_state(repo: Path, receipt: dict[str, Any]) -> None:
    """現在の legacy tree が archive のいずれかと一致する場合だけ削除 commit を作る。"""
    legacy = legacy_feedback_root(repo)
    head_paths = run_git(
        ["ls-tree", "-r", "--name-only", "HEAD", "--", _LEGACY_PREFIX],
        repo,
    ).stdout.splitlines()
    if not legacy.exists():
        if not head_paths:
            return
        index_paths = run_git(
            ["ls-files", "--", _LEGACY_PREFIX], repo
        ).stdout.splitlines()
        staged = run_git(["diff", "--cached", "--name-only"], repo).stdout.splitlines()
        unstaged = run_git(["diff", "--name-only"], repo).stdout.splitlines()
        untracked = run_git(
            ["ls-files", "--others", "--exclude-standard"], repo
        ).stdout.splitlines()
        if (
            index_paths
            or not staged
            or unstaged
            or untracked
            or any(
                path != _LEGACY_PREFIX and not path.startswith(f"{_LEGACY_PREFIX}/")
                for path in staged
            )
        ):
            raise CmocError(
                "legacy feedback state の削除途中を安全に再開できません。",
                ["Git index と working tree を人間が確認してください。"],
                (
                    f"head: {head_paths}\nindex: {index_paths}\n"
                    f"staged: {staged}\nunstaged: {unstaged}\nuntracked: {untracked}"
                ),
            )
        _commit_legacy_deletion(repo)
        return
    unsupported = [
        path
        for path in legacy.rglob("*")
        if path.is_symlink() or (not path.is_dir() and not path.is_file())
    ]
    if unsupported:
        raise CmocError(
            "legacy feedback state に archive 未検証の特殊 path があります。",
            ["内容を保持したまま人間が確認してください。"],
            "\n".join(str(path) for path in unsupported),
        )
    current = {
        path.relative_to(legacy).as_posix(): path.read_bytes()
        for path in legacy.rglob("*")
        if path.is_file() and not path.is_symlink()
    }
    matched = False
    for candidate in receipt.get("candidates", []):
        if not isinstance(candidate, dict):
            continue
        archived: dict[str, bytes] = {}
        for item in candidate.get("files", []):
            if not isinstance(item, dict):
                continue
            path = feedback_root(repo) / str(item.get("archive_path"))
            if path.is_file() and sha256_bytes(path.read_bytes()) == item.get("sha256"):
                archived[str(item.get("legacy_path"))] = path.read_bytes()
        if archived == current:
            matched = True
            break
    if not matched:
        raise CmocError(
            "legacy feedback state が migration archive と一致しません。",
            ["内容差がある path を保持したまま人間が確認してください。"],
            str(legacy),
        )
    require_clean_worktree(repo)
    run_git(["rm", "-r", "--", _LEGACY_PREFIX], repo)
    staged = run_git(["diff", "--cached", "--name-only"], repo).stdout.splitlines()
    if not staged or any(
        path != _LEGACY_PREFIX and not path.startswith(f"{_LEGACY_PREFIX}/")
        for path in staged
    ):
        raise CmocError(
            "legacy feedback state の削除 commit を分離できません。",
            ["Git index を確認してください。"],
            repr(staged),
        )
    _commit_legacy_deletion(repo)


def _commit_legacy_deletion(repo: Path) -> None:
    """旧 state の staged deletion だけを一回限りの commit にする。"""
    run_git(
        ["commit", "-m", "cmoc feedback state migration", "--", _LEGACY_PREFIX],
        repo,
    )


def _validate_prepared_artifacts(repo: Path, receipt: dict[str, Any]) -> None:
    """deletion 前に保存した migration output の hash を再検査する。"""
    validate_migration_artifacts(
        repo,
        receipt,
        source_path=migration_root(repo) / "prepared.json",
    )


def _write_receipt(repo: Path, path: Path, receipt: dict[str, Any]) -> None:
    """migration receipt を最後の durable artifact として保存する。"""
    validate_migration_artifacts(repo, receipt, source_path=path)
    try:
        write_immutable_json(path, receipt)
    except Exception as exc:
        raise CmocError(
            "feedback migration receipt を durable に保存できません。",
            ["migration archive を保持したまま再実行してください。"],
            str(path),
        ) from exc


def _read_canonical_object(path: Path, description: str) -> dict[str, Any]:
    """migration artifact を canonical JSON object として読む。"""
    try:
        if path.is_symlink() or not path.is_file():
            raise ValueError("regular file required")
        content = path.read_bytes()
        value = json.loads(content)
        if not isinstance(value, dict) or content != canonical_json_bytes(value):
            raise ValueError("canonical JSON object required")
        return value
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        raise CmocError(
            f"{description} が不正です。",
            ["migration artifact を人間が確認してください。"],
            str(path),
        ) from exc
