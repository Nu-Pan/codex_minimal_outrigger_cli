# `fork`

## Summary
- refactor fork で使う変更要約とファイル単位レビュー・修正の agent call 定義をまとめ、各 call の出力契約も定義する。
- 変更要約は指定された commit 間の差分全体を読む read-only 作業、ファイル単位 call は指定 path から所見を調査し、同じ call 内で realization file を修正・検証する作業の入口となる。

## Read this when
- fork の変更要約 call について、調査範囲や commit 境界、出力内容を変更または確認するとき。
- ファイル単位レビュー・修正 call の調査範囲、書き込み範囲、同一 call 内での修正・検証・変更報告の扱いを確認するとき。

## Do not read this when
- fork 全体の起動や call の順序、commit 管理を調べる場合は、agent call 定義ではなくそれらを担う orchestration を読む。
- 共通の prompt 構築、パス解決、構造化出力検査の挙動が論点なら、この call 定義ではなく各共通定義を直接読む。

## hash
- 388717684a8311bfa27fd864a9b1cce60c7fc53b64133c70c9626ebc447821c5
