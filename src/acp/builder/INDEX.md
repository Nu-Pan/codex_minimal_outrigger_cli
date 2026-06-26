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
- oracle レビューの各段階で AI エージェントへ渡す呼び出しパラメータと Structured Output 契約を定義する領域。正本仕様断片から新規所見を列挙し、所見を擁護・反証する理由を追加調査し、採否を判定し、所見リストの重複や矛盾を整理するためのレビュー用サブタスクへの入口になる。
- 各サブタスクは、対象所見、既知理由、既知所見などの補助文脈をプロンプトへ組み込み、oracle file を根拠に読む制約、モデル種別、推論強度、ファイルアクセス制約、対応する構造化出力を結び付ける。

## Read this when
- `cmoc review oracle` で AI エージェントに渡す role、summary、goal、補助文脈、ファイルアクセス制約、モデル設定、推論強度を確認または変更したいとき。
- oracle file に基づくレビュー所見の列挙、所見を妥当とする理由の調査、所見を否定する理由の調査、採否判定、所見リストの整理のいずれかの AI 呼び出し内容を追いたいとき。
- 既知の所見や既知理由との重複を避け、新規の所見・理由・編集操作だけを返させる制御を実装または検証したいとき。
- レビュー所見、理由、採否判定、整理操作をどの意味単位で構造化出力として受け渡すか確認したいとき。

## Do not read this when
- `cmoc review oracle` の CLI 引数解析、サブコマンドの実行順序、結果の保存・表示・集約処理を調べたいだけのとき。
- oracle file の定義、正本仕様断片の管理方針、oracle レビューの一般基準そのものを確認したいとき。
- 実際にレビュー対象となる個別の正本仕様断片の内容を調べたいとき。
- レビュー以外の AI 呼び出しパラメータ構築、共通プロンプト部品、汎用的な JSON Schema 読み込み処理を変更したいとき。

## hash
- 5d5baf5a6bb8dd2e07f688e5cc0a0e9ef5b6f1685c2cbdc7ae4a423574e9ae74

# `session`

## Summary
- session 系サブコマンドで AI エージェントを呼び出すためのパラメータ構築を扱う領域。現在は、session join における merge conflict marker 解消担当エージェントへ渡す complete prompt と AgentCallParameter を組み立てる実装への入口となる。
- 衝突対象ファイルの実パス解決、対象ファイル一覧の補助 prompt 化、作業範囲・編集禁止事項・oracle file への限定的な編集許可、モデル種別・推論量・ファイルアクセス権限の指定を確認するためのまとまり。

## Read this when
- session join の conflict marker 解消用エージェントに渡す prompt、補助 prompt、権限、モデル、推論量、または AgentCallParameter の内容を確認・変更したいとき。
- conflict marker 解消作業で、対象ファイル以外の編集禁止、仕様の意味的改訂の禁止、git add や git commit の禁止、作業後に marker を残さない指示がどのように組み込まれるかを調べたいとき。
- 衝突対象として受け取ったパスが作業ルート基準の実パスへ解決され、エージェント向けの対象ファイル一覧として渡される流れを確認したいとき。
- oracle file に conflict marker がある場合だけ、解消に必要な最小範囲の編集を許可する例外指示を確認したいとき。

## Do not read this when
- session join 全体の制御フロー、git merge の実行、衝突検出、または join コマンドの通常処理を調べたいだけのとき。
- complete prompt の共通構築、StructDoc の markdown 化、AgentCallParameter 型、モデル enum、ファイルアクセス権限 enum など、呼び出しパラメータ構築に使われる共通部品そのものを確認したいとき。
- merge conflict marker の検出方法や、衝突内容を実際に解決するアルゴリズムを探しているとき。
- session join 以外の session 系処理や、AI 呼び出しを伴わない session サブコマンドの挙動を調べたいとき。

## hash
- 01616e04bbe6d0b9b4647750bae282ca9c92d0f3bc46616e13e3668f45051701

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
