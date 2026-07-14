"""oracle.acp_builder を acp.builder として公開する互換入口。

`{{work-root}}/oracle/src/oracle/acp_builder` を正本に保ったまま既存の
`acp.builder.*` 参照を成立させるために残す。削除条件は realization 側と
利用者向け公開面から `acp.builder.*` 参照がなくなること。
"""

import sys
from importlib import import_module
from importlib.util import find_spec

_oracle_spec = find_spec("oracle.acp_builder")
if _oracle_spec is None or _oracle_spec.submodule_search_locations is None:
    raise ModuleNotFoundError("oracle.acp_builder package was not found")

# `{{work-root}}/oracle/src/oracle/acp_builder` supplies canonical modules such
# as `basic.py`; local wrappers stay first in `__path__` so they can adapt
# oracle outputs where compatibility still needs it.
for _path in _oracle_spec.submodule_search_locations:
    if _path not in __path__:
        __path__.append(_path)

_basic_module = import_module("oracle.acp_builder.basic")
sys.modules[f"{__name__}.basic"] = _basic_module
setattr(sys.modules[__name__], "basic", _basic_module)
