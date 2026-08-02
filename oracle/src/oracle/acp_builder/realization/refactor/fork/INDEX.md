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
- 実装レビューで検出した所見を、根拠・oracle 要求・実装状況・理由・対応結果・検証結果とともに記録する JSON スキーマ定義。レビュー結果を構造化して返すための入口。

## Read this when
- 実装レビューや修正対応の所見フォーマットを確認するとき
- 所見の根拠位置、oracle 要求、対応状態、検証結果の構造を確認するとき

## Do not read this when
- 実装レビューの具体的な観点や対象ファイルを確認したいとき
- 通常の実装・テスト仕様や、別形式の出力スキーマを扱うとき

## hash
- 4a1ec12adc95a23912e38113ca366655a433bcf323284cfb08675bf8c11cc167

# `file_review_and_fix.py`

## Summary
- `cmoc realization refactor fork` のファイル単位レビュー・修正用 AgentCallParameter を構築するモジュール。対象ファイルを起点に完全なレビュー・修正プロンプトを生成し、モデル・権限・検証・Structured Output schema などの実行条件をまとめて返す。
- プロンプト本文の組み立て、対象パスの解決、構造化 Markdown 化、実行パラメータ生成が主な責務であり、ファイル単位レビュー・修正フローの入口となる。

## Read this when
- ファイル単位の realization レビュー・修正 prompt の構成や実行条件を変更するとき
- 対象 path、worktree、file access mode、reasoning/model 設定、Structured Output schema の指定を確認するとき
- レビュー時の oracle・realization 参照規則や修正・検証条件を確認するとき

## Do not read this when
- レビュー対象ファイルそのものの実装内容や個別の所見を調査するとき
- レビュー結果の Structured Output schema 定義だけを確認するとき
- 共通 prompt builder や path model の内部仕様を直接確認するとき

## hash
- d28b48d3e7a7160ccd6b4efb68a2725ea2e4ebc471d032b45d5adbb5978a4164
