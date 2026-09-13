# `acp_builder`

## Summary
- AI コーディングエージェント呼び出しの共通パラメータ型と、cmoc の論理的なファイルアクセスモードを定義する。
- oracle の編集・調査、realization の反映・修正、feedback issue の正規化・remediation、session join の conflict 解消、TUI・quota probe の各 agent call 構築への入口を提供する。
- INDEX.md エントリー生成用を含む Structured Output schema と、それに対応する読み取り専用 agent call の構築を扱う。

## Read this when
- oracle 配下の agent call について、処理種別ごとの prompt・権限・作業ディレクトリ・Structured Output・indexing preflight の設定を横断して確認するとき。
- 共通の AgentCallParameter や FileAccessMode の定義、および個別 builder への責務分担を把握したいとき。
- agent call の構築実装または出力 schema の変更箇所を特定するとき。

## Do not read this when
- 特定の agent call の詳細な prompt や結果分類を確認したいときは、対応する oracle、realization、feedback、session、tui、quota_probe、または indexing の下位要素を直接読む。
- Codex CLI sandbox へのアクセスモードの対応や、共通 prompt・policy の定義そのものを確認したいとき。
- 実際の oracle file・realization file の編集、feedback の受付処理、Git 差分処理、または session join の通常マージ処理を調べたいとき。

## hash
- 11c10852800543b785a137bcbf65c3ed35c5df9852ffcd370b2c4356429d3f3a

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
- agent call 向け prompt の構築に関わる型定義、完全 prompt の組み立て、エディタ入力の初期文面、prompt 部品、作業種別ごとの policy 定義を確認するための入口。
- placeholder の置換値型、prompt の構成と統合、入力文面の生成、oracle／realization の説明部品、各種 policy の選択経路という下位要素へ進むためのまとまり。

## Read this when
- agent に渡す prompt の構成や、任意 policy の注入、目的・追加文面・placeholder の統合を調べるとき。
- prompt builder に関わる型定義、エディタ入力の初期文面、oracle／realization の prompt 部品、作業種別別 policy の入口を確認するとき。
- 個別の prompt builder 機能について、型・組み立て入口・入力生成・部品・policy のどこから読み始めるべきか判断するとき。

## Do not read this when
- 個別 policy の具体的な instruction 文面や実装だけを確認したいときは、policy 配下の該当定義を直接読む。
- oracle／realization の責務や正本仕様、実際のファイル分類ロジックを確認したいときは、prompt builder の部品ではなく対応する正本仕様や分類実装を直接読む。
- agent call の実行処理や、prompt builder と無関係な構造定義を確認したいとき。

## hash
- 5adbabfb1340a75af3163628fea21ef4ef0a9baf42d4fbdc6344562085c1790c
