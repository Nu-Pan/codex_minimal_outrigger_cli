# `basic.py`

## Summary
- Agent Call Parameter の呼び出し種別、ファイルアクセスモード、実行設定をまとめるデータクラスです。
- agent call の prompt、Structured Output schema、cwd、indexing preflight の設定を保持する入口です。

## Read this when
- agent call のパラメータ構造や、呼び出し時に指定するアクセスモードと実行設定を確認するとき。
- Agent Call Parameter の各設定値がどのように一つの呼び出し設定へ集約されるかを確認するとき。

## Do not read this when
- ファイルアクセスモードの各値の正本上の意味や Codex CLI sandbox との対応を確認したいとき。
- Agent Call Parameter を生成・利用する builder や、実際の agent call 実行処理を確認したいとき。

## hash
- 581a8b33c6ac557a5d598fa4c76b38f03b32f5964b6de8c0f1f01243f924dfdc

# `feedback`

## Summary
- feedback issue の同一性判断と検証に関する agent call の出力スキーマおよび実行定義をまとめた領域。既存 issue candidate との同一性判定、candidate の現在状態の verification、各処理の入力・参照範囲・Structured Output 契約への入口を提供する。

## Read this when
- feedback issue が既存 issue と同一か新規かを判定する出力契約や agent call の構築を確認するとき
- 既存 issue candidate の現在状態を検証する出力契約、prompt、参照範囲、起動パラメータを確認するとき

## Do not read this when
- feedback issue の観測送信、candidate の生成・収集、事前絞り込みなど、同一性判定や verification より前段の処理を確認したいとき
- summary、impact、原因、actionability、relation など issue 内容の生成・評価ロジック自体を確認したいとき
- feedback 領域以外の ACP builder 出力契約や共通 prompt builder の定義を確認したいとき

## hash
- f0a2adfa41b59b65486ef90e92abeb5d7312afadf418df2b8e1ea3364efe7f26

# `indexing`

## Summary
- INDEX.md エントリー生成 agent call の出力形式を定義する JSON Schema と、`cmoc indexing` 用 prompt・起動パラメータ構築を扱う。
- 出力形式の確認は `index_entry.json`、indexing agent call の構成やアクセス条件の確認は `index_entry.py` から始める。

## Read this when
- INDEX.md エントリー生成結果の構造や必須項目を確認するとき。
- `cmoc indexing` の prompt、対象本文の埋め込み、読み取り専用設定、cwd、Structured Output schema、preflight 設定を変更・確認するとき。

## Do not read this when
- INDEX.md の既存ルーティング内容を確認するとき。
- indexing サブコマンドの実行処理や、一般的な agent call パラメータの仕様を調べるとき。

## hash
- 37152661db8f1ea3ecd682fed2ac40879fd7c2e37781938b4986faf8d86eac21

# `oracle`

## Summary
- oracle file の編集・調査・レビューに関する agent call の起動設定と prompt 構築を扱う入口。
- edit は本命編集と成功後の仕様削減、investigation は oracle 調査、review は所見の列挙・採否判定・統合・擁護・反証を担当する。

## Read this when
- oracle edit の編集または仕様削減で、prompt、oracle 専用アクセス、作業ディレクトリ、indexing preflight、未コミット変更の扱いを確認するとき。
- oracle investigation の調査範囲、ユーザー指示の prompt への組み込み、読み取り専用条件、TUI 起動設定を確認するとき。
- oracle review の所見列挙・採否判定・重複整理・擁護理由・反証理由について、入力情報、Structured Output schema、読み取り範囲、起動設定を確認するとき。

## Do not read this when
- 具体的な oracle file の編集内容、調査対象、レビュー基準を確認したいときは、対象の oracle file や対応する規則を直接読む。
- 共通の完全 prompt 構築規則、agent call パラメータ、型定義を確認したいときは、対応する共通 builder や型定義を直接読む。
- レビュー処理の実行本体や Structured Output の具体的な項目定義だけを確認したいときは、対応する review 実装または schema を直接読む。

## hash
- 46d8519a530fbdedfbacbea14e8a9297108dc072cb6f09a579abc1c6c148ccb4

# `quota_probe.py`

## Summary
- Codex CLI の quota 回復確認用 agent call を構築する定義。短い応答だけを返す読み取り専用 probe の prompt と、再帰的な indexing preflight を避ける起動設定を扱う。

## Read this when
- quota の利用可能性を確認する agent call の prompt、アクセスモード、作業ディレクトリ、起動オプションを確認・変更するとき。

## Do not read this when
- 通常の quota 判定ロジックや追加調査・実作業の実装を確認したいとき。この対象は probe の呼び出しパラメータ構築に限定される。

## hash
- 602e12a985f727cfbaeaa41f0c953171116fb1b35d8b4ee2bed1e136c524094c

# `realization`

## Summary
- fork 間の oracle file 差分を realization file へ反映する agent call の構築入口です。commit 範囲、raw git diff、write モードなど差分追従固有の起動条件を扱います。
- realization refactor の変更要約およびファイル単位のレビュー・修正を行う agent call の契約と構築規則を扱う下位領域です。

## Read this when
- fork 間の oracle file 差分を realization file へ反映する prompt や起動パラメータを確認・変更するとき
- realization refactor の変更要約、レビュー、修正、検証に関する agent call の出力契約や起動条件を確認するとき

## Do not read this when
- 通常の realization file の実装やテスト、oracle の要求、realization の設計・実装規則を直接確認・変更したいとき
- 差分追従や realization refactor 以外の agent call、一般的な prompt 構築処理を調べたいとき

## hash
- 2d27e7735e65ab72b50444188678a0540cf9d980b136c63dbc69c115c7000d81

# `session`

## Summary
- `cmoc session join` で発生した git merge conflict の解消をエージェントへ依頼する際の起動パラメータと prompt を構築する入口。対象ファイル、専用の解消ポリシー、書き込み権限、preflight を行わない起動条件を扱う。

## Read this when
- `session join` の conflict 解消に使うエージェントの prompt または起動パラメータを確認・変更するとき。
- conflict 対象ファイルの指定方法、oracle file の編集範囲、専用 policy、preflight を省略する起動設定を確認するとき。

## Do not read this when
- merge conflict marker の検出・解消処理そのものを確認したいとき。
- 一般的な prompt 構築、パス解決、または `session join` の別処理を直接確認したいとき。

## hash
- 474dd53a2350ba7cbcb30ec5589e1bc3aa4ba3efb068cdbcd18954d572068b7a

# `tui`

## Summary
- 日本語技術文書のルーティング情報として、対象本文の責務を簡潔に整理します。

## Read this when
- `cmoc tui` の起動パラメータ生成を調べるとき。
- ユーザー入力を完全プロンプトへ埋め込み、リポジトリ書き込み権限・リポジトリルートの作業ディレクトリ・インデックス事前処理を含む TUI 起動条件を確認するとき。

## Do not read this when
- 完全プロンプトの共通構造や適用するポリシー自体を確認したいとき。
- TUI 起動後の実行処理や、`cmoc tui` 以外のサブコマンドのパラメータ生成を確認したいとき。

## hash
- 1a5e2bc53b3cf0fa64d52b3bd9ea867edb07e16a98856c1237c2a9e8de1975ae
