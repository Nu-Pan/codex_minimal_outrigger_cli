# `apply`

## Summary
- `cmoc realization apply fork` 用の AgentCallParameter を構築する定義で、追従対象の commit 範囲や oracle file の raw git diff を prompt に組み込み、run worktree を起動コンテキストとして設定する。差分追従 Agent のモデル、権限、調査・検証・routing 方針などの起動条件を扱う。

## Read this when
- realization apply fork の Agent 起動パラメータ、prompt 構築、commit 差分の埋め込み、run worktree 設定を確認・変更するとき。
- oracle file の変更を realization file 全体へ追従させる Agent call のモデル設定、権限設定、実行前 indexing 設定を確認するとき。

## Do not read this when
- 通常の realization implementation、test、ancillary の具体的な実装内容を確認する場合。
- Agent call の共通パラメータ型や prompt の共通生成規則を確認する場合。これらは各定義元を直接読む。

## hash
- 5c1ddc42291f0e1accc1b99ce0370d596a38dc64ab6747635e214e8ff3596e72

# `refactor`

## Summary
- refactor fork における agent call の出力契約と起動パラメータ構築を扱うディレクトリ。変更差分要約とファイル単位のレビュー・修正について、prompt、実行コンテキスト、アクセスモード、モデル、Structured Output schema、調査・修正・検証要件を確認する入口となる。

## Read this when
- refactor fork の変更差分要約 agent call の出力形式、prompt、実行コンテキスト、アクセスモード、モデル設定、Structured Output schema を確認・変更するとき
- refactor fork のファイル単位レビュー・修正 agent call の出力契約、調査範囲、修正権限、検証要件、prompt、AgentCallParameter の構築方法を確認・変更するとき

## Do not read this when
- 変更差分の取得・要約生成ロジック自体を調べるとき
- レビュー対象の実装、個別仕様、所見判定、レビュー・修正 agent の実行処理を調べるとき
- 構造化出力の項目・型・形式だけを確認するとき
- 一般的な prompt builder、path model、struct document の仕様を確認するとき

## hash
- bee16cc11ecff3d4fd783dbd56a8b2ec2404522d1eecda259e494ac131ef3838
