# cmoc
from basic.struct_doc import StructDoc

# local
from .file_access_rule import build_file_access_rule, FileAccessMode
from .oracle_standard import build_oracle_standard
from .realization_standard import build_realization_standard
from .oracle_and_realization_basic import build_oracle_and_realization_basic
from .apply_review_aspect import build_apply_review_aspect


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
    apply_review_aspect: bool = False,
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

    apply_review_aspect:
        True の時、apply review aspect をプロンプトに注入する

    return:
        agent call にそのまま渡すことができる完全なプロンプト
    """
    struct_doc = [
        StructDoc(
            "role",
            role,
        ),
        StructDoc(
            "summary",
            summary,
        ),
        StructDoc(
            "goal",
            goal,
        ),
        build_file_access_rule(file_access_mode),
        *aux_prompt,
    ]
    if (
        oracle_and_realization_basic
        or oracle_standard
        or realization_standard
        or apply_review_aspect
    ):
        struct_doc.append(build_oracle_and_realization_basic())
    if oracle_standard:
        struct_doc.append(build_oracle_standard())
    if realization_standard:
        struct_doc.append(build_realization_standard())
    if apply_review_aspect:
        struct_doc.append(build_apply_review_aspect())
    return struct_doc
