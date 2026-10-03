"""検索用コンポーネントの識別情報、設定型、および MCP の入出力と利用説明。

意味仕様の委譲元は `{{cmoc-root}}/oracle/doc/app_spec/document_search.md` の
「初期方式と推論の失敗」「stdio MCP と失敗の公開」「設定と未確定事項」。
"""

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal, TypedDict

from oracle.acp_builder.basic import DocumentSearchScope


@dataclass(frozen=True)
class ModelArtifact:
    """取得と互換性照合に共用する固定 GGUF の識別情報。"""

    repository: str
    revision: str
    filename: str
    size_bytes: int
    sha256: str
    tokenizer_metadata_sha256: str
    pooling: Literal["LAST"]


@dataclass(frozen=True)
class SearchMaterials:
    """推論・ベクトル演算のために初期採用する検索用コンポーネントの組合せ。"""

    node_version: str
    node_llama_cpp_version: str
    llama_cpp_revision: str
    sqlite_vec_version: str
    embedding: ModelArtifact
    embedding_dimensions: int


# NOTE 2026-09-25 の PoC の報告表と materials.json を照合した初期採用のコンポーネント。
# 一時コードや取得元のローカル path は製品の依存にしない。
INITIAL_SEARCH_MATERIALS = SearchMaterials(
    node_version="22.23.2",
    node_llama_cpp_version="3.20.0",
    llama_cpp_revision="b10361",
    sqlite_vec_version="0.1.9",
    embedding=ModelArtifact(
        repository="Qwen/Qwen3-Embedding-4B-GGUF",
        revision="f4602530db1d980e16da9d7d3a70294cf5c190be",
        filename="Qwen3-Embedding-4B-Q4_K_M.gguf",
        size_bytes=2496703776,
        sha256="2b0cf8f17b4c723c27303015383c27ec4bf2d8314bb677d05e920dd70bb0f16b",
        tokenizer_metadata_sha256=(
            "768390d5a5a3dedfa0aea66e9342fabb445b142559029d0b4821c064b6045957"
        ),
        pooling="LAST",
    ),
    embedding_dimensions=2560,
)

# 文書は本文だけを渡し、embedding tokenizer の special-token interpretation は無効。
EMBEDDING_QUERY_TEMPLATE = (
    "Instruct: Given a web search query, retrieve relevant passages that answer the query"
    "\nQuery:{query}"
)

# candidate_count と MCP 引数 limit に共通する、指定可能な件数の範囲。
SEARCH_CANDIDATE_COUNT_MIN = 20
SEARCH_CANDIDATE_COUNT_MAX = 50


@dataclass(frozen=True)
class DocumentSearchConfig:
    """検索 tuning の型・制約と、生成・補完に使う暫定既定値。

    NOTE
        int の項目は JSON 整数、float の項目は有限の JSON 数値とする。
        bool を数値として受理しない。chunk_overlap_tokens 以外は正数、
        chunk_overlap_tokens は 0 以上 chunk_tokens 未満。
        candidate_count は SEARCH_CANDIDATE_COUNT_MIN 以上
        SEARCH_CANDIDATE_COUNT_MAX 以下。
        chunk_tokens は embedding_context_tokens より小さくし、
        本文以外の入力の余地を残す。この大小関係だけで入力全体の収容を保証せず、
        文書・query それぞれに入力整形・特殊 token を加えた実入力が
        embedding tokenizer の context 上限内に収まることも検証する。
    """

    chunk_tokens: int = 512
    chunk_overlap_tokens: int = 64
    candidate_count: int = 50
    embedding_context_tokens: int = 2048
    batch_tokens: int = 512
    threads: int = 4
    startup_timeout_seconds: float = 120.0
    request_timeout_seconds: float = 600.0
    shutdown_grace_seconds: float = 5.0
    resource_wait_timeout_seconds: float = 600.0
    sync_no_progress_timeout_seconds: float = 600.0
    post_sync_search_timeout_seconds: float = 600.0
    search_request_timeout_seconds: float = 3600.0


