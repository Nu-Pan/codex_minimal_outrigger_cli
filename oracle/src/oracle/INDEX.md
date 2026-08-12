# `acp_builder`

## Summary
- 対象ディレクトリには、agent call の共通データモデルやサブコマンド別の呼び出し定義が置かれており、各処理の prompt・モデル・推論強度・ファイルアクセス・Structured Output 連携を確認するための入口です。
- 基本的な AgentCallParameter の契約は `basic.py`、indexing・oracle・realization・session・tui・quota probe など個別用途の呼び出し構築は対応するサブディレクトリまたはモジュールへ進みます。

## Read this when
- agent call の共通パラメータ契約、モデル選択、推論強度、ファイルアクセスモードを確認・変更するとき
- indexing、oracle、realization、session、tui、quota probe、feedback など特定用途の prompt や起動設定を確認・変更するとき
- agent call と Structured Output schema、indexing preflight、作業ディレクトリの接続を調査するとき

## Do not read this when
- 通常の INDEX.md の内容や生成対象ファイル自身の責務だけを調べるとき
- バックエンド固有のモデル名解決や具体的なアクセス規則の文面だけを確認するとき
- agent call の実行処理や個別の生成・適用ロジックだけを調べるときは、対応する実装を直接読む

## hash
- 257bec0b102f75dd942bdfc0e7af3f5a80756416aabb9617452efd3ae174e8b7

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
- cmoc のリポジトリ固有設定を集約するデータクラス群を定義する。JSON/TOML 共通値、Codex CLI の provider・モデル・推論 effort、oracle review のループ上限を扱う設定構造の入口。
- cmoc のパス表記に用いる root placeholder と、agent call 単位の work root・repository root を表現するモデルを定義する。placeholder 付きパスの解決、Git worktree・repository root の探索、実パスから placeholder 表記への変換を担う。
- agent 向け instruction の要求文面を構造化する標準と、その要求項目を表すデータモデルを定義する。標準の保持と StructDoc への変換処理の入口を担う。
- 構造化文書の要素を見出し階層付き Markdown へ変換するヘルパーを提供する。文書構造、参照可能なブロック、コードブロックを表現し、参照先やブロック ID の検証、文字列のインデント正規化を担う。

## Read this when
- cmoc の設定項目や既定値、Codex CLI のモデル設定、ファイルアクセス規則違反時のリカバリ回数、または oracle review のループ設定を変更・確認するとき。
- cmoc のパス placeholder、agent call の作業コンテキスト、worktree や repository root の探索・変換規則を変更・調査するとき。
- agent 向け instruction の標準形式、要求ラベル、Standard・Requirement の生成や StructDoc への変換を調べるとき。
- Markdown をプログラムで組み立てる処理、見出し階層、cmoc_block・cmoc_ref、コードフェンス、参照検証の挙動を変更・調査するとき。

## Do not read this when
- 永続化された設定 JSON の生成・同期・人手調整だけを確認するときは、対象の設定ファイルや doctor 実装を直接読む。列挙型の値だけを確認するときは、その型定義を直接読む。
- パスモデルを利用する個別機能だけを確認するとき、またはパス解決と無関係な一般的な CLI・oracle・realization 仕様を読むとき。
- 個別の instruction 本文や StructDoc の一般仕様だけを確認するとき、または標準データモデルを使わない oracle 実装・テストを調べるとき。
- 通常の Markdown 記述や構造化文書を使わない文書生成処理を確認するとき、またはレンダリング実装の挙動が目的でないとき。

## hash
- 457a12faf12238fa7b95ede55e89ce82363626bd49c2bcdf1cff218b5f721ad0

# `prompt_builder`

## Summary
- プレースホルダ名を実パスや文字列へ対応付ける型定義を置く。置換対象を共通表現で扱う必要がある場合の入口。
- 選択した規則・補助プロンプト・動的な役割情報を統合し、placeholder を解決して完全な agent prompt を構築する。prompt の統合順序や規則の有効化条件を確認する入口。
- エディタ経由で後続 AI エージェントへ渡すユーザー入力ファイルの初期表示文面を構築する。入力案内や完全 prompt の差し込み構造を扱う。
- oracle・realization の追従要否やレビュー基準、conflict 解消、human feedback、アクセス制限、INDEX.md ルーティング、oracle/realization の規範など、agent call 向け標準規則を構築する prompt 部品群。個別規則の生成経路を確認する入口。

## Read this when
- prompt builder の型定義、完全 prompt の統合処理、エディタ入力文面の構造を変更または確認するとき。
- 特定の agent call 向けに oracle、realization、review、routing、feedback、アクセス規則などの標準規範がどのように構築されるかを調査するとき。

## Do not read this when
- 個別の oracle 文書、realization 実装、realization test の内容を調査するとき。
- prompt builder 部品を組み合わせる呼び出し元や agent call 全体の選択処理を調べるときは、呼び出し元の実装を直接読む。
- 既存 INDEX.md のルーティング情報だけを確認・更新するとき。
- Structured Output schema の形式や、ファイル名・hash など機械的な識別情報だけを確認するとき。

## hash
- 6cf1b086cadb55f225321c3b47855deb1f9b7dccf576022213d9b31590a3e867
