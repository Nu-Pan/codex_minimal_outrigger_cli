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
- ACP の agent 向けプロンプトを構成する再利用可能な prompt part 群を扱うディレクトリ。
- ファイルアクセス規則、ルーティング規則、oracle/realization の基本概念と標準、レビュー標準、INDEX.md エントリー標準などを、構造化ドキュメントとして生成する実装への入口となる。
- 完全な agent プロンプトを組み立てる処理から参照される標準プロンプト部品の責務や依存関係を確認するための起点になる。

## Read this when
- ACP が agent に渡す標準プロンプト断片の内容、構成、追加条件、組み立て順を確認または変更したいとき。
- ファイルアクセス制約、INDEX.md を使った読み進め方、oracle file と realization file の責務境界、各種標準文書のいずれかを agent prompt に含める処理を扱うとき。
- oracle file や realization file の品質基準、レビュー所見の判断基準、INDEX.md エントリーの品質基準を、実装から生成される文章として確認したいとき。
- 標準プロンプト同士の依存関係や、フラグ指定によってどの標準文書が最終プロンプトに含まれるかを追いたいとき。

## Do not read this when
- 個別サブコマンドの CLI 挙動、状態ファイル、path model、出力 schema などの具体仕様や実装詳細だけを探しているとき。
- 構造化ドキュメントや標準文書を表す共通データ型、レンダリング処理、低レベルの整形仕様だけを確認したいとき。
- 特定の oracle file や realization file の本文に書かれた仕様内容そのものを確認したいとき。
- 通常の機能実装、テスト追加、リファクタリング作業で、agent prompt に提示される標準文書の内容や生成条件を変更しないとき。

## hash
- 514be3968c0697d9b5fca9df08ff9310346af275ec8eb134909d3f6cc2dc514e
