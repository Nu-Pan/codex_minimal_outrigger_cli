# `oracle`

## Summary
- `oracle/src/oracle` は、cmoc が利用する oracle 側の Python 実装と Structured Output 定義をまとめる領域です。agent call パラメータ、feedback 入力、設定・パス・構造化文書、prompt 構築を扱い、各責務の詳細は `acp_builder`、`feedback`、`other`、`prompt_builder` の下位ディレクトリから確認します。

## Read this when
- oracle 配下の実装コードや Structured Output 定義の責務を調査・変更するとき
- agent call 構築、feedback reporter 入力、cmoc 設定・パス解決・Markdown レンダリング、prompt 構築のいずれかの入口を探すとき

## Do not read this when
- 人間が所有する oracle の意味仕様そのものを確認するとき
- cmoc の realization 実装、CLI 実行処理、テストの具体的な挙動を直接確認すれば足りるとき
- 特定の下位責務が明らかな場合は、この階層ではなく `acp_builder`、`feedback`、`other`、`prompt_builder` の該当ディレクトリを直接読むとき

## hash
- f17c55f666ea3b55412f13e4abc9265cdf0ec458555ef6fb18a0dfa59810a461
