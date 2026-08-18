# `apply`

## Summary
- `cmoc realization apply fork` の差分追従 Agent Call 構築群への入口。fork 配下で、oracle file の変更差分をリポジトリ全体の realization file へ反映するための prompt、起動設定、参照・routing 方針を扱う。具体的な起動パラメータ実装は `fork/launch_exec.py` から確認する。

## Read this when
- `cmoc realization apply fork` の差分追従処理における prompt、commit 範囲や oracle diff の渡し方、Agent Call のモデル・推論・ファイルアクセス設定を確認または変更するとき。
- 差分追従の完了条件、oracle/realization の参照方針、リポジトリ全体を対象とする routing 設定の入口を探すとき。

## Do not read this when
- 具体的な prompt 構築や AgentCallParameter の実装を確認するときは、`fork/launch_exec.py` を直接読む。
- realization の個別実装・テスト・補助ファイル、または共通の prompt・AgentCall・パス・構造化文書の仕様を確認するときは、それぞれの対象を直接読む。

## hash
- b7b3913e390bd7a3532aa231059fdbe7b201288d8ca9613faf12ee686e4efa28

# `refactor`

## Summary
- refactor fork の変更差分要約と、ファイル単位のレビュー・修正に関する prompt builder および Structured Output schema の入口。変更要約では差分を意味論的カテゴリに分類し、レビュー・修正では oracle/realization の要求に基づく所見、修正、検証、変更 path の対応を扱う。
- 変更要約とファイル単位レビュー・修正の実行条件は対応する Python 定義で確認し、出力契約の項目・型・変更 path の扱いは対応する JSON schema で確認する。

## Read this when
- refactor fork の変更差分を人間向けに分類・要約する prompt と起動設定を調べるとき
- ファイル単位レビュー・修正の対象 path、worktree、ファイルアクセス、oracle/realization policy、検証条件を調べるとき
- 変更要約またはレビュー結果の Structured Output 契約と、変更 path・根拠・対応状態の関係を確認するとき

## Do not read this when
- 具体的な変更要約の prompt 構築処理を調査するときは、変更要約用 Python ファイルを直接読む
- ファイル単位レビュー・修正の prompt 構築処理を調査するときは、レビュー・修正用 Python ファイルを直接読む
- Structured Output の項目・型・status の値だけを確認するときは、対応する JSON schema ファイルを直接読む
- レビュー対象の実装内容、oracle/realization の個別要求、または実際の差分を調査するときは、対象ファイルや diff を直接読む

## hash
- 60204a0d0a0ebfd4b16c98d8255daf5f67165b186c06f5f5bfe63016c797d2f7
