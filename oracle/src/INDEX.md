# `oracle`

## Summary
- cmoc の oracle src を構成する実装群。ACP agent call パラメータ、oracle review・apply・indexing の prompt と Structured Output schema、共通 prompt 規範、設定・パス・構造化文書モデルを扱う。各サブディレクトリは、個別機能の prompt 実装や共通モデルへ進む入口になる。

## Read this when
- oracle src 全体の責務分担や、ACP builder・prompt builder・共通モデルの関係を確認するとき。
- oracle review、apply fork、indexing、session join などの agent call 設定や Structured Output schema の実装を調査するとき。
- cmoc 設定、モデル・推論強度、ファイルアクセス、パス解決、構造化文書変換の実装を確認するとき。

## Do not read this when
- 特定の oracle review 操作、prompt 部品、設定モデル、パスモデルの詳細だけを調べるとき。
- CLI サブコマンドの呼び出し経路や永続化処理など、oracle src 外の上位実装を直接確認すべきとき。
- 既存の Structured Output schema や prompt 本文を変更せず、realization 側の実装だけを調査するとき。

## hash
- 868b694c9695f17727eaa6a3f3b27ddef23f695a4d07e3d6865318228bede101
