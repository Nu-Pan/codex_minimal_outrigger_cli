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
- realization refactor fork の full-cycle workload を実行し、run の初期化から対象 file の調査・修正、完了判定、joinable 化、fork report 保存までを一貫して管理する。
- 各処理単位で agent の変更、findings、unresolved 状態、refactor state、commit を検証・同期し、中断時やエラー時の rollback、run state 更新、report 保存も扱う。

## Read this when
- realization refactor fork の lifecycle、処理単位の進捗、unresolved findings の管理、完了理由、変更概要、interruption/error cleanup の挙動を確認するとき。
- agent が realization file と changed_paths、git commit、INDEX refresh に関して満たすべき検証境界を確認するとき。

## Do not read this when
- realization refactor の対象選択や state の基本形式だけを確認したいときは、refactor state を管理する対象を直接読む。
- run の join、abandon、共通の editing run lifecycle、または一般的な INDEX 更新仕様だけを確認したいときは、それぞれの共通 runtime や oracle specification を直接読む。

## hash
- 7a4447331aa882f043d96b4ae3177c81a12bb66d1367b691eee6dda4b918ddae
