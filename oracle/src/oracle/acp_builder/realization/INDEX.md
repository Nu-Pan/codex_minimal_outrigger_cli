# `apply`

## Summary
- 対象ディレクトリの責務を、fork 経路の TUI 起動パラメータ構築と oracle 差分追従 agent 向け prompt 生成の入口として説明する。

## Read this when
- `cmoc realization apply fork` の TUI 起動処理、差分追従 prompt、対象 commit 範囲や raw oracle diff の受け渡し、AgentCallParameter の設定を変更・検証するとき。

## Do not read this when
- 通常の realization apply 処理や fork 以外の起動経路を調べるとき。prompt の共通部品や構造化文書の実装を直接確認する場合は、対応する prompt builder・構造化文書実装を先に読む。

## hash
- 79ae07a0923be45ce3302614622014379c09661e54e9fc95dfa7668986fa10af

# `refactor`

## Summary
- refactor fork における変更要約と、ファイル単位の realization review・fix 用 AgentCallParameter および Structured Output schema の正本を定義する。差分要約、所見・修正結果、prompt 構築、モデル・権限・検証設定を確認する入口である。

## Read this when
- refactor fork の変更差分を人間向けに要約する出力形式や prompt 構築方法を確認するとき。
- 単一ファイルの realization review・fix の構造化出力、prompt 構成、対象・権限・モデル設定を確認するとき。

## Do not read this when
- 実際の review・fix 処理そのものを確認したいとき。
- review・fix や変更要約の共通 prompt builder の仕様だけを確認したいとき。
- refactor fork 全体の状態遷移や候補ファイルの処理順を確認したいとき。

## hash
- f7b3492af78cf9239a6fa53b56dbdc21856145a425f2569821961e29695be2fe
