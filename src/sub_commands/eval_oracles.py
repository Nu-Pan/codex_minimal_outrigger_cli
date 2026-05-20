"""`eval-oracles.py` 実装を import しやすくする互換 module。"""

from importlib import util
from pathlib import Path
from types import ModuleType


def load_eval_oracles_module() -> ModuleType:
    """ハイフン付き本命実装ファイルを Python module として読み込む。"""
    # Python の通常 import で扱えないファイル名を importlib で読み込む。
    path = Path(__file__).with_name("eval-oracles.py")
    spec = util.spec_from_file_location("sub_commands.eval-oracles", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Failed to load {path}")
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_module = load_eval_oracles_module()
cmoc_eval_oracles_impl = _module.cmoc_eval_oracles_impl
_evaluation_prompt = _module._evaluation_prompt
