# `fork`

## Summary
- refactor fork における変更要約とファイル単位レビュー・修正の agent call 定義、およびそれぞれの Structured Output schema を扱うディレクトリ。変更差分の要約形式・起動パラメータ・レビュー修正処理の呼び出し条件を確認する入口である。

## Read this when
- refactor fork の変更差分要約 agent call の出力契約や起動パラメータを確認するとき
- ファイル単位のレビュー・修正処理における AgentCallParameter、作業条件、検証結果の構造を確認するとき
- 対応する JSON schema と prompt 構築実装の関係を調査するとき

## Do not read this when
- 変更差分の要約ロジックやレビュー・修正の具体的な実装を調べる場合は、各担当の Python 実装を直接読むとき
- 出力項目や型だけを確認したい場合は、対応する JSON schema を直接読むとき
- レビュー対象の実装内容や正本仕様そのものを調査する場合は、対象の realization または oracle file を直接読むとき

## hash
- a1d7eecc8707ca19af34e0af4b45c96c492fb2af2b97a40d30606c804f3569da
