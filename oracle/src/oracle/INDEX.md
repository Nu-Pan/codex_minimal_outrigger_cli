# `acp_builder`

## Summary
- AI エージェント呼び出しに必要な共通データモデルと、indexing・oracle・realization・session・TUI・quota probe など用途別の起動定義を扱う領域。各用途の prompt、Structured Output、実行権限、作業ディレクトリ、モデル・推論設定を確認するための入口。

## Read this when
- AI エージェント呼び出しの共通パラメータや用途別の起動条件を調査・変更するとき
- 特定用途の prompt、出力契約、アクセスモード、モデル、推論強度、cwd、preflight 設定を確認するとき
- 配下の用途別定義へ進む前に、どの領域を読むべきか判断するとき

## Do not read this when
- 対象用途の具体的な prompt や Structured Output の詳細を直接確認できるとき
- 共通 prompt 生成規則だけを調べるとき
- 実際の agent call 実行処理、対象ファイルの仕様、または通常の session join 処理を調べるとき

## hash
- c7c42a03da38420de26179d512fb58089a41df5d20b9b01745203e40f9345d89

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
- agent call 向けの構造化プロンプトを組み立てるモジュール群。完全 prompt の統合、エディタ入力文面、placeholder 型、oracle・realization・レビュー・アクセス制限・routing などの規則部品を扱い、prompt 生成経路や個別 builder の責務を調べる際の入口となる。

## Read this when
- agent 向け prompt の構成や builder の組み合わせを変更・調査するとき。
- oracle、realization、レビュー、human feedback、ファイルアクセス、INDEX routing などの標準規則を prompt に組み込む経路を確認するとき。
- エディタ入力用の初期文面や placeholder 表現の定義を確認・変更するとき。

## Do not read this when
- 個別の oracle 文書、realization 実装、realization test の内容を調査するとき。
- prompt builder を呼び出す側の選択処理や agent call 全体の挙動だけを調べるとき。
- 既存の INDEX.md のルーティング情報だけを確認・更新するとき。
- Structured Output schema の形式や、ファイル名・hash など機械的な識別情報だけを確認するとき。

## hash
- 1f27c8649a6d8312ae1c40de828b871ea0455b77b2b09f790bf4b2cbe54dad88
