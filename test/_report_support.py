"""人間向け report を Markdown として読み、表示契約を確認する。"""

import yaml
from markdown_it import MarkdownIt


def report_text(content):
    """Markdown の装飾・HTML tag を除いた、読み手に見える本文を取り出す。"""
    return "\n".join(
        "".join(
            child.content
            for child in token.children or ()
            if child.type in {"text", "code_inline"}
        )
        for token in MarkdownIt().parse(content)
        if token.type == "inline"
    )


def report_metadata(content):
    tokens = MarkdownIt().parse(content)
    information = next(
        token.content
        for token in reversed(tokens)
        if token.type == "fence" and token.info == "yaml"
    )
    metadata = yaml.safe_load(information)
    assert isinstance(metadata, dict)
    return metadata


def report_section(content, heading):
    tokens = MarkdownIt().parse(content)
    for index, token in enumerate(tokens):
        if token.type != "heading_open" or tokens[index + 1].content != heading:
            continue
        start = token.map[1]
        end = next(
            (
                following.map[0]
                for following in tokens[index + 1 :]
                if following.type == "heading_open"
                and following.level <= token.level
                and following.tag <= token.tag
            ),
            len(content.splitlines()),
        )
        return "".join(content.splitlines(keepends=True)[start:end])
    raise AssertionError(f"report section is missing: {heading}")


def original_report_input(content):
    section = report_section(content, "元の指示")
    return next(
        token.content for token in MarkdownIt().parse(section) if token.type == "fence"
    ).removesuffix("\n")


def assert_report_layout(content):
    tokens = MarkdownIt().parse(content)
    assert tokens[0].type == "heading_open" and tokens[0].tag == "h1"
    assert not content.startswith("---")
    lines = content.splitlines()
    headings = []
    for index, token in enumerate(tokens):
        if token.type == "heading_open":
            headings.append(tokens[index + 1].content)
            start, end = token.map
            assert start == 0 or not lines[start - 1].strip(), lines[start]
            assert end == len(lines) or not lines[end].strip(), lines[start]
    assert headings.index("次の操作") < headings.index("元の指示")
    assert headings.index("元の指示") < headings.index("詳細結果")
    assert headings.index("詳細結果") < headings.index("実行記録")
    assert headings[-1] == "実行情報"
    assert report_metadata(content)["execution_id"]
