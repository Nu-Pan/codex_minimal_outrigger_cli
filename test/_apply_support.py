from pathlib import Path


def apply_worktree_from_state(root: Path, state: dict) -> Path:
    """apply session state snapshot に記録された managed path を返す。"""
    # {{work-root}}/oracle/doc/branch_model.md
    # {{work-root}}/oracle/doc/app_spec/session_state.md
    # 期待 path がテスト対象の production worktree lookup を共有しないよう、仕様を直接
    # decode する。
    parts = state["apply"]["apply_branch"].split("/")
    if len(parts) != 4 or parts[:2] != ["cmoc", "apply"] or not all(parts[2:]):
        raise ValueError(f"invalid apply branch: {state['apply']['apply_branch']}")
    return root / ".cmoc" / "gu" / "worktree" / parts[2] / parts[3]
