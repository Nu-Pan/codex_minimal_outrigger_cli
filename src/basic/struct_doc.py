"""
# Structured markdown

対応 oracle file: `<work-root>/oracle/src/basic/struct_doc.py`。

- 階層構造を持つ自然言語文章を markdown にレンダリングするためのヘルパークラス
- 主に見出しの深さを自動計算してくれることに価値がある
"""

import textwrap


class StructDoc:
    """
    構造化文章クラス
    """

    def __init__(
        self: "StructDoc",
        title: str,
        *children: "StructDoc|StructCodeBlock|str",
    ) -> None:
        """見出しと子要素から構造化文章を作る。

        Args:
            title: Markdown 見出しとして出力するテキスト。
            children: 下位見出し、本文文字列、またはコードブロック。
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
    def title(self: "StructDoc") -> str:
        """
        見出しテキストを取得する
        """
        return self._title

    @property
    def children(self: "StructDoc") -> "list[StructDoc] | StructCodeBlock | str":
        """
        子要素を取得する
        """
        return self._children


class StructCodeBlock:
    """
    StructDoc 内に挿入可能なコードブロック
    """

    def __init__(
        self: "StructCodeBlock",
        info: str | None,
        body: str,
    ) -> None:
        """Markdown code fence として埋め込む本文を保持する。

        Args:
            info: code fence の info string。指定しない場合は None。
            body: code fence 内に出力する本文。
        """
        self._info = info
        self._body = body

    @property
    def info(self: "StructCodeBlock") -> str | None:
        """
        info string を取得する
        """
        return self._info

    @property
    def body(self: "StructCodeBlock") -> str:
        """
        本体テキストを取得する
        """
        return self._body


def render_as_markdown(struct_doc: StructDoc | list[StructDoc]) -> str:
    """構造化文章を Markdown としてレンダリングする。

    Args:
        struct_doc: 単一文書、または同じ深さで並べる文書リスト。
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
    result = _collapse_blank_lines(result)
    # 正常終了
    return result


def _collapse_blank_lines(text: str) -> str:
    """
    2 行以上連続する空行を 1 行にまとめる。
    空白文字だけの行も空行として扱う。
    """
    lines: list[str] = []
    previous_blank = False
    for line in text.splitlines():
        blank = not line.strip()
        if blank:
            if previous_blank:
                continue
            lines.append("")
        else:
            lines.append(line)
        previous_blank = blank
    if text.endswith("\n"):
        return "\n".join(lines) + "\n"
    return "\n".join(lines)


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
