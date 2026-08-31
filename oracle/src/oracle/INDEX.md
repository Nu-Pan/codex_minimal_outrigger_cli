# `acp_builder`

## Summary
- AI コーディングエージェント呼び出しのパラメータ型と、各コマンド・用途別の prompt／起動設定の構築定義をまとめた入口。
- quota probe、INDEX.md エントリー生成、feedback issue 判定・検証、TUI 起動などの agent call builder へ進むための上位ルーティング。

## Read this when
- agent call の共通パラメータ、ファイルアクセスモード、cwd、Structured Output schema、editor input handoff MCP、indexing preflight の設定を確認するとき。
- 特定の用途における agent call の prompt 構築や起動条件を調べるとき。
- quota probe、indexing、feedback、oracle、realization、session、TUI の各 builder の入口を選ぶとき。

## Do not read this when
- ファイルアクセスモードの詳細な意味や Codex CLI sandbox への対応を確認したいときは、参照される正本仕様を読む。
- 個別の agent call の実装詳細、prompt の共通レンダリング、または実行フローだけを確認したいときは、対応する下位ファイルや共通基盤を直接読む。
- Structured Output schema の受理条件そのものを確認したいときは、対応する schema ファイルを直接読む。
- 既存 INDEX.md の内容や一般的なルーティング規則を確認したいときは、このディレクトリではなく対象の INDEX.md を読む。

## hash
- faa81796a0eb346f3c5e9c132edb210ac28e9c4627178b98e910be01a6cca17c

# `editor_input_handoff`

## Summary
- cmoc のエディタ入力上書きツールが受け取る入力契約を定義する JSON Schema です。
- 上書き対象を識別する値と、対象へ渡す内容を指定するための直接の参照先です。

## Read this when
- エディタ入力上書きツールの呼び出し形式を確認するとき。
- 上書き対象と書き込む内容に必要な入力項目を確認するとき。

## Do not read this when
- エディタ入力上書き処理の実装やワークフローを確認するとき。
- エディタ入力上書き以外のツール入力契約を確認するとき。

## hash
- ab2b3f70177976188963683a20698484d105ee1df31cc928aa2c4f2b6ecbdd56

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
- cmoc の設定モデル、パスコンテキスト、構造化文書の Markdown レンダリングを担う基盤要素への入口です。
- リポジトリ固有設定の構造と既定値、agent call のルートプレースホルダ解決、構造化要素の見出し・タグブロック・コードブロック・規定文への変換を扱います。

## Read this when
- cmoc の設定モデルや既定値、Codex CLI・oracle review 向け設定の構造を確認するとき。
- agent call の worktree・repository ルートや {{cmoc-root}} などのパスプレースホルダの導出・解決規則を調べるとき。
- 構造化された文書要素を Markdown へレンダリングする見出し深度、タグブロック、コードフェンス、規定文の挙動を確認するとき。

## Do not read this when
- 具体的な設定ファイルの生成・同期処理や、設定値を利用する個別機能の挙動だけを調べるとき。
- Codex CLI の呼び出し処理、oracle review の実行ロジック、その他の個別 CLI 機能の責務を調べるとき。
- Markdown 以外の出力処理や、構造化文書の具体的な内容・正本仕様を確認するとき。

## hash
- 3fd788f1c9b21981b8b200ab384aec8d98a5b244a00dbe9ab35b7eae8f465c80

# `prompt_builder`

## Summary
- agent call に渡す完全な prompt と、その初期入力文面を構築する prompt builder の実装群への入口。共通 placeholder 型、完全 prompt の統合、editor 向け初期テキスト、oracle・realization 概念、各種 policy の組み立てを扱う。
- prompt の構成や policy の適用条件、placeholder 統合、editor input の生成、oracle・realization の分類や routing 情報の構築を確認するための下位要素への入口。

## Read this when
- agent call 用 prompt の生成責務を全体的に把握したいとき。
- 完全 prompt の構成、policy の組み込み、placeholder の統合、editor 初期入力、oracle・realization の基本概念や分類を調査するとき。
- 具体的な prompt builder の責務に応じて、配下の該当モジュールへ進む必要があるとき。

## Do not read this when
- 個別の policy の詳細、完全 prompt のテンプレート、editor input の具体的な初期文面、oracle・realization の正本仕様を直接確認したいときは、対応する下位対象または参照先を読む。
- CLI の実行処理、実際の oracle・realization ファイル、INDEX.md の生成処理そのものを調べるとき。
- prompt builder と無関係な型定義やプロンプト仕様を確認するとき。

## hash
- 14ec6fd297984174f91b5accab84727e68583cb50e4a4892df9605a489f8dd90
