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
- realization file の refactor fork 全体を実行する単一 workload。editing run を開始し、refactor state と INDEX を初期化した後、対象 file ごとに agent に調査・修正を委譲する。agent の変更、changed_paths、commit、state 更新を検証し、処理単位として commit する。
- current fork 内の unresolved finding、rename、調査要求状態を追跡し、全対象の完了不変条件を検査する。natural_completion または completed_with_unresolved を判定し、変更概要と fork report を保存して run を joinable にする。
- KeyboardInterrupt と予期しない例外では、Codex descendant の停止、rollback、run state 更新、interruption/error report の生成を行う。refactor fork の lifecycle、cleanup、report、完了判定を確認する入口であり、個別 agent prompt や変更概要生成の詳細は import 先へ進む。

## Read this when
- `cmoc realization refactor fork` の開始から joinable 公開までの lifecycle を調査・変更するとき
- realization refactor の target 選択、処理単位、refactor state、current fork 内の unresolved 管理、rename reconciliation、完了判定を確認するとき
- agent の変更 path 検証、agent commit 拒否、INDEX refresh、commit、rollback、Codex descendant cleanup の責務を確認するとき
- realization refactor fork の interruption/error handling、primary report、fork report、completion result を調査するとき

## Do not read this when
- 個別 realization file の調査・修正 agent prompt の内容だけを確認したいときは、file review builder の対象へ直接進む
- refactor の変更概要生成の Structured Output や prompt だけを確認したいときは、change summary builder の対象へ直接進む
- 一般的な run join、run abandon、editing run の共通仕様だけを確認したいときは、対応する app_spec または runtime lifecycle の正本へ直接進む
- INDEX 更新の一般仕様だけを確認したいときは、indexing の正本へ直接進む

## hash
- 052c3307c7dbefebbddca52653c6a5e5d953c35eed2424acbef3e2b33f08c4f7
