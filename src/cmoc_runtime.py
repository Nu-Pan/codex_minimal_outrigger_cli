import sys

from commons import cmoc_runtime as _implementation

sys.modules[__name__] = _implementation
