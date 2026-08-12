# `acp_builder`

## Summary
- AI エージェント呼び出しの基礎モデル、用途別の prompt・起動パラメータ定義、および oracle・realization・session・tui・indexing・feedback・quota probe 向けの構築処理を扱う領域。共通の呼び出し契約を確認した後、目的に対応する下位定義へ進むための入口。

## Read this when
- AI エージェント呼び出しの共通パラメータ、または用途別の prompt・モデル・推論強度・アクセス権限・作業ディレクトリ・事前 indexing 設定を確認・変更するとき
- indexing、feedback、quota probe、oracle、realization、session join、tui の agent call 構築定義を調査するとき

## Do not read this when
- 通常のサブコマンド実行フロー、agent call の実行処理、または個別の oracle・realization ファイルの内容を確認するとき
- Structured Output の項目・型・形式だけを確認するときは、対応する下位 schema を直接読む
- 共通の ACP builder 実装や、バックエンド固有のモデル解決・ファイルアクセス規則だけを確認するときは、それぞれの直接の定義へ進む

## hash
- a3de673dfc2a30e15090d4da8ddd32a123ce481aabc3d0d78bd8849003cbe51e

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
- agent call 向けの完全な構造化 prompt を組み立てる実装群。placeholder 定義、静的・動的 prompt の統合、エディタ入力文面、各種規範や routing・feedback・access rule の構築部品を扱い、prompt 生成経路を確認する際の入口となる。

## Read this when
- prompt builder の構成や、agent call 用 prompt の生成・統合順序を調査するとき。
- oracle・realization・レビュー・routing・human feedback・file access などの標準規範が、どの部品から構築されるか確認するとき。
- placeholder の定義、エディタ入力の初期文面、構造化 prompt の組み立てを変更・レビューするとき。

## Do not read this when
- 個別の oracle 文書、realization 実装、realization test の内容を調査するとき。
- prompt builder を呼び出す上位の選択処理や agent call の実行方法だけを確認したいとき。
- Structured Output schema や構造化文書型そのものだけを確認したいときは、該当する型定義を直接読む。

## hash
- 4787824fd631ba0053b4c988234b7bb60c67df522d38c788abc57a83774c9e0e
