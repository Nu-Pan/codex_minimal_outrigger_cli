"""`{{work-root}}/oracle/src/oracle/other/path_model.py` の公開 path model を再公開する。

正本実装を realization 側へ複製せず既存の `basic.path_model` 参照を保つために残す。
削除条件は realization 側と利用者向け公開面から `basic.path_model` 参照がなくなること。
"""

from oracle.other.path_model import (
    RootPathPlaceHolder,
    resolve_ph_path,
    resolve_real_path,
)

__all__ = [
    "RootPathPlaceHolder",
    "resolve_ph_path",
    "resolve_real_path",
]
