# `oracle`

## Summary
- cmoc の agent call 用正本ソースをまとめる領域です。共通パラメータ、用途別の呼び出し条件、Structured Output 連携、prompt 構築、設定・パス・構造化文書モデル、feedback 入力契約を扱います。各機能の prompt builder や構造化モデルの実装へ進む入口です。

## Read this when
- agent call の共通パラメータ、モデル、推論強度、ファイルアクセスモード、作業 root の扱いを確認するとき。
- indexing、oracle review、realization、session join、TUI、feedback など用途別の agent call 構築を調査・変更するとき。
- agent prompt の組み立て、placeholder、oracle・realization の適用規範、Structured Output schema の接続を確認するとき。
- 設定値、パス解決、規範モデル、構造化文書の変換や Markdown レンダリングを調査するとき。

## Do not read this when
- 実際の agent call の実行制御、CLI・TUI の上位フロー、または通常の realization 実装を調査するとき。
- 正本仕様そのものや、feedback の保存・集約・重複判定だけを確認するとき。
- 特定の用途やモデルの詳細が明らかな場合は、この領域全体ではなく該当する下位実装を直接読むとき。

## hash
- f965a5c35f43dfa6f97a364e64b688703b10ff9b12ec7b30ba98e85d4a61f83a
