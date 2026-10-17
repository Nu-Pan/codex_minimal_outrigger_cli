"""`cmoc run join` の公開 CLI と共通 join lifecycle の接続。"""

from cmoc_runtime import TerminalResult, run_cli_subcommand
from commons.runtime_run_join import join_editing_run


def cmoc_run_join_impl(force_resolve: bool = False) -> None:
    """停止した active editing run の取り込みを実行する。"""
    # 自動 join と同じ処理を、独立した最外側 invocation として起動する。
    run_cli_subcommand(
        _cmoc_run_join_body,
        force_resolve,
        command_name="run join",
        command_argv=[
            "cmoc",
            "run",
            "join",
            *(["--force-resolve"] if force_resolve else []),
        ],
        doctor_preprocess=False,
        total_steps=6,
    )


def _cmoc_run_join_body(force_resolve: bool) -> TerminalResult:
    """検査、merge、post-join、report と資源回収を共通 lifecycle へ渡す。"""
    # 共通処理は最外側 invocation の report だけを作る。
    return join_editing_run(force_resolve=force_resolve)
