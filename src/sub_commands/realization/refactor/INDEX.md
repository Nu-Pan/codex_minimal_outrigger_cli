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
- realization refactor fork の CLI 実行ライフサイクル全体を担う実装。refactor run の初期化、対象ファイルごとの agent 調査・修正、差分と commit の検証、state と unresolved finding の同期、完了・中断・エラー処理、fork report の生成までを一貫して管理する。
- 対象ファイルの調査・修正処理や refactor fork の完了条件、run isolation、report 内容を変更・確認するときの実装入口であり、個別の agent parameter や共通 runtime 処理そのものを読むだけなら下位依存先へ直接進む。

## Read this when
- realization refactor fork サブコマンドの実行順序、状態遷移、処理単位、commit 境界を調査するとき
- refactor target の選択、unresolved finding の current fork 内管理、rename 後の state 同期、完了判定を変更・検証するとき
- 中断・例外時の child process 停止、rollback、run state 更新、error/interruption report の挙動を調査するとき
- fork report の change summary、state 集計、completion log の生成内容を変更・確認するとき

## Do not read this when
- file review agent の prompt や Structured Output parameter の仕様だけを確認したい場合は、個別の builder 実装を直接読む
- refactor state のデータ構造や target 同期処理だけを確認したい場合は、commons の runtime refactor 実装を直接読む
- run の共通 lifecycle、git 差分分類、process tracking の一般仕様だけを確認したい場合は、commons の対応する runtime 実装や正本仕様へ進む
- INDEX 更新処理そのものの仕様だけを確認したい場合は、indexing 関連の実装・正本仕様を直接読む

## hash
- 8184329644a7dc12da8482390aa4e29788d836a638d0b2e5a5ded29cab494923
