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
