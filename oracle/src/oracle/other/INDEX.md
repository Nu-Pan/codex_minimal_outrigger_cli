# `cmoc_config.py`

## Summary
- cmoc のリポジトリ固有設定を表すデータモデル。Codex CLI のモデル・推論設定、AI 呼び出しの並列数、ファイルアクセス違反時のリカバリ回数、oracle review の各ループ上限を定義する。設定の JSON/TOML 表現や既定値の構成を確認する入口でもある。

## Read this when
- cmoc の設定項目を追加・変更するとき
- Codex CLI のモデル、provider-local 設定、推論 effort、リカバリ試行回数の扱いを確認するとき
- `cmoc oracle review` の所見列挙・マージ・検証ループの設定を確認するとき
- 設定のシリアライズ規則や既定の設定構造を確認するとき

## Do not read this when
- Codex CLI の呼び出し処理そのものや CLI 実装の責務を確認したいとき
- `cmoc oracle review` のレビュー処理の実装や所見生成ロジックを確認したいとき
- 設定ファイルの実際の保存内容や人間による調整結果だけを確認したいとき

## hash
- 8b7d86400aa658565b80abc2ecd33aa4f7b0af8d9a43f907cd939972cc422efd

# `path_model.py`

## Summary
- cmoc におけるパス表記と、agent call の作業ルート・リポジトリルートを扱う正本モデル。root placeholder の定義、placeholder と実パスの相互変換、Git worktree からの各ルート解決を提供する。パスの解決規則や agent call のパスコンテキストを確認・変更する作業では、この対象を入口にする。

## Read this when
- root placeholder の意味や `{{repo-root}}`・`{{work-root}}`・`{{run-root}}` の解決規則を確認するとき
- agent call の cwd から worktree root や repository root を導出する処理を変更するとき
- placeholder 表記と実際の絶対パスの変換処理を確認・変更するとき

## Do not read this when
- 特定の CLI 機能や realization の責務配置だけを確認する場合
- パスモデルを利用する個別機能の挙動を確認する場合は、その機能の実装や仕様を直接読むべきとき

## hash
- 8fc522d7e3ef8f4b608c64102a5f4a6d7eb7cf64422cd3c3f7b239dab4255418

# `struct_doc.py`

## Summary
- 階層構造を保持する見出し・タグブロック・コードブロック・規定文などのノードを定義し、Markdown 文章へ再帰的にレンダリングするヘルパーを提供する。Markdown 見出しの深さ、タグ参照、コードフェンス、空行、インデント付き三重引用文字列の正規化を扱う実装の入口である。

## Read this when
- 構造化された文書を Markdown として生成する処理を変更・調査するとき。
- SDHeader、SDTagBlock、SDCodeBlock、SDPolicy、SDNode、または各種レンダリング・正規化関数の挙動を確認するとき。
- Markdown 見出し深度の自動計算、参照可能な cmoc ブロック、コードフェンスの安全な生成を扱うとき。

## Do not read this when
- Markdown 以外の出力形式や、構造化文書ノードを利用する上位のプロンプト生成処理だけを確認するとき。
- 文書構造の正本仕様や CLI の責務を確認することが目的で、レンダリング実装の詳細を調べる必要がないとき。

## hash
- a4d994e70c1be362c2450b3f0a32c49298e27fcf3549cdd7083213fe5f11e1aa
