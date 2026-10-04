"""検索用コンポーネントと MCP 返却値を実装内で扱う型。"""

from dataclasses import dataclass
from typing import Any, Literal, TypedDict

from oracle.other.document_search import INITIAL_SEARCH_MATERIALS, SearchErrorCode


@dataclass(frozen=True)
class ModelArtifact:
    """取得と互換性照合に共用する GGUF の識別情報。"""

    repository: str
    revision: str
    filename: str
    size_bytes: int
    sha256: str
    tokenizer_metadata_sha256: str
    pooling: Literal["LAST"]


@dataclass(frozen=True)
class SearchMaterials:
    """準備・検査・索引 identity で共有するコンポーネントの組合せ。"""

    node_version: str
    node_llama_cpp_version: str
    llama_cpp_revision: str
    sqlite_vec_version: str
    embedding: ModelArtifact
    embedding_dimensions: int


def _initial_materials() -> SearchMaterials:
    # 正本の固定データを、実装で共用する dataclass へ変換する。
    values: dict[str, Any] = dict(INITIAL_SEARCH_MATERIALS)
    values["embedding"] = ModelArtifact(**values["embedding"])
    return SearchMaterials(**values)


SEARCH_MATERIALS = _initial_materials()


class SearchRange(TypedDict):
    """統合した候補位置と最大類似度を MCP 返却へ渡す。"""

    start_line: int
    end_line: int
    max_similarity: float


class SearchHit(TypedDict):
    """ファイルごとに集約した候補位置と類似度を MCP 返却へ渡す。"""

    path: str
    ranges: list[SearchRange]


class SearchResult(TypedDict):
    """公開 outputSchema に対応する検索成功の内部表現。"""

    status: Literal["ok"]
    hits: list[SearchHit]


class SearchFailure(TypedDict):
    """公開 outputSchema に対応する検索失敗の内部表現。"""

    status: Literal["error"]
    code: SearchErrorCode
    message: str
