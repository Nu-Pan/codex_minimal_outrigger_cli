"""
- プログラム上は階層構造を保持し、それを自然言語文章にレンダリングするためのヘルパークラス
- 今のところ markdown だけサポート
- 主に見出しの深さを自動計算してくれることに価値がある
"""

# std
import re
import textwrap
from dataclasses import dataclass, field
from xml.sax.saxutils import quoteattr


class SDHeader:
    """文章のヘッダー（見出し）を表すクラス

    Markdown 的に言うところの、見出しを先頭とするブロック１つを表す。
    """

    def __init__(
        self,
        title: str,
        *children: "SDNode",
    ):
        """
        コンストラクタ
        """
        # タイトル
        self._title = title
        # 子要素
        self._children: "list[SDNode]"
        if len(children) == 0:
            raise ValueError(f"children must not be empty (title={title})")
        elif len(children) == 1:
            if isinstance(children[0], SDNode.__value__):
                self._children = [children[0]]
            else:
                raise TypeError(
                    "children contains unexpected type element "
                    f"(title={title}, type={type(children[0])})"
                )
        else:
            self._children = list()
            for c in children:
                if isinstance(c, SDNode.__value__):
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
    ) -> "list[SDNode]":
        """
        子要素を取得する
        """
        return self._children


class SDTagBlock:
    """XML タグ風表記によってマークされた参照可能な文章ブロックを表すクラス

    このインスタンスの子要素 `{{child}}` は以下のようにレンダリングされる

    ```markdown
    <cmoc_block id="block_id">
    {{child}}
    </cmoc_block>
    ```

    このブロック参照するには `<cmoc_ref target="block_id"/>` の形式で記述する
    この参照記法は `SDTagBlock.ref_tag` で生成可能
    """

    def __init__(
        self,
        block_id: str,
        *children: "SDNode",
    ):
        # ブロック ID
        if not isinstance(block_id, str):
            raise TypeError(f"block_id must be str (type={type(block_id)})")
        self._block_id = block_id
        # 子要素
        self._children: "list[SDNode]"
        if len(children) == 0:
            raise ValueError(f"children must not be empty (block_id={block_id})")
        elif len(children) == 1:
            if isinstance(children[0], SDNode.__value__):
                self._children = [children[0]]
            else:
                raise TypeError(
                    "children contains unexpected type element "
                    f"(block_id={block_id}, type={type(children[0])})"
                )
        else:
            self._children = list()
            for c in children:
                if isinstance(c, SDNode.__value__):
                    self._children.append(c)
                else:
                    raise TypeError(
                        f"children contains unexpected type element (block_id={block_id}, type={type(c)})"
                    )

    @property
    def block_id(self) -> str:
        return self._block_id

    @property
    def childlen(
        self,
    ) -> "list[SDNode]":
        return self._children

    @property
    def ref_tag(self) -> str:
        return f'<cmoc_ref target="{self._block_id}"/>'


@dataclass(frozen=True)
class SDCodeBlock:
    """自然言語文章中に埋め込み可能なコードブロックを表すクラス

    Markdown 的に言う所の、back quart 3 つ以上のフェンスで囲われたブロックのこと
    ↓みたいなの

    ```{{info-here}}
    {{body-here}}
    ```
    """

    # コードブロックの先頭に挿入される info string
    # 指定なしの場合は None を渡す
    # e.g. python, cpp, bash
    info: str | None

    # コードブロックで囲われる本体テキスト
    body: str


@dataclass(frozen=True)
class SDPolicy:
    """構造化された規定文章を表すクラス

    SDHeader 直下の単一要素として保持される事を想定している
    """

    # この規定が一体何者であるかを述べる
    what_is_this: str

    # 「必須」カテゴリに属する規定のリスト
    # 1 項目 1 文で「～しなければならない」「～すること」が並ぶ
    require: tuple[str, ...] = field(default_factory=lambda: tuple())

    # 「禁止」カテゴリに属する規定のリスト
    # 1 項目 1 文で「～してはいけない」「～は禁止」が並ぶ
    prohibit: tuple[str, ...] = field(default_factory=lambda: tuple())

    # 「許容」カテゴリに属する規定のリスト
    # 1 項目 1 文で「～してもよい」が並ぶ
    # 必須・禁止との違いは、する・しないの裁量がエージェントに委ねられている事
    allow: tuple[str, ...] = field(default_factory=lambda: tuple())

    # 各規定が言っていることを理解するために必要な補足情報のリスト
    # 1 項目 1 文で補足情報を並べる
    supplemental: tuple[str, ...] = field(default_factory=lambda: tuple())


# SD... 系クラスをまとめた型エイリアス
type SDNode = SDHeader | SDTagBlock | SDCodeBlock | SDPolicy | str


