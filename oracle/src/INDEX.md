# `oracle`

## Summary
- cmoc の agent call 構築、prompt・policy・Structured Output 契約、パスモデル、構造化文書レンダリングを実装する oracle source の最上位入口。
- `acp_builder` は用途別 agent call の起動パラメータと出力契約、`prompt_builder` は共通 prompt と各種 policy、`other` は設定・パス・文書モデル、`feedback` は feedback 入力契約を扱う。

## Read this when
- cmoc の oracle source 全体の責務分担や、agent call 構築・prompt 生成・設定・パス解決・feedback 契約のどの下位領域から調査を始めるか判断するとき。
- agent call の用途別実装、共通 prompt policy、Structured Output 契約、root path placeholder、または構造化 Markdown レンダリングの入口を確認するとき。

## Do not read this when
- 特定の agent call の詳細な起動処理、feedback issue の検証・重複判定、oracle review、realization 追従、session conflict 解消、または TUI の挙動だけを確認したいときは、対応する下位領域を直接読む。
- 設定値の具体的な内容、パス解決の個別規則、prompt policy の詳細、または出力契約の詳細だけを確認したいときは、対応する実装・定義ファイルを直接読む。
- 既存の INDEX.md の内容やルーティング結果だけを確認したいとき。

## hash
- b205cf8713d57b5121f325ea2c5e2e7ebad905f3b1c986947ab4cf355eea3dbc
