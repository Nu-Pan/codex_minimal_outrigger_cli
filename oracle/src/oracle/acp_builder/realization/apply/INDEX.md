# `fork`

## Summary
- 対象は、`cmoc realization apply fork` が oracle file の差分を realization file に反映するための AgentCallParameter を構築する定義です。commit 範囲・raw git diff・実行コンテキスト・権限・モデル設定・調査検証方針の確認や変更時に、このディレクトリの入口として読みます。

## Read this when
- `cmoc realization apply fork` の prompt 内容、差分追従の完了条件、AgentCallParameter の起動設定を確認・変更するとき。
- oracle file の変更を realization 全体へ反映する agent call の作業範囲、権限、パスコンテキストを調査するとき。

## Do not read this when
- realization の具体的な実装・テスト・補助ファイルを確認または変更する場合は、生成 prompt の定義ではなく対象の realization file を直接読む。
- 一般的な prompt 構築や、他の realization 起動経路を調査する場合は、それぞれの builder 定義を直接読む。

## hash
- 2465d8396deba8c46b2f1cd1931d37c0249eabfdf287e8edb5d99599a935a343
