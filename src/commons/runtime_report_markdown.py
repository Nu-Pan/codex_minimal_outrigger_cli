"""primary report の読み順と、確定済み情報の Markdown 表示を共有する。"""

import json
import re
from dataclasses import dataclass

from .runtime_errors import safe_text
from .runtime_primary_report_specs import TerminalClassification

# 実行情報の各値で同じ設定を使い、encoder の再生成を省く。
_METADATA_JSON_ENCODER = json.JSONEncoder(ensure_ascii=False, sort_keys=True)


@dataclass(frozen=True)
class ReportSummary:
    """掲載時点で分かっている結果、確認範囲、注意事項、次操作。"""

    outcome: str
    scope: tuple[str, ...] = ()
    attention: tuple[str, ...] = ()
    next_actions: tuple[str, ...] = ()


_PURPOSES = {
    "doctor": "実行環境・設定・管理領域・検索用コンポーネントを検査・修復する",
    "session fork": "作業用 session branch と session state を作成する",
    "session join": "session の変更を home branch へ取り込む",
    "session abandon": "session を終了し、対象 branch を破棄する",
    "oracle edit": "確定したユーザー指示に従い、2 回の agent call で oracle を編集する",
    "realization apply": "指定 commit 範囲の oracle 変更を realization へ反映する",
    "realization refactor": "realization の調査・改善を巡回し、確定済み成果を保存する",
    "run join": "確定済みの run 成果を session へ取り込む",
    "run abandon": "run の process を停止し、worktree と branch を破棄する",
    "feedback report": "feedback を再確認・修正し、判定と根拠を generation にまとめる",
    "feedback close": "人間が外部解決を確認した案件を理由とともに終了する",
}


def terminal_outcome(classification: TerminalClassification) -> str:
    """確定した invocation の終端分類を人間向けに表示する。"""
    # 問題の有無とは分け、実行自体の成否だけを示す。
    return {
        "natural_completion": "完了。この invocation は自然完了しました。",
        "user_interruption": "中断完了。この invocation はユーザー中断要求により完了しました。",
        "error": "失敗。この invocation はエラー終了しました。",
    }[classification]


def render_report_document(
    title: str,
    fields: dict[str, object],
    summary: ReportSummary,
    details: str,
    *,
    original_input: str | None = None,
    execution_record: str = "",
) -> str:
    """原文を変えず、要約・入力・詳細・末尾の実行情報を順に配置する。"""
    # command の argv に長い理由が含まれても、冒頭ではコマンド名だけを示す。
    invocation = str(fields.get("command", ""))
    command = next(
        (
            name
            for name in _PURPOSES
            if invocation == f"cmoc {name}" or invocation.startswith(f"cmoc {name} ")
        ),
        invocation.removeprefix("cmoc "),
    )
    purpose = _PURPOSES.get(command, "確定した操作を実行する")
    target = _report_target(command, fields)
    accepts_input = command in {"oracle edit", "feedback close"}
    identity = [
        f"# {title}",
        f"- コマンド: `cmoc {command}`",
        f"- 実行目的: {purpose}",
        f"- 対象: {_brief(target)}",
    ]
    if accepts_input:
        identity.append(
            "- 入力の抜粋: "
            + (
                _brief(original_input, 160)
                if original_input is not None
                else "入力未確定"
            )
        )
    intro = markdown_sections(
        [
            *identity,
            "## 実行結果",
            summary.outcome,
            *(f"- {_brief(item)}" for item in summary.scope),
            "## 要注意事項",
            *(f"- {_brief(item)}" for item in summary.attention),
            *(
                []
                if summary.attention
                else [
                    "- この実行で報告された warning・エラーはありません。未実行の検査は確認範囲に含みません。"
                ]
            ),
            "## 次の操作",
            *(
                [f"- {_brief(item)}" for item in summary.next_actions]
                or ["- 必要な追加操作はありません。"]
            ),
        ]
    )
    if accepts_input:
        instruction = (
            fenced_text(original_input)
            if original_input is not None
            else "入力未確定。確定済みの指示本文はありません。"
        )
    else:
        instruction = fenced_text(f"操作目的: {purpose}\n対象: {target}")
    metadata = "\n".join(
        f"{key}: {yaml_scalar(value)}" for key, value in fields.items()
    )
    return (
        "\n\n".join(
            [
                intro.rstrip("\n"),
                "## 元の指示",
                instruction,
                "## 詳細結果",
                details.rstrip("\n"),
                *([execution_record.rstrip("\n")] if execution_record else []),
                "## 実行情報",
                fenced_text(metadata, "yaml"),
            ]
        )
        + "\n"
    )


