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
- ACP の agent call 用プロンプトを構成する標準部品群を扱う実装ディレクトリ。基本概念、ファイルアクセス規則、ルーティング規則、oracle / realization / review / INDEX.md エントリー生成の各標準文書を、構造化文書として組み立てる入口を含む。
- 完全なプロンプト構成を作る実装から参照される下位要素群であり、標準プロンプトの本文、依存関係、有効化条件、各レビュー・生成タスクで AI に渡す規範文を確認するための入口になる。

## Read this when
- ACP が agent に渡すプロンプト本文のうち、標準規範や作業ルールの文面がどこで生成されるかを確認したいとき。
- oracle file、realization file、レビュー、apply review、INDEX.md エントリー生成などの標準プロンプトを追加・変更・削除したいとき。
- 完全なプロンプトに含まれる標準部品の組み立て順、依存する標準文書の自動有効化、または基本要素との関係を確認したいとき。
- ファイルアクセス制限や INDEX.md による読み進め方など、agent に提示される共通ルール文の生成内容を確認・変更したいとき。
- oracle file と realization file の責務境界、各種標準、レビュー所見の判断基準を、agent 用プロンプトとしてどう表現しているかを調べたいとき。

## Do not read this when
- 特定サブコマンドの実行処理、CLI 引数、外部プロセス起動、永続状態、入出力 schema などの具体的な実装挙動を調べたいとき。
- プロンプト部品が生成する規範本文ではなく、構造化文書型、Standard 変換、複数行文字列整形などの共通ユーティリティだけを確認したいとき。
- パスキーワードや root path の定義そのものを確認したいときは、パスモデル側を読む方が直接的である。
- 個別の oracle file が定めるプロダクト仕様や、テスト対象の具体的な期待挙動を確認したいとき。
- INDEX.md エントリーの文面を作るために対象本文がすでに特定できており、このディレクトリのプロンプト生成実装を確認する必要がないとき。

## hash
- 00f737082d5d84a6fc729b9331acf9719988f25cdac49f6bfcb81a64245bf80d
