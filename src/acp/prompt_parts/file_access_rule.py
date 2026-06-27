"""file access rule prompt part の realization。

対応 oracle file: `<work-root>/oracle/src/acp/prompt_parts/file_access_rule.py`。
"""

# cmoc
from basic.path_model import resolve_work_root
from basic.struct_doc import StructDoc, ntqs
from basic.acp import FileAccessMode


def build_file_access_rule(mode: FileAccessMode) -> StructDoc:
    """
    AI エージェントによるファイル読み書き規則のプロンプトを構築する

    mode:
        読み書きモードプリセット
    """
    # エイリアス
    work_root = resolve_work_root()

    # 本文を構築
    match mode:
        case FileAccessMode.READONLY:
            body = ntqs(f"""
            - `{work_root}` ツリー外は読み書き禁止
            - `{work_root}` ツリー内は書き込み禁止
            - `{work_root}/memo` は読み書き禁止
            """)
        case FileAccessMode.PURE_ORACLE_READ:
            body = ntqs(f"""
            - `{work_root}` ツリー外は読み書き禁止
            - `{work_root}/oracle` ツリー内は書き込み禁止
            - `{work_root}/oracle` ツリー外は読み書き禁止
            """)
        case FileAccessMode.REALIZATION_WRITE:
            body = ntqs(f"""
            - `{work_root}` ツリー外は読み書き禁止
            - `{work_root}/oracle` ツリー内は書き込み禁止
            - `{work_root}/memo` は読み書き禁止
            """)
        case FileAccessMode.ORACLE_WRITE:
            body = ntqs(f"""
            - `{work_root}` ツリー外は読み書き禁止
            - `{work_root}/oracle` ツリー外は書き込み禁止
            - `{work_root}/memo` は読み書き禁止
            """)
        case FileAccessMode.REPO_WRITE:
            body = ntqs(f"""
            - `{work_root}` ツリー外は読み書き共に禁止
            - `{work_root}/memo` は読み書き禁止
            """)
        case _:
            raise ValueError(f"Invalid mode (mode={mode})")
    # 正常終了
    return StructDoc(
        f"file read write rule - {mode.value}",
        body,
    )
