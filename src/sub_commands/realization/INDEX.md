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
- `cmoc realization apply fork` の実行本体として、差分始点を解決し、realization 追従 agent を実行する。agent の差分と生成物を検査・commit し、joinable または error の run と fork report を公開する。

## Read this when
- realization の apply workload の内容を調査・変更するとき。
- realization apply fork の実行フロー、差分始点の解決、agent の commit 検査、差分の検査・commit、INDEX 更新、run state や fork report の公開動作を確認するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。
- realization apply fork の launch parameter の組み立てだけを確認したいとき。
- run の join・abandon、一般的な editing run lifecycle、または report の共通実装を確認したいとき。

## hash
- 858afe03b4cd355ac13913f774fb8c53980a1b90279c9a2af2f0dbcb29161d9c

# `refactor`

## Summary
- realization のリファクタリング処理への入口となるパッケージ。
- realization refactor fork の実行ライフサイクル、処理単位の進捗、unresolved findings、完了判定、変更・commit・INDEX 更新の検証、中断・エラー時の cleanup と report 保存を扱う。

## Read this when
- realization のリファクタリング処理の構成や入口を確認するとき。
- realization refactor fork の lifecycle、進捗、unresolved findings、完了理由、変更概要、agent の変更・realization file・changed_paths・git commit・INDEX refresh の検証境界を確認するとき。

## Do not read this when
- realization のリファクタリング以外の処理を確認するとき。
- refactor state の基本形式、run の join・abandon、共通の editing run lifecycle、一般的な INDEX 更新仕様だけを確認するとき。

## hash
- aae4389dc97e77f1c1b683be1312b56ab438920521b7cbf8b3efb45edd6d2a6c
