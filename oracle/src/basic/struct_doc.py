"""
# Structured markdown

- 階層構造を持つ自然言語文章を markdown にレンダリングするためのヘルパークラス
- 主に見出しの深さを自動計算してくれることに価値がある
"""

import textwrap


class StructDoc:
    """
    構造化文章クラス
    """

    def __init__(
        self,
        title: str,
        *children: "StructDoc|StructCodeBlock|str",
    ):
        """
        コンストラクタ
        """
        self._title = title
        self._children: list[StructDoc] | StructCodeBlock | str
        if len(children) == 1 and isinstance(children[0], (StructCodeBlock, str)):
            self._children = children[0]
        else:
            self._children = list()
            for c in children:
                if isinstance(c, StructDoc):
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
    def children(self) -> list["StructDoc"] | "StructCodeBlock" | str:
        """
        子要素を取得する
        """
        return self._children


class StructCodeBlock:
    """
    StructDoc 内に挿入可能なコードブロック
    """

    def __init__(
        self,
        info: str | None,
        body: str,
    ):
        """コンストラクタ

        info:
            コードブロックの先頭に挿入される info string
            指定なしの場合は None を渡す
            e.g. python, cpp, bash

        body:
            コードブロックで囲われる本体テキスト
        """
        self._info = info
        self._body = body

    @property
    def info(self) -> str | None:
        """
        info string を取得する
        """
        return self._info

    @property
    def body(self) -> str:
        """
        本体テキストを取得する
        """
        return self._body


def render_as_markdown(struct_doc: StructDoc | list[StructDoc]) -> str:
    """
    struct_doc を markdown としてレンダリングする
    """
    result = ""
    if isinstance(struct_doc, StructDoc):
        result += _render_as_markdown(struct_doc)
    elif isinstance(struct_doc, list):
        for sd in struct_doc:
            result += "\n"
            result += _render_as_markdown(sd)
    else:
        raise TypeError(f"Invalid type of struct_doc (type={type(struct_doc)})")
    return result


def _render_as_markdown(struct_doc: StructDoc, depth: int = 1) -> str:
    """
    struct_doc を markdown としてレンダリングする
    内部実装
    """
    # 見出しを生成
    result = ""
    result += ("#" * depth) + " " + struct_doc.title + "\n"
    # 子要素を追加
    if isinstance(struct_doc.children, list):
        for c in struct_doc.children:
            result += "\n"
            result += _render_as_markdown(c, depth + 1) + "\n"
    elif isinstance(struct_doc.children, StructCodeBlock):
        result += "\n"
        if struct_doc.children.info:
            result += f"```{struct_doc.children.info}\n"
        else:
            result += f"```\n"
        result += ntqs(struct_doc.children.body) + "\n"
        result += "```\n"
    elif isinstance(struct_doc.children, str):
        result += "\n"
        result += ntqs(struct_doc.children) + "\n"
    else:
        raise TypeError(
            f"Invalid type of struct_doc.children (type={type(struct_doc.children)})"
        )
    # TODO
    #   空行が２つ以上連続する場合、１つの空行にまとめる
    #   空白文字しか無い行も空行とみなす
    # 正常終了
    return result


def ntqs(text: str) -> str:
    """
    Triple quoted string で書かれた文字列を正規化する。
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
