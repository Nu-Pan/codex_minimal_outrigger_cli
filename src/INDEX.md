# `commons`

## Summary

- `<work-root>/src/commons` 配下の共通処理をまとめた目次です。
- `<work-root>/src/commons/__init__.py` は `src.commons` パッケージの宣言だけを担います。
- `<work-root>/src/commons/codex.py` は `codex exec` 呼び出しの共通基盤で、再試行、schema 検証、出力検査、`resume` 復旧、quota/capacity 対応、workspace-write 時の保護を扱います。
- `<work-root>/src/commons/command_runner.py` はサブコマンド実行の共通ラッパーで、repo root 解決、ログ開始、例外整形、完了集計を扱います。
- `<work-root>/src/commons/errors.py` は共通例外 `CmocError` とエラーレポート整形を扱います。
- `<work-root>/src/commons/indexing.py` は `INDEX.md` の生成・再生成・整合性検査を扱います。
- `<work-root>/src/commons/repo.py` は git リポジトリと cmoc 作業領域の共通基盤で、repo root 探索、状態管理、`.cmoc` 追跡外保証、ファイル列挙を扱います。
- `<work-root>/src/commons/report_files.py` はタイムスタンプ付き Markdown レポートの排他的作成を扱います。
- `<work-root>/src/commons/subcommand_log.py` はサブコマンド呼び出しごとの JSON Lines ログ作成と追記を扱います。
- `<work-root>/src/commons/timing.py` はステップ計測と完了サマリー、経過時間の整形を扱います。
- `<work-root>/src/commons/timestamps.py` は `<time-stamp>` 文字列の生成・判定とコンソール表示用日時文字列を扱います。

## Read this when

- `<work-root>/src/commons` 配下の共通基盤モジュールの入口をまとめて把握したいとき。
- `codex exec` 呼び出し、サブコマンド実行、repo/worktree 解決、エラー整形、`INDEX.md` メンテナンス、ログ、経過時間表示の責務分担を確認したいとき。
- 個別ファイルへ進む前に、`<work-root>/src/commons` のどのモジュールがどの役割を持つか整理したいとき。
- 共通処理の変更時に、影響を受ける入口ファイルを素早く見つけたいとき。

## Do not read this when

- `<work-root>/src/commons` 配下の対象モジュールがすでに分かっていて、`codex.py` や `repo.py` など個別ファイルへ直接進みたいとき。
- `codex exec` 呼び出し、repo/worktree 解決、エラー整形、ログ、時間表示など、特定の共通処理だけを確認したいとき。
- `<work-root>/src/sub_commands` や `tests` など、`<work-root>/src/commons` 以外の実装・回帰テストを探しているとき。
- `INDEX.md` の生成・再生成ルールや `oracles` 側の正本仕様だけを確認したいとき。

## hash

- 81ebe9996bbce9e8c88c4b6d3ed1217939ee1f8378e9fe4e7a3198b6a04339cd

# `main.py`

## Summary

- `<work-root>/src/main.py` は cmoc CLI のエントリーポイントで、Typer のルート `app` と `session` / `apply` / `review` の各サブアプリを組み立てる。
- `init` と `indexing`、`session` / `apply` / `review` の各サブコマンド登録、`eval-oracle` / `eval-oracles` の隠し別名、各コマンドの既定オプションをまとめる。
- サブコマンド未指定時の `CmocError` 生成、補完プローブ時の分岐、Click/Typer 例外の共通整形、`python <work-root>/src/main.py` 直実行の起動経路を扱う。

## Read this when

- cmoc CLI のルート構成と `session` / `apply` / `review` のサブアプリ構成を確認したいとき。
- `init`、`indexing`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracles` の登録名や既定引数を確認したいとき。
- サブコマンド未指定時のエラー処理、補完プローブ時の分岐、Click/Typer 例外の共通整形、`python <work-root>/src/main.py` 直実行の経路を確認したいとき。

## Do not read this when

- 個別サブコマンドの本体実装だけを確認したいとき。
- `commons.errors` や `commons.command_runner` など、共通基盤の詳細だけを追いたいとき。
- CLI 入口ではなく、`oracles` 側の正本仕様や利用手順だけを確認したいとき。

## hash

- a722fe60ee6c89051de98ebb10ad0b4119ba2b9c4a71282bf0a5918838002889

# `sub_commands`

## Summary

- `<work-root>/src/sub_commands` ディレクトリのルーティング文書で、`__init__.py`、`init.py`、`indexing.py`、`apply/`、`session/`、`review/` への入口です。
- この階層では、パッケージ宣言だけの最小モジュールと、`cmoc init` / `cmoc indexing` の本体、および各サブコマンドパッケージへの分岐を整理します。
- 個別実装に進む前に、どのモジュールがどの責務を持つかを切り分けるための目次です。

## Read this when

- `<work-root>/src/sub_commands` 配下の入口構造を把握し、どの実装ファイルや下位ディレクトリへ進むべきかを判断したいとき。
- `cmoc init` や `cmoc indexing` の本体実装を確認したいとき。
- `cmoc apply`、`cmoc session`、`cmoc review` の各パッケージへ分岐する前に、まずこの階層の役割を整理したいとき。

## Do not read this when

- すでに読む対象の `init.py`、`indexing.py`、`apply/`、`session/`、`review/` が分かっていて、直接その先へ進めるとき。
- `<work-root>/src/sub_commands` 全体ではなく、個別のサブコマンド実装やその下位ディレクトリの `INDEX.md` だけを確認したいとき。
- CLI 登録や起動経路ではなく、`oracles` 側の正本仕様断片だけを確認したいとき。

## hash

- 8d0656deb657a201935c7d650f8ae5d7a196af38ae51e848284c332090e651ef
