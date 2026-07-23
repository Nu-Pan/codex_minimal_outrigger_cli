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
- realization refactor fork の一連の処理を担い、対象選択、file 単位の agent 実行、差分検証、refactor state 更新、commit、完了判定、unresolved 管理、joinable/error report 生成までを単一の lifecycle として実装する。
- 中断時の child process 停止・rollback・state 更新・report 保存、および異常時の error state への遷移も扱う。関連する refactor state、editing run、git 差分、report の実装をつなぐ上位 orchestration の入口である。

## Read this when
- realization refactor fork の全体 lifecycle、処理単位の進行、完了条件、unresolved finding の扱いを変更・調査するとき
- agent call 後の差分検証、refactor state 同期、commit、run state、report 生成の連携を確認するとき
- KeyboardInterrupt や処理失敗時の cleanup、rollback、error report の挙動を確認するとき

## Do not read this when
- refactor agent の Structured Output parameter や file review 固有の処理だけを変更・調査するときは、対応する builder または file review module を直接読む
- refactor state のデータ構造や target 同期だけを確認するときは、commons.runtime_refactor を直接読む
- editing run の git 差分分類・state 遷移・report 共通処理だけを確認するときは、対応する commons runtime module を直接読む

## hash
- 073415da4f0872bd8a931bccd3db9fa1b54686d879d18207d9cdc08a1150a06d
