"""oracle.request_builder を acp.builder として公開する互換入口。

`{{work-root}}/reference/src/oracle/request_builder` を正本に保ったまま既存の
`acp.builder.*` 参照を成立させるために残す。削除条件は realization 側と
利用者向け公開面から `acp.builder.*` 参照がなくなること。
"""

import sys as _sys

from oracle.request_builder import basic

__all__ = ["basic"]

# `basic` だけは local adapter を持たず、正本 module と同一の型を公開する。
_sys.modules[f"{__name__}.basic"] = basic
