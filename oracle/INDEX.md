# `docs`

## Summary

- この `docs` ディレクトリのルーティング文書で、`app_specs/`、`considered_alternatives/`、`dev_rules/` への入口です。
- `path_model.md` ではパス表記の基本ルールとルートトークンを、`branch_model.md` では cmoc の branch/worktree モデルを案内します。
- 利用手順や共通仕様をたどるときは `app_specs/`、採用しなかった設計判断をたどるときは `considered_alternatives/`、開発規約を確認するときは `dev_rules/` に分岐します。

## Read this when

- cmoc の利用方法、共通仕様、パス表記、branch モデルの入口をまとめて把握したいとき。
- 採用しなかった設計案とその理由を確認したいとき。
- 実装やテストの前に、コーディング規約・設計方針・開発環境・テスト規約を整理したいとき。
- どの下位ディレクトリの文書や個別仕様を読むべきか迷ったとき。

## Do not read this when

- 目的の文書がすでに分かっていて、`app_specs/`、`considered_alternatives/`、`dev_rules/`、`path_model.md`、`branch_model.md` の該当ファイルへ直接進めるとき。
- この階層ではなく、各下位ディレクトリの `INDEX.md` や個別仕様ファイルだけを確認したいとき。
- `README.md` や `AGENTS.md` など、`docs` 以外のリポジトリ運用ルールだけを確認したいとき。

## hash

- f737c1fc659284ca0b8275ebc165ac36cc342d04d1b6219ce8fdc6d4b4e48556

# `schemas`

## Summary

- `<cmoc-root>/oracle/schemas/structured_output/` 配下の Structured Output schema をまとめた目次です。
- 現状は `structured_output/` を案内し、`cmoc review oracle` で使う JSON schema 群へ分岐します。
- 所見の列挙・統合・妥当性検証・採否判定の各段階に応じて、読むべき schema を切り分ける入口です。

## Read this when

- Structured Output schema の置き場所と役割分担を確認したいとき。
- `structured_output/` 配下の schema 一式へ進むべきか迷ったとき。
- `cmoc review oracle` 用の JSON schema を追加・修正・レビューしているとき。

## Do not read this when

- `structured_output/` 配下の個別 schema がすでに分かっていて、直接読むとき。
- `cmoc review oracle` の利用手順や評価フローだけを確認したいとき。
- Structured Output ではなく、`docs/` 配下の自然言語仕様や開発規約を探しているとき。

## hash

- fddfcc48c7f8fba67f3d097f0607e14f7ccd8cfd95924cca10b9c201dbce1040
