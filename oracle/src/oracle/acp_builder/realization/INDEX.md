# `apply`

## Summary
- realization apply の追従起動処理をまとめる領域。変更差分を含む完全 prompt と AgentCallParameter を構築し、下位の fork 実装へ進む入口となる。

## Read this when
- realization apply fork の agent call に渡す変更情報、prompt、実行権限、worktree、モデル・推論設定、実行前 indexing を確認・変更するとき。

## Do not read this when
- oracle file の変更内容や realization implementation・test の具体的な実装を確認するとき。一般的な prompt 構築や別の実行系の起動設定を調べるとき。

## hash
- aa0fd1c9af2f8eba0efc0afc6e21a02df0907fd17c4ed18e3e74bb47e0a9282c

# `refactor`

## Summary
- refactor fork における変更要約とファイル単位のレビュー・修正を扱う定義群。差分の意味論的分類、レビュー・修正 agent call のプロンプト構築、oracle・realization 参照規則、検証条件、結果報告の契約を確認する入口。

## Read this when
- refactor fork の変更差分を人間向けに分類・要約する agent call の契約や起動条件を確認するとき
- refactor fork の特定ファイルを起点としたレビュー・修正の作業範囲、参照規則、修正条件、検証条件を確認するとき
- レビュー・修正結果における所見、根拠、変更 path、対応状態の報告方法を確認するとき

## Do not read this when
- 変更要約の出力項目や形式だけを確認する場合は、変更要約用の Structured Output schema を直接読む
- レビュー・修正結果の出力項目や形式だけを確認する場合は、ファイル単位レビュー・修正用の Structured Output schema を直接読む
- レビュー対象の実装や個別仕様を調査する場合は、対象の oracle file または realization file を直接読む
- refactor fork 以外の agent call 構築規則を確認する場合は、該当する定義を直接読む

## hash
- cc9bff6e33e725c9d30c7896cfce4e77de6f2c6a4fa8e64bc4aef418f107f365
