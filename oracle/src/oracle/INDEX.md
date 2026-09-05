# `acp_builder`

## Summary
- AI コーディングエージェント呼び出しの共通パラメータ型と、用途別の prompt・起動設定を構築する上位入口。
- quota probe、INDEX.md エントリー生成、feedback issue の同一性判定・remediation、TUI 起動の各 agent call 定義へ進むための集約点。
- indexing、feedback、tui の下位要素では、それぞれの agent call に固有の入力、アクセス権限、Structured Output、検証・起動条件を扱う。

## Read this when
- agent call builder 全体の責務分担や、共通パラメータから用途別定義への入口を確認するとき。
- 複数の agent call に共通するファイルアクセスモード、prompt、cwd、Structured Output schema、indexing preflight の設定箇所を探すとき。
- quota probe、indexing、feedback、または TUI の agent call 構築を調べる際に、該当する下位要素へ進む前の構成を把握するとき。

## Do not read this when
- 特定の agent call の詳細な prompt、入力データ、結果分類、または起動条件だけを確認したい場合は、対応する下位要素を直接読む。
- Codex CLI の sandbox へ対応するファイルアクセスモードの意味を確認したい場合は、basic.py が参照する正本仕様を読む。
- Structured Output schema の機械的な受理条件だけを確認したい場合は、対応する JSON schema を直接読む。
- INDEX.md の更新処理や、oracle・realization ファイル自体の内容を確認したい場合。

## hash
- ff75a9e35d500113ace32d295f620adfcceb0cd342819a768c1ccb9b3397a6a5

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
- cmoc の周辺基盤モデルをまとめたディレクトリ。設定データクラス、Git worktree とルートプレースホルダを扱うパスコンテキスト、構造化文書を Markdown に変換する要素・レンダラーへの入口。

## Read this when
- cmoc のリポジトリ固有設定、agent call のパス解決、または構造化文書の Markdown レンダリングを横断して調べるとき
- 個別モジュールの責務が設定・パスモデル・構造化文書のどれに属するかを判断し、該当する実装へ進むとき

## Do not read this when
- 特定の設定項目、ルートプレースホルダ解決、または Markdown 要素のレンダリングだけを調べる場合は、該当する個別モジュールを直接読むとき
- agent call の具体的な処理フロー、CLI 呼び出し、設定ファイルの生成・同期など、これらの基盤モデルを利用する上位実装だけを調べるとき

## hash
- b39b9b65f91790a4f4f66f750bc72b78f59e3bdc4506213d8ba9d788a7f5a863

# `prompt_builder`

## Summary
- agent call 向けの完全 prompt とエディタ初期入力を組み立てる実装、および prompt 構築に使う部品・policy 定義をまとめたディレクトリ。
- 型定義から入力文面生成、完全 prompt の統合、個別 policy の構築まで、prompt builder の責務へ進むための入口。

## Read this when
- agent call 用 prompt の構成、placeholder 統合、エディタ入力の初期文面、または個別 policy の選択・注入を確認・変更するとき。
- oracle／realization の説明や分類条件を prompt 部品として組み込む処理の入口を確認したいとき。

## Do not read this when
- 個別 policy の具体的な規定文や、その参照先である正本仕様を確認したい場合は、対応する policy モジュールまたは oracle file を直接読む。
- prompt builder を使わない CLI、MCP tool、または realization file の具体的な挙動だけを調べる場合。

## hash
- d30a96d735a04a371f3b5eb78452467c917b2edbfc9927fd9d0981581840fa29
