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
- oracle investigation の正本 builder 関数を互換 import 経路として公開する。既存の acp.builder.oracle.investigation.launch_tui 利用箇所から正本実装へ接続するための入口で、oracle.* への移行完了後は削除対象となる。

## Read this when
- 既存の acp.builder.oracle.investigation.launch_tui import 経路の互換性や、oracle investigation の launch_tui builder への移行状況を確認するとき。

## Do not read this when
- 正本の builder 実装や oracle investigation の仕様・挙動を確認したいときは、oracle 側の launch_tui 実装を直接読む。
- acp.builder.oracle.investigation.launch_tui の互換性を調べる必要がない一般的な oracle investigation の調査では、このファイルを読む必要はない。

## hash
- c9ebfcd1e073b1bb8b9430c48b70b35c88846eb0e05f45525bfa9f90da992c7e
