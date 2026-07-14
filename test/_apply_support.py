from pathlib import Path


def apply_worktree_from_state(root: Path, state: dict) -> Path:
    """Return the managed path encoded by an apply session state snapshot."""
    # {{work-root}}/oracle/doc/branch_model.md
    # {{work-root}}/oracle/doc/app_spec/session_state.md
    # Decode the specification directly so this expected path does not share
    # the production worktree lookup used by the behavior under test.
    parts = state["apply"]["apply_branch"].split("/")
    if len(parts) != 4 or parts[:2] != ["cmoc", "apply"] or not all(parts[2:]):
        raise ValueError(f"invalid apply branch: {state['apply']['apply_branch']}")
    return root / ".cmoc" / "gu" / "worktree" / parts[2] / parts[3]
