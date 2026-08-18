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
- refactor fork の変更差分を要約する prompt と AgentCallParameter を構築する定義。
- run_worktree を agent_call_cwd として設定し、raw_git_diff を入力にした readonly の要約 agent call を起動する。
- prompt には差分、作業範囲、Structured Output に従う要約目的を組み込み、効率重視のモデル・推論設定と専用 schema を指定する。

## Read this when
- refactor fork の run branch 差分を人間向けに要約する agent call の prompt や起動パラメータを変更・確認するとき。
- AgentCallPathContext、readonly のファイルアクセス、モデル・推論設定、Structured Output schema の組み合わせを確認するとき。

## Do not read this when
- refactor fork の変更差分そのものを確認したいとき。
- 変更要約以外の refactor 処理や、一般的な prompt 構築処理を直接調査するとき。

## hash
- a1cc9dff42f3d854b7ab8eae99c48a5146fc5a27db30b927c985ae6e326268e4

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
- 指定された oracle/realization file を起点に、refactor fork におけるファイル単位レビュー・修正用 AgentCallParameter の構築を定義する。レビュー対象の linked worktree を agent_call_cwd に設定し、完全な調査・修正プロンプト、各種ポリシー、Structured Output schema、実行設定を組み立てる。
- レビュー対象ファイルの調査から修正後検証までを agent call に要求するプロンプト構築の入口であり、refactor fork の同種のファイル単位レビュー・修正処理を確認するときに読む。

## Read this when
- refactor fork でファイル単位のレビュー・修正用 AgentCallParameter がどのように構築されるか確認するとき
- レビュー対象 path、run worktree、agent_call_cwd、完全プロンプト、適用する各種ポリシーの関係を調査するとき
- レビュー結果の Structured Output schema と、実際の realization file 変更 path の一致条件がプロンプトへどう組み込まれるか確認するとき

## Do not read this when
- レビュー・修正処理の具体的な実装対象や oracle の内容を確認する場合は、対象となる realization file または oracle file を直接読むとき
- Structured Output の項目や型だけを確認する場合は、対応する schema file を直接読むとき
- refactor fork 以外の prompt builder や AgentCallParameter の一般仕様だけを調査する場合は、対応する共通実装・仕様を直接読むとき

## hash
- d56728669f9b000a17c06ecd0f823158065b3cba59d3f1fc8bb758f403f7fa81
