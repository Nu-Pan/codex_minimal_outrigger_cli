# `change_summary.json`

## Summary
- 変更差分を意味論的カテゴリごとに要約するための構造化出力スキーマ。各変更についてカテゴリ、概要、根拠となる変更ファイルのリポジトリ相対パスを記録する。

## Read this when
- 変更内容をカテゴリ別に整理する出力形式を確認するとき
- 変更要約データの必須項目や構造を確認するとき

## Do not read this when
- 変更要約の生成ロジック自体を確認したいとき
- ファイルレビューや修正処理の仕様を確認したいとき

## hash
- e76fe63bf6beed0b226e9f22def53577dccda561d911a3b47d58510b06565791

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
- レビュー・修正処理の結果を表す構造化出力スキーマ。所見ごとに根拠、変更ファイル、正本仕様との関係、実装状況、理由、対応結果を記録する。
- レビュー対象の問題を追跡し、修正済みか未解消かを検証結果とともに返す処理の入口。

## Read this when
- レビュー結果の出力契約、所見の根拠、変更パス、対応状態を確認するとき。
- レビュー・修正処理が要求する結果項目や、修正後の検証情報を確認するとき。

## Do not read this when
- レビュー対象の実装内容や個別仕様を調査するとき。
- INDEX.mdのルーティング情報だけで足りるとき。

## hash
- 88da683b3cb7259b7c469c6521f8d85c2e72cbed8a6af90c736e1a2354c4c62d

# `file_review_and_fix.py`

## Summary
- cmoc realization refactor fork における、ファイル単位レビュー兼修正用の AgentCallParameter を構築する oracle 実装です。対象ファイルを起点に完全な調査・修正プロンプトを生成し、パス解決、アクセス権、モデル設定、構造化出力スキーマ、事前インデックス処理をまとめて指定します。関連する fork のレビュー・修正呼び出しパラメータを確認する入口です。

## Read this when
- realization refactor fork のファイル単位レビューまたは修正 agent call のプロンプト生成を変更・調査するとき
- 対象 path、run worktree、oracle/realization のアクセス規則、構造化出力スキーマの設定を確認するとき
- レビュー標準や realization 標準を組み込んだ完全プロンプトの構築経路を追うとき

## Do not read this when
- 実際のレビュー対象 realization file の実装内容や個別の所見を調査するときは、対象ファイルと対応する oracle file を直接読む
- 構造化出力のフィールド定義だけを確認するときは、参照される専用 JSON スキーマを直接読む
- fork 以外の agent call 種別のプロンプト生成を調査するとき

## hash
- fb010285bf85bf62984330369c1f7e6f99a45c49ead01679bfc04c36101b8cfa
