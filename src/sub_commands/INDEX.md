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
- apply の開始・中断・統合に関する実装へ分岐する前の、最小限の目次として役割を切り分けます。

## Read this when

- `src/sub_commands/apply` 配下の入口構造をまとめて把握し、どの実装モジュールへ進むべきか整理したいとき。
- `cmoc apply` 系サブコマンドのパッケージ宣言と、`abandon.py`・`fork.py`・`join.py` の役割分担を確認したいとき。
- apply の開始・中断・統合の処理順をたどる前に、この階層のルーティング文書として概要を押さえたいとき。

## Do not read this when

- すでに `cmoc apply fork`、`cmoc apply join`、`cmoc apply abandon` のどれを読むか決まっていて、この階層の目次を確認する必要がないとき。
- 個別サブコマンドの実装や引数仕様だけを直接確認したいとき。
- `oracles` 側の正本仕様や利用手順だけを確認したいとき。

## hash

- 794d4d0aed803f84854318d0d9dbb627bd180d06f8038aef2cad8af695a9759f

# `indexing.py`

## Summary

- `cmoc indexing` の本体実装で、`repo_root` が未指定なら `run_command()` に処理を委譲します。
- `StepTimer` と `start_step()` を使って、repository 状態検証と `INDEX.md` メンテナンスまたは整合性検査の 2 段階で進みます。
- `assert_no_uncommitted_changes()` で clean repo を確認し、`check` モードでは `find_index_inconsistencies()`、通常モードでは `maintain_indexes()` を呼び分けます。
- 通常モードでは `INDEX.md` の変更有無に応じて標準出力を変え、`check` モードでは未反映の不整合があれば `CmocError` を送出します。

## Read this when

- `cmoc indexing` の実装・修正・レビュー・テストを行いたいとき。
- 実行前の未コミット差分チェックと `INDEX.md` メンテナンスの呼び出し順を確認したいとき。
- `run_command()` による `repo_root` 解決や、`StepTimer` と `start_step()` を使った 2 段階の処理フローを追いたいとき。
- `find_index_inconsistencies()` と `maintain_indexes()` のどちらを使うか、またその結果に応じてどこで標準出力やエラーが出るか確認したいとき。

## Do not read this when

- `cmoc indexing` の正本仕様だけを確認したいときは、`oracles/docs/app_specs/sub_commands/indexing.md` を直接読むべきです。
- `INDEX.md` の生成アルゴリズム、深い階層からの更新順、コミット対象の制御だけを確認したいときは、`src/commons/indexing.py` を直接読むべきです。
- `cmoc init`、`session`、`apply`、`review` など、別サブコマンドの実装を追いたいとき。
- `src/sub_commands` 配下の入口構造だけを確認したいときで、`cmoc indexing` 本体の処理は不要なとき。

## hash

- fce12fd41ef1f022d65537b43eb35089e1832b43e3b9973a0636cb4f23380efb

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

- `src/sub_commands/review` 配下のルーティング文書で、`cmoc review` 系サブコマンドの入口を整理する階層です。
- `__init__.py` はパッケージ宣言だけを担う最小モジュールです。
- `oracles.py` は `cmoc review oracles` の本体実装です。

## Read this when

- `src/sub_commands/review` の入口構造と、どの実装ファイルへ進むべきかを把握したいとき。
- `cmoc review oracles` の実装・修正・レビュー・テストを行いたいとき。
- review 用パッケージ宣言と中核実装の役割分担を確認したいとき。

## Do not read this when

- `cmoc review oracles` の実行フローや評価ロジックを追いたいときは、この目次ではなく `oracles.py` を直接読むべきとき。
- `cmoc review oracles` の利用手順、引数、出力仕様だけを確認したいときは、`oracles/docs/app_specs/sub_commands/review_oracles.md` を直接読むべきとき。
- `cmoc review` の CLI 登録や hidden alias だけを確認したいときは、`src/main.py` を読むべきとき。

## hash

- 324b076001f5daac44d3d344d5bad8b51bccc55f62f2a659ab2e241c966471dc

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
