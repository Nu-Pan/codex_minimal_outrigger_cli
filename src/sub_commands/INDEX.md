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

- `src/sub_commands/apply` 配下のルーティング文書で、`cmoc apply` パッケージ内の実装モジュールへ案内する入口です。
- パッケージ宣言の `__init__.py` と、`abandon.py`、`fork.py`、`join.py` の各実装ファイルを目的別に切り分けます。

## Read this when

- `src/sub_commands/apply` 配下で、どの実装モジュールを開くべきか迷ったとき。
- `cmoc apply fork`、`cmoc apply join`、`cmoc apply abandon` の責務や入口を一覧で把握したいとき。
- `src/sub_commands/apply` の構成をレビュー・修正・テスト前に整理したいとき。

## Do not read this when

- `src/sub_commands/apply` 配下の読み先がすでに決まっていて、`__init__.py`、`abandon.py`、`fork.py`、`join.py` のいずれかへ直接進むとき。
- `cmoc apply` の利用手順や正本仕様だけを確認したいとき。
- この階層ではなく、上位の `src/sub_commands/INDEX.md` だけで十分なとき。

## hash

- 92101a40048dabe808713af15ca35aad2f4a025a8d217204ad9b5273d322aebe

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

- `src/sub_commands/review` ディレクトリのルーティング文書で、`__init__.py` と `oracles.py` へ案内する入口です。
- `__init__.py` はパッケージ宣言のみを担う最小モジュールで、`oracles.py` は `cmoc review oracles` の本体実装です。
- この階層では、パッケージ構造の確認か、レビュー処理の実装確認かを切り分けて次の参照先を選びます。

## Read this when

- `src/sub_commands/review` が Python パッケージとして宣言されていることを確認したいとき。
- `cmoc review oracles` の実装本体である `oracles.py` の実行フロー、評価パイプライン、Structured Output schema の扱いを追いたいとき。
- `cmoc review` 系サブコマンドの入口構造を把握してから、関連ファイルへ進みたいとき。

## Do not read this when

- `cmoc review oracles` の利用手順や引数仕様だけを確認したいときは、`oracles/docs/app_specs/sub_commands/review_oracles.md` を読むべきです。
- `cmoc review` の CLI 登録や hidden alias だけを確認したいときは、`src/main.py` を読むべきです。
- `src/sub_commands/review` の入口構造ではなく、`oracles.py` の実装詳細だけを直接確認したいときは、この `INDEX.md` を経由する必要はありません。

## hash

- 2cd09861a16a37ce63a059a9eb1a26222059b958680bedfc0d124ab6ff3d97b8

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

- b12b591472c17099b833589a6ea8fdeffa5febc7a25d65b8493a9682ebdb256b
