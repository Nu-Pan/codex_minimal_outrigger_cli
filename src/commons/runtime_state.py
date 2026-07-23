import fcntl
import json
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from commons.runtime_errors import CmocError
from commons.runtime_git import git_common_dir
from commons.runtime_paths import sessions_dir

SESSION_STATES = {"active", "joined", "abandoned", "error"}
RUN_STATES = {"ready", "running", "joinable", "error"}
RUN_KINDS = {"realization_apply", "realization_refactor"}


@dataclass
class SessionPart:
    """session branch と home branch の lifecycle state。"""

    state: str = "active"
    session_home_branch: str | None = None
    session_fork_commit: str | None = None
    last_joined_apply_fork_commit: str | None = None


@dataclass
class RunPart:
    """active session が高々一つ保持する editing run state。"""

    state: str = "ready"
    kind: str | None = None
    branch: str | None = None
    fork_commit: str | None = None


@dataclass
class SessionState:
    """`{{work-root}}/oracle/doc/app_spec/session_state.md` の永続 state。"""

    session: SessionPart = field(default_factory=SessionPart)
    run: RunPart = field(default_factory=RunPart)

    @classmethod
    def from_dict(
        cls: type["SessionState"], data: dict[str, Any], source: Path | None = None
    ) -> "SessionState":
        """欠落 field を補わず、正本 schema に一致する JSON object を復元する。"""
        if not isinstance(data, dict):
            raise _invalid_state(
                source, "top-level JSON は object である必要があります。"
            )
        session_data = _part_data(data, "session", SessionPart, source)
        run_data = _part_data(data, "run", RunPart, source)
        _require_state(session_data, "session", SESSION_STATES, source)
        _require_state(run_data, "run", RUN_STATES, source)
        _require_nullable_strings(session_data, "session", source)
        _require_session_identity(session_data, source)
        _require_nullable_strings(run_data, "run", source)
        _validate_run_fields(run_data, source)
        return cls(SessionPart(**session_data), RunPart(**run_data))

    def to_dict(self) -> dict[str, Any]:
        """JSON 保存用の正本と同形の object を返す。"""
        return asdict(self)


def state_path(root: Path, session_id: str) -> Path:
    """session_id に対応する session state file の保存先を返す。"""
    return sessions_dir(root) / f"{session_id}.json"


@contextmanager
def session_fork_lock(root: Path) -> Iterator[None]:
    """repository 共通の session fork 排他 lock を保持する。"""
    lock_path = git_common_dir(root) / "cmoc-session-fork.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+") as lock_file:
        # {{work-root}}/oracle/doc/app_spec/sub_command/session_fork.md
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def branch_session_id(branch: str) -> str:
    """cmoc session branch 名から session-id を取り出す。"""
    prefix = "cmoc/session/"
    parts = branch.split("/")
    if not branch.startswith(prefix) or len(parts) != 3 or not parts[2]:
        raise CmocError(
            "session branch 名から session-id を特定できません。",
            ["branch 名と session state file を確認してください。"],
            f"branch: {branch}",
        )
    return parts[2]


def run_branch_session_id(branch: str) -> str:
    """`cmoc/run/{{session-id}}/{{run-id}}` から session-id を取り出す。"""
    parts = branch.split("/")
    if len(parts) != 4 or parts[:2] != ["cmoc", "run"] or not parts[2] or not parts[3]:
        raise CmocError(
            "run branch 名から session-id を特定できません。",
            ["branch 名と session state file を確認してください。"],
            f"branch: {branch}",
        )
    return parts[2]


def load_state_for_branch(root: Path, branch: str) -> tuple[str, Path, SessionState]:
    """session branch または run branch に対応する state を読み込む。"""
    if branch.startswith("cmoc/session/"):
        session_id = branch_session_id(branch)
    elif branch.startswith("cmoc/run/"):
        session_id = run_branch_session_id(branch)
    else:
        raise CmocError(
            "現在の branch は cmoc 管理 branch ではありません。",
            ["cmoc session branch または active run branch 上で再実行してください。"],
            f"current branch: {branch}",
        )
    path = state_path(root, session_id)
    data = _read_state_data(path)
    return session_id, path, SessionState.from_dict(data, path)


