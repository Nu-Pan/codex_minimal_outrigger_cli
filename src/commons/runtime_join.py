"""run/session join の準備・取り込み・復旧を共有する。"""

import json
import os
import tempfile
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from reference.request_builder.basic import AgentCallParameter

from .runtime_errors import CmocError
from .runtime_git import (
    current_branch,
    head_commit,
    literal_pathspec,
    require_clean_worktree,
    run_git,
)
from .runtime_merge_conflict import resolve_merge_conflicts
from .runtime_primary_report import update_primary_report_fields
from .runtime_refactor import merge_refactor_states
from .runtime_results import CodexExecCallable
from .runtime_run import (
    run_process_tracking,
    stop_tracked_codex_children,
    write_run_process_id,
)
from .runtime_run_lifecycle import commit_work_unit, tree_changes, worktree_change_paths


@dataclass(frozen=True)
class MergeContext:
    """取り込み元と取り込み先、および復旧処理が所有する repository。"""

    repo: Path
    session_id: str
    source_branch: str
    source_worktree: Path
    target_branch: str
    target_worktree: Path
    revert_base: str | None = None


@dataclass(kw_only=True)
class MergeRecord(ABC):
    """取り込み確定を境界に復旧方法を選ぶ、両 join 共通の進行記録。"""

    original_source_head: str
    target_head: str | None = None
    prepared_head: str | None = None
    sync_commit: str | None = None
    resolution: dict[str, Any] = field(default_factory=dict)
    preparation_started: bool = False
    owned_source_head: str | None = None
    pending_action: str | None = None
    force_paths: list[str] = field(default_factory=list)
    attempts: list[dict[str, Any]] = field(default_factory=list)
    import_started: bool = False
    imported: bool = False
    join_commit: str | None = None
    target_commit: str | None = None
    target_tree: str | None = None
    finished: bool = False

    def __post_init__(self) -> None:
        if self.owned_source_head is None:
            self.owned_source_head = self.original_source_head

    @property
    @abstractmethod
    def endpoints(self) -> MergeContext:
        """コマンド固有の identity を共通の branch 対応として返す。"""

    @abstractmethod
    def save(self) -> None:
        """資源を削除した後も再開できる場所へ進行記録を保存する。"""


def require_regular_record_path(path: Path) -> None:
    """復旧情報を symlink や特殊 file 経由で読み書きしない。"""
    if any(parent.is_symlink() for parent in (path, *path.parents)) or (
        path.exists() and not path.is_file()
    ):
        raise CmocError("join 復旧記録の path が不正です。", [], str(path))


def save_merge_record(path: Path, record: MergeRecord) -> None:
    """置換と directory flush を終えてから次の不可逆操作へ進む。"""
    require_regular_record_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = asdict(record)
    data["context"] = {
        key: str(value) if isinstance(value, Path) else value
        for key, value in data["context"].items()
    }
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, delete=False
        ) as stream:
            temporary = stream.name
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary is not None:
            Path(temporary).unlink(missing_ok=True)


def validate_merge_record(record: MergeRecord) -> None:
    """Git 照合前に記録の型と未確定操作の種類を確認する。"""
    for name in (
        "original_source_head",
        "target_head",
        "prepared_head",
        "sync_commit",
        "join_commit",
        "target_commit",
        "target_tree",
        "owned_source_head",
    ):
        value = getattr(record, name)
        if value is not None and (
            not isinstance(value, str)
            or len(value) != 40
            or any(char not in "0123456789abcdef" for char in value)
        ):
            raise ValueError(f"invalid {name}")
    if record.original_source_head is None or not isinstance(record.resolution, dict):
        raise ValueError("invalid outcome")
    for name in ("preparation_started", "import_started", "imported", "finished"):
        if type(getattr(record, name)) is not bool:
            raise ValueError(f"invalid {name}")
    if (
        record.pending_action not in {None, "doctor", "force", "merge", "sync"}
        or not isinstance(record.force_paths, list)
        or not all(isinstance(path, str) for path in record.force_paths)
    ):
        raise ValueError("invalid preparation action")
    if not isinstance(record.attempts, list) or any(
        not isinstance(attempt, dict)
        or set(attempt) != {"target_head", "prepared_head", "sync_commit", "resolution"}
        for attempt in record.attempts
    ):
        raise ValueError("invalid preparation history")


