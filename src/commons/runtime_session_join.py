"""session join の identity、復旧記録、および未完了操作の境界。"""

import json
from dataclasses import dataclass
from pathlib import Path

from .runtime_errors import CmocError
from .runtime_join import (
    MergeContext,
    MergeRecord,
    require_regular_record_path,
    save_merge_record,
    validate_merge_record,
)
from .runtime_paths import repo_root, sessions_dir, work_root
from .runtime_state import load_state_for_branch, state_path


@dataclass
class SessionJoinRecord(MergeRecord):
    """session 資源の削除後も home への取り込みと後処理を追跡する。"""

    context: MergeContext

    @property
    def endpoints(self) -> MergeContext:
        """session → home の対応を返す。"""
        return self.context

    def save(self) -> None:
        """session branch に依存しない管理領域へ復旧記録を保存する。"""
        save_merge_record(
            _record_path(self.context.repo, self.context.session_id), self
        )

    def report_fields(self) -> dict[str, object]:
        """rollback 後も、その試行の call と機械検査の結果・基準を報告する。"""
        attempt = (
            self.attempts[-1] if self.target_head is None and self.attempts else {}
        )
        resolution = self.resolution or attempt.get("resolution", {})
        return {
            "session_branch": self.context.source_branch,
            "home_branch": self.context.target_branch,
            "session_branch_head_before_merge": self.original_source_head,
            "home_branch_head_before_merge": self.target_head
            or attempt.get("target_head"),
            "prepared_session_head": self.prepared_head or attempt.get("prepared_head"),
            "merge_commit": self.join_commit,
            "imported_home_commit": self.target_commit,
            "imported_home_tree": self.target_tree,
            "merge_status": "completed" if self.imported else "not_completed",
            "join_recovery": "post_join" if self.imported else "preparation",
            "conflict_resolution": resolution,
            "conflict_paths": [
                str(self.context.source_worktree / path)
                for path in resolution.get("initial_conflicts", [])
            ],
            "conflict_resolution_status": resolution.get("agent_status"),
            "conflict_resolution_result": (
                "confirmed" if resolution.get("verified_commit") else "not_confirmed"
            )
            if resolution.get("initial_conflicts")
            else None,
            "conflict_agent_report": resolution.get("agent_report"),
            "conflict_incidental_paths": resolution.get("incidental_paths", []),
            "conflict_call_log": resolution.get("call_log"),
            "session_preparation": "rolled_back"
            if attempt
            else "completed"
            if self.prepared_head
            else "not_completed",
        }


def _record_path(repo: Path, session_id: str) -> Path:
    # state_path は session ID を検証する。保存先は branch を削除しても残る。
    state_path(repo, session_id)
    return sessions_dir(repo) / "session_join" / f"{session_id}.json"


def load_session_join_record(repo: Path, session_id: str) -> SessionJoinRecord | None:
    """保存した identity と repository・worktree・session state の対応を検証する。"""
    path = _record_path(repo, session_id)
    require_regular_record_path(path)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if set(data) != set(SessionJoinRecord.__dataclass_fields__):
            raise ValueError("unexpected fields")
        context = data.pop("context")
        for key in ("repo", "source_worktree", "target_worktree"):
            context[key] = Path(context[key])
        record = SessionJoinRecord(context=MergeContext(**context), **data)
        validate_merge_record(record)
        identity = record.context
        if (
            identity.repo != repo
            or identity.session_id != session_id
            or identity.source_branch != f"cmoc/session/{session_id}"
            or identity.source_worktree != identity.target_worktree
            or not identity.source_worktree.is_absolute()
            or identity.source_worktree.resolve() != identity.source_worktree
            or (
                not record.finished
                and (
                    repo_root(identity.source_worktree) != repo
                    or work_root(identity.source_worktree) != identity.source_worktree
                )
            )
        ):
            raise ValueError("identity differs")
        _, _, state = load_state_for_branch(repo, identity.source_branch)
        if state.session.session_home_branch != identity.target_branch:
            raise ValueError("home branch differs")
        return record
    except (OSError, ValueError, TypeError, KeyError) as exc:
        raise CmocError(
            "session join 復旧記録を検証できません。", [], str(path)
        ) from exc


def pending_session_join(repo: Path, worktree: Path) -> SessionJoinRecord | None:
    """home へ切替済み・session 削除済みの場合も未完了の取り込みを特定する。"""
    directory = sessions_dir(repo) / "session_join"
    if directory.is_symlink():
        raise CmocError(
            "session join 復旧記録の directory が不正です。", [], str(directory)
        )
    pending: list[SessionJoinRecord] = []
    for path in directory.glob("*.json"):
        record = load_session_join_record(repo, path.stem)
        if (
            record is not None
            and not record.finished
            and record.context.source_worktree == worktree
        ):
            pending.append(record)
    if len(pending) > 1:
        raise CmocError(
            "未完了の session join を一意に特定できません。", [], str(directory)
        )
    return pending[0] if pending else None


def require_no_pending_session_join(repo: Path, worktree: Path) -> None:
    """未完了の取り込みを通常の編集や session 終了で上書きしない。"""
    record = pending_session_join(repo, worktree)
    if record is not None:
        raise CmocError(
            "session join の復旧を先に実行してください。",
            ["`cmoc session join` で未完了の準備または後処理を再開してください。"],
            record.context.source_branch,
        )
