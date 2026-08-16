# `fork`

## Summary
- 対象ディレクトリは、refactor fork における変更要約とファイル単位レビュー・修正の agent call 定義、およびそれらの構造化出力スキーマを扱う入口です。
- 変更差分を意味論的カテゴリへ整理する出力契約を確認する場合は change_summary.json、要約 prompt と起動パラメータを変更・レビューする場合は change_summary.py を読みます。
- レビュー結果の出力契約を確認する場合は file_review_and_fix.json、レビュー・修正 agent call の prompt・権限・パス解決・検証設定を変更・レビューする場合は file_review_and_fix.py を読みます。

## Read this when
- refactor fork の変更差分を構造化要約する形式や、必須項目を確認するとき。
- 変更要約 agent の prompt、実行設定、Structured Output schema、linked worktree 設定を変更・レビューするとき。
- ファイル単位のレビュー・修正結果の契約、または対象 path を起点とする agent call の調査・修正・検証設定を確認するとき。

## Do not read this when
- 変更要約の生成ロジック自体ではなく、実際の変更内容や差分を調査するとき。
- レビュー対象の実装、正本仕様、個別ファイルの内容を調査するときは、該当する対象ファイルや oracle file を直接読みます。
- 共通 prompt 生成処理や refactor fork 以外の agent call builder を確認・変更するとき。

## hash
- cd30a22808714df3224da2435acf9b3712d38cf94153a4905d4633da5837021d
