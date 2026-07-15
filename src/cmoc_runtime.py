import sys
from typing import TYPE_CHECKING

# pyproject が cmoc_runtime を公開し、tree 内の呼び出し元も直接 import している間は、
# この互換 import path を残す。対応対象が commons.cmoc_runtime か責務別 runtime module へ
# 移行したら削除する。
if TYPE_CHECKING:
    # runtime の module alias を静的解析へ表現する唯一の star import。
    # 公開名は commons.cmoc_runtime.__all__ で明示的に固定している。
    from commons.cmoc_runtime import *  # noqa: F403
else:
    from commons import cmoc_runtime as _implementation

    sys.modules[__name__] = _implementation
