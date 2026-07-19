# `change_summary.json`

## Summary
- 変更要約生成エージェントの構造化出力スキーマを定義し、変更内容をカテゴリ別の要約と根拠ファイル一覧として返せるようにする。

## Read this when
- refactor fork の変更要約出力形式や、要約結果の検証項目を確認するとき

## Do not read this when
- ファイル単位レビュー・修正の出力形式を確認したいときは、対応するレビュー用スキーマを直接読む

## hash
- dc922a0d0f2d939d57f9fe06e94599cbe8166bdbfd52c2ff17cd5c65882b6eda

# `change_summary.py`

## Summary
- cmoc の realization refactor fork 差分を要約する agent call パラメータを構築する oracle src。差分を埋め込んだ読み取り専用 prompt、モデル・推論設定、Structured Output schema、事前インデックス処理を定義する。

## Read this when
- realization refactor fork の変更要約 prompt の構築方法、入力差分の渡し方、モデル設定、出力 schema の指定を確認するとき。

## Do not read this when
- refactor 差分そのものの内容を確認したいとき。
- 変更要約の Structured Output schema の詳細だけを確認したいとき。

## hash
- 7dc4a8a193cda8108332d73c5038399de0a3799a17f0df4437990b657150489f

# `file_review_and_fix.json`

## Summary
- ファイル単位の realization review・修正 agent call が返す所見の構造化出力 schema。各所見について根拠位置、oracle 要件、観測実装、修正理由、解消状況と検証結果を定義する。対応する prompt builder の出力形式を確認する入口である。

## Read this when
- ファイル単位の review・fix agent call の structured output 形式を確認するとき。
- 所見の根拠、修正要件、観測結果、解消状況を含む出力データを生成・検証するとき。

## Do not read this when
- review・fix の prompt 内容や agent call の入力パラメータを確認したいときは、対応する Python prompt 定義を直接読む。
- refactor fork 全体の状態遷移や候補 file の処理順を確認したいときは、該当する app specification を読む。

## hash
- 5636bc81054a256c1274e6b3ecd31896dc960944ba162e64d97422b57cf40a63

# `file_review_and_fix.py`

## Summary
- `cmoc realization refactor fork` における、指定ファイルを起点としたファイル単位レビュー・修正用の AgentCallParameter を構築する。完全プロンプト、アクセス権、モデル設定、構造化出力スキーマ、インデックス事前処理を定義する。

## Read this when
- ファイル単位の realization review・修正処理の prompt 構築を変更または確認するとき
- レビュー対象のパス、プロンプト生成、oracle・realization standard、出力スキーマの設定を追跡するとき

## Do not read this when
- 実際のレビュー・修正処理の実装詳細だけを調査するとき
- 他の prompt builder や path model の一般仕様だけを確認するときは、それぞれの対象ファイルを直接読む

## hash
- 3a6667d04d6984eda8f72ed3878d68e0ad780fecede3fdb44535261b1f655c53
