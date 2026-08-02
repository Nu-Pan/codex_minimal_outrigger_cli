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
- 対象ファイルに対応する realization implementation と既存テストを確認したが、要修正点は見つからなかった。

## Read this when
- realization refactor の file review・修正 builder の schema と実行契約を確認するとき。

## Do not read this when
- change summary builder や別の ACP builder の契約だけを確認するとき。

## hash
- 2c9d5c94fd9445868a9fb6622a21a543177468f0a827bf9eecd1e9aef0cebc04

# `file_review_and_fix.py`

## Summary
- cmoc の realization refactor fork における、単一ファイルのレビュー兼修正用 AgentCallParameter を構築する正本実装。対象ファイルを起点に完全プロンプト、パス文脈、アクセス権、モデル設定、構造化出力 schema を組み立てる。

## Read this when
- realization refactor fork のファイル単位レビュー・修正処理を変更または調査するとき
- 対象 path、agent call の作業ディレクトリ、プロンプト生成規則、検証・修正条件の設定を確認するとき

## Do not read this when
- 実際のレビュー対象ファイルの実装内容を調査するとき
- レビュー結果の structured output schema だけを確認するときは、対応する schema ファイルを直接読む

## hash
- 5ee953a70d14c96b13aff4437a95f19fc2208f0f52bf81d3e492e895b00b446f
