# CLI 自動補完規則

- `_CMOC_COMPLETE` が設定された呼び出しは、ユーザーによる通常の `cmoc` 実行ではなく、Click/Typer の自動補完用プローブとして扱う。
- この場合、cmoc 独自の事前検査（サブコマンド未指定判定、`<repo-root>` 探索、状態検査など）とエラーレポート出力は行わず、Click/Typer の補完処理へそのまま委譲する。
- 補完モードの stdout/stderr には、Click/Typer が必要とする補完用出力以外を混ぜてはならない。
