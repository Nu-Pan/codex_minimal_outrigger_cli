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
- realization apply の workload 実装を扱うディレクトリ。apply workload 全体の調査・変更時に、配下の各実装へ進む入口となる。

## Read this when
- realization apply workload の実行フロー、agent 起動、差分検証、commit・rollback、run state、fork report の挙動を調査・変更するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。
- agent 起動パラメータ、run の共通 lifecycle・差分計算・状態管理、fork report の形式だけを変更・調査するとき。

## hash
- b01abe2a06082d4c8096e120594ec68328dcac5efc628f9af6800bddd4c4486b

# `refactor`

## Summary
- realization のリファクタリング処理を扱うパッケージ。fork のライフサイクル実行と関連処理への入口を提供する。
- fork は、run 初期化から target 選択、調査・修正・commit、unresolved 管理、完了検証、summary/report 生成、中断・例外時の cleanup までを一つのフローとして実装する。

## Read this when
- realization refactor fork の CLI 実行フロー、target 処理、unresolved finding、完了判定を確認・変更するとき。
- 中断・例外時の cleanup、run state、fork report、change summary、worktree や agent 出力の整合性を調査するとき。
- realization のリファクタリング作業全体の構成や入口を確認するとき。

## Do not read this when
- target 選択や state 同期だけを変更・調査する場合。
- file 単位の調査・修正 agent の prompt 構築だけを変更する場合。
- 一般的な run lifecycle、report 出力、process tracking の共通実装だけを確認する場合。

## hash
- a4e80e064346eb0492ad620f30f739fca349cd4a88d53da14baec64b3d4607e5
