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
- realization refactor fork の full-cycle CLI workload を実装するエントリー処理。run の初期化、対象 realization file の選択、Codex による調査・修正、差分と所見の検証、refactor state の更新、処理単位の commit、unresolved 管理、完了判定、joinable/error/interruption 時の cleanup と report 保存までを一貫して扱う。
- realization refactor fork のライフサイクルと、run worktree・process tracking・INDEX 更新・Git commit の整合性を確認するための主要な実装入口である。個別の所見生成や change summary の詳細は、呼び出される builder や report 実装を直接読む。

## Read this when
- realization refactor fork の CLI 挙動、対象選択から完了までの処理フローを調査・変更するとき
- Codex agent の差分検証、agent commit の拒否、rename、refactor state、unresolved finding の整合性を確認するとき
- 正常完了・ユーザー中断・例外発生時の run state、rollback、child process 停止、report 保存を調査するとき

## Do not read this when
- 個別の refactor agent prompt や change summary の Structured Output 定義だけを確認したいときは、対応する builder を直接読む
- 一般的な editing run の仕様、run isolation、INDEX 更新規則だけを確認したいときは、参照コメントが示す oracle 仕様を直接読む
- fork report の Markdown 表現や共通 report 書き込み処理だけを確認したいときは、report 実装を直接読む

## hash
- 8d08d96f613134db333003e15018a12b1fac6bccd56424e761da79f2c59f7449
