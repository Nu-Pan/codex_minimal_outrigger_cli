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

- `src/sub_commands/apply` は `cmoc apply` 系サブコマンドの実装をまとめた Python パッケージです。
- `__init__.py` のパッケージ宣言と、`abandon.py` / `fork.py` / `join.py` の各本体実装を含みます。
- apply の開始・修正反復・取り消し・統合の処理順と共通補助を確認するための入口です。

## Read this when

- `cmoc apply` の入口構造や各モジュールの役割分担を把握したいとき。
- apply run の開始、取り消し、merge 取り込みの実装位置を素早く選びたいとき。
- どのモジュールを修正・テスト・レビューすべきかを判断したいとき。

## Do not read this when

- `cmoc session` や `cmoc review` の実装だけを追いたいとき。
- `cmoc apply` の利用手順や正本仕様だけを確認したいときは、`oracles/docs/app_specs/sub_commands/` 側を読むべきとき。
- `src/sub_commands/apply` 配下の個別挙動ではなく、共通開発ルールや `INDEX.md` 生成ルールだけを確認したいとき。

## hash

- 20b1b3be3968501e19bb84769cdf6cb700401a1af14bf1e52f1aa2fe55336593

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
