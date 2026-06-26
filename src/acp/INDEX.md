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
- AI agent に渡すプロンプトを構成する標準部品群を集めた領域。oracle / realization の基本概念、各種標準、レビュー基準、ファイルアクセス規則、ルーティング規則、INDEX.md エントリー規範などを、構造化文書として生成する実装を扱う。
- 完全な agent prompt の組み立てに使われる個別プロンプト部品の責務と、標準プロンプト同士の関係を確認する入口になる。

## Read this when
- agent に渡すプロンプトへ、どの標準文書や規則文書が含まれるかを確認・変更したいとき。
- oracle file、realization file、レビュー、INDEX.md、ファイルアクセス、ルーティングに関する共通規範のプロンプト本文を確認・調整したいとき。
- 標準プロンプトの有効化フラグ、依存関係、注入順序、または基本プロンプトとの組み合わせを追いたいとき。
- AI agent に提示される作業規則の文面が、構造化文書としてどのように生成されるかを調べたいとき。

## Do not read this when
- 個別サブコマンドの CLI 挙動、状態ファイル、path model、入出力 schema など、プロンプト部品ではない機能仕様や実装を探しているとき。
- oracle file や realization file の本文そのものを編集・確認したいだけで、それを説明する標準プロンプトの生成処理を調べる必要がないとき。
- 構造化文書の基盤型、文字列整形 helper、agent 呼び出し処理など、プロンプト部品を利用する下位または上位の仕組みを調べたいとき。
- 特定の標準文書の内容だけが必要で、読むべき個別部品がすでに分かっているとき。

## hash
- 7f9fda2fe4128e8d183a1375518232cccaa31de36b6d084d39a849528b23664f
