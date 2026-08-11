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
- realization の apply 処理を構成する実装を扱うディレクトリ。apply workload の実装と、apply fork における agent 実行、差分検査、run状態更新、rollback、fork report保存の入口となる。

## Read this when
- realization の apply workload の内容を調査・変更するとき。
- `cmoc realization apply fork` の実行フロー、run状態遷移、fork reportの保存条件を調べるとき。
- apply agentが作成した差分の許可範囲、commit検査、想定外変更、失敗時のrollbackやerror stateを確認・変更するとき。

## Do not read this when
- apply workload以外のrealization処理を扱うとき。
- apply agent自体のプロンプト生成や差分適用仕様を調べるとき。
- editing run全般の共通ライフサイクル、INDEX生成機能そのものの仕様や実装を調べるとき。

## hash
- 2eb7b3e16a04df8e5901fe5b1081254e24ec9cf33810dcec224ead9f8de8563e

# `refactor`

## Summary
- realization のリファクタリング処理をまとめるパッケージ。fork 単位の実行管理と、関連するリファクタリング処理への入口を提供する。

## Read this when
- realization のリファクタリング作業の構成や実行管理を確認するとき
- 対象 file の調査・修正、refactor state と INDEX の同期、commit、完了判定、report 保存を含む fork のライフサイクルを確認するとき
- refactor fork の unresolved finding、rename、変更 path、agent 違反、cleanup failure の追跡を確認するとき

## Do not read this when
- realization のリファクタリング以外の処理を確認するとき
- 個別の realization file の修正・レビュー方法だけを確認したいとき
- refactor state のデータ構造や target 選択ロジックだけを確認したいとき
- INDEX.md の生成規則や routing だけを確認したいとき

## hash
- d7f438e5e9473162267f907970f7567797c0a137239f7eb7732eadcd321ddc5a
