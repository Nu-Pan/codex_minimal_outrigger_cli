import sys
from pathlib import Path


def write_python_executable(path: Path, lines: list[str]) -> None:
    """標準ライブラリだけで動く fake external command を書き込む。"""
    # {{work-root}}/spec/dev_rule/development_environment.md は BOM なし UTF-8 を求める。
    # fake には不要な site-packages と .pth の初期化を起動ごとに繰り返さない。
    path.write_text(
        "\n".join([f"#!{sys.executable} -S", *lines]) + "\n", encoding="utf-8"
    )
    path.chmod(0o755)
