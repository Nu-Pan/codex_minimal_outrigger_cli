"""editing run report writer の旧 import path を保つ薄い shim。"""

# canonical 実装は共通処理の配置規則に従い commons に置く。
# {{work-root}}/oracle/doc/dev_rule/design_rule.md
# 旧 import path を利用する利用者が commons 側へ移行し、互換性が不要になった時に
# この shim と対応する INDEX entry を削除する。
# {{work-root}}/oracle/src/oracle/prompt_builder/parts/realization_standard.py
from commons.runtime_run_report import write_fork_report, write_lifecycle_report

__all__ = ["write_fork_report", "write_lifecycle_report"]
