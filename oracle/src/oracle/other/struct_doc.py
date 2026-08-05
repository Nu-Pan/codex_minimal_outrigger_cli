"""
# Structured markdown

- 階層構造を持つ自然言語文章を markdown にレンダリングするためのヘルパークラス
- 主に見出しの深さを自動計算してくれることに価値がある
"""

# std
import re
import textwrap
from xml.sax.saxutils import quoteattr

_CMOC_REF_PATTERN = re.compile(r'<cmoc_ref target="([^"]+)"/>')


class StructDoc:
    """
    構造化文章クラス
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
        self._children: list[StructDoc | StructBlock] | StructCodeBlock | str
        if len(children) == 1 and isinstance(children[0], (StructCodeBlock, str)):
            self._children = children[0]
        else:
            self._children = list()
            for c in children:
                if isinstance(c, (StructDoc, StructBlock)):
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
    def children(
        self,
    ) -> "list[StructDoc | StructBlock] | StructCodeBlock | str":
        """
        子要素を取得する
        """
        return self._children


class StructBlock:
    """
    `cmoc_block` としてレンダリングする親要素

    プロンプト内でこのブロック参照するには `<cmoc_ref target="..."/>` の形式で記述する
    """

    def __init__(self, block_id: str, child: StructDoc):
        if not isinstance(block_id, str):
            raise TypeError(f"block_id has unexpected type (type={type(block_id)})")
        if not block_id:
            raise ValueError("block_id must not be empty")
        if not isinstance(child, StructDoc):
            raise TypeError(f"child has unexpected type (type={type(child)})")
        self._block_id = block_id
        self._child = child

    @property
    def block_id(self) -> str:
        return self._block_id

    @property
    def child(self) -> StructDoc:
        return self._child


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


def render_as_markdown(
    struct_doc: StructDoc | StructBlock | list[StructDoc | StructBlock],
) -> str:
    """
    struct_doc を markdown としてレンダリングする
    """
    if isinstance(struct_doc, (StructDoc, StructBlock)):
        roots = [struct_doc]
    elif isinstance(struct_doc, list):
        roots = struct_doc
        for root in roots:
            if not isinstance(root, (StructDoc, StructBlock)):
                raise TypeError(
                    f"struct_doc contains unexpected type element (type={type(root)})"
                )
    else:
        raise TypeError(f"Invalid type of struct_doc (type={type(struct_doc)})")
    _validate_references(roots)
    return "\n".join(_render_as_markdown(root) for root in roots)


def _render_as_markdown(
    struct_node: StructDoc | StructBlock,
    depth: int = 1,
) -> str:
    """
    struct_node を markdown としてレンダリングする
    内部実装
    """
    if isinstance(struct_node, StructBlock):
        result = f"<cmoc_block id={quoteattr(struct_node.block_id)}>\n"
        result += _render_as_markdown(struct_node.child, depth)
        result += "</cmoc_block>\n"
        return _collapse_blank_lines(result)

    struct_doc = struct_node
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
            result += "```\n"
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


def _validate_references(roots: list[StructDoc | StructBlock]) -> None:
    """
    参照先ブロックの欠落と block id の重複をレンダリング直前に検査する。

    根拠: <work-root>/oracle/doc/app_spec/prompt_standard.md
    """
    blocks: dict[str, StructBlock] = {}
    refs: list[str] = []

    def _visit(node: StructDoc | StructBlock) -> None:
        if isinstance(node, StructBlock):
            if node.block_id in blocks:
                raise ValueError(f"Duplicate cmoc_block id (id={node.block_id!r})")
            blocks[node.block_id] = node
            _visit(node.child)
            return

        if isinstance(node.children, list):
            for child in node.children:
                _visit(child)
        elif isinstance(node.children, str):
            matches = list(_CMOC_REF_PATTERN.finditer(node.children))
            if node.children.count("<cmoc_ref") != len(matches):
                raise ValueError("Invalid cmoc_ref syntax")
            refs.extend(match.group(1) for match in matches)

    for root in roots:
        _visit(root)

    for target in refs:
        if target not in blocks:
            raise ValueError(f"cmoc_ref target is not present (target={target!r})")


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
