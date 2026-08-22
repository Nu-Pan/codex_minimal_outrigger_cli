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
- refactor fork におけるファイル単位レビュー・修正用の AgentCallParameter 構築定義。対象ファイルを起点に、必要な oracle／realization file を含む完全な調査・修正・検証 prompt を組み立て、指定 schema に従う agent call を返す。
- 対象 path と linked worktree を AgentCallPathContext に設定し、対象 file の解決済みパス、アクセスモード、oracle／realization／routing／findings policy、構造化 prompt、schema path、最大推論設定などをまとめる実装。

## Read this when
- refactor fork のファイル単位レビュー・修正 agent call の prompt 構築方法を確認するとき
- 対象 file を起点とする調査範囲、realization write 権限、検証要件、構造化出力の事後条件を変更するとき
- AgentCallParameter のモデル、reasoning effort、作業ディレクトリ、schema の指定方法を追跡するとき

## Do not read this when
- レビュー・修正 agent の実際の処理ロジックや所見判定を確認したい場合は、構築された prompt の実行側または対応する oracle／realization file を直接読むとき
- 構造化出力の項目や型だけを確認したい場合は、参照される schema file を直接読むとき
- 一般的な prompt builder、path model、struct document の仕様だけを調べる場合は、それぞれの実装・仕様 file を直接読むとき

## hash
- 2acc323186b24e07521f6bb4b1702b1f0a0fd209f6ab2b4b0b8c16160ef60670
