# `apply`

## Summary
- 対象は、oracle file の差分を realization file へ反映する `cmoc realization apply fork` 用の AgentCallParameter 構築定義です。差分追従の起動設定や作業範囲を確認・変更する際の入口になります。

## Read this when
- `cmoc realization apply fork` の prompt 内容、完了条件、AgentCallParameter の起動設定を確認・変更するとき。
- oracle file の変更を realization 全体へ反映する agent call の作業範囲、権限、実行コンテキストを調査するとき。

## Do not read this when
- realization の具体的な実装・テスト・補助ファイルを確認または変更するときは、生成 prompt の定義ではなく対象の realization file を直接読む。
- 一般的な prompt 構築や、他の realization 起動経路を調査するときは、それぞれの builder 定義を直接読む。

## hash
- 7ba48007845e06850bffb709d75714e4f4eefc6e20056ad910fdf13cb4a5687e

# `refactor`

## Summary
- refactor 作業用 fork の変更差分要約と、ファイル単位レビュー・修正を行う AgentCallParameter の構築実装および Structured Output schema を扱うディレクトリ。refactor fork に関する出力契約、プロンプト条件、起動設定を確認する入口であり、具体的な定義は fork 配下から参照する。

## Read this when
- refactor fork の変更差分要約 agent call の出力契約、プロンプト、起動パラメータを確認・変更するとき
- refactor fork のファイル単位レビュー・修正 agent call の作業条件、検証条件、出力契約を確認・変更するとき
- 変更要約またはレビュー・修正に関する JSON schema と Python 実装の対応を調査するとき

## Do not read this when
- 変更差分の取得や要約生成そのものの処理を調査するときは、対応する実装へ直接進む
- レビュー対象の実装内容や個別仕様を調査・修正するときは、対象の realization file と必要な oracle file を直接読む
- Structured Output の具体的な項目や形式だけを確認するときは、対応する JSON schema ファイルを直接読む
- refactor fork 以外の AgentCallParameter 構築定義を調査するときは、該当する別ディレクトリへ進む

## hash
- 4bcf45d4b171f64ba2402a5ee33483c246ae96280cda74cbce774b1f6f704362
