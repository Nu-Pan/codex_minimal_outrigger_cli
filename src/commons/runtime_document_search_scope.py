"""信頼された workload が文書検索へ渡す閲覧範囲を構築する。"""

from dataclasses import asdict
from pathlib import PurePosixPath

from oracle.acp_builder.basic import DocumentSearchScope


def oracle_doc_scope() -> DocumentSearchScope:
    """oracle/doc 全体を参照できる workload の実効範囲を返す。

    呼び出し元は、その workload に追加の oracle/doc 閲覧禁止がないことを
    確認したうえで使用する。個別制限がある call は明示的な狭い範囲を作る。
    """
    return DocumentSearchScope(allowed_subtrees=("oracle/doc",))


def validate_document_search_scope(scope: DocumentSearchScope) -> DocumentSearchScope:
    """曖昧な path と型を拒否し、scope を正規形へ変換する。"""
    if not isinstance(scope, DocumentSearchScope):
        raise ValueError("document search scope is missing or invalid")
    normalized: dict[str, tuple[str, ...]] = {}
    for field, paths in asdict(scope).items():
        if not isinstance(paths, tuple):
            raise ValueError(f"invalid document search scope field: {field}")
        values: list[str] = []
        for value in paths:
            if (
                not isinstance(value, str)
                or not value
                or value.startswith("/")
                or "\\" in value
                or "\x00" in value
                or any(part in ("", ".", "..") for part in value.split("/"))
                or PurePosixPath(value).as_posix() != value
            ):
                raise ValueError(f"invalid document search scope path: {value!r}")
            values.append(value)
        normalized[field] = tuple(sorted(set(values)))
    return DocumentSearchScope(**normalized)


def scope_allows(scope: DocumentSearchScope, path: str) -> bool:
    """component 境界の subtree 許可と除外を評価する。"""

    def in_subtree(subtree: str) -> bool:
        return path == subtree or path.startswith(subtree + "/")

    included = path in scope.allowed_files or any(
        in_subtree(subtree) for subtree in scope.allowed_subtrees
    )
    excluded = path in scope.excluded_files or any(
        in_subtree(subtree) for subtree in scope.excluded_subtrees
    )
    return included and not excluded
