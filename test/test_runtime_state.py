"""session/apply state の形状と branch 解析を検証する。

根拠:
- <work-root>/oracle/doc/app_spec/session_state.md
- <work-root>/oracle/doc/app_spec/sub_command/session_join.md
"""

from pathlib import Path

import pytest

from cmoc_runtime import CmocError
from commons.runtime_state import (
    SessionState,
    apply_branch_session_id,
    branch_session_id,
    load_state_for_branch,
    state_path,
    write_state,
)


@pytest.mark.parametrize(
    "branch",
    [
        "cmoc/session/",
        "cmoc/session/2026-06-24_20-40_40_571606000/extra",
    ],
)
def test_branch_session_id_rejects_invalid_session_branch_shape(branch: str) -> None:
    """session branch 名の余分な区切りや空 session id を拒否する。"""
    with pytest.raises(CmocError):
        branch_session_id(branch)


@pytest.mark.parametrize(
    "branch",
    [
        "cmoc/apply/",
        "cmoc/apply/session",
        "cmoc/apply/session/run/extra",
    ],
)
def test_apply_branch_session_id_rejects_invalid_apply_branch_shape(branch: str) -> None:
    """apply branch 名は session id と run id の 2 要素だけを受け付ける。"""
    with pytest.raises(CmocError):
        apply_branch_session_id(branch)


def test_load_state_for_branch_rejects_apply_branch_with_extra_parts(tmp_path: Path) -> None:
    """破損した apply branch 名から session state を誤って読まない。"""
    path = state_path(tmp_path, "session")
    write_state(path, SessionState())

    with pytest.raises(CmocError):
        load_state_for_branch(tmp_path, "cmoc/apply/session/run/extra")


@pytest.mark.parametrize("part", ["session", "apply"])
@pytest.mark.parametrize("value", [[], {}])
def test_session_state_rejects_unhashable_state_values(
    part: str, value: object
) -> None:
    """session/apply state の state フィールドに list や dict を指定した入力を拒否する。"""
    data = SessionState().to_dict()
    data[part]["state"] = value

    with pytest.raises(CmocError) as exc_info:
        SessionState.from_dict(data)

    assert exc_info.value.summary == "session state file が不正です。"
    assert f"`{part}.state` が不正です" in exc_info.value.detail


@pytest.mark.parametrize(
    ("part", "field"),
    [
        ("session", "session_home_branch"),
        ("session", "session_start_commit"),
        ("session", "last_joined_apply_oracle_snapshot_commit"),
        ("session", "joined_at"),
        ("apply", "apply_branch"),
        ("apply", "oracle_snapshot_commit"),
    ],
)
@pytest.mark.parametrize("value", [[], {}, 1, False])
def test_session_state_rejects_non_string_payload_fields(
    part: str, field: str, value: object
) -> None:
    """session state の payload フィールドに非文字列値を指定した入力を拒否する。"""
    data = SessionState().to_dict()
    data[part][field] = value

    with pytest.raises(CmocError) as exc_info:
        SessionState.from_dict(data)

    assert exc_info.value.summary == "session state file が不正です。"
    assert f"`{part}.{field}` は string または null" in exc_info.value.detail


@pytest.mark.parametrize("part", ["session", "apply"])
def test_session_state_allows_nullable_payload_fields(part: str) -> None:
    """session state の payload フィールドに null を指定した入力を受け付ける。"""
    data = SessionState().to_dict()
    for field in data[part]:
        if field != "state":
            data[part][field] = None

    SessionState.from_dict(data)
