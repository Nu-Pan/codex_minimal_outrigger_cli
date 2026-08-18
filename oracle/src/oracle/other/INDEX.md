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
- 構造化された文書ノード（見出し、タグ付きブロック、コードブロック、規定、文字列）を保持し、Markdownへレンダリングするヘルパーを提供する。
- 見出し階層の深さを自動的に計算し、タグ付き参照ブロック、バッククォートを含むコードブロック、規定リスト、三重引用文字列のインデント正規化を扱う。
- 文書生成やMarkdownレンダリングの実装を確認する際の入口であり、個別ノードの構造・参照タグ・出力整形の挙動を調べるために読む。

## Read this when
- 構造化文書をMarkdownへ変換する処理を変更または調査するとき
- 見出し深度、cmoc_block/cmoc_ref、コードフェンス、規定リスト、空行やインデント正規化の出力を確認するとき
- SDHeader、SDTagBlock、SDCodeBlock、SDPolicy、ntqsの責務や相互関係を確認するとき

## Do not read this when
- Markdown以外の文書形式の処理を調べるとき
- CLIの入出力や文書生成の呼び出し元だけを確認したいとき
- 対象ノードの利用箇所やテストの具体例を直接確認することが目的のとき

## hash
- 34a56b18f581521595f61712d637b7005649d736d28e030acaad2fe0e2b90eb8
