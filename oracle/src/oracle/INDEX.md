# `acp_builder`

## Summary
- AIコーディングエージェント呼び出し用の論理モデル、推論強度、ファイルアクセス、プロンプト、Structured Output schema、作業ディレクトリなどの AgentCallParameter 定義を扱うディレクトリ。feedback、indexing、oracle、realization、session、tui など用途別の agent call 構築定義への入口を提供する。

## Read this when
- agent call の共通パラメータ契約やモデル・推論・ファイルアクセス設定を確認するとき
- feedback issue 判定、INDEX.md エントリー生成、oracle 操作、realization 反映・refactor、session conflict 解消、TUI、quota probe の起動設定や出力契約を調査・変更するとき

## Do not read this when
- 実際のモデル名やバックエンド固有の解決処理を確認するとき
- oracle や realization の正本仕様・具体的な実装やテストを確認するとき
- 共通 prompt 生成、CLI のサブコマンド解析、TUI の画面処理など、このディレクトリの用途別 agent call 定義に直接属さない処理を確認するとき

## hash
- e83d8d3998bbc8c030f56d4faa50269583ee65f4dff52ea22c6dad15f891a9a7

# `feedback`

## Summary
- 対象ディレクトリは、agent が検出した問題を feedback reporter から collector へ渡すための入力契約を扱う領域です。問題の分類・重要度・影響、人間の対応が必要な理由、原因の確信度、再確認可能な根拠、作業継続状態を表現・検証する下位要素への入口になります。

## Read this when
- feedback reporter の入力形式や、検出した問題を人間向け feedback として構造化する処理を確認するとき。
- 入力契約を構成するスキーマや関連する検証定義を調査・変更するとき。

## Do not read this when
- collector 側の保存、集約、重複判定の仕様だけを確認したいとき。
- feedback の検出方法や、agent が作業を継続するかどうかの判断ロジックだけを確認したいとき。

## hash
- a86d0e0a2687a4eed300cd97383ba6e521f2347418e4446a2bfba702aedcd9ba

# `other`

## Summary
- oracle/src/oracle/other は、cmoc の複数機能が共有する補助モデルと文書化ヘルパーを扱うディレクトリである。
- cmoc_config.py はリポジトリ固有設定、Codex CLI 設定、oracle review のループ上限とシリアライズ対象を確認する入口である。
- path_model.py は root placeholder、Git worktree からの root 解決、agent call のパスコンテキストを確認する入口である。
- struct_doc.py は構造化文書ノードを Markdown に変換し、見出し階層、cmoc_block/cmoc_ref、コードフェンス、規定文章を扱う処理の入口である。

## Read this when
- 複数の機能から共有される cmoc 設定モデル、パスモデル、または構造化 Markdown 生成ヘルパーの責務を確認するとき
- 設定項目や既定値、JSON/TOML 化の対象を確認するときは cmoc_config.py を読むとき
- root placeholder や worktree root、repository root、agent call のパスコンテキストの解決規則を確認するときは path_model.py を読むとき
- 構造化文書のノード型や Markdown レンダリング規則を確認するときは struct_doc.py を読むとき

## Do not read this when
- 特定の CLI サブコマンドや realization の処理フローだけを確認したいとき
- Codex CLI の呼び出し実装や oracle review の所見生成ロジックを確認したいとき
- 設定ファイルの実際の保存内容や人間による調整結果だけを確認したいとき
- 構造化文書ヘルパーの利用側が定める仕様や呼び出し元の責務だけを確認したいとき
- INDEX.md のルーティング規則や文書全体のナビゲーションだけを確認したいとき

## hash
- 2d59e9705d8be1d2d0f6cc2db9ef0a6098a3f509f1a086fa4122680ad8668565

# `prompt_builder`

## Summary
- agent call 向けプロンプトを構築する実装群。共通のプレースホルダー型、完全プロンプト生成、エディタ入力、oracle・realization の基本説明、用途別 policy を扱う。
- 完全プロンプトの構築順序や全体統合を確認する入口は complete_prompt.py。個別の制約や判断規範は policy 配下、共通概念は parts 配下へ進む。

## Read this when
- agent 向け完全プロンプトの生成経路や構成要素を確認・変更するとき。
- file access、oracle・realization、routing、feedback、review、conflict 解消、editor handoff、INDEX.md エントリー生成などの policy の入口を特定するとき。
- プレースホルダー定義、エディタ入力の初期文面、oracle と realization の基本概念を調べるとき。

## Do not read this when
- oracle または realization の正本仕様、実装、テスト本文を確認したいとき。
- 特定の policy の具体的な挙動だけを調べる場合は、ディレクトリ全体ではなく対応する policy ファイルを直接読む。
- 生成済みプロンプトの結果だけが必要で、prompt builder の構成元を確認する必要がないとき。

## hash
- 579012b1ee9380542a233fb726e4d188d982d50a93c304bc9fe0a5988c116574
