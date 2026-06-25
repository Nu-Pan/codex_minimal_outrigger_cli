# `builder`

## Summary
- AI エージェント呼び出し用のパラメータ構築処理と、その構造化出力 schema をまとめる領域。各サブコマンドの処理本体ではなく、別エージェントへ渡す role、summary、goal、補助文脈、参照標準、ファイルアクセスモード、モデル種別、reasoning effort、schema の対応関係を確認する入口になる。
- 扱う呼び出しは、実装所見の列挙・整理・修正・変更要約、目次エントリー生成、oracle file レビュー、merge conflict marker 解消、TUI 実行前のパラメータ選定に分かれる。目的別の下位領域へ進むことで、どの入力を prompt に埋め込み、どの権限と schema でエージェントを起動するかを追える。

## Read this when
- サブコマンドから AI Agent CLI/TUI へ渡す呼び出し条件を確認または変更したいとき。
- エージェント向け prompt に、対象パス、対象本文、git diff、所見、既知理由、conflict 対象、ユーザープロンプトなどの補助文脈がどう埋め込まれるかを追いたいとき。
- 用途ごとのモデルクラス、reasoning effort、論理ファイルアクセスモード、参照する標準、構造化出力 schema の対応関係を確認したいとき。
- レビュー、適用、目次生成、TUI パラメータ選定、conflict 解消のうち、実行フロー本体ではなく別エージェント呼び出しの契約や出力形式を調べたいとき。

## Do not read this when
- CLI のサブコマンド登録、引数解析、ファイル走査、git 操作、状態更新、結果保存、TUI 表示など、呼び出しパラメータ構築を使う側の実行フローを調べたいとき。
- 完全 prompt の共通組み立て、構造化 Markdown レンダリング、パス解決、AgentCallParameter やモデル種別の共通型定義そのものを変更したいとき。
- oracle file、realization file、各種 standard の本文や、レビュー基準そのものを確認したいとき。
- 実際の修正対象ファイル、テスト実装、merge conflict の具体的な解消内容、または個別コード変更の中身を調べたいとき。

## hash
- 8fcd61c197ffc06d38af2ed749a18ff735f3b31f600d8a26b2f455f23491c1a0

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
