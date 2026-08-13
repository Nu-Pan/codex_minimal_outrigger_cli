# `fork`

## Summary
- 変更要約とファイル単位のレビュー・修正を扱う Structured Output 定義および agent call 構築定義をまとめた領域。差分要約の出力契約、refactor fork の agent call 起動条件、レビュー用 prompt と検証設定を確認するための入口となる。

## Read this when
- 変更内容を意味論的カテゴリ別に要約する出力契約を確認するとき
- refactor fork の差分要約 agent call の入力差分、起動条件、実行環境を確認するとき
- refactor fork のファイル単位レビュー・修正用 prompt、oracle・realization 参照規則、検証設定を確認するとき
- レビュー・修正結果の出力契約や、所見の根拠・対応状態の記録方法を確認するとき

## Do not read this when
- 変更要約やレビュー・修正結果の出力項目・形式だけを確認する場合は、該当する Structured Output schema を直接読む
- レビュー対象の実装内容や個別仕様を調査する場合は、対象の oracle file または realization file を直接読む
- refactor fork 以外の agent call 構築や一般的な prompt 生成規則を確認する場合は、該当する別の定義を直接読む

## hash
- f33c71d1a90dee9a52ce62a73d5d8a8447ef951d0fbc4685471447096b9a7908
