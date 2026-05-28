# `app_specs`

## Summary

- `cmoc` を実際にどう呼び出し、`init` から session/apply の反復作業へ進むかをまとめた使用手引きです。
- `PATH` 設定、初回の `cmoc init`、`session fork` / `review oracles` / `apply fork` / `apply join` / `session join` の全体フローを扱います。
- 人間が `<repo-root>/oracles` を更新しながら、実装追従と最終的な session 反映を回す前提を示します。

## Read this when

- `cmoc` の呼び出し方法や、最初に何を一度だけ行うかを確認したいとき。
- `oracles` の修正と `review oracles`、`apply`、`session` の一連の作業順を俯瞰したいとき。
- `cmoc` を使った日常の開発フローを、人間と AI の役割分担込みで理解したいとき。

## Do not read this when

- 個別サブコマンドの引数、状態遷移、終了条件などの詳細仕様だけを確認したいとき。
- `PATH` 設定やワークフローではなく、`branch_model` や `error_handling` などの共通仕様を確認したいとき。
- 実装コードやテストコードの修正だけで足りるとき。

## hash

- d3c3e927b356fc5cea9e1cfd1041d62a4ad6e721a7ee3654114e48538cab4573

# `considered_alternatives`

## Summary

- `cmoc` で採用しなかった設計案や、その不採用理由をまとめたディレクトリの入口です。
- 修正点リスト後の作業計画立案、AI-generated kaizen の自動注入、作業計画レビューの不採用理由を扱います。
- `oracles` と実装の役割分担を考えるときに、代替案の判断材料をたどるための目次です。

## Read this when

- `cmoc apply` 系で、修正点リスト完成後に作業計画を立てる案を採用しなかった理由を確認したいとき。
- AI-generated kaizen を次回の実行コンテキストへ自動的に持ち越さない方針と、その理由を整理したいとき。
- `tgbt plan` や `/plan` のような作業計画レビューを採用しなかった背景や、人間が `oracles` を編集して AI が追従する方針を把握したいとき。

## Do not read this when

- `cmoc apply` 系の実装手順やコマンド仕様そのものを確認したいときは、この配下ではなく該当する正本仕様を直接読むべきです。
- `INDEX.md` の生成ルールや `oracles` 全体のルーティング方針だけを確認したいときは、このディレクトリを読む必要はありません。
- この配下のうち特定の代替案だけを見たいときは、`apply_behavior.md`、`memory_alternative.md`、`working_plan_review.md` を直接参照すべきです。

## hash

- f2a1dd4e497749ef098f24010c2ea174bc89d7c7203024192c524c53e3bb0490

# `dev_rules`

## Summary

- `cmoc` の開発ルールをまとめたディレクトリの入口です。
- Python のコーディング規則、CLI と共通処理の設計方針、開発環境の前提、テスト実装規約を案内します。
- 実装やテストを書く前に、共通の作法と前提条件を素早く確認するための目次です。

## Read this when

- cmoc 全体のコーディング規則、設計方針、開発環境、テスト規約をまとめて確認したいとき。
- `src` と `tests` に実装を書く前に、共通の開発ルールを整理したいとき。
- Python の書き方、CLI の構成、仮想環境の扱い、テストの目的と範囲を俯瞰したいとき。

## Do not read this when

- cmoc の個別サブコマンドの手順や引数だけを確認したいときは、このディレクトリではなく該当する正本仕様を読むべきです。
- `INDEX.md` の生成・更新ルールだけを確認したいときは、このディレクトリではなく `indexing.md` を読むべきです。
- `oracles` 全体のルーティング方針や他の入口文書だけを確認したいときは、このディレクトリを読む必要はありません。

## hash

- 063534dc2090eb68dec8185beccb39c68d595cf015b9cf1568df4fe31f5ceb45
