# std
from typing import Literal

# cmoc
from utils.path_model import (
    resolve_cmoc_root,
    resolve_repo_root,
    resolve_run_root,
    resolve_work_root,
)
from oracle.src.utils.struct_doc import StructDoc, ntqs

type FileAccessMode = Literal[
    "readonly",
    "pure_oracle_read",
    "realization_write",
    "oracle_write",
]


def build_file_access_rule(
    mode: FileAccessMode,
    aux_rules: str | None = None,
) -> StructDoc:
    """
    AI エージェントによるファイル読み書き規則のプロンプトを構築する

    mode:
        読み書きモードプリセット

    aux_rules:
        任意の追加読み書き規則
        箇条書きスタイルを想定
    """
    # エイリアス
    work_root = resolve_work_root()

    # 本文を構築
    match mode:
        case "readonly":
            body = ntqs(f"""
            - `{work_root}` ツリー外は読み書き共に禁止
            - リポジトリに対する書き込み操作は一切禁止
            - `{work_root}/memo` は読み込みも禁止
            """)
        case "pure_oracle_read":
            body = ntqs(f"""
            - `{work_root}` ツリー外は読み書き共に禁止
            - `{work_root}/oracle` ツリー内は書き込み禁止
            - `{work_root}/oracle` ツリー外は読み書き共に禁止
            """)
        case "realization_write":
            body = ntqs(f"""
            - `{work_root}` ツリー外は読み書き共に禁止
            - `{work_root}/oracle` ツリー内は書き込み禁止
            - `{work_root}/memo` は読み書き共に禁止
            """)
        case "oracle_write":
            body = ntqs(f"""
            - `{work_root}` ツリー外は読み書き共に禁止
            - `{work_root}/oracle` ツリー外は書き込み禁止
            - `{work_root}/memo` は読み込みも禁止
            """)
        case _:
            raise ValueError(f"Invalid mode (mode={mode})")
    # StructDocs を構築
    struct_doc = []
    if aux_rules:
        body += "\n"
        body += ntqs(aux_rules)
    # 正常終了
    return StructDoc(
        "ファイル読み書き規則",
        body,
    )
