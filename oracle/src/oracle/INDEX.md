# `acp_builder`

## Summary
- AI コーディングエージェント呼び出しの prompt と AgentCallParameter を構築する定義を、用途別の下位ディレクトリに分けて扱う。
- feedback は observation の issue 同一性判定と realization file の remediation、indexing は INDEX.md エントリー生成、oracle は oracle 操作、realization は realization 反映・refactor、session は conflict 解消、tui は TUI 起動を扱う。
- quota_probe.py は Codex CLI の利用可能性確認用 agent call の構築を担う。
- basic.py は agent call の共通パラメータ型と論理的ファイルアクセスモードを定義する。

## Read this when
- agent call の用途別 builder 定義を探すとき。
- feedback、indexing、oracle、realization、session、tui の各 agent call の prompt・アクセスモード・起動設定を確認または変更するとき。
- 共通の AgentCallParameter や FileAccessMode の定義を確認するとき。
- Codex CLI の quota availability probe の呼び出し条件を確認するとき。

## Do not read this when
- 各 agent call の実行処理、対象ファイルの具体的な編集、Git 操作、または TUI の実行結果を確認したいとき。
- アクセスモードの正本仕様や共通 prompt 構造を確認したいときは、参照される仕様・prompt builder を直接読むとき。
- Structured Output schema の詳細な受理条件だけを確認したいときは、各用途の schema ファイルを直接読むとき。
- 生成済み INDEX.md のルーティング内容や、feedback issue・oracle・realization の実体を確認したいとき。

## hash
- 371d8cc6c1d1e383e47081dfc7116a7611329f77afdd6318908c836b7e845cae

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
- agent 呼び出し向けの完全な prompt と、エディタ入力用の初期文面を組み立てる実装群への入口。
- placeholder の型定義、prompt 構築、editor input の生成、oracle／realization の説明部品、個別 policy の構築を扱う。

## Read this when
- agent 向け prompt の構成順序、任意 policy の選択、目的・追加文面・placeholder の統合を確認するとき。
- エディタへ渡す初期入力文面や、oracle／realization、feedback、file access、routing、INDEX エントリーなどの policy 部品の生成経路を調べるとき。

## Do not read this when
- 個別 policy の具体的な規定文面や、その根拠となる正本仕様を直接確認したいとき。
- 実際の placeholder 置換処理、構造化文書の定義、ファイル分類など、下位要素の個別実装だけを調べるとき。

## hash
- 373663e29b57adc872b0f07a299ffa1bbe020e9d6daccc6b0a9080367d4be4e8
