from pathlib import Path

from oracle.acp_builder.basic import AgentCallParameter
from oracle.acp_builder.review.oracle.enumerate_finding import *  # noqa: F403
from oracle.acp_builder.review.oracle.enumerate_finding import (
    build_review_oracle_enumerate_finding_parameter as _build_parameter,
)
from oracle.other.path_model import resolve_real_path
from oracle.other.struct_doc import render_as_markdown
from oracle.prompt_builder.parts.apply_review_standard import build_apply_review_standard


def build_review_oracle_enumerate_finding_parameter(
    oracle_path: Path,
    related_findings: str,
) -> AgentCallParameter:
    parameter = _build_parameter(oracle_path, related_findings)
    return type(parameter)(
        parameter.model_class,
        parameter.reasoning_effort,
        parameter.file_access_mode,
        _append_review_context(parameter.prompt, oracle_path),
        parameter.structured_output_schema_path,
    )


def _append_review_context(prompt: str, oracle_path: Path) -> str:
    parts = [prompt.rstrip()]
    if "# apply review standard" not in prompt:
        parts.append(render_as_markdown(build_apply_review_standard()[1]).rstrip())
    parts.append(_target_oracle_file_section(oracle_path).rstrip())
    parts.append(_output_schema_section())
    return "\n\n".join(parts) + "\n"


def _target_oracle_file_section(oracle_path: Path) -> str:
    path = _resolve_path_for_prompt(oracle_path)
    body = path.read_text(encoding="utf-8") if path.is_file() else ""
    return (
        "# target oracle file\n\n"
        f"- path: `{path}`\n\n"
        f"{_fenced_code('markdown', body)}"
    )


def _resolve_path_for_prompt(oracle_path: Path) -> Path:
    try:
        return resolve_real_path(oracle_path)
    except (TypeError, ValueError):
        return oracle_path


def _output_schema_section() -> str:
    return (
        "# output schema\n\n"
        "- `findings` は新規所見の配列である\n"
        "- 各 finding は `severity`, `title`, `oracle_path`, `reason` を持つ\n"
        "- 新規所見がない場合は `findings: []` を返す"
    )


def _fenced_code(language: str, body: str) -> str:
    fence = "```"
    while fence in body:
        fence += "`"
    return f"{fence}{language}\n{body}\n{fence}"
