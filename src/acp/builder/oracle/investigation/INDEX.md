# `__init__.py`

## Summary
- `cmoc oracle investigation` 用 builder adapter パッケージの役割を示す。

## Read this when
- 調査コマンド向け builder 群の中で、このパッケージの位置づけを確認するとき。

## Do not read this when
- 起動 TUI 用パラメーターの生成や互換 import の公開内容を調べるときは、該当する個別 builder モジュールを直接読む。

## hash
- c4c41f07d0b59e430e93561b97dcc2321301abc3cedb93fdeb0ef16a0c9a9637

# `launch_tui.py`

## Summary
- oracle 調査用 TUI パラメータを構築する正本 builder を、旧 import 経路で再公開する互換 adapter。prompt や起動設定の構築自体は委譲先が担う。

## Read this when
- 旧 import 経路の維持・移行・削除条件や、この adapter を使う呼び出し箇所を調べるとき。

## Do not read this when
- prompt 内容、調査範囲、TUI 起動パラメータの選択や理由を調べるときは、正本 builder へ進む。
- サブコマンドの入力手順や起動の流れを調べるときは、サブコマンド実装へ進む。
- 調査の意味上の責務や境界を確認するときは、oracle investigation の正本仕様へ進む。

## hash
- c9ebfcd1e073b1bb8b9430c48b70b35c88846eb0e05f45525bfa9f90da992c7e
