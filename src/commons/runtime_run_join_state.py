"""run 資源の削除後にも残す join の進行記録と Git の照合。"""

import json
import os
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .runtime_errors import CmocError
from .runtime_git import head_commit, run_git
from .runtime_paths import reuse_root_queries, sessions_dir
from .runtime_run_lifecycle import EditingRunContext
from .runtime_state import (
    RunPart,
    branch_session_id,
    load_state_for_branch,
    run_branch_session_id,
    write_state,
)


@dataclass
class JoinRecord:
    """元の成果、準備、取り込み、後処理を同じ run identity に結び付ける。"""

    context: EditingRunContext
    original_run_head: str
    session_head: str | None = None
    prepared_run_head: str | None = None
    sync_commit: str | None = None
    resolution: dict[str, object] = field(default_factory=dict)
    preparation_started: bool = False
    owned_run_head: str | None = None
    pending_action: str | None = None
    force_paths: list[str] = field(default_factory=list)
    attempts: list[dict[str, object]] = field(default_factory=list)
    imported: bool = False
    join_commit: str | None = None
    session_commit: str | None = None
    session_tree: str | None = None
    hook: str | None = None
    workload_post_join: bool = False
    finished: bool = False

    def __post_init__(self) -> None:
        # 新規記録の帰属の起点は、固定した元の成果だけとする。
        if self.owned_run_head is None:
            self.owned_run_head = self.original_run_head

    def save(self) -> None:
        """置換と directory flush を終えてから次の不可逆操作へ進む。"""
        # run worktree と独立した session 管理領域へ atomic に保存する。
        path = _record_path(self.context.repo, self.context.session_id)
        _require_regular_path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = asdict(self)
        data["context"] = {
            key: str(value) if isinstance(value, Path) else value
            for key, value in asdict(self.context).items()
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

    def report_fields(self) -> dict[str, object]:
        """復旧でも元の取り込み結果と準備の役割を保って報告する。"""
        # rollback 後も、その試行で確定していた基準と検証記録を報告する。
        attempt = (
            self.attempts[-1] if self.session_head is None and self.attempts else {}
        )
        session_head = self.session_head or attempt.get("session_head")
        prepared = self.prepared_run_head or attempt.get("prepared_run_head")
        sync_commit = self.sync_commit or attempt.get("sync_commit")
        fields: dict[str, object] = {
            "original_run_head": self.original_run_head,
            "baseline_session_head": session_head,
            "prepared_run_head": prepared,
            "join_diff_base": {"same_as": "run_fork_commit"},
            "join_diff_end": {"same_as": "original_run_head"},
            "run_join_commit": self.join_commit,
            "imported_session_commit": self.session_commit,
            "imported_session_tree": self.session_tree,
            "merge_status": ("merged" if self.join_commit else "no_op")
            if self.imported
            else "not_run",
            "refactor_state_sync_status": "rolled_back"
            if attempt and (prepared or sync_commit)
            else "completed"
            if self.prepared_run_head
            else "not_run",
            "refactor_state_sync_commit": sync_commit,
            "run_preparation": "rolled_back"
            if attempt
            else "completed"
            if prepared
            else "not_run",
            "preparation_validation": "completed" if prepared else "not_run",
            "conflict_resolution": self.resolution or attempt.get("resolution", {}),
        }
        # 複数の役割を持つ commit は既存の役割を参照し、同じ ID を再掲載しない。
        seen = {
            self.context.session_fork_commit: "session_fork_commit",
            self.context.run_fork_commit: "run_fork_commit",
        }
        for name in (
            "run_join_commit",
            "refactor_state_sync_commit",
            "original_run_head",
            "baseline_session_head",
            "prepared_run_head",
            "imported_session_commit",
        ):
            value = fields[name]
            if isinstance(value, str):
                if value in seen:
                    fields[name] = {"same_as": seen[value]}
                else:
                    seen[value] = name
        return fields


def _record_path(repo: Path, session_id: str) -> Path:
    return sessions_dir(repo) / "join" / f"{session_id}.json"


def _require_regular_path(path: Path) -> None:
    if any(parent.is_symlink() for parent in (path, *path.parents)) or (
        path.exists() and not path.is_file()
    ):
        raise CmocError("join 復旧記録の path が不正です。", [], str(path))


def load_join_record(repo: Path, session_id: str) -> JoinRecord | None:
    """通常 file の記録を読み、run identity と保存先の対応を確認する。"""
    # 壊れた復旧情報を未作成として扱わない。
    path = _record_path(repo, session_id)
    _require_regular_path(path)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if set(data) != set(JoinRecord.__dataclass_fields__):
            raise ValueError("unexpected fields")
        context = data.pop("context")
        for key in ("repo", "session_worktree", "state_path", "run_worktree"):
            context[key] = Path(context[key])
        record = JoinRecord(context=EditingRunContext(**context), **data)
        if record.context.repo != repo or record.context.session_id != session_id:
            raise ValueError("identity differs")
        from .runtime_run import expected_run_worktree, worktree_for_branch
        from .runtime_state import state_path

        if (
            record.context.session_branch != f"cmoc/session/{session_id}"
            or record.context.state_path != state_path(repo, session_id)
            or record.context.run_worktree
            != expected_run_worktree(repo, record.context.run_branch)
            or record.context.session_worktree
            != worktree_for_branch(repo, record.context.session_branch)
        ):
            raise ValueError("managed paths differ")
        for name in (
            "original_run_head",
            "session_head",
            "prepared_run_head",
            "sync_commit",
            "join_commit",
            "session_commit",
            "session_tree",
            "owned_run_head",
        ):
            value = getattr(record, name)
            if value is not None and (
                not isinstance(value, str)
                or len(value) != 40
                or any(char not in "0123456789abcdef" for char in value)
            ):
                raise ValueError(f"invalid {name}")
        if record.original_run_head is None or not isinstance(record.resolution, dict):
            raise ValueError("invalid outcome")
        for name in (
            "preparation_started",
            "imported",
            "workload_post_join",
            "finished",
        ):
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
            or set(attempt)
            != {"session_head", "prepared_run_head", "sync_commit", "resolution"}
            for attempt in record.attempts
        ):
            raise ValueError("invalid preparation history")
        return record
    except (OSError, ValueError, TypeError, KeyError) as exc:
        raise CmocError("join 復旧記録を検証できません。", [], str(path)) from exc


