import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from commons.runtime_errors import CmocError
from commons.runtime_paths import sessions_dir


@dataclass
class SessionPart:
    """session branch と home branch の関係を保存する state 断片。"""

    state: str = "active"
    session_home_branch: str | None = None
    session_start_commit: str | None = None
    last_joined_apply_oracle_snapshot_commit: str | None = None
    # <work-root>/oracle/doc/app_spec/sub_command/session_abandon.md
    # session abandon requires this field to remain serialized as JSON null.
    joined_at: str | None = None


@dataclass
class ApplyPart:
    """active session にぶら下がる apply run の進行状態を保存する state 断片。"""

    state: str = "ready"
    apply_branch: str | None = None
    oracle_snapshot_commit: str | None = None


@dataclass
class SessionState:
    """session state file 全体を表す永続化用の集約 state。"""

    session: SessionPart = field(default_factory=SessionPart)
    apply: ApplyPart = field(default_factory=ApplyPart)

    @classmethod
    def from_dict(
        cls: type["SessionState"], data: dict[str, Any], source: Path | None = None
    ) -> "SessionState":
        # <work-root>/oracle/doc/app_spec/session_state.md
        # JSON 読み込み時は、新規作成用 default で欠落 field を active/ready に補わない。
        if not isinstance(data, dict):
            raise _invalid_state(source, "top-level JSON は object である必要があります。")
        session_data = _part_data(data, "session", SessionPart, source)
        apply_data = _part_data(data, "apply", ApplyPart, source)
        _require_state(
            session_data, "session", {"active", "joined", "abandoned", "error"}, source
        )
        _require_state(
            apply_data, "apply", {"ready", "running", "completed", "error"}, source
        )
        _require_nullable_strings(session_data, "session", source)
        _require_nullable_strings(apply_data, "apply", source)
        return cls(
            session=SessionPart(**session_data),
            apply=ApplyPart(**apply_data),
        )

    def to_dict(self) -> dict[str, Any]:
        """JSON 保存に使う素朴な dict 構造へ変換する。"""
        return asdict(self)


def state_path(root: Path, session_id: str) -> Path:
    """session_id に対応する session state file の保存先を返す。"""
    return sessions_dir(root) / f"{session_id}.json"


def branch_session_id(branch: str, kind: str = "session") -> str:
    """cmoc 管理 branch 名から session_id を取り出す。"""
    prefix = f"cmoc/{kind}/"
    if not branch.startswith(prefix):
        raise CmocError(
            f"現在の branch は cmoc {kind} branch ではありません。",
            [f"`cmoc {kind}` 系コマンドを cmoc {kind} branch 上で実行してください。"],
            f"current branch: {branch}",
        )
    parts = branch.split("/")
    if len(parts) != 3 or not parts[2]:
        raise CmocError(
            f"{kind} branch 名から session-id を特定できません。",
            ["branch 名と session state file を確認してください。"],
            f"branch: {branch}",
        )
    return parts[2]


def apply_branch_session_id(branch: str) -> str:
    """cmoc apply branch 名から session_id を取り出す。"""
    parts = branch.split("/")
    if (
        len(parts) != 4
        or parts[:2] != ["cmoc", "apply"]
        or not parts[2]
        or not parts[3]
    ):
        raise CmocError(
            "apply branch 名から session-id を特定できません。",
            ["branch 名と session state file を確認してください。"],
            f"branch: {branch}",
        )
    return parts[2]


def load_state_for_branch(root: Path, branch: str) -> tuple[str, Path, SessionState]:
    """現在 branch に対応する session state file を読み込む。"""
    if branch.startswith("cmoc/session/"):
        session_id = branch_session_id(branch, "session")
    elif branch.startswith("cmoc/apply/"):
        session_id = apply_branch_session_id(branch)
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
    return session_id, path, SessionState.from_dict(json.loads(path.read_text()), path)


def write_state(path: Path, state: SessionState) -> None:
    """session state file を canonical JSON 形式で書き戻す。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state.to_dict(), ensure_ascii=False, indent=2) + "\n")


def active_session_for_home(root: Path, home_branch: str) -> Path | None:
    """home branch に紐づく active session state file を探す。"""
    for path in sessions_dir(root).glob("*.json"):
        state = SessionState.from_dict(json.loads(path.read_text()), path)
        if (
            state.session.state == "active"
            and state.session.session_home_branch == home_branch
        ):
            return path
    return None


def _part_data(
    data: dict[str, Any],
    key: str,
    part_type: type[SessionPart] | type[ApplyPart],
    source: Path | None,
) -> dict[str, Any]:
    part = data.get(key)
    if not isinstance(part, dict):
        raise _invalid_state(source, f"`{key}` は object である必要があります。")
    fields = part_type.__dataclass_fields__
    missing = [field for field in fields if field not in part]
    if missing:
        raise _invalid_state(
            source, f"`{key}` に必須 field がありません: {', '.join(missing)}"
        )
    return {field: part[field] for field in fields}


def _require_state(
    part: dict[str, Any], key: str, allowed: set[str], source: Path | None
) -> None:
    state = part["state"]
    if not isinstance(state, str) or state not in allowed:
        raise _invalid_state(
            source,
            f"`{key}.state` が不正です: {state!r}; allowed: {', '.join(sorted(allowed))}",
        )


def _require_nullable_strings(
    part: dict[str, Any], key: str, source: Path | None
) -> None:
    for field, value in part.items():
        if field != "state" and value is not None and not isinstance(value, str):
            raise _invalid_state(
                source,
                f"`{key}.{field}` は string または null である必要があります: {value!r}",
            )


def _invalid_state(source: Path | None, reason: str) -> CmocError:
    detail = f"{source}\n{reason}" if source else reason
    return CmocError(
        "session state file が不正です。",
        ["session state file を確認し、schema に従って修復してください。"],
        detail,
    )
