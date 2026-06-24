import traceback


class CmocError(RuntimeError):
    def __init__(self, summary: str, next_actions: list[str], detail: str):
        super().__init__(summary)
        self.summary = summary
        self.next_actions = next_actions
        self.detail = detail


def render_error(exc: BaseException) -> str:
    if isinstance(exc, CmocError):
        summary = exc.summary
        actions = exc.next_actions
        detail = exc.detail
    else:
        summary = str(exc) or exc.__class__.__name__
        actions = [
            "エラー内容を確認し、必要なら手動で状態を修復してから再実行してください。"
        ]
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
