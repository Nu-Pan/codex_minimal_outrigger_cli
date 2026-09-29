"""Codex 呼び出し失敗を共通のエラーテキストへ変換する。"""

from .runtime_errors import CmocError


def format_codex_call_error(error: BaseException) -> str:
    """Codex 起動失敗を console と event に共通の error text へ変換する。

    根拠: {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
    """
    # CmocError は利用者向けの概要と診断用の詳細を結合して記録する。
    if isinstance(error, CmocError):
        return f"{error.summary}: {error.detail}"
    # その他の例外は空の文字列表現でも例外型を失わないようにする。
    return str(error) or repr(error)
