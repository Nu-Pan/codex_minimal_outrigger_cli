# `change_summary.json`

## Summary
- 差分内容を意味論上のカテゴリごとにまとめるための構造を定義するスキーマ。各カテゴリの人間向け要約と、根拠として読むべき主要な変更対象を対応付ける。
- 実装変更やテスト変更などを混在した差分としてではなく、作業意図ごとのまとまりとして報告・保存したい場面への入口になる。

## Read this when
- 適用・分岐処理の結果として、変更内容をカテゴリ単位で要約する出力仕様を確認したいとき。
- 変更要約に含める粒度が、網羅的な全ファイル一覧ではなく主要な根拠対象の列挙でよいかを判断したいとき。
- 差分要約の各まとまりに、カテゴリ名、何をどう変えたかの説明、主要な変更対象を持たせる必要があるとき。

## Do not read this when
- 個々の差分をどのように検出するか、またはカテゴリへ分類するアルゴリズムを調べたいとき。
- 実際の変更対象ファイルの内容や、適用処理そのものの制御フローを確認したいとき。
- ルーティング文書、テスト、実装など特定カテゴリの詳細な本文を直接確認すれば足りるとき。

## hash
- 51ffe6e61588c7c347494a36267c02b8d48f69f6e264fcaf396096938cdd672d

# `change_summary.py`

## Summary
- `cmoc apply fork` の作業レポートで使う、差分から人間向け変更要約を生成するための AI 呼び出しパラメータを組み立てる実装。
- 未加工の git diff を読み取り専用プロンプトの補助情報として埋め込み、変更要約担当ロール、目的、oracle/realization の基本規範、モデル種別、推論量、出力 schema 指定をまとめて返す。

## Read this when
- `cmoc apply fork` の変更要約生成 prompt の文面、役割、goal、差分の渡し方を確認または変更したいとき。
- apply fork の作業レポート用に、AI エージェントへどの file access mode、model class、reasoning effort、Structured Output schema を渡しているか確認したいとき。
- 未加工の `git diff` 出力を解析・整形せず prompt に含める経路を追いたいとき。

## Do not read this when
- fork 用ブランチの作成、適用、削除、git diff の取得そのものを調べたいとき。
- 生成された変更要約の保存、表示、レポート全体の組み立てを調べたいとき。
- 共通 prompt 部品のレンダリング仕様、構造化ドキュメントの markdown 化、path model の詳細を調べたいとき。
- `cmoc apply fork` 以外のサブコマンド向け AI 呼び出しパラメータを調べたいとき。

## hash
- e67af8eaca19963295dc8e237d26d5d2619001f6757af6a00da778a4cbccc002

# `file_finding_enumeration.json`

## Summary
- 実装調査で見つかった問題点を、根拠位置、正本仕様上の要求、観測された実装、問題理由、修正方針として報告するための構造化出力を定義する。
- 仕様と実装の乖離をレビュー結果として人間に渡す場面で使う、所見リストの出力契約を担う。

## Read this when
- 実装レビューや適合性調査の結果として、明確に修正が必要な所見を返す出力形式を確認したいとき。
- 所見に含めるべき根拠情報、仕様要求、観測結果、理由、修正方針の粒度を確認したいとき。
- レビュー結果の生成側または検証側で、所見リストが空でない根拠位置を持つことを前提にしたいとき。

## Do not read this when
- 単に実装対象の仕様そのものを探しているとき。ここには個別機能の要求ではなく、レビュー所見の報告形式だけがある。
- INDEX.md 用エントリーや一般的なルーティング文書の書き方を確認したいとき。
- 所見を JSON 以外の文章、ログ、CLI 表示としてどう見せるかを確認したいとき。

## hash
- 0bed168a2a89c47730cdc914c08c08f2a3ad4022595c4b910c5d8ff9ca335524

# `file_finding_enumeration.py`

## Summary
- `cmoc apply fork` で、指定ファイルを起点に oracle file と realization file を読み、realization file の要修正点をファイル単位で列挙するための AI 呼び出しパラメータを構築する実装。
- 読み取り専用の調査 prompt に、oracle standard、realization standard、apply review standard を含め、所見リストを Structured Output として返させる役割を持つ。
- ファイル数分だけ呼び出される重い処理だが、下流処理への影響が大きいため MAINSTREAM モデルと MEDIUM reasoning を選ぶ判断が書かれている。

## Read this when
- `cmoc apply fork` の中で、対象ファイルごとに realization file の要修正点を洗い出す AI 呼び出し内容を確認・変更したいとき。
- apply fork の所見列挙が、どの標準文書を prompt に含め、どのファイルアクセス権限で動くかを確認したいとき。
- oracle file または realization file を起点にした apply review 用の AgentCallParameter 生成処理を追いたいとき。
- 所見列挙処理のモデルクラス、reasoning effort、出力 schema 対応ファイルの選択理由を確認したいとき。

## Do not read this when
- `cmoc apply fork` のファイル探索そのもの、fork 作成、差分適用、またはレビュー結果の集約処理を調べたいだけのとき。
- AgentCallParameter、ModelClass、FileAccessMode などの基本データ構造や enum の定義を確認したいとき。
- prompt 部品の共通組み立て規則や markdown rendering の詳細を調べたいとき。
- apply review standard の内容そのものや oracle・realization の正本仕様を確認したいとき。

## hash
- 8c27e836c8957d364dacd591645166d9aa1b00ef081fc85e523add1c6a97963d

# `finding_application.py`

## Summary
- `cmoc apply fork` で検出済み所見に対応する実装修正作業を AI エージェントへ依頼するための呼び出しパラメータを組み立てる。
- 所見リストを JSON コードブロック付きの補助プロンプトとして埋め込み、realization file の修正、realization standard への適合、git add/commit 禁止などの作業条件を含む完全プロンプトを生成する。

## Read this when
- `cmoc apply fork` が所見本文を実装修正担当エージェントへ渡す際の prompt 内容、権限、モデル設定、推論強度を確認または変更したいとき。
- 所見対応作業で、findings の各要素がどのように JSON としてプロンプトへ埋め込まれるかを調べたいとき。
- realization file 書き込みを許可するエージェント呼び出しに、oracle/realization basic や realization standard を含める制御を確認したいとき。

## Do not read this when
- `cmoc apply fork` の所見検出処理、fork 作成処理、または修正結果の適用処理を調べたいだけのとき。
- AgentCallParameter、ModelClass、ReasoningEffort、FileAccessMode の型定義や共通仕様を確認したいとき。
- 完全プロンプトの汎用組み立て処理や Markdown レンダリング処理そのものを変更したいとき。

## hash
- 61fdb8a4dc76cc84716908dffb8d88e88ff5636b58d7589e4c6abfb89d52d93a
