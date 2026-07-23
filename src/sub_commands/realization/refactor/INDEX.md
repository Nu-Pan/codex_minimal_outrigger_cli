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
- realization refactor fork の full-cycle CLI 実装。run の初期化、対象ファイル単位の調査・修正、所見と refactor state の同期、commit、完了判定、変更要約、fork report、割り込み・エラー時の cleanup を一つの lifecycle として管理する。

## Read this when
- realization refactor fork の実行フロー、対象選択、処理単位の commit、unresolved 管理、完了条件、report 内容を変更・調査するとき。
- refactor agent の Structured Output 検証や、agent が作成した差分・state・index の整合性を確認するとき。
- realization refactor run の割り込み・例外時における rollback、state 更新、report 保存の挙動を確認するとき。

## Do not read this when
- 通常の realization refactor の仕様や agent prompt の内容だけを確認したいときは、対応する oracle 文書を直接読む。
- refactor state のデータ構造や対象同期処理だけを変更・調査するときは、commons.runtime_refactor の実装を直接読む。
- run の一般的な lifecycle、差分分類、report 共通処理だけを変更・調査するときは、sub_commands.run 配下の各責務モジュールを直接読む。

## hash
- 5109685faac38927aea71882486b8a19c6d54232d65f626313cef27b247ae147
