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


_CMOC_TERM_REPLACEMENTS = (
    ("cmoc から呼び出された", "依頼された"),
    ("`cmoc eval-oracle`", "oracle file レビュー"),
    ("`cmoc apply join`", "apply join 操作"),
    ("cmoc eval-oracle", "oracle file レビュー"),
    ("cmoc apply join", "apply join 操作"),
    ("cmoc 側", "呼び出し側"),
    ("cmoc により", "継続的に"),
    ("cmoc でも", "この作業対象でも"),
    ("cmoc は", "この作業対象では"),
    ("cmoc が", "呼び出し側が"),
    ("cmoc の", "この作業対象の"),
    ("cmoc を", "このツールを"),
    ("cmoc", "このツール"),
)


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
    """agent に渡す標準文書から cmoc 固有語と root token を除去する。"""
    children = doc.children
    title = _sanitize_prompt_text(doc.title)
    if isinstance(children, list):
        return StructDoc(title, *[_sanitize_prompt_doc(child) for child in children])
    if isinstance(children, StructCodeBlock):
        return StructDoc(
            title,
            StructCodeBlock(children.info, _sanitize_prompt_text(children.body)),
        )
    return StructDoc(title, _sanitize_prompt_text(children))


def _sanitize_prompt_text(text: str) -> str:
    """prompt text 内の作業対象に不要な内部呼称を呼び出し先向けに置換する。"""
    for token in RootToken:
        text = text.replace(token.value, str(_prompt_root_path(token)))
    for before, after in _CMOC_TERM_REPLACEMENTS:
        text = text.replace(before, after)
    return text


def _prompt_root_path(token: RootToken) -> Path:
    """run root が未確定な通常呼び出しでは work root を代替 root として使う。"""
    try:
        return resolve_real_path(token)
    except ValueError:
        # Codex CLI に渡す prompt では root token を残さない。run worktree が無い
        # 通常 worktree 上の呼び出しでは、現在の作業ルートを具体パスとして使う。
        return resolve_work_root()
