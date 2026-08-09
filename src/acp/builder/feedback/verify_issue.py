"""feedback issue verification の正本 builder を再公開する adapter。

対応する oracle file:
`{{work-root}}/oracle/src/oracle/acp_builder/feedback/verify_issue.py`。
"""

from oracle.acp_builder.feedback.verify_issue import (
    build_feedback_verify_issue_parameter,
)

__all__ = ["build_feedback_verify_issue_parameter"]
