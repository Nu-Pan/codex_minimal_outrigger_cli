# `doc`

## Summary
- cmoc の正本仕様断片のうち、自然言語で書かれた文書群を集める領域。アプリケーション仕様、branch/worktree モデル、不採用設計案、開発規則など、実装前に読むべき仕様文書への入口になる。
- 外部挙動や横断仕様、git branch と worktree の概念、開発・テスト方針、過去に退けた代替案を切り分けて確認するためのルーティング対象である。

## Read this when
- cmoc の仕様を自然言語の oracle doc から確認し、対象がアプリケーション仕様、branch/worktree モデル、開発規則、不採用設計案のどれに属するかを選びたいとき。
- CLI 挙動、サブコマンド、状態遷移、ログ、エラー処理、Codex CLI 連携などの外部仕様や横断仕様を探すとき。
- session fork/join、run worktree、managed branch など、cmoc の git branch・commit・worktree モデルを確認したいとき。
- Python 実装、CLI 構成、開発環境、pytest を中心としたテスト規約など、realization code や realization test の書き方を確認したいとき。
- 現行設計に対して、過去に不採用となった代替案やその理由を再検討したいとき。

## Do not read this when
- 自然言語仕様ではなく、oracle src、oracle test、realization code の具体的な実装・テスト本文を確認したいとき。
- oracle file と realization file の一般的な責務境界、編集責任、INDEX.md エントリー作成規則だけを確認したいとき。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` などのパスキーワード定義そのものだけを確認したいとき。
- 採用済み仕様ではなく実装上の関数、クラス、内部 helper、テスト構造を直接調べたいとき。

## hash
- 690fd1aca1eb642216bd1c09a5f3a860789ec5694de8c0a2e8f3ee2837e31db9

# `src`

## Summary
- AI agent call のパラメータ、プロンプト構築、設定、パス、構造化文書 helper など、cmoc の基礎概念を定義する oracle src 領域。
- agent call の入力契約・出力契約、共通規範プロンプト、リポジトリ別設定、モデル指定、ファイルアクセス権限、preflight、パスプレースホルダなどの正本仕様断片への入口。

## Read this when
- cmoc が AI agent call をどの prompt、Structured Output schema、モデル設定、ファイルアクセス権限、preflight 設定で組み立てるか確認したいとき。
- agent call 用の完全プロンプトが、役割、概要、ゴール、標準文書、読み書き規則、プレースホルダ定義などからどう構築されるか確認したいとき。
- oracle standard、realization standard、review standard、apply review standard、index entry standard など、AI に注入する共通規範プロンプトの生成元を探すとき。
- cmoc のリポジトリ別設定、モデル指定、実行予算、設定 JSON 保存方針、管理対象 Ollama に関する正本仕様断片を探すとき。
- パスプレースホルダ、ルート探索、実パス変換、構造化 Markdown レンダリング helper など、複数領域から参照される基礎概念を確認したいとき。

## Do not read this when
- CLI サブコマンド固有の利用者向け入出力、実行フロー、状態ファイル仕様、branch 操作、diff 取得、merge 実行などを調べたいとき。
- バックエンド API へ送る実リクエスト形式、具体的なモデル名解決、agent CLI 実行処理など realization src 側の実装詳細を調べたいとき。
- 個別の規範本文や生成済み Markdown 文書の意味だけを読みたいとき。
- oracle file、realization file、INDEX.md などの管理方針そのものだけを確認したいとき。
- 実装ファイルやテストファイルの現在構造を把握して直接修正したいだけで、agent call parameter、prompt 生成、設定、パス、文書モデルに関係しないとき。

## hash
- 418936a60b9acdebe4b99b30cece62d752aa59483e995e3ccd49bde5944a898a
