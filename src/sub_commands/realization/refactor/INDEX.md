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
- realization refactor fork の full-cycle workload を実装する CLI ランタイム。
- refactor state を初期化・同期し、realization file ごとに agent call、差分検証、所見の記録、再調査要求の更新、commit を実行する。
- current fork 内の unresolved finding を管理し、自然完了または unresolved 付き完了を検証する。
- 中断・エラー時には child process 停止、作業単位 rollback、run state 更新、fork report 保存までを一貫して処理する。
- 正常完了時には変更概要を生成し、処理単位、state 集計、unresolved 所見、変更対象を fork report と CLI 出力へまとめる。

## Read this when
- realization refactor fork の実行フロー、処理単位、完了条件を変更・調査するとき
- refactor state と unresolved finding の同期・判定ロジックを確認するとき
- realization refactor における agent call 後の差分検証や commit 方針を確認するとき
- fork の中断処理、エラー処理、run state、report 保存の挙動を確認するとき

## Do not read this when
- realization refactor の agent call パラメータ生成だけを変更・調査するときは、file review 用 builder を直接読む
- 変更概要の Structured Output 生成だけを変更・調査するときは、change summary 用 builder を直接読む
- 共通の editing run lifecycle、refactor state、process tracking、report 生成の実装を調査するときは、それぞれの共通 runtime module を直接読む

## hash
- c816da04aac2e0f4db4d80c2cf8db78b1d12c353cf1ea39f27166d982f3e4df9
