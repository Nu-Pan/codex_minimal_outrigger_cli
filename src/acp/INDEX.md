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
- AI エージェントへ渡すプロンプト部品を構築する実装群。oracle / realization の基本概念、oracle・realization・レビュー・ルーティング・ファイルアクセス・INDEX.md エントリーの各標準文書を、構造化文書として組み立てる責務を持つ。
- 個別標準の本文生成だけでなく、役割・概要・ゴール・アクセス規則・ルーティング規則・補助プロンプトを組み合わせ、標準間の依存関係や Codex CLI 向けの語句・ルート置換を含む最終プロンプト構成への入口になる。
- レビューで所見として扱うべき差分、仕様断片の隙間として許容すべき実装差、実装・テストの肥大化抑制、INDEX.md を使った読み進め方など、AI に提示する作業規範の生成箇所を探すための起点となる。

## Read this when
- AI エージェントへ提示する標準プロンプトや規範文書の生成内容、組み込み順序、依存関係を確認・変更したいとき。
- oracle file と realization file の責務境界、oracle 標準、realization 標準、レビュー標準、ルーティング規則、ファイルアクセス規則、INDEX.md エントリー標準のいずれかの文面生成を探したいとき。
- Codex CLI 向けに cmoc 固有語やルートトークンがどのように置換され、作業ルート解決失敗がどう扱われるかを確認したいとき。
- レビュー用プロンプトで、oracle file 単体の問題分類や oracle file と realization file の不整合判定をどの基準で説明しているか確認したいとき。
- ファイル読み書きモードごとの禁止範囲、INDEX.md による探索手順、または INDEX.md エントリー品質基準を AI へどう説明しているか確認したいとき。

## Do not read this when
- 個別サブコマンド、path model、永続状態、出力 schema など、プロダクト機能そのものの仕様や実装詳細を探しているとき。
- 構造化文書、標準、要求、本文整形 helper などの共通データ型や変換基盤そのものを調べたいとき。
- 読み書きモードの列挙値、パス語彙、ルート解決規則そのものを確認したいだけのとき。
- 生成された規範文書を使う側ではなく、実際の OS レベル・実行環境レベルのアクセス制御や enforcement を探しているとき。
- 既に読む対象が個別の標準生成モジュールに絞れており、プロンプト部品群全体の入口や関連標準の所在を確認する必要がないとき。

## hash
- 71d4b1e646d4a6240474c06b0580734d8c752f8fc6c40d644f9a0b9912d88cbe
