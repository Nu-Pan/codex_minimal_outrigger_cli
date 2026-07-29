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
- realization refactor fork の CLI 実行全体を管理する単一 workload。run の初期化、realization file 単位の agent 調査・修正、差分検証、refactor state 更新、処理単位 commit、unresolved finding 管理、完了判定、joinable/error report 保存までを担当する。
- 中断・異常終了時には Codex 子プロセス停止、rollback、run state 更新、進捗と cleanup warning を含む report 生成を行う。

## Read this when
- realization refactor fork のライフサイクル、処理単位の選択・commit、unresolved finding の扱い、完了条件を変更または調査するとき
- refactor state と run worktree の差分検証、INDEX refresh、Codex descendant の停止、joinable/error report の連携を確認するとき
- realization refactor fork の正常完了・ユーザー中断・異常終了時の出力や状態遷移を追跡するとき

## Do not read this when
- 単一 realization file の調査・修正ロジックだけを確認したい場合は、file review 用の下位実装を直接読む
- refactor fork の変更概要生成だけを確認したい場合は、change summary 用の下位実装を直接読む
- 一般的な run isolation、editing run、INDEX 更新、refactor state の仕様を確認したい場合は、対応する oracle 文書や共通 runtime 実装を先に読む

## hash
- 9d8390051c495b3bcd5f4af399b66b342b4dc86491a45daedf82eb39e7a9c187
