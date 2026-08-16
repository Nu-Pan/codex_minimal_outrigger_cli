# `apply`

## Summary
- realization apply fork の起動パラメータと完全 prompt を構築する実装。oracle file の commit 範囲・raw diff を追従対象として組み込み、linked worktree、realization write 権限、モデル・推論強度、各種ポリシー、indexing preflight を固定した AgentCallParameter を返す。差分追従処理の起動条件や prompt・実行設定を確認する入口。

## Read this when
- realization apply fork の差分追従 AgentCallParameter、oracle diff の prompt への組み込み、worktree やアクセスモード、モデル・推論設定、indexing preflight を確認・変更するとき。

## Do not read this when
- realization file の具体的な実装・テスト・補助ファイルを確認するとき。oracle file の仕様や一般的な AgentCallParameter 定義を直接確認するとき。

## hash
- 64971e260467e6aaf07b094630c1c049b70bcbfa3c477b614b0dac6e86301801

# `refactor`

## Summary
- refactor fork の変更要約と、ファイル単位のレビュー・修正を起動する AgentCallParameter、および各処理の Structured Output 契約を定義する。変更差分の意味論的な分類、レビュー所見と修正結果、対象範囲・権限・検証条件を確認する際の入口となる。

## Read this when
- refactor fork の変更差分を人間向けに分類・要約する agent call の prompt、モデル設定、入力差分、出力契約を確認または変更するとき
- ファイル単位のレビュー・修正 agent call の対象範囲、oracle／realization の参照規則、書き込み権限、検証条件を確認または変更するとき
- 変更要約またはレビュー・修正の Structured Output schema を確認・変更するとき

## Do not read this when
- 実際の refactor 差分、レビュー対象ファイル、または realization 実装そのものを調査するとき
- レビュー所見や変更要約のフィールド定義だけを確認する場合は、対応する JSON schema を直接読む
- refactor fork 以外の agent call 構築、prompt builder、または realization 実装の責務を調査するとき

## hash
- 2b5cce0711134ad15ddc2f60585063b4b1b6dc0b7f20ac1f155d713345a784e2
