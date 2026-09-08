# `cmoc_config.py`

## Summary
- `CmocConfig` と関連する不変データクラスで、リポジトリごとに変わりうる cmoc の設定を集約し、JSON/TOML 共通値、Codex の provider・agent call 設定、並列数、アクセス規定違反時の復旧試行回数を定義する。
- 設定の既定値と、agent call 種別ごとの model provider・model・reasoning effort の対応を確認するための入口。

## Read this when
- cmoc の設定項目や既定値を調べるとき
- Codex CLI の provider-local 設定、agent call ごとのモデル設定、並列数、復旧試行回数を変更・確認するとき

## Do not read this when
- 実際の永続化ファイル `.cmoc/gt/ar/config.json` の生成・同期や人間による調整方法だけを確認したいとき
- 設定を利用する個別の処理の挙動を調べるときは、その処理の実装を直接読む場合

## hash
- cae2f9a6ef429774e14d23af747acc5c54bdb278f5424b3ac4886283407a3908

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
