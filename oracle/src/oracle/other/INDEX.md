# `cmoc_config.py`

## Summary
- 開発対象リポジトリごとに変わりうる cmoc の挙動設定を集約し、Codex CLI の provider・agent call 設定や並列数、アクセス規定違反時の復旧試行回数を定義する設定モデル。設定の永続化先と JSON シリアライズ時のメンバー順序も説明する。

## Read this when
- cmoc の設定項目、既定値、Codex CLI 呼び出しごとのモデル設定、provider-local 設定、または設定の永続化・編集方針を確認するとき。

## Do not read this when
- agent call のプロンプト生成や実際の CLI 呼び出し処理を調べるとき。設定値を保存・同期する具体的な処理だけを調べる場合は、その処理を実装する対象を直接読む。

## hash
- d6ce4046ae9484f0eebdbb1e9bbc9e0ff6d7243038f8dcf18550fe038f1a67a5

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
- 構造化ドキュメント要素（見出し、参照可能ブロック、コードブロック、規定）を保持し、Markdownへレンダリングするためのクラスと関数を定義する。
- Markdownレンダリング時の見出し深さ、cmoc_block参照タグ、コードフェンス、規定カテゴリ、空行、三重引用文字列の正規化を扱う実装への入口。

## Read this when
- 構造化された自然言語文書をMarkdownへ変換する挙動や、見出し階層・cmoc_block/cmoc_ref・コードブロック・SDPolicyの出力形式を確認したいとき。
- SDHeader、SDTagBlock、SDCodeBlock、SDPolicy、SDNode、render_sd_node_as_markdown、ntqsの責務や利用方法を調べるとき。

## Do not read this when
- Markdown以外の文書形式のレンダリングや、文書構造自体の仕様・入力生成規則を確認したいとき。
- cmocの一般的な規定や参照ルーティングの仕様だけを確認したいときは、まずそれぞれの正本仕様・ポリシー文書を読む。

## hash
- df3cddf6ae11ada0c83f33ecf46283d3e485a68c1383cfcec42ae78cd97f5a18
