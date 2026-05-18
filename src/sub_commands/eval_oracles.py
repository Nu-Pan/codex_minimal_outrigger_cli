"""`cmoc eval-oracles` 本体の import 互換ラッパー。"""

import importlib.util
import sys
from pathlib import Path

_BODY_PATH = Path(__file__).with_name("eval-oracles.py")
_BODY_MODULE_NAME = "sub_commands._eval_oracles_body"
_BODY_SPEC = importlib.util.spec_from_file_location(
    _BODY_MODULE_NAME,
    _BODY_PATH,
)
if _BODY_SPEC is None or _BODY_SPEC.loader is None:
    raise ImportError(f"Failed to load eval-oracles body: {_BODY_PATH}")
_BODY_MODULE = importlib.util.module_from_spec(_BODY_SPEC)
sys.modules[_BODY_MODULE_NAME] = _BODY_MODULE
_BODY_SPEC.loader.exec_module(_BODY_MODULE)

run_codex_exec = _BODY_MODULE.run_codex_exec
maintain_indexes = _BODY_MODULE.maintain_indexes


def cmoc_eval_oracles_impl(
    repo_root: Path | None = None,
    *,
    full: bool,
) -> None:
    """hyphen 名ファイル上の本体処理を呼び出す。"""
    # 既存テストや利用側の monkeypatch を本体 module へ同期する。
    _BODY_MODULE.run_codex_exec = run_codex_exec
    _BODY_MODULE.maintain_indexes = maintain_indexes
    _BODY_MODULE.cmoc_eval_oracles_impl(repo_root, full=full)
