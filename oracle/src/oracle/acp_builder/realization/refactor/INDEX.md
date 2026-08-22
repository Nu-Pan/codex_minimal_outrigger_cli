# `fork`

## Summary
- `change_summary.json` と `change_summary.py` は、refactor fork における変更差分要約 agent call の出力契約と起動パラメータ構築を扱う入口である。差分をカテゴリ別に要約する形式、raw_git_diff の埋め込み、linked worktree を実行コンテキストにする設定、モデル・アクセスモード・Structured Output schema の指定を確認する必要がある場合に読む。
- `file_review_and_fix.json` と `file_review_and_fix.py` は、refactor fork におけるファイル単位のレビュー・修正 agent call の出力契約と起動パラメータ構築を扱う入口である。レビュー所見と修正結果の記録形式、対象ファイルを起点とした調査範囲、oracle／realization の扱い、修正・検証要件、AgentCallParameter の構成を確認する必要がある場合に読む。

## Read this when
- refactor fork の変更差分要約 agent call の出力形式、prompt、実行コンテキスト、アクセスモード、モデル設定、Structured Output schema の指定を確認・変更するとき
- refactor fork のファイル単位レビュー・修正 agent call の出力契約、調査範囲、修正権限、検証要件、prompt や AgentCallParameter の構築方法を確認・変更するとき

## Do not read this when
- 変更差分の要約生成ロジック自体を調べる場合は、差分取得・生成を担当する実装を直接読むとき
- レビュー対象の実装、個別仕様、所見判定、またはレビュー・修正 agent の実行処理を調べる場合は、対応する実装や oracle／realization file を直接読むとき
- 構造化出力の項目・型・形式だけを確認する場合は、各 JSON schema を直接読むとき
- 一般的な prompt builder、path model、struct document の仕様を確認する場合は、それぞれの担当実装・仕様を直接読むとき

## hash
- 956a8715e5e0062f48baeaa5a54b42aec5a48e147dd9e62d094f4dd5cf2db4c6
