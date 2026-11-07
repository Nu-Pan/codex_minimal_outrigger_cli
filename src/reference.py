"""`src` だけの起動でも正本側 `reference.*` を解決する package shim。"""

from pathlib import Path

# `{{work-root}}/reference/src` は packaged realization tree の外にあるが、既存の
# compatibility module は canonical reference module を再公開する。
_reference_package = (
    Path(__file__).resolve().parents[1] / "reference" / "src" / "reference"
)

if not _reference_package.is_dir():
    raise ModuleNotFoundError(
        f"reference package source was not found: {_reference_package}"
    )

__path__ = [str(_reference_package)]
