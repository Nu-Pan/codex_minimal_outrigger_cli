# `fork`

## Summary
- refactor fork における変更要約とファイル単位レビュー・修正の agent call 定義、およびそれらの構造化出力契約をまとめた入口。変更差分の要約契約、要約用パラメータ、レビュー結果契約、レビュー用パラメータを確認できる。

## Read this when
- realization refactor の変更差分を要約する agent call の出力契約や、指定 commit 間の差分取得・実行条件を確認するとき
- realization refactor のファイル単位レビュー・修正 agent call の出力契約や、対象範囲・書き込み権限・実行条件を確認するとき

## Do not read this when
- 変更差分の具体的な実装内容、分類結果、レビュー対象ファイルの内容や個別所見を確認したいとき
- oracle の要求、realization の実装、共通 prompt 生成や構造化文書レンダリングの責務を直接調査・変更するとき

## hash
- b4b632ac0e3cd5ed0f95a54283fd8941a98e12ede141996d50ede89ef2ad4da3
