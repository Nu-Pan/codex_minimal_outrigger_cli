# `builder`

## Summary
- AI エージェント呼び出しに渡す prompt、補助文脈、ファイルアクセス条件、モデル設定、推論量、Structured Output schema の組み立てを、用途別に扱う実装領域。レビュー、適用、競合解消、TUI 実行前解決、ルーティング文書用エントリー生成など、cmoc の各工程で AI に何を読ませ、何を返させ、どの制約で作業させるかを確認する入口になる。
- 工程ごとの制御フローそのものではなく、AI 呼び出しパラメータと機械処理用の出力契約を追うための領域。oracle file、realization file、review standard、git diff、既知所見、conflict 対象、元プロンプトなどを、各エージェントへどの意味の文脈として渡すかを把握できる。

## Read this when
- cmoc の各サブコマンドや TUI で、AI エージェントへ渡す role、goal、補助 prompt、参照コンテキスト、ファイルアクセスモード、モデル種別、推論量を確認または変更したいとき。
- AI の Structured Output schema が、レビュー所見、理由、採否、所見整理操作、差分要約、ルーティング文書用エントリー、TUI 実行前の判定結果などとしてどの責務を持つか確認したいとき。
- oracle file だけを根拠にする、realization file への書き込みを許可する、git add・git commit を禁止する、conflict 解消時だけ oracle file の最小編集を例外的に許すなど、AI 作業制限の組み立てを追いたいとき。
- 既知の所見や理由、検出済み conflict、対象本文、作業後差分、元プロンプトなどの入力情報が、AI 呼び出しの補助文脈へどう反映されるかを調べたいとき。
- INDEX.md エントリー生成や TUI 実行前パラメータ解決のように、AI に判断させる内容とその返却契約を実装・テストしたいとき。

## Do not read this when
- CLI 引数解析、サブコマンド全体の実行順序、fork 作成、branch 操作、merge 実行、差分適用、保存、表示、集計など、AI 呼び出しパラメータ構築の外側にある orchestration を調べたいとき。
- oracle file、realization file、review standard、apply review standard、INDEX.md 運用規則などの正本仕様や基準本文そのものを確認したいとき。
- AgentCallParameter、ModelClass、ReasoningEffort、FileAccessMode、markdown rendering、構造化ドキュメント表現、パス解決などの共通基盤の定義や汎用実装を調べたいとき。
- 実際の変更対象ファイルの中身、個別差分の検出処理、変更カテゴリ分類、conflict marker 検出や解消アルゴリズム、TUI の表示・対話・入力取得を調べたいとき。
- 個別の INDEX.md エントリー本文を作成・評価したいだけで、エントリー生成に使う schema やエージェント呼び出しパラメータの実装を確認する必要がないとき。

## hash
- 3d80b6cf3c308bdfa53ab5b527a5ec024582d37bf2d5271809fd0cb5fab6a8cf

# `prompt_parts`

## Summary
- AI agent に渡す作業プロンプトを構成する部品群を扱う領域。ファイルアクセス規則、ルーティング規則、oracle/realization の基本概念、各種標準、レビュー基準、完全なプロンプトの組み立てを構造化文書として生成する実装がまとまっている。
- 個別の標準文書そのものを確認する入口と、それらを依存関係込みで最終プロンプトへ注入する入口の両方を含むため、agent 呼び出し時にどの規範や制約が提示されるかを追う起点になる。
- 正本仕様断片と具体化物の責務境界、INDEX.md を使った探索規則、INDEX.md エントリー品質、oracle/realization レビューの判断基準など、cmoc の AI 作業方針を文章化する prompt part の集合である。

## Read this when
- agent call に渡すプロンプト全体、またはその中に含まれる標準規範・制約文・補助文書の構成を確認したいとき。
- ファイルアクセス制約、INDEX.md を使った読み進め方、oracle file と realization file の責務境界を、AI 向けプロンプトとしてどう表現しているか確認したいとき。
- oracle file、realization file、INDEX.md エントリー、oracle レビュー、oracle と realization の照合レビューに関する共通標準や判断基準の文面を確認・変更したいとき。
- 特定の標準プロンプトを最終プロンプトに含める指定が、他のどの標準プロンプトを依存関係として追加するかを調べたいとき。
- Codex CLI 向けに、プロンプト内の仕様・実装・ブランチ・ルートトークンなどの用語が作業者向け表現や実パスへどう置換されるか確認したいとき。

## Do not read this when
- 個別サブコマンドの実行制御、CLI 引数、入出力 schema、永続状態、path model などの具体的なプロダクト挙動を調べたいとき。
- 構造化文書のデータ型、Markdown 変換、標準文書変換 helper など、prompt part が利用する基盤処理そのものを確認したいとき。
- 実際の OS レベル・実行環境レベルのファイルアクセス enforcement や agent call の実行処理を探しているとき。
- 個別の oracle file が定める正本仕様や、src/test 配下の機能実装・テストの詳細を読むべき状況で、AI 向けプロンプト文面の生成には関心がないとき。
- INDEX.md エントリーの文面だけを作るために対象本文が既に特定できており、prompt part 側の規範実装を確認する必要がないとき。

## hash
- 8d43db4d61a9de4beee7919e934d57d494b3cbe7aff98595a87d3bbb4e2a41d0
