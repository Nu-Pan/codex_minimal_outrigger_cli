# `apply`

## Summary
- `cmoc apply fork` の AI 呼び出し用 prompt 構築と、それに対応する Structured Output schema を扱う領域。レビュー所見の列挙、列挙済み所見への修正依頼、作業後差分の人間向け要約という工程ごとに、role・goal・参照コンテキスト・file access mode・model class・reasoning effort・出力 schema の対応を定義する。
- git diff、oracle file、realization file、apply review standard、検出済み所見を、各 AI エージェントへどのような読み取り専用または realization 書き込み可能コンテキストとして渡すかを確認する入口になる。

## Read this when
- `cmoc apply fork` のレビュー工程で、ファイル単位の realization file 要修正点を列挙する AI 呼び出しの prompt、参照基準、呼び出し条件を確認・変更したいとき。
- 列挙済み所見を修正担当エージェントへ渡す工程で、所見本文の扱い、realization file の書き込み許可、git add・git commit 禁止などの作業条件を確認したいとき。
- 適用後の git diff を人間向けに意味カテゴリ別へ要約する工程の prompt や出力責務を確認したいとき。
- この領域で使う Structured Output schema が、差分要約や所見リストとしてどの意味上の責務を持つかを確認したいとき。
- `cmoc apply fork` の AI 呼び出しにおける model class、reasoning effort、file access mode、出力 schema の組み合わせを追いたいとき。

## Do not read this when
- `cmoc apply fork` 全体の制御フロー、fork 作成、ブランチ操作、差分適用、git コマンド実行の流れを調べたいとき。
- oracle standard、realization standard、apply review standard そのものの本文や定義を確認したいとき。
- 汎用 prompt 構築部品、markdown rendering、構造化ドキュメント表現、AgentCallParameter 型、repo root や実パス解決などの共通基盤を調べたいとき。
- 実際の変更対象ファイルの中身、個別差分の検出処理、または変更カテゴリ分類アルゴリズムそのものを確認したいとき。

## hash
- f729cd6868793e75c893ba1eca5bef86ca1a311f6abae6a456b41c786c64f7fc

# `indexing`

## Summary
- cmoc indexing におけるルーティング文書用エントリー生成の入力契約と agent call パラメータ構築を扱う領域。生成 AI に渡すプロンプト、読み取り専用の実行条件、効率モデルや reasoning effort、構造化出力 schema の指定、および生成結果に求める意味情報の境界を確認する入口になる。
- 対象本文から INDEX.md エントリー用の意味情報を生成し、それを後続の Markdown 目次情報へ渡す前段を理解するための実装と schema がまとまっている。

## Read this when
- cmoc indexing がルーティング文書用エントリーを生成する際に、AI へどの role・goal・補助プロンプト・対象本文・関連参照条件を渡すか確認または変更したいとき。
- 生成結果として必要な意味情報、余分な項目を許さない出力契約、不正な生成結果として扱われる境界を確認したいとき。
- 対象パスや対象本文が agent call のプロンプトへどのように埋め込まれ、読み取り専用・効率モデル・低 reasoning effort・構造化出力 schema と結び付くかを追いたいとき。
- 対象がディレクトリの場合に、直下の目次本文を入力内容として扱う前提を確認したいとき。

## Do not read this when
- cmoc indexing の CLI 引数解析、対象列挙、ハッシュ判定、並列実行、生成結果の保存、コミット処理、またはサブコマンド全体の実行フローを確認したいとき。
- 生成済み INDEX.md の Markdown 表示形式、レンダリング処理、構造化文書表現、共通プロンプト部品、パス解決、または agent call 型そのものを調べたいとき。
- 既存の目次情報の内容、各ディレクトリのルーティング方針、生成済みエントリーの品質評価、または INDEX.md を読む利用側の挙動だけを確認したいとき。
- Codex CLI や LLM の出力品質そのもの、または indexing 以外のサブコマンド仕様を確認したいとき。