def markdown_sections(lines: list[str]) -> str:
    """生成した見出しを空行で区切り、引用のコードブロックには触れない。"""
    # 原文を含む複数行の要素は分割・整形しない。
    rendered: list[str] = []
    fence: str | None = None
    for line in lines:
        if fence is None and re.fullmatch(r"#{1,6} [^\r\n]+", line):
            if rendered and rendered[-1] != "":
                rendered.append("")
            rendered.extend([line, ""])
        else:
            rendered.append(line)
        if "\n" not in line and "\r" not in line:
            if fence is not None:
                if line == fence:
                    fence = None
            else:
                match = re.fullmatch(r"(`{3,}|~{3,})[\w-]*", line)
                if match:
                    fence = match[1]
    return "\n".join(rendered).strip("\n") + "\n"


def fenced_text(value: str, language: str = "text") -> str:
    """本文の backtick より長い区切りで原文をそのまま掲載する。"""
    # 区切りの改行を report 側へ加え、value の改行や見出しは変更しない。
    fence = "`" * max(
        3, 1 + max((len(run) for run in re.findall(r"`+", value)), default=0)
    )
    return f"{fence}{language}\n{value}\n{fence}"


def inline_code(value: str) -> str:
    """一行の文字列を、本文の記号を変えずに code span として示す。"""
    # 本文中の backtick と衝突しない区切りを使い、境界の空白も保持する。
    if not value:
        return ""
    delimiter = "`" * max(
        1, 1 + max((len(run) for run in re.findall(r"`+", value)), default=0)
    )
    padding = (
        " "
        if value.startswith("`")
        or value.endswith("`")
        or (value.startswith(" ") and value.endswith(" ") and value.strip(" "))
        else ""
    )
    return f"{delimiter}{padding}{value}{padding}{delimiter}"


def yaml_scalar(value: object) -> str:
    """report の実行情報を YAML の値として安全に表示する。"""
    # JSON の表記を使い、改行を含む値も metadata の構造から分離する。
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, (list, dict)):
        return _METADATA_JSON_ENCODER.encode(_safe_json_value(value))
    return _METADATA_JSON_ENCODER.encode(safe_text(value))


def _report_target(command: str, fields: dict[str, object]) -> str:
    # 未取得の値を既定値で埋めず、操作ごとに確定した対象を示す。
    def value(key: str) -> str:
        item = fields.get(key)
        return str(item) if item is not None else "未確定"

    if command == "doctor":
        return f"work-root: {value('work_root')}"
    if command == "oracle edit":
        return f"repo-root: {value('repo_root')} / session branch: {value('session_branch')}"
    if command == "realization apply":
        return f"commit 範囲: {value('diff_base_commit')} → {value('run_fork_commit')}"
    if command == "feedback close":
        return f"案件 ID: {value('case_id')}"
    if command == "feedback report":
        return f"report cut: {value('report_cut_id')} / 入力境界: {value('final_high_watermark')}"
    if command.startswith("session "):
        return f"session branch: {value('session_branch')} / home branch: {value('home_branch')}"
    return f"run branch: {value('run_branch')} / worktree: {value('run_worktree')}"


def _brief(value: str, limit: int = 240) -> str:
    # 抜粋だけを一行に整え、長い入力でも結果要約を押し下げない。
    text = " ".join(safe_text(value).split())
    if len(text) > limit:
        text = text[:limit] + "…（全文は後続の詳細を参照）"
    return inline_code(text)


def _safe_json_value(value: object) -> object:
    # UTF-8 として保存できない surrogate は metadata 上の可視表現にする。
    if isinstance(value, str):
        return safe_text(value)
    if isinstance(value, list):
        return [_safe_json_value(item) for item in value]
    if isinstance(value, dict):
        return {safe_text(key): _safe_json_value(item) for key, item in value.items()}
    return value
