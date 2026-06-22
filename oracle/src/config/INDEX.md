# `cmoc_config.py`

## Summary

- `<cmoc-root>/oracle/src/config/cmoc_config.py` は、cmoc 全体の設定を束ねる `CmocConfig` と、その下位設定である `CmocConfigCodex`、`CmocConfigApplyFork`、`CmocConfigReviewOracle` を定義する入口です。
- この設定は `<repo-root>/.cmoc/config.json` として永続化され、`num_parallel` や `cmoc apply fork` / `cmoc review oracle` の反復回数、Codex CLI 向けの `model` / `reasoning_effort` 対応表をまとめます。

## Read this when

- cmoc 全体設定をどこに集約しているか確認したいとき。
- `CmocConfig` と、その下位の `CmocConfigCodex`、`CmocConfigApplyFork`、`CmocConfigReviewOracle` の構成を把握したいとき。
- `<repo-root>/.cmoc/config.json` に永続化される設定項目や、Enum 値を value 化して保存する方針を確認したいとき。

## Do not read this when

- `CmocConfig`、`CmocConfigCodex`、`CmocConfigApplyFork`、`CmocConfigReviewOracle` の役割がすでに分かっていて、このファイル本体を直接確認したいとき。
- 設定の読み書き処理や JSON 変換の実装を探しているとき。
- `basic/acp.py` の `ModelClass` や `ReasoningEffort` だけを確認したいとき。

## hash

- ccea2a3965b4022ccab0f635678dd917808b71820431e9e91f76f699315338f6
