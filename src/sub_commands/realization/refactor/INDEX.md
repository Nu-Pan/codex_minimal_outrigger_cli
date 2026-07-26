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
- realization refactor fork の CLI 実行全体を管理する実装。editing run の開始・初期化、realization file 単位の調査と修正、所見および refactor state の更新、処理単位の commit、完了判定、joinable/error 状態への遷移、fork report の保存までを一つの lifecycle として扱う。
- 中断時やエラー時には追跡中の Codex child process の停止、作業単位の rollback、状態更新、詳細 report の生成を行う。current fork 内で unresolved finding を保持し、未解決対象が残る場合も次の対象へ進める。

## Read this when
- realization refactor fork の CLI lifecycle、対象選択、処理単位の commit、unresolved finding の管理、完了不変条件を変更・調査するとき
- realization refactor の editing run における中断・エラー cleanup、状態遷移、fork report の内容を確認するとき
- refactor state と worktree 差分、INDEX 更新、change summary の連携を追跡するとき

## Do not read this when
- 単一ファイルの調査・修正 agent call の入出力仕様だけを確認したいときは、file review and fix の実装を直接読む
- 変更概要の Structured Output や report の共通保存処理だけを確認したいときは、それぞれの parameter builder または runtime report 実装を直接読む
- realization refactor 以外の editing run や一般的な run join・abandon の仕様だけを調査するとき

## hash
- f954f909a82ef93d227e1381ed8d246e88df581c7b1ada3d695f357468bd18ba
