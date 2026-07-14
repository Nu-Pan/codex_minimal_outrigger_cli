"""TUI 起動 parameter builder の realization 側互換入口。"""

from oracle.acp_builder.basic import AgentCallParameter, FileAccessMode
from oracle.acp_builder.tui.launch_tui import (
    build_tui_launch_tui_parameter as _oracle_build_tui_launch_tui_parameter,
)

from basic.path_model import RootPathPlaceHolder, resolve_real_path
from commons.runtime_paths import logs_dir


def build_tui_launch_tui_parameter(
    time_stamp: str,
    role: str,
    summary: str,
    goal: str,
    file_access_mode: FileAccessMode,
    original_prompt: str,
    oracle_and_realization_basic: bool,
    oracle_standard: bool,
    realization_standard: bool,
    review_oracle_standard: bool,
    apply_review_standard: bool,
    index_entry_standard: bool,
) -> AgentCallParameter:
    """`cmoc tui` の TUI 起動用 AgentCallParameter を構築する。"""
    # {{work-root}}/oracle/doc/app_spec/sub_command/tui.md
    # oracle builder が正本だが保存先 directory を作らないため、呼び出し前に
    # runtime 側の配置だけ保証する。oracle 側で作成されるようになれば削除できる。
    repo = resolve_real_path(RootPathPlaceHolder.REPO)
    (logs_dir(repo).parent / "tui").mkdir(parents=True, exist_ok=True)
    return _oracle_build_tui_launch_tui_parameter(
        time_stamp,
        role,
        summary,
        goal,
        file_access_mode,
        original_prompt,
        oracle_and_realization_basic,
        oracle_standard,
        realization_standard,
        review_oracle_standard,
        apply_review_standard,
        index_entry_standard,
    )


__all__ = ["build_tui_launch_tui_parameter"]
