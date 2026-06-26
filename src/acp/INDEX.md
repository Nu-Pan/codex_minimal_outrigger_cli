# `builder`

## Summary
- AI エージェントを呼び出す前段で、各サブコマンドや工程ごとの AgentCallParameter と Structured Output schema の対応を組み立てる実装群への入口。
- 差分要約、実装所見の列挙と修正依頼、正本仕様断片レビューの所見列挙・検証・採否・整理、merge conflict marker 解消、TUI 実行前のパラメータ解決、ルーティング文書エントリー生成を扱う。
- 各工程でエージェントへ渡す role、summary、goal、補助文脈、標準文書参照、ファイルアクセスモード、model class、reasoning effort、返却 schema を確認するための領域。

## Read this when
- サブコマンドや工程が AI エージェントへどのような prompt と実行条件を渡すかを、機能領域別に探し始めたいとき。
- AgentCallParameter の構築内容と Structured Output schema の接続を、apply fork、review oracle、session join、tui、indexing のいずれかについて確認または変更したいとき。
- 差分要約、レビュー所見、所見対応作業、conflict 解消、TUI パラメータ選定、INDEX.md エントリー生成などの AI 呼び出し境界を追いたいとき。
- 各 AI 呼び出しで使うファイルアクセス権限、モデル種別、推論強度、標準文書断片、補助入力の埋め込み方を比較しながら確認したいとき。

## Do not read this when
- AI 呼び出しより上位の CLI 引数解析、サブコマンドの実行順序、状態保存、git 操作、対象ファイル探索などの実行制御を調べたいとき。
- prompt に含められる oracle standard、realization standard、review standard、apply review standard、index entry standard などの標準文書本文そのものを確認したいとき。
- StructDoc、Markdown rendering、AgentCallParameter、FileAccessMode、path 解決、complete prompt 生成など、複数領域で使われる共通基盤の型や helper を調べたいとき。
- 生成済みのレビュー所見、差分要約、INDEX.md エントリーなど、AI 呼び出し結果の保存・表示・利用側の挙動を確認したいとき。
- 特定工程の対象ファイルが既に分かっており、その工程固有の prompt 構築や schema だけを直接読めば足りるとき。

## hash
- f72a68ff48e10f4bbb4c1f88d877d3fb606c64fc9d46f223b9c3e49d987adcb2

# `prompt_parts`

## Summary
- AI agent に渡すプロンプトを構成する部品群を扱うディレクトリ。ファイルアクセス規則、ルーティング規則、oracle/realization の基本説明、oracle・realization・レビュー・INDEX.md エントリーの標準文書を構造化文書として組み立てる実装がまとまっている。
- 個別の標準文書本文を生成する部品と、それらを依頼内容・アクセスモード・追加プロンプト・有効化フラグに応じて完全な agent 用プロンプトへ集約する入口がある。

## Read this when
- AI agent に渡す最終プロンプトの構成、標準文書の注入順序、または有効化フラグ間の依存関係を確認・変更したいとき。
- ファイル読み書き制約、INDEX.md を使った読み進め方、oracle file と realization file の責務境界を、agent 向けプロンプトとしてどの文面で提示しているか確認したいとき。
- oracle file、realization file、oracle review、oracle-to-realization review、INDEX.md エントリー生成に関する標準文書の生成内容を確認・変更したいとき。
- 標準文書を構成する要求・背景・判断例が、どの構造化文書として agent prompt に組み込まれるかを追いたいとき。

## Do not read this when
- 特定の CLI サブコマンド、状態ファイル、path model、入出力 schema などの個別機能仕様や実装詳細を探しているとき。
- 標準文書を利用する側ではなく、構造化文書型、標準項目型、またはそれらの変換基盤そのものを確認したいとき。
- テスト実装や fixture の内容を確認したいとき。
- INDEX.md エントリーの完成文面だけが必要で、対象本文をすでに直接読める状態にあるとき。

## hash
- ac07129c880ae3dc8b3364000026c106640eb98405ec3b2a163479f01af1c160
