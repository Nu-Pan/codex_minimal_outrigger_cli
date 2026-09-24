# `__init__.py`

## Summary
- TUI 起動 builder の既存 import 経路を保つ互換パッケージであり、realization 側と利用者向け公開面からその経路がなくなった後に削除できるかを判断する入口です。

## Read this when
- TUI 起動 builder の旧 import 経路を維持する必要があるか、互換パッケージを削除できるかを確認するとき。

## Do not read this when
- 起動パラメーターの生成処理や内容を変更するときは、互換パッケージの説明ではなく、生成処理の実装と正本側の定義を確認してください。

## hash
- d9cfe056fb590ace7dace1732eced1ab73daab8f28e521f8d480dd52beb37a60

# `launch_tui.py`

## Summary
- TUI 起動パラメータ構築関数を既存の import 経路から再公開する互換層です。
- パラメータ構築の処理本体は oracle 側の実装定義にあります。

## Read this when
- TUI 起動パラメータ構築関数の公開経路や、その互換層の構成を確認・変更するとき。

## Do not read this when
- prompt の文面や起動パラメータの具体的な構築方法を調べるときは、処理本体の実装定義を直接読む。

## hash
- 1a8a4aaf0f802fad209b12e2f0fbf5a2632620119c7e31c49847c01a3da61a93
