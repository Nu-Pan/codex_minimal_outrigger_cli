"""FileAccessMode の永続化値を検証する。

根拠:
- {{work-root}}/reference/src/oracle/request_builder/basic.py

sandbox の全 mode 変換と未知 mode の拒否は test_runtime_codex_profile.py で検証する。
"""

from basic.acp import FileAccessMode


def test_file_access_mode_values_are_json_ready() -> None:
    """FileAccessMode の永続化値は JSON schema 側と共有できる文字列にする。"""
    assert FileAccessMode.READONLY.value == "readonly"
    assert FileAccessMode.PURE_ORACLE_READ.value == "pure_oracle_read"
    assert FileAccessMode.REPO_WRITE.value == "repo_write"
    assert FileAccessMode.PURE_ORACLE_WRITE.value == "pure_oracle_write"
    assert FileAccessMode.REALIZATION_WRITE.value == "realization_write"
    assert FileAccessMode.NO_POLICY.value == "no_policy"
