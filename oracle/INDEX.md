# `doc`

## Summary
- cmoc の自然言語で書かれた正本仕様断片を集めた領域。アプリケーション仕様、branch/worktree モデル、不採用設計案、開発規則など、実装差を避けたい判断や利用者向け挙動、開発時の規約への入口になる。
- 機能仕様、git 上の作業隔離モデル、設計判断の背景、realization code/test の書き方を、責務ごとの下位領域へ絞り込むために読む。

## Read this when
- cmoc の実装・テスト・設計判断で、自然言語の正本仕様断片から根拠を探したいとき。
- CLI 挙動、LLM 実行、補完、ログ、doctor preprocess、indexing、run 隔離、session state、managed ollama、外部 provider、サブコマンド仕様などのアプリケーション仕様へ進みたいとき。
- session fork/join、apply/review などの run が扱う branch、commit、worktree、managed branch の意味や命名規則を確認したいとき。
- 過去に不採用となった設計案の背景や、再検討時に避けるべき理由を確認したいとき。
- Python 実装、CLI 構成、開発環境、pytest を中心とした realization code/test の開発規則を確認したいとき。

## Do not read this when
- oracle file と realization file の一般的な定義、責務境界、編集権限、品質基準、INDEX.md エントリー生成規則だけを確認したいとき。
- パスキーワードやルート種別の定義だけを確認したいとき。
- 実装ファイルの内部構造、既存関数、テスト配置、具体的な realization code の詳細だけを調べたいとき。
- 特定の正本仕様断片や対象機能が既に分かっているときは、この領域全体ではなく該当する下位領域または個別仕様を直接読む。

## hash
- 2b5cf67e41557e6dbb33afb3da0d76c1658b6ca40bc8d4f037a2eb35e7e40545

# `src`

## Summary
- cmoc の正本実装断片を扱う領域。AI agent call parameter、prompt 構築、リポジトリ設定、パス表記、規範データ構造、Markdown レンダリングなど、複数の realization 実装が参照する横断的な仕様断片への入口になる。
- CLI サブコマンドの実行制御そのものではなく、agent call の入力契約・出力契約、共通プロンプト部品、横断的な補助概念を確認するためのまとまり。

## Read this when
- cmoc が AI agent call に渡す prompt、Structured Output schema、モデル設定、reasoning effort、cwd、ファイルアクセス権限、preflight 設定を確認したいとき。
- agent call 用プロンプトの構築順序、静的部分と動的部分の分離、ファイルアクセス規則や各種標準文書の注入方法を確認したいとき。
- リポジトリ別設定、ルートパスプレースホルダ、正本文書モデル、構造化文書から Markdown へのレンダリング helper など、横断的な正本実装断片を探すとき。
- INDEX.md エントリー生成、oracle file レビュー、fork 適用後レビュー、session join の conflict marker 解消、TUI 起動前後の agent call parameter 選定に関する正本仕様断片を確認したいとき。

## Do not read this when
- CLI 引数処理、branch 操作、diff 取得、merge 実行、保存処理、表示整形など、サブコマンドの実行制御実装を直接調べたいとき。
- oracle file と realization file の管理方針、文書品質基準、レビュー基準などの標準文書本文だけを確認したいとき。
- バックエンド API へ送る実際のリクエスト形式、具体的なモデル名解決、agent CLI 実行処理など realization implementation 側の詳細を調べたいとき。
- 実装ファイルやテストファイルの現在構造を把握して直接修正したいだけで、正本実装断片や prompt 生成に関係しないとき。

## hash
- 7564c7161e90ebc5984671d2f8fa985758094269a783deb5db927d6a53cfdd43
