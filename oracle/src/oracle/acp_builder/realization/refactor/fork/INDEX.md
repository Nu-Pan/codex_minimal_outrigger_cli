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
- refactor fork の作業差分を人間向けに要約するための agent call パラメータを構築する。差分を動的 prompt に埋め込み、readonly で実行する変更要約処理への入口となる。

## Read this when
- refactor fork の差分要約 prompt の構築方法、使用するモデル・推論設定、Structured Output schema の指定方法を確認するとき。

## Do not read this when
- refactor 差分そのものの内容や要約結果を確認したいとき。prompt の共通構築処理を変更したいときは、まず共通 prompt builder の実装を読む。

## hash
- d89c323079e06eaf51b8e276168087332b10c5bfe7078ae1278962b744ce4f92

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
- cmoc の realization refactor fork における、単一ファイルのレビュー・修正用 AgentCallParameter を構築する oracle src。対象ファイルを起点に完全プロンプトを生成し、効率モデル・最大推論・realization write 権限・構造化出力・索引付け事前処理を設定する。

## Read this when
- ファイル単位の realization review／fix 用 agent call のプロンプト構成を変更するとき
- レビュー対象、アクセスモード、モデル設定、構造化出力 schema、placeholder の設定を確認するとき
- complete prompt に渡す oracle standard・realization standard・apply review standard の適用条件を確認するとき

## Do not read this when
- 実際のレビュー・修正処理の実装を確認したいとき
- レビュー結果の構造化出力 schema 自体を確認したいとき
- 一般的な prompt builder の共通仕様だけを確認したいとき

## hash
- 16438a1787da7b1e1a09fb9c7cafbe6babca798489d9068d2ddc1f8ebdcd8709
