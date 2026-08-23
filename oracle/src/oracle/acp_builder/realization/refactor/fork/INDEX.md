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
- refactor fork の変更差分を要約する agent call の prompt と起動パラメータを構築する。
- 入力差分を動的 prompt に埋め込み、読み取り専用かつ指定 worktree 上で実行する AgentCallParameter を返す。
- モデル効率設定、Structured Output schema、indexing preflight など、変更判断を伴わない要約実行条件を定義する。

## Read this when
- refactor fork の差分要約用 agent call の prompt や起動パラメータを変更・確認するとき
- 差分入力、agent call の作業ディレクトリ、読み取り専用アクセス、モデル設定、Structured Output schema、preflight 条件の関係を確認するとき

## Do not read this when
- refactor fork の実際の変更差分や変更内容を確認したいとき
- 一般的な prompt 構築処理や他の realization の agent call パラメータを確認したいとき

## hash
- aeda70f400eee69f017e15d5fd42257dc468c96ed1d6dfc64ebea66aa03d110b

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
- 対象ファイルは、refactor fork のファイル単位レビュー・修正用 AgentCallParameter を構築する定義です。対象を起点に必要な oracle／realization file を調査し、修正・検証・所見の Structured Output 返却までを要求する prompt と実行設定を組み立てます。

## Read this when
- refactor fork のファイル単位レビュー・修正 agent call の prompt、アクセス範囲、モデル・推論設定、事前インデックス確認、変更 path の事後条件を確認・変更するとき。

## Do not read this when
- レビュー対象 realization file の実装内容や、レビュー結果 schema のみを確認したいとき。
- refactor fork 以外の agent call 構築定義を直接調査するとき。

## hash
- fba06e19a6414a09227038cb5f571eae63614317579c1400e7fd7dbe1337c50e
