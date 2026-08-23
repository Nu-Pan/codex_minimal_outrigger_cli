# `apply`

## Summary
- `realization apply fork` の Agent call 起動定義を扱うディレクトリ。commit 範囲、oracle file の raw git diff、linked worktree を prompt と `AgentCallParameter` に組み立て、oracle file の変更をリポジトリ全体の realization file へ反映する追従処理の入口となる。

## Read this when
- `realization apply fork` の Agent call に渡す追従対象変更、prompt、ファイルアクセス権限、作業ディレクトリ、モデル・推論強度、indexing preflight の設定を確認・変更するとき。
- oracle file の差分を起点とする realization file 追従の作業方針、完了条件、oracle・realization・routing policy の適用範囲を確認するとき。

## Do not read this when
- `realization apply fork` 以外の apply 経路の起動定義を調べるときは、該当する apply 配下の対象を直接読む。
- 共通 prompt 生成や構造化ドキュメントの仕様を調べるときは、`build_complete_prompt` や `struct_doc` の定義を直接読む。
- 個別の realization implementation・test・ancillary の挙動、または oracle file の変更内容や repository 共通の開発ルールを確認するときは、それぞれの対象を直接読む。

## hash
- e4fc67f0d3814acd19413b7469a487bff46e4948094247c1f88f13788c413ab0

# `refactor`

## Summary
- refactor fork の agent call 定義をまとめるディレクトリ。確定済み refactor 差分の意味論的な変更要約と、ファイル単位の実装レビュー・修正に必要な prompt、アクセス方針、検証条件、起動パラメータの構築入口を提供する。
- 配下には、変更要約用とファイルレビュー・修正用の処理定義、および各処理の Structured Output schema がある。実装対象の内容や実際の差分を調べる場合は別の対象へ進み、出力形式だけを確認する場合は該当 schema を直接読む。

## Read this when
- refactor fork の差分要約 agent call の責務や起動条件を確認するとき
- ファイル単位のレビュー・修正 agent call の調査範囲、修正方針、検証条件、アクセス方針を確認するとき
- 差分要約またはレビュー・修正処理の Structured Output schema への入口を探すとき

## Do not read this when
- 実際の refactor 差分や生成済み要約を確認したいとき
- レビュー対象の実装、個別仕様、またはレビュー・修正処理の詳細実装を調査したいとき
- Structured Output の具体的な項目・型・形式だけを確認したいときは、対応する schema file を直接読む

## hash
- fc309b7eea922df762f382c73321dac0afe30271d63434736674b028a0912a88
