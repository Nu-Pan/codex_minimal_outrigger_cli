# `acp_builder`

## Summary
- AI コーディングエージェント呼び出しの共通パラメータ型とファイルアクセスモードを定義する。
- quota availability probe、INDEX.md エントリー生成、feedback issue 処理、oracle・realization・session・TUI など、用途別の agent call builder への入口をまとめる。
- 各用途に応じた prompt、Structured Output schema、作業ディレクトリ、editor input handoff、indexing preflight の設定を確認できる。

## Read this when
- agent call の共通パラメータ、アクセスモード、prompt、Structured Output schema、cwd、editor input handoff、または indexing preflight の設定を確認するとき。
- 用途別の agent call builder を探すとき。
- quota probe、indexing、feedback、oracle、realization、session、TUI の agent call 構築責務の入口を確認するとき。

## Do not read this when
- 特定の agent call の prompt や出力契約の詳細を確認したいときは、該当する下位ファイルを直接読む。
- agent call の共通実行処理や Codex CLI の実際の挙動を調査するとき。
- oracle・realization file の具体的な内容、編集手順、または feedback issue の保存・受付処理を確認するとき。

## hash
- 1c30d36fd04b48d7e50c884f1e64ee15f70f18d6731aa581d251b69cfd0c1ed5

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
- cmoc の設定モデル、パスコンテキスト、構造化 Markdown 文書モデルを扱う基盤モジュール群への入口。設定の既定値や Codex 呼び出し設定、プレースホルダ付きパスの解決、文書ノードの Markdown 化を確認・変更するときに参照する。

## Read this when
- cmoc の設定データモデルや Codex provider・agent call 設定を調べるとき。
- worktree・repository・run のルート導出や {{cmoc-root}} などのパスプレースホルダ処理を調べるとき。
- 見出し、タグ付きブロック、コードブロック、ポリシーなどの構造化文書を Markdown に変換する挙動を調べるとき。

## Do not read this when
- 設定ファイルの実体や doctor による生成・同期処理だけを確認したいとき。
- 個別の agent call 実行、Codex CLI 起動、設定値の検証・読み書きなどの呼び出し側処理を直接調べるとき。
- 個別のポリシー本文や文書テンプレート、Markdown 以外の出力仕様だけを確認したいとき。

## hash
- c2d41bb5a147876d4bcbc41ce5f4f1be5cc646617058ff26c92a7c090e5823ab

# `prompt_builder`

## Summary
- `prompt_builder` は、agent call に渡す prompt の構成要素を定義・組み立てるディレクトリで、placeholder 型、完全 prompt の組み立て、エディタ初期入力、oracle／realization 関連部品、policy 群への入口を提供する。

## Read this when
- agent 向け prompt の構成順序や placeholder 統合を確認したいとき。
- prompt に注入する個別 policy や oracle／realization 関連部品の生成定義を探したいとき。
- エディタへ渡す初期プロンプト文面の構築を確認したいとき。

## Do not read this when
- 個別 policy の意味仕様や実際のファイル分類ロジックを確認したいときは、それぞれの正本仕様・実装を直接読む。
- 既存の INDEX.md、agent call の実行結果、または prompt 適用後の具体的な挙動だけを確認したいとき。

## hash
- 543de79184f238dedb0cd23351c980f80fa8a9fe16b06b4a9bc582e01dd8a9b3
