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
- realization refactor fork の CLI 実行ライフサイクルを管理する実装。run の初期化、対象 file の選択・agent call・差分検証・commit、refactor state と unresolved finding の追跡、完了判定、joinable/error/interruption report の生成までを一体として扱う。

## Read this when
- realization refactor fork の処理順序、run isolation、処理単位の commit、agent 差分検証を変更または調査するとき
- refactor state の investigation_required と current fork の unresolved 状態の整合性、完了理由、report 内容を変更または調査するとき
- 中断・例外時の Codex child 停止、rollback、run state 更新、error report の挙動を変更または調査するとき

## Do not read this when
- realization refactor の state 同期や target 選択だけを調査する場合は、対応する commons の runtime 実装を直接読む
- agent への入力 parameter の構築や change summary の生成だけを調査する場合は、各 builder 実装を直接読む
- 一般的な run lifecycle や report 表示の共通仕様だけを確認する場合は、対応する commons モジュールまたは oracle 文書を直接読む

## hash
- d447a6c01903e362b06d60f1b6e6ec93db8805cfd7da998208a83f551e759867
