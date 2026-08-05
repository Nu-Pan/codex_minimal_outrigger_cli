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
- realization refactor fork の全ライフサイクルを実行する CLI サブコマンド実装。run の初期化から対象 file の選択、Codex による調査・修正、差分・commit・state の検証、unresolved 所見の管理、完了判定、joinable/error/interruption report の保存までを一貫して扱う。
- refactor state、INDEX 更新、run worktree、process tracking、Git commit/rollback、変更概要生成など複数の補助機能を連携させる、realization refactor 処理の主要なオーケストレーション入口。

## Read this when
- `cmoc realization refactor fork` の実行フロー、対象 file の処理単位、refactor state の更新、unresolved 所見の扱いを調査または変更するとき。
- fork の正常完了・中断・エラー時における run state、cleanup、rollback、report 生成の挙動を確認するとき。
- agent が作成した差分、changed_paths、commit、INDEX 更新、完了条件の検証ロジックを調査するとき。

## Do not read this when
- 個別の refactor agent 用 Structured Output や prompt builder の仕様だけを確認する場合は、該当する builder 実装を直接読む。
- refactor state のデータ形式や対象選択ロジックだけを確認する場合は、state 管理を担う runtime_refactor 実装を直接読む。
- run の共通ライフサイクル、report 表現、process tracking、INDEX 更新の一般仕様だけを確認する場合は、それぞれの共通 runtime 実装または正本仕様を直接読む。

## hash
- dfa6c077494c737f1de89734761784e94cde51ca03506c8414256b65ff243677
