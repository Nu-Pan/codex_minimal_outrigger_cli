"""editing run report writer の旧 import path を保つ薄い shim。"""

# canonical 実装は共通処理の配置規則に従い commons に置く。
# {{work-root}}/oracle/doc/dev_rule/design_rule.md
from commons.runtime_run_report import write_fork_report, write_lifecycle_report

__all__ = ["write_fork_report", "write_lifecycle_report"]
