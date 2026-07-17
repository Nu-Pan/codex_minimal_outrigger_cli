# {{work-root}}/oracle/doc/app_spec/error_handling.md
import traceback

DEFAULT_NEXT_ACTIONS = [
    "入力、実行場所、設定、作業ツリー状態に問題がある場合は、該当箇所を修正してから再実行してください。",
    "原因が実装不具合または仕様不足に見える場合は、Detail と Call stack を添えて調査してください。",
]


class CmocError(RuntimeError):
    """利用者向けエラーレポートに必要な情報を持つ cmoc の実行時例外。"""

    def __init__(
        self: "CmocError", summary: str, next_actions: list[str], detail: str
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


def _multiple_next_actions(actions: list[str]) -> list[str]:
    """Next actions が最低 2 件になるよう既定案内を補う。"""
    merged = list(actions) or list(DEFAULT_NEXT_ACTIONS)
    for action in DEFAULT_NEXT_ACTIONS:
        if len(merged) >= 2:
            break
        if action not in merged:
            merged.append(action)
    return merged


def render_error(exc: BaseException) -> str:
    """例外を cmoc 共通の Markdown エラーレポートへ変換する。"""
    if isinstance(exc, CmocError):
        summary = exc.summary
        actions = _multiple_next_actions(exc.next_actions)
        detail = exc.detail
    else:
        summary = str(exc) or exc.__class__.__name__
        actions = _multiple_next_actions(DEFAULT_NEXT_ACTIONS)
        detail = repr(exc)
    return "\n".join(
        [
            "# ERROR",
            "## Summary",
            summary,
            "## Next actions",
            *[f"- {action}" for action in actions],
            "## Detail",
            detail,
            "## Call stack",
            traceback.format_exc(),
        ]
    )
