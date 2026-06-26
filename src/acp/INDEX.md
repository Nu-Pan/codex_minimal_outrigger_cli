# `builder`

## Summary
- ACP 経由で補助エージェントを呼び出すためのパラメータ構築を集めた領域。適用後レビュー、oracle レビュー、ルーティング文書エントリー生成、merge conflict marker 解消、TUI 実行前の判定など、各用途ごとの prompt、標準文書参照、ファイルアクセス制約、モデル設定、Structured Output schema の境界を扱う。
- AI エージェントに渡す役割・目的・補助文脈・読み書き権限・構造化出力契約を用途別に確認する入口であり、実際の CLI 実行制御や標準本文そのものではなく、呼び出し内容を組み立てる実装へ進むための案内になる。

## Read this when
- 補助エージェント呼び出しで、用途別にどの prompt、標準文書、対象ファイル情報、既知所見、差分、conflict 対象、元プロンプトなどを渡すか確認・変更したいとき。
- apply 後の差分要約、realization file の所見列挙、検出済み所見への修正依頼について、AI への依頼内容、出力契約、ファイルアクセス制約を追いたいとき。
- oracle を根拠にしたレビュー工程で、新規所見、支持理由、反証理由、採否判定、重複・矛盾・統合整理をどの構造化出力として返させるか確認したいとき。
- ルーティング文書用エントリー生成で、対象本文を主根拠にする方針、関連文書参照の扱い、読み取り専用条件、生成結果 schema を確認したいとき。
- merge conflict marker 解消や TUI 実行前のパラメータ解決など、特定の作業前処理を AI エージェントに依頼する際の呼び出し内容と判定結果 schema を確認したいとき。

## Do not read this when
- 各サブコマンド全体の実行順序、CLI 引数解析、git 操作、ブランチ操作、保存・表示・集計・通知など、ACP 呼び出しパラメータ構築より外側の制御フローを調べたいとき。
- oracle file、realization file、review standard、apply review standard、INDEX.md エントリー標準など、prompt に組み込まれる標準本文そのものを読みたいとき。
- 実際に仕様違反やレビュー所見を判断する基準、個別カテゴリの網羅、merge conflict の編集アルゴリズム、git diff や変更ファイル抽出の生成処理を調べたいとき。
- 汎用的な prompt 部品、ACP 呼び出し型、Markdown rendering、構造化ドキュメント表現、パス解決 helper など、用途横断の共通基盤だけを確認したいとき。
- TUI の表示・対話、session join の統合処理、apply fork のフォーク作成・適用、review の結果保存など、利用者向け操作や後続処理の実装を調べたいとき。

## hash
- dfcd3584952aed7fd54e88640f4ecfc9c72d06aa0215eaa89b16c356ec2f5d89

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
