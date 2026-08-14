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
- 対象は `cmoc realization refactor fork` の一連の実行ライフサイクルを管理する入口です。run の初期化、refactor state と INDEX の同期、realization file 単位の調査・修正、差分・commit・子 process の検証、unresolved finding の追跡、完了判定、interruption/error cleanup、joinable run の公開と fork report 保存を一つの進捗状態で扱います。realization refactor fork の挙動、処理単位の進行、完了条件、run isolation、report 内容を確認・変更するときの入口です。
- 対象 file 内の個別 agent prompt、change summary、file review、共通 run lifecycle、refactor state、report の実装詳細だけを調べる場合は、それぞれの専用 builder・runtime helper・oracle/spec を直接参照してください。

## Read this when
- `cmoc realization refactor fork` の CLI 実行フローや lifecycle を調査・変更するとき
- refactor target の選択から file 単位の agent call、state 更新、commit、次 target への遷移を確認するとき
- unresolved finding の current fork 内管理、rename 後の追跡、完了理由の判定を確認するとき
- Ctrl+C、agent failure、cleanup failure、error/joinable state、fork report の生成を確認するとき
- realization refactor fork における想定外差分、agent commit、INDEX refresh、run worktree isolation の検証を確認するとき

## Do not read this when
- 個別の realization file review 用 agent prompt や change summary 用 agent prompt の内容だけを確認するときは、対応する builder を直接読む
- 共通の run 作成・commit・rollback・process tracking・report rendering の仕様や実装だけを確認するときは、対応する runtime helper または oracle/spec を直接読む
- INDEX 更新の一般規則や realization refactor 全体の永続 state 契約だけを確認するときは、対応する indexing/refactor state の仕様を直接読む

## hash
- d7d4f2fbc55e7043aa6aa3dc2747dfe8b276a51ee30ebc4a526b922e4d7cda02
