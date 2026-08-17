"""fallback primary report の個別サブコマンド定義を保持する。

根拠:
- {{work-root}}/oracle/doc/app_spec/console_and_file_log.md
- {{work-root}}/oracle/doc/app_spec/sub_command/
"""

from dataclasses import dataclass
from typing import Literal

ReportTemplate = Literal["summary", "oracle_review", "feedback_invocation"]
TerminalClassification = Literal["natural_completion", "user_interruption", "error"]


@dataclass(frozen=True)
class PrimaryReportSpec:
    """fallback report の保存先、役割、および必須項目を表す。"""

    directory: str
    role: str
    title: str
    fields: tuple[str, ...] = ()
    template: ReportTemplate = "summary"


# 個別仕様が保存先と front matter を定める現行の非対話末端サブコマンドだけを
# 登録する。TUI の通知境界を使う tui と oracle investigation は含めない。
# {{work-root}}/oracle/doc/app_spec/windows_toast_notification.md
_PRIMARY_REPORT_SPECS: dict[str, PrimaryReportSpec] = {
    "doctor": PrimaryReportSpec(
        "doctor",
        "doctor execution report",
        "cmoc doctor report",
    ),
    "indexing": PrimaryReportSpec(
        "indexing",
        "indexing execution report",
        "cmoc indexing report",
        ("commit_id",),
    ),
    "session fork": PrimaryReportSpec(
        "session/fork",
        "session fork report",
        "cmoc session fork report",
        (
            "session_id",
            "home_branch",
            "session_branch",
            "session_fork_commit",
            "session_state_before",
            "session_state_after",
        ),
    ),
    "session join": PrimaryReportSpec(
        "session/join",
        "session join report",
        "cmoc session join report",
        (
            "session_branch",
            "home_branch",
            "session_branch_head_before_merge",
            "home_branch_head_before_merge",
            "merge_commit",
            "session_state_before",
            "session_state_after",
        ),
    ),
    "session abandon": PrimaryReportSpec(
        "session/abandon",
        "session abandon report",
        "cmoc session abandon report",
        (
            "session_branch",
            "home_branch",
            "abandoned_branch_start_commit",
            "session_state_before",
            "session_state_after",
        ),
    ),
    "oracle edit": PrimaryReportSpec(
        "oracle_edit",
        "oracle edit execution report",
        "cmoc oracle edit report",
        ("main_agent_call_status", "reduction_agent_call_status"),
    ),
    "oracle review": PrimaryReportSpec(
        "oracle_review",
        "oracle review report",
        "cmoc oracle review report",
        (
            "scope",
            "session_branch",
            "session_fork_commit",
            "run_branch",
            "run_fork_commit",
            "run_join_commit",
            "oracle_count_total",
            "oracle_count_evaluated",
            "fatal_findings_accepted_count",
            "minor_findings_accepted_count",
            "fatal_findings_rejected_count",
            "minor_findings_rejected_count",
            "result",
        ),
        "oracle_review",
    ),
    "realization apply fork": PrimaryReportSpec(
        "realization/apply/fork",
        "realization apply fork report",
        "cmoc realization apply fork report",
        (
            "run_kind",
            "session_branch",
            "session_fork_commit",
            "run_branch",
            "run_fork_commit",
            "run_worktree",
            "state_before",
            "state_after",
            "completion_reason",
            "diff_base_commit",
            "codex_returncode",
            "changed_paths",
            "feedback_observation_count",
            "feedback_observations",
        ),
    ),
    "realization refactor fork": PrimaryReportSpec(
        "realization/refactor/fork",
        "realization refactor fork report",
        "cmoc realization refactor fork report",
        (
            "run_kind",
            "session_branch",
            "session_fork_commit",
            "run_branch",
            "run_fork_commit",
            "run_worktree",
            "state_before",
            "state_after",
            "refactor_state_path",
            "completion_reason",
        ),
    ),
    "run join": PrimaryReportSpec(
        "run/join",
        "run join report",
        "cmoc run join report",
        (
            "run_kind",
            "session_branch",
            "run_branch",
            "run_fork_commit",
            "run_worktree",
            "state_before",
            "state_after",
            "run_join_commit",
        ),
    ),
    "run abandon": PrimaryReportSpec(
        "run/abandon",
        "run abandon report",
        "cmoc run abandon report",
        (
            "run_kind",
            "session_branch",
            "run_branch",
            "run_fork_commit",
            "run_worktree",
            "state_before",
            "state_after",
        ),
    ),
    "feedback report": PrimaryReportSpec(
        "feedback/invocation",
        "feedback invocation summary report",
        "cmoc feedback report invocation summary",
        (
            "session_branch",
            "report_cut_id",
            "report_cut_at",
            "normal_publication_status",
            "incomplete_diagnostic_status",
            "current_pointer_update_status",
        ),
        "feedback_invocation",
    ),
}


def primary_report_spec(command_name: str) -> PrimaryReportSpec | None:
    """command 名に対応する fallback report 定義を返す。"""
    return _PRIMARY_REPORT_SPECS.get(command_name)
