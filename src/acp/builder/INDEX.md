# `apply`

## Summary
- 適用処理の分岐実行で使う補助 AI 呼び出しパラメータを構築する領域。変更差分の人間向け要約、ファイル単位の所見列挙、所見リストの整理、所見に基づく realization file 修正作業を扱う。
- 各呼び出しで AI に渡す role、goal、読み書き権限、補助プロンプト、参照する標準、Structured Output schema との対応を確認する入口になる。
- 実際の git 操作や適用処理本体ではなく、適用前後のレビュー・修正・レポート生成を支えるエージェント呼び出し仕様をまとめる。

## Read this when
- 適用処理の中で、変更差分を作業レポート向けに要約する AI 呼び出し条件を確認または変更したいとき。
- oracle file または realization file を起点に、realization file への所見を列挙するプロンプト、参照標準、読み取り権限、出力 schema を追いたいとき。
- 複数の所見を、重複・矛盾・False-Positive を除いた作業可能な所見リストへ整理する AI 呼び出しを確認したいとき。
- 所見本文をヒントとして realization file を修正する補助エージェントの権限、注意事項、参照標準を確認したいとき。
- レビュー所見や変更要約を、後続処理へ渡せる構造化データとしてどの単位で表すかを確認したいとき。

## Do not read this when
- 実際のブランチ作成、差分取得、git コマンド実行、サブコマンドの制御フロー、CLI 引数解析を調べたいとき。
- path keyword の定義、ファイルアクセスモード、モデル種別、reasoning effort、AgentCallParameter、完全プロンプト構築、StructDoc 描画などの共通部品そのものを変更したいとき。
- oracle file、realization file、各 standard の定義本文や個別の正本仕様を確認したいとき。
- 所見で指摘された具体的な修正対象ファイルの本文や、実際に変更されるコード内容を読む必要があるとき。
- 適用後レポートやレビュー結果をどう実行・保存・集約するかという上位の処理順序を調べたいとき。

## hash
- 235cce2d3b4810d7d0ec00513a5d5f39399800cea612649c56a9f866b354979b

# `indexing`

## Summary
- cmoc indexing の INDEX.md エントリー生成に必要な構造化出力 schema と、AI エージェント呼び出しパラメータをまとめる領域。生成結果に含める意味情報の最小単位、prompt への対象本文の埋め込み、既存目次ではなくオリジナル本文を根拠にする制約、読み取り専用の実行条件を確認する入口になる。

## Read this when
- INDEX.md エントリー生成の出力 schema と、生成用 AI 呼び出しで渡す prompt や実行パラメータの両方を確認したいとき。
- cmoc indexing が、対象パスと対象本文からどのようにルーティング文書生成用の構造化出力を得るかを追うとき。
- 既存目次を根拠にせず、対象のオリジナル本文だけを使ってエントリーを生成させる制約の実装位置を確認したいとき。

## Do not read this when
- 生成された個別の INDEX.md エントリー内容や、特定ファイル・ディレクトリのルーティング品質だけを確認したいとき。
- cmoc indexing 全体のファイル走査、INDEX.md の読み書き、サブコマンド実行フローを調べたいとき。
- path keyword の定義、AgentCallParameter や FileAccessMode の型定義、oracle file と realization file の仕様体系そのものを確認したいとき。

## hash
- dbb5006940305e3f49d87fe96d1fa1c4fa126c8950771604eea1877e666f873e

# `review`

## Summary
- oracle file を対象にしたレビュー工程の AI 呼び出しパラメータと応答契約をまとめる領域。新規所見の列挙、所見リストの重複・矛盾整理、所見を妥当とする理由・妥当ではない理由の列挙、最終的に人間へ提示すべきかの採否判定を扱う。
- 各工程では、レビュー対象の oracle file、既知の関連所見、既知の擁護理由・反証理由、判定対象所見を標準プロンプトへ渡し、oracle file だけを読ませるファイルアクセス方針、モデル設定、Structured Output schema を組み合わせてエージェント呼び出しを構成する。

## Read this when
- oracle file レビューで、新規所見検出、所見整理、所見の擁護・反証、採否判定のいずれかの AI 呼び出し内容を確認・変更したいとき。
- レビュー対象所見、既知の関連所見、既知の妥当理由や非妥当理由が、各レビュー工程のプロンプトへどのように渡されるかを追いたいとき。
- oracle file を根拠にしたレビュー結果を、重大度、見出し、根拠パス、理由、編集操作、採否理由などの機械検証可能な応答として扱う実装を確認したいとき。
- review oracle 系の処理で使う標準プロンプト断片、ファイルアクセスモード、モデル種別、reasoning effort、Structured Output schema の組み合わせを調べたいとき。

## Do not read this when
- oracle file や realization file の基本概念、path keyword、正本仕様断片そのもの、または oracle 標準全体を確認したいとき。
- review 以外のサブコマンド、CLI 引数解析、サブコマンド登録、実行制御、レビュー結果の保存・集計・通知・UI を調べたいとき。
- 個々の oracle file の仕様本文や、レビュー対象となる正本仕様断片の内容そのものを読みたいとき。
- 汎用のプロンプト組み立て、構造化 markdown レンダリング、パス解決、エージェント呼び出し型など、review oracle に限定されない共通部品を調べたいとき。
- INDEX.md エントリー生成やルーティング文書の書き方を確認したいとき。

## hash
- 3c122f18e3d9493cd095bddcc1a6d2a42fbb4aab9705ed85a1592d5fb7081481

# `session`

## Summary
- session 系サブコマンドから起動する AI エージェント呼び出しパラメータを組み立てる領域。現在は、session join で merge conflict marker 解消だけを担当するエージェントへ渡す model、reasoning、file access mode、complete prompt の構成を扱う。
- conflict 対象パスを work root 基準の実パスへ解決し、対象一覧、作業範囲、oracle file の例外的な最小編集許可、git add/commit 禁止などを prompt に埋め込む処理への入口。

## Read this when
- session 系サブコマンドが AI エージェントへ渡す AgentCallParameter の内容を確認または変更したいとき。
- session join の merge conflict marker 解消エージェントに渡る role、summary、goal、補助 prompt、file access mode、model、reasoning effort を確認したいとき。
- conflict 対象ファイル一覧が prompt にどう埋め込まれるか、実パス解決後の表示がどう作られるかを確認したいとき。
- merge conflict marker 解消に限定する指示、仕様改訂禁止、対象外ファイル編集禁止、oracle file の例外的な編集許可、git add/commit 禁止の文言を調整したいとき。

## Do not read this when
- session join の通常実行フロー、merge 実行、conflict marker 検出、join 後処理そのものを調べたいとき。
- complete prompt の共通組み立て、markdown rendering、AgentCallParameter や FileAccessMode などの型定義を調べたいとき。
- real path、work root、パスキーワードの定義、パス解決関数そのものの仕様を確認したいとき。
- merge conflict marker 解消ではない session 系の実行制御、CLI 引数、状態管理、または他サブコマンドの処理を調べたいとき。

## hash
- 9c349137de9dd93d9b9206760be2310b902102e349c94b45d6be693497c0ef57
