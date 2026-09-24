# `launch_tui.py`

## Summary
- `cmoc oracle investigation` の Codex TUI 向けに、ユーザーの調査指示を含む完全プロンプトと、oracle 読み取り専用の起動パラメータを組み立てる。
- 調査結果で oracle file を根拠として特定させ、editor-input handoff と indexing preflight を有効にする起動設定の入口。

## Read this when
- `cmoc oracle investigation` の TUI 呼び出しで、調査指示のプロンプトへの組み込み方、oracle 読み取り制限、handoff、preflight、起動パラメータを変更または追跡するとき。
- 調査タスクの責務や、agent に渡す調査範囲・根拠提示基準を確認するとき。

## Do not read this when
- 個別の oracle file の内容や仕様自体を調査・改訂するとき。この起動設定を変えないなら対象外。
- agent 呼び出し全般に共通する prompt 構築や型定義を変更するとき。この対象は oracle investigation 固有の TUI 設定に限られる。

## hash
- 1a42a8af1276a394d082ff1f55912e556dbf1aefc9bdcebb837c8b93911662a6
