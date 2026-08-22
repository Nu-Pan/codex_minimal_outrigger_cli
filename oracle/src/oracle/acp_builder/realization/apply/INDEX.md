# `fork`

## Summary
- `cmoc realization apply fork` 用の AgentCallParameter を構築する定義。追従対象の commit 範囲と oracle file の raw git diff を prompt に組み込み、run worktree を起動コンテキストとして設定する。
- 差分追従 Agent のモデル・推論品質・realization 書き込み権限・調査、検証、routing 方針などの起動条件を定める。realization apply fork の起動方法や、oracle file の変更を realization file へ反映する処理を確認する際の入口となる。

## Read this when
- realization apply fork の Agent 起動パラメータ、prompt 構築、commit 差分の埋め込み、または run worktree の設定を確認・変更するとき。
- oracle file の変更を realization file 全体へ追従させる Agent call のモデル設定、権限設定、実行前 indexing 設定を確認するとき。

## Do not read this when
- 通常の realization implementation、test、ancillary の具体的な実装内容を確認する場合。
- Agent call の共通パラメータ型や prompt の共通生成規則を確認する場合は、それぞれの定義元を直接読む。

## hash
- 775886f92ab78ad0d28effda4ad3edfed8d38e80a7d59d8ff4f36b71cfe7fc5c
