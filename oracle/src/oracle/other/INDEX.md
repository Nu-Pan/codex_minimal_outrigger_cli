# `cmoc_config.py`

## Summary
- 開発対象リポジトリごとに異なる cmoc の挙動設定を集約する設定データモデル。JSON/TOML 共通値、Codex の provider・agent call 設定、oracle review のループ上限を扱う。
- 設定値の既定値と構造を確認したいときの入口であり、`config.json` の生成・同期・人手調整に対応する構成を理解するために読む。

## Read this when
- CmocConfig の項目、既定値、Codex CLI 呼び出し設定、model provider 設定を変更または確認するとき。
- `cmoc oracle review` の列挙・マージ・検証ループ上限を調整するとき。
- 設定クラスを JSON/TOML にシリアライズする構造や、永続化される config.json との対応を調べるとき。

## Do not read this when
- agent call のプロンプト生成や個別の Codex 呼び出し処理そのものを調べる場合は、直接その実装を読む。
- oracle review の所見生成・検証ロジックの挙動を調べる場合は、ループ設定ではなく該当する review 実装を直接読む。
- 永続化ファイルの実際の内容だけを確認する場合は、生成された config.json を直接読む。

## hash
- 39a62379f22af3b1e8547a6f499bc01750671c294099d12f46633d04200396bd

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
