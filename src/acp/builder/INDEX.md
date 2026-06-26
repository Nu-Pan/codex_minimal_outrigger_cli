# `apply`

## Summary
- `cmoc apply fork` の補助エージェント呼び出しを構築する領域。フォーク適用後の変更差分要約、ファイル単位の所見列挙、検出済み所見への修正対応について、prompt に渡す役割・目的・標準文書・読み書き権限・モデル設定・構造化出力契約を扱う。
- 作業レポート用の差分要約、apply review standard に基づく realization file の要修正点調査、所見 JSON を入力にした realization file 修正依頼の入口として読む対象。

## Read this when
- `cmoc apply fork` の後段で AI エージェントに差分要約、所見列挙、所見対応を依頼する prompt 内容や呼び出し条件を確認・変更したいとき。
- ファイルを起点に oracle file と realization file を読ませ、apply review standard に従った所見リストを構造化出力させる条件を追いたいとき。
- 検出済み所見を修正担当エージェントへ渡す際の所見 JSON の埋め込み方、作業上の注意、realization file への書き込み権限、参照する標準文書を確認したいとき。
- 作業レポート向けに git 差分をそのまま渡し、人間向けのカテゴリ別変更要約を生成させる呼び出しと出力契約を確認したいとき。
- 所見リストや変更要約の Structured Output schema が、根拠情報、仕様要求、観測された実装、修正方針、主要な変更パスなどをどう要求しているか確認したいとき。

## Do not read this when
- `cmoc apply fork` 全体の実行制御、フォークの作成・適用・統合、ブランチ操作、git コマンド実行そのものを調べたいとき。
- oracle file、realization file、apply review standard、realization standard など、prompt に組み込まれる標準本文そのものを読みたいとき。
- 汎用的なエージェント呼び出しパラメータ、完全 prompt の共通構築、構造化ドキュメントの markdown rendering、repo root や実パス解決 helper の詳細を調べたいとき。
- カテゴリ分けや所見抽出の実際の判断基準、個別カテゴリ名の網羅、git diff の生成方法、変更ファイル抽出アルゴリズムを調べたいとき。
- INDEX.md エントリーの書き方や一般的なルーティング文書生成の規則だけを確認したいとき。

## hash
- 784dc2822745537568d9cd1813a3eaaf38eec8de4cb7640b52b89c4dc31784ec

# `indexing`

## Summary
- ルーティング文書用エントリー生成に関する実装と出力 schema をまとめた領域。対象本文からエントリー生成用のエージェント呼び出しパラメータを組み立てる処理と、生成結果が満たすべき構造化出力の外形を扱う。
- 既存の目次情報を根拠にせず対象本文を主根拠にする方針、関連文書参照の許可、読み取り専用の実行条件、効率モデル・低 reasoning effort・構造化出力 schema の指定を確認する入口になる。

## Read this when
- ルーティング文書用エントリー生成で、AI に渡すプロンプト、補助指示、対象本文の埋め込み方、出力 schema の指定を確認または変更したいとき。
- エントリー生成結果を検証する実装やテストで、必須項目、文字列配列、追加項目禁止といった structured output の外形を確認したいとき。
- 対象がファイルまたはディレクトリの場合に、生成対象パスや直下内容がどのようにエージェント呼び出しへ渡るかを追いたいとき。
- インデックスエントリー生成時のファイルアクセスモード、モデルクラス、reasoning effort、schema 連携を確認したいとき。

## Do not read this when
- 生成済みの目次情報そのものや、各ディレクトリのルーティング内容の良し悪しを確認したいだけのとき。
- 特定の対象について実際に読むべきかどうか、またはエントリーに書く意味内容の判断基準を確認したいとき。
- プロンプト部品の共通構築、Markdown レンダリング、構造化文書表現、パス解決、エージェント呼び出し型の定義そのものを調べたいとき。
- CLI 引数解析、対象ファイル探索、生成結果の保存、コマンド実行フロー、または INDEX.md を利用して作業対象を選ぶ側の挙動を調べたいとき。

## hash
- d2279f0da7c6e9f6fb967482165c38fdf8c28afaf6c1ff93dfef1a184fcf09f7

# `review`

## Summary
- oracle review で使う AI 呼び出しパラメータ構築と Structured Output 契約を扱う領域。新規所見の列挙、所見を擁護または反証する理由の追加調査、所見の採否判定、重複や矛盾を含む所見群の整理について、プロンプト内容、補助入力、ファイルアクセス制約、モデル設定、出力 schema への接続を確認する入口になる。
- レビュー対象の正本仕様断片そのものを読む処理ではなく、レビュー結果として扱う所見・理由・判定・整理操作を AI に生成、検証、整形させるための境界をまとめる。

