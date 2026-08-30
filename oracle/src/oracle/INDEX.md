# `acp_builder`

## Summary
- AI コーディングエージェントの各種呼び出しに使う prompt、アクセスモード、cwd、Structured Output schema などの起動パラメータ構築をまとめる領域。
- indexing、feedback、oracle、realization、session、tui、quota probe など、用途別の agent call 定義へ進む入口を提供する。

## Read this when
- agent call の用途別 builder、prompt、ファイルアクセス設定、cwd、Structured Output schema、エディタ入力や preflight の指定を確認・変更するとき。
- 共通の呼び出しパラメータ定義から、indexing、feedback、oracle、realization、session、tui、quota probe の個別設定へ調査を始めるとき。

## Do not read this when
- agent call の実行処理、共通 prompt の生成規則、CLI サブコマンドの引数解析を確認したいときは、対応する実行本体や共通 builder を直接読む。
- 特定用途の出力項目・型・形式、個別 oracle や realization の仕様、レビューや conflict 解消の処理順序を確認したいときは、該当する下位ファイルを直接読む。

## hash
- 9e9a9fc78f7198e9df1dc52bdad46335dc248b9ceb73b5605482c1d87e7e7b90

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
- 日本語技術文書のルーティングエントリーを、対象ディレクトリ内の構造化文書・設定モデル・パスモデルの責務に基づいて整理します。

## Read this when
- cmoc の設定集約、パスコンテキストやプレースホルダ解決、構造化文書の Markdown レンダリングを調査・変更するとき。
- これらの実装対象のどれを入口にすべきか、またはディレクトリ内の関連モジュールの責務の境界を確認したいとき。

## Do not read this when
- 個別モジュールのフィールド定義、既定値、具体的な変換規則を確認したいときは、ルーティング情報ではなく該当ファイルを直接読むべきです。
- agent call の生成規則や index エントリー生成処理そのもの、または一般的な CLI 機能を調査するときは、別の仕様・実装対象を直接読むべきです。

## hash
- 01da7b21d4a4bb34d4188332c0c76f0719fcce78b2fcb31d8220c81697804620

# `prompt_builder`

## Summary
- プロンプト構築に関する共通型、完全 prompt の統合、エディタ初期入力、oracle／realization 概念、各種 prompt policy builder を扱う実装群への入口。
- placeholder の型定義から、policy の有効化・順序制御、衝突検出、完全 prompt やエディタ入力の生成まで、agent call 用プロンプトを組み立てる責務を分担する。

## Read this when
- agent call に渡す prompt の構成、policy の組み込み、placeholder 統合、またはエディタ入力の初期文面を確認・変更するとき。
- oracle／realization の基本概念やファイル分類を prompt に反映する処理、または prompt policy builder の責務を調べるとき。

## Do not read this when
- 個別 policy の根拠となる正本仕様、具体的な oracle 文書、実装・テストの詳細を確認するときは、それぞれの対象を直接読む。
- prompt 生成後の CLI 実行、ファイルアクセス、conflict 解消、Markdown 構造化文書の詳細を確認するときは、対応する実装を直接読む。

## hash
- 9fa2c0c8b03929044759263489ec8293b8010c9cd530a63420511275f1b0b7b4
