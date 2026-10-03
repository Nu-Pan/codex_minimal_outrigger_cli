"""検索用コンポーネントの識別情報、設定型、および MCP の入出力と利用説明。

意味仕様の委譲元は `{{cmoc-root}}/oracle/doc/app_spec/document_search.md` の
「初期方式と推論の失敗」「stdio MCP と失敗の公開」「設定と未確定事項」。
"""

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal, TypedDict, get_args

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
    "description": (
        "検索文と任意の候補箇所数の上限だけを指定する。"
        "不正な引数は JSON-RPC の入力エラー（code: -32602）となり、"
        "検索結果の structuredContent は返さない。"
    ),
    "additionalProperties": False,
    "required": ["query"],
    "properties": {
        "query": {
            "type": "string",
            "minLength": 1,
            "pattern": "\\S",
            "description": (
                "許可された oracle/doc の原文候補を探す検索文。"
                "空文字・空白だけの文字列は不可。"
            ),
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
                "candidate_count は検索要求で使う設定上限で、引数では拡張できない。"
                f"候補不足なら {SEARCH_CANDIDATE_COUNT_MIN} 件未満でも返る。"
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
    # 入出力の詳細は schema に置き、ここでは機能と接続の閲覧境界を伝える。
    return (
        "許可された oracle/doc 内の Markdown を意味検索し、現在原文の候補位置を返す。\n\n"
        f"- この検索接続の work-root は `{work_root}`。"
        "対象はその配下の oracle/doc 内で閲覧を許可された通常の `.md` ファイルのみ。"
        "root や閲覧範囲は tool 引数から変更できない。\n"
        "- 以下は work-root 相対 path による閲覧範囲。allowed_files は個別 file、"
        "allowed_subtrees は配下、excluded_files/excluded_subtrees は優先する除外。"
        "許可の両配列が空なら対象なし。所属する Git repository で未追跡かつ ignore 対象のファイル、"
        "AGENTS.md、Git metadata、symlink は検索対象に含めない。"
        "検索を使っても、この call のファイルアクセス制限は拡張されない。\n"
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


SEARCH_TOOL_OUTPUT_SCHEMA: dict[str, object] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "description": (
        "MCP result の structuredContent。content の text にも同じ JSON を返す。"
        "成功と構造化された検索失敗を表し、JSON-RPC protocol error は対象外。"
    ),
    "oneOf": [
        {
            "type": "object",
            "description": "正常完了した検索結果。MCP result の isError は false。",
            "additionalProperties": False,
            "required": ["status", "hits"],
            "properties": {
                "status": {
                    "type": "string",
                    "const": "ok",
                    "description": "検索成功。hits が空でも成功ゼロ件を表す。",
                },
                "hits": {
                    "type": "array",
                    "description": (
                        "採用した候補箇所をファイルごとに集約した位置情報。"
                        "同一パスは一度だけ掲載する。ファイル数や行範囲数は、"
                        "limit・candidate_count が数える集約前の候補箇所数より少なくなり得る。"
                        "本文・抜粋・見出し文・スコアは含まない。"
                    ),
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["path", "ranges"],
                        "properties": {
                            "path": {
                                "type": "string",
                                "minLength": 1,
                                "description": (
                                    "この検索接続の work-root 相対の POSIX path。"
                                    "現在原文のファイルを指す。"
                                ),
                            },
                            "ranges": {
                                "type": "array",
                                "minItems": 1,
                                "description": (
                                    "ファイル内の候補行範囲。重複・重なりのある範囲は統合済み。"
                                ),
                                "items": {
                                    "type": "array",
                                    "minItems": 2,
                                    "maxItems": 2,
                                    "items": {"type": "integer", "minimum": 1},
                                    "description": (
                                        "[開始行, 終了行]。行番号は 1 起点で両端を含み、"
                                        "開始行 <= 終了行。同じ行番号二つは一行だけの範囲。"
                                    ),
                                },
                            },
                        },
                    },
                },
            },
        },
        {
            "type": "object",
            "description": (
                "検索中の失敗。MCP result の isError は true。正常結果を併記しない。"
            ),
            "additionalProperties": False,
            "required": ["status", "code", "message"],
            "properties": {
                "status": {
                    "type": "string",
                    "const": "error",
                    "description": "検索失敗。成功ゼロ件とは区別する。",
                },
                "code": {
                    "type": "string",
                    "enum": list(get_args(SearchErrorCode.__value__)),
                    "description": (
                        "INVALID_SCOPE: 閲覧範囲不正、ROOT_UNAVAILABLE: work-root 利用不能、"
                        "ENUMERATION_FAILED: 列挙失敗、READ_FAILED: 読取失敗、"
                        "SYNC_FAILED: 同期・保存失敗、SOURCE_CHANGED: 本文変更競合、"
                        "NOT_READY: 検索未準備、MODEL_IDENTITY_MISMATCH: コンポーネント不一致、"
                        "MODEL_FAILURE: 推論失敗、DEADLINE_EXCEEDED: 期限超過、CANCELLED: 取消。"
                    ),
                },
                "message": {
                    "type": "string",
                    "description": "失敗理由と、案内可能な場合は対処方法。",
                },
            },
        },
    ],
}
