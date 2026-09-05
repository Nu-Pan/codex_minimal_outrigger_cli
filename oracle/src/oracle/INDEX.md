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
- 日本語技術文書として、prompt_builder 配下の型定義・完全 prompt 構築・エディタ入力・oracle／realization 部品・policy 集約を案内する入口。

## Read this when
- agent call 向け prompt の構成、入力初期文面、placeholder 定義、oracle／realization のプロンプト部品、または policy 群の配置と選択条件を調べるとき。

## Do not read this when
- 個別 policy の具体的な文面や実装、placeholder 置換処理そのもの、prompt 全体の正本仕様を直接確認したいときは、該当する個別対象へ進む。

## hash
- aade97b212f1e61ff885fcb481c40e82d0a5db10c66c6039d706207c17519de7
