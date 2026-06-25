# `fork`

## Summary
- `cmoc apply fork` のレビュー・修正・変更要約工程で使う AI エージェント呼び出しと、その Structured Output schema をまとめる領域。差分要約、ファイル単位の所見列挙、検出済み所見の適用依頼に分かれ、git diff や oracle/realization の基準を読み取り専用コンテキストとして渡すための prompt 構築が中心になる。
- 適用後の差分を人間向けにカテゴリ化して報告する処理、realization file の要修正点を仕様との乖離として列挙する処理、または列挙済み所見を修正担当エージェントへ渡す処理へ進む入口になる。

## Read this when
- `cmoc apply fork` の内部で、レビュー所見の列挙、所見対応、作業後の変更要約といった AI 呼び出し工程の prompt や呼び出し条件を確認・変更したいとき。
- ファイル単位の所見リスト、差分カテゴリ別の変更要約など、この領域で使う Structured Output schema の意味上の責務を確認したいとき。
- oracle file と realization file、apply review standard、git diff、検出済み所見をどのように AI への読み取り専用コンテキストとして渡すかを追いたいとき。
- `cmoc apply fork` のレビュー工程で使う model class、reasoning effort、file access mode、出力 schema の対応関係を確認したいとき。

## Do not read this when
- `cmoc apply fork` 全体の orchestration、fork 作成、ブランチ操作、差分適用、git コマンド実行などの制御フローを調べたいとき。
- oracle standard、realization standard、apply review standard そのものの本文を確認したいとき。
- 汎用 prompt 部品、markdown rendering、StructDoc、AgentCallParameter 型定義、repo root 解決など、共通基盤側の実装を調べたいとき。
- 実際の変更対象ファイルの中身や、個々の差分検出・カテゴリ分類アルゴリズムを確認したいとき。

## hash
- 6a6c52c19a23e8306649ab4416e718f8664a6c991cbe19d38575a16ceae0d02a
