# `apply`

## Summary
- `cmoc realization apply fork` の realization 追従用 AgentCallParameter を構築する定義。
- commit 範囲と oracle file の raw git diff を prompt に埋め込み、リポジトリ全体の oracle file と realization file の齟齬確認・反映作業へ接続する入口。

## Read this when
- `cmoc realization apply fork` の Agent call に、作業範囲、完了条件、realization 書き込み権限、linked worktree、indexing preflight を設定する方法を確認したいとき。
- commit 範囲と oracle file の raw git diff を追従対象変更として prompt に渡し、関連する oracle file と realization file をリポジトリ全体から調査させる条件を確認したいとき。

## Do not read this when
- 追従対象となる oracle file の具体的な差分や、個々の realization file への反映内容を確認したいとき。
- 共通の complete prompt 生成処理、構造化文書ノード、AgentCallParameter の一般仕様を確認したいとき。

## hash
- 6a36f0da6fbe98fc95a2b9e31875f966b1b3b2f210b92cbe062bb4620b35c833

# `refactor`

## Summary
- realization refactor の fork にある、変更要約用とファイル単位レビュー・修正用の agent call 定義、および各出力の Structured Output schema を扱う入口。
- 変更差分の意味論的分類と人間向け要約、要約 prompt の構築・実行条件を確認できる。
- ファイル単位レビュー・修正の対象範囲、oracle・realization の調査方針、修正と検証の条件、所見および変更 path の報告契約を確認できる。

## Read this when
- realization refactor の差分要約のカテゴリ、要約内容、根拠となる変更 file の扱いを確認するとき
- realization refactor の変更要約 agent call の prompt、読み取り権限、実行前 indexing 条件を調査するとき
- oracle file または realization file を起点とするファイル単位レビュー・修正の調査範囲、修正条件、検証条件を確認するとき
- レビュー所見の根拠、oracle 要求、観測実装、修正状態、検証結果、realization file の net 差分の報告形式を確認するとき

## Do not read this when
- realization refactor の実装内容、具体的な差分、個別の分類結果やレビュー所見を確認したいとき
- oracle file に記載された要求や設計責務そのものを確認するとき
- realization refactor 以外の agent call 構築、差分生成・適用、通常の入出力契約を調査するとき

## hash
- 988673e601c04074a857b8d938d37676cf7e6eaeb7814d686e2da68fb5b5ad93
