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
- 対象ファイルは所見を記録するための Structured Output schema であり、内容上の要修正点は確認できません。

## Read this when
- この schema のレビュー結果を確認するとき

## Do not read this when
- 実装ファイルの挙動や修正内容を調査するとき

## hash
- 0510d3855b5b99e1f3cfbcdfb863e34e58dc00054954c748b0b6ccf8129677cc

# `file_review_and_fix.py`

## Summary
- cmoc の realization refactor fork における、ファイル単位レビュー兼修正 agent call のパラメータを構築する oracle source。完全な調査・修正・検証 prompt、対象パスのプレースホルダ、モデル・推論設定、Structured Output schema を定義する。

## Read this when
- ファイル単位の realization review・修正 agent call の prompt 構成や実行パラメータを変更するとき
- レビュー対象ファイル、アクセスモード、モデル設定、検証・出力要件の関係を確認するとき

## Do not read this when
- レビュー対象の realization 実装そのものを調査・修正するとき
- レビュー結果の Structured Output schema の詳細だけを確認するときは、対応する schema file を直接読む

## hash
- 4a1ffe3d0db1a8dd9cbb1ea93c798d3afd70bc36a8f31df9fbcf7ac9fb008195
