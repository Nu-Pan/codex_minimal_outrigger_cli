# `__init__.py`

## Summary
- realization のリファクタリング作業を扱うパッケージ。関連するリファクタリング処理への入口となる。

## Read this when
- realization のリファクタリング作業の内容や構成を確認するとき。

## Do not read this when
- realization のリファクタリング以外の処理を確認するとき。

## hash
- d070e139f0ebc38e439ff4bf3b37f76a7a536a3424248e4afcc0525de0573746

# `fork.py`

## Summary
- realization refactor fork の全ライフサイクルを実行する CLI 実装。refactor state の初期化、realization file 単位の agent 調査・修正、差分検証と commit、unresolved 所見の管理、完了判定、joinable/error 状態への更新、fork report の生成を一貫して扱う。
- realization refactor fork の処理フロー、完了不変条件、中断・失敗時の cleanup、state 集計、変更概要・unresolved 所見の report 形式を確認するための入口。

## Read this when
- realization refactor fork の実行フローや処理単位を変更するとき
- refactor state、調査対象の再要求、unresolved finding、完了理由の整合性を調査するとき
- fork の joinable/error 遷移、中断時 rollback、Codex child 停止、report 生成を変更・検証するとき
- realization refactor の差分検証、commit、INDEX 同期の責務を確認するとき

## Do not read this when
- 単一ファイルの調査・修正 agent 呼び出しの詳細だけを変更する場合は、file review and fix の実装を直接読む
- 変更概要の Structured Output パラメータだけを変更する場合は、change summary の実装を直接読む
- 一般的な editing run の共通ライフサイクルや run 状態操作だけを確認する場合は、対応する commons 実装を直接読む

## hash
- 7144dbc0f18b04ba13238ecd3901496bbfeb8a8792752b5b9a87bf07b27cdb60
