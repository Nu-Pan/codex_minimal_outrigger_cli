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
- refactor fork の変更差分を人間向けに要約する prompt と AgentCallParameter を構築する定義。差分を動的 prompt に埋め込み、readonly・効率性重視の実行条件、構造化出力 schema、linked worktree の作業ディレクトリを設定する。

## Read this when
- refactor fork の report 用変更要約 prompt を変更・レビューするとき
- 変更要約 agent のモデル種別、推論強度、ファイルアクセス、作業ディレクトリ、構造化出力 schema の起動設定を確認するとき

## Do not read this when
- refactor fork の実際の変更内容や差分そのものを確認したいとき
- 一般的な prompt 構築処理や他の realization の実装を確認するとき

## hash
- 151120b4b451745fb409a615a098af28cb57d0bdcee8aad2ecfaff769d529304

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
- ファイル単位の refactor fork レビュー・修正用 AgentCallParameter を構築する。対象 path と linked worktree を基に、完全な調査・修正・検証プロンプト、アクセス権限、各種ポリシー、Structured Output schema、実行モデルを設定する。
- 対象ファイルを起点に、差分を前提とせず oracle file と realization file の調査から realization file の修正・検証までを行う agent call を定義したい場合の入口。プロンプト本文の構築は `build_complete_prompt`、パス解決は `AgentCallPathContext` と `resolve_real_path`、構造化文書化は `StructDoc` に委譲している。

## Read this when
- refactor fork のファイル単位レビュー・修正 agent call のパラメータ生成を変更するとき
- レビュー対象の linked worktree、realization write 権限、oracle/realization・routing・apply review 各ポリシーの適用方法を確認するとき
- レビュー結果の Structured Output schema、決定論的な変更 path 申告、最大推論設定、indexing preflight の組み合わせを変更するとき

## Do not read this when
- refactor fork 以外の agent call builder を調べるとき
- 共通プロンプト生成の仕様や `build_complete_prompt` 自体の実装を変更・確認するときは、まずその共通実装を直接読むとき
- レビュー対象の realization 実装や oracle 文書の内容を調査するときは、対象ファイルを直接読むとき

## hash
- dcb3db5fa137b8f9c95b2f03ce6c4fe20318e8c1d007125d9c970fac4e9d2786
