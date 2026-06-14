"""
# Structured markdown

- 階層構造を持つ自然言語文章を markdown にレンダリングするためのヘルパークラス
- 主に見出しの深さを自動計算してくれることに価値がある
"""

import textwrap


class StructDocs:
    """
    構造化文章クラス
    """

    def __init__(
        self,
        title: str,
        *children: "StructDocs|str",
    ):
        """
        コンストラクタ
        """
        self._title = title
        self._children: list[StructDocs] | str
        if len(children) == 1 and isinstance(children[0], str):
            self._children = children[0]
        else:
            self._children = list()
            for c in children:
                if isinstance(c, StructDocs):
                    self._children.append(c)
                else:
                    raise TypeError(
                        f"children contains unexpected type element (type={type(c)})"
                    )

    @property
    def title(self) -> str:
        """
        見出しテキストを取得する
        """
        return self._title

    @property
    def children(self) -> list["StructDocs"] | str:
        """
        子要素を取得する
        """
        return self._children


def render_as_markdown(struct_docs: StructDocs | list[StructDocs]) -> str:
    """
    struct_docs を markdown としてレンダリングする
    """
    result = ""
    if isinstance(struct_docs, StructDocs):
        result += _render_as_markdown(struct_docs)
    elif isinstance(struct_docs, list):
        for sd in struct_docs:
            result += "\n"
            result += _render_as_markdown(sd)
    else:
        raise TypeError(f"Invalid type of struct_docs (type={type(struct_docs)})")
    return result


def _render_as_markdown(struct_docs: StructDocs, depth: int = 1) -> str:
    """
    struct_docs を markdown としてレンダリングする
    内部実装
    """
    # 見出しを生成
    result = ""
    result += ("#" * depth) + " " + struct_docs.title + "\n"
    # 子要素を追加
    if isinstance(struct_docs.children, list):
        for c in struct_docs.children:
            result += "\n"
            result += _render_as_markdown(c, depth + 1) + "\n"
    elif isinstance(struct_docs.children, str):
        result += "\n"
        result += ntqs(struct_docs.children) + "\n"
    else:
        raise TypeError(
            f"Invalid type of struct_docs.children (type={type(struct_docs.children)})"
        )
    # 正常終了
    return result


def ntqs(text: str) -> str:
    """
    Triple quarted string で書かれた文字列を正規化する。
    インデントを維持して書いた tqs を、インデントされていないような感じにする
    """
    # 先頭・末尾の空行だけを落としてから、共通インデントを解除する。
    lines = text.splitlines()
    start = 0
    end = len(lines)
    while start < end and not lines[start].strip():
        start += 1
    while start < end and not lines[end - 1].strip():
        end -= 1
    return textwrap.dedent("\n".join(lines[start:end]))
