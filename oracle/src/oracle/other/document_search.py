"""文書検索の資材識別、設定型、および MCP 入出力の正確な定義。

意味仕様の委譲元は `{{cmoc-root}}/oracle/doc/app_spec/document_search.md` の
「初期方式と推論の失敗」「stdio MCP と失敗の公開」「設定と未確定事項」。
"""

from dataclasses import dataclass
from typing import Literal, TypedDict


@dataclass(frozen=True)
class ModelArtifact:
    """取得と互換性照合に共用する固定 GGUF の識別情報。"""

    repository: str
    revision: str
    filename: str
    size_bytes: int
    sha256: str
    tokenizer_metadata_sha256: str
    pooling: Literal["LAST", "RANK"]


@dataclass(frozen=True)
class SearchMaterials:
    """初期採用する推論・ベクトル演算資材の組合せ。"""

    node_version: str
    node_llama_cpp_version: str
    llama_cpp_revision: str
    sqlite_vec_version: str
    embedding: ModelArtifact
    reranker: ModelArtifact
    embedding_dimensions: int


# NOTE 2026-09-25 の PoC の報告表と materials.json を照合した初期採用資材。
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
    reranker=ModelArtifact(
        repository="giladgd/Qwen3-Reranker-4B-GGUF",
        revision="618ca919a196583806708d695f64dc002bd229a3",
        filename="Qwen3-Reranker-4B.Q4_K_M.gguf",
        size_bytes=2496717472,
        sha256="941f7d1d1524251c026a797b803ac9575545c5d7aa19b26e0e49661d7720af49",
        tokenizer_metadata_sha256=(
            "6971da22c3bb7eeef0ef7d05ff8936f7a2403ad33387988dc2ac5c5655229d26"
        ),
        pooling="RANK",
    ),
    embedding_dimensions=2560,
)

# 文書は本文だけを渡し、embedding tokenizer の special-token interpretation は無効。
EMBEDDING_QUERY_TEMPLATE = (
    "Instruct: Given a web search query, retrieve relevant passages that answer the query"
    "\nQuery:{query}"
)
# reranker は固定 GGUF 内の template と yes/no classifier を使う。
RERANKER_INPUT_FORMAT = "gguf_template_yes_no"
# 内部 API を採用する場合の互換検査対象。実際の raw 採点の欠落を検査する。
RAW_RANKING_API = (
    "LlamaRankingContext._getEvaluationInput",
    "LlamaRankingContext._llamaContext._ctx.getEmbedding",
)


@dataclass(frozen=True)
class DocumentSearchConfig:
    """全体測定で確定する tuning 値。PoC の数値を既定値にしない。

    NOTE
        個数・token 上限・threads は正整数、期限・猶予は有限の正数。
        overlap は 0 以上 chunk_tokens 未満。context は入力整形と特殊 token を
        含む入力を収容できることを検証する。bool を数値として受理しない。
    """

    chunk_tokens: int
    chunk_overlap_tokens: int
    candidate_count: int
    embedding_context_tokens: int
    reranker_context_tokens: int
    batch_tokens: int
    threads: int
    startup_timeout_seconds: float
    request_timeout_seconds: float
    shutdown_grace_seconds: float


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
            "minimum": 1,
            "description": "返す候補の最大件数。省略時は設定された候補数。",
        },
    },
}


class SearchHit(TypedDict):
    """現在確認した原文の箇所。行番号は 1 起点で両端を含む。"""

    path: str  # work-root 相対の POSIX path
    start_line: int
    end_line: int
    excerpt: str


class SearchResult(TypedDict):
    """正常完了した検索結果。hits の空配列も成功を表す。"""

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
