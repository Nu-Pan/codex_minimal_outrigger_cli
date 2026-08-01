"""Repository local skill の YAML frontmatter 契約を検証する。"""

from collections.abc import Mapping
from pathlib import Path

import yaml

_WORK_ROOT = Path(__file__).resolve().parents[1]
_SKILLS_ROOT = _WORK_ROOT / ".agents" / "skills"


def test_repository_skill_frontmatter() -> None:
    """すべての repository local skill が必須 metadata を持つことを検証する。"""
    # skill の追加を自動で検査対象に含め、検査対象が空なら明示的に失敗させる。
    skill_paths = tuple(sorted(_SKILLS_ROOT.glob("*/SKILL.md")))
    assert skill_paths, f"repository local skill がありません: {_SKILLS_ROOT}"

    # YAML の安全な loader で、Codex が参照する必須 metadata を検証する。
    for skill_path in skill_paths:
        content = skill_path.read_text(encoding="utf-8")
        assert content.startswith("---\n"), (
            f"frontmatter の開始行がありません: {skill_path}"
        )
        frontmatter, separator, _body = content[4:].partition("\n---\n")
        assert separator, f"frontmatter の終了行がありません: {skill_path}"

        metadata = yaml.safe_load(frontmatter)
        assert isinstance(metadata, Mapping), (
            f"frontmatter が mapping ではありません: {skill_path}"
        )

        name = metadata.get("name")
        description = metadata.get("description")
        assert isinstance(name, str), f"name が文字列ではありません: {skill_path}"
        assert isinstance(description, str), (
            f"description が文字列ではありません: {skill_path}"
        )
        assert name == skill_path.parent.name, (
            f"name と skill directory が一致しません: {skill_path}"
        )