def render_sd_node_as_markdown(
    *sd_nodes: SDNode,
) -> str:
    """
    sd_node を markdown としてレンダリングする
    """
    return _collapse_blank_lines(_render_sd_node_as_markdown(*sd_nodes))


def _render_sd_node_as_markdown(
    *sd_nodes: SDNode,
    depth: int = 0,
) -> str:
    """sd_node を markdown としてレンダリングする

    内部実装の入口・再帰呼び出しの入口として使う
    """
    # 先頭から順番にレンダリングする
    individual: list[str] = list()
    for sd_node in sd_nodes:
        if isinstance(sd_node, SDHeader):
            individual.append(_render_sd_header_as_markdown(sd_node, depth + 1))
        elif isinstance(sd_node, SDTagBlock):
            # NOTE タグで囲っても見出しの深さは変わらないので depth はそのままで良い
            individual.append(_render_sd_tag_block_as_markdown(sd_node, depth))
        elif isinstance(sd_node, SDCodeBlock):
            individual.append(_render_sd_code_block_as_markdown(sd_node))
        elif isinstance(sd_node, SDPolicy):
            individual.append(_render_sd_policy_as_markdown(sd_node))
        elif isinstance(sd_node, str):
            individual.append(_render_str_as_markdown(sd_node))
        else:
            raise TypeError(
                f"Invalid sd_node type` (expect={SDNode}, actual={type(sd_node)})"
            )
    return "\n".join(individual)


def _render_sd_header_as_markdown(
    sd_node: SDHeader,
    depth: int,
) -> str:
    """sd_node を markdown としてレンダリングする

    内部実装
    SDHeader 専用
    """
    # 見出し
    result = ""
    result += ("#" * depth) + " " + sd_node.title + "\n"
    # 子要素
    if isinstance(sd_node.children, list):
        for c in sd_node.children:
            result += "\n"
            result += _render_sd_node_as_markdown(c, depth=depth)
            result += "\n"
    else:
        raise TypeError(
            f"sd_node.children must be list (type={type(sd_node.children)})"
        )
    return result


def _render_sd_tag_block_as_markdown(
    sd_node: SDTagBlock,
    depth: int,
) -> str:
    """sd_node を markdown としてレンダリングする

    内部実装
    SDTagBlock 専用
    """
    # ブロック開始
    result = "\n"
    result += f"<cmoc_block id={quoteattr(sd_node.block_id)}>\n"
    result += "\n"
    # 中身
    for child in sd_node.childlen:
        result += "\n"
        result += _render_sd_node_as_markdown(child, depth=depth)
        result += "\n"
    # ブロック終了
    result += "\n"
    result += "</cmoc_block>\n"
    result += "\n"
    return result


def _render_sd_code_block_as_markdown(
    sd_node: SDCodeBlock,
) -> str:
    """sd_node を markdown としてレンダリングする

    内部実装
    SDCodeBlock 専用

    NOTE
        動的本文中の backtick が外側の Markdown code block を閉じないよう、
        本文の最長 backtick 列より 1 文字長く、かつ最低 3 文字の fence を使う。
    """
    # 本文を取得
    body = ntqs(sd_node.body)
    # フェンス文字列を生成
    longest_backtick_run_length = max(
        (len(match.group()) for match in re.finditer(r"`+", body)),
        default=0,
    )
    fence = "`" * max(3, longest_backtick_run_length + 1)
    # レンダリング
    result = ""
    if sd_node.info:
        result += f"{fence}{sd_node.info}\n"
    else:
        result += f"{fence}\n"
    result += body + "\n"
    result += f"{fence}\n"
    return result


def _render_sd_policy_as_markdown(
    sd_node: SDPolicy,
):
    """sd_node を markdown としてレンダリングする

    内部実装
    str 専用
    """
    result: list[str] = list()
    if sd_node.what_is_this:
        result += [
            "",
            sd_node.what_is_this,
            "",
        ]
    if sd_node.require:
        result += [
            "",
            "**必須**",
            "",
        ]
        result += [f"- {r}" for r in sd_node.require]
        result += [
            "",
        ]
    if sd_node.prohibit:
        result += [
            "",
            "**禁止**",
            "",
        ]
        result += [f"- {p}" for p in sd_node.prohibit]
        result += [
            "",
        ]
    if sd_node.allow:
        result += [
            "",
            "**許容**",
            "",
        ]
        result += [f"- {a}" for a in sd_node.allow]
        result += [
            "",
        ]
    if sd_node.supplemental:
        result += [
            "",
            "**補足情報**",
            "",
        ]
        result += [f"- {s}" for s in sd_node.supplemental]
        result += [
            "",
        ]
    return "\n".join(result)


def _render_str_as_markdown(
    sd_node: str,
) -> str:
    """sd_node を markdown としてレンダリングする

    内部実装
    str 専用
    """
    return ntqs(sd_node)


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
