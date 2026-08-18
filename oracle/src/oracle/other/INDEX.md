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
- 構造化された文書ノード（見出し、参照可能なタグブロック、コードブロック、規定文章、文字列）を保持し、Markdownへレンダリングするヘルパーを提供する。
- Markdown見出しの深さを階層から自動計算し、タグブロックの参照タグ生成、コードフェンスの安全な生成、空行・インデントの正規化を扱う。
- 構造化文書の生成・Markdown変換・`cmoc_block`/`cmoc_ref`形式の扱いを確認する際の入口となる。

## Read this when
- 構造化された文章をプログラム上で組み立ててMarkdownへ変換する処理を変更・調査するとき。
- 見出し階層、参照可能な文書ブロック、埋め込みコードブロック、規定文章のレンダリング挙動を確認するとき。
- Markdownコードフェンス、空行、Triple quoted stringの正規化に関する挙動を確認するとき。

## Do not read this when
- INDEX.mdのルーティング規則や文書全体のナビゲーションを確認したいとき。
- 構造化文書の利用側の仕様や呼び出し元の責務を確認したいときは、まずその利用側の対象を直接読む。
- Markdown以外の出力形式や、構造化文書モデル以外の一般的な文章処理を調査するとき。

## hash
- 090f3ef760a292b680b3d919454e8b83bc56f66ff7f607294fb478091953ac36
