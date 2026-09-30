"""検索と現在原文の確認による routing 規定文面の構築定義。"""

import json
from dataclasses import asdict

from oracle.acp_builder.basic import DocumentSearchScope
from oracle.other.document_search import SEARCH_MCP_SERVER, SEARCH_TOOL_NAME
from oracle.other.path_model import AgentCallPathContext
from oracle.other.struct_doc import SDCodeBlock, SDHeader, SDPolicy
from oracle.prompt_builder.basic import PlaceholderMap


def build_routing_policy(
    path_context: AgentCallPathContext,
    document_search_scope: DocumentSearchScope | None = None,
) -> tuple[PlaceholderMap, SDHeader]:
    """検索の併用条件と、原文確認・閲覧範囲の指示を構築する。

    NOTE
        意味仕様は `{{cmoc-root}}/oracle/doc/app_spec/document_search.md` の
        「検索と routing」「対象と信頼境界」を参照。
    """
    # 接続の有無と同じ scope を使い、利用できない tool を案内しない。
    search_instructions: list[SDHeader] = []
    if document_search_scope is not None:
        search_instructions.append(
            SDHeader(
                "ベクトル検索の利用",
                f"- MCP tool `{SEARCH_MCP_SERVER}.{SEARCH_TOOL_NAME}` に `query` と、"
                "必要なら最大結果件数 `limit` を渡して原文候補を探せる。\n"
                "- 対象は `{{work-root}}/oracle/doc` 内の閲覧可能な Markdown。"
                "root や閲覧範囲を tool 引数で変更することはできない。\n"
                "- 以下は work-root 相対 path による範囲。allowed_files は個別 file、"
                "allowed_subtrees は配下、excluded_files/excluded_subtrees は優先する除外。"
                "許可の両配列が空なら対象なし。分類とこの call の閲覧制限も適用される。",
                SDCodeBlock(
                    "json",
                    json.dumps(asdict(document_search_scope), ensure_ascii=False),
                ),
            )
        )
    else:
        search_instructions.append(
            SDHeader(
                "利用できる参照手段",
                "この call では文書検索 MCP は無効。許可された原文への直接参照や既存のキーワード検索を使える。",
            )
        )

    root_definitions = path_context.root_placeholder_definitions()
    return (
        {"work-root": root_definitions["work-root"]},
        SDHeader(
            "routing policy",
            SDPolicy(
                what_is_this="必要な原文へ到達し、判断するための規定を以下に示す",
                require=(
                    "oracle doc 上の仕様文章を検索するときは、標準的なキーワード検索に加えて、MCP tool によるベクトル検索も併用すること",
                    "このセッションに課せられているファイルアクセス制限は、検索結果についても適用される",
                    "「検索失敗」と「検索成功の上でヒットゼロ件」は区別すること",
                ),
                prohibit=(
                    "検索ヒットゼロ件だけを根拠に「仕様の不存在」「調査完了」と判断してはいけない",
                ),
                exception=(
                    "何らかの理由で検索に失敗した場合は、許可された手段で調査を続けて良い",
                ),
            ),
            *search_instructions,
        ),
    )
