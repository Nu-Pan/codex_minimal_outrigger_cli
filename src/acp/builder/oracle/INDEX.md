# `__init__.py`

## Summary
- Oracle コマンド builder 用の realization adapter 群をまとめる package-level entry です。initializer 自身は builder 関数を公開せず、既存 import 経路を保つ adapter の位置づけを示します。
- コマンド固有の adapter は正本 builder への互換 import 経路を担います。コマンドの構築処理そのものは正本 builder 側にあります。

## Read this when
- Oracle コマンド builder の adapter 群の役割や、互換 import を扱う範囲を確認するとき。
- 特定コマンドの adapter がどの package 群に属するかを判断するとき。

## Do not read this when
- 編集系または調査系の個別 adapter の import や公開内容を変更するときは、その adapter package を直接読む。
- コマンドの parameter 構築や起動時の動作を調べるときは、正本 builder の実装を直接読む。

## hash
- 04f29448a0f9d675976d8cda22279a162a5e8e89a169554a4926766bf0f88d6b

# `edit`

## Summary
- `cmoc oracle edit` が利用する ACP builder の互換 import 入口を提供し、正本 builder の関数を公開する。
- 実装は正本 builder からの再 export に限られ、exec parameter や prompt の構築定義はここにはない。

## Read this when
- `cmoc oracle edit` の ACP builder import 名や、パッケージ配置時の互換 import 経路を確認・変更するとき。

## Do not read this when
- CLI の実行順序、editor 入力、agent call の制御を調べるときは、subcommand の実行処理を直接読む。
- prompt の内容、oracle 編集方針、exec parameter の構成を変更するときは、委譲先の oracle 側 builder 定義を直接読む。

## hash
- 5da3687b9528c9878fc050790608d23901e1dec1e3fd53f6cda380ce869ed50e

# `investigation`

## Summary
- oracle investigation builder の旧 import 経路を保つ互換 adapter。正本側の builder 関数を再公開し、呼び出し元の移行まで旧経路を維持する。

## Read this when
- 旧 `acp.builder` 系 import 経路の互換性、移行、削除条件を調べるとき。

## Do not read this when
- 調査用 prompt や TUI 起動パラメータの構築内容を調べるときは、正本 builder の定義を直接読む。
- CLI コマンドから builder までの呼び出しの流れを調べるときは、コマンド側の処理を直接読む。

## hash
- ee2b233b3a0171319a5425e67d6d5c88e7ef3c3f306281f8eba3a8a0996a918c

# `review`

## Summary
- 所見レビュー用の互換 import 経路を提供し、列挙・採否判定・統合・擁護理由と反証理由の調査に使う呼び出しパラメータ生成を、正本側の実装へ委譲する。

## Read this when
- レビュー呼び出し側との互換性や、この経路から公開されるパラメータ生成処理を確認するとき。

## Do not read this when
- レビュー用プロンプトやパラメータの生成内容を調べるときは、正本側の各実装から確認する。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
