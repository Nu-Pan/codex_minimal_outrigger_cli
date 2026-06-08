# `__init__.py`

## Summary

- `src/sub_commands/__init__.py` は `src.sub_commands` パッケージを宣言するだけの最小モジュールです。
- 公開 API、定数、実行ロジック、再エクスポートは持ちません。

## Read this when

- `src.sub_commands` が Python パッケージとして宣言されていることを確認したいとき。
- `src/sub_commands` ディレクトリの入口として、最小限の役割だけを把握したいとき。
- パッケージとしての存在確認だけで足り、追加の公開 API や実行処理が不要なとき。

## Do not read this when

- `src.sub_commands` 配下の個別サブコマンド実装や実行フローを確認したいとき。
- `apply`、`session`、`review`、`init` などの各モジュールの仕様を追いたいとき。
- `src.sub_commands` のパッケージ宣言ではなく、実際の業務ロジックや CLI 入口を見たいとき。

## hash

- ea4df02b820eba1ca77dfb1b2227c81dbff61cd7c4c2bf4d26d891369b57fa77

# `apply`

## Summary

- `src/sub_commands/apply` 配下のルーティング文書で、`cmoc apply` 系サブコマンドへ進むための入口です。
- `__init__.py` はパッケージ宣言、`abandon.py` は `cmoc apply abandon`、`fork.py` は `cmoc apply fork`、`join.py` は `cmoc apply join` の本体実装を案内します。
- apply の開始・統合・破棄に関する実装へ分岐する前の、最小限の目次として役割を切り分けます。

## Read this when

- `src/sub_commands/apply` 配下の入口構造をまとめて把握し、どの実装モジュールへ進むべきか整理したいとき。
- `cmoc apply` 系サブコマンドのパッケージ宣言と、`abandon.py`・`fork.py`・`join.py` の役割分担を確認したいとき。
- apply の開始・統合・破棄に関する処理順をたどる前に、この階層のルーティング文書として概要を押さえたいとき。
- `src/sub_commands/apply` 配下の構成を変更・追加・再配置する前に、既存の案内先を確認したいとき。

## Do not read this when

- すでに `cmoc apply fork`、`cmoc apply join`、`cmoc apply abandon` のどれを読むか決まっていて、個別の実装モジュールへ直接進めるとき。
- 個別サブコマンドの引数仕様や処理本体だけを確認したいとき。
- `oracles` 側の正本仕様や利用手順だけを確認したいとき。

## hash

- eb7bf45e95efc57506f723a4a3763eeb10c1e95c98c77c483facfb7e0ee9c058

# `indexing.py`

## Summary

- `src/sub_commands/indexing.py` は `cmoc indexing` の本体処理を持つモジュールです。
- `repo_root` が未指定なら共通 runner に処理を委譲し、指定済みなら repository 状態検証と `INDEX.md` メンテナンスの 2 段階で進みます。
- `assert_no_uncommitted_changes()` で clean repo を確認し、`maintain_indexes()` の結果に応じて標準出力を切り替えます。

## Read this when

- `cmoc indexing` の実装・修正・レビュー・テストを行いたいとき。
- `repo_root` の自動解決や、`StepTimer` と `start_step()` を使った 2 段階の処理フローを確認したいとき。
- 実行前の未コミット差分チェックと、`INDEX.md` メンテナンス後の標準出力を確認したいとき。

## Do not read this when

- `INDEX.md` の生成アルゴリズム、再利用条件、配置対象の判定だけを確認したいときは、このモジュールではなく `src/commons/indexing.py` を読むべきです。
- `cmoc indexing` の正本仕様や利用手順だけを確認したいときは、`oracles/docs/app_specs/sub_commands/indexing.md` を直接読むべきです。
- `cmoc` の他のサブコマンドの入口や実装を追いたいときは、このファイルではなく該当モジュールを読むべきです。

## hash

- 1d50ad1105d309676b3745dcc539bb313c9b31f155df7a1cd8a90c6459d5b2de

# `init.py`

## Summary

- `src/sub_commands/init.py` は `cmoc init` の本体処理を持つモジュールです。
- `repo_root` が未指定なら共通 runner に委譲し、指定済みなら `.cmoc` の ignore 確認と初期化変更の commit という 2 段階で処理します。
- `.cmoc` の ignore 保証、既存 tracked `.cmoc` の追跡解除、初期化に伴う差分 commit と結果表示をまとめて扱います。

## Read this when

- `cmoc init` の実装・修正・テスト・レビューを行いたいとき。
- `.cmoc` を git 追跡対象外にする処理、`.gitignore` 更新、tracked file の解除、初期化差分の commit 規則を確認したいとき。
- `run_command()` 経由で repo root を解決しつつ、`StepTimer` と `start_step()` で 2 段階の初期化フローをどう実行するかを把握したいとき。

## Do not read this when

- `cmoc init` 以外のサブコマンドの入口や CLI 登録だけを確認したいとき。
- `.cmoc` の ignore 保証や初期化 commit の流れが論点に入っていないとき。
- 初期化後の session / apply の運用仕様だけを追いたいとき。

## hash

- d521f2e6b339670dceeea2ae04fae5971c16a7ac9760586977de57e4f82240e6

# `review`

## Summary

- この `src/sub_commands/review` 配下のルーティング文書で、`cmoc review` 系サブコマンドの入口を整理する階層です。
- `__init__.py` はパッケージ宣言だけを担う最小モジュールです。
- `oracles.py` は `cmoc review oracles` の本体実装です。

## Read this when

- `src/sub_commands/review` の入口構造と、どの実装ファイルへ進むべきかを把握したいとき。
- `cmoc review oracles` の実装・修正・レビュー・テストを行いたいとき。
- review 用パッケージ宣言と中核実装の役割分担を確認したいとき。

## Do not read this when

- `cmoc review oracles` の実行フローや評価ロジックそのものを追いたいときは、この目次ではなく `src/sub_commands/review/oracles.py` を直接読むとき。
- `cmoc review oracles` の利用手順、引数、出力仕様だけを確認したいときは、`oracles/docs/app_specs/sub_commands/review_oracles.md` を直接読むとき。
- `cmoc review` の CLI 登録や hidden alias だけを確認したいときは、`src/main.py` を読むとき。

## hash

- 108c291e5bcbac9153b93e2a76563d4962b5b26daad11fd44ecea1c50258e88a

# `session`

## Summary

- `src/sub_commands/session` は `cmoc session` 系サブコマンド実装の入口ディレクトリです。
- `__init__.py` はパッケージ宣言だけを担う最小モジュールです。
- `abandon.py` は session branch の破棄、`fork.py` は session branch の作成、`join.py` は session branch の統合を担います。

## Read this when

- `src/sub_commands/session` 配下の入口構造と、どのモジュールを開くべきかを把握したいとき。
- `cmoc session fork` / `join` / `abandon` の責務分担や、各実装モジュールの役割を確認したいとき。
- session 系の実装・修正・レビュー・テストに入る前に、パッケージ全体の目次を整理したいとき。

## Do not read this when

- `cmoc session` 以外のサブコマンドの実装や CLI 登録だけを確認したいとき。
- `cmoc apply` 系や `cmoc review` 系の仕様・実装を追いたいとき。
- `oracles` 側の正本仕様だけを確認したいとき。

## hash

- 92a4881bdb0a53d39acb955bd2f2b695b91c7332cb32fc52ab8c5771bd25536a
