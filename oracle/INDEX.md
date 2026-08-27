# `doc`

## Summary
- cmoc の正本ドキュメントを集約するディレクトリ。アプリケーション仕様、branch・commit・worktree モデル、不採用案、Python 開発規約など、実装や運用の判断根拠となる上位文書への入口を提供する。各領域の詳細は配下の文書・ディレクトリで確認する。

## Read this when
- cmoc の正本仕様や開発規約を横断的に探すとき
- アプリケーション挙動、branch・worktree、設計上の不採用案、Python 開発・テスト規約の参照先を判断するとき
- 具体的な機能仕様や開発ルールの下位文書へ進む入口を確認するとき

## Do not read this when
- 特定機能の挙動や特定の開発規約を確認したい場合は、該当する配下の文書へ直接進むとき
- realization file の具体的な実装責務や現在の実装内容だけを確認するとき
- 既存の INDEX.md エントリー内容そのものを確認・更新するとき

## hash
- a3af185f146f9207b098f48f165ae97d8691d7b666d9ffffb37ee11c6e42a1af

# `src`

## Summary
- `oracle/src/oracle` は、cmoc が利用する oracle 側の Python 実装と Structured Output 定義の中核領域です。agent call パラメータ、feedback 入力、設定・パス・構造化文書、prompt 構築を扱い、詳細な責務ごとに `acp_builder`、`feedback`、`other`、`prompt_builder` へ分かれています。

## Read this when
- oracle 側の実装コードや Structured Output 定義の全体像を調査・変更するとき
- agent call の構築、feedback 入力、cmoc 設定・パス解決・構造化文書、prompt 構築の入口を探すとき
- 下位責務がまだ特定できず、適切な下位ディレクトリへのルーティングが必要なとき

## Do not read this when
- 人間が所有する oracle の意味仕様そのものを確認するとき
- cmoc の realization 実装、CLI 実行処理、テストの具体的な挙動を直接確認すれば足りるとき
- 特定の責務が明らかな場合は、この階層ではなく `acp_builder`、`feedback`、`other`、`prompt_builder` の該当ディレクトリを直接読むとき

## hash
- c3539dffe2759740eaf86ab7d54eb9e9666e534fa07f51d4e354463bac04c80a
