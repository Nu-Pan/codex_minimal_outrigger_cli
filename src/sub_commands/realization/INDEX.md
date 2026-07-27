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
- realization の apply 処理に関する workload と、`cmoc realization apply fork` の実行制御を扱う。apply workload の調査入口であり、fork では editing run の開始から agent 実行、差分検査、commit・rollback、run 状態更新、report 保存、joinable 公開までを統括する。

## Read this when
- realization の apply workload の内容を調査・変更するとき
- `cmoc realization apply fork` の開始から joinable または error までの制御フローを確認するとき
- apply agent の実行条件、oracle 差分、想定外差分、commit、rollback、run report、例外処理を調査・変更するとき

## Do not read this when
- apply workload 以外の処理を扱うとき
- 共通の editing run ライフサイクル、process tracking、report 生成の一般仕様や実装だけを調査するとき
- `cmoc realization apply` の通常実行や別の apply サブコマンドだけを調査するとき
- apply agent の prompt 構築内容だけを確認するとき

## hash
- 66f6170c37b0f2633264194384049584f7809db7f2ef2c8455dba3f5466cd08e

# `refactor`

## Summary
- realization のリファクタリング処理を扱うパッケージ。fork サブコマンドの実行ライフサイクル、対象ファイルの調査・修正、差分検証、状態更新、commit、cleanup、report 生成への入口を提供する。

## Read this when
- realization refactor fork の挙動、処理単位、完了条件、commit 単位を確認・変更するとき
- refactor state、unresolved finding、cleanup、report 保存の整合性を確認するとき
- fork の joinable・error・user interruption 遷移や realization file 以外の差分処理を調査するとき

## Do not read this when
- realization refactor の agent 入力パラメータや change summary の schema だけを確認するとき
- 共通 run lifecycle、process tracking、state 永続化、report 基盤の一般挙動だけを確認するとき
- INDEX 更新処理そのものだけを調査するとき

## hash
- a9d17514881d56b62369b8d41ccded2603c5a9b7424370b584376b3822deb327
