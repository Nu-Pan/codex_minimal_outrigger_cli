# cmoc
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


_FORBIDDEN_PROMPT_REPLACEMENTS = {
    "<cmoc-root>": "実装ルートの実パス",
    "<repo-root>": "対象リポジトリの実パス",
    "<run-root>": "実行用 worktree の実パス",
    "<work-root>": "作業対象ルートの実パス",
    "cmoc から呼び出された": "依頼を受けた",
}


def _sanitize_agent_prompt_text(text: str) -> str:
    for forbidden, replacement in _FORBIDDEN_PROMPT_REPLACEMENTS.items():
        text = text.replace(forbidden, replacement)
    return text


def _sanitize_agent_prompt_doc(doc: StructDoc) -> StructDoc:
    children = doc.children
    if isinstance(children, str):
        return StructDoc(
            _sanitize_agent_prompt_text(doc.title),
            _sanitize_agent_prompt_text(children),
        )
    if isinstance(children, StructCodeBlock):
        return StructDoc(
            _sanitize_agent_prompt_text(doc.title),
            StructCodeBlock(
                children.info,
                _sanitize_agent_prompt_text(children.body),
            ),
        )
    return StructDoc(
        _sanitize_agent_prompt_text(doc.title),
        *[_sanitize_agent_prompt_doc(child) for child in children],
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
    return [_sanitize_agent_prompt_doc(doc) for doc in struct_doc]
