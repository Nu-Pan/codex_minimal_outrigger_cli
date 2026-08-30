# `basic.py`

## Summary
- AI コーディングエージェント呼び出しのパラメータ型と、ファイルアクセスモードを定義する。
- エージェント呼び出し種別、アクセスモード、prompt、Structured Output schema、実行 cwd、editor input MCP の有効化、indexing preflight の設定をまとめる入口。

## Read this when
- Agent Call Parameter の構造や生成・受け渡し項目を確認するとき
- cmoc の論理的なファイルアクセスモードの列挙を確認するとき
- agent call の editor input MCP または indexing preflight の設定を確認するとき

## Do not read this when
- 各ファイルアクセスモードの詳細な意味や Codex CLI sandbox への対応を確認したいときは、本文が参照する正本仕様を読む
- agent call の具体的な構築処理や file access policy の生成処理を確認したいとき
- Structured Output schema の機械的な受理条件を確認したいとき

## hash
- 23a9f8d92cc7f3453214b8f5042ba4a495fb3427ffa5434bb5113e25bed1200e

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
- oracle file の編集と、成功後の仕様削減を行う agent call の起動条件・prompt・oracle 専用アクセス設定を扱う入口。
- oracle file の読み取り専用調査用 TUI の prompt、アクセス範囲、エディタ入力連携、indexing preflight を扱う入口。
- oracle review の所見列挙・採否判定・重複や矛盾の統合・擁護理由と反証理由の追加調査について、agent call の入力契約と Structured Output 定義を扱う入口。

## Read this when
- oracle file の編集または仕様削減を実行する agent call の条件、書き込み範囲、作業ディレクトリ、indexing preflight を確認・変更するとき。
- oracle file の調査用 TUI を起動する prompt、読み取り範囲、ユーザー指示やエディタ入力の引き渡しを確認するとき。
- oracle review で所見を列挙・判定・整理し、擁護理由または反証理由を追加調査する agent call の入力、出力契約、起動設定を確認・変更するとき。

## Do not read this when
- 個別の oracle file の具体的な編集内容、調査対象、レビュー基準または所見の妥当性を確認するときは、対象の oracle file や対応する規則を直接読みます。
- oracle review 以外の agent call の共通 prompt 構築、一般的な Structured Output 定義、または共通型の責務を確認するときは、対応する共通 builder や型定義を直接読みます。
- 実装されたレビュー処理の実行順序や所見データの適用ロジックを確認するときは、agent call 設定ではなくレビュー実行本体を直接読みます。

## hash
- 2cdd369ab0d2cf5db0ab94c2d0a5c0a76ab5af802c30b692ae0ece86eb0abc42

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
- `cmoc tui` が AI Agent CLI/TUI に渡す起動パラメータと完全プロンプトを構築する実装。
- オリジナルプロンプト、リポジトリルートを基準とする作業コンテキスト、ファイルアクセス・各種ポリシー、エディタ入力引き継ぎを起動設定へまとめる。

## Read this when
- `cmoc tui` の起動時に生成する完全プロンプトや固定起動パラメータを確認・変更するとき。
- オリジナルプロンプトの埋め込み、作業ディレクトリの解決、TUI 起動時のファイルアクセス設定やポリシー適用を追跡するとき。

## Do not read this when
- TUI の画面表示や対話制御そのものを調べるとき。
- 完全プロンプトの共通的な生成規則を調べるとき。
- TUI 起動後のエージェント実行処理や、別のサブコマンドの引数解析を調べるとき。

## hash
- 56d2d7c78b7a75e64846714b63956232cbc2a47c98f5a953b2691aaa6e8c4d39
