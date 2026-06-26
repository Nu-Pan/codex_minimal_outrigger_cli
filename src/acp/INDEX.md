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
- `src/acp/prompt_parts` は、ACP agent に渡す構造化プロンプトの標準部品を組み立てる実装群です。ファイルアクセス規則、ルーティング規則、oracle/realization の基本概念、各種 standard、レビュー基準、INDEX.md エントリー基準を `StructDoc` として生成し、完全な agent prompt に依存関係込みで注入する入口も含みます。
- このディレクトリは、agent に提示されるプロンプト本文の内容や構成、標準プロンプト同士の依存関係、root token の実パス置換などを確認・変更するための入口です。

## Read this when
- ACP agent に渡す標準プロンプト部品の文言、構成、生成処理を確認・変更したいとき。
- ファイルアクセス規則、INDEX.md ルーティング規則、oracle/realization の基本説明、oracle/realization/review/index-entry 向け standard のどれがどの条件でプロンプトに含まれるか確認したいとき。
- agent call に渡す完全なプロンプトの組み立て順、追加プロンプトの差し込み位置、標準プロンプト間の依存関係、内部 root token や呼び出し元表現のサニタイズ処理を追いたいとき。
- cmoc が AI に渡す作業規範やレビュー規範を、自然言語の正本仕様ではなく Python 実装としてどこで構築しているか探したいとき。

## Do not read this when
- 個別 CLI サブコマンド、path model、状態ファイル、Git 操作、実行制御など、プロンプト部品ではない具体機能の仕様や実装を調べたいとき。
- 生成済みプロンプトを受け取った agent が実際にどう実行されるか、プロセス起動や ACP 通信の制御を追いたいとき。
- StructDoc、StructCodeBlock、Standard、Requirement、FileAccessMode、RootToken など、プロンプト部品が利用する基盤データ型や列挙値そのものの定義を確認したいとき。
- INDEX.md エントリーの対象本文がすでに個別ファイルまで特定できており、そのファイル単体の責務や文言だけを確認すればよいとき。

## hash
- 939c132501d123684bd14a51aed9662bd793ae0159b3b739fdb046968f542763
