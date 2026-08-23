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
- refactor fork の変更差分を人間向けに要約する agent call の prompt と起動パラメータを構築する定義。差分を補助入力として完全 prompt に埋め込み、readonly・効率重視の実行条件と Structured Output schema を指定する。

## Read this when
- refactor fork の変更差分要約 agent call の prompt 内容、入力差分の渡し方、実行モデルや推論設定、作業ディレクトリ、読み取り専用条件を確認・変更するとき。

## Do not read this when
- 変更要約の出力形式そのものを確認するときは、対応する Structured Output schema を直接読む。
- refactor fork の実際の変更内容を確認するときは、この起動定義ではなく生成された raw git diff や対象の実装差分を直接読む。

## hash
- bc780d3ef3c3f1e9bee23801596aa74afa59f4c45e19bdc0ab6629272d98eec2

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
- refactor fork におけるファイル単位レビュー・修正用の AgentCallParameter を構築する実装。対象 path と run worktree から prompt のパス文脈を作り、レビュー・修正担当向けの完全な prompt、oracle/realization・所見・routing 各ポリシー、Structured Output の事後条件を組み立てる。
- レビュー対象のファイル変更を許可する効率重視・最大推論設定の agent call として、実行 cwd、構造化出力 schema、indexing preflight を含むパラメータを返す。関連する prompt 構築、パス解決、構造化文書レンダリング、モデル・アクセスモード設定の入口となる。

## Read this when
- refactor fork のファイル単位レビュー・修正 agent call の prompt や実行パラメータの構築を変更・確認するとき
- 対象 path、run worktree、realization write 権限、Structured Output schema、indexing preflight の連携を調査するとき
- レビュー所見・修正結果・routing policy を含む完全 prompt の構成を確認するとき

## Do not read this when
- レビュー対象ファイルそのものの実装内容や個別の所見を調査する場合は、生成された agent call の対象 realization file を直接読む
- 一般的な prompt 構築や構造化文書のレンダリングだけを調査する場合は、対応する prompt builder または struct document 実装を直接読む
- Structured Output の項目定義を確認する場合は、この実装ではなく同名の schema file を読む

## hash
- f40543dd3708c7e2844c88e96ba43813a1a85efff0857ea60c9990ce990ecd87
