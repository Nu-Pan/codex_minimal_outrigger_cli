# `index_entry.json`

## Summary
- cmoc indexing の目次情報生成 agent call が返す、INDEX.md エントリー用の意味情報を定義する Structured Output schema。
- 生成結果を、対象の役割、読むべき条件、読まなくてよい境界を表す自然言語配列に限定し、余分な項目を受け付けない出力契約として使われる。

## Read this when
- INDEX.md エントリー生成 agent call の返却値として、どの意味情報が必須かを確認したいとき。
- cmoc indexing が生成結果を Markdown の目次情報へ変換する前提となる Structured Output schema を確認したいとき。
- エントリー生成結果が不正として扱われる原因を、出力契約の側から確認したいとき。

## Do not read this when
- INDEX.md エントリー生成 prompt の文面や agent call パラメータ構築を確認したいときは、対応するビルダー実装を読む。
- cmoc indexing の対象列挙、ハッシュ判定、並列実行、コミット処理を確認したいときは、indexing サブコマンドの実装または正本仕様を読む。
- 生成済み INDEX.md の Markdown 表示形式やレンダリング処理だけを確認したいときは、Structured Output を消費するレンダリング実装を読む。

## hash
- 47e9c5375a67b63817553f33e25546c4b56567bafc5641fd01f65f2502442bc8

# `index_entry.py`

## Summary
- `cmoc indexing` でファイルまたはディレクトリの内容からルーティング文書用エントリーを生成させるための、AI エージェント呼び出しパラメータを組み立てる実装。対象パスを実パス化し、読み取り専用・効率モデル・低 reasoning effort・構造化出力 schema を指定した完全プロンプトを生成する入口になる。
- 生成プロンプトには、既存の目次情報を根拠にしないこと、対象本文を主根拠にすること、必要に応じて関連文書を参照できること、対象本文そのものを含めることを組み込む。

## Read this when
- `cmoc indexing` の目次情報生成で、AI に渡す role・summary・goal・補助プロンプト・Structured Output schema の指定方法を確認または変更したいとき。
- 目次情報生成対象のパスや本文が、どのように `AgentCallParameter` のプロンプト本文へ埋め込まれるかを追いたいとき。
- インデックスエントリー生成時のファイルアクセスモード、モデルクラス、reasoning effort、出力 schema の紐付けを確認したいとき。
- 対象がディレクトリの場合に直下の目次本文が入力内容として渡される前提を確認したいとき。

## Do not read this when
- 既存の目次情報そのものの内容、各ディレクトリのルーティング方針、または生成済みエントリーの良し悪しを確認したいだけのとき。
- プロンプト部品の共通構築処理、Markdown レンダリング、構造化文書表現、パス解決、またはエージェント呼び出し型の定義そのものを調べたいとき。
- `cmoc indexing` の CLI 引数解析、対象ファイル探索、生成結果の保存、またはコマンド実行フローを調べたいとき。
- INDEX.md を読んで作業対象を選ぶルーティング利用側の挙動を調べたいとき。

## hash
- 884a0801f0878fbe06cc0249fe6eb968c0caca3401325ce0681abfe8d748a684
