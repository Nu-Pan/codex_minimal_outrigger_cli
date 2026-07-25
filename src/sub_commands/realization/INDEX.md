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
- realization の apply 処理に関する workload を扱うディレクトリ。apply workload の実装を確認する入口となる。
- `cmoc realization apply fork` の CLI 実行処理を担当し、apply fork の run lifecycle、agent 実行、差分検証、commit、状態遷移、report 保存、失敗時 rollback を扱う。

## Read this when
- realization の apply workload の内容を調査・変更するとき。
- `cmoc realization apply fork` の CLI 挙動、run lifecycle、agent 実行、差分検証、commit、joinable/error state、fork report、失敗時 rollback を調査・変更するとき。

## Do not read this when
- apply workload 以外の処理を扱うとき。
- realization apply agent のプロンプトや起動パラメータ生成だけを扱うとき。
- run 状態管理、差分取得、commit、INDEX 更新、report 生成の共通仕様・実装だけを確認するとき。
- `cmoc realization apply fork` 以外のサブコマンドの CLI 本体を扱うとき。

## hash
- 8fcac3ceac4121ef9caeffdcd6f3f3b6d866432259fc7803d12301b2838d7520

# `refactor`

## Summary
- realization のリファクタリング処理をまとめたパッケージ。リファクタリング関連 CLI の入口と、対象ファイルの調査・修正から完了判定までの処理を扱う。
- refactor fork のライフサイクル全体を実行する CLI 実装。state 管理、realization file の調査・修正、差分検証、commit、所見管理、完了・中断・エラー処理、report 生成を担う。

## Read this when
- realization のリファクタリング機能の構成や入口を確認するときは、まずこのディレクトリを読む。
- refactor fork の実行フロー、state 遷移、agent の調査・修正、差分検証、cleanup、report 生成を変更・調査するときは fork の実装を読む。

## Do not read this when
- realization のリファクタリング以外の処理を確認するとき。
- 単一ファイルの調査・修正 agent の詳細だけを確認するとき。
- 変更概要の Structured Output や一般的な run lifecycle の共通処理だけを確認するとき。

## hash
- 970cfb9d7ce69e19acf82e0d51fba1c941ed4aa6a467d13254ad27a8777ebf9e
