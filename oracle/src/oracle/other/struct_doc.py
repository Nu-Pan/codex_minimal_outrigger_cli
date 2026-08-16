"""
# Structured markdown

- 階層構造を持つ自然言語文章を markdown にレンダリングするためのヘルパークラス
- 主に見出しの深さを自動計算してくれることに価値がある
"""

# std
import re
import textwrap
from collections.abc import Sequence
from html import unescape
from xml.sax.saxutils import quoteattr

_CMOC_BLOCK_PATTERN = re.compile(r'<cmoc_block id="([^"]+)>')
_CMOC_REF_PATTERN = re.compile(r'<cmoc_ref target="([^"]+)"/>')


class StructDoc:
    """
    構造化文章クラス

    Markdown 的に言うところの、見出しを先頭とするブロック１つを表す。
    """

    def __init__(
        self,
        title: str,
        *children: "StructDoc|StructBlock|StructCodeBlock|str",
    ):
        """
        コンストラクタ
        """
        self._title = title
        self._children: list[StructDoc | StructBlock | StructCodeBlock | str]
        if len(children) == 0:
            raise ValueError(f"children must not be empty (title={title})")
        if len(children) == 1 and isinstance(
            children[0], (StructDoc, StructBlock, StructCodeBlock, str)
        ):
            self._children = [children[0]]
        else:
            self._children = list()
            for c in children:
                if isinstance(c, (StructDoc, StructBlock, StructCodeBlock, str)):
                    self._children.append(c)
                else:
                    raise TypeError(
                        f"children contains unexpected type element (title={title}, type={type(c)})"
                    )

    @property
    def title(self) -> str:
        """
        見出しテキストを取得する
        """
        return self._title

    @property
    def children(
        self,
    ) -> "list[StructDoc | StructBlock | StructCodeBlock | str]":
        """
        子要素を取得する
        """
        return self._children


class StructBlock:
    """
    参照可能な文章ブロックを表すクラス

    このインスタンスの子要素 `{{child}}` は以下のようにレンダリングされる

    ```markdown
    <cmoc_block id="block_id">
    {{child}}
    </cmoc_block>
    ```

    このブロック参照するには `<cmoc_ref target="block_id"/>` の形式で記述する
    """

    def __init__(
        self,
        block_id: str,
        childlen: "StructDoc | StructBlock | Sequence[StructDoc | StructBlock] | str",
    ):
        # ブロック ID
        if not isinstance(block_id, str):
            raise TypeError(f"block_id must be str (type={type(block_id)})")
        self._block_id = block_id
        # 子要素
        if isinstance(childlen, Sequence) and not isinstance(childlen, str):
            for child in childlen:
                if not isinstance(child, (StructDoc, StructBlock)):
                    raise TypeError(
                        f"child must contains StructDoc or StructBlock (type={type(child)})"
                    )
        elif not isinstance(childlen, (StructDoc, StructBlock, str)):
            raise TypeError(f"child has unexpected type (type={type(childlen)})")
        self._child = childlen

    @property
    def block_id(self) -> str:
        return self._block_id

    @property
    def childlen(
        self,
    ) -> "StructDoc | StructBlock | Sequence[StructDoc | StructBlock] | str":
        return self._child


class StructCodeBlock:
    """
    StructDoc 内に挿入可能なコードブロック

    Markdown 的に言う所の、 back quart 3 つ以上のフェンスで囲われたブロック
    ↓みたいなの

    ```{{info-here}}
    {{body-here}}
    ```
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


def render_as_markdown(
    struct_node: StructDoc | StructBlock | list[StructDoc | StructBlock],
) -> str:
    """
    struct_node を markdown としてレンダリングする
    """
    # 正規化と型チェック
    if isinstance(struct_node, (StructDoc, StructBlock)):
        roots = [struct_node]
    elif isinstance(struct_node, list):
        roots = struct_node
        for root in roots:
            if not isinstance(root, (StructDoc, StructBlock)):
                raise TypeError(
                    f"struct_doc contains unexpected type element (type={type(root)})"
                )
    else:
        raise TypeError(f"Invalid type of struct_doc (type={type(struct_node)})")
    # 内部処理に委託
    result = _collapse_blank_lines(
        "\n".join(_render_as_markdown(root) for root in roots)
    )
    # 正常終了
    return result


def _render_as_markdown(
    struct_node: StructDoc | StructBlock | StructCodeBlock | str,
    depth: int = 1,
) -> str:
    """
    struct_node を markdown としてレンダリングする
    内部実装
    """
    if isinstance(struct_node, StructDoc):
        return _render_as_markdown_struct_doc(struct_node, depth)
    elif isinstance(struct_node, StructBlock):
        return _render_as_markdown_struct_block(struct_node, depth)
    elif isinstance(struct_node, StructCodeBlock):
        return _render_as_markdown_struct_code_block(struct_node)
    elif isinstance(struct_node, str):
        return _render_as_markdown_str(struct_node)
    else:
        raise TypeError(
            f"struct_node must be `StructDoc | StructBlock | StructCodeBlock | str` (type={type(struct_node)})"
        )


def _render_as_markdown_struct_doc(
    struct_node: StructDoc,
    depth: int = 1,
) -> str:
    """
    struct_node を markdown としてレンダリングする
    内部実装
    StructDoc 専用
    """
    # 見出し
    result = ""
    result += ("#" * depth) + " " + struct_node.title + "\n"
    # 子要素
    if isinstance(struct_node.children, list):
        for c in struct_node.children:
            result += "\n"
            result += _render_as_markdown(c, depth + 1)
            result += "\n"
    else:
        raise TypeError(
            f"struct_node.children must be list (type={type(struct_node.children)})"
        )
    # 正常終了
    return result


def _render_as_markdown_struct_block(
    struct_node: StructBlock,
    depth: int = 1,
) -> str:
    """
    struct_node を markdown としてレンダリングする
    内部実装
    StructBlock 専用
    """
    result = f"<cmoc_block id={quoteattr(struct_node.block_id)}>\n"
    child = struct_node.childlen
    if isinstance(child, str):
        return result + child + "</cmoc_block>\n"
    if isinstance(child, Sequence):
        result += "\n".join(_render_as_markdown(element, depth) for element in child)
    else:
        result += _render_as_markdown(child, depth)
    result += "</cmoc_block>\n"
    return result


def _render_as_markdown_struct_code_block(
    struct_node: StructCodeBlock,
) -> str:
    """
    struct_node を markdown としてレンダリングする
    内部実装
    StructCodeBlock 専用

    NOTE:
        動的本文中の backtick が外側の Markdown code block を閉じないよう、
        本文の最長 backtick 列より 1 文字長く、かつ最低 3 文字の fence を使う。
    """
    # 本文を取得
    body = ntqs(struct_node.body)
    # フェンス文字列を生成
    longest_backtick_run_length = max(
        (len(match.group()) for match in re.finditer(r"`+", body)),
        default=0,
    )
    fence = "`" * max(3, longest_backtick_run_length + 1)
    # レンダリング
    result = ""
    if struct_node.info:
        result += f"{fence}{struct_node.info}\n"
    else:
        result += f"{fence}\n"
    result += body + "\n"
    result += f"{fence}\n"
    # 正常終了
    return result


def _render_as_markdown_str(
    struct_node: str,
) -> str:
    """
    struct_node を markdown としてレンダリングする
    内部実装
    str 専用
    """
    return ntqs(struct_node)


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
