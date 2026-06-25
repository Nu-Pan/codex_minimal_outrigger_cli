# std
from collections.abc import Callable
from pathlib import Path

# cmoc
from basic.path_model import (
    RootToken,
    resolve_cmoc_root,
    resolve_real_path,
    resolve_repo_root,
    resolve_work_root,
)
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


def _resolve_prompt_root_token(root_token: RootToken) -> Path:
    match root_token:
        case RootToken.CMOC:
            return resolve_cmoc_root()
        case RootToken.REPO:
            return resolve_repo_root()
        case RootToken.RUN:
            return resolve_real_path(root_token)
        case RootToken.WORK:
            return resolve_work_root()


def _safe_resolve_prompt_root_token(root_token: RootToken) -> Path:
    try:
        return _resolve_prompt_root_token(root_token)
    except ValueError:
        return resolve_work_root()


def _agent_text_replacements() -> list[tuple[str, str]]:
    work_root = resolve_work_root()
    replacements = [
        ("`cmoc review oracle`", "仕様レビュー作業"),
        ("`cmoc apply join`", "`apply join`"),
        ("cmoc-managed branch", "管理対象ブランチ"),
        ("Codex Minimal Outrigger CLI", "このリポジトリ"),
        ("cmoc から", "呼び出し元から"),
        ("cmoc が", "呼び出し元が"),
        ("cmoc は", "このリポジトリでは"),
        ("cmoc により", "このリポジトリで"),
        ("cmoc の", "このリポジトリの"),
        ("cmoc でも", "このリポジトリでも"),
        ("cmoc 側", "呼び出し元側"),
        ("session home branch", "作業開始元ブランチ"),
        ("session branch", "作業用ブランチ"),
        ("run branch", "隔離作業ブランチ"),
        ("run worktree", "隔離作業ディレクトリ"),
        ("linked worktree", "連結された作業ディレクトリ"),
        ("oracle and realization basic", "仕様ファイルと編集対象の扱い"),
        ("apply review standard", "仕様と実装の照合基準"),
        ("review oracle standard", "仕様文書レビュー基準"),
        ("index entry standard", "INDEX.md エントリー基準"),
        ("oracle standard", "仕様文書の記述基準"),
        ("realization standard", "編集対象ファイルの保守基準"),
        ("oracle doc", f"`{work_root}/oracle/doc` 配下の仕様Markdown"),
        ("oracle src", f"`{work_root}/oracle/src` 配下の仕様コード"),
        ("oracle test", f"`{work_root}/oracle/test` 配下の仕様テスト"),
        ("realization implementation", f"`{work_root}/src` 配下の実装"),
        ("realization code", "編集対象コード"),
        ("realization test", f"`{work_root}/test` 配下のテスト"),
        ("realization ancillary", "補助ファイル"),
        ("oracle spec", "仕様説明"),
        ("oracles file", "仕様ファイル"),
        ("oracle file", "仕様ファイル"),
        ("realization file", "編集対象ファイル"),
        ("正本仕様断片", "人間が管理する仕様"),
        ("正本仕様", "人間が管理する仕様"),
        ("実装者である AI agent", "作業担当者"),
        ("実装者である AI", "作業担当者"),
        ("AI agent", "作業担当者"),
        ("AI Agent", "作業担当者"),
    ]
    for root_token in RootToken:
        replacements.append(
            (root_token.value, str(_safe_resolve_prompt_root_token(root_token)))
        )
    return replacements


def _agent_title_replacements() -> list[tuple[str, str]]:
    return [
        ("oracle and realization basic", "仕様ファイルと編集対象の扱い"),
        ("apply review standard", "仕様と実装の照合基準"),
        ("review oracle standard", "仕様文書レビュー基準"),
        ("index entry standard", "INDEX.md エントリー基準"),
        ("oracle standard", "仕様文書の記述基準"),
        ("realization standard", "編集対象ファイルの保守基準"),
        ("realization implementation", "実装"),
        ("realization ancillary", "補助ファイル"),
        ("realization code", "編集対象コード"),
        ("realization test", "テスト"),
        ("oracle file", "仕様ファイル"),
        ("realization file", "編集対象ファイル"),
        ("oracle", "人間管理仕様"),
    ]


def _replace_text(text: str, replacements: list[tuple[str, str]]) -> str:
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def _rewrite_agent_doc(
    struct_doc: StructDoc,
    title_replacements: list[tuple[str, str]],
    text_replacements: list[tuple[str, str]],
) -> StructDoc:
    title = _replace_text(struct_doc.title, title_replacements)
    children = struct_doc.children
    if isinstance(children, list):
        return StructDoc(
            title,
            *[
                _rewrite_agent_doc(child, title_replacements, text_replacements)
                for child in children
            ],
        )
    if isinstance(children, str):
        return StructDoc(title, _replace_text(children, text_replacements))
    if isinstance(children, StructCodeBlock):
        return StructDoc(title, children)
    raise TypeError(f"Invalid type of struct_doc.children (type={type(children)})")


def _for_codex_cli(struct_doc: StructDoc) -> StructDoc:
    return _rewrite_agent_doc(
        struct_doc,
        _agent_title_replacements(),
        _agent_text_replacements(),
    )


def _append_for_codex_cli(
    struct_doc: list[StructDoc],
    builder: Callable[[], StructDoc],
) -> None:
    struct_doc.append(_for_codex_cli(builder()))


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
        _for_codex_cli(StructDoc("role", role)),
        _for_codex_cli(StructDoc("summary", summary)),
        _for_codex_cli(StructDoc("goal", goal)),
        build_file_access_rule(file_access_mode),
        build_routing_rule(),
        *[_for_codex_cli(prompt) for prompt in aux_prompt],
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
        _append_for_codex_cli(struct_doc, build_oracle_and_realization_basic)
    if oracle_standard:
        _append_for_codex_cli(struct_doc, build_oracle_standard)
    if realization_standard:
        _append_for_codex_cli(struct_doc, build_realization_standard)
    if apply_review_standard:
        _append_for_codex_cli(struct_doc, build_apply_review_standard)
    if review_oracle_standard:
        _append_for_codex_cli(struct_doc, build_review_oracle_standard)
    if index_entry_standard:
        _append_for_codex_cli(struct_doc, build_index_entry_standard)
    return struct_doc
