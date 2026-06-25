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
- cmoc indexing におけるルーティング文書用エントリー生成の実装領域。生成結果に求める構造化出力の形と、対象本文・アクセス条件・モデル設定・補助プロンプトを含む AI エージェント呼び出しパラメータの組み立てを扱う。
- INDEX.md エントリー生成処理について、出力 schema 側の制約とプロンプト構築側の挙動をまとめて確認する入口になる。

## Read this when
- cmoc indexing がルーティング文書用エントリーをどのような構造化出力として生成させるか確認したいとき。
- エントリー生成時に AI へ渡す role、goal、補助プロンプト、対象本文、ファイルアクセスモード、モデル設定の組み立てを追いたいとき。
- 対象がファイルまたはディレクトリの場合に、生成対象パスと対象内容がエージェント呼び出しパラメータへどう反映されるか確認したいとき。
- 既存の目次情報を根拠にせず、オリジナル本文を根拠にエントリーを生成させるためのプロンプト条件を確認または変更したいとき。

## Do not read this when
- 個別の INDEX.md エントリー本文そのものを作成・評価したいだけで、生成 schema やエージェント呼び出しパラメータの実装を確認する必要がないとき。
- cmoc indexing の CLI 引数解析、対象ファイル探索、生成結果の保存、またはコマンド全体の実行フローを調べたいとき。
- Markdown レンダリング、構造化文書表現、パス解決、エージェント呼び出し型など、エントリー生成プロンプトを支える共通部品そのものを調べたいとき。
- oracle file と realization file の関係、INDEX.md の読み進め方、ルーティング文書の運用規則など、実装ではなく仕様体系や利用側の規則を確認したいとき。

## hash
- d2279f0da7c6e9f6fb967482165c38fdf8c28afaf6c1ff93dfef1a184fcf09f7

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
- `cmoc session join` の conflict marker 解消を AI に依頼するための呼び出し設定を組み立てる領域。対象ファイルの実パス化、解消作業に閉じた role/summary/goal/prompt、モデル・推論努力、realization 書き込み権限と oracle/realization 標準指示の付与を扱う。

## Read this when
- `cmoc session join` で検出済みの conflict marker を AI に解消させるための呼び出しパラメータを確認または変更したいとき。
- conflict 対象パスをどの時点で実パスへ解決し、AI prompt にどう列挙するかを確認したいとき。
- conflict 解消時のファイルアクセス権限、realization 書き込み許可、oracle file の最小編集許可、oracle/realization 標準指示の付与範囲を確認したいとき。
- AI に git add や git commit をさせず、conflict marker が残らない状態だけを目標にさせる prompt を確認したいとき。

## Do not read this when
- `cmoc session join` 全体の制御、merge 実行、conflict marker 検出、join 後の状態更新を調べたいとき。
- AI 呼び出しパラメータの共通型、モデル種別、推論努力、ファイルアクセスモード自体の定義を調べたいとき。
- prompt 部品の markdown レンダリング、共通 prompt 構築、oracle/realization 標準指示本文を変更したいとき。
- conflict marker 解消以外の session 処理、または対象外ファイルの編集方針を調べたいとき。

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
