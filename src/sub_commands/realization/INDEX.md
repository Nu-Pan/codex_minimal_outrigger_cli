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
- realization apply に関する処理をまとめたディレクトリ。apply workload の実装と、`realization apply fork` の CLI 実行フローを確認する入口となる。

## Read this when
- realization apply workload の内容を調査・変更するとき。
- `cmoc realization apply fork` の実行フロー、run state 遷移、fork report、変更検査、失敗時の rollback・cleanup・joinable 公開を調査・変更するとき。

## Do not read this when
- apply workload の実装詳細だけを確認したい場合は、配下の workload 実装を直接読む。
- agent のプロンプト生成や launch parameter を確認したい場合は、対応する builder 実装を直接読む。
- editing run 全般の状態管理や共通 rollback の仕様・実装を確認したい場合は、共通 runtime lifecycle または対応する正本仕様を直接読む。

## hash
- 11c127c114c434911902b1dc3f817e22ec1a3f17109d79087d8ced934a3e13b7

# `refactor`

## Summary
- realization のリファクタリング処理をまとめるパッケージ。refactor fork の full-cycle 実行と、対象選択から agent 呼び出し、変更・状態検証、finding 追跡、完了判定、cleanup、report 生成までの lifecycle への入口を提供する。

## Read this when
- realization のリファクタリング処理の構成や入口を確認するとき。
- realization refactor fork の実行フロー、処理単位の commit、state 更新、unresolved finding の完了条件を調査・変更するとき。
- agent による変更検証、INDEX 更新、run の joinable/error/interruption 処理、fork report の生成を追跡するとき。

## Do not read this when
- realization のリファクタリング以外の処理を確認するとき。
- realization refactor の agent prompt や change summary の入力形式だけを確認するときは、対応する builder 実装を直接読む。
- 編集 run の一般的な状態遷移や worktree isolation の正本仕様だけを確認するときは、対応する oracle doc を直接読む。

## hash
- 8722271f8ae83385f3107e553bf82bbf341bc068c0623c5da0fe30bfbb6fca7b
