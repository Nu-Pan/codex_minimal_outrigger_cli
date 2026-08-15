# `__init__.py`

## Summary
- `cmoc oracle investigation` 用 builder adapter パッケージの入口。oracle investigation 向け builder 機能へ進む際の参照先。

## Read this when
- oracle investigation 用 builder adapter の構成や入口を確認するとき
- 該当パッケージ内の下位実装へ進む前に責務を確認するとき

## Do not read this when
- builder adapter の具体的な実装詳細を確認したいとき
- oracle investigation 以外の builder や ACP 実装を調べるとき

## hash
- c4c41f07d0b59e430e93561b97dcc2321301abc3cedb93fdeb0ef16a0c9a9637

# `launch_tui.py`

## Summary
- oracle investigation の正本 builder を互換 import 経路として公開するファイル。investigation 起動 TUI パラメータ builder への入口を提供し、正本実装を直接再定義せずに再公開する。

## Read this when
- oracle investigation の起動 TUI パラメータ builder を、既存の互換 import 経路から参照する必要があるとき
- この互換経路の公開対象や import の再公開範囲を確認するとき

## Do not read this when
- builder の処理内容や investigation 起動パラメータの仕様を確認・変更するとき
- 正本実装を確認する必要があるときは、oracle investigation 側の正本 builder を直接読む

## hash
- 2d3936ac0809fdf6e1636e9ec6c8bd7f16738e5ba0ae456a8c9e2a347a82ad94
