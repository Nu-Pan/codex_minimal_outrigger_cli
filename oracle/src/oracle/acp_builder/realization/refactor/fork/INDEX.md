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
- refactor fork の作業差分を人間向けに要約するための prompt と AgentCallParameter を構築する定義。差分本文を動的 prompt に埋め込み、変更判断ではなく確定済み差分の要約に限定する。
- 読み取り専用・効率重視の agent call として、構造化出力 schema、実行ディレクトリ、preflight 実行有無、推論設定などの起動パラメータを組み立てる。

## Read this when
- refactor fork の差分要約用 agent call の prompt 構成や起動パラメータを変更・確認するとき
- raw git diff をどのように要約 agent へ渡すか、またその agent call の読み取り専用性や実行コンテキストを確認するとき

## Do not read this when
- refactor fork の実際の変更内容や要約結果を確認したいときは、生成済みの差分または要約出力を直接読む
- refactor fork 以外の agent call 構築や prompt の共通仕様を確認したいときは、対象の共通 builder・仕様ファイルを直接読む

## hash
- 5dc68b6040ff44076c3a4dd8584d841526c1fc8f96033fa34618b4978468cf07

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
- refactor fork のファイル単位レビュー・修正を行う agent call のパラメータ構築定義。対象 file を起点に oracle／realization の調査範囲、修正方針、検証要件、Structured Output の事後条件を含む prompt を組み立て、実装用 AgentCallParameter と schema path を返す。
- レビュー対象 file の path context を構築し、完全な prompt を生成する責務を担う。同階層の他定義ではなく、ファイル単位の realization review・fix 用 call を変更・調査するときの入口となる。
- model class、reasoning effort、realization write 権限、agent call の作業ディレクトリ、indexing preflight の設定もここで固定する。

## Read this when
- refactor fork のファイル単位レビュー・修正 prompt の内容や調査・修正方針を変更するとき
- 対象 path、run worktree、file access mode、モデル設定、reasoning effort、preflight 設定の構築方法を確認するとき
- Structured Output の変更 path 照合や、oracle／realization／findings／routing policy を prompt に組み込む方法を確認するとき

## Do not read this when
- レビュー・修正処理そのものの実装や、対象 realization file の内容を確認することが目的のときは、対応する realization file を直接読む
- Structured Output の項目や JSON schema の形式だけを確認したいときは、対応する schema file を直接読む
- refactor fork 以外の agent call の prompt 構築や、一般的な prompt builder の仕様だけを調べるとき

## hash
- e34ed8fde2ed9fd764e4742874d61efa9037ba953f63686ef84e511838799175
