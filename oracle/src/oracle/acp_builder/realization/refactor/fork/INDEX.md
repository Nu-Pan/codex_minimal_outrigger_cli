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
- refactor fork の確定済み Git 差分を人間向けに要約する agent call の定義。prompt の役割・要約対象・完了条件、読み取り専用の実行条件、実行モデルや推論設定、linked worktree の扱い、Structured Output schema の参照先をまとめて構築する。refactor fork の変更要約処理へ進む入口であり、一般的な prompt 構築や refactor 本体の実装とは責務が異なる。

## Read this when
- refactor fork の変更要約 agent call の起動パラメータ、prompt、読み取り専用の実行条件を確認するとき
- refactor 差分を入力とする要約処理のモデル分類、推論設定、作業ディレクトリ、Structured Output schema の構成を変更または調査するとき

## Do not read this when
- refactor fork の実際のコード変更や差分生成処理を調べるとき
- refactor と無関係な prompt の共通構築規則を調べるとき
- 変更要約の出力項目や JSON schema の詳細だけを確認するときは、対応する schema 定義へ直接進む

## hash
- cd77f8c64c6201ed4c3cee9eee1772ac87afb788b0d8120b7063dca25352fe16

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
- refactor fork におけるファイル単位レビュー・修正用の AgentCallParameter を構築する定義。対象パスを起点に完全プロンプト、アクセス権、モデル設定、構造化出力スキーマ、作業用 worktree を組み立てる。

## Read this when
- ファイル単位のレビュー・修正 agent call の prompt や実行パラメータを変更・確認するとき
- レビュー結果の構造化出力、oracle/realization 参照規則、修正後検証の要求を確認するとき
- refactor fork のレビュー処理から agent call を起動する経路を調査するとき

## Do not read this when
- レビュー対象ファイルの実装内容や個別の所見だけを確認するとき
- 一般的な prompt 構築機能や別の agent call 種別を調査するとき
- 構造化出力 JSON Schema の具体的な制約だけを確認するとき

## hash
- 276ababf5454576e1f351a31fd91e5575b8b55123098dd2b0b5d8890bdb26ea2
