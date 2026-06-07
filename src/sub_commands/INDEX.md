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

- この `apply` ディレクトリのルーティング文書で、`cmoc apply fork`、`cmoc apply join`、`cmoc apply abandon` の実装入口へ案内する目次です。
- `__init__.py` はパッケージ宣言のみ、`fork.py` は開始と修正ループ、`join.py` は session への取り込み、`abandon.py` は未 join の apply run の破棄を担います。
- 個別の実装を読む前に、目的に応じてどの `apply` サブコマンドへ進むべきかを切り分けるための文書です。

## Read this when

- `src/sub_commands/apply` 配下の `cmoc apply` 実装の入口を把握したいとき。
- `cmoc apply fork`、`cmoc apply join`、`cmoc apply abandon` の処理順や状態遷移を確認したいとき。
- `apply` 系サブコマンドのパッケージ構成と、各モジュールの役割分担を確認したいとき。
- `cmoc apply` の実装・修正・テスト・レビューを始める前に、どのファイルへ進むべきかを切り分けたいとき。

## Do not read this when

- `cmoc apply` の利用手順や正本仕様だけを確認したいときは、`oracles/docs/app_specs/sub_commands/` 側の該当文書を読むべきとき。
- `cmoc session fork`、`cmoc session join`、`cmoc session abandon` など、session 側の開始・統合・破棄だけを確認したいとき。
- `cmoc review oracles` や `cmoc init` など、`apply` 以外のサブコマンド実装を追いたいとき。
- `src/sub_commands/apply/__init__.py` だけで十分で、パッケージ宣言以外の実装を読む必要がないとき。

## hash

- 8c32fac4549c8565c6466e29e5efd3cd3591c846a2317d6be16d78de0fb83dca

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

- `src/sub_commands/review` は `cmoc review` 系サブコマンドの入口ディレクトリです。
- `__init__.py` はパッケージ宣言だけを担う最小モジュールです。
- `oracles.py` は `cmoc review oracles` の本体処理を担い、スナップショット固定、評価、改善、レポート出力までを実行します。

## Read this when

- `src/sub_commands/review` が Python パッケージとして宣言されていることを確認したいとき。
- `cmoc review` 系サブコマンドの入口構造や、`oracles.py` の役割を把握したいとき。
- `cmoc review oracles` の本体処理、開始時点の `oracles` スナップショット固定、評価、改善、レポート出力の流れを確認したいとき。

## Do not read this when

- `cmoc review oracles` の利用手順や引数だけを確認したいときは、`oracles/docs/app_specs/sub_commands/review_oracles.md` を読むべきです。
- `cmoc review` の CLI 登録や hidden alias だけを確認したいときは、`src/main.py` を読むべきです。
- `INDEX.md` の生成・更新ルールや、`oracles` 全体のルーティング方針だけを確認したいときは、このディレクトリを読む必要はありません。

## hash

- 85794ff51a4f9a190c00cedff044aa30985d0fa29a59ff9ca6121f5d889e709d

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
