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
- realization の apply 処理に関する workload を扱うモジュール。apply workload の実装を確認する入口となる。
- `cmoc realization apply fork` サブコマンドの実行処理を担う。差分の始点特定、oracle diff 構築、realization apply agent の実行、変更検査・commit、run の joinable 更新、fork report 保存までを管理する。

## Read this when
- realization の apply workload の内容を調査・変更するとき。
- realization apply fork の実行フロー、run の joinable/error 遷移、agent 差分の検査や commit、fork report の生成を変更・調査するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。
- realization apply の prompt 構築だけを変更・調査するときは、launch parameter builder を直接読む。run の共通ライフサイクルや状態管理だけを変更・調査するときは、commons の runtime lifecycle 実装を直接読む。

## hash
- 433885d3f3ddd4ccb2b128466bfba4252746073331fdee9ef6162bb6684dd05a

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
