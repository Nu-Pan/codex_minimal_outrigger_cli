# `oracles`

## Summary

- `cmoc review oracle` で発生する Codex CLI 呼び出し仕様への入口です。
- `oracles/` は、新規所見列挙、所見リストマージ、所見の否定理由列挙、擁護理由列挙、採否判定の agent call parameter と schema をまとめます。
- すべて読み取り専用で、oracle file を対象に Structured Output を返すレビュー用呼び出しです。

## Read this when

- `cmoc review oracle` の Codex CLI 呼び出し仕様をまとめて確認したいとき。
- 所見の列挙、統合、妥当性検証、採否判定のどの prompt/schema を読むべきか判断したいとき。

## Do not read this when

- `cmoc apply fork`、`cmoc indexing`、`cmoc session join` の agent call parameter を探しているとき。
- review oracle のレポート markdown 生成や run isolation など、Codex CLI 以外の制御処理だけを確認したいとき。

## hash

- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
