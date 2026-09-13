# `acp_builder`

## Summary
- AI コーディングエージェント呼び出しの共通パラメータ型とファイルアクセスモードを定義する。
- quota probe、INDEX.md エントリー生成、feedback issue 処理、oracle 調査・編集、realization 追従・レビュー、session join の競合解消、TUI 起動に関する agent call 構築処理への入口。
- 各 agent call の prompt、対象範囲、起動 cwd、Structured Output schema、editor input MCP、indexing preflight の設定を扱う。

## Read this when
- agent call の共通パラメータや論理ファイルアクセスモードを確認するとき。
- 特定の cmoc サブコマンドに対応する agent call の prompt、起動条件、権限、作業範囲を調べるとき。
- feedback、indexing、oracle、realization、session join、TUI の下位処理へ進む入口を判断するとき。

## Do not read this when
- ファイルアクセスモードの正本上の意味や Codex CLI sandbox への対応を確認したいとき。
- agent call の実際の実行処理、prompt 共通構造、path context、構造化文書のレンダリングを直接調べたいとき。
- feedback の受付・候補 issue 管理、oracle file や realization file の具体的内容、通常の Git 差分処理そのものを調べたいとき。

## hash
- 9b2196fe2b6b7a617707200fe497dab2da9968d35ee417bca4b601de159c717c

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
- フィードバック問題報告入力の正本スキーマを扱う領域で、分類・重要度・影響・未解消制約・原因・再確認用根拠・継続状態の入力契約への入口。

## Read this when
- cmoc_feedback.submit_observation に送る問題報告の入力項目、許容値、文字数制約、根拠に応じた path 条件を確認するとき。
- 問題報告を JSON として組み立てる際に、reporter input の形式と根拠記述の要件を確認するとき。

## Do not read this when
- 問題報告の送信手順や collector の処理を確認したいとき。
- reporter input のスキーマではなく、フィードバック収集結果や重複判定の実装を確認したいとき。

## hash
- 709d2b0ca7660b1772a43fe8fdaed710d40142564511ba28a435a49b6776aa67

# `other`

## Summary
- cmoc の設定モデル、パスコンテキスト、構造化文書の Markdown レンダリングを担う基盤モジュール群への入口。設定値の構造、リポジトリ内のパス解決、文書ノードの出力規則を確認する際に参照する。

## Read this when
- CmocConfig などの設定モデルや Codex CLI 呼び出し設定の既定値・構造を確認または変更するとき。
- worktree・repository・run のルート導出、パスプレースホルダの解決・変換規則を調べるとき。
- 見出し、タグ付きブロック、コードブロック、ポリシーなどの構造化文書を Markdown 化する仕様を調べるとき。

## Do not read this when
- Codex CLI の呼び出し実装や agent call の実行フローだけを調べるとき。
- 設定の永続化・生成処理や doctor コマンドなど、設定モデルを利用する処理の挙動だけを確認したいとき。
- 個別機能の動作、一般的なファイル操作、または個別のポリシー本文・テンプレートだけを直接確認すれば足りるとき。

## hash
- aad6313c4fdb76fe58bf0ac778bee22571cdf5d0e592669794065472800697e2

# `prompt_builder`

## Summary
- agent call に渡す完全な構造化 prompt を組み立てる入口と、追加 prompt・目的・placeholder の統合を扱う。
- ファイルアクセス、routing、oracle／realization、feedback、conflict 解消、INDEX エントリーなど、用途別の prompt policy を責務ごとに提供する。
- エディタ入力用の初期文面や、oracle／realization の基本知識など、agent prompt に注入する構造化文面の部品を提供する。

## Read this when
- agent call の完全 prompt の構成順序、任意 policy の有効化、目的・追加文面の組み込み方を確認・変更するとき。
- prompt builder における file access、routing、oracle／realization、feedback、conflict 解消、INDEX routing などの規定の構築経路を調べるとき。
- placeholder 定義の統合や、エディタ経由の prompt 初期文面、agent 向け構造化文面の部品を確認するとき。

## Do not read this when
- 個別 policy の正本仕様や具体的な規定内容だけを確認したいときは、対応する policy の実装または正本仕様を直接読む。
- oracle／realization の責務そのもの、実際のファイル分類、または INDEX routing の意味仕様を確認したいときは、対応する正本仕様を直接読む。
- prompt builder と無関係な型定義、実装処理、または特定の agent call の実行結果を調べるとき。

## hash
- fdaaf063c3dbeda9f12257a80401506b9f0817056db9742b249d1d488e45dff6
