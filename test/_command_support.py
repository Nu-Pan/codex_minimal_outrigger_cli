import sys
from pathlib import Path


def write_python_executable(path: Path, lines: list[str]) -> None:
    """fake external command として使う executable Python script を書き込む。"""
    # {{work-root}}/oracle/doc/dev_rule/development_environment.md は BOM なし UTF-8 を求める。
    path.write_text("\n".join([f"#!{sys.executable}", *lines]) + "\n", encoding="utf-8")
    path.chmod(0o755)
