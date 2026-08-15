"""oracle edit の正本 exec builder を呼び出す realization adapter。"""

from oracle.acp_builder.basic import AgentCallParameter as _AgentCallParameter
from oracle.acp_builder.oracle.edit.launch_exec import (
    build_oracle_edit_main_launch_exec_parameter as _build_main_parameter,
)
from oracle.acp_builder.oracle.edit.launch_exec import (
    build_oracle_edit_reduction_launch_exec_parameter as _build_reduction_parameter,
)

from basic.path_model import RootPathPlaceHolder as _RootPathPlaceHolder
from basic.path_model import resolve_real_path as _resolve_real_path
from commons.runtime_paths import editor_input_log_dir as _editor_input_log_dir


def build_oracle_edit_main_launch_exec_parameter(
    time_stamp: str,
    user_instruction: str,
) -> _AgentCallParameter:
    """正本 builder が完全 prompt を保存する directory を準備する。

    根拠: {{work-root}}/oracle/src/oracle/acp_builder/oracle/edit/launch_exec.py
    """
    # 本命 builder は editor input log に完全 prompt の skeleton を保存する。
    repo = _resolve_real_path(_RootPathPlaceHolder.REPO)
    _editor_input_log_dir(repo).mkdir(parents=True, exist_ok=True)
    return _build_main_parameter(time_stamp, user_instruction)


def build_oracle_edit_reduction_launch_exec_parameter(
    user_instruction: str,
) -> _AgentCallParameter:
    """正本 builder から仕様削減用の固定パラメータを返す。

    根拠: {{work-root}}/oracle/src/oracle/acp_builder/oracle/edit/launch_exec.py
    """
    # 仕様削減 prompt は parameter 本文として構築され、補助 file を作らない。
    return _build_reduction_parameter(user_instruction)


__all__ = [
    "build_oracle_edit_main_launch_exec_parameter",
    "build_oracle_edit_reduction_launch_exec_parameter",
]
