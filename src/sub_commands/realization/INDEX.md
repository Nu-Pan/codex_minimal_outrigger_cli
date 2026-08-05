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
- realization の apply 処理を構成するモジュール群。apply workload の実装入口と、`cmoc realization apply fork` の実行・run lifecycle・差分検査・commit・状態遷移・fork report 保存を扱う。

## Read this when
- realization の apply workload の内容を調査または変更するとき。
- `cmoc realization apply fork` の CLI 動作、run lifecycle、agent 差分の許可範囲、commit・joinable/error 遷移、fork report の生成を確認または変更するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。
- apply agent に渡す launch parameter だけを確認するとき。
- run の join・abandon 処理や共通 lifecycle の実装を確認するとき。
- realization apply の正本仕様を確認するとき。

## hash
- 6328a3fb5fd66ea735889bff8f471e4af11f51a9b873ee20bec41d585ea8b27e

# `refactor`

## Summary
- realization のリファクタリング処理をまとめるパッケージで、関連する CLI 実装への入口となる。
- fork.py は realization refactor fork の実行全体を統括し、対象選択、Codex による調査・修正、state・差分・commit・INDEX の検証、所見管理、完了判定、report 保存までを扱う。

## Read this when
- realization のリファクタリング処理の構成や CLI 実行フローを確認するとき。
- fork の正常完了・中断・エラー時の state 更新、cleanup、rollback、report 生成を調査するとき。
- 対象 file の処理、agent 差分、commit、INDEX 更新、完了条件の検証を確認するとき。

## Do not read this when
- 個別 refactor agent の Structured Output や prompt builder だけを確認したいとき。
- refactor state のデータ形式や対象選択ロジックだけを確認したいときは、state 管理を担う実装を直接読む。
- run 共通ライフサイクル、report 表現、process tracking、INDEX 更新の一般仕様だけを確認したいときは、各共通実装または正本仕様を直接読む。

## hash
- ed2e75232055fb8cd9c338ea6e73e5c2004cfe6f55b5fa95a01c7a5f0a608d93
