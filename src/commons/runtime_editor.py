"""人間向けファイル表示と editor input が共用するエディタ選択。"""

import shutil

from .runtime_errors import CmocError


def select_editor() -> tuple[str, str]:
    """仕様の優先順で利用可能な editor command と実行ファイルを返す。"""
    # {{work-root}}/oracle/doc/app_spec/prompt_editor_input.md
    for command in ("code", "nano", "vim", "vi"):
        executable = shutil.which(command)
        if executable is not None:
            return command, executable
    raise CmocError(
        "利用可能なエディタが見つかりません。",
        ["code, nano, vim, vi のいずれかを PATH から起動できるようにしてください。"],
        "searched: code, nano, vim, vi",
    )
