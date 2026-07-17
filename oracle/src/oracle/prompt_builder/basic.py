# std
from pathlib import Path

# プレースホルダと実際の値の対応関係を表す
#
# key: str
#   プレースホルダの名前
#   例えば `{{repo-root}}` なら key="repo-root"
#
# value: str
#   プレースホルダの置換先文字列
#   例えば `{{repo-root}}` --> `/home/happy/codex_minimal_outrigger_cli_stage1` なら、
#   value="/home/happy/codex_minimal_outrigger_cli_stage1"
type PlaceholderMap = dict[str, str | Path]
