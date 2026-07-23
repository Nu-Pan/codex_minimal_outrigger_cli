"""oracle investigation の正本 builder を呼ぶ realization adapter。"""

from oracle.acp_builder.basic import AgentCallParameter
from oracle.acp_builder.oracle.investigation.launch_tui import (
    build_oracle_investigation_launch_tui_parameter as _build_parameter,
)

from basic.path_model import RootPathPlaceHolder, resolve_real_path
from commons.runtime_paths import editor_input_dir


def build_oracle_investigation_launch_tui_parameter(
    time_stamp: str,
    user_instruction: str,
) -> AgentCallParameter:
    """正本 builder が完全 prompt を保存する directory を準備する。

    根拠: {{work-root}}/oracle/src/oracle/acp_builder/oracle/investigation/launch_tui.py
    """
    repo = resolve_real_path(RootPathPlaceHolder.REPO)
    editor_input_dir(repo).mkdir(parents=True, exist_ok=True)
    return _build_parameter(time_stamp, user_instruction)


__all__ = ["build_oracle_investigation_launch_tui_parameter"]
