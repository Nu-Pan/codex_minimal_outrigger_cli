# `change_summary.json`

## Summary
- 差分全体を意味論上のカテゴリごとに分け、人間向け要約と根拠となる主要変更箇所を返すための構造を定める JSON Schema。
- 変更報告やレビュー用の出力で、単なるファイル一覧ではなく「何をどう変えたか」をカテゴリ単位で伝える場面への入口となる。

## Read this when
- fork 適用後の変更内容を、人間が読む要約としてどの粒度・まとまりで表すべきか確認したいとき。
- 差分要約の出力を生成・検証する処理で、カテゴリ、要約文、主要変更箇所の対応関係を固定したいとき。
- 変更カテゴリごとに、網羅的な一覧ではなく要約の根拠として有用な主な変更箇所だけを扱う必要があるとき。

## Do not read this when
- 個々の変更内容そのものや実際の差分を確認したいだけのとき。
- fork の生成、適用、実行制御の手順や副作用を調べたいとき。
- ルーティング文書や仕様本文の書き方そのものを確認したいとき。

## hash
- 4148f8f7efb949b4872076b64dcb4bd2792df6d888011903c10501ce6f519987

# `change_summary.py`

## Summary
- `cmoc apply fork` の作業レポート向けに、対象ブランチ上の生の差分から変更要約生成用の AI 呼び出しパラメータを組み立てる実装。
- 差分テキストをそのまま補助プロンプトに埋め込み、リポジトリルート内の変更要約を Structured Output として返すための complete prompt、モデル種別、推論量、読み取り専用アクセス、出力 schema 参照をまとめて返す入口。

## Read this when
- `cmoc apply fork` の作業レポートで、変更内容の要約を生成する AI 呼び出し条件や prompt 構成を確認・変更したいとき。
- git diff の生出力を、解析せずに要約生成プロンプトへ渡す経路を確認したいとき。
- apply fork 系の要約生成で、使用するモデルクラス、推論 effort、ファイルアクセスモード、Structured Output schema の指定箇所を確認したいとき。

## Do not read this when
- 差分の取得方法、ブランチ操作、fork 適用処理そのものを調べたいだけのとき。
- 生成された変更要約の schema 定義や各フィールドの意味を確認したいとき。
- complete prompt の共通組み立て規則や、パス解決・構造化 markdown レンダリングの共通実装を調べたいとき。

## hash
- f7139a4d9752c26d62ddb939269bfbde48caa56ed647ad461b99e24cc8ad869b

# `file_finding_enumeration.json`

## Summary
- 実装調査で見つかった問題点を、根拠位置、要求、観測された実装、問題理由、修正方針まで含めて報告するための構造を定める JSON Schema。
- oracle file や standard と realization implementation の乖離を、空でない根拠付きの所見として返す出力契約を確認する入口になる。

## Read this when
- 実装レビューや fork/apply 系の調査結果として、問題所見をどの粒度・根拠付き情報で返すべきか確認したいとき。
- oracle requirement と observed implementation の差分を報告する処理、テスト、バリデーションを実装・修正するとき。
- 所見ごとに根拠ファイルの位置情報、要求、実装状態、問題理由、修正方針を揃える必要がある出力仕様を確認するとき。

## Do not read this when
- ファイル探索や列挙そのもののアルゴリズム、対象ファイルの発見手順、fork/apply の実行フローを知りたいだけのとき。
- 個別の oracle standard や realization standard の本文を確認したいとき。
- INDEX.md ルーティング文書の書き方やエントリー生成規則を確認したいとき。

## hash
- 0bed168a2a89c47730cdc914c08c08f2a3ad4022595c4b910c5d8ff9ca335524

# `file_finding_enumeration.py`

## Summary
- `cmoc apply fork` で、指定された起点ファイルごとに realization file の要修正点を列挙させる AI 呼び出しパラメータを構築する実装。対象ファイルと work root を解決し、oracle・realization・apply review standard を含む read-only 調査用 complete prompt を組み立て、所見リスト用の structured output 保存先を持つ `AgentCallParameter` を返す。

## Read this when
- `cmoc apply fork` のファイル単位レビューで、所見列挙エージェントへ渡す role・summary・goal・標準群・file access mode を確認または変更したいとき。
- 起点となる oracle file または realization file から、同じ work root 内の関連ファイルも読ませて要修正点を列挙するプロンプト生成経路を調べるとき。
- 所見列挙処理で使う model class、reasoning effort、出力 schema の対応先を確認したいとき。

## Do not read this when
- `cmoc apply fork` 全体の制御フロー、サブコマンド引数、fork 実行、レビュー結果の統合や適用処理を調べたいだけのとき。
- oracle standard、realization standard、apply review standard の本文や判定基準そのものを確認したいとき。
- ファイル探索やパス解決 helper の詳細挙動、または complete prompt の markdown レンダリング実装を調べたいとき。

## hash
- cb7b0d664859e5e14b4544befaed393c3d3d520aa898fbed026cf429c177cfba

# `finding_application.py`

## Summary
- `cmoc apply fork` で検出された所見を AI エージェントに渡し、realization file の修正作業を行わせるための呼び出しパラメータを構築する実装。
- 所見リストを JSON コードブロックとしてプロンプトへ埋め込み、realization write 権限、mainstream モデル、中程度の reasoning effort を指定した AgentCallParameter を返す。
- complete prompt 構築、所見本文の提示、oracle/realization 基本情報と realization standard の同梱に関する処理への入口となる。

## Read this when
- `cmoc apply fork` の所見対応作業で、AI エージェントに渡す role、summary、goal、注意事項、所見本文の構成を確認または変更したいとき。
- 所見リストがどのようにプロンプトへ整形されるか、また各所見が JSON としてどの粒度で渡されるかを確認したいとき。
- 所見対応用のエージェント呼び出しに使う model class、reasoning effort、file access mode、complete prompt オプションを確認または調整したいとき。

## Do not read this when
- `cmoc apply fork` の CLI 引数解析、サブコマンド登録、実行フロー全体を確認したいだけで、所見対応用プロンプト構築の詳細を扱わないとき。
- 所見そのものの生成、検出、レビュー、保存、集約のロジックを調べたいとき。
- 汎用の complete prompt 構築処理、StructDoc の markdown レンダリング、repo root 解決、AgentCallParameter 型定義の内部挙動を調べたいとき。

## hash
- a18a7c5c2a2c1c37f21238d6fa69437dd805ae1dfea7adb82b9f437e27b8bd64
