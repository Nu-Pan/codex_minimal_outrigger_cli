# `acp_builder`

## Summary
- ACP builder の各種 agent call について、prompt、アクセスモード、作業ディレクトリ、Structured Output、indexing 実行条件などの起動パラメータを構築する実装群。
- oracle 編集・調査、realization 追従・修正、feedback 処理、index entry 生成、TUI 起動、session conflict 解消、quota probe への入口を含む。

## Read this when
- ACP builder の agent call パラメータや prompt 構築の責務を確認したいとき。
- サブコマンド別の agent 起動条件、ファイルアクセス境界、Structured Output schema の関連を調べるとき。
- 特定の処理を担当する下位領域が不明で、まず builder 全体の構成と入口を把握したいとき。

## Do not read this when
- INDEX.md のルーティング生成処理だけを確認したい場合は、indexing の下位項目を直接読むとき。
- oracle 編集、feedback、realization、session など特定機能の実装詳細だけが必要な場合は、対応する下位ディレクトリへ直接進むとき。
- agent call の実行そのものや prompt policy の正本仕様を確認する場合は、この builder ではなく実行経路または oracle/doc の仕様を読むとき。

## hash
- 68207a8b15fc00df719e967c0efaf97818fe1d3a936fa898af8d8de3b13e3d0d

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
- agent に渡す完全 prompt を、パス由来の placeholder 定義、基礎規定、選択式 policy、目的、追加文面の順に組み立てる中核モジュール。
- prompt_builder.basic は placeholder の型を定義し、parts と policy の各 builder は oracle/realization、アクセス制限、routing、INDEX entry、feedback などの構造化文面を提供する。
- editor_input はエディタ経由のユーザー入力用初期文面を生成し、complete_prompt は各部品の placeholder 衝突を検査して最終 prompt を構成する。

## Read this when
- agent call に渡す完全 prompt の構成、含める policy、目的情報、placeholder の統合方法を確認・変更するとき。
- oracle/realization や INDEX entry など、既存の構造化された規定文面を prompt builder へ組み込む流れを調べるとき。
- エディタ経由の入力テンプレートや、完全 prompt 内へユーザー入力を配置する初期文面を確認するとき。

## Do not read this when
- 個別 policy の本文だけを確認すれば足り、完全 prompt への組み込み順序や共通 builder の挙動を調べる必要がないとき。
- prompt builder 以外の agent call 実行、構造化文書のレンダリング、パスコンテキストの実装を直接調べるとき。

## hash
- a6dea3d0ece30dbee8bf9e1a110fe12b1e4f33ffd357b6fa9ef909ac02ace9d5
