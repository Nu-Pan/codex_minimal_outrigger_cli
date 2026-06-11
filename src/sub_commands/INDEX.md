# `__init__.py`

## Summary

- `<work-root>/src/sub_commands/__init__.py` は `src.sub_commands` パッケージを宣言するだけの最小モジュールです。
- 公開 API、定数、実行ロジック、再エクスポートは持ちません。

## Read this when

- `src.sub_commands` が Python パッケージとして宣言されていることを確認したいとき。
- `<work-root>/src/sub_commands` ディレクトリの入口として、最小限の役割だけを把握したいとき。
- パッケージとしての存在確認だけで足り、追加の公開 API や実行処理が不要なとき。

## Do not read this when

- `<work-root>/src/sub_commands` 配下の個別サブコマンド実装や実行フローを確認したいとき。
- `apply`、`session`、`review`、`init`、`indexing` などの各モジュールの仕様を追いたいとき。
- `src.sub_commands` のパッケージ宣言ではなく、実際の業務ロジックや CLI 入口を見たいとき。

## hash

- ea4df02b820eba1ca77dfb1b2227c81dbff61cd7c4c2bf4d26d891369b57fa77

# `apply`

## Summary

- この `<work-root>/src/sub_commands/apply` ディレクトリのルーティング文書で、`cmoc apply` 系サブコマンド実装への入口です。
- `__init__.py`、`abandon.py`、`fork.py`、`join.py` の役割を素早く切り分けるための目次です。
- `apply` の実行制御、破棄、取り込みのどの実装へ進むべきかを判断する起点です。

## Read this when

- `cmoc apply` 系のパッケージ構成や、どのモジュールを読むべきか迷ったとき。
- `cmoc apply fork` の調査・修正ループや `abandon` / `join` の処理本体を追いたいとき。
- このディレクトリの各実装ファイルの役割を確認してから、詳細実装やテストに進みたいとき。

## Do not read this when

- すでに読む対象の `abandon.py`、`fork.py`、`join.py` が分かっていて、直接そのファイルへ進めるとき。
- `cmoc apply` の利用手順や仕様断片だけを確認したいときは、`<work-root>/oracles/docs/app_specs/sub_commands/` 側を読むべきとき。
- `<work-root>/src/sub_commands/apply` 以外のサブコマンド実装や、`README.md` などの運用ルールだけを確認したいとき。

## hash

- 527850383368036f8a48abf21594f411153558643e45094e47b5fa70dabc789a

# `indexing.py`

## Summary

- `<cmoc-root>/src/sub_commands/indexing.py` は `cmoc indexing` の本体実装モジュールで、CLI から受け取った `repo_root` を起点に共通 runner と `commons.indexing` へ処理を振り分けます。
- `repo_root` が未指定なら `commons.command_runner.run_command()` に委譲し、指定済みなら未コミット差分の事前チェック後に `maintain_indexes()` を実行します。
- 差分が発生した場合は `committed INDEX.md maintenance changes`、差分がなければ `no INDEX.md maintenance changes` を標準出力に出します。

## Read this when

- `cmoc indexing` の本体処理と、`repo_root` 未指定時の共通 runner への委譲経路を確認したいとき。
- `assert_no_uncommitted_changes()` による事前チェックと、`maintain_indexes()` 実行後の標準出力を確認したいとき。
- `StepTimer` と `start_step()` を使った `INDEX.md` メンテナンスの実行順を把握したいとき。

## Do not read this when

- `cmoc indexing` の生成アルゴリズム、配置対象の判定、既存 `INDEX.md` の再利用条件そのものを確認したいときは、`<cmoc-root>/src/commons/indexing.py` を読むべきです。
- CLI 登録やサブコマンドの起動経路だけを確認したいときは、`<cmoc-root>/src/main.py` を読むべきです。
- 利用手順や正本仕様だけを確認したいときは、`<cmoc-root>/oracles/docs/app_specs/sub_commands/indexing.md` を読むべきです。

