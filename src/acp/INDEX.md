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
- ACP で AI agent に渡すプロンプトを構成する部品群を扱う領域。ファイルアクセス規則、INDEX.md ルーティング規則、oracle と realization の基本概念、oracle・realization・レビュー・案内エントリー生成の各標準規範を、構造化文書として組み立てる実装がまとまっている。
- 個別の標準プロンプト本文を生成する部品だけでなく、依頼の role・summary・goal、任意追加文書、各種標準プロンプト指定を結合し、依存する基礎情報を補って agent に渡せる完全なプロンプト列へ整える入口も含む。
- 下位要素は、規則本文や標準本文そのものを確認・変更したい場合の読む先と、複数の prompt part をどの順序・依存関係で最終プロンプトへ組み込むかを確認する読む先に分かれる。

## Read this when
- ACP 経由で AI agent に提示されるプロンプト本文が、どの規則・標準・基礎説明から構成されるかを確認したいとき。
- ファイルアクセス制約、INDEX.md の使い方、oracle file と realization file の関係、oracle 標準、realization 標準、レビュー標準、案内エントリー標準のいずれかのプロンプト文面を確認・変更したいとき。
- 標準プロンプトの有効化に応じて、oracle/realization の基本説明や他の標準規範がどのように依存追加されるかを追いたいとき。
- agent に渡す前に root token や呼び出し元表現がどのように実パス・依頼者向け表現へ変換されるかを確認したいとき。
- プロンプト部品が `StructDoc` としてどの粒度でまとめられ、背景・要求・例を含む規範集合として出力されるかを把握したいとき。

## Do not read this when
- 構造化文書、標準、要求項目、コードブロックなどの基盤データ型そのものを調べたいときは、それらを定義する基盤側を読む。
- root token、作業ルート、実パス解決、パス概念の正本仕様や実装を確認したいときは、パスモデル側を読む。
- agent 実行、サブプロセス起動、LLM 呼び出し、ACP セッション制御など、構築済みプロンプトを利用する側の処理を調べたいとき。
- 特定の CLI サブコマンド、状態ファイル、出力 schema、ユーザー操作の実挙動を確認したいときは、その挙動を実装する領域を直接読む。
- 個別の規範本文ではなく、既存テストの期待値やテスト fixture を確認したいときは、対応するテスト側を読む。

## hash
- 4324c579581bdb347df20760fbd57da6b3acbec94537b3a5f419ffe0db8a31c1
