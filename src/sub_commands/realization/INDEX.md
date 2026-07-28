# `__init__.py`

## Summary
- realization workload サブコマンドのパッケージ入口。

## Read this when
- realization workload サブコマンドの実装や構成を確認するとき。

## Do not read this when
- realization workload サブコマンドに関係しない処理を確認するとき。

## hash
- 45f2cdf62d9edd181a1f1cc14734db2757e556059630746b1486c1bd5d1101b4

# `apply`

## Summary
- `__init__.py` は realization の apply workload を扱うモジュールで、apply workload 実装の入口となる。
- `fork.py` は `cmoc realization apply fork` の CLI サブコマンド実装で、agent 起動、oracle 差分、変更検査、INDEX 更新、commit・rollback、run 状態、fork report を扱う。

## Read this when
- realization の apply workload の内容を調査・変更するとき。
- `realization apply fork` の実行フロー、run 状態遷移、agent 差分の許可判定、commit・rollback、fork report を確認するとき。
- realization apply agent の起動条件、oracle 差分の受け渡し、INDEX 更新を含む処理単位を確認するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。
- realization apply の prompt 構築や agent parameter の詳細だけを確認するとき。
- run の共通ライフサイクル、プロセス追跡、report 出力の共通仕様だけを確認するとき。

## hash
- 186517b2c807ee9b332dd2edad16cd426f331f86f4a22d26f2273738341fbdd1

# `refactor`

## Summary
- realization のリファクタリング処理をまとめるパッケージ。パッケージ全体の構成確認や、fork によるリファクタリング実行フローの調査・変更への入口となる。

## Read this when
- realization のリファクタリング機能の構成や実行フローを確認するとき
- 対象選択、agent による調査・修正、差分検証、状態更新、commit、完了判定、report 保存を調査・変更するとき
- 割り込み・エラー時の cleanup や unresolved finding の管理を確認するとき

## Do not read this when
- refactor agent の入力 parameter や所見形式だけを確認したいとき
- change summary の Structured Output 生成だけを確認したいとき
- run の一般的なライフサイクルや git 差分操作の共通実装だけを確認したいとき

## hash
- 1166e47f271f99a6220ea300967130ac57cfc249d2110ed3f2c8ecc1e864e6c4