def branch_head(root: Path, branch: str) -> str:
    """remote-tracking ref や同名 tag を使わず local branch の HEAD を取得する。"""
    return run_git(
        ["rev-parse", "--verify", f"refs/heads/{branch}"], root
    ).stdout.strip()


def rollback_join_preparation(record: MergeRecord) -> None:
    """取り込み前の準備だけを戻し、確定済み成果と人間の変更を保持する。"""
    if confirm_import(record) or not record.preparation_started:
        return
    context = record.endpoints
    stop_tracked_codex_children(context.repo, context.session_id)
    source, target = context.source_worktree, context.target_worktree
    # 同じ worktree を使う session join では、取り込み中の home から戻る。
    if current_branch(target) == context.target_branch:
        merge_head = run_git(
            ["rev-parse", "-q", "--verify", "MERGE_HEAD"], target, check=False
        )
        if merge_head.returncode == 0:
            if (
                not record.import_started
                or merge_head.stdout.strip() != record.prepared_head
                or head_commit(target) != record.target_head
                or run_git(["write-tree"], target).stdout.strip()
                != tree_id(context.repo, record.prepared_head or "")
                or run_git(["diff", "--quiet"], target, check=False).returncode
                or run_git(
                    ["ls-files", "--others", "--exclude-standard"], target
                ).stdout
            ):
                raise CmocError(
                    "取り込み先の未確定差分の帰属を確認できません。", [], ""
                )
            run_git(["merge", "--abort"], target)
        if source == target:
            if not record.import_started:
                raise CmocError("join の作業 branch が変更されています。", [], "")
            require_clean_worktree(target)
            run_git(["switch", "--no-guess", context.source_branch], source)
    if current_branch(source) != context.source_branch:
        raise CmocError("join の取り込み元 branch が変更されています。", [], "")
    require_preparation_ownership(record)
    if run_git(
        ["ls-tree", "-r", "--name-only", record.original_source_head, "--", ".cmoc/gu"],
        source,
    ).stdout:
        # doctor が追跡を外した管理領域を reset で戻すと、今回の記録を上書きし得る。
        raise CmocError(
            "管理領域を再追跡する準備前の tree へは自動復旧できません。",
            ["管理領域の保存内容を保持して、追跡状態と準備変更を確認してください。"],
            record.original_source_head,
        )
    run_git(["merge", "--abort"], source, check=False)
    run_git(["reset", "--hard", record.original_source_head], source)
    run_git(["clean", "-fd"], source)
    record.attempts.append(
        {
            "target_head": record.target_head,
            "prepared_head": record.prepared_head,
            "sync_commit": record.sync_commit,
            "resolution": record.resolution,
        }
    )
    record.target_head = record.prepared_head = record.sync_commit = None
    record.resolution = {}
    record.preparation_started = record.import_started = False
    record.owned_source_head = record.original_source_head
    record.pending_action = None
    record.force_paths = []
    record.save()
    update_primary_report_fields(merge_rollback="completed", process_stop="confirmed")


