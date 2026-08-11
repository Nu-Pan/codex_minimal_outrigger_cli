# `acp_builder`

## Summary
- `oracle/acp_builder` 配下の正本ソース本文を確認するための入口。AI コーディングエージェント呼び出しに使う共通モデル、用途別の呼び出し定義、prompt・実行条件・Structured Output 契約を扱う下位領域へ進む起点となる。

## Read this when
- agent call の共通パラメータやモデル・推論強度・ファイルアクセス設定を確認するとき
- indexing、feedback、oracle、realization、session、tui など用途別の agent call 定義を調査・変更するとき
- 配下の正本ソースの有無や、agent call 関連の Structured Output 契約の入口を確認するとき

## Do not read this when
- 通常のコマンド処理や agent call の生成処理そのものを確認するとき
- oracle file の仕様本文や、実際の INDEX.md のルーティング内容を確認するとき
- agent call と無関係な実装仕様や処理内容だけを調査するとき

## hash
- e3f65e061b3e6a1edf89366c9a62f61b94dcc1f4f634db51cbac70346111412a

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
- oracle の共通基盤実装をまとめた領域。リポジトリ設定、agent call のパスモデル、agent 向け instruction 標準、階層構造を持つ文書モデルと Markdown レンダリングを扱う。各機能の共通データモデルや変換処理を確認する入口となる。

## Read this when
- cmoc の設定項目や既定値、Codex CLI の provider・モデル・推論 effort、oracle review のループ設定を確認・変更するとき。
- agent call の cwd、repository root・work root・run root の導出、root placeholder、実パス変換、worktree 境界を確認・変更するとき。
- agent 向け instruction の標準形式、要求項目のデータモデル、標準から構造化文書への変換を確認するとき。
- 構造化文書のモデル、Markdown レンダリング、cmoc_block 参照検証、見出し深度計算、空行や文字列正規化を確認・変更するとき。

## Do not read this when
- 永続化された設定 JSON の生成・同期・調整だけを確認するときは、対象の設定ファイルや doctor 実装を直接読む。
- ModelClass や ReasoningEffort の列挙値だけを確認するときは、参照元の型定義を直接読む。
- CLI の具体的なサブコマンドや agent call prompt の生成処理だけを調査するときは、それぞれの直接実装を読む。
- 個別の instruction 本文や構造化文書の正本仕様だけを確認するときは、対応する仕様文書を読む。
- 一般的な Markdown 生成や、この領域のモデルを使わない機能を調査するときは、対象機能へ直接進む。

## hash
- 41ef3ab12e8ab887215a10fe786213665fa3bcc98dd488914539686c0e287ec1

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
