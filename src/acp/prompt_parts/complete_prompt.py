"""agent call 用 prompt part を統合する realization。

対応 oracle file: `<work-root>/oracle/src/acp/prompt_parts/complete_prompt.py`。
"""

# cmoc
from pathlib import Path

from basic.path_model import RootToken, resolve_real_path, resolve_work_root
from basic.struct_doc import StructCodeBlock, StructDoc

# local
from .file_access_rule import build_file_access_rule, FileAccessMode
from .oracle_standard import build_oracle_standard
from .realization_standard import build_realization_standard
from .oracle_and_realization_basic import build_oracle_and_realization_basic
from .apply_review_standard import build_apply_review_standard
from .oracle_review_standard import build_review_oracle_standard
from .index_entry_standard import build_index_entry_standard
from .routing_rule import build_routing_rule


def build_complete_prompt(
    *,
    role: str,
    summary: str,
    goal: str,
    file_access_mode: FileAccessMode,
    aux_prompt: list[StructDoc],
    oracle_and_realization_basic: bool = False,
    oracle_standard: bool = False,
    realization_standard: bool = False,
    review_oracle_standard: bool = False,
    apply_review_standard: bool = False,
    index_entry_standard: bool = False,
) -> list[StructDoc]:
    """
    agent call にそのまま渡すことができる完全なプロンプトを構築する

    role:
        agent が果たすべき役割の短い説明

    summaey:
        agent への依頼する作業の概要・短い説明

    goal:
        agent が作業完了と判断する条件・基準

    file_access_mode:
        agent によるファイルアクセスに対する制限設定

    aux_prompt:
        任意に追加可能なプロンプト
        典型的には、汎用性の一切ない特殊事情についての説明をプロンプトとして注入する場合に使う事を想定している

    oracle_and_realization_basic:
        True の時、oracle, realization についての基本情報をプロンプトに注入する

    oracle_standard:
        True の時、oracle standard をプロンプトに注入する

    realization_standard:
        True の時、realization standard をプロンプトに注入する

    review_oracle_standard:
        True の時、review oracle standard をプロンプトに注入する

    apply_review_standard:
        True の時、apply review standard をプロンプトに注入する

    index_entry_standard:
        True の時、index entry standard をプロンプトに注入する

    return:
        agent call にそのまま渡すことができる完全なプロンプト
    """
    # 基本プロンプト
    struct_doc = [
        StructDoc("role", role),
        StructDoc("summary", summary),
        StructDoc("goal", goal),
        build_file_access_rule(file_access_mode),
        build_routing_rule(),
        *aux_prompt,
    ]
    # 依存関係の有る情報を必ず含めるようにする
    if oracle_and_realization_basic:
        pass
    if oracle_standard:
        oracle_and_realization_basic = True
    if realization_standard:
        oracle_and_realization_basic = True
    if review_oracle_standard:
        oracle_and_realization_basic = True
        oracle_standard = True
    if apply_review_standard:
        oracle_and_realization_basic = True
        realization_standard = True
    if index_entry_standard:
        oracle_and_realization_basic = True
        oracle_standard = True
        realization_standard = True
    # パターンプロンプトの注入
    if oracle_and_realization_basic:
        struct_doc.append(build_oracle_and_realization_basic())
    if oracle_standard:
        struct_doc.append(build_oracle_standard())
    if realization_standard:
        struct_doc.append(build_realization_standard())
    if apply_review_standard:
        struct_doc.append(build_apply_review_standard())
    if review_oracle_standard:
        struct_doc.append(build_review_oracle_standard())
    if index_entry_standard:
        struct_doc.append(build_index_entry_standard())
    return [_sanitize_prompt_doc(doc) for doc in struct_doc]


def _sanitize_prompt_doc(doc: StructDoc) -> StructDoc:
    """Codex CLI に渡す直前の root token 置換を文書木全体へ適用する。"""
    children = doc.children
    title = _sanitize_prompt_text(doc.title)
    if isinstance(children, str):
        return StructDoc(title, _sanitize_prompt_text(children))
    if isinstance(children, StructCodeBlock):
        return StructDoc(
            title,
            StructCodeBlock(children.info, _sanitize_prompt_text(children.body)),
        )
    return StructDoc(title, *[_sanitize_prompt_doc(child) for child in children])


def _sanitize_prompt_text(text: str) -> str:
    """標準 prompt 内の cmoc 固有表記を実行時の Codex 向け表記へ寄せる。"""
    # `<work-root>/oracle/doc/app_spec/prompt_standard.md` requires concrete paths
    # before text is passed to Codex CLI.
    for root_token in RootToken:
        text = text.replace(root_token.value, str(_resolve_prompt_root(root_token)))
    return text.replace("cmoc から呼び出された AI Agent", "AI Agent")


def _resolve_prompt_root(root_token: RootToken) -> Path:
    """prompt 用 root token を Codex から見える実 path へ解決する。"""
    try:
        return resolve_real_path(root_token)
    except ValueError:
        if root_token is RootToken.RUN:
            return resolve_work_root()
        raise
