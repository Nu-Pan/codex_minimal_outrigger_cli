# `app_specs`

## Summary

- `cmoc` のアプリ仕様断片をまとめた入口で、`branch_model`、`codex_call`、`console_and_file_log`、`error_handling`、`indexing`、`misc_specs`、`oracles`、`session_state`、`usage`、`sub_commands` への案内をまとめます。
- `sub_commands/INDEX.md` から `apply`、`session`、`eval-oracles`、`init` など個別サブコマンドの正本仕様へたどれます。
- `INDEX.md` 自体の生成・更新ルールは `indexing.md` が担当し、`oracles` の扱いは `oracles.md` が担当します。

## Read this when

- `cmoc` の共通仕様や、その参照先となる正本断片を確認したいとき。
- `apply`、`session`、`eval-oracles`、`init` などの前提になるルールを横断的に見直したいとき。
- どの仕様ファイルを読むべきか、`app_specs` 配下の案内から判断したいとき。
- 個別サブコマンドの入口を含めて、`branch_model`、`codex_call`、ログ、エラー処理、利用方法のどこへ進むべきか整理したいとき。

## Do not read this when

- 個別サブコマンドの手順だけを確認したいときは、`sub_commands/INDEX.md` から該当文書へ直接進むべきです。
- 特定の仕様本文だけを読みたいときは、対応する `*.md` を直接参照すべきです。
- 実装コードやテストコードだけで足りる場合は、このディレクトリの案内を読む必要はありません。
- `INDEX.md` の生成・更新ルールだけを確認したいときは、`indexing.md` を読むべきです。

## hash

- aad42a59c4a387144a49a40b5aae5776c1d864d73441f6d118bb6cf058ab2140

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

- `cmoc` の開発ルールをまとめたディレクトリの入口です。Python 実装のコーディング規約、CLI と共通機能の設計方針、開発環境の前提、テスト規約を扱います。
- `coding_rules.md` は型ヒント、import、docstring、コメント、ログメッセージ、非公開識別子などのコーディング規則を定めます。
- `design_rules.md` は `src/main.py`、`src/sub_commands`、`src/commons` の配置方針と、関数分割・並び順の考え方を定めます。
- `development_environment.md` は対象 OS、Python バージョン、`.venv` の扱い、文字コードなどの開発環境前提を定めます。
- `test_rules.md` は pytest を使った自動テストの書き方、配置先、Fake Codex CLI の扱いを定めます。

## Read this when

- `cmoc` の Python 実装やレビューで、基本的なコーディング規約を確認したいとき。
- CLI のエントリーポイント、サブコマンド配置、共有機能の置き場所、関数分割方針を決めたいとき。
- 開発環境、Python バージョン、仮想環境、文字コードなどの前提を確認したいとき。
- pytest ベースの自動テスト方針や、Fake Codex CLI を使う可否を確認したいとき。
- 実装やテストが `dev_rules` のどの規則に従うべきかを切り分けたいとき。

## Do not read this when

- `cmoc` のユーザー向けコマンド手順や各サブコマンドの仕様だけを確認したいとき。
- `branch_model`、`apply`、`eval-oracles` などの個別仕様だけを確認したいとき。
- `INDEX.md` の生成・更新ルールそのものだけを確認したいとき。
- コーディング、設計、開発環境、テストのうち特定の 1 領域だけを深掘りしたいとき。

## hash

- 063534dc2090eb68dec8185beccb39c68d595cf015b9cf1568df4fe31f5ceb45
