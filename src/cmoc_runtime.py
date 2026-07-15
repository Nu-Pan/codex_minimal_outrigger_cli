# pyproject が cmoc_runtime を公開し、tree 内の呼び出し元も直接 import している間は、
# この互換 import path を残す。対応対象が commons.cmoc_runtime か責務別 runtime module へ
# 移行したら削除する。
# `commons.cmoc_runtime.__all__` で公開面を限定した star import により、runtime と
# 型チェッカーの双方へ同じ互換公開名を伝える。
from commons.cmoc_runtime import *  # noqa: F403
from commons.cmoc_runtime import __all__ as __all__
