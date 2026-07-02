# `doc`

## Summary
- cmoc の正本仕様ドキュメント群を置く領域であり、アプリケーション仕様、branch/worktree モデル、採用しなかった代替案、開発規則など、自然言語で書かれた oracle doc への入口になる。
- 利用者向け外部挙動、git branch / worktree の概念、設計判断の背景、realization code の開発基準などを、下位領域や個別文書ごとに分けて扱う。

## Read this when
- cmoc の仕様を自然言語の正本仕様断片から確認したいとき。
- CLI 挙動、サブコマンド仕様、Codex CLI 呼び出し、ログ、エラー、セッション状態、INDEX.md 自動生成、run 隔離などのアプリケーション仕様文書へ進む入口を探すとき。
- session fork / join、cmoc-managed branch、run branch、linked worktree、fork / join commit などの git branch / worktree モデルを確認したいとき。
- 採用されなかった設計案の背景や、不採用理由を確認して、自然に見える代替案を再導入してよいか判断したいとき。
- Python 実装、CLI 構成、開発環境、pytest 方針など、realization code を追加・変更する前の横断的な開発規則を確認したいとき。

## Do not read this when
- oracle file と realization file の一般的な責務分担、編集権限、品質基準、INDEX.md エントリー生成基準そのものを確認したいだけのとき。
- パスキーワードやルートディレクトリ概念そのものの定義だけを確認したいとき。
- 現在の実装ファイル、テストファイル、既存関数、内部 helper、依存関係など realization code の具体構造を調べたいとき。
- 既に読むべき個別の正本仕様文書や下位領域が特定できており、その本文を直接読む方が早いとき。

## hash
- 70d66840404497d3494dcf52385a33c7ce77c82bd116110b178b148893699d30

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
