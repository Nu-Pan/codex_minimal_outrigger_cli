"""検索用コンポーネントと MCP 返却値を実装内で扱う型。"""

import json
from dataclasses import dataclass
from importlib import resources
from typing import Any, Literal, TypedDict

from oracle.other.document_search import EMBEDDING_MODEL, SearchErrorCode


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
    llama_cpp_release: str
    llama_cpp_revision: str
    sqlite_vec_version: str
    document_embedding_contract: str
    embedding: ModelArtifact
    embedding_dimensions: int


def _initial_materials() -> SearchMaterials:
    # 採用記録は配布 package、モデルの詳細は正本から取り込む。
    package = json.loads(
        resources.files("commons.document_search_worker")
        .joinpath("package.json")
        .read_text(encoding="utf-8")
    )
    adopted = package["cmoc"]
    model: dict[str, Any] = dict(EMBEDDING_MODEL)
    dimensions = model.pop("embedding_dimensions")
    return SearchMaterials(
        node_version=package["engines"]["node"],
        node_llama_cpp_version=package["dependencies"]["node-llama-cpp"],
        llama_cpp_release=adopted["llama_cpp_release"],
        llama_cpp_revision=adopted["llama_cpp_revision"],
        sqlite_vec_version=adopted["sqlite_vec_version"],
        document_embedding_contract=adopted["document_embedding_contract"],
        embedding=ModelArtifact(**model),
        embedding_dimensions=dimensions,
    )


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
