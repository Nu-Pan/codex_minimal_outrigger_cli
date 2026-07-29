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
- realization refactor fork の CLI 実行全体を担当する。run の初期化・process tracking、realization file 単位の調査と修正、差分検証・state 更新・commit、unresolved 管理、完了判定、interruption/error cleanup、fork report と完了ログまでを一貫して扱う。

## Read this when
- realization refactor fork の lifecycle、処理単位、current fork 内の unresolved finding 管理、完了不変条件、run state 遷移を変更または調査するとき
- refactor agent の差分検証、state と INDEX の同期、commit 後の進捗記録、interruption/error 時の rollback・report を確認するとき
- fork report の内容や正常完了・中断・エラー時の出力を変更するとき

## Do not read this when
- refactor 対象 file の個別調査・修正 prompt の生成だけを変更するときは、file review and fix の実装を直接読む
- 変更概要の Structured Output 生成だけを変更するときは、change summary の実装を直接読む
- refactor state の一般的な永続化・target 選択処理だけを変更するときは、runtime refactor の実装を直接読む
- run の共通 lifecycle や report 描画を変更するときは、対応する commons 実装を直接読む

## hash
- 0b0e7166cb7005eecb2c80afb8d63fc76f17e653a9b4199d9b31f5158c40e867
