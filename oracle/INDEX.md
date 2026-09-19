# `doc`

## Summary
- cmoc の自然言語による正本仕様ドキュメント群。ブランチモデル、アプリケーション仕様、開発規約、および採用しなかった設計案の記録を、カテゴリ別の下位文書への入口として提供する。

## Read this when
- cmoc の仕様全体から確認を始めるとき。
- サブコマンド、状態管理、ファイル分類、ログ、フィードバック、開発・テスト規約などの正本ドキュメントを探すとき。
- 現在の仕様に加えて、過去に検討したが採用しなかった設計判断の理由を確認するとき。

## Do not read this when
- 特定の仕様内容が分かっており、該当する下位の Markdown 文書を直接読めるとき。
- 実装コードの具体的な挙動を確認したいとき。
- テストコードや実行成果物を確認したいとき。

## hash
- 503724d55ffb90f47222b9428eacdfd484103d837bf015d41949314fc4ce1d4b

# `src`

## Summary
- oracle/src は cmoc の oracle 実装と agent 呼び出し用 Structured Output schema の入口で、ACP builder、prompt builder、設定・パス・構造化文書モデル、editor input handoff、feedback を含む。
- ACP builder は agent call の共通パラメータと、quota probe、INDEX エントリー生成、oracle 編集・調査、realization、feedback、session、TUI の起動定義を扱う。
- prompt builder は完全 prompt、プレースホルダー、ファイルアクセスや oracle/realization、routing、feedback などのポリシー文面を組み立てる。
- other は cmoc 設定、リポジトリおよび worktree のパスモデル、構造化文書と Markdown レンダリングを提供する。
- editor_input_handoff は MCP から受け取った依頼と送信元情報を editor work file 用 Markdown に変換し、feedback は問題報告入力の Structured Output schema を定義する。

## Read this when
- oracle/src 全体の責務分担や、agent call・prompt・設定・パスモデルの実装入口を確認するとき。
- oracle/src 配下で対象の領域を選び、ACP builder、prompt builder、other、editor input handoff、feedback のいずれから調査を始めるか判断するとき。
- oracle 実装と agent 呼び出し用 schema の関係を横断して確認するとき。

## Do not read this when
- 特定の agent call、prompt policy、設定値、パス解決、入力本文生成、feedback schema の詳細が既に特定できているときは、該当する下位ディレクトリまたはファイルを直接読む。
- 正本仕様文書、realization 実装、realization テスト、または個別の CLI 実行フローを確認したいとき。
- INDEX.md のルーティング規則自体や、対象ディレクトリに属さない文書を確認したいとき。

## hash
- a90235014b807cc22977faac2b7ceadfe75ee1cb8ce3cd410c50ad72d3b33259
