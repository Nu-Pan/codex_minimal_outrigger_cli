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
    """利用できる検索手段と、原文確認・閲覧範囲の指示を構築する。

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

    # 検索方式の選択を固定せず、どの手段でも同じ原文・閲覧境界を伝える。
    root_definitions = path_context.root_placeholder_definitions()
    return (
        {"work-root": root_definitions["work-root"]},
        SDHeader(
            "routing policy",
            SDPolicy(
                what_is_this="必要な原文へ到達し、判断するための規定を以下に示す",
                require=(
                    "利用可能なベクトル検索、既存のキーワード検索、原文への直接参照から、目的に合う手段を選ぶこと。単独でも組み合わせてもよく、利用順序は固定しない",
                    "検索結果の path・該当箇所・抜粋は参照先を選ぶために使い、必要な現在原文を開いて判断すること。食い違う場合も原文を優先すること",
                    "`{{work-root}}/oracle/src` と `{{work-root}}/oracle/test` は直接参照または既存の文字列検索で確認すること",
                    "検索でも直接参照でも、この call の閲覧制限を守ること。検索結果を使って閲覧権限を広げないこと",
                    "検索失敗と正常ゼロ件を区別し、ゼロ件だけで仕様の不存在や調査完了を判断しないこと",
                ),
            ),
            *search_instructions,
        ),
    )
