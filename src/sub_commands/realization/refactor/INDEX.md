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
- realization refactor fork の full-cycle CLI workload を実装する。run の初期化、realization target の選択、target 単位の調査・修正・commit、current fork 内の unresolved 管理、完了状態の検証、change summary と fork report の生成を一つの lifecycle として扱う。
- 中断時・例外時には追跡中の Codex child 停止、作業単位 rollback、run state 更新、error/interruption report 生成までを担う。refactor state、worktree 差分、agent 出力の整合性も検証する。

## Read this when
- realization refactor fork の CLI 実行フロー、target 処理ループ、unresolved finding の扱い、完了判定を変更・調査するとき。
- realization refactor の中断・エラー時 cleanup、run state、fork report、change summary の連携を確認するとき。
- refactor state と worktree 差分、Codex agent の Structured Output の検証不備を調査するとき。

## Do not read this when
- realization refactor の target 選択や state 同期そのものだけを変更する場合は、commons.runtime_refactor の実装を先に確認する。
- file 単位の調査・修正 agent の prompt 構築だけを変更する場合は、refactor fork の builder 実装を直接確認する。
- 一般的な run lifecycle、report 出力、process tracking の共通実装だけを変更する場合は、それぞれの専用 module を直接確認する。

## hash
- c4ccf7fc653fe4f59e192ae0478cfddc4bda00c77637d7894a7dae5d228d70ff
