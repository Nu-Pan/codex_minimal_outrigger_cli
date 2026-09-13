# `acp_builder`

## Summary
- 対象ディレクトリは、oracle・feedback・indexing・quota probe・realization・session・TUI などの用途別に、エージェント呼び出しの基本設定や prompt、出力契約を組み立てる下位要素への入口。
- 共通の AgentCallParameter 定義を用途別の呼び出し構築へ振り分け、各用途固有の起動条件・権限・作業ディレクトリ・indexing 設定を確認するための階層。

## Read this when
- oracle、feedback、indexing、quota probe、realization、session join、または TUI に関する agent call の構築条件や、対応する下位実装への入口を判断するとき。
- 用途別の prompt、ファイルアクセス権、Structured Output、作業ディレクトリ、MCP handoff、indexing preflight の設定を横断して追跡するとき。

## Do not read this when
- 特定用途の agent call の具体的な prompt や出力契約だけを調べる場合は、該当する下位対象を直接読む。
- 共通の呼び出しパラメータ型・既定値・ファイルアクセスモードの一般定義だけを確認する場合は、共通定義を直接読む。
- 各用途の意味仕様、実際の Git 差分・realization 編集・merge 処理、または index エントリー生成規則そのものを調べる場合は、それぞれの正本仕様や実装を直接読む。

## hash
- cafaef716d95a07fc8596431f91a8d642d7186db92d487d2ba3f51f398fb3aae

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
- cmoc のリポジトリ固有設定を表すデータモデル。並列実行数、Codex の provider・model・推論設定、ファイルアクセス規定違反時のリカバリ試行回数を集約する。
- パス表記とルートプレースホルダの基盤モデル。agent call の cwd から worktree・main repository を導出し、プレースホルダと絶対パスの相互変換を扱う。
- 階層化された文章要素、参照可能なタグ付きブロック、コードブロック、構造化ポリシーを保持し、Markdownへレンダリングするための型と処理を提供する。

## Read this when
- cmoc の設定項目や既定値、Codex call 種別ごとの provider・model・推論設定、JSON/TOML表現、並列数やリカバリ回数を確認・変更するとき。
- agent call の cwd、worktree root、main repository root、{{cmoc-root}}・{{repo-root}}・{{run-root}}・{{work-root}} の解決規則やパス変換を確認・変更するとき。
- 構造化文書のノード型、見出し深度、cmoc_ref／cmoc_block、コードフェンス、ポリシー、空行やインデントのMarkdownレンダリングを確認・変更するとき。

## Do not read this when
- 設定ファイルの永続化・生成・同期や doctor の挙動を確認したいときは、設定入出力を担う対象を読むべき。
- 個別の agent call、CLI、TUI、oracle、realization の実行フローを確認したいときは、それぞれの処理対象を直接読むべき。
- 個別のポリシー本文・文書テンプレート、またはMarkdown以外の出力形式や生成側の仕様を確認したいときは、該当する対象を直接読むべき。

## hash
- 4e0b3934e69f302d3c6e7691504546545c65bd697a2075c99ba4cd57455ef24d

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
