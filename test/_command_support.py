import sys
from pathlib import Path


def write_python_executable(path: Path, lines: list[str]) -> None:
    """Write an executable Python script used as a fake external command."""
    # {{work-root}}/oracle/doc/dev_rule/development_environment.md requires UTF-8 without BOM.
    path.write_text("\n".join([f"#!{sys.executable}", *lines]) + "\n", encoding="utf-8")
    path.chmod(0o755)
