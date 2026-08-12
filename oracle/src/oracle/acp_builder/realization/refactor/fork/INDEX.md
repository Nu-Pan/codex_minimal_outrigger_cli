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
- 対象ファイルは、refactor fork におけるファイル単位レビュー・修正用 AgentCallParameter の構築を担う。対象 path と run worktree を受け取り、レビュー対象を起点に調査・修正・検証を行う完全な prompt、oracle/realization の参照規則、書き込み範囲、構造化出力 schema、実行設定を組み立てる。
- このファイルはレビュー兼修正 agent の呼び出し定義を確認または変更するときの入口であり、実際のレビュー prompt 文面や出力契約を変更する場合に読む。呼び出し対象の個別レビュー実装や、schema の詳細だけを確認する場合は、それぞれの直接の定義へ進む。

## Read this when
- refactor fork のファイル単位レビュー・修正 agent の呼び出しパラメータ、prompt 構築、アクセス権限、検証規則、または実行モデル設定を確認・変更するとき
- ファイル単位レビュー用 agent が、対象ファイルを起点にどの範囲を調査し、どの条件で realization file を修正するかを確認するとき
- この agent call の構造化出力契約と、変更 path 集合の申告条件を含む事後条件を確認するとき

## Do not read this when
- レビュー対象ファイルそのものの実装内容や、レビュー結果の所見だけを確認したいとき
- 構造化出力 schema の項目・型・形式だけを確認したいときは、対応する schema 定義を直接読む
- 共通 prompt 構築処理や path 解決処理だけを確認したいときは、対応する共通実装を直接読む

## hash
- bfeeff85da635b4807768764c42bbdeee1ed2830e087efc501a2b321a44ef52d
