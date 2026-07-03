# `doc`

## Summary
- cmoc の正本仕様断片のうち、自然言語で書かれた文書群へ進むための領域。アプリケーション全体の外部挙動、branch / worktree モデル、採用しなかった設計案、開発時の横断規則を扱う入口になる。
- 個別の実装構造ではなく、CLI、agent call、状態管理、作業隔離、インデクシング、開発・テスト方針などについて、人間意図に基づく仕様判断を始めるために読む。

## Read this when
- cmoc の利用者向け挙動、サブコマンド仕様、ログ、エラー処理、補完、Codex CLI 呼び出し、Structured Output、retry / resume、run 隔離、セッション状態、apply / fork / join などに関する正本仕様断片を探すとき。
- session branch、run branch、linked worktree、cmoc-managed branch、fork / join commit など、git branch・commit・worktree の cmoc 用語と責務を確認したいとき。
- 機能や workflow の追加時に、過去に検討されたが採用されなかった設計案と、その不採用理由を確認したいとき。
- Python 実装、CLI 構成、共通処理の配置、開発環境、依存追加、pytest による決定論的テストなど、realization code を変更する前の共通開発規則を確認したいとき。
- どの自然言語仕様文書へ進むべきかを、アプリケーション仕様、branch モデル、不採用案、開発規則という観点で切り分けたいとき。

## Do not read this when
- oracle file と realization file の一般的な責務分担、編集権限、品質基準、INDEX.md エントリー作成基準そのものだけを確認したいとき。
- パスキーワードやルート種別の定義そのものを確認したいとき。
- 実装モジュール、テスト、helper 分割、既存関数、現在のテスト期待値など、realization 側の具体的なコード構造だけを調べたいとき。
- 特定サブコマンドや特定の仕様断片の読む先が既に分かっており、その本文から実装・テスト判断を行うだけのとき。
- 採用済み仕様ではなく実装都合だけを確認したいとき、または Codex CLI や LLM の実際の応答品質そのものを評価したいとき。

## hash
- a3b821774f43dc74d64ca71ee581b605c8cf1699fda4023c20e31f30fbc47959

# `src`

## Summary
- AI agent call に渡すパラメータ、完全プロンプト構築、Structured Output schema、設定、パス表記、構造化文書モデルなど、正本実装断片の基礎領域を束ねる入口。
- 用途別の agent call parameter 構築仕様、横断的な prompt 部品、ルートプレースホルダ付きパス解決、規範文書モデル、Markdown レンダリング helper へ進むためのルーティングを担う。

## Read this when
- AI 呼び出しで使う role、summary、goal、prompt 断片、placeholder、モデル設定、reasoning effort、file access mode、出力契約を正本仕様断片から確認または変更したいとき。
- 完全プロンプトの構成順序、静的・動的 prompt 部品、file access rule、routing rule、各種 standard の prompt 注入責務を切り分けたいとき。
- cmoc の設定項目、既定値、永続化境界、リポジトリ別の挙動設定を確認したいとき。
- ルート概念、プレースホルダ付きパス、絶対パス、git worktree との関係を確認したいとき。
- 規範文書を構造化して保持するモデルや、階層化された文章を Markdown として整形する helper を確認したいとき。

## Do not read this when
- CLI 引数解析、git 操作、branch 操作、作業レポート保存、結果集約、表示処理など、サブコマンド全体の実行フローを調べたいとき。
- agent call のプロセス起動、バックエンドが受理する具体的なモデル名への変換、結果処理、エラー処理を調べたいとき。
- 設定の読み書き処理、JSON 変換処理、初期化処理など、正本仕様断片ではなく実装箇所を探しているとき。
- oracle file、realization file、index entry、各 standard、review oracle standard などの品質基準本文や定義そのものを読みたいとき。
- 実装ファイルやテストファイルの現在構造を確認して、具体的なコード変更箇所を探したいだけのとき。

## hash
- 5350b7f74981181688d9ab42765673257c459fcf1de99ea6d39c3437de7bf0e1
