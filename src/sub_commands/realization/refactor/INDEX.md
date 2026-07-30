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
- realization refactor fork の CLI 実行ライフサイクル全体を管理する workload。refactor state の初期化、対象 file ごとの agent 調査・修正、差分と commit の検証、unresolved 所見の追跡、完了判定、fork report の保存までを一つの処理単位として扱う。
- 通常完了・ユーザー中断・エラーの各経路で、run state、子プロセス、worktree、report を整合させる。realization file 以外の想定外変更、agent による commit、state と unresolved 集合の不一致を検出して拒否する。

## Read this when
- realization refactor fork サブコマンドの実行順序、対象選択、処理単位、commit、完了条件を変更または調査するとき
- refactor state と current fork 内の unresolved findings の対応、rename 後の追跡、report 内容を確認するとき
- fork の中断・エラー cleanup、Codex 子プロセス停止、run state 更新、worktree rollback の挙動を確認するとき
- realization refactor の差分検証、INDEX refresh、change summary、completion log の実装を確認するとき

## Do not read this when
- realization refactor の agent parameter 構築そのものを変更または調査する場合は、対応する builder file を直接読む
- refactor state のデータ構造や対象同期処理を変更または調査する場合は、commons の refactor state 実装を直接読む
- run の一般的な isolation・lifecycle・report 共通処理を変更または調査する場合は、対応する commons runtime module と oracle specification を直接読む
- refactor fork の利用者向け仕様だけを確認する場合は、対応する oracle の subcommand 仕様を先に読む

## hash
- 14b2d055b47573245628146d5f1f68a08fcebb7b5492f622b63922c535dc9d12
