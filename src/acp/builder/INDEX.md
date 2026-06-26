# `apply`

## Summary
- `cmoc apply fork` の AI 支援工程で使う呼び出しパラメータ構築と構造化出力契約を扱う領域。
- フォーク適用後の差分要約、ファイル起点の所見列挙、検出済み所見への修正依頼について、prompt に含める役割・目標・補助文脈・権限・model class・reasoning effort を定義する。

## Read this when
- `cmoc apply fork` が AI エージェントへ渡す prompt、ファイルアクセス権限、model class、reasoning effort、構造化出力契約を確認または変更したいとき。
- apply fork のレビュー工程で、差分要約、ファイル単位の所見列挙、所見対応作業のいずれかの呼び出し内容を追いたいとき。
- 差分要約やレビュー所見の構造化出力を、生成側の prompt 構築と対応づけて確認したいとき。

## Do not read this when
- fork の作成、ブランチ操作、git コマンド実行、差分適用など、apply fork 全体の実行制御や低レベル処理を調べたいとき。
- oracle standard、realization standard、apply review standard など、prompt に含められる標準文書の本文そのものを確認したいとき。
- 汎用的な prompt 構築、markdown rendering、AgentCallParameter 型、repo root 解決など、apply fork 固有でない共通基盤を調べたいとき。

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
- `cmoc session join` で merge conflict marker 解消を AI エージェントへ依頼するための呼び出しパラメータ構築を扱う領域。
- conflict 対象パスの実パス化、対象ファイル一覧の提示、作業範囲・編集禁止事項・oracle file への限定的な例外許可を含む complete prompt の組み立てを確認する入口。
- 利用モデル、reasoning effort、ファイルアクセスモード、生成済み markdown prompt を agent 実行パラメータへ渡す処理を扱う。

## Read this when
- `cmoc session join` の conflict marker 解消を AI エージェントへ委譲するための prompt 内容や実行パラメータを確認・変更したいとき。
- conflict 対象ファイルの実パス解決、対象一覧の提示、作業範囲の説明が agent 向け文書へどう埋め込まれるかを確認したいとき。
- conflict 解消時の編集可能範囲、仕様改訂や対象外ファイル編集の禁止、git add/commit 禁止、conflict marker 残存禁止などの制約を確認したいとき。
- oracle file に conflict marker がある場合だけ、conflict 解消に必要な最小限の編集を許可する方針を確認したいとき。

## Do not read this when
- `cmoc session join` 全体の制御フロー、merge 実行、conflict marker 検出そのものを調べたいとき。
- complete prompt の共通構造、markdown レンダリング、構造化ドキュメント部品の汎用仕様を調べたいとき。
- path model の語彙定義、作業ルート解決、実パス解決の共通仕様や共通実装を調べたいとき。
- conflict 解消後の検証、保存、コミット、ブランチ操作など、agent 呼び出しパラメータ構築の外側にある処理を調べたいとき。

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