## hash
- 1c86ce9a89b73fdca13f36e355c37fadb75ce2701c89527a52928027d36d403d

# `review`

## Summary
- `cmoc review oracle` で AI エージェントへ渡す呼び出しパラメータと、各段階の機械処理用出力契約を扱う領域。oracle file から新規所見を列挙し、所見の擁護理由・反証理由を集め、採否を判定し、所見リストの重複や矛盾を整理するための prompt 構築がまとまっている。
- レビュー対象や既知の所見・理由を補助文脈として渡し、oracle file だけを読み取り根拠にする制約、モデル種別、推論量、ファイルアクセスモード、隣接する出力契約との対応を確認する入口になる。

## Read this when
- `cmoc review oracle` の所見列挙、理由検証、採否判定、所見整理で、AI 呼び出しに渡す役割・目的・補助文脈・読み取り制約を確認または変更したいとき。
- レビュー所見、所見が妥当である理由、妥当ではない理由、採否結果、所見リスト編集操作を、後続処理が扱える形で返す契約を確認・実装・テストしたいとき。
- 既知の所見や既知理由と重複しない新規所見・新規擁護理由・新規反証理由だけを返させる制御を追いたいとき。
- oracle file の記述を具体的根拠として、推測ではなくレビュー結果を列挙・検証・判定・整理する流れを調べたいとき。

## Do not read this when
- oracle file や realization file の基本概念、正本仕様断片としての一般ルール、レビュー基準そのものを確認したいとき。
- `cmoc review oracle` の CLI 引数解析、サブコマンドの実行順序、所見の保存・表示・集計など、AI 呼び出しパラメータ構築より外側の制御を調べたいとき。
- 個々の oracle file の仕様内容や、所見に基づく oracle file の具体的な編集提案を確認したいとき。
- レビュー以外の AI 呼び出しパラメータ構築、共通 prompt 部品、または汎用的な JSON Schema の書き方を調べたいとき。

## hash
- 574ee24fc5a41aa597e5c9063033e712aededca0ce8adff11db4e8f352a9c9c6

# `session`

## Summary
- `cmoc session join` で検出済みの merge conflict marker を解消するため、AI エージェントへ渡す呼び出しパラメータを構築する領域。
- conflict 対象パスの work root 基準実パスへの解決、解消対象ファイル一覧、作業制限、oracle file の例外的な最小編集許可、git add・git commit 禁止を含む complete prompt と AgentCallParameter の組み立てを扱う。

## Read this when
- `cmoc session join` 中の conflict marker 解消を担当するエージェント呼び出し内容を確認または変更したいとき。
- conflict 解消担当へ渡す role、summary、goal、補助 prompt、対象ファイル一覧の文面や構成を調整したいとき。
- conflicted paths を実パスへ解決し、編集対象パスとして AgentCallParameter に渡す流れを確認したいとき。
- merge conflict marker 解消時に限って oracle file の必要最小限の編集を許可する例外ルールや、git add・git commit を禁止する制御を確認したいとき。
- conflict 解消タスクで使うモデル種別、推論強度、ファイルアクセスモード、complete prompt rendering の設定箇所を確認したいとき。

## Do not read this when
- `cmoc session join` 全体の orchestration、branch 操作、merge 実行、conflict 検出の流れだけを調べたいとき。
- merge conflict marker の有無を検出する処理や、marker の内容を解析して選択・削除するアルゴリズムを探しているとき。
- AgentCallParameter、ModelClass、ReasoningEffort、FileAccessMode の定義や共通仕様を確認したいとき。
- complete prompt の共通構築規則、oracle/realization 標準 prompt、StructDoc の markdown rendering を調べたいとき。
- 通常の realization write 権限や oracle file 編集禁止ルールそのものの基本定義を確認したいとき。

## hash
- 6db380564eacbecaf7b8408e8d043936111d3713b708311986248c9f0734f837

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
