import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from commons.runtime_errors import CmocError
from commons.runtime_paths import sessions_dir


@dataclass
class SessionPart:
    state: str = "active"
    session_home_branch: str | None = None
    session_start_commit: str | None = None
    last_joined_apply_join_commit: str | None = None
    joined_at: str | None = None


@dataclass
class ApplyPart:
    state: str = "ready"
    apply_branch: str | None = None
    oracle_snapshot_commit: str | None = None


@dataclass
class SessionState:
    session: SessionPart = field(default_factory=SessionPart)
    apply: ApplyPart = field(default_factory=ApplyPart)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SessionState":
        session_data = {
            key: value
            for key, value in data.get("session", {}).items()
            if key in SessionPart.__dataclass_fields__
        }
        apply_data = {
            key: value
            for key, value in data.get("apply", {}).items()
            if key in ApplyPart.__dataclass_fields__
        }
        return cls(
            session=SessionPart(**session_data),
            apply=ApplyPart(**apply_data),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def state_path(root: Path, session_id: str) -> Path:
    return sessions_dir(root) / f"{session_id}.json"


def branch_session_id(branch: str, kind: str = "session") -> str:
    prefix = f"cmoc/{kind}/"
    if not branch.startswith(prefix):
        raise CmocError(
            f"現在の branch は cmoc {kind} branch ではありません。",
            [f"`cmoc {kind}` 系コマンドを cmoc {kind} branch 上で実行してください。"],
            f"current branch: {branch}",
        )
    return branch.removeprefix(prefix).split("/", 1)[0]


def load_state_for_branch(root: Path, branch: str) -> tuple[str, Path, SessionState]:
    if branch.startswith("cmoc/session/"):
        session_id = branch_session_id(branch, "session")
    elif branch.startswith("cmoc/apply/"):
        parts = branch.split("/")
        if len(parts) < 4:
            raise CmocError(
                "apply branch 名から session-id を特定できません。",
                ["branch 名と session state file を確認してください。"],
                f"branch: {branch}",
            )
        session_id = parts[2]
    else:
        raise CmocError(
            "現在の branch は cmoc 管理 branch ではありません。",
            ["cmoc session branch または cmoc apply branch 上で再実行してください。"],
            f"current branch: {branch}",
        )
    path = state_path(root, session_id)
    if not path.is_file():
        raise CmocError(
            "session state file が存在しません。",
            ["対象 session が正しく作成されているか確認してください。"],
            str(path),
        )
    return session_id, path, SessionState.from_dict(json.loads(path.read_text()))


def write_state(path: Path, state: SessionState) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state.to_dict(), ensure_ascii=False, indent=2) + "\n")


def active_session_for_home(root: Path, home_branch: str) -> Path | None:
    for path in sessions_dir(root).glob("*.json"):
        state = SessionState.from_dict(json.loads(path.read_text()))
        if (
            state.session.state == "active"
            and state.session.session_home_branch == home_branch
        ):
            return path
    return None
