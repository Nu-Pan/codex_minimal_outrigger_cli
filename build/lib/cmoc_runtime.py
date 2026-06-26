import sys

from commons import cmoc_runtime as _implementation

# Keep this compatibility import path while pyproject exposes cmoc_runtime and
# in-tree callers still import it directly. Remove it after all supported
# callers use commons.cmoc_runtime or the responsibility-specific runtime modules.
sys.modules[__name__] = _implementation
