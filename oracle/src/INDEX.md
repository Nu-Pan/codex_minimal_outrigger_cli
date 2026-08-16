# `oracle`

## Summary
- cmoc の agent call 構築、完全 prompt 生成、共通モデル、パス解決、構造化文書変換、feedback 入力契約を扱う定義群の入口です。
- agent call の共通パラメータや処理別設定を調査するときは `acp_builder` へ進み、prompt の統合や policy を確認するときは `prompt_builder` へ進みます。
- リポジトリ設定・root placeholder・構造化文書ヘルパーは `other`、feedback reporter の入力契約は `feedback` で確認します。

## Read this when
- cmoc の agent call 構築責務、処理別の prompt・アクセス制御・モデル設定の分割を確認するとき
- agent call 用の完全 prompt、共通 policy、Structured Document の組み立てや Markdown 変換を調査するとき
- agent call の cwd、work root、repository root、placeholder 解決規則を確認するとき
- feedback reporter が collector に渡す問題入力の契約を確認するとき

## Do not read this when
- agent call の実行制御、終了結果の処理、または個別 CLI サブコマンドの挙動だけを調査するとき
- 特定の処理の prompt 詳細、Structured Output schema、または policy 本文を直接確認したいとき
- 実際の設定値や人間による調整結果だけを確認したいとき

## hash
- d7747309899db4398390f59ebe789862e5970d8279a7db051fe68ffa6f831b60
