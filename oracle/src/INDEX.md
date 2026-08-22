# `oracle`

## Summary
- oracle 配下の正本仕様・実装構築定義を、agent call、prompt、設定・パス・構造化文書、feedback などの責務領域ごとに案内する最上位の入口。
- acp_builder、feedback、other、prompt_builder の各下位領域へ進む判断基準を提供し、具体的な agent call 構築、feedback 入力契約、共通モデル、prompt 生成規定は対応する下位対象で確認する。

## Read this when
- oracle 配下で調査・変更すべき責務領域を特定するとき
- agent call 構築、prompt 生成、feedback 入力契約、設定・パス・構造化文書のどの下位領域を読むべきか判断するとき

## Do not read this when
- 対象の具体的な処理や仕様が既に特定できており、対応する下位ファイルを直接確認できるとき
- 実行制御や通常の CLI 動作など、oracle 配下の構築定義以外を直接調べるとき

## hash
- cf82a8f8767ac1f839d461b6aee15e794e5a740d6244a749bf12b5e5f18bcf8d
