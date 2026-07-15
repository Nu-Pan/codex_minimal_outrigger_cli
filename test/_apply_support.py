from collections.abc import Mapping
from pathlib import Path


def apply_worktree_from_state(root: Path, state: Mapping[str, object]) -> Path:
    """Return the managed path encoded by an apply session state snapshot."""
    # {{work-root}}/oracle/doc/branch_model.md
    # {{work-root}}/oracle/doc/app_spec/session_state.md
    # Decode the specification directly so this expected path does not share
    # the production worktree lookup used by the behavior under test.
    apply_part = state.get("apply")
    if not isinstance(apply_part, dict):
        raise ValueError("missing apply state")
    apply_branch = apply_part.get("apply_branch")
    if not isinstance(apply_branch, str):
        raise ValueError("missing apply branch")
    parts = apply_branch.split("/")
    if len(parts) != 4 or parts[:2] != ["cmoc", "apply"] or not all(parts[2:]):
        raise ValueError(f"invalid apply branch: {apply_branch}")
    return root / ".cmoc" / "gu" / "worktree" / parts[2] / parts[3]
