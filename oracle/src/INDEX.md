# `oracle`

## Summary
- 各種 cmoc フローで AI Agent 呼び出しに使用する正本ソースを配置するディレクトリ。共通呼び出しパラメータ、用途別の prompt・起動設定、Structured Output schema を扱い、feedback や prompt_builder など下位領域への入口となる。

## Read this when
- cmoc の Agent call に使う prompt、モデル・推論設定、アクセス権限、作業ディレクトリ、実行前設定を調査・変更するとき。
- Agent call の出力契約や用途別 Structured Output schema を確認するとき。
- feedback、prompt_builder など、用途別の呼び出し設定や共通定義の入口を探すとき。

## Do not read this when
- 通常の realization 実装・テストや CLI／TUI の実行フローそのものを調査するとき。
- 正本仕様、Codex CLI の sandbox・permission profile、共通 prompt 構築の詳細だけを調査するとき。
- 特定用途の prompt や schema の詳細を調査するときは、該当する下位ディレクトリを直接読むとき。

## hash
- b9294ed9b837fb118eb54d01107244d5979dbf0ecfca12bd4880da16a36c44a2
