# `cmoc_config.py`

## Summary

- `<cmoc-root>/oracle/src/cmoc_config/cmoc_config.py` は、cmoc 全体の設定をまとめる `CmocConfig` と、Codex CLI 向けの対応表を持つ `CmocConfigCodex` を定義する入口です。
- この設定は `<cmoc-root>/.cmoc/config.json` として永続化され、`BackendType`、`ModelClass`、`ReasoningEffort` を束ねる前提になっています。

## Read this when

- cmoc の設定項目をどこに集約しているか確認したいとき。
- `CmocConfig` と `CmocConfigCodex` の役割や、Codex CLI 向けの `model` / `reasoning_effort` 対応付けを把握したいとき。
- 設定を `<cmoc-root>/.cmoc/config.json` に永続化する前提や、Enum 値を value 化して保存する方針を確認したいとき。

## Do not read this when

- すでに `CmocConfig` と `CmocConfigCodex` の定義場所が分かっていて、この目次を経由せずに `cmoc_config.py` 本体を直接確認するとき。
- 設定の読み書き処理や JSON 変換の実装を探しているとき。
- `agent_call_parameter/base.py` の `BackendType`、`ModelClass`、`ReasoningEffort` だけを確認したいとき。

## hash

- 27fc1c26c773b767e4ba15c6f45826c1f2b9e85924a9990d4e77fc96823c5ea1
