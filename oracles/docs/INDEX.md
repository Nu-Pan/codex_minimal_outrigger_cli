# `app_specs`

## Summary

- `cmoc` の呼び出し手順から共通仕様、各サブコマンド入口までをまとめた `docs/app_specs` の目次です。
- `usage.md` で日常フロー、`branch_model.md` でブランチモデル、`sub_commands/` で個別サブコマンド仕様へ分岐します。
- `indexing.md` や `oracles.md` を含み、`INDEX.md` の配置・更新方針と `oracles` 取り扱いの入口にもなります。

## Read this when

- `cmoc` の利用方法、初回初期化、session/apply の反復フローをまとめて把握したいとき。
- branch モデル、`codex exec` 呼び出し、エラーハンドリング、セッション状態などの共通仕様を確認したいとき。
- `INDEX.md` の生成ルールや `oracles` 配下の読み方、個別サブコマンド仕様の入口を素早くたどりたいとき。

## Do not read this when

- 個別サブコマンドの引数や状態遷移だけを確認したいときは、`sub_commands/` 配下の該当文書を直接読むべきです。
- `dev_rules/` 側のコーディング規則、設計方針、テスト規約だけを確認したいときは、この目次ではなくそちらを読むべきです。
- `README.md` や `AGENTS.md` などのリポジトリ運用ルールだけを確認したいときは、このディレクトリを読む必要はありません。

## hash

- 646256542f483fabc4c22b4a4c72529b0accc4d4bedc9634dc8ff0bcdbd80abc

# `considered_alternatives`

## Summary

- `cmoc` で採用しなかった設計案と、その不採用理由をまとめたディレクトリの入口です。
- 修正点リスト後の作業計画立案、AI-generated kaizen の自動注入、作業計画レビューの不採用理由を扱います。
- `oracles` と実装の役割分担を考えるときに、代替案の判断材料をたどるための目次です。

## Read this when

- `cmoc apply` 系で、修正点リスト完成後に作業計画を立てる案を採用しなかった理由を確認したいとき。
- AI-generated kaizen を次回の実行コンテキストへ自動的に持ち越さない方針と、その理由を整理したいとき。
- `tgbt plan` や `/plan` のような作業計画レビューを採用しなかった背景や、人間が `oracles` を編集して AI が追従する方針を把握したいとき。

## Do not read this when

- `cmoc apply` 系の実装手順やコマンド仕様そのものを確認したいときは、該当する正本仕様を直接読むべきです。
- `INDEX.md` の生成ルールや `oracles` 全体のルーティング方針だけを確認したいときは、このディレクトリを読む必要はありません。
- この配下のうち特定の代替案だけを見たいときは、`apply_behavior.md`、`memory_alternative.md`、`working_plan_review.md` を直接参照すべきです。

## hash

- 5326c864cc9e8c75a90c03568805dc2c2049a51f0d7e375da4b44b4c92c0fe00

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

- cmoc の個別サブコマンドの仕様や引数だけを確認したいとき。
- `oracles` 全体のルーティング方針や他ディレクトリの入口文書だけを確認したいとき。
- `INDEX.md` の生成・更新ルールそのものだけを確認したいときは、ここではなく `indexing.md` を参照すべきとき。

## hash

- 3e4d31733982a9b80629b97d1b9396964a868e7cbfeda46f65c00eb9564a46fd
