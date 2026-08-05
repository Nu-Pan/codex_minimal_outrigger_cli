"""oracle edit の正本 TUI builder を呼び出す realization adapter。"""

from oracle.acp_builder.basic import AgentCallParameter as _AgentCallParameter
from oracle.acp_builder.oracle.edit.launch_tui import (
    build_oracle_edit_launch_tui_parameter as _build_parameter,
)

from basic.path_model import RootPathPlaceHolder as _RootPathPlaceHolder
from basic.path_model import resolve_real_path as _resolve_real_path
from commons.runtime_paths import editor_input_dir as _editor_input_dir


def build_oracle_edit_launch_tui_parameter(
    time_stamp: str,
    user_instruction: str,
) -> _AgentCallParameter:
    """正本 builder が完全 prompt を保存する directory を準備する。

    根拠: {{work-root}}/oracle/src/oracle/acp_builder/oracle/edit/launch_tui.py
    """
    repo = _resolve_real_path(_RootPathPlaceHolder.REPO)
    _editor_input_dir(repo).mkdir(parents=True, exist_ok=True)
    return _build_parameter(time_stamp, user_instruction)


__all__ = ["build_oracle_edit_launch_tui_parameter"]
