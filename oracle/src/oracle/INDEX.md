# `acp_builder`

## Summary
- AI エージェント呼び出しに共通するパラメータ型とアクセスモードを定義し、機能別に prompt と起動設定を組み立てる builder 群をまとめる。
- 複数の呼び出し領域に分かれた実装から、変更対象の機能に合う builder を選ぶ入口となる。

## Read this when
- AI エージェント呼び出しに共通するパラメータ型やアクセスモードを変更するとき。
- 特定機能が生成する prompt、実行設定、構造化出力 schema の参照、または indexing preflight の設定を変更するときに、担当する builder を探す入口として読む。
- 複数の呼び出し種別に共通する構成や設定を把握するとき。

## Do not read this when
- 対象の呼び出し種別が特定済みで、その実装だけを調べる場合は、機能別の下位項目へ直接進む。
- 共通の prompt 合成規則を調べる場合は、共有の prompt builder 実装から読む。
- コマンドの正本仕様上の要件を確認するときは、その機能を定義する oracle doc から読む。

## hash
- c71f5671f6889d06ed99c5b574653624091dcae5e63e2ac52793b8292c2bd1fe

# `editor_input_handoff`

## Summary
- editor input handoff の MCP 入出力契約と、handoff 本文・ガイドの構築定義を担う正本ソースの入口です。
- handoff 全体の運用仕様から参照される、契約と生成内容の詳細を確認する場所です。

## Read this when
- handoff MCP の入力説明や受理条件、結果形式を確認・変更するとき。
- 項目別入力と送信元情報からの本文生成や、受信先ガイドの構築を確認・変更するとき。

## Do not read this when
- target の登録・有効期間、処理手順、失敗時の扱いなど、handoff 機能全体の仕様を確認するときは、その機能の仕様書を直接読んでください。
- agent に渡す handoff instruction の利用条件・送信手順・責務を確認するときは、その instruction の文面定義を直接読んでください。

## hash
- a2a1263148e18bfbd7bc09d014034824d810a0f333b5cb8c958c0676e6ec0ee8

# `feedback`

## Summary
- 定義するのは feedback observation の agent 提出入力契約で、tool discovery と受け入れ検査が共通して参照する。

## Read this when
- feedback observation の提出データが満たす構造や制約を確認・変更するとき。
- reporter と collector で共有する入力検査の契約を確認するとき。

## Do not read this when
- 報告対象の判断基準や収集・保存の動作を確認するときは、feedback observation の正本仕様を読む。
- agent 向け報告指示の文面や prompt への配置を確認するときは、その生成を担う prompt builder を読む。

## hash
- 709d2b0ca7660b1772a43fe8fdaed710d40142564511ba28a435a49b6776aa67

# `other`

## Summary
- cmoc の処理を横断して使う設定値、agent call 起点のルート・パス表現、および文書参照のデータ構造を扱う。
- 構造化された文書ノードの Markdown 描画と文書参照の表現も提供する。これらの共通モデルや変換を変更するときの入口となる。

## Read this when
- 開発対象リポジトリごとの設定値や Codex call の設定モデルを変更するとき。
- ルートプレースホルダー、agent call の作業場所から導く repository/work root、またはパスの解決・変換を調べるとき。
- 構造化文書の Markdown 描画、文書参照のデータ形式や表示を変更するとき。

## Do not read this when
- 特定のコマンドや処理フローの手順・制御・プロンプトを変更し、ここにある共通モデルや表現形式が関係しないときは、その機能の実装へ進む。
- 正本仕様の意味を確認または変更するときは、実装モデルではなく該当する仕様文書を直接読む。

## hash
- 74fb243037b93c0e6495b1d7d9d0df359866098f1c8b0464e502986cad867055

# `prompt_builder`

## Summary
- Agent call に渡す構造化 prompt の共通的な組み立てと、選択して差し込む規定文面・共通知識を構築する層。
- 競合解消用 prompt と、エディタ起動前に表示する案内の builder も含む。

## Read this when
- 複数種類の agent call に共通する prompt の構成や、規定文面の選択・配置、placeholder 定義の統合を変更するとき。
- アクセス制限、feedback 報告、routing、oracle・realization、handoff、競合解消について agent に渡す規定文面を変更するとき。
- 競合解消用 prompt の組み立てや、エディタ起動前の案内を変更するとき。

## Do not read this when
- agent call ごとの処理手順、固有の入力値、起動・実行経路を調べるときは、ACP builder 側から確認する。
- 規定の意味や要求そのものを確認・変更するときは、該当テーマの正本仕様から読み始める。
- path context や構造化文書ノードの定義・レンダリングを調べるときは、それらを所有する共通モデル側から確認する。
- handoff の MCP 処理や受信側入力の扱いを調べるときは、handoff 機能側から確認する。

## hash
- 1854014e850c201f3ca4769bab51e91f3b70526fae4c67a0ffa1c39fb937eeae
