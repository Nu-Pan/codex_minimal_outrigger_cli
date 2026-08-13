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
- refactor fork の変更差分を人間向けに要約する agent call の prompt と起動パラメータを構築する定義。差分を動的 prompt に埋め込み、readonly の linked worktree 上で指定 schema の要約を生成する処理への入口。

## Read this when
- refactor fork の作業差分を要約する agent call の構築方法、入力差分の渡し方、実行モデルや作業ディレクトリなどの起動条件を確認するとき。

## Do not read this when
- refactor fork の差分要約そのものや出力形式だけを確認したいときは、変更要約用の schema を直接読む。
- refactor fork 以外の agent call 構築や、一般的な prompt の組み立て規則を確認するとき。

## hash
- b17cc5297186030d4e3176bae423ea5a5f9ece171ef159aea14893ed32dd6c79

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
- refactor fork におけるファイル単位レビュー・修正用の AgentCallParameter を構築する。対象ファイルを起点に完全プロンプトを生成し、oracle・realization の参照、レビュー、修正、検証、Structured Output の報告条件を定義する。
- パスコンテキスト、ファイルアクセス権限、モデル・推論設定、構造化出力スキーマ、実行時の作業ディレクトリをまとめ、ファイル単位の追従処理へ渡す入口となる。

## Read this when
- refactor fork のファイル単位レビュー・修正処理を追加・変更するとき
- 対象ファイルを起点とするレビュー用プロンプト、oracle・realization の参照規則、修正後検証の設定を確認するとき
- AgentCallParameter のモデル、作業ディレクトリ、アクセスモード、Structured Output 設定を確認するとき

## Do not read this when
- レビュー対象ファイルの実装内容そのものを調査するときは、対象の oracle file または realization file を直接読む
- レビュー結果の出力項目や JSON Schema の形式だけを確認するときは、関連する Structured Output schema を直接読む
- refactor fork 以外の AgentCallParameter 構築や、一般的なプロンプト生成の仕様だけを確認するとき

## hash
- 69bfa835a0e66f27e52a62ce2349dfc9c41db79f4a8256afee2271e6609ce1ab