## hash

- 822801872f1ebdc971018787dcf090c67c3ef542bfe891e0108a41b090cadf19

# `init.py`

## Summary

- `<work-root>/src/sub_commands/init.py` は `cmoc init` の本体処理を持つモジュールです。
- `repo_root` が未指定なら共通 runner に委譲し、指定済みなら `.cmoc` の ignore 確認と初期化変更の commit という 2 段階で処理します。
- .cmoc の ignore 保証、既存 tracked `.cmoc` の追跡解除、初期化に伴う差分 commit と結果表示をまとめて扱います。

## Read this when

- `cmoc init` の実装・修正・テスト・レビューを行いたいとき。
- `.cmoc` を git 追跡対象外にする処理、`.gitignore` 更新、tracked file の解除、初期化に伴う差分 commit 規則を確認したいとき。
- `run_command()` 経由で repo root を解決しつつ、`StepTimer` と `start_step()` で 2 段階の初期化フローをどう実行するかを把握したいとき。

## Do not read this when

- `cmoc init` 以外のサブコマンドの入口や CLI 登録だけを確認したいとき。
- .cmoc の ignore 保証や初期化 commit の流れが論点に入っていないとき。
- 初期化後の session / apply の運用仕様だけを追いたいとき。

## hash

- d521f2e6b339670dceeea2ae04fae5971c16a7ac9760586977de57e4f82240e6

# `review`

## Summary

- `<cmoc-root>/src/sub_commands/review` ディレクトリのルーティング文書で、`__init__.py` と `oracles.py` へ案内する入口です。
- `__init__.py` はパッケージ宣言のみを担う最小モジュールで、`oracles.py` は `cmoc review oracles` の本体実装です。
- この階層では、パッケージ構造の確認か、レビュー処理の実装確認かを切り分けて次の参照先を選びます。

## Read this when

- `<cmoc-root>/src/sub_commands/review` が Python パッケージとして宣言されていることを確認したいとき。
- `cmoc review oracles` の実装本体である `oracles.py` の実行フロー、評価パイプライン、Structured Output schema の扱いを追いたいとき。
- `cmoc review` 系サブコマンドの入口構造を把握してから、関連ファイルへ進みたいとき。

## Do not read this when

- `cmoc review oracles` の利用手順や引数仕様だけを確認したいときは、`<cmoc-root>/oracles/docs/app_specs/sub_commands/review_oracles.md` を読むべきです。
- `cmoc review` の CLI 登録や hidden alias だけを確認したいときは、`<cmoc-root>/src/main.py` を読むべきです。
- `<work-root>/src/sub_commands/review` の入口構造ではなく、`oracles.py` の実装詳細だけを直接確認したいときは、この `INDEX.md` を経由する必要はありません。

## hash

- 2cd09861a16a37ce63a059a9eb1a26222059b958680bedfc0d124ab6ff3d97b8

# `session`

## Summary

- `<work-root>/src/sub_commands/session` は `cmoc session` 系サブコマンド実装の入口ディレクトリです。
- `__init__.py` はパッケージ宣言だけを担う最小モジュールです。
- `abandon.py` は session branch の破棄、`fork.py` は session branch の作成、`join.py` は session branch の統合を担います。

## Read this when

- `<work-root>/src/sub_commands/session` 配下の入口構造と、どのモジュールを開くべきかを把握したいとき。
- `cmoc session fork` / `join` / `abandon` の責務分担や、各実装モジュールの役割を確認したいとき。
- session 系の実装・修正・レビュー・テストに入る前に、パッケージ全体の目次を整理したいとき。

## Do not read this when

- `cmoc session` 以外のサブコマンドの実装や CLI 登録だけを確認したいとき。
- `cmoc apply` 系や `cmoc review` 系の仕様・実装を追いたいとき。
- `oracles` 側の正本仕様だけを確認したいとき。

## hash

- b12b591472c17099b833589a6ea8fdeffa5febc7a25d65b8493a9682ebdb256b
