"""feedback issue verification builder の互換 import 経路。

対応する oracle file:
`{{work-root}}/oracle/src/oracle/acp_builder/feedback/verify_issue.py`。
"""

from oracle.acp_builder.feedback.verify_issue import (
    build_feedback_verify_issue_parameter,
)

__all__ = ["build_feedback_verify_issue_parameter"]
