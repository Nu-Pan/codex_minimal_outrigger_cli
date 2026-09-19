# `cmoc_config.py`

## Summary
- cmoc のリポジトリ固有設定を集約するデータモデル。並列数、Codex の model provider 設定、agent call 種別ごとの model・推論設定、ファイルアクセス規定違反時のリカバリ試行回数を定義し、設定ファイルへの JSON/TOML 表現を支える。

## Read this when
- cmoc の設定項目や既定値を確認・変更するとき
- Codex CLI の provider、model、reasoning effort を agent call 種別ごとに調整するとき
- 設定値の JSON/TOML 対応やメンバー順序保持の前提を確認するとき
- 並列実行数やファイルアクセス規定違反時のリカバリ回数を調整するとき

## Do not read this when
- 実際の永続化・生成・同期処理の実装を確認したいとき。設定ファイルの読み書きや doctor の挙動を担う対象を直接読むべき
- 個別の agent call の実行フローや TUI、oracle、realization の処理内容を確認したいとき
- 設定値ではなく、既存実装のリファクタリングやテストの内容を確認したいとき

## hash
- ee5b4124d403fce92e2805370de4448ab820c775edd44780be0b71eaf35688be

# `doc_ref_model.py`

## Summary
- 文書参照を、絶対パスの参照先ファイルと任意の安定した参照箇所で表す不変データモデルを定義する。
- 参照先パスと参照箇所の入力条件を検査し、単一参照のインライン Markdown 表記と、複数参照をファイル単位でまとめた Markdown 一覧表記を提供する。
- handoff 本文などで参照情報のデータ構造・妥当性検査・Markdown への変換規則を確認するときの入口となる。

## Read this when
- 文書参照の値がどのようなパス形式・参照箇所形式を要求するか確認したいとき
- 単一または複数の文書参照が Markdown にどう表現されるか確認したいとき
- handoff 本文に渡す参照情報のモデルとレンダリング処理を追跡するとき

## Do not read this when
- 参照情報そのものの意味仕様や handoff 全体の要件を確認したい場合は、先に app_spec の参照情報記述を読むべきとき
- 参照一覧を本文へ配置する上位の handoff builder の見出し・順序・空項目の扱いだけを確認したいとき
- 文書参照を利用する MCP 入力処理や別の呼び出し側の実装だけを調べたいとき

## hash
- 0bff83f413a89dcc2a3f881293a595221ea1012097880bf4661a7af14c949ca5

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
