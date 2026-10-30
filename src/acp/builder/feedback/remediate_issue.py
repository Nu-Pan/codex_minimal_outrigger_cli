"""feedback issue remediation builder の互換 import 経路。

対応する oracle file:
`{{work-root}}/reference/src/oracle/acp_builder/feedback/report/remediate_issue.py`。
"""

from oracle.acp_builder.feedback.report.remediate_issue import (
    build_feedback_issue_remediation_request,
)

__all__ = ["build_feedback_issue_remediation_request"]