SEARCH_MCP_SERVER = "cmoc_document_search"
SEARCH_TOOL_NAME = "search"
SEARCH_TOOL_INPUT_SCHEMA: dict[str, object] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["query"],
    "properties": {
        "query": {
            "type": "string",
            "minLength": 1,
            "pattern": "\\S",
            "description": "許可された oracle/doc の原文候補を探す検索文。",
        },
        "limit": {
            "type": "integer",
            "minimum": SEARCH_CANDIDATE_COUNT_MIN,
            "maximum": SEARCH_CANDIDATE_COUNT_MAX,
            "description": (
                "ファイル集約・行範囲統合前の候補箇所数の上限。"
                f"{SEARCH_CANDIDATE_COUNT_MIN}〜{SEARCH_CANDIDATE_COUNT_MAX} の整数。"
                "省略時は設定された candidate_count を使い、"
                "指定時は limit と candidate_count の小さい方を採用する。"
            ),
        },
    },
}


def build_search_tool_description(
    work_root: Path,
    scope: DocumentSearchScope,
) -> str:
    """検索接続の固定 context を含む、agent 向けの tool 利用説明を構築する。

    Args:
        work_root: 検索接続に設定された work-root の絶対パス。
        scope: 同じ接続に設定された閲覧範囲。

    Returns:
        MCP の tool description として公開する文面。

    NOTE
        意味仕様は `{{cmoc-root}}/oracle/doc/app_spec/document_search.md` の
        「検索と routing」「対象と信頼境界」「stdio MCP と失敗の公開」を参照。
    """
    # 引数説明と併せて、仕様文書を参照せず結果と検索範囲を解釈できるようにする。
    return (
        "許可された oracle/doc 内の Markdown を意味検索し、現在原文の候補位置を返す。\n\n"
        '- 成功結果は `status: "ok"` と `hits`。各 hit は work-root 相対の '
        "`path` と、`[開始行, 終了行]` の配列 `ranges` を持つ。"
        "行番号は 1 起点で両端を含む。同一パスは一度だけ掲載し、"
        "重複・重なりのある行範囲は統合する。本文・抜粋・見出し文・スコアは含まない。\n"
        f"- 候補不足なら {SEARCH_CANDIDATE_COUNT_MIN} 件未満でも返る。"
        "ファイル集約・行範囲統合後のファイル数や行範囲数は、候補箇所数より少なくなり得る。\n"
        "- `hits` が空なら成功ゼロ件。検索中の失敗は `isError=true` と "
        '`status: "error"`・`code`・`message` で返す。引数不正は MCP の入力エラー。\n'
        f"- この検索接続の work-root は `{work_root}`。"
        "対象はその配下の oracle/doc 内で閲覧を許可された Markdown のみ。"
        "root や閲覧範囲は tool 引数から変更できない。\n"
        "- 以下は work-root 相対 path による閲覧範囲。allowed_files は個別 file、"
        "allowed_subtrees は配下、excluded_files/excluded_subtrees は優先する除外。"
        "許可の両配列が空なら対象なし。oracle file の分類と、この call の閲覧制限も適用される。\n"
        f"```json\n{json.dumps(asdict(scope), ensure_ascii=False)}\n```"
    )


class SearchHit(TypedDict):
    """一つのファイルに集約された候補位置の形式。

    ranges は空でない配列で、各 tuple は JSON では [開始行, 終了行] とする。
    行番号は bool を除く JSON 整数で、1 <= 開始行 <= 終了行、両端を含む。
    候補情報の field は path と ranges に限る。
    """

    path: str  # work-root 相対の POSIX path
    ranges: list[tuple[int, int]]


class SearchResult(TypedDict):
    """正常完了した検索結果。hits はファイル単位で、空配列も成功を表す。"""

    status: Literal["ok"]
    hits: list[SearchHit]


type SearchErrorCode = Literal[
    "INVALID_SCOPE",
    "ROOT_UNAVAILABLE",
    "ENUMERATION_FAILED",
    "READ_FAILED",
    "SYNC_FAILED",
    "SOURCE_CHANGED",
    "NOT_READY",
    "MODEL_IDENTITY_MISMATCH",
    "MODEL_FAILURE",
    "DEADLINE_EXCEEDED",
    "CANCELLED",
]


class SearchFailure(TypedDict):
    """MCP isError=true で返す検索失敗。正常結果を併記しない。"""

    status: Literal["error"]
    code: SearchErrorCode
    message: str
