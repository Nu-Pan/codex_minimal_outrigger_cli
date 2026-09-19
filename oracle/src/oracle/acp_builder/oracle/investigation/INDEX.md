# `launch_tui.py`

## Summary
- 対象は、Oracle 側の ACP builder 調査用 TUI を起動する処理を担う実装ファイルです。
- 調査用起動処理の挙動、起動引数、または TUI 起動経路を確認・変更するときの入口になります。

## Read this when
- Oracle の ACP builder 調査フローで TUI の起動方法や起動時の処理を確認したいとき。
- この調査用ランチャーの引数処理や呼び出し先との接続を変更するとき。

## Do not read this when
- TUI 本体の画面表示・対話ロジックを直接調べたいときは、起動先の実装を直接読んでください。
- ACP builder の一般的な実装や仕様を確認したいだけで、調査用 TUI の起動経路に関係しないとき。

## hash
- 23f74c627d7e822d0314711a4c1c36a76a8a4571bc5b0dc9ec7ab45f182154fb
