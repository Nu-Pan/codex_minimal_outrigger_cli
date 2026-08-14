# {{work-root}}/oracle/doc/app_spec/error_handling.md

from .runtime_results import TerminalResult

DEFAULT_NEXT_ACTION = (
    "入力、実行場所、設定、作業ツリー状態を確認してから再実行してください。"
)


class CmocError(RuntimeError):
    """利用者向けエラーレポートに必要な情報を持つ cmoc の実行時例外。"""

    def __init__(
        self: "CmocError",
        summary: str,
        next_actions: list[str],
        detail: str,
        *,
        terminal_result: TerminalResult | None = None,
    ) -> None:
        """エラー概要、復旧案、詳細を例外 object に保持する。

        Args:
            summary: エラーレポートの Summary に出す短い説明。
            next_actions: 利用者に提示する復旧または調査手順。
            detail: エラー原因の具体情報。
        """
        super().__init__(summary)
        self.summary = summary
        self.next_actions = next_actions
        self.detail = detail
        self.terminal_result = terminal_result


def render_error(exc: BaseException) -> str:
    """ログを初期化できない境界向けの簡潔な handled failure を描画する。"""
    if isinstance(exc, CmocError):
        summary = exc.summary
        actions = list(exc.next_actions) or [DEFAULT_NEXT_ACTION]
        detail = exc.detail
    else:
        summary = str(exc) or exc.__class__.__name__
        actions = [DEFAULT_NEXT_ACTION]
        detail = repr(exc)
    return "\n".join(
        [
            "# 失敗: cmoc",
            f"- 理由: {summary}",
            *[f"- 次の操作: {action}" for action in actions],
            f"- 詳細: {detail}",
        ]
    )