@reuse_root_queries()
def join_record(context: EditingRunContext) -> JoinRecord:
    """同じ run の記録を再利用し、新規 run では元の成果を先に固定する。"""
    # 配置の探索だけを取得内で共有し、保存内容・worktree 登録は毎回検証する。
    record = load_join_record(context.repo, context.session_id)
    if record is not None and record.context.run_branch == context.run_branch:
        if (
            record.context.kind != context.kind
            or record.context.run_fork_commit != context.run_fork_commit
        ):
            raise CmocError("join 復旧記録と run identity が一致しません。", [], "")
        return record
    if record is not None and not record.finished:
        raise CmocError("別 run の join 後処理が未完了です。", [], "")
    record = JoinRecord(context, head_commit(context.run_worktree))
    record.save()
    return record


def tree_id(root: Path, commit: str) -> str:
    """記録した commit の tree を取得する。"""
    return run_git(["rev-parse", f"{commit}^{{tree}}"], root).stdout.strip()


def confirm_import(record: JoinRecord) -> bool:
    """保存直前の停止も、両 parent と tree の一致から取り込みを確認する。"""
    # 到達可能性だけでは、準備や別の取り込みを成功と読み替えない。
    context = record.context
    if record.imported:
        if (
            record.session_commit is None
            or record.session_tree is None
            or record.prepared_run_head is None
            or record.session_head is None
        ):
            raise CmocError("join の取り込み記録が不完全です。", [], "")
        # 同じ immutable commit の tree と親を、照合ごとに一括で取り直す。
        commits = run_git(
            [
                "log",
                "--no-walk=unsorted",
                "--format=%H %T %P",
                record.session_commit,
                record.prepared_run_head,
            ],
            context.repo,
        ).stdout.splitlines()
        metadata = {
            fields[0]: fields[1:] for line in commits if (fields := line.split())
        }
        if (
            record.session_commit not in metadata
            or record.prepared_run_head not in metadata
            or metadata[record.session_commit][0] != record.session_tree
            or metadata[record.prepared_run_head][0] != record.session_tree
            or run_git(
                [
                    "merge-base",
                    "--is-ancestor",
                    record.session_commit,
                    context.session_branch,
                ],
                context.repo,
                check=False,
            ).returncode
            != 0
        ):
            raise CmocError("記録した取り込み成果を確認できません。", [], "")
        if record.join_commit is None:
            valid = (
                record.session_commit == record.session_head == record.prepared_run_head
            )
        else:
            valid = record.join_commit == record.session_commit and metadata[
                record.session_commit
            ][1:] == [record.session_head, record.prepared_run_head]
        if not valid:
            raise CmocError("join の取り込み履歴と基準が一致しません。", [], "")
        return True
    if record.prepared_run_head is None or record.session_head is None:
        return False
    commits = run_git(
        [
            "log",
            "--first-parent",
            "--format=%H %T %P",
            f"{record.session_head}..{context.session_branch}",
        ],
        context.repo,
    ).stdout.splitlines()
    # 親と tree を履歴と一括取得し、候補ごとの process 起動を避ける。
    candidates = [
        (fields[0], fields[1])
        for line in commits
        if (fields := line.split())[2:]
        == [record.session_head, record.prepared_run_head]
    ]
    if not candidates:
        return False
    prepared_tree = tree_id(context.repo, record.prepared_run_head)
    matches = [commit for commit, tree in candidates if tree == prepared_tree]
    if len(matches) > 1:
        raise CmocError("join の取り込み成立を一意に確認できません。", [], "")
    if not matches:
        return False
    record.imported = True
    record.join_commit = record.session_commit = matches[0]
    record.session_tree = prepared_tree
    record.save()
    return True


def restore_pending_join(repo: Path, branch: str) -> JoinRecord | None:
    """ready 初期化後の停止を、新しい run や session 終了の前に復元する。"""
    # 呼び出し入口でのみ使用し、cleanup 中の ready を active に戻さない。
    if not branch.startswith(("cmoc/session/", "cmoc/run/")):
        return None
    session_id = (
        branch_session_id(branch)
        if branch.startswith("cmoc/session/")
        else run_branch_session_id(branch)
    )
    record = load_join_record(repo, session_id)
    if record is None or record.finished:
        return None
    from .runtime_run import run_lifecycle_lock

    with run_lifecycle_lock(repo, session_id):
        record = load_join_record(repo, session_id)
        if record is None or record.finished:
            return None
        _, path, state = load_state_for_branch(repo, branch)
        if state.run.state == "ready":
            state.run = RunPart(
                "error",
                record.context.kind,
                record.context.run_branch,
                record.context.run_fork_commit,
            )
            write_state(path, state)
        elif state.run.branch != record.context.run_branch:
            raise CmocError("未完了 join と active run が一致しません。", [], str(path))
        return record
