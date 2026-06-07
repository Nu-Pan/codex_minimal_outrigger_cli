# `commons`

## Summary

- `src/commons` 配下の共通モジュール群へのルーティング文書で、`cmoc` の実行基盤や補助処理をまとめて案内する階層です。
- `__init__.py` に加えて、`codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`report_files.py`、`subcommand_log.py`、`timestamps.py`、`timing.py` へ進むための入口です。
- CLI 実行、共通エラー整形、repo / worktree 操作、`INDEX.md` 維持、サブコマンドログ、時間計測、タイムスタンプ、レポート保存を切り分けるための目次です。

## Read this when

- `src/commons` がどの共通モジュールをまとめているかを一覧したいとき。
- `codex exec` の呼び出し基盤、サブコマンド共通実行、エラー整形、repo 管理、`INDEX.md` 維持、ログ、時刻・時間計測の入口を切り分けたいとき。
- `INDEX.md` から `src/commons/*.py` のどれへ進むべきか迷ったとき。
- package 入口の `__init__.py` を含めて、commons 配下の役割分担を確認したいとき。

## Do not read this when

- 目的の共通モジュールがすでに分かっていて、`codex.py` や `repo.py` などの個別ファイルへ直接進めるとき。
- サブコマンド固有の業務ロジックや `src/sub_commands` 側の実装だけを確認したいとき。
- `oracles` 側の正本仕様や `docs/` のルーティングだけを確認したいとき。
- `README.md` や `AGENTS.md` など、リポジトリ運用ルールだけを確認したいとき。

## hash

- bb6479ae760ce716dd11d53d0fceacf86cf4745d14f8399661bedd32cb6d3ed4

# `main.py`

## Summary

- `src/main.py` は cmoc CLI のエントリーポイントで、Typer のルート `app` と `session` / `apply` / `review` の各サブアプリを組み立てるファイルです。
- `init`、`indexing`、`session`、`apply`、`review` の各コマンド登録に加えて、`eval-oracle` / `eval-oracles` の隠し別名や各コマンドの既定オプションをまとめています。
- サブコマンド未指定時の `CmocError` 生成、補完プローブ時の分岐、Click/Typer 例外の共通整形、`python src/main.py` 直実行の起動経路を扱います。

## Read this when

- cmoc CLI の起点として、`session` / `apply` / `review` のサブアプリ構成を確認したいとき。
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracles` の登録名や隠し別名を確認したいとき。
- `apply fork` の既定反復回数や `scope`、`apply join` の `--force-resolve` などの既定オプションを確認したいとき。
- サブコマンド未指定時の利用者向けエラー、補完プローブ時の分岐、Click/Typer 例外の共通整形、`python src/main.py` 直実行の経路を確認したいとき。

## Do not read this when

- `session`、`apply`、`review` など個別サブコマンドの本体実装だけを確認したいとき。
- `commons.errors` や `format_error_report()` の共通エラー整形だけを確認したいとき。
- `bin/cmoc` のシェル起動ラッパーだけを確認したいとき。

## hash

- a756de7b8e379a66e5e1bdfc4aa80c43d910a513c480de908c6d46a9f1196f81

# `sub_commands`

## Summary

- `src/sub_commands` は cmoc のサブコマンド実装の入口で、`__init__.py`、`indexing.py`、`init.py`、`apply/`、`review/`、`session/` へ案内する目次です。
- `indexing.py` は `INDEX.md` メンテナンス、`init.py` は初期化、`apply/` は apply 系、`review/` は review 系、`session/` は session 系の入口です。
- ここは個別実装に進む前に、どのサブコマンドやパッケージを読むべきかを切り分けるためのルーティング文書です。

## Read this when

- `src/sub_commands` 配下のサブコマンド実装全体の入口を把握したいとき。
- `cmoc indexing`、`cmoc init`、`cmoc apply`、`cmoc review`、`cmoc session` のどこへ進むべきか迷っているとき。
- 実装・修正・レビュー・テストの前に、対象モジュールを絞り込みたいとき。
- `src/sub_commands` が Python パッケージとしてどう構成されているか確認したいとき。

## Do not read this when

- 進むべき個別モジュールがすでに分かっていて、`indexing.py`、`init.py`、`apply/`、`review/`、`session/` に直接進めるとき。
- 個別サブコマンドの詳細な実行フローや状態遷移だけを確認したいとき。
- `oracles/docs/app_specs/sub_commands/` 側の正本仕様だけを確認したいとき。
- `src/sub_commands` の入口案内ではなく、実際の業務ロジックや CLI 入口を直接見たいとき。

## hash

- 91c3dcf79fc00938fabaf862c6cbce27756898330dd0ee9b528a58bc9b8805f1
