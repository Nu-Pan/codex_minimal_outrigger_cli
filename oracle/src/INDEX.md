# `oracle`

## Summary
- AI コーディングエージェント呼び出し用の AgentCallParameter 定義を集約する領域。共通パラメータ契約に加え、indexing、feedback、realization、session、tui、oracle 向けの prompt、アクセス制御、モデル・推論設定、Structured Output、作業ディレクトリなどを扱う。処理別の設定を調査・変更する際は、共通定義または対応する下位要素へ進む入口となる。

## Read this when
- 特定の cmoc 処理が構築する agent call パラメータや完全 prompt を調査・変更するとき
- モデル・推論設定、ファイルアクセス制御、Structured Output、cwd、indexing preflight の設定箇所を特定するとき
- oracle、realization、feedback など処理別の agent call builder における設定責務の分割を確認するとき

## Do not read this when
- agent call の実行制御や終了結果の処理を調査するときは、呼び出し側または実行処理を直接読む
- モデル名や Codex CLI sandbox の具体的な解決仕様を確認するときは、realization 実装または指定された oracle 文書を読む
- 個別の Structured Output schema、prompt の詳細、または対象処理の通常フローだけを調査するときは、対応する下位要素を直接読む

## hash
- 662a907794675947058c6985786eeb9373a340a0387f33201a84b1b11af35041
