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
- realization refactor fork の CLI 実行全体を管理する一時状態共有型の workload 実装。run の作成・初期化・中断/error cleanup・joinable 公開・fork report 保存までの lifecycle を担う。
- refactor state から対象 realization file を選び、file 単位の Codex 調査・修正、変更 path と commit の検証、所見および unresolved 状態の更新、INDEX 同期を処理する。
- 処理完了時には investigation_required と unresolved target の一致を検査し、natural completion または unresolved 付き完了を判定する。変更概要、処理単位、未解決所見、state、cleanup 警告を fork report と終了ログへまとめる。
- realization refactor fork の実行 lifecycle、対象選択後の処理単位、run isolation、refactor state、INDEX 更新、structured output の changed_paths 検証、完了・中断・error report の挙動を確認するための入口である。

## Read this when
- realization refactor fork CLI の実行順序、run state、joinable 公開、fork report、完了条件を変更または調査するとき
- refactor 対象 file の選択、Codex agent call、所見の unresolved 管理、rename 後の state reconcile、処理単位 commit の挙動を確認するとき
- 中断・例外時の Codex child 停止、rollback、error state、report 保存の責務を確認するとき
- refactor state と INDEX refresh による差分検証、agent の commit 禁止、changed_paths の postcondition を調査するとき

## Do not read this when
- realization refactor の一般仕様や CLI 契約だけを確認したい場合は、先に対応する oracle の app specification を読む
- file 単位の agent prompt や finding schema の生成内容だけを調査する場合は、対応する builder 実装へ直接進む
- run の共通 lifecycle、git 差分分類、process tracking など共通機構の詳細だけを確認する場合は、参照されている commons 実装へ直接進む
- INDEX 生成規則そのものや INDEX 更新処理だけを確認する場合は、indexing 関連の仕様・実装へ直接進む

## hash
- 6ba39b1993f25a5d0414bf6899f21d7d3a70cae0410d5388058bca5beae3a83c