def prepare_and_import(
    record: MergeRecord,
    build_request: Callable[[str, str, Path], AgentCallParameter],
    *,
    warnings: list[str],
    codex_exec: CodexExecCallable | None = None,
) -> None:
    """取り込み元で統合・検証し、その tree を取り込み先へ確定する。"""
    context = record.endpoints
    source, target = context.source_worktree, context.target_worktree
    try:
        if confirm_import(record):
            update_primary_report_fields(join_recovery="post_join")
            return
        if current_branch(source) != context.source_branch:
            raise CmocError("join の取り込み元 branch が変更されています。", [], "")
        require_clean_worktree(source)
        if target != source:
            require_clean_worktree(target)
        baseline = record.target_head or branch_head(
            context.repo, context.target_branch
        )
        if branch_head(context.repo, context.target_branch) != baseline:
            raise CmocError("準備中に取り込み先 HEAD が変更されました。", [], "")
        record.target_head = baseline
        record.preparation_started = True
        source_head = require_preparation_ownership(record)
        record.owned_source_head = source_head
        record.pending_action = "merge"
        record.save()
        update_primary_report_fields(
            join_phase="merge preparation", merge_status="started"
        )
        merge = run_git(["merge", "--ff", "--no-edit", baseline], source, check=False)
        record.resolution = {"agent_status": "not_needed", "initial_conflicts": []}
        if merge.returncode != 0:
            write_run_process_id(context.repo, context.session_id, os.getpid())

            def stop_writers() -> None:
                warnings.extend(
                    stop_tracked_codex_children(context.repo, context.session_id) or []
                )

            def save_resolution(result: dict[str, Any]) -> None:
                record.resolution = dict(result)
                record.save()

            with run_process_tracking(context.repo, context.session_id):
                resolve_merge_conflicts(
                    source,
                    lambda: build_request(source_head, baseline, source),
                    codex_exec=codex_exec,
                    purpose="join conflict resolution",
                    before_commit=stop_writers,
                    record_result=save_resolution,
                    sync_managed_entries=False,
                )
        merged_head = require_preparation_ownership(record)
        record.resolution["verified_commit"] = merged_head
        record.owned_source_head = merged_head
        record.pending_action = "sync"
        record.save()
        update_primary_report_fields(join_phase="refactor state sync")
        merge_refactor_states(source, (source_head, baseline))
        record.sync_commit = commit_work_unit(
            source, "cmoc refactor state sync before join"
        )
        record.prepared_head = require_preparation_ownership(record)
        record.owned_source_head = record.prepared_head
        record.pending_action = None
        require_clean_worktree(source)
        record.save()
        # branch 切替や取り込みを開始する前に、停止後の復旧に必要な境界を保存する。
        if branch_head(context.repo, context.target_branch) != baseline:
            raise CmocError("準備中に取り込み先 HEAD が変更されました。", [], "")
        record.import_started = True
        record.save()
        update_primary_report_fields(join_phase="merge import")
        if source == target:
            run_git(["switch", "--no-guess", context.target_branch], target)
        if current_branch(target) != context.target_branch:
            raise CmocError("join の取り込み先 branch が変更されています。", [], "")
        require_clean_worktree(target)
        if (
            head_commit(target) != baseline
            or branch_head(context.repo, context.source_branch) != record.prepared_head
        ):
            raise CmocError("準備後に join 対象 HEAD が変更されました。", [], "")
        if record.prepared_head == baseline:
            record.target_commit = baseline
            record.target_tree = tree_id(context.repo, baseline)
            record.imported = True
            record.save()
        else:
            run_git(["merge", "--no-ff", "--no-commit", record.prepared_head], target)
            if (
                head_commit(target) != baseline
                or run_git(["write-tree"], target).stdout.strip()
                != tree_id(context.repo, record.prepared_head)
                or run_git(["diff", "--quiet"], target, check=False).returncode
            ):
                raise CmocError("join の取り込み条件が変更されました。", [], "")
            run_git(["commit", "--no-edit"], target)
            if not confirm_import(record):
                raise CmocError("join の取り込み成立を確認できません。", [], "")
        update_primary_report_fields(merge_status="completed")
    except BaseException as exc:
        try:
            rollback_join_preparation(record)
        except BaseException as recovery_error:
            update_primary_report_fields(
                merge_rollback="failed", rollback_error=repr(recovery_error)
            )
            raise CmocError(
                "join の準備を復旧できませんでした。", [], repr(recovery_error)
            ) from exc
        raise


def tree_id(root: Path, commit: str) -> str:
    """記録した commit の tree を取得する。"""
    return run_git(["rev-parse", f"{commit}^{{tree}}"], root).stdout.strip()


