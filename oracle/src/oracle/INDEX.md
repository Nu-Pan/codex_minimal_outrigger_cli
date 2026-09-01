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
- リポジトリごとに変化する cmoc の挙動設定を集約し、JSON/TOML 共通値、Codex provider、agent call、全体設定の dataclass を定義する設定モデル。
- agent call 全体で共有するパスコンテキストを構築し、worktree・main repository・run の各ルート導出と、cmoc のルートプレースホルダとの相互変換を担う基盤モデル。
- 見出し、参照ブロック、コードブロック、規定などの構造化文書要素を保持し、cmoc の文書記法を Markdown へレンダリングするためのモデルと関数。

## Read this when
- cmoc の設定項目や既定値、Codex CLI の provider・model・reasoning effort、agent call 種別ごとの設定、永続化対象を確認するとき。
- agent call の cwd から worktree root や main repository root を導出する規則、{{cmoc-root}}・{{repo-root}}・{{run-root}}・{{work-root}} の解決や変換、Git metadata に基づくルート探索を確認するとき。
- 構造化文書を Markdown に変換する処理、見出し階層、cmoc_block/cmoc_ref、コードフェンス、SDPolicy の出力形式、または関連する SDNode 系の責務を調べるとき。

## Do not read this when
- 特定の agent call のプロンプト生成・実行処理や、設定値の JSON 同期・生成といった周辺処理そのものを調べるとき。
- 個別の CLI 機能・realization の実装責務、またはパスモデルを介さない一般的なファイル操作を確認するとき。
- Markdown 以外の文書形式、文書構造の仕様・入力生成規則、または cmoc の一般的な規定・参照ルーティング仕様を確認するとき。

## hash
- 0e76c8bef13380706d6a2a5160587050fe6a42a1f1f5fd4753f1018ce0241d64

# `prompt_builder`

## Summary
- agent call 向け prompt builder の構成と、基礎規定・目的・追加文面・placeholder の統合入口を扱う階層。
- oracle／realization の説明部品と、各種 policy 文面の構築定義へ進むための入口。
- placeholder 型定義、エディタ初期入力、個別 policy の具体的な構築処理を確認するための下位要素を含む。

## Read this when
- agent call の prompt 構成、policy の選択・注入、placeholder の統合方針を確認したいとき。
- oracle／realization、file access、routing、feedback、INDEX.md エントリーなどの prompt 規定の構築箇所を探すとき。
- エディタへ渡す初期 prompt や、placeholder 置換値の型定義を確認したいとき。

## Do not read this when
- 個別 policy の意味仕様や正本規定そのものを確認したいときは、対応する仕様文書を直接読む。
- 実際の placeholder 置換処理、プロンプト生成全体の実装詳細、または個別の oracle／realization ファイルだけを確認したいとき。
- 構造化文書ノードの定義や Markdown レンダリング仕様を確認したいときは、struct_doc の実装を直接読む。

## hash
- 202b5294d9d93e0190edf37cad00ab13d1757028a86034f80cb25c6f39a4cdbe
