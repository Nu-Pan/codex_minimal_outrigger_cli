# `fork`

## Summary
- realization refactor の fork にある、変更要約用およびファイル単位レビュー・修正用の agent call 定義と、その Structured Output schema を扱う入口。
- 変更差分の要約契約、要約 agent call の prompt・実行条件、レビュー・修正結果の報告項目、対象特定と実行条件の構築責務を確認できる。

## Read this when
- realization refactor の変更差分を人間向けに要約する出力形式や prompt 構成を確認するとき
- realization refactor のファイル単位レビュー・修正 agent call の出力契約、対象範囲、prompt、権限、実行前設定を調査するとき
- レビュー所見の根拠、oracle 要求との関係、修正済み・未解消の対応状況を追跡するとき

## Do not read this when
- realization の実装内容、具体的な変更差分、個別の分類結果やレビュー所見を確認したいとき
- oracle file の要求や設計責務を確認するとき
- realization refactor 以外の agent call 構築、差分生成・適用、通常の入出力契約を調査するとき

## hash
- a9622f5d52f757202913395eeb8fc77de7928db8acc7aad98ec215f85f3faa0f
