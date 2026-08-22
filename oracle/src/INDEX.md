# `oracle`

## Summary
- oracle の実装定義を構成する最上位領域。AI コーディングエージェント呼び出しの論理パラメータと用途別起動定義、cmoc の設定・パス・構造化文書モデル、agent 向け完全 prompt と各種 policy を扱う。具体的な呼び出し用途は `acp_builder`、共通モデルや設定は `other`、prompt の構築規則は `prompt_builder` へ進む。

## Read this when
- AI コーディングエージェント呼び出しのパラメータ契約や用途別の起動定義を調べるとき
- cmoc の設定モデル、root path 解決、構造化文書の表現・Markdown レンダリングを調べるとき
- agent 向け完全 prompt の構成、placeholder 統合、oracle・realization・feedback・routing などの policy を調べるとき

## Do not read this when
- 実際の Codex CLI 呼び出し、サブコマンド解析、TUI の実行処理など、agent call の定義を利用する側の実装だけを調べるとき
- oracle や realization の正本仕様、または個別機能の保存・適用処理だけを確認したいとき
- この領域で定義された共通モデルや prompt 構築規則ではなく、個別の下位機能の具体的な挙動だけを確認したいとき

## hash
- de39aa07f0a35bd1a39098f2bad239681ed7619326a33a81d1c578acd73e874e
