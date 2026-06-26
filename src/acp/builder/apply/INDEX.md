# `fork`

## Summary
- フォーク適用作業に関わる AI エージェント呼び出しと、その結果を受け渡す構造化出力 schema をまとめた領域。変更要約生成、ファイル単位の要修正点列挙、検出済み所見の修正依頼という、適用後レビューから修正・レポート化までの補助処理への入口になる。

## Read this when
- フォーク適用処理の中で、AI エージェントに差分要約、所見列挙、所見対応を依頼する prompt や呼び出し条件を確認・変更したいとき。
- フォーク適用後のレビュー結果や変更要約を、構造化出力としてどの粒度・責務で受け渡すかを確認したいとき。
- 対象パス、work tree、git diff、所見 JSON、標準参照などが、フォーク適用関連の AI 呼び出しへどのように埋め込まれるかを追いたいとき。

## Do not read this when
- フォーク作成、ブランチ操作、差分取得、ファイル適用など、フォーク適用全体の実行制御や git 操作そのものを調べたいとき。
- oracle file、realization file、apply review standard などの正本仕様や標準文書の内容そのものを確認したいとき。
- 汎用 prompt 構築、markdown rendering、path 解決、AgentCallParameter や model class の共通定義を調べたいとき。

## hash
- b3803215560b94a2b0c6a709ceb98305174d3951980a125aa45b6a982ad78b60
