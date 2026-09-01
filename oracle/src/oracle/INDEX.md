# `acp_builder`

## Summary
- 各種 agent call の入力パラメータと prompt 構築定義をまとめたディレクトリ。共通の AgentCallParameter、indexing、oracle 編集・調査、quota probe、realization 追従、session join、TUI などの用途別設定への入口を提供する。

## Read this when
- agent call の起動条件、prompt、ファイルアクセス制御、cwd、editor input、indexing preflight、Structured Output schema などの構築定義を調べるとき
- 特定の cmoc コマンドに対応する agent call パラメータの担当ファイルを特定し、用途別の定義へ進むとき

## Do not read this when
- agent call の共通仕様や policy の定義そのものを確認したいときは、共通の prompt・builder 定義を直接読むとき
- 実際の agent call 実行、session join の競合解消、oracle や realization の本文編集、INDEX.md 更新など、呼び出しパラメータ構築後の処理を確認したいとき
- 特定の Structured Output schema の機械的な受理条件だけを確認したいときは、対応する schema 定義を直接読むとき

## hash
- 7130b785d995a064147eb3ed76bbc875085e6b1cce25ed7963feead6351e8075

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
- 対象ディレクトリは、agent が検出した問題を feedback reporter から collector へ渡すための入力契約を扱う領域です。問題の分類・重要度・影響、人間の対応が必要な理由、原因の確信度、再確認可能な根拠、作業継続状態を表現・検証する下位要素への入口になります。

## Read this when
- feedback reporter の入力形式や、検出した問題を人間向け feedback として構造化する処理を確認するとき。
- 入力契約を構成するスキーマや関連する検証定義を調査・変更するとき。

## Do not read this when
- collector 側の保存、集約、重複判定の仕様だけを確認したいとき。
- feedback の検出方法や、agent が作業を継続するかどうかの判断ロジックだけを確認したいとき。

## hash
- a86d0e0a2687a4eed300cd97383ba6e521f2347418e4446a2bfba702aedcd9ba

# `other`

## Summary
- cmoc の共有基盤として、設定定義、agent call 間で使うパスコンテキスト、構造化文書の Markdown レンダリングを扱う要素への入口です。
- 設定の既定値や Codex provider 対応、worktree・repository・run のルート解決、構造化文書の整形処理を確認できます。

## Read this when
- cmoc の設定項目、既定値、Codex CLI の provider・model・reasoning effort 対応を確認するとき。
- agent call の設定や設定の永続化対象を確認するとき。
- worktree root・main repository root・run root の導出規則や、cmoc プレースホルダの解決・変換を確認するとき。
- 構造化文書を Markdown に変換する処理、見出し深度、参照ブロック、コードフェンス、規定文、空行の整形を確認するとき。

## Do not read this when
- 特定の agent call のプロンプト生成や実行処理そのものを調べるとき。
- 設定値の JSON 同期・生成や doctor による永続化処理を直接確認したいとき。
- 個別の CLI 機能や realization の実装責務だけを確認したいとき。
- Markdown 以外の出力形式、文書要素の具体的内容、または正本仕様を直接確認したいとき。

## hash
- 24d115721f401060c1235a3dfbb7d21b7338b4a1e75fe058d142daaef79bd859

# `prompt_builder`

## Summary
- `prompt_builder` は、agent call に渡す完全な prompt と、その共通部品・入力初期文面・oracle／realization 概念を組み立てる実装群への入口。
- 個別の policy builder、prompt template、editor input、共通 placeholder 型を確認するための下位要素を含む。

## Read this when
- agent call 向け prompt の構成、共通部品の組み合わせ、policy の選択経路を把握したいとき。
- prompt に注入される oracle／realization の概念、ファイル分類、routing や INDEX エントリー生成に関する構築経路を確認したいとき。
- prompt builder 配下で、placeholder 型、完全 prompt 組み立て、editor 初期入力、または個別 policy builder の担当対象を特定したいとき。

## Do not read this when
- 個別 policy の具体的な文面や生成処理だけを調べる場合は、該当する policy builder を直接読む。
- 実際の oracle 文書、realization の実装・テスト、または生成済み prompt の実行処理を確認したい場合は、それぞれの対象を直接読む。
- prompt builder と無関係な構造化文書ノード、SDHeader／SDPolicy などの共通データ型、CLI 挙動を調べる場合。

## hash
- 096d45cf3746f5776a342ea0a7146c38e070e3c4defa4772c26f2762c025d687
