# `launch_tui.py`

## Summary
- `cmoc oracle investigation` の TUI 起動用パラメータを構築する実装。ユーザー調査指示を埋め込んだ完全プロンプトを生成・保存し、モデルやアクセス権限など固定の起動設定とともに返す。

## Read this when
- `cmoc oracle investigation` の TUI 起動処理、完全プロンプトの構築・保存、または起動パラメータの固定値を変更・調査するとき。

## Do not read this when
- 調査用プロンプトの本文構成や共通プロンプト生成規則だけを確認したいときは、完全プロンプトを構築する実装を直接読む。
- oracle investigation 以外の agent call パラメータや TUI 起動処理を調査するとき。

## hash
- 7424488cff693a4c6b5cb8e411e2f7fa3c36378184089e42399714114b227c37
