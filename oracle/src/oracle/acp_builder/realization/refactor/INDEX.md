# `fork`

## Summary
- refactor fork の変更差分要約に関する構造化出力スキーマ、差分要約用 AgentCallParameter の構築実装、ファイル単位レビュー・修正結果のスキーマ、およびレビュー・修正用 AgentCallParameter の構築定義を扱うディレクトリ。各ファイルの役割と参照条件を確認する入口となる。

## Read this when
- refactor fork の変更差分要約 agent call の出力契約や起動パラメータを確認・変更するとき
- ファイル単位のレビュー・修正 agent call の構築定義、作業条件、検証条件を確認・変更するとき
- 差分要約またはレビュー・修正に関する JSON schema と Python 実装の対応を調査するとき

## Do not read this when
- 変更要約の生成ロジック自体を調査するときは、差分取得・生成を担う実装へ直接進む
- レビュー対象の実装内容や個別仕様を調査・修正するときは、対象の realization file と必要な oracle file を直接読む
- Structured Output の具体的な項目や形式だけを確認するときは、対応する JSON schema ファイルを直接読む
- refactor fork 以外の AgentCallParameter 構築定義を調査するときは、該当する別ディレクトリへ進む

## hash
- 6ffb49fc8021beb7dcba645d2627a9f54aa8177f81bd5ad5ef5d4d451a16f34d
