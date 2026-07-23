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
- realization refactor fork の一連の CLI 処理を実行する中核モジュール。refactor run の初期化、対象 realization file ごとの agent 調査・修正、差分検証と commit、未解決所見の管理、完了判定、joinable/error 時の report 保存までを同じ lifecycle 状態で扱う。

## Read this when
- realization refactor fork の実行フロー、対象選択、処理単位の commit、未解決所見、完了条件、または fork report の挙動を変更・調査するとき。
- realization refactor 実行中の中断・cleanup failure・error state の処理を確認するとき。

## Do not read this when
- realization refactor の agent parameter の構築内容だけを確認したいときは、関連する parameter builder を直接読む。
- refactor state のデータ操作だけを確認したいときは、state 管理用の共通モジュールを直接読む。
- 一般的な run lifecycle、git 差分分類、または report 共通処理だけを確認したいときは、それぞれの共通 lifecycle/report モジュールを直接読む。

## hash
- 7c51238797398f091b7cf0c831aec82acf68b9c7c4c92ad362e698c622c09193
