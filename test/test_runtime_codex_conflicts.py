"""session join conflict target の Codex write policy を検証する。

根拠:
- <work-root>/oracle/src/oracle/acp_builder/session/join/conflict_resolution.py
- <work-root>/oracle/src/oracle/prompt_builder/parts/file_access_rule.py
"""

from pathlib import Path

import pytest

from acp.builder.session.join.conflict_resolution import (
    build_session_join_conflict_resolution_parameter,
)
from cmoc_runtime import CmocError
from commons.runtime_codex_profile import build_codex_override_args
from config.cmoc_config import CmocConfig

from _codex_support import (
    _assert_writable,
    _override_permission_roots,
    _standard_realization_override_roots,
)


def test_codex_overrides_uses_file_roots_for_session_join_conflict_resolution(
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    (root / "src").mkdir()
    (root / "oracle").mkdir()
    target = root / "oracle" / "spec.md"
    target.write_text("conflict\n")

    override_args = build_codex_override_args(
        build_session_join_conflict_resolution_parameter([target]),
        CmocConfig(),
        root,
        extra_writable_paths=[target],
        allow_oracle_conflict_writes=True,
    )

    assert _override_permission_roots(override_args, "write") == {
        *_standard_realization_override_roots(root),
        str((root / "oracle").resolve()),
    }
    _assert_writable(override_args, target)


@pytest.mark.parametrize("extra", ["oracle/INDEX.md", "oracle/AGENTS.md"])
def test_codex_overrides_rejects_session_join_conflict_targets_with_denied_names(
    tmp_path: Path, extra: str
) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    (root / "src").mkdir()
    target = root / extra
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("conflict\n")

    with pytest.raises(CmocError, match="追加書き込み許可 path"):
        build_codex_override_args(
            build_session_join_conflict_resolution_parameter([target]),
            CmocConfig(),
            root,
            extra_writable_paths=[target],
            allow_oracle_conflict_writes=True,
        )


@pytest.mark.parametrize("extra", ["INDEX.md", "AGENTS.md"])
def test_codex_overrides_rejects_root_file_session_join_conflict_targets(
    tmp_path: Path, extra: str
) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    (root / "src").mkdir()
    target = root / extra
    target.write_text("conflict\n")

    with pytest.raises(CmocError, match="追加書き込み許可 path"):
        build_codex_override_args(
            build_session_join_conflict_resolution_parameter([target]),
            CmocConfig(),
            root,
            extra_writable_paths=[target],
            allow_oracle_conflict_writes=True,
        )


def test_codex_overrides_allows_root_readme_session_join_conflict_target(
    tmp_path: Path,
) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    (root / "src").mkdir()
    target = root / "README.md"
    target.write_text("conflict\n")

    override_args = build_codex_override_args(
        build_session_join_conflict_resolution_parameter([target]),
        CmocConfig(),
        root,
        extra_writable_paths=[target],
        allow_oracle_conflict_writes=True,
    )

    assert _override_permission_roots(override_args, "write") == {
        *_standard_realization_override_roots(root),
        str((root / "README.md").resolve()),
        str((root / "oracle").resolve()),
    }
    _assert_writable(override_args, target)


@pytest.mark.parametrize(
    "extra",
    [
        ".agents/blocked.md",
        ".cmoc/local/state.json",
        ".codex/config.toml",
        ".git/config",
        "memo/blocked.md",
    ],
)
def test_codex_overrides_rejects_runtime_paths_even_for_session_join_conflict(
    tmp_path: Path, extra: str
) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    (root / "src").mkdir()

    with pytest.raises(CmocError, match="追加書き込み許可 path"):
        build_codex_override_args(
            build_session_join_conflict_resolution_parameter([root / extra]),
            CmocConfig(),
            root,
            extra_writable_paths=[root / extra],
            allow_oracle_conflict_writes=True,
        )
