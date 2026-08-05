"""oracle file を扱う agent call に注入する規範の正本。"""

# cmoc
from oracle.other.path_model import AgentCallPathContext
from oracle.other.standard import Requirement, Standard, standard_to_struct_doc
from oracle.other.struct_doc import StructDoc
from oracle.prompt_builder.basic import PlaceholderMap


def build_oracle_standard(
    path_context: AgentCallPathContext,
) -> tuple[PlaceholderMap, StructDoc]:
    """oracle file の作成・変更・調査・レビューに必要な規範を構築する。"""
    # 規範本文が参照する work-root を call-scoped context から取得する。
    root_definitions = path_context.root_placeholder_definitions()
    standards = [
        Standard(
            title="oracle file を正本仕様断片として扱う",
            backgrounds=[
                "oracle file は人間が所有し、realization file が具体化する正本仕様断片である",
                "installed skill は実行環境ごとに存在しない場合がある",
            ],
            requirements=[
                Requirement("必須", "判断の根拠を関連する oracle file に置く"),
                Requirement(
                    "必須",
                    "cmoc 固有契約または oracle file と installed skill が競合する場合は前者を優先する",
                ),
                Requirement(
                    "禁止",
                    "installed skill の存在を oracle file の意味または作業完了条件の前提にしてはいけない",
                ),
                Requirement(
                    "禁止",
                    "一般的なベストプラクティスだけを根拠に oracle file の要求を変更してはいけない",
                ),
            ],
        ),
        Standard(
            title="重要な人間意図へ絞り、仕様の隙間を許容する",
            backgrounds=[
                "oracle file の規模は人間が維持し、AI が読む文脈量に影響する",
                "正本仕様断片の間に未定義部分が残ることは意図された状態である",
            ],
            requirements=[
                Requirement(
                    "必須",
                    "実装差を許容しない事項と、人間が判断すべき境界を明示する",
                ),
                Requirement(
                    "禁止",
                    "仕様全体を網羅するためだけの分類、列挙、説明を追加してはいけない",
                ),
                Requirement(
                    "許容",
                    "明示仕様の隙間は、現行の oracle file と、file access が許す場合の"
                    "既存実装・既存 test から自然に導ける小さな範囲で実装者が補ってよい",
                ),
                Requirement(
                    "禁止",
                    "未定義部分を埋めることだけを目的に oracle file を増やしてはいけない",
                ),
                Requirement(
                    "必須",
                    "過剰な実装を誘発し得る境界では goal と non-goal を読み取れるようにする",
                ),
            ],
        ),
        Standard(
            title="実装から正本仕様を逆算しない",
            backgrounds=[
                "realization file には実装者の裁量、過去の都合、偶然の挙動が含まれ得る",
                "実装上の制約は正本仕様の実現可能性を調べる材料にはなる",
            ],
            requirements=[
                Requirement(
                    "禁止",
                    "oracle file を調査せず、実装だけから正本仕様を導いてはいけない",
                ),
                Requirement(
                    "禁止",
                    "既存実装の都合または挙動だけを根拠に oracle file を変更してはいけない",
                ),
                Requirement(
                    "許容",
                    "正本仕様の矛盾または実現不能を調べる場合に限り、実装上の制約を修正提案の材料にしてよい",
                ),
            ],
        ),
        Standard(
            title="正本仕様断片の整合性と検索性を保つ",
            backgrounds=[
                "相互に矛盾する正本仕様断片から一貫した realization file は導けない",
                "用語と命名の揺れは検索と読解を不安定にする",
            ],
            requirements=[
                Requirement(
                    "禁止",
                    "一方の正本仕様断片に従うと別の正本仕様断片へ必ず違反する状態を作ってはいけない",
                ),
                Requirement(
                    "必須",
                    "一般方針と個別仕様の優先関係を読み取れるようにする",
                ),
                Requirement(
                    "必須",
                    "依頼の対象外である既存仕様の意味を維持する",
                ),
                Requirement(
                    "必須",
                    "oracle file を作成または変更する場合は、同じ概念の用語と表記を統一し、名前から推測される意味を定義と一致させる",
                ),
                Requirement(
                    "必須",
                    "oracle file を作成または変更する場合は、文意または検索性を損なう誤字、脱字、文法誤りを残さない",
                ),
                Requirement(
                    "禁止",
                    "oracle file を作成または変更する場合は、同じ意味の記述を複数箇所へ重複させてはいけない",
                ),
            ],
        ),
    ]
    return (
        {"work-root": root_definitions["work-root"]},
        StructDoc(
            "oracle standard",
            StructDoc(
                "適用条件",
                "- oracle file を作成、変更、調査、またはレビューする場合に適用する",
            ),
            *[standard_to_struct_doc(standard) for standard in standards],
        ),
    )
