"""feedback issue 同一性判断 builder の互換 import 経路。

対応する oracle file:
`{{work-root}}/reference/src/oracle/acp_builder/feedback/report/normalize_issue.py`。
"""

from oracle.acp_builder.feedback.report.normalize_issue import (
    build_feedback_issue_normalization_request,
)

__all__ = ["build_feedback_issue_normalization_request"]
