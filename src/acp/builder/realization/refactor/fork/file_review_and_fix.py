"""realization refactor の file review 正本 builder を再公開する adapter。

対応する oracle file:
`{{work-root}}/referenece/src/oracle/acp_builder/realization/refactor/fork/file_review_and_fix.py`
`{{work-root}}/referenece/src/oracle/acp_builder/realization/refactor/fork/file_review_and_fix.json`。
"""

from oracle.acp_builder.realization.refactor.fork.file_review_and_fix import (
    build_realization_refactor_request,
)

__all__ = ["build_realization_refactor_request"]
