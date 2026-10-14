"""実行 ID で指定した TUI workload の公開再開入口。"""

from commons.runtime_cli import run_cli_subcommand
from commons.runtime_codex_tui import resume_codex_tui
from commons.runtime_paths import repo_root


def cmoc_resume_impl(execution_id: str) -> None:
    """新しい最外側 invocation で、終了済み会話の再開を準備する。"""
    # 公開 resume の実行・通知は、元の workload の invocation から分離する。

    def body() -> None:
        # 元の workload と保存環境の照合は、起動管理側に集約する。
        resume_codex_tui(execution_id, repo_root())

    run_cli_subcommand(
        body,
        command_name="resume",
        command_argv=["cmoc", "resume", execution_id],
        tui_process=True,
    )
