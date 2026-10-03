"""検索と現在原文の確認による routing 規定文面の構築定義。"""

from oracle.other.document_search import (
    SEARCH_MCP_SERVER,
    SEARCH_TOOL_NAME,
)
from oracle.other.struct_doc import SDHeader, SDPolicy
from oracle.prompt_builder.basic import PlaceholderMap


def build_routing_policy(
    search_mcp_tool_available: bool,
) -> tuple[PlaceholderMap, SDHeader]:
    """文章ルーティングについての規定を構築する。

    Args:
        search_mcp_tool_available: そのセッションでベクトル検索 MCP tool が利用可能であるなら True

    Returns:
        文章ルーティングについての構造化された規定

    NOTE
        意味仕様は `{{cmoc-root}}/oracle/doc/app_spec/document_search.md` の
        「検索と routing」「対象と信頼境界」を参照。
    """
    # 利用可否に応じた検索方針だけを示し、使い方は tool 自体の説明に委ねる。
    return (
        {},
        SDHeader(
            "routing policy",
            SDPolicy(
                what_is_this="必要な原文へ到達し、判断するための規定を以下に示す",
                require=(
                    (
                        f"oracle doc 内の仕様文章を検索するときは、標準的なキーワード検索に加えて、MCP tool `{SEARCH_MCP_SERVER}.{SEARCH_TOOL_NAME}` によるベクトル検索も併用すること"
                        if search_mcp_tool_available
                        else "任意の方法で関係文章を検索すること"
                    ),
                    "検索の結果得られた位置情報を手がかりに、原文を読んで確認すること。",
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
        ),
    )
