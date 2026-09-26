# `__init__.py`

## Summary
- realization の apply workload を示すパッケージ説明です。実行処理を追う際は、配下の workload 実装が入口になります。

## Read this when
- realization の apply workload が refactor workload とどう区別されるか、パッケージ説明を確認するとき。

## Do not read this when
- コマンド登録や fork の実行手順を調べるとき。このファイルはパッケージ説明のみなので、登録箇所または workload 実装を確認してください。

## hash
- d6d2ca470e50cfd6872e3d6ceaaf3a134b7f0dc8205826c843ca70d79352d5f7

# `fork.py`

## Summary
- `cmoc realization apply fork` の実行単位を管理し、oracle の差分を agent に適用させて joinable run として公開する。
- 差分基点の選択、agent の変更検査と commit、成功・失敗時の cleanup と fork report を扱う。

## Read this when
- `realization apply fork` の run 作成から agent 呼び出し、差分の確定、report 保存までの挙動を変更・調査するとき。
- agent による commit や想定外変更、失敗時の rollback、fork report の内容を調べるとき。

## Do not read this when
- agent 向け指示や launch parameter の生成方法を変更するときは、realization apply の oracle builder を直接確認する。
- realization refactor の full-cycle や共通 run lifecycle の挙動を調べるときは、それぞれの担当実装を直接確認する。

## hash
- 9ec1462cc0cd4cf0f03b2f5cb6f11bd9aa4fd00dd5e2362c88d8e7329e401990
