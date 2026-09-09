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
- realization の apply workload を扱うモジュール群への入口。
- apply fork の実行入口として、editing run の作成、oracle 差分範囲の固定、追従 agent の実行、変更検査と commit、joinable/error 状態の記録を担う。

## Read this when
- realization apply workload の構成や実装を調査・変更するとき
- realization apply fork の実行手順、差分の始点、agent 実行後の変更検査・commit、joinable/error run の状態遷移を確認するとき

## Do not read this when
- apply workload 以外の realization 処理を扱うとき
- realization apply の agent 起動パラメータを確認したいとき
- editing run の共通 lifecycle や run の join・abandon 実装を確認したいとき
- INDEX.md 生成の一般仕様や利用者向け CLI 仕様だけを確認したいとき

## hash
- c3a77808dce997fb29e44a0e9c6129da744dc557e9ee958b581a261b12cedb17

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
