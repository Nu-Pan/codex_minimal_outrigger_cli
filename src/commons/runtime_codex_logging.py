from .runtime_errors import CmocError


def format_codex_call_error(error: BaseException) -> str:
    """Codex 起動失敗を console と event に共通の error text へ変換する。

    根拠: {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
    """
    if isinstance(error, CmocError):
        return f"{error.summary}: {error.detail}"
    return str(error) or repr(error)
