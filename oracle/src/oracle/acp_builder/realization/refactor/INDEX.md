# `fork`

## Summary
- refactor fork に関する agent call の構造化出力 schema と、変更要約・ファイル単位レビュー／修正用パラメータ構築処理をまとめた領域。差分要約の出力形式、レビュー結果 schema、対象ファイルや linked worktree を含む agent call 設定の入口を扱う。

## Read this when
- refactor fork の変更要約出力形式や検証項目を確認するとき
- refactor fork の差分要約 prompt、実行条件、モデル設定、Structured Output schema を確認するとき
- ファイル単位の realization review・fix agent call の prompt、権限、対象 path、検証要件を変更または確認するとき

## Do not read this when
- 実際の変更内容や realization code の挙動を調査するとき
- Structured Output schema の具体的な定義だけを確認するときは、対応する schema file を直接読む
- レビュー・修正の実処理そのものを調査するとき
- 他の agent call 種別の prompt 構築規則だけを調査するとき

## hash
- ce90c7784015e55b280235812052ddf4a0768f40ee12985f5e5277179be5a804