def load_session_part_for_branch(
    root: Path, branch: str
) -> tuple[str, Path, SessionPart]:
    """session branch に対応する session 部分だけを検証して読み込む。

    根拠: {{work-root}}/oracle/doc/app_spec/sub_command/oracle_edit.md
    """
    session_id = branch_session_id(branch)
    path = state_path(root, session_id)
    data = _read_state_data(path)
    session_data = _part_data(data, "session", SessionPart, path)
    _require_state(session_data, "session", SESSION_STATES, path)
    _require_nullable_strings(session_data, "session", path)
    _require_session_identity(session_data, path)
    return session_id, path, SessionPart(**session_data)


def _read_state_data(path: Path) -> dict[str, Any]:
    """session state file を JSON object として読み込む。"""
    if not path.is_file():
        raise CmocError(
            "session state file が存在しません。",
            ["対象 session が正しく作成されているか確認してください。"],
            str(path),
        )
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise _invalid_state(path, "JSON 構文が不正です。") from exc
    if not isinstance(data, dict):
        raise _invalid_state(path, "top-level JSON は object である必要があります。")
    return data


def write_state(path: Path, state: SessionState) -> None:
    """session state を安定した JSON 表現で保存する。"""
    validated = SessionState.from_dict(state.to_dict(), path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(validated.to_dict(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def active_session_for_home(root: Path, home_branch: str) -> Path | None:
    """home branch に紐づく active session state file を探す。"""
    for path in sessions_dir(root).glob("*.json"):
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            raise _invalid_state(path, "JSON 構文が不正です。") from exc
        state = SessionState.from_dict(data, path)
        if (
            state.session.state == "active"
            and state.session.session_home_branch == home_branch
        ):
            return path
    return None


def _part_data(
    data: dict[str, Any],
    key: str,
    part_type: type[SessionPart] | type[RunPart],
    source: Path | None,
) -> dict[str, Any]:
    """state part を必須 field だけの dict として検証する。"""
    part = data.get(key)
    if not isinstance(part, dict):
        raise _invalid_state(source, f"`{key}` は object である必要があります。")
    fields = part_type.__dataclass_fields__
    missing = [name for name in fields if name not in part]
    extra = [name for name in part if name not in fields]
    if missing or extra:
        details = []
        if missing:
            details.append(f"必須 field がありません: {', '.join(missing)}")
        if extra:
            details.append(f"未定義 field があります: {', '.join(extra)}")
        raise _invalid_state(source, f"`{key}` に" + " / ".join(details))
    return {name: part[name] for name in fields}


def _require_state(
    part: dict[str, Any], key: str, allowed: set[str], source: Path | None
) -> None:
    value = part["state"]
    if not isinstance(value, str) or value not in allowed:
        raise _invalid_state(
            source,
            f"`{key}.state` が不正です: {value!r}; allowed: {', '.join(sorted(allowed))}",
        )


def _require_nullable_strings(
    part: dict[str, Any], key: str, source: Path | None
) -> None:
    for name, value in part.items():
        if name != "state" and value is not None and not isinstance(value, str):
            raise _invalid_state(
                source,
                f"`{key}.{name}` は string または null である必要があります: {value!r}",
            )


def _require_session_identity(session: dict[str, Any], source: Path | None) -> None:
    """永続 state に必要な session の fork 元情報を検証する。

    根拠: {{work-root}}/oracle/doc/app_spec/session_state.md
    """
    for name in ("session_home_branch", "session_fork_commit"):
        if not isinstance(session[name], str):
            raise _invalid_state(
                source,
                f"`session.{name}` は string である必要があります: {session[name]!r}",
            )


def _validate_run_fields(run: dict[str, Any], source: Path | None) -> None:
    """ready と active run の payload 不変条件を検証する。"""
    payload = (run["kind"], run["branch"], run["fork_commit"])
    if run["state"] == "ready":
        if any(value is not None for value in payload):
            raise _invalid_state(
                source, "`run.state=ready` の active run field は null です。"
            )
        return
    if run["kind"] not in RUN_KINDS or any(value is None for value in payload[1:]):
        raise _invalid_state(
            source,
            "active run には有効な kind, branch, fork_commit が必要です。",
        )


def _invalid_state(source: Path | None, reason: str) -> CmocError:
    detail = f"{source}\n{reason}" if source else reason
    return CmocError(
        "session state file が不正です。",
        ["session state file を確認し、schema に従って修復してください。"],
        detail,
    )
