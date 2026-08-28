# `fork`

## Summary
- realization refactor の変更要約に関する Structured Output schema、agent call の構築定義、ファイル単位レビュー・修正の出力契約および起動パラメータを扱うディレクトリです。
- 変更要約の出力形式を確認する場合は change_summary.json、要約 agent call の prompt・起動条件を確認する場合は change_summary.py が入口です。
- ファイル単位レビュー・修正の結果契約を確認する場合は file_review_and_fix.json、対応する agent call の構築規則を確認する場合は file_review_and_fix.py が入口です。

## Read this when
- realization refactor の変更差分を人間向けに要約する処理の出力形式や起動定義を確認するとき
- realization refactor のファイル単位レビュー・修正について、出力契約または agent call のパラメータ構築規則を確認するとき

## Do not read this when
- realization refactor の実装差分、変更の分類結果、またはレビュー対象そのものを確認したいとき
- oracle file の要求や設計責務を確認したいとき
- realization refactor 以外の agent call や出力形式を確認したいとき

## hash
- 4e4d3e58737a032a24b3de0d885a11b7e55015128a435bf8bd368b9a5e60d85d
