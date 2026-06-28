# `fork`

## Summary
- `cmoc apply fork` の AI エージェント呼び出しに関わる prompt builder と構造化出力契約をまとめる領域。差分要約、起点ファイルごとの適合性調査、検出済み所見への修正依頼という各フェーズで、role・goal・補助入力・file access mode・model/reasoning・Structured Output schema をどう組み立てるかへの入口になる。
- 実際の git 操作や作業ツリー操作ではなく、apply fork の各段階で AI に何を読ませ、何を出力させ、どの権限で呼び出すかを定義する責務を持つ。

## Read this when
- `cmoc apply fork` の作業レポート向けに、変更差分を人間向けカテゴリ別要約へ変換する AI 呼び出しや出力契約を確認したいとき。
- 起点ファイルから関連する oracle file と realization file を読ませ、仕様と実装の乖離や要修正所見を列挙させる調査フェーズの prompt、モデル指定、権限、出力形式を確認または変更したいとき。
- 検出済み所見を AI への修正作業指示へ変換する際の prompt 内容、realization file 修正条件、git add/commit 禁止、realization standard 適用などの作業条件を確認したいとき。
- apply fork 系で、AI エージェントに渡す raw diff、所見 JSON、起点パスなどの補助入力が complete prompt と AgentCallParameter にどう接続されるかを追いたいとき。
- apply fork のレビュー・要約・所見対応フェーズにおける Structured Output schema の意味的な責務と、その schema を使う呼び出し側の対応関係を確認したいとき。

## Do not read this when
- `cmoc apply fork` の CLI 引数解析、サブコマンド登録、実行フロー全体、git branch 操作、実際の fork 適用処理、作業ツリー変更処理を調べたいだけのとき。
- 個々の差分検出、差分分類アルゴリズム、ファイル列挙、複数ファイル分の呼び出し集約、結果の適用制御を確認したいとき。
- complete prompt の共通構築規則、Markdown rendering、StructDoc、path model、file access mode、AgentCallParameter などの基礎型や共通定義そのものを調べたいとき。
- 単一ファイルの本文内容、具体的な変更後コード、または realization file の実装修正箇所を直接調べたいだけのとき。
- 一般的な INDEX.md 用エントリーの書き方やルーティング文書全体の規約を確認したいとき。

## hash
- dfcfb1f164fc840aea194a1f73483c2ac39d2a5afcffeaea0da829f68e648827
