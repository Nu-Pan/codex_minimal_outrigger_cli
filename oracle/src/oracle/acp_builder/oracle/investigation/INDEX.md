# `launch_tui.py`

## Summary
- `cmoc oracle investigation` 用の完全プロンプトと Codex CLI TUI 起動パラメータを構築する実装。oracle 調査指示を固定の役割・制約・作業範囲へ組み込み、ログ保存先と実行設定を含む起動情報を返す。

## Read this when
- `cmoc oracle investigation` の TUI 起動条件、プロンプト構築、調査用ファイルアクセスモード、モデル・推論設定を変更または確認するとき。

## Do not read this when
- oracle investigation の調査内容や oracle file の仕様を確認したいときは、調査対象の oracle file やプロンプト構築処理を直接読む。
- 通常の Codex CLI 起動処理や、他の cmoc コマンドの起動パラメータだけを確認するとき。

## hash
- da8ff69fc3875c205415dee7f21a1ca2209cf3f1d175019cc697538e5ebb5925
