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
- refactor fork の変更差分を要約する agent call 用パラメータを構築する実装。raw_git_diff と linked worktree を受け取り、worktree を実行コンテキストとして確定したうえで、差分要約用 prompt と READONLY のアクセス設定を組み立てる。
- prompt は差分を動的入力として埋め込み、効率性重視のモデル分類・中程度の推論強度・指定された Structured Output schema・indexing preflight を含む AgentCallParameter を返す。

## Read this when
- refactor fork の変更差分要約 agent call の prompt、実行コンテキスト、モデル分類、アクセスモード、Structured Output schema の起動パラメータを確認・変更するとき。
- raw_git_diff の埋め込み方や run_worktree を agent_call_cwd に設定する処理を追跡するとき。

## Do not read this when
- 変更差分の要約結果の形式や項目を確認したいだけの場合は、直接対応する Structured Output schema を読む。
- refactor fork の差分取得・生成処理そのもの、または要約 agent の実行処理を調べる場合は、それぞれの担当実装を直接読む。

## hash
- 7cc5adc466a124afb610773b53715e19722096b14febcfa754286d5d17db9cd0

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
- refactor fork におけるファイル単位レビュー・修正用の AgentCallParameter を構築する定義。対象ファイルを起点に、必要な oracle・realization file の調査、対応する realization file の修正、検証、Structured Output 返却までを担う。
- AgentCall の作業ディレクトリ、アクセス権限、モデル・推論設定、完全プロンプト、構造化出力スキーマを組み立てる実装の入口であり、ファイル単位レビュー・修正の呼び出し仕様を変更・確認するときに読む。

## Read this when
- refactor fork のファイル単位レビュー・修正処理で AgentCallParameter の構築内容を確認または変更するとき
- 対象 path の解決、プロンプト生成、oracle・realization policy、Structured Output schema の指定を確認するとき
- レビュー対象ファイルを起点とした調査・修正・検証の作業条件を確認するとき

## Do not read this when
- レビュー・修正処理の具体的な realization 実装を直接確認したい場合は、対象となる realization file を読むとき
- Structured Output の項目や型だけを確認したい場合は、対応する JSON schema を直接読むとき
- 一般的なプロンプト生成や AgentCallParameter の共通仕様だけを確認したい場合は、参照される共通実装を直接読むとき

## hash
- b1734c37a4bcc68d2ce49b953f8b0ebfb8b0167c9fc706df960862bd3ac8237c
