# `acp_builder`

## Summary
- AI コーディングエージェント呼び出しの prompt と起動パラメータを構築する定義をまとめた領域。
- 共通の呼び出しパラメータとファイルアクセスモードを基盤に、indexing、TUI、quota probe、session join、feedback、oracle、realization の各 agent call 構築へ進む入口を提供する。
- oracle review と realization refactor では、所見の列挙・検証・判定・統合や変更要約・ファイル単位のレビュー修正など、処理段階ごとの出力契約も扱う。

## Read this when
- agent call の prompt、cwd、ファイルアクセスモード、Structured Output、editor input handoff、indexing preflight の構築を確認するとき
- 特定の cmoc サブコマンドに対応する agent call の構築箇所を探すとき
- feedback issue、oracle review、realization の処理段階ごとの入力・出力契約を確認するとき

## Do not read this when
- 論理的なファイルアクセスモードの詳細な意味や Codex CLI sandbox との対応を確認したいときは、本文が参照する正本仕様を読む
- agent call の実行処理、サブコマンドの業務ロジック、または prompt の共通生成規則を確認したいときは、対応する実行本体・サブコマンド実装・共通 prompt builder を直接読む
- Structured Output の機械的な受理条件だけを確認したいときは、各下位領域の schema を直接読む
- 個別の oracle file、realization file、feedback state の内容やレビュー結果そのものを確認したいとき

## hash
- 3c007304ded3c11a82abad325490e2ec0fc53a9c73aa98ae9d0e271762a61f19

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
- プロンプト生成を構成する共通型、完全 prompt、エディター入力、基本概念、policy 群の入口。
- agent 向け prompt の構成や、prompt builder 内の規定・入力生成・共通定義を確認するための上位ルーティング先。

## Read this when
- agent call に渡す prompt の構成要素や統合責務の所在を確認したいとき。
- prompt builder 内で、共通型、完全 prompt の組み立て、エディター用初期入力、oracle・realization の基本概念、各種 policy のどの領域を読むべきか判断したいとき。
- 複数の prompt builder 部品にまたがる変更や、prompt 生成に関する入口を特定したいとき。

## Do not read this when
- 特定の policy、共通型、完全 prompt、エディター入力、oracle・realization の基本概念の詳細だけを確認したいときは、該当する下位対象を直接読む。
- 実際の prompt 利用側、CLI の実行処理、個別の oracle・realization 文書や実装の内容を確認したいとき。
- prompt builder と無関係な構造化文書や一般的な Markdown 表現の仕様を確認したいとき。

## hash
- e11370a4e730df42b5d0a3ec72dff640d9e6fcb6783ab2e0f12e14f33e81b6f0
