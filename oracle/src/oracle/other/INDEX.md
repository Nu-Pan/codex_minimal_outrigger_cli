# `cmoc_config.py`

## Summary
- 日本語技術文書のルーティングエントリー生成のため、指定された本文を根拠に対象の責務と入口を簡潔に整理します。

## Read this when
- CmocConfig とそのネストした設定データクラスの責務、既定値、JSON/TOML 表現、Codex CLI や oracle review の設定項目を確認したいとき。
- 開発対象リポジトリ固有の cmoc 設定がどのように集約され、永続化・同期されるかの入口を確認したいとき。

## Do not read this when
- 設定クラスの具体的なフィールド定義や既定値を直接確認したいときは、このルーティング情報ではなく対象本文を読むべきです。
- agent call の生成規則や index エントリー生成処理そのものを確認したいときは、別の仕様・実装対象を直接読むべきです。

## hash
- 4fcdbcad0a81da47e5d8298b116d3e3f6fa6a2c08d0a9c53a08a2898ef2ba25e

# `path_model.py`

## Summary
- cmoc におけるパス表記、ルートプレースホルダー、agent call 単位のパスコンテキストを定義するモジュール。
- `AgentCallPathContext` により agent call の cwd から work root と repository root を導出し、プレースホルダーと実パスの相互変換を提供する。
- ルート解決、実パス解決、プレースホルダー変換の挙動や、Git worktree を基準にしたパス境界を確認するための入口となる。

## Read this when
- パスを `{{repo-root}}`、`{{work-root}}`、`{{run-root}}`、`{{cmoc-root}}` 形式で扱う実装や仕様を変更・調査するとき。
- agent call の cwd、worktree、main repository の対応関係や、パスコンテキストの導出規則を確認するとき。
- プレースホルダー付きパスと絶対パスの解決・変換処理を確認するとき。

## Do not read this when
- 特定の CLI 機能や oracle 文書の内容だけを調べ、パス解決・worktree 境界・プレースホルダー変換に関係しないとき。
- 実装ではなく、既存の INDEX.md のルーティング情報だけを確認するとき。

## hash
- 1a839609f52bd2ae5d493f18d80e141471f0b0ca4961f329baac2c4849fc85d0

# `struct_doc.py`

## Summary
- 構造化された文書要素を保持し、Markdownへレンダリングするヘルパークラスと関数を定義する。見出し、参照可能なタグブロック、コードブロック、規定文を扱い、見出し深度・コードフェンス・空行・三重引用文字列を自動整形する。文書生成やMarkdownレンダリングの挙動を確認・変更する際の入口となる。

## Read this when
- 構造化文書をMarkdownへ変換する処理を調査・変更するとき
- 見出し深度、cmocブロック参照、コードフェンス、規定文のレンダリング仕様を確認するとき
- ntqsや空行圧縮など、レンダリング前後の文字列整形を扱うとき

## Do not read this when
- Markdown以外の出力形式や、構造化文書の利用側の処理だけを調べるとき
- 文書要素の具体的な内容や正本仕様を確認する必要があり、別の仕様・呼び出し元を直接読むべきとき

## hash
- 1dba895a9a9af7a3d54a386f00858ff02ff58ef1cd79646d7c14f952b89c80ff
