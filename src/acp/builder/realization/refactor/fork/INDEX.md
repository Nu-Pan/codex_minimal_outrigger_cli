# `__init__.py`

## Summary
- `cmoc realization refactor fork` 用 builder adapter という、このパッケージ領域の役割を示す説明ファイル。builder の処理や公開名は定義しない。

## Read this when
- realization refactor fork 配下の builder adapter 群の位置づけを確認するとき。

## Do not read this when
- change summary または file review and fix の builder 処理や parameter 構築を調べるときは、各処理を担う下位モジュールから読む。

## hash
- e2e95e4974cee8956ab6d1e32ba70f20ad2afb6bee161325bbeeb9561c4b4cf5

# `change_summary.py`

## Summary
- refactor fork の変更要約パラメータ builder を acp.builder 側から利用できるようにする互換入口です。

## Read this when
- refactor fork の完了処理が使う変更要約 builder の import 経路を確認するとき。

## Do not read this when
- prompt の内容や commit 範囲など builder 本体の挙動を調べるときは、正本の builder 実装へ進んでください。
- ファイル単位レビュー・修正 builder の利用経路を調べるときは、そちらの adapter を参照してください。

## hash
- c0d7a42b998e37cd0eb58c2bed866165a5efdd716ffffa493db1a14b5780c2d8

# `file_review_and_fix.py`

## Summary
- realization refactor fork のファイルレビュー・修正用 parameter builder を、正本実装から再公開する互換 adapter。import 経路を提供し、このファイル自体には prompt 生成ロジックを持たない。

## Read this when
- ファイルレビュー・修正用 builder の互換 import 経路を利用・確認するとき。

## Do not read this when
- prompt の組み立て、引数の処理、Structured Output schema やレビュー所見の仕様を調べるときは、正本 builder と対応する schema を直接読む。
- commit 範囲の change summary 用 builder を調べるときは、その builder の adapter を読む。

## hash
- a051f806eb19e9b73542f4bde735c17f507b6f008cf69e3c9c6a6b7e8c9d02b3
