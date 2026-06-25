# `builder`

## Summary
- AI エージェント呼び出しに渡す AgentCallParameter、prompt、Structured Output schema、model class、reasoning effort、ファイルアクセス権限を、用途別に組み立てる builder 群をまとめる領域。
- 適用・分岐処理、目次エントリー生成、oracle file レビュー、merge conflict 解消、TUI 実行前パラメータ選定など、各機能が AI に何を読ませ、どの構造化結果を期待し、どの実行条件で呼び出すかを確認する入口になる。
- CLI 実行フローや Git 操作そのものではなく、各機能から別 AI エージェントへ委譲する際の契約、入力文脈、出力 schema、権限・モデル設定を追うためのまとまり。

## Read this when
- cmoc の各機能が AI エージェントを呼び出す際の prompt 構成、補助文脈、Structured Output schema、モデル種別、reasoning effort、ファイルアクセス権限を確認または変更したいとき。
- 変更要約、レビュー所見列挙、所見への修正依頼、目次エントリー生成、oracle file レビュー、merge conflict marker 解消、TUI 実行前の実行パラメータ選定のいずれかに関する AI 呼び出し契約を探したいとき。
- 対象ファイル、差分、既存所見、oracle file、ユーザー入力、conflict 対象パスなどの入力が、AI 向け complete prompt や構造化出力へどう接続されるかを追いたいとき。
- 機能ごとに、どの標準文書や補助情報を prompt に含めるか、どの読み書き権限で別エージェントへ渡すかの境界を確認したいとき。

## Do not read this when
- サブコマンド登録、CLI 引数解析、実行制御、Git コマンド、branch 作成、差分取得、conflict 検出、結果保存など、AI 呼び出しを使う側の処理フロー本体だけを調べたいとき。
- AgentCallParameter の基礎型、共通 prompt 構築、Markdown rendering、パス解決、論理ファイルアクセスモードなど、複数機能で使われる共通部品そのものの実装詳細を調べたいとき。
- oracle standard、realization standard、review standard、INDEX.md エントリー標準、path keyword など、prompt に同梱または参照される仕様本文自体を読みたいとき。
- 個別の oracle file、変更対象ファイル、テスト、conflict 本文の内容を直接確認したいだけで、AI 呼び出し条件や出力契約を変更しないとき。

## hash
- e9596524e64090f46752d08c68c7cda5785bc4b4b02b1d75cb06241f5f99c374

# `prompt_parts`

## Summary
- AI agent に渡す標準プロンプト部品を構築する実装群を収める領域。ファイルアクセス規則、ルーティング規則、oracle/realization の基本概念、oracle・realization・review・INDEX.md エントリーの各標準、完全なプロンプト列の組み立てを扱う。
- 個別の規範文章を構造化文書として生成する部品と、それらを依存関係に従って agent call 用の完全なプロンプトへまとめる入口を探すためのルーティング先である。

## Read this when
- agent に渡すプロンプトへ、どの標準規範や基本情報を含めるか、またはどの順序・依存関係で組み立てるかを確認したいとき。
- ファイルアクセス規則、INDEX.md を使った読み進め方、oracle file と realization file の責務境界など、AI agent 向けの共通説明文を生成する処理を変更したいとき。
- oracle file、realization file、oracle review、apply review、INDEX.md エントリーに関する標準プロンプト本文の生成内容や判断基準を確認したいとき。
- 新しい標準プロンプト部品を追加する、既存の標準プロンプトを削除・分割・統合する、または完全なプロンプトへの組み込み条件を調整したいとき。

## Do not read this when
- 特定サブコマンドの CLI 引数、入出力 schema、永続状態、path model、実行フローなど、プロンプト文面ではなくプロダクト挙動そのものの仕様や実装を探しているとき。
- agent call の外部プロセス起動、標準入力・標準出力の処理、実行結果の利用側など、生成されたプロンプトを渡した後の処理を調べたいとき。
- 構造化文書の共通データ型、整形 helper、標準文書変換の低レベル実装だけを確認したいとき。
- 個別の oracle file や realization file が定める具体的な機能仕様を読みたいとき。

## hash
- db8b24372e8fdb9ab29f2c9a08e61562784d0e2f8229ff855de4fe38fd73642c
