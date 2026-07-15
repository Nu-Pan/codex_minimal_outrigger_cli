import sys

from commons import cmoc_runtime as _implementation

# pyproject が cmoc_runtime を公開し、tree 内の呼び出し元も直接 import している間は、
# この互換 import path を残す。対応対象が commons.cmoc_runtime か責務別 runtime module へ
# 移行したら削除する。
sys.modules[__name__] = _implementation
