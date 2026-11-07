"""decision の形式検証 MCP tool の公開定義。

検証処理と stdio server は、この定義を直接利用する realization として実装する。
cmoc の事前検証と MCP からの再検証では、同じ検証処理を使用する。
"""

VALIDATION_MCP_SERVER = "cmoc_decision_validation"
VALIDATION_TOOL_NAME = "validate"

VALIDATION_TOOL_DESCRIPTION = (
    "この call の work-root 内にある decision file 全体を、保存済みの最新内容で検証する。"
    "ファイルは変更せず、検証対象を絞り込む引数も受け付けない。"
    "\n検査規則:"
    "\n- GitHub Flavored Markdown の見出しと本文を検査する。"
    r"見出しの先頭には正規表現 `\[DEC-\d{6}\]` に一致する ID が必要で、decision 全体で一意とする。"
    "\n- 本文中の `[DEC-XXXXXX]` 形式の参照は、実在する見出しの ID に一意に解決できること。"
    "XXXXXX は6桁の数字を表す。"
    "\n- コードブロック・inline code 内の記述例は検査対象外。ID の欠番は許容する。"
    "\n- decision file が存在しない場合や、空のファイルだけの場合は問題なしとする。"
    "\n- 決定内容の意味の妥当性、SPC 参照、外部リンクは検査しない。"
)

VALIDATION_TOOL_ANNOTATIONS: dict[str, bool] = {
    "readOnlyHint": True,
    "destructiveHint": False,
    "idempotentHint": True,
    "openWorldHint": False,
}

VALIDATION_TOOL_INPUT_SCHEMA: dict[str, object] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "description": (
        "引数なし。work-root は call の起動時に固定され、検証対象は decision file 全体。"
        "不正な引数は JSON-RPC の入力エラー（code: -32602）となる。"
    ),
    "additionalProperties": False,
    "properties": {},
}

VALIDATION_TOOL_OUTPUT_SCHEMA: dict[str, object] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "description": (
        "MCP result の structuredContent。content の text にも同じ JSON を返す。"
        "全対象の検証が正常終了した場合と、検証を完了できなかった場合を区別する。"
    ),
    "oneOf": [
        {
            "type": "object",
            "description": (
                "全対象の検証が正常終了した結果。問題の有無にかかわらず isError は false。"
            ),
            "additionalProperties": False,
            "required": ["status", "problems"],
            "properties": {
                "status": {"type": "string", "const": "ok"},
                "problems": {
                    "type": "array",
                    "description": (
                        "検出した問題の全件。空配列だけが、機械的に検査した規則への違反がないことを表す。"
                        "決定内容の意味の妥当性を保証するものではない。"
                    ),
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["path", "line", "message"],
                        "properties": {
                            "path": {
                                "type": "string",
                                "minLength": 1,
                                "description": "問題がある decision file の work-root 相対の POSIX path。",
                            },
                            "line": {
                                "type": "integer",
                                "minimum": 1,
                                "description": "問題箇所の1始まりの行番号。",
                            },
                            "message": {
                                "type": "string",
                                "pattern": r"\S",
                                "description": "違反した規則と、修正箇所を判断するための説明。",
                            },
                        },
                    },
                },
            },
        },
        {
            "type": "object",
            "description": (
                "列挙・読み取り等に失敗し、検証を完了できなかった結果。isError は true。"
                "部分的な検証結果を問題なしとして返さず、problems も併記しない。"
            ),
            "additionalProperties": False,
            "required": ["status", "message"],
            "properties": {
                "status": {"type": "string", "const": "error"},
                "message": {
                    "type": "string",
                    "pattern": r"\S",
                    "description": "検証を完了できなかった理由。",
                },
            },
        },
    ],
}
