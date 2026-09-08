# `cmoc_config.py`

## Summary
- cmoc のリポジトリ固有設定を集約する設定データクラスを定義する。
- 並列実行数、Codex CLI の model provider と agent call 別設定、ファイルアクセス規定違反時のリカバリ試行回数を扱う。
- 設定は JSON/TOML 表現を前提とし、永続化される設定構造の入口となる。

## Read this when
- cmoc の設定項目や既定値を確認したいとき
- Codex CLI の provider-local 設定または agent call 種別ごとの model・reasoning effort を確認したいとき
- 設定値の JSON/TOML 表現や設定データクラスの構造を確認したいとき

## Do not read this when
- 設定ファイルの生成・同期を行う doctor 処理を確認したいとき
- 設定を実際に読み込み、Codex CLI 呼び出しへ適用する処理を確認したいとき
- 個別の agent call の実行内容や oracle・realization の処理を確認したいとき

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
- 階層化した文章要素（見出し、タグ付きブロック、コードブロック、構造化ポリシー）を保持し、Markdownへレンダリングするクラスとヘルパー関数を扱う。
- Markdown出力の見出し深度、参照タグ、コードフェンス、空行整理、三重引用文字列のインデント正規化を確認するための入口。

## Read this when
- 構造化された文書ノードの型や保持形式を変更・利用するとき。
- SDHeader、SDTagBlock、SDCodeBlock、SDPolicyのMarkdown変換仕様を確認するとき。
- コード本文中のバッククォート、ポリシー区分、空行やインデントのレンダリング挙動を調査するとき。

## Do not read this when
- Markdown以外の出力形式や、文書構造を生成する呼び出し側の仕様を確認したいとき。
- 対象となる個別のポリシー本文や文書テンプレート自体を直接確認すれば足りるとき。

## hash
- 82108c5a2e45e6a12ccd0fad2e797635f574d6aadbf65031d920a3e3872857f8
