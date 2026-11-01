"""run 資源の削除後にも残す join の進行記録と Git の照合。"""

import json
from dataclasses import dataclass
from pathlib import Path

from .runtime_errors import CmocError
from .runtime_git import head_commit
from .runtime_join import (
    MergeContext,
    MergeRecord,
    require_regular_record_path,
    save_merge_record,
    validate_merge_record,
)
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
class JoinRecord(MergeRecord):
    """共通の merge 記録に、run の identity と後処理の進行を結び付ける。"""

    context: EditingRunContext
    hook: str | None = None
    workload_post_join: bool = False

    @property
    def endpoints(self) -> MergeContext:
        """run → session の branch と worktree の対応を返す。"""
        context = self.context
        return MergeContext(
            context.repo,
            context.session_id,
            context.run_branch,
            context.run_worktree,
            context.session_branch,
            context.session_worktree,
            context.run_fork_commit,
        )

    def save(self) -> None:
        """run 資源を回収した後も使える場所へ復旧記録を保存する。"""
        save_merge_record(
            _record_path(self.context.repo, self.context.session_id), self
        )

    def report_fields(self) -> dict[str, object]:
        """復旧でも元の取り込み結果と準備の役割を保って報告する。"""
        # rollback 後も、その試行で確定していた基準と検証記録を報告する。
        attempt = (
            self.attempts[-1] if self.target_head is None and self.attempts else {}
        )
        session_head = self.target_head or attempt.get("target_head")
        prepared = self.prepared_head or attempt.get("prepared_head")
        sync_commit = self.sync_commit or attempt.get("sync_commit")
        fields: dict[str, object] = {
            "original_run_head": self.original_source_head,
            "baseline_session_head": session_head,
            "prepared_run_head": prepared,
            "join_diff_base": {"same_as": "run_fork_commit"},
            "join_diff_end": {"same_as": "original_run_head"},
            "run_join_commit": self.join_commit,
            "imported_session_commit": self.target_commit,
            "imported_session_tree": self.target_tree,
            "merge_status": ("merged" if self.join_commit else "no_op")
            if self.imported
            else "not_run",
            "refactor_state_sync_status": "rolled_back"
            if attempt and (prepared or sync_commit)
            else "completed"
            if self.prepared_head
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


@reuse_root_queries()
def load_join_record(repo: Path, session_id: str) -> JoinRecord | None:
    """通常 file の記録を読み、run identity と保存先の対応を確認する。"""
    # 配置探索だけを今回の読込内で共有し、保存内容・worktree 登録は毎回検証する。
    # 壊れた復旧情報を未作成として扱わない。
    path = _record_path(repo, session_id)
    require_regular_record_path(path)
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
        validate_merge_record(record)
        if type(record.workload_post_join) is not bool:
            raise ValueError("invalid workload_post_join")
        return record
    except (OSError, ValueError, TypeError, KeyError) as exc:
        raise CmocError("join 復旧記録を検証できません。", [], str(path)) from exc


def join_record(context: EditingRunContext) -> JoinRecord:
    """同じ run の記録を再利用し、新規 run では元の成果を先に固定する。"""
    # 記録の run identity を確認し、未完了の別 run を上書きしない。
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
    record = JoinRecord(context, original_source_head=head_commit(context.run_worktree))
    record.save()
    return record


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
