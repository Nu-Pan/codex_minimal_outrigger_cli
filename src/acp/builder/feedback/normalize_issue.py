"""feedback issue 同一性判断の正本 builder を再公開する adapter。

対応する oracle file:
`{{work-root}}/oracle/src/oracle/acp_builder/feedback/normalize_issue.py`。
"""

from oracle.acp_builder.feedback.normalize_issue import (
    build_feedback_normalize_issue_parameter,
)

__all__ = ["build_feedback_normalize_issue_parameter"]
