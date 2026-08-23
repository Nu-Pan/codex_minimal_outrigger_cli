# `fork`

## Summary
- refactor fork における差分要約とファイル単位レビュー・修正の agent call 定義、および各処理の Structured Output schema を案内するルーティング文書。差分要約用では確定済み変更の要約、レビュー用では対象ファイルの調査・修正・検証に関する prompt と起動パラメータの確認入口となる。

## Read this when
- refactor fork の変更差分を意味論的カテゴリに整理する出力形式や、そのための agent call 構築を確認するとき
- ファイル単位のレビュー・修正処理における prompt、調査範囲、修正方針、検証条件、起動パラメータを確認するとき

## Do not read this when
- 実際の変更内容や生成済みの差分要約を確認したいとき
- レビュー対象の実装内容、個別仕様、またはレビュー・修正処理そのものの実装を調査したいとき
- Structured Output の項目や JSON schema の形式だけを確認したいときは、対応する schema file を直接読む

## hash
- ed32ab35f60e7bea9708f50907fc4ae7e409a71fe5d8f76892ae932a4a5a9160
