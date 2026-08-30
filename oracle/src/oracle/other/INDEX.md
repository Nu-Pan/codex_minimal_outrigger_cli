# `cmoc_config.py`

## Summary
- cmoc のリポジトリ固有設定を表す不変データクラス群の定義。並列数、Codex CLI の provider・agent call 設定、oracle review のループ上限を扱う設定モデルへの入口。
- 設定値の既定値と、JSON/TOML 共通値、provider-local 設定、agent call 種別ごとの model・reasoning effort などの構造を確認したいときに読む。

## Read this when
- CmocConfig の項目や既定値を変更・確認するとき。
- Codex CLI の provider 設定、agent call ごとのモデル設定、または oracle review のループ回数の意味を調べるとき。
- config.json へのシリアライズ対象となる設定モデルの構造を確認するとき。

## Do not read this when
- cmoc の具体的な設定ファイル生成・同期処理の実装を調べるとき。
- Codex CLI の呼び出し処理そのものや oracle review の実行ロジックを調べるとき。
- 設定値を利用する個別機能の挙動だけを確認したいとき。

## hash
- b6ba0b8fc08e7f0a5efed0683cc06f9ce170b2b208220b9c20f89b80dc74ecf9

# `path_model.py`

## Summary
- cmoc のパス表記とルートプレースホルダを定義する基盤モデルです。
- agent call の cwd から worktree root と main repository root を導出し、呼び出し全体で共有するパスコンテキストを提供します。
- プレースホルダを絶対パスへ解決する処理と、絶対パスをプレースホルダ表記へ変換する処理を扱います。
- Git metadata や cmoc の配置を探索して、repository・worktree・run の各ルートを特定します。

## Read this when
- agent call のパスコンテキスト、worktree root、main repository root の導出規則を確認するとき。
- {{cmoc-root}}、{{repo-root}}、{{run-root}}、{{work-root}} の解決または変換処理を変更・調査するとき。
- プレースホルダ付き相対パスの入力制約や、Git worktree metadata に基づくルート探索の挙動を確認するとき。

## Do not read this when
- 個別の CLI 機能や realization の実装責務だけを確認したいとき。
- パスモデルを介さない一般的なファイル操作や、対象モジュール以外の仕様を直接調べるとき。

## hash
- 7172c36b342a5b115ebddf8f4731b459a305d57195f24b2e2af448f2caabb628

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
