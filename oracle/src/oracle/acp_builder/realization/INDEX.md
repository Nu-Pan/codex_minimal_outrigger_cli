# `apply`

## Summary
- Oracle の変更差分を埋め込んだ realization 追従用の完全な prompt と AgentCallParameter を構築し、linked worktree、commit 範囲、書き込み権限、モデル設定、事前 indexing を含む agent call の起動設定を担う。

## Read this when
- oracle file の変更を realization implementation・test・ancillary 全体へ反映する agent call の起動条件や prompt を変更するとき。
- realization apply fork の実行 cwd、差分情報、権限、モデル・推論設定を確認するとき。

## Do not read this when
- 通常の realization 実装やテストの内容を変更するとき。
- oracle の仕様や共通 prompt 構築処理を確認するとき。対応する oracle file や prompt builder を直接読む。

## hash
- 8c1fa6ddc8b66ad59031966d99e543a070f67a0f3980b967283a5aa98b205aa6

# `refactor`

## Summary
- refactor fork の変更要約およびファイル単位レビュー・修正に関する Structured Output schema と、これらの agent call パラメータ構築処理をまとめた領域。差分要約、レビュー所見、対象 path・linked worktree・prompt・モデル・権限・検証設定を扱う。

## Read this when
- refactor fork の変更要約やレビュー結果の出力 schema を確認するとき
- 変更要約 agent call の prompt、差分入力、実行条件、モデル設定を確認するとき
- ファイル単位の realization review・fix agent call の対象 path、権限、検証要件、Structured Output schema 指定を確認するとき

## Do not read this when
- 実際の変更内容や realization code の挙動を調査するとき
- 個別の Structured Output schema の具体的な定義だけを確認するとき
- レビュー・修正 agent call の実処理そのものを調査するとき
- 他の agent call 種別の prompt 構築規則だけを調査するとき

## hash
- 318ecc69d1d90df72308619839ab42029bdaa4869e8935526c77c0d890cfbe3e
