# `builder`

## Summary
- AI agent 呼び出し用の AgentCallParameter と Structured Output 契約を、サブ領域ごとに構築する builder 群への入口。apply、indexing、review、session、tui の各処理で、prompt に渡す役割・目的・補助文脈・標準文書・ファイルアクセス権限・モデル設定・推論量・出力 schema を組み立てる責務を持つ。
- CLI/TUI の本体制御ではなく、対象処理の後段または前段で AI に渡す依頼内容と、AI から受け取る構造化結果の形を確認するための領域。

## Read this when
- apply、indexing、review、session、tui のいずれかで、AI agent に渡す prompt、補助指示、参照標準、アクセス権限、モデル、reasoning effort、Structured Output schema の指定を確認または変更したいとき。
- 差分要約、apply review、INDEX.md エントリー生成、oracle review、merge conflict marker 解消、TUI 実行前パラメータ解決など、処理別の AI サブタスク呼び出し条件を探したいとき。
- AI に渡す入力文脈と、AI から返させる構造化出力の意味単位を、サブコマンドや用途ごとの入口からたどりたいとき。
- 特定のサブ領域へ進む前に、どの builder がどの AI 呼び出し責務を担うかを切り分けたいとき。

## Do not read this when
- CLI サブコマンド全体の実行制御、引数解析、git 操作、ファイル探索、結果保存、表示、統合フローそのものを調べたいとき。
- prompt に埋め込まれる oracle file、realization file、各種 standard の本文そのもの、または個別の正本仕様断片を読みたいとき。
- AgentCallParameter 型、モデル enum、ファイルアクセス権限 enum、StructDoc の markdown 化、パス解決 helper など、共通部品そのものの定義を確認したいとき。
- AI が返した所見・理由・変更要約・判定結果の中身を評価したいだけで、呼び出しパラメータや出力契約を変更しないとき。
- INDEX.md エントリーの一般的な書き方、ルーティング文書の品質基準、または生成済みルーティング内容の妥当性だけを確認したいとき。

## hash
- 2760b9582cc34098381e4baa949b5875af0a80ad389f2f7a90aa07ed810d9ee7

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
