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
- 対象ファイル単位のレビュー兼修正用 AgentCallParameter を構築する定義。対象パスを起点に、完全な調査・修正プロンプト、作業範囲、参照ポリシー、検証条件、Structured Output スキーマを組み立てる。
- refactor fork のファイル単位レビュー・修正フローで、対象ファイルを起点とした agent call の実行条件やプロンプト構成を確認・変更するときの入口となる。

## Read this when
- refactor fork のファイル単位レビュー・修正 agent call の prompt、権限、パスコンテキスト、モデル設定、出力スキーマ指定を変更するとき
- 対象ファイルを起点に oracle・realization の調査から修正後検証までを要求する agent call の構築方法を確認するとき

## Do not read this when
- レビュー・修正 prompt の実際の内容ではなく、Structured Output のフィールド定義だけを確認するときは、対応する JSON スキーマを直接読む
- refactor fork 以外の agent call 構築や、実際のレビュー対象 realization の実装を調査するとき

## hash
- ecd8d82c82127794fe7aec2667cf94c24a2fcdb152481ca7ce702bc0bc283afb
