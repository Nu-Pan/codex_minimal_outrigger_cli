"""FileAccessMode の Codex sandbox 変換契約を検証する。

根拠:
- <work-root>/oracle/src/oracle/acp_builder/basic.py
- <work-root>/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
"""

from basic.acp import FileAccessMode
from cmoc_runtime import file_access_to_sandbox_mode


def test_file_access_mode_values_are_json_ready() -> None:
    """FileAccessMode の永続化値は JSON schema 側と共有できる文字列にする。"""
    assert FileAccessMode.READONLY.value == "readonly"
    assert FileAccessMode.PURE_ORACLE_READ.value == "pure_oracle_read"
    assert FileAccessMode.REPO_WRITE.value == "repo_write"
    assert FileAccessMode.PURE_ORACLE_WRITE.value == "pure_oracle_write"
    assert FileAccessMode.REALIZATION_WRITE.value == "realization_write"


def test_file_access_to_sandbox_mode_supports_repo_write() -> None:
    """repo write mode まで Codex sandbox mode へ欠落なく変換する。"""
    assert file_access_to_sandbox_mode(FileAccessMode.READONLY) == "read-only"
    assert file_access_to_sandbox_mode(FileAccessMode.PURE_ORACLE_READ) == "read-only"
    assert file_access_to_sandbox_mode(FileAccessMode.REALIZATION_WRITE) == "workspace-write"
    assert file_access_to_sandbox_mode(FileAccessMode.PURE_ORACLE_WRITE) == "workspace-write"
    assert file_access_to_sandbox_mode(FileAccessMode.REPO_WRITE) == "workspace-write"
