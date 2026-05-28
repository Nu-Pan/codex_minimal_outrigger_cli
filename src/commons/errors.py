"""cmoc 全体で使うエラー処理。"""

import traceback
from collections.abc import Sequence


class CmocError(RuntimeError):
    """ユーザーに次の操作を提示すべき cmoc の実行時エラー。"""

    def __init__(
        self,
        message: str,
        actions: Sequence[str],
        detail: str | None = None,
        exit_code: int = 1,
    ) -> None:
        """エラーレポートに必要な情報を保持する。"""
        # 共通エラーレポートは、場合分けした複数の次アクションを必須にする。
        if len(actions) < 2:
            raise ValueError("CmocError requires at least two actions.")

        # RuntimeError としての message と、cmoc report 用の詳細情報を両方保持する。
        super().__init__(message)
        self.message = message
        self.actions = list(actions)
        self.detail = detail or message
        self.exit_code = exit_code


def format_error_report(error: BaseException) -> str:
    """仕様で要求される stdout 向けエラーレポートを作る。"""
    # CmocError は利用者向け action/detail をそのまま使う。
    if isinstance(error, CmocError):
        actions = error.actions
        detail = error.detail
        message = error.message
    else:
        actions = [
            "入力値が誤っている場合は、コマンド引数を修正してから cmoc を再実行してください。",
            "リポジトリ状態が原因の場合は、Detail と Call stack を確認して作業ツリーや設定を修正してください。",
        ]
        detail = str(error)
        if not detail.strip():
            detail = (
                f"{error.__class__.__module__}."
                f"{error.__class__.__name__} がメッセージなしで発生しました。"
            )
        message = error.__class__.__name__

    # エラー内容と復旧操作を機械的に並べる。
    lines = [
        "ERROR",
        "",
        "Summary:",
        message,
        "",
        "Next actions:",
    ]
    for action in actions:
        lines.append(f"- {action}")
    lines.extend(
        [
            "",
            "Detail:",
            detail,
            "",
            "Call stack:",
            _format_call_stack(error),
        ]
    )
    return "\n".join(lines)


def _format_call_stack(error: BaseException) -> str:
    """受け取った例外そのもののコールスタックを整形する。"""
    if error.__traceback__ is None:
        return (
            "Traceback is not available for this exception. "
            "The exception may not have been raised yet."
        )
    return "".join(traceback.format_exception(type(error), error, error.__traceback__))
