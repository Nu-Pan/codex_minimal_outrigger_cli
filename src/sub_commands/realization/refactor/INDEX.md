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
- realization refactor fork の一連のライフサイクルを実行する CLI ワークロード。refactor state の初期化、対象ファイル単位の agent 調査・修正、差分検証、commit、未解決所見の current fork 内管理、完了判定、joinable/error report の生成を一体として担う。

## Read this when
- realization refactor fork の実行フロー、処理単位、state 更新、未解決所見、割り込み・エラー時の cleanup、完了条件または report 形式を変更・調査するとき。

## Do not read this when
- realization refactor の対象選択や state 永続化の共通処理だけを調べるときは、該当する runtime_refactor 実装を直接読む。
- file review agent の prompt parameter や change summary の生成仕様だけを調べるときは、各 builder 実装を直接読む。
- editing run の共通ライフサイクルや report writer の一般仕様だけを調べるときは、該当する runtime_run モジュールを直接読む。

## hash
- 53cd5aeb062dbb194995d89befba7d88154fb59a28f1b9695d986b0e6df2db34
