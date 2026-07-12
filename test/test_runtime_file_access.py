"""FileAccessMode と binary 判定の契約を検証する。

根拠:
- <work-root>/oracle/src/oracle/acp_builder/basic.py
- <work-root>/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
"""

from pathlib import Path

from basic.acp import FileAccessMode
from cmoc_runtime import file_access_to_sandbox_mode
from commons.runtime_codex_profile import file_access_to_codex_cwd
from commons.runtime_content import is_binary


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


def test_file_access_to_codex_cwd_keeps_work_root_for_compatibility(
    tmp_path: Path,
) -> None:
    """Codex の作業 root は AgentCallParameter.cwd 側で指定する。"""
    root = tmp_path / "repo"
    root.mkdir()

    assert file_access_to_codex_cwd(FileAccessMode.READONLY, root) == root.resolve()
    assert file_access_to_codex_cwd(FileAccessMode.PURE_ORACLE_READ, root) == root.resolve()
    assert file_access_to_codex_cwd(FileAccessMode.PURE_ORACLE_WRITE, root) == root.resolve()


def test_is_binary_reads_only_initial_chunk() -> None:
    """binary 判定は大きい file 全体を読まず先頭 chunk だけを見る。"""
    class Reader:
        def __init__(self) -> None:
            self.size: int | None = None

        def __enter__(self) -> "Reader":
            return self

        def __exit__(self, *args: object) -> None:
            pass

        def read(self, size: int) -> bytes:
            self.size = size
            return b"text"

    class FakePath:
        def __init__(self) -> None:
            self.reader = Reader()

        def open(self, mode: str) -> Reader:
            assert mode == "rb"
            return self.reader

    path = FakePath()

    assert is_binary(path) is False
    assert path.reader.size == 4096
