# `apply`

## Summary
- `cmoc realization apply fork` における差分追従 agent call の起動パラメータ構築を扱う。
- commit 範囲、oracle file の raw git diff、prompt、ファイルアクセスモード、作業ディレクトリ、モデル・推論設定、indexing preflight を定義する `fork` への入口である。

## Read this when
- `cmoc realization apply fork` の差分追従 agent call の起動条件や prompt を確認・変更するとき
- oracle file の変更をリポジトリ全体の realization file へ反映する agent call の完了条件を確認するとき

## Do not read this when
- 差分追従 agent call が実施する realization 実装、テスト、補助成果物の内容を調査するとき
- `cmoc realization apply fork` 以外の agent call 構築や、通常の realization 実装を確認するとき

## hash
- 1a96bca774699248cc2a8049204c34fcf0d018c3868609be69dc6ac59a1ea74d

# `refactor`

## Summary
- refactor fork における変更差分の要約 agent call と、ファイル単位のレビュー・修正 agent call を定義するディレクトリ。変更要約では差分入力から分類済み要約を生成し、レビュー・修正では対象ファイルを起点に調査・修正・検証を行う。各 agent call の prompt 構築、起動パラメータ、Structured Output schema が下位ファイルに分かれているため、それらの契約や関係を確認する入口となる。

## Read this when
- refactor fork の変更差分要約 agent call の責務、入力となる差分、読み取り専用の実行条件を確認するとき
- ファイル単位のレビュー・修正 agent call の対象範囲、oracle・realization の参照方針、修正と検証の条件を確認するとき
- 変更要約またはレビュー・修正の prompt 構築実装と、それに対応する Structured Output schema の関係を調査するとき

## Do not read this when
- 変更差分の要約処理やレビュー・修正処理の具体的な実装を調べる場合は、対応する Python 実装を直接読むとき
- Structured Output の項目、型、必須条件だけを確認したい場合は、対応する JSON schema を直接読むとき
- レビュー対象の実装や oracle の正本仕様を調査する場合は、対象の realization file または oracle file を直接読むとき

## hash
- dfb34395a4d45dc1287949930f93f7db01129cf6fd5b5b1aa9337b5281aef83e
