"""`src` だけの起動でも正本側 `oracle.*` を解決する package shim。"""

from pathlib import Path

# `{{work-root}}/oracle/src` は packaged realization tree の外にあるが、既存の
# compatibility module は canonical oracle module を再公開する。
_oracle_package = Path(__file__).resolve().parents[1] / "oracle" / "src" / "oracle"

if not _oracle_package.is_dir():
    raise ModuleNotFoundError(f"oracle package source was not found: {_oracle_package}")

__path__ = [str(_oracle_package)]
