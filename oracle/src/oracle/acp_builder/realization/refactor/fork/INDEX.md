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
- refactor fork の作業差分を人間向けに要約する AgentCallParameter を構築する正本実装。差分を補助入力として prompt、読み取り専用の実行条件、効率重視のモデル設定、Structured Output schema の参照先をまとめる。

## Read this when
- refactor fork の変更差分を要約する prompt 構築処理や、その AgentCallParameter の実行条件を確認・変更するとき。

## Do not read this when
- refactor fork の変更内容そのものや要約結果の形式だけを確認したいとき。差分入力や Structured Output schema の定義を直接確認する場合は、対応する入力元・schema を読む。

## hash
- af7d317b4f642b2960d33444e913d1f38c4f4a6e05ecc93c5f2844e52253b36a

# `file_review_and_fix.json`

## Summary
- agent call の所見・対応結果を記述する JSON Schema を定義する対象。レビュー結果を返す処理の契約と、各所見の根拠・変更・要求・実装状況・解消状態を扱う。

## Read this when
- この対象に従う所見出力の形式を確認・生成・検証するとき。

## Do not read this when
- 個別の実装や oracle 要求そのものを調査するとき。対象のスキーマではなく、該当する oracle または realization の本文を直接読む。

## hash
- 3a341995439328e1aec77700036953546bccb4fde829145e9d4162174129bf4f

# `file_review_and_fix.py`

## Summary
- cmoc の realization refactor fork における、ファイル単位レビュー・修正用の agent call パラメータを構築する実装。対象ファイルを起点に完全な調査・修正プロンプトを生成し、oracle/realization の参照規則、レビュー基準、修正・検証条件、変更パス報告規則を組み込む。
- 対象ファイルのパス文脈を設定し、効率重視・最大推論のモデル設定、realization write 権限、構造化出力スキーマ、インデックス事前処理を含む AgentCallParameter を返す。

## Read this when
- ファイル単位の realization レビュー・修正 agent call の prompt 構成や実行パラメータを変更するとき
- レビュー結果の構造化出力、変更パス、修正後検証、oracle/realization 参照規則の組み込み方を確認するとき

## Do not read this when
- レビュー対象ファイルの具体的な実装内容やレビュー基準そのものを確認したいとき
- agent call の構造化出力スキーマだけを確認したいときは、対応する JSON スキーマを直接読む

## hash
- eac6581e368c11cc412386c8a9d7b7970f8cded86d9b676c63f897b1c131bbaa
