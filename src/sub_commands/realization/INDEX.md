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
- realization の apply 処理を実行する CLI 実装群。apply workload の入口であり、fork 実行のライフサイクル管理や成果物・失敗状態の処理を確認するためのディレクトリ。

## Read this when
- realization apply workload の実装を調査・変更するとき。
- `cmoc realization apply fork` の実行、差分検査、rollback、state 更新、fork report 保存の挙動を確認するとき。

## Do not read this when
- apply agent の prompt や launch parameter だけを確認したいとき。
- editing run の共通 lifecycle や join・abandon の一般仕様だけを確認したいとき。
- INDEX.md の生成規則そのものを確認したいとき。

## hash
- 656380685f3cfc655990d62480989ca03a00cb933c758f8a9edbca3f204a7556

# `refactor`

## Summary
- realization のリファクタリング作業を扱うパッケージ。関連するリファクタリング処理への入口となる。

## Read this when
- realization のリファクタリング作業の内容や構成を確認するとき。

## Do not read this when
- realization のリファクタリング以外の処理を確認するとき。

## hash
- 3d24150ed3141eea9fbd28b6f09763a26944911cd85111e390c461511185c52a
