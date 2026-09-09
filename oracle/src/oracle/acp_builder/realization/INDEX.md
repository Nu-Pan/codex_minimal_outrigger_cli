# `apply`

## Summary
- 指定した始点・終点commit間のoracle file変更をrealization fileへ追従させるagentのpromptとAgentCallParameterを構築する。
- linked worktree、realization書き込み権限、実行前indexing、差分取得失敗時の報告条件を起動パラメータへ設定する。

## Read this when
- realizationの差分追従agentを起動するpromptとAgentCallParameterの構築経路を確認するとき。
- commit範囲内のoracle fileについて、追加・削除・rename・oracle配下内外の移動を含む変更判定条件を確認するとき。
- linked worktree、realization書き込み、実行前indexing、差分取得失敗時の扱いを確認するとき。

## Do not read this when
- fork処理の実行、Git差分の取得処理、またはrealization fileへの具体的な変更処理を調べるとき。
- 共通のprompt構築処理やAgentCallParameterの一般仕様だけを確認するとき。

## hash
- 1a7c545c1945749c633abcf0a8ffde4076221a1515e0aff35c99808776c51a1a

# `refactor`

## Summary
- refactor fork の変更差分を指定 commit 範囲から取得して分類・要約する agent call と、その起動パラメータおよび出力契約への入口。
- refactor fork の指定ファイルを起点に oracle・realization を調査し、realization の所見を修正・検証する agent call と、その権限・実行条件・出力契約への入口。

## Read this when
- 指定 commit 間の tree 差分を要約する agent call の prompt、実行条件、commit 範囲パラメータ、または変更要約の構造化出力契約を確認するとき
- 差分の有無に依存しないファイル単位レビュー・修正の対象範囲、realization への書き込み条件、所見の修正・検証ルール、またはレビュー結果の構造化出力契約を確認するとき

## Do not read this when
- 具体的な変更差分の内容、分類結果、レビュー対象ファイルの実装、個別の所見や修正結果を確認したいとき
- oracle 要求や realization 実装そのもの、共通 prompt の生成、構造化文書レンダリングの仕組みを直接調査・変更するとき

## hash
- c3978677de16c4e9c9913210e654257d656947613274247636402c7420633a46
