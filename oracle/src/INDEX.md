# `oracle`

## Summary
- cmoc の oracle 定義をまとめる領域。agent call のパラメータ、feedback 入力契約、設定・パス・構造化 Markdown の共通モデル、完全 prompt の構築を扱う。
- agent call や prompt の構成を調査・変更する際の上位入口であり、共通モデルや機能別定義は対応する下位ディレクトリへ進んで確認する。

## Read this when
- oracle 配下の agent call パラメータ、prompt、feedback、設定、パスモデル、構造化文書の責務を横断して把握するとき
- 特定機能の定義を探す入口を判断するとき

## Do not read this when
- 実際の CLI 実行制御、realization 実装、oracle 文書など、oracle/src/oracle 配下にない責務を調査するとき
- 個別ファイルの実装やスキーマだけを確認すれば足りるときは、対応する下位要素を直接読む

## hash
- d6aabd34f1b05a4663f5699b41f61f19be309b49481cf284bf7774fe880615b4
