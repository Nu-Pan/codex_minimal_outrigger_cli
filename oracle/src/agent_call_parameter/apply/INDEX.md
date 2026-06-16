# `fork`

## Summary

- `cmoc apply fork` で発生する Codex CLI 呼び出し仕様への入口です。
- `fork/` は、ファイル単位監査、要修正点リスト改善、要修正点対応作業、作業レポート用変更要約生成の agent call parameter をまとめます。
- Structured Output schema を使う呼び出しと、実装修正のように schema を使わない呼び出しの両方を案内します。

## Read this when

- `cmoc apply fork` の Codex CLI 呼び出し仕様をまとめて確認したいとき。
- apply fork の各段階でどの prompt と schema が使われるか把握したいとき。
- `fork/INDEX.md` へ進むべきか判断したいとき。

## Do not read this when

- `cmoc review oracle`、`cmoc indexing`、`cmoc session join` の Codex CLI 呼び出し仕様を探しているとき。
- apply fork の run isolation、git commit、レポート保存など Codex CLI 以外の制御処理だけを確認したいとき。

## hash

- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
