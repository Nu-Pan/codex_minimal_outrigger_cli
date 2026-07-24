"""oracle.acp_builder を acp.builder として公開する互換入口。

`{{work-root}}/oracle/src/oracle/acp_builder` を正本に保ったまま既存の
`acp.builder.*` 参照を成立させるために残す。削除条件は realization 側と
利用者向け公開面から `acp.builder.*` 参照がなくなること。
"""

import sys as _sys
from importlib import import_module as _import_module
from importlib.util import find_spec as _find_spec

__all__ = ["basic"]

_oracle_spec = _find_spec("oracle.acp_builder")
if _oracle_spec is None or _oracle_spec.submodule_search_locations is None:
    raise ModuleNotFoundError("oracle.acp_builder package was not found")

# `{{work-root}}/oracle/src/oracle/acp_builder` は `basic.py` などの canonical module を
# 提供する。local wrapper を `__path__` の先頭に置き、compatibility が必要な場合に
# oracle output を適合させる。
for _path in _oracle_spec.submodule_search_locations:
    if _path not in __path__:
        __path__.append(_path)

_basic_module = _import_module("oracle.acp_builder.basic")
_sys.modules[f"{__name__}.basic"] = _basic_module
setattr(_sys.modules[__name__], "basic", _basic_module)