## Read this when
- oracle review の各段階で、どの役割の AI 呼び出しがどの入力を受け取り、どの目的でプロンプトを構築するか確認したいとき。
- 既知の関連所見や既知理由を渡し、新規所見や新規理由だけを返させる重複回避の扱いを確認したいとき。
- 正本仕様断片を根拠にした所見、妥当理由、不当理由、採否判定、編集操作の Structured Output 契約を実装、検証、調整したいとき。
- レビュー標準や oracle 標準をプロンプトへ含める経路、読み取り専用の oracle file アクセス制約、呼び出しごとのモデル設定を追いたいとき。
- 重大度、根拠となる正本仕様断片、採否理由、削除・置換・統合などの後処理方針をレビュー出力としてどの粒度で扱うか確認したいとき。

## Do not read this when
- oracle file や realization file の基本定義、所有責任、配置ルールだけを確認したいとき。
- 個々の正本仕様断片の内容そのものや、実際にどの oracle file を調査すべきかを探しているとき。
- review oracle 全体の CLI 引数解析、サブコマンドの実行順序、所見の保存・表示・集計・通知など、AI 呼び出しパラメータ構築より外側または後段の処理を調べたいとき。
- 汎用的なプロンプト部品、パス解決、AgentCallParameter の基本構造、またはレビュー以外の ACP 呼び出し構築を確認したいとき。
- 一般的な INDEX.md エントリーの記述方針、ルーティング文書の基準、または JSON Schema 構文そのものを確認したいとき。

## hash
- 574ee24fc5a41aa597e5c9063033e712aededca0ce8adff11db4e8f352a9c9c6

# `session`

## Summary
- `cmoc session join` で検出された merge conflict marker を解消するための AI エージェント呼び出しパラメータ構築を扱う領域。
- 対象ファイル一覧を prompt に埋め込み、作業範囲を conflict marker 解消に限定し、oracle file を含む追加ファイルアクセス条件、モデル、reasoning、アクセスモードを固定する実装への入口となる。

## Read this when
- session join の merge conflict marker 解消用に、エージェントへ渡す role、summary、goal、補助 prompt、対象パス一覧の組み立てを確認または変更したいとき。
- conflict 対象ファイルがどのように実パスへ解決され、prompt 内の対象一覧として渡されるかを調べたいとき。
- conflict marker 解消時だけ許可される oracle file 編集条件や、呼び出し時の file access mode、model class、reasoning effort を確認したいとき。

## Do not read this when
- session join 全体の制御フロー、merge conflict marker の検出方法、git merge や commit の操作を調べたいとき。
- conflict marker 解消以外の通常の session join prompt やエージェント呼び出し条件を確認したいとき。
- prompt 部品の markdown レンダリング、構造化ドキュメント、パス解決、AgentCallParameter 自体の共通実装を調べたいとき。

## hash
- 9a2f6d3958ca7a062f831b72e14760fc17a7b00c304e271bb519ccae350825a1

# `tui`

## Summary
- AI Agent CLI/TUI のうち、TUI 実行前に元プロンプトからエージェント呼び出しパラメータを解決する領域。作業依頼に対する論理ファイルアクセス権限の選択と、oracle・realization・review・INDEX.md エントリー作成に関する標準参照要否の判定を、Structured Output schema 付きの読み取り専用エージェント呼び出しへ組み立てる実装と、その判定結果の期待形を扱う。

## Read this when
- TUI で入力された元プロンプトから、実行時に選ぶべきファイルアクセスモードをどう判定するか確認したいとき。
- TUI 実行前の parameter resolve 処理が、どのモデル・推論努力・アクセス権限・Structured Output schema を指定してエージェントを呼び出すか追うとき。
- 作業依頼に応じて oracle、realization、review、INDEX.md エントリー作成の各標準を読む必要があるかどうかを、どのような理由付き判定として返すか確認するとき。
- TUI のパラメータ解決プロンプトに含める標準文書、アクセスモード候補、元プロンプト埋め込み、または判定結果 schema を変更・検証するとき。

## Do not read this when
- 実際の oracle file や realization file の責務、編集可否、品質基準そのものを確認したいだけのとき。
- INDEX.md エントリー本文の書き方や、ルーティング文書としての判断基準だけを確認したいとき。
- TUI の表示、対話フロー、エディタ入力の取得、コメント除去、strip 処理、またはコマンドライン引数の挙動を調べたいとき。
- TUI 以外のサブコマンドにおける実行パラメータ解決を調べたいとき。

## hash
- 20de0fa032e291d3d295507c1029caa4da12575832bfa7fb90fb1b73f91d9dda
