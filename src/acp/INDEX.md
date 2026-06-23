# `builder`

## Summary
- AI エージェント呼び出しに渡すパラメータと構造化応答契約を、適用支援、ルーティング文書生成、oracle file レビュー、session 系 conflict 解消の各用途ごとに組み立てる実装領域。
- 各用途で必要な role、goal、補助 prompt、読み書き権限、model、reasoning effort、参照標準、Structured Output schema の対応を確認する入口になる。
- 実際のサブコマンド実行、git 操作、ファイル走査、結果保存ではなく、上位処理から呼び出される補助 AI への依頼内容と応答形式を定義する。

## Read this when
- 適用処理、INDEX.md エントリー生成、oracle file レビュー、session join の merge conflict marker 解消で、補助 AI に渡す AgentCallParameter の内容を確認または変更したいとき。
- 変更差分の要約、realization file への所見列挙、所見リスト整理、所見に基づく realization file 修正支援など、適用前後のレビュー・修正・レポート生成を支える AI 呼び出し仕様を追いたいとき。
- INDEX.md エントリー生成で、対象本文を prompt に埋め込み、既存目次ではなくオリジナル本文を根拠に構造化出力を得る制約や実行条件を確認したいとき。
- oracle file レビューで、新規所見検出、所見整理、擁護理由・反証理由の列挙、最終採否判定に使う prompt、ファイルアクセス方針、応答 schema を確認したいとき。
- session join の conflict 解消支援で、対象パス一覧、作業範囲、oracle file の例外的な最小編集許可、git add/commit 禁止などが補助 AI へどう伝わるかを調べたいとき。

## Do not read this when
- CLI 引数解析、サブコマンド登録、通常の実行制御、ブランチ作成、merge 実行、差分取得、git コマンド実行など、上位フローや外部操作そのものを調べたいとき。
- INDEX.md のファイル走査、読み書き、生成結果の保存、適用後レポートやレビュー結果の集約・通知・UI など、AI 呼び出し後の処理を調べたいとき。
- path keyword、real path、work root、FileAccessMode、AgentCallParameter、StructDoc、complete prompt 構築など、複数領域で使われる共通型・共通 helper そのものを変更したいとき。
- oracle file、realization file、各 standard の定義本文や、個別の正本仕様断片・実装対象ファイルの内容を確認したいとき。
- 生成済みの個別 INDEX.md エントリー内容や、特定ファイル・ディレクトリのルーティング品質だけを確認したいとき。

## hash
- f607008ebe9c6d7d8803bea7613902fe1da8fefaf31d4efe8d30a61d58e1c9a9

# `prompt_parts`

## Summary
- AI agent に渡す構造化プロンプトの部品を生成する実装群をまとめる領域。基本プロンプト、ファイルアクセス規則、ルーティング規則、oracle / realization の概念説明、各種標準文書、レビュー判断基準、INDEX.md エントリー規範などを扱う。
- 個別の標準文書本文を構築する対象と、それらを依存関係に従って完全なプロンプト列へ組み立てる対象への入口になる。
- cmoc が agent call に渡す規範・制約・作業指示をどのような構造化文書として生成するかを確認するための実装上の集約地点である。

## Read this when
- agent に渡すプロンプト全体の構成、基本要素、標準プロンプトの追加条件や依存関係を確認したいとき。
- ファイルアクセス規則、INDEX.md を使った読み進め方、oracle file と realization file の関係など、AI agent へ提示する共通規則の文面生成を調整したいとき。
- oracle file、realization file、レビュー所見、INDEX.md エントリーに関する標準文書や判断基準が、どのプロンプト部品として生成されるかを確認したいとき。
- 新しい標準プロンプト部品を追加する、既存の規範文書生成を変更する、または完全なプロンプトへの組み込み順や有効化条件を調整するとき。

## Do not read this when
- 特定の CLI サブコマンド、path model、状態ファイル、入出力 schema などの個別機能仕様や実装詳細を探しているとき。
- 構造化文書の共通データ型、標準文書の変換 helper、agent call の実行処理、外部プロセス起動など、プロンプト部品の利用側や基盤実装を確認したいとき。
- oracle file そのものの正本仕様断片や、特定の実装・テストの本文を確認したいだけで、agent 用プロンプト文面の生成には関心がないとき。
- INDEX.md エントリーの実際の文面だけを対象本文から作りたいときは、必要な標準を確認した後、対象本文を直接読む方が適切である。

## hash
- 301e1caa796138766a33b5f9b34750fc8afbf6b5715432ece7c11ebaf38f2cc0
