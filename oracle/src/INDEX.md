# `oracle`

## Summary
- AI agent call に渡すパラメータ、完全プロンプト構築、Structured Output schema、設定・パス表記・構造化文書モデルなど、正本実装断片の基礎領域を束ねる入口。
- 用途別の agent call parameter 構築仕様、横断的な prompt 部品、ルートプレースホルダ付きパス解決、規範文書モデル、Markdown レンダリング helper へ進むためのルーティングを担う。

## Read this when
- AI 呼び出しで使う role、summary、goal、prompt 断片、placeholder、モデル設定、reasoning effort、file access mode、出力契約を正本仕様断片から確認または変更したいとき。
- 完全プロンプトの構成順序、静的・動的 prompt 部品、file access rule、routing rule、各種 standard の prompt 注入責務を切り分けたいとき。
- cmoc の設定項目、既定値、永続化境界、リポジトリ別の挙動設定を確認したいとき。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` などのルート概念、プレースホルダ付きパス、絶対パス、git worktree との関係を確認したいとき。
- 規範文書を構造化して保持するモデルや、階層化された文章を Markdown として整形する helper を確認したいとき。

## Do not read this when
- CLI 引数解析、git 操作、branch 操作、作業レポート保存、結果集約、表示処理など、サブコマンド全体の実行フローを調べたいとき。
- agent call のプロセス起動、バックエンドが受理する具体的なモデル名への変換、結果処理、エラー処理を調べたいとき。
- 設定の読み書き処理、JSON 変換処理、初期化処理など、正本仕様断片ではなく実装箇所を探しているとき。
- oracle file、realization file、index entry、各 standard、review oracle standard などの品質基準本文や定義そのものを読みたいとき。
- 実装ファイルやテストファイルの現在構造を確認して、具体的なコード変更箇所を探したいだけのとき。

## hash
- 131c99457642dc05ca605a1debcb0f487ca5b5a3c2e6411158e29c92c57be4d1
