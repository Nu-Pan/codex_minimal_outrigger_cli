# `resolve_parameter.json`

## Summary
- `cmoc tui` の実行前に、オリジナルプロンプトに対して AI Agent CLI/TUI へ与えるファイルアクセスモードと標準文書注入フラグを決定する Structured Output schema。
- `file_access_mode` と各標準注入フラグを、選択値と理由の組で返す契約を定義する。

## Read this when
- `cmoc tui` のパラメータ解決 agent call が返す JSON の形を確認したいとき。
- TUI で選択可能な `FileAccessMode` の enum 値や、標準文書注入フラグの必須項目を変更・検証するとき。

## Do not read this when
- `cmoc tui` のエディタ起動、HTML コメント除去、Codex CLI/TUI 起動など、schema 以外の実行フローを確認したいとき。
- 完全プロンプトの共通構築やファイルアクセス規則そのものの文面を調べたいとき。

## hash
- manual

# `resolve_parameter.py`

## Summary
- `cmoc tui` の実行パラメータ解決用 AI 呼び出しパラメータを構築する実装。
- オリジナルプロンプト、利用可能なファイルアクセスモード一覧、oracle/realization/review/apply/indexing の標準文書を含む完全プロンプトを作り、効率重視モデル・中程度推論・読み取り専用権限・専用 schema を指定して返す。

## Read this when
- TUI のパラメータ解決 prompt、モデル種別、reasoning effort、file access mode、標準文書注入フラグを確認または変更したいとき。
- オリジナルプロンプトが解決用 prompt にどのように埋め込まれるか、利用可能なファイルアクセスモードがどう提示されるかを追うとき。

## Do not read this when
- 解決後のパラメータを使って最終プロンプトや Codex CLI/TUI 起動を行う上位フローを調べたいとき。
- 個々の標準文書本文や Structured Output schema の詳細だけを確認したいとき。

## hash
- manual
