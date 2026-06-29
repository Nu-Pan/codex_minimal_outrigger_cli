"""`<work-root>/oracle/src/oracle/other/path_model.py` の path model を再公開する。

正本実装を realization 側へ複製せず既存の `basic.path_model` 参照を保つために残す。
削除条件は realization 側と利用者向け公開面から `basic.path_model` 参照がなくなること。
"""

from oracle.other.path_model import (
    RootPathPlaceHolder,
    resolve_cmoc_root,
    resolve_ph_path,
    resolve_real_path,
    resolve_repo_root,
    resolve_run_root,
    resolve_work_root,
)

__all__ = [
    "RootPathPlaceHolder",
    "resolve_cmoc_root",
    "resolve_ph_path",
    "resolve_real_path",
    "resolve_repo_root",
    "resolve_run_root",
    "resolve_work_root",
]
