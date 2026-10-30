"""realization refactor の file review 正本 builder を再公開する adapter。

対応する oracle file:
`{{work-root}}/reference/src/oracle/request_builder/realization/refactor/file_review_and_fix.py`
`{{work-root}}/reference/src/oracle/request_builder/realization/refactor/file_review_and_fix.json`。
"""

from oracle.request_builder.realization.refactor.file_review_and_fix import (
    build_realization_refactor_request,
)

__all__ = ["build_realization_refactor_request"]
