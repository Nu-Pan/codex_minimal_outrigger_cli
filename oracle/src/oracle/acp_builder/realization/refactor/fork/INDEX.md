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
- refactor fork の変更差分を人間向け要約へ変換する AgentCallParameter を構築する。差分を実行時プロンプトへ埋め込み、読み取り専用・効率重視の実行条件と変更要約用 Structured Output schema を設定する。

## Read this when
- refactor fork の差分要約 prompt の構築方法、入力差分の渡し方、または要約用 AgentCall の実行条件を変更・確認するとき。

## Do not read this when
- refactor fork の実際の変更処理や差分生成の挙動を確認したいとき。変更処理側の実装を直接読むこと。
- 変更要約の出力項目や JSON schema を確認したいとき。対応する schema 定義を直接読むこと。

## hash
- 31727a9d9e6e699906258cbf32b18b7fab70f27ae54cfe19371beaf16c07a4cc

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
- oracle file または realization file を起点とする、ファイル単位の実装レビュー兼修正用 AgentCallParameter を構築する。対象 path と linked worktree を受け取り、完全な調査・修正プロンプト、ファイルアクセス範囲、モデル設定、構造化出力スキーマ、事前インデックス実行条件をまとめる。
- レビュー対象ファイルを起点に、差分へ依存せず work-root 内の必要な oracle file と realization file を調査し、所見の修正と検証まで行わせる処理への入口である。

## Read this when
- ファイル単位の realization refactor fork のレビュー・修正処理を変更するとき
- レビュー用 AgentCallParameter のプロンプト構成、アクセスモード、モデル設定、構造化出力指定、パスコンテキストを確認するとき
- 対象ファイルを起点とした調査・修正・検証の完了条件や作業上の制約を確認するとき

## Do not read this when
- レビュー対象の実装そのものや、レビュー結果の構造化出力スキーマだけを確認したいとき
- ファイル単位ではない fork 処理や、別の prompt builder の責務だけを調査するとき
- 通常の realization 実装・テストの挙動を確認する場合は、対応する realization file または oracle file を直接読むとき

## hash
- 3d695ad5c71bce43e9aee3aa04d0443a72254c9b6f933ed8cb53246ec25dd33b
