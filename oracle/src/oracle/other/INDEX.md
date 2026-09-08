# `cmoc_config.py`

## Summary
- 開発対象リポジトリごとに変わりうる cmoc 設定をデータクラスとして定義し、並列数、Codex CLI の model provider・agent call 設定、ファイルアクセス規定違反時のリカバリ試行回数を扱う設定モデル。
- Codex CLI 設定の構造や既定値、agent call 種別ごとのモデル・reasoning effort、provider-local 設定を確認・変更するときの入口。設定は JSON/TOML 共通値として表現でき、永続化対象の設定構造を確認する場合にも読む。

## Read this when
- CmocConfig、CmocConfigCodex、CodexCallConfig、CodexModelProviderConfig のフィールドや既定値を確認・変更するとき。
- agent call 種別ごとの Codex CLI 呼び出し設定、model provider 設定、並列数、リカバリ試行回数の扱いを調べるとき。
- config.json の生成・同期や人間による調整に対応する設定モデルの構造を確認するとき。

## Do not read this when
- Codex CLI 呼び出し処理そのものや agent call の実行フローを調べる場合は、呼び出し実装側を直接読む。
- config.json の実際の永続化・生成処理や doctor コマンドの挙動だけを確認する場合は、その処理を定義する対象を直接読む。
- 設定値を利用する個別機能の動作だけを調べ、設定モデルのフィールドや既定値を確認する必要がない場合。

## hash
- 5b8eb2882961f95f73f811c3eaa5648cab07bc46ccbadd7156a8ce22c9a739d8

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
