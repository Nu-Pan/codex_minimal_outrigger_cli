from pathlib import Path

from agent_call_parameters.prompt_parts.realization_standards import (
    build_realization_standards,
)
from utils.struct_docs import render_as_markdown


def test_build_realization_standards_renders_same_content_as_oracle() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    expected = (
        repo_root / "oracles" / "docs" / "app_specs" / "realization" / "standards.md"
    ).read_text()

    actual = render_as_markdown(build_realization_standards())

    assert _compact_markdown(actual) == _compact_markdown(expected)


def _compact_markdown(markdown: str) -> list[str]:
    return [line.rstrip() for line in markdown.splitlines() if line.strip()]