def confirm_import(record: MergeRecord) -> bool:
    """保存直前の停止も、両 parent と tree の一致から取り込みを確認する。"""
    # 到達可能性だけでは、準備や別の取り込みを成功と読み替えない。
    context = record.endpoints
    if record.imported:
        if (
            record.target_commit is None
            or record.target_tree is None
            or record.prepared_head is None
            or record.target_head is None
        ):
            raise CmocError("join の取り込み記録が不完全です。", [], "")
        # 同じ immutable commit の tree と親を、照合ごとに一括で取り直す。
        commits = run_git(
            [
                "log",
                "--no-walk=unsorted",
                "--format=%H %T %P",
                record.target_commit,
                record.prepared_head,
            ],
            context.repo,
        ).stdout.splitlines()
        metadata = {
            fields[0]: fields[1:] for line in commits if (fields := line.split())
        }
        if (
            record.target_commit not in metadata
            or record.prepared_head not in metadata
            or metadata[record.target_commit][0] != record.target_tree
            or metadata[record.prepared_head][0] != record.target_tree
        ):
            raise CmocError("記録した取り込み成果を確認できません。", [], "")
        if record.join_commit is None:
            valid = record.target_commit == record.target_head == record.prepared_head
        else:
            valid = record.join_commit == record.target_commit and metadata[
                record.target_commit
            ][1:] == [record.target_head, record.prepared_head]
        if not valid:
            raise CmocError("join の取り込み履歴と基準が一致しません。", [], "")
        # 不整合な記録では ref 照会を省き、正常な記録では毎回到達可能性を検査する。
        if (
            run_git(
                [
                    "merge-base",
                    "--is-ancestor",
                    record.target_commit,
                    context.target_branch,
                ],
                context.repo,
                check=False,
            ).returncode
            != 0
        ):
            raise CmocError("記録した取り込み成果を確認できません。", [], "")
        return True
    if record.prepared_head is None or record.target_head is None:
        return False
    commits = run_git(
        [
            "log",
            "--first-parent",
            "--format=%H %T %P",
            f"{record.target_head}..{context.target_branch}",
        ],
        context.repo,
    ).stdout.splitlines()
    # 親と tree を履歴と一括取得し、候補ごとの process 起動を避ける。
    candidates = [
        (fields[0], fields[1])
        for line in commits
        if (fields := line.split())[2:] == [record.target_head, record.prepared_head]
    ]
    if not candidates:
        return False
    prepared_tree = tree_id(context.repo, record.prepared_head)
    matches = [commit for commit, tree in candidates if tree == prepared_tree]
    if len(matches) > 1:
        raise CmocError("join の取り込み成立を一意に確認できません。", [], "")
    if not matches:
        return False
    record.imported = True
    record.join_commit = record.target_commit = matches[0]
    record.target_tree = prepared_tree
    record.save()
    return True


def require_preparation_ownership(record: MergeRecord) -> str:
    """準備が所有する commit と差分だけを復旧対象として認める。"""
    # commit 作成と記録保存の間に停止した場合だけ、保留した操作と履歴を照合する。
    # 確認した HEAD を直後の記録にも使い、次の操作後は改めて検査する。
    context = record.endpoints
    head = head_commit(context.source_worktree)
    pending_paths = set(
        worktree_change_paths(context.source_worktree, include_rename_sources=True)
    )
    if not _preparation_paths_match(record, pending_paths):
        raise CmocError(
            "取り込み元の未確定差分の帰属を確認できません。",
            [],
            "\n".join(sorted(pending_paths)),
        )
    if head == record.owned_source_head:
        if record.pending_action is None:
            require_clean_worktree(context.source_worktree)
        return head
    parents = run_git(["show", "-s", "--format=%P", head], context.repo).stdout.split()
    expected = [record.owned_source_head]
    allowed = False
    if record.pending_action == "merge":
        allowed = parents == [record.owned_source_head, record.target_head] or (
            head == record.target_head
            and run_git(
                ["merge-base", "--is-ancestor", record.owned_source_head or "", head],
                context.repo,
                check=False,
            ).returncode
            == 0
        )
    elif parents == expected and record.pending_action in {"doctor", "force", "sync"}:
        changes = tree_changes(context.repo, record.owned_source_head or "", head)
        paths = {path for change in changes for path in change.paths}
        if record.pending_action in {"sync", "doctor"}:
            allowed = _preparation_paths_match(record, paths) and all(
                change.status == "D"
                for change in changes
                if any(path.startswith(".cmoc/gu/") for path in change.paths)
            )
        else:
            allowed = (
                context.revert_base is not None
                and paths <= set(record.force_paths)
                and run_git(
                    [
                        "diff",
                        "--quiet",
                        head,
                        context.revert_base,
                        "--",
                        *[literal_pathspec(path) for path in record.force_paths],
                    ],
                    context.repo,
                    check=False,
                ).returncode
                == 0
            )
    if not allowed:
        raise CmocError(
            "取り込み元の準備変更の帰属を確認できません。",
            ["取り込み元の履歴と差分を確認してください。"],
            head,
        )
    return head


def _preparation_paths_match(record: MergeRecord, paths: set[str]) -> bool:
    # 管理更新の保留中に、無関係な差分を巻き込んで戻さない。
    if record.pending_action == "force":
        return paths <= set(record.force_paths)
    if record.pending_action == "sync":
        return paths <= {".cmoc/gt/realization/refactor/state.json"}
    if record.pending_action == "doctor":
        return all(
            path
            in {
                ".gitignore",
                ".cmoc/gt/config.json",
                ".cmoc/gt/realization/refactor/state.json",
            }
            or path.startswith(".agents/")
            or path.startswith(".cmoc/gu/")
            for path in paths
        )
    return record.pending_action == "merge" or not paths
