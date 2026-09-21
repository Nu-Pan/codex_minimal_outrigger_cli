# `launch_tui.py`

## Summary
- `cmoc oracle investigation` 用の完全プロンプトと Codex CLI TUI 起動パラメータを構築する。ユーザーの調査指示を埋め込み、oracle file のみを根拠とする読み取り調査、エディタ入力引き継ぎ、索引付け事前処理などの実行条件を固定する。

## Read this when
- `cmoc oracle investigation` の TUI 起動条件や、ユーザーの oracle file 調査指示から起動パラメータを組み立てる処理を確認・変更するとき。

## Do not read this when
- 完全プロンプトの共通生成規則を確認したいときは prompt builder の実装を直接読むべき場合。
- oracle investigation 以外の ACP 起動処理や、TUI 自体の表示・操作実装を確認するとき。

## hash
- 1a42a8af1276a394d082ff1f55912e556dbf1aefc9bdcebb837c8b93911662a6
