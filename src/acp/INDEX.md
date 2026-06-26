# `builder`

## Summary
- AI エージェント呼び出しパラメータを組み立てる実装群の入口。apply、oracle review、session join、TUI 実行前判定、INDEX.md エントリー生成など、各用途の prompt 内容、補助入力、ファイルアクセス条件、モデル設定、Structured Output 契約への接続を扱う。
- 実際の CLI 実行制御や git 操作、標準文書本文、汎用 prompt 部品そのものではなく、用途別にエージェントへ何を渡し、どの制約で何を返させるかを確認するための領域。

## Read this when
- cmoc の各サブ機能が AI エージェントを呼び出す際の role、goal、補助 prompt、対象パスや差分などの入力埋め込み、読み書き権限、モデルや reasoning effort の指定を確認・変更したいとき。
- apply fork 後の差分要約、realization file の所見列挙、検出済み所見への修正依頼など、apply 系の後段エージェント呼び出し条件と出力契約を追いたいとき。
- oracle review で、新規所見、理由追加、採否判定、所見整理を生成させる prompt と、正本仕様断片を根拠にした Structured Output schema を確認したいとき。
- session join の merge conflict marker 解消や、TUI 実行前のファイルアクセスモード・標準参照要否判定など、特定用途の事前解決エージェント呼び出しを調べたいとき。
- INDEX.md エントリー生成で、対象本文の渡し方、既存目次を根拠にしない方針、読み取り専用条件、出力 schema 指定を実装・検証したいとき。

## Do not read this when
- サブコマンド全体の実行順序、CLI 引数解析、git 操作、フォーク作成・統合、merge conflict marker 検出、生成結果の保存など、エージェント呼び出しパラメータ構築の外側を調べたいとき。
- oracle file、realization file、review standard、apply review standard、realization standard など、prompt に含められる標準文書や仕様本文そのものを読みたいとき。
- 汎用的な prompt 部品、Markdown rendering、構造化ドキュメント表現、パス解決 helper、AgentCallParameter の基本定義だけを確認したいとき。
- 個別の所見カテゴリやレビュー判断基準、実際の対象ファイル探索、git diff 生成、変更ファイル抽出アルゴリズムなど、呼び出しに渡す材料を作る側の詳細を調べたいとき。
- 生成済み INDEX.md の内容評価や、ルーティング文書一般の書き方だけを確認したいとき。

## hash
- 841d3789d8ef7a945918bcbf8698e7b6ef089bc26fc78778ab6c055169f75648

# `prompt_parts`

## Summary
- AI agent に渡す ACP 向けプロンプトを構成する部品群を扱う領域。基本概念、ファイルアクセス制約、ルーティング規則、各種レビュー・実装・仕様記述の標準、案内エントリー生成標準を構造化文書として組み立てる実装がまとまっている。
- 個別の規範本文を生成する部品と、それらを必要条件に応じて完全なプロンプトへ組み込む制御の入口を含むため、agent call 前に提示される自然言語指示の内容と構成を追う起点になる。
- oracle file と realization file の責務境界、正本仕様断片の扱い、realization file の品質基準、レビュー所見の基準、案内エントリーの書き方など、AI に渡す標準プロンプトの意味的な根拠を確認するための下位要素へ進む場所である。

## Read this when
- ACP 向けに AI agent へ渡すプロンプト全体または標準プロンプト部品の構成・順序・有効化条件を確認したいとき。
- ファイルアクセス規則、ルーティング規則、oracle と realization の基本概念、oracle 標準、realization 標準、レビュー標準、案内エントリー標準のいずれかの文面を確認または変更したいとき。
- 新しい標準プロンプト種別を追加し、既存の構造化文書部品や完全プロンプトへの組み込み方に合わせたいとき。
- oracle file と realization file の照合レビュー、oracle file 単体レビュー、または INDEX.md エントリー生成で、AI にどの判断基準を提示しているかを調べたいとき。
- agent に提示される role、summary、goal、ファイルアクセス制限、ルーティング規則、補助プロンプト、標準プロンプトがどのように一連の構造化文書へ統合されるかを追いたいとき。

## Do not read this when
- 特定の CLI サブコマンド、状態ファイル、path model、入出力 schema、永続化処理など、プロダクト本体の具体的な挙動を調べたいとき。
- 構造化文書、標準、要求といった共通データ型や、それらの出力形式・変換処理そのものを変更したいとき。
- 個別の oracle file や realization file の本文内容を確認したいだけで、AI に渡す標準プロンプトの文面や構成を扱わないとき。
- テスト実装、fixture、外部コマンド実行、agent 呼び出し後の制御フローなど、生成済みプロンプトを使う側の処理を追いたいとき。
- 案内エントリーを作る対象本文の責務を確認したい段階で、既に対象の本文ファイルや対象ディレクトリが特定できているとき。

## hash
- 1c19cb8c7d184a81adbe3c863c8a812a3cbcde9fe24fac450843aedc35b42188
