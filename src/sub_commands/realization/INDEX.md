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
- realization の apply 処理に関する実装を扱うディレクトリ。apply workload の実装と、`realization apply fork` の CLI 実行フローを調査・変更する際の入口となる。
- apply fork では editing run の開始、差分追従 agent の実行、想定外変更や agent commit などの検査、INDEX 生成を含む変更の commit、joinable/error 状態と report の保存を扱う。

## Read this when
- realization の apply workload の内容を調査・変更するとき。
- `cmoc realization apply fork` の実行フロー、editing run の状態遷移、差分の commit・rollback・report 保存を確認するとき。
- apply agent の変更と cmoc が生成する INDEX 差分の境界、agent commit や遅延 child の扱いを確認するとき。

## Do not read this when
- apply workload 以外の realization 処理を扱うとき。
- apply agent の起動パラメータだけを変更するときは、agent launch parameter の実装を直接読む。
- editing run の共通ライフサイクル、git 操作、state 管理、index refresh の一般仕様だけを確認するときは、対応する共通実装または正本仕様を直接読む。
- apply fork の利用者向け仕様や run isolation・indexing の正本仕様を確認するときは、参照されている app specification を読む。

## hash
- 1cac93e44cd9b42024897895b67141aebefc28ad7144e9c990518c4195d92219

# `refactor`

## Summary
- realization のリファクタリング作業を扱うパッケージ。refactor fork の実行 lifecycle と関連処理への入口となる。
- fork の実行順序、対象選択、agent による変更検証、state 更新、INDEX 同期、完了・中断・エラー時の処理を確認する際は fork 実装へ進む。

## Read this when
- realization refactor fork の CLI 実行 lifecycle や処理順序を調査するとき
- 対象 realization file の選択、findings と unresolved の整合、refactor state 更新、完了条件を確認するとき
- agent の変更検証、INDEX refresh、rollback・joinable・error 処理を確認するとき
- fork report や completion log の生成内容・完了理由を確認するとき

## Do not read this when
- file review agent の入力形式や調査・修正プロンプトだけを確認する場合
- 正常完了時の変更概要生成の入力・Structured Output を確認する場合
- refactor state の一般的な保存・同期仕様だけを確認する場合
- run isolation や interruption の正本仕様を確認する場合

## hash
- 6d967dc9ec35685fad62a7e8185c1e5e92cae8c9f2a49bcbdcf72eff281457a9
