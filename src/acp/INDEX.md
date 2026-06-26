# `builder`

## Summary
- AI エージェント呼び出しパラメータを、用途別サブコマンドの文脈から組み立てる実装をまとめた領域。プロンプト本文、補助文脈、ファイルアクセスモード、モデル種別、推論強度、構造化出力 schema の接続を、適用後補助作業、目次エントリー生成、正本仕様断片レビュー、session join の conflict 解消、TUI 実行パラメータ解決ごとに扱う。
- 各下位領域は、呼び出し先エージェントに何を依頼するか、入力値をどのようにプロンプトへ埋め込むか、どの標準文書を prompt_parts から含めるか、返却結果に schema を要求するかを確認する入口になる。

## Read this when
- cmoc の各処理が AI エージェントへ渡す role、summary、goal、補助文脈、完了プロンプトをどのように構築しているか確認・変更したいとき。
- 差分要約、realization file の所見列挙、所見対応修正、INDEX.md エントリー生成、oracle review の所見処理、merge conflict marker 解消、TUI 実行前のパラメータ判定に関する ACP 呼び出し定義を探すとき。
- エージェント呼び出しごとに選ばれるファイルアクセスモード、モデルクラス、reasoning effort、対象パス解決、作業ルートや正本ルートの扱いを追いたいとき。
- AI から受け取る structured output の外形や、プロンプト構築実装と JSON schema ファイルの対応を確認・検証したいとき。
- oracle standard、realization standard、review oracle standard、apply review standard、index entry standard などの標準 prompt 断片が、どの種類の呼び出しへ含まれるか調べたいとき。

## Do not read this when
- エージェント呼び出しで共通利用される prompt 部品そのもの、標準文書の本文、ファイルアクセス規則の文言、markdown rendering、StructDoc、AgentCallParameter、ModelClass、Path 解決 helper の定義を調べたいとき。
- cmoc apply、cmoc review、cmoc indexing、cmoc session、cmoc tui の CLI 引数解析、実行順序、状態更新、保存処理、git コマンド実行など、呼び出しパラメータ構築より上位の制御フローを確認したいとき。
- oracle file や realization file の実際の仕様・実装内容、レビュー対象の所見本文、適用対象コード、conflict の具体的な解消内容を調査したいだけのとき。
- 生成済み INDEX.md のルーティング内容そのものや、個別ディレクトリのエントリー品質を確認したいだけのとき。
- 構造化出力 schema の一般的な書き方や JSON Schema の仕様を調べたいだけで、cmoc のエージェント呼び出しとの接続を変更しないとき。

## hash
- cc4f73f6205a15106b37a47921549963c5c444d49958d12bfacfdaf919bd58a5

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
