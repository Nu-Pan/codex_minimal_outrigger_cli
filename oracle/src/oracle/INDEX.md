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
- cmoc の設定モデルを定義し、JSON/TOML 共通設定、Codex の provider・agent call 設定、並列数、ファイルアクセス違反時のリカバリ回数を扱う入口。
- cmoc のパス表記とルートプレースホルダを定義し、agent call のパスコンテキスト導出、プレースホルダ解決・変換、Git metadata に基づく各ルート探索を扱う基盤。
- 構造化ドキュメント要素を保持し、見出し、参照可能ブロック、コードブロック、規定を Markdown にレンダリングする実装への入口。

## Read this when
- cmoc の設定項目、既定値、Codex 呼び出しごとの設定、provider-local 設定、不変性、JSON 構造や agent call 種別と Codex call 設定の対応を確認するとき。
- agent call の cwd から導出される worktree root・main repository root、{{cmoc-root}}・{{repo-root}}・{{run-root}}・{{work-root}} の解決と変換、Git worktree metadata に基づく探索規則を確認するとき。
- 構造化文書の Markdown レンダリング、見出し階層、cmoc_block/cmoc_ref、コードブロック、SDPolicy、SDNode、ntqs の挙動や利用方法を確認するとき。

## Do not read this when
- 設定ファイルの生成・同期処理、JSON シリアライズ処理、特定の agent call の実行フロー、Codex CLI 起動、oracle・realization の処理内容を直接確認したいとき。
- 個別の CLI 機能や realization の責務、パスモデルを介さない一般的なファイル操作、対象モジュール以外の仕様を確認したいとき。
- Markdown 以外の文書形式のレンダリング、文書構造の仕様・入力生成規則、cmoc の一般的な規定や参照ルーティングの仕様を確認したいとき。

## hash
- 759f4486e74e9a2dc7d94c9b88105a0c80f67e3db342bfd6b8c2f69e04f20fb8

# `prompt_builder`

## Summary
- プロンプト構築の共通型、完全 prompt の組み立て、エディタ入力初期文面、oracle／realization 部品、および個別 policy 部品を扱うディレクトリへの入口。
- agent call 向け prompt の構成と、作業規定を組み込む部品群を、共通構築処理・部品・policy 定義に分けて確認できる。

## Read this when
- agent call に渡す prompt の構成、placeholder 定義の統合、またはエディタ入力への初期 prompt 埋め込みを調べるとき。
- oracle／realization の説明部品や、file access・feedback・routing・INDEX エントリー生成などの作業 policy を prompt に組み込む処理を確認するとき。
- 個別 policy の実装入口や、複数 policy を組み合わせる prompt builder の責務境界を確認したいとき。

## Do not read this when
- 個別 policy の意味仕様そのもの、oracle／realization の正本仕様、実際のファイル分類や feedback 送信の実装を直接確認したいとき。
- 生成済み prompt に適用されたセッション固有の規定や、一般的な Markdown・構造化文書の仕様だけを調べるとき。

## hash
- 145fa5a113548ca36370ff694cc94d668e6129137907d058a4d984453e7fbae5
