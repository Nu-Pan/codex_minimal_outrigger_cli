# `oracle`

## Summary
- cmoc の oracle 正本を扱う実装領域で、agent call 構築、prompt・policy 生成、パス解決、構造化文書、editor handoff、feedback 入力契約などの基盤を提供する。
- oracle に関する呼び出しパラメータ、入力スキーマ、prompt 部品、ファイルアクセス制約、パスコンテキスト、Markdown 構造化モデルを調べるための下位入口。

## Read this when
- oracle の agent call や TUI・編集・調査・レビュー処理の構築定義を確認するとき。
- oracle 関連 prompt、policy、入力スキーマ、アクセスモード、作業パス解決の実装を探すとき。
- oracle を含む構造化文書のモデルや Markdown レンダリングの挙動を確認するとき。

## Do not read this when
- oracle ファイルそのものの具体的な内容や編集手順を確認したいときは、対象の正本ファイルや専用処理を直接読む。
- realization、feedback の収集・受付処理、または Codex CLI の共通実行挙動だけを調べるとき。

## hash
- 7dd58b5536ac78fa779bdfa19789e1f95a6b7d64447b04ef07d412e12e3ab4c3
