"""検索と現在原文の確認による routing 規定文面の構築定義。"""

import json
from dataclasses import asdict

from oracle.acp_builder.basic import DocumentSearchScope
from oracle.other.document_search import (
    SEARCH_CANDIDATE_COUNT_MAX,
    SEARCH_CANDIDATE_COUNT_MIN,
    SEARCH_MCP_SERVER,
    SEARCH_TOOL_NAME,
    DocumentSearchConfig,
)
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
                "必要なら候補箇所数の上限 `limit` を渡して原文候補を探せる。\n"
                f"- `limit` は {SEARCH_CANDIDATE_COUNT_MIN}〜{SEARCH_CANDIDATE_COUNT_MAX} の整数。"
                "省略時は設定された `candidate_count`"
                f"（既定値 {DocumentSearchConfig().candidate_count}）を使う。"
                "指定時は `limit` と `candidate_count` の小さい方が採用上限となる。\n"
                "- 件数はファイル集約・行範囲統合前の候補箇所数を表す。"
                f"候補不足なら {SEARCH_CANDIDATE_COUNT_MIN} 件未満でも返り、"
                "集約後のファイル数や行範囲数はさらに少なくなることがある。\n"
                '- 成功結果は `status: "ok"` と `hits`。`hits` の各要素は、'
                "work-root 相対のファイルパス `path` と、"
                "`[開始行, 終了行]` の配列 `ranges` を持つ。"
                "行番号は 1 起点で両端を含み、同一パスは一度だけ、"
                "重複・重なりのある行範囲は統合して返る。本文・抜粋・見出し文・スコアは含まない。\n"
                "- 返されたパスと行範囲を手掛かりに、必要な現在原文を選び、読んで確認すること。"
                "`hits` が空なら成功ゼロ件であり、"
                '`isError=true` と `status: "error"`・`code`・`message` を伴う検索中の失敗と区別する。'
                "引数不正は MCP の入力エラーとして返る。\n"
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
                    (
                        "oracle/doc 内の仕様文章を検索するときは、標準的なキーワード検索に加えて、MCP tool によるベクトル検索も併用すること"
                        if document_search_scope is not None
                        else "oracle/doc 内の仕様文章を調べるときは、許可された原文への直接参照や標準的なキーワード検索を利用すること"
                    ),
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
