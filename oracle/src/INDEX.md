# `oracle`

## Summary
- cmoc の agent call に関する正本実装をまとめるディレクトリ。用途別の AgentCallParameter、プロンプト構築、設定・パスモデル、feedback 入力契約を下位要素への入口として提供する。
- agent call の起動設定や Structured Output 契約は `acp_builder`、プロンプト統合と policy 生成は `prompt_builder`、設定・パス・構造化文書モデルは `other`、feedback reporter の入力契約は `feedback` を読む。

## Read this when
- cmoc の agent call 起動パラメータ、モデル・推論強度・ファイルアクセス・cwd・preflight・Structured Output を確認または変更するとき
- agent call に渡す完全プロンプト、placeholder、用途別 policy、oracle／realization／routing 規定の組み立てを確認または変更するとき
- cmoc の設定モデル、Codex provider 設定、root placeholder と worktree/repository root の解決、構造化文書モデルを確認または変更するとき
- feedback reporter が collector に渡す入力形式や検証契約を確認または変更するとき
- 上記の責務を担う下位ディレクトリのどれを読むべきか判断するとき

## Do not read this when
- 具体的な realization・oracle・TUI の実装やテストを確認したいときは、該当する下位対象を直接読む
- 個別の正本仕様や既存 INDEX.md の内容を確認したいときは、その対象を直接読む
- prompt_builder が生成した最終プロンプトの利用箇所だけを確認したいときは、呼び出し元または生成対象を読む
- collector 側の feedback 保存・集約・重複判定や、問題検出後の継続判断だけを確認したいとき
- 設定ファイルの実際の保存内容や、TUI の画面表示だけを確認したいとき

## hash
- 4a33eb865da3ecbafbb3bd06df9904058f82cc872eb6304663779d0aafac4b29
