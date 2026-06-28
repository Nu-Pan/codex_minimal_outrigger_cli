"""`src` だけの起動でも正本側 `oracle.*` を解決する package shim。"""

from pathlib import Path

# `<work-root>/oracle/src` is intentionally outside the packaged realization
# tree, but existing compatibility modules re-export canonical oracle modules.
_oracle_package = Path(__file__).resolve().parents[1] / "oracle" / "src" / "oracle"

if not _oracle_package.is_dir():
    raise ModuleNotFoundError(f"oracle package source was not found: {_oracle_package}")

__path__ = [str(_oracle_package)]
