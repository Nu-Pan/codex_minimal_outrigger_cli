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
- 開発対象リポジトリごとに変わる cmoc 設定を集約し、Codex CLI の provider・agent call 設定、並列数、アクセス規定違反時の復旧試行回数を定義する設定モデル。設定の永続化と編集方針も扱う。
- agent call の cwd と Git metadata から worktree・main repository・run のルートを導出し、{{cmoc-root}}、{{repo-root}}、{{run-root}}、{{work-root}} の解決・変換を担うパスコンテキストの基盤モデル。
- 見出し、参照可能ブロック、コードブロック、規定を構造化して保持し、見出し階層や cmoc_block/cmoc_ref、コードフェンス、SDPolicy を Markdown にレンダリングする文書構造ヘルパー。

## Read this when
- cmoc の設定項目、既定値、Codex CLI 呼び出し設定、provider-local 設定、設定の永続化・編集方針を確認するとき。
- agent call の cwd から各ルートを導出する規則、パスプレースホルダの解決・変換、Git worktree metadata の探索挙動を確認するとき。
- 構造化文書の要素、見出し深さ、cmoc_block/cmoc_ref、コードブロック、SDPolicy の Markdown 出力を調べるとき。

## Do not read this when
- agent call のプロンプト生成や Codex CLI の実際の呼び出し処理を調べるとき。設定の保存・同期の具体的な処理だけを調べる場合は、その処理の実装対象を直接読む。
- 個別の CLI 機能や realization の実装責務だけを確認するとき。パスモデルを介さない一般的なファイル操作や他モジュールの仕様を調べるとき。
- Markdown 以外の文書レンダリング、文書構造の仕様や入力生成規則、cmoc の一般的な規定・参照ルーティング仕様を確認するとき。

## hash
- 411eec9964f041d171dbcd8abaab25593d0ee42c50677fbf43783e308ae381a3

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
