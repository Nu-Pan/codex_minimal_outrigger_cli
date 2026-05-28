# `commons`

## Summary

- `src/commons` は、cmoc 全体で再利用する共通処理をまとめたディレクトリです。Codex CLI 呼び出し、サブコマンド実行制御、エラー整形、リポジトリ操作、ログ、時間計測、タイムスタンプ、`INDEX.md` 生成をここに集約します。
- 各モジュールは個別の責務を持ちつつ、サブコマンド実装から呼び出される共通基盤として機能します。`__init__.py` はパッケージ定義のみを担います。

## Read this when

- 複数のサブコマンドから共通で使う処理を探したいときに読むべきです。
- Codex CLI 呼び出し、Structured Output、`INDEX.md` 生成・維持、gitignore 判定の流れを確認したいときに読むべきです。
- `<repo-root>` の探索、branch 判定、session state、apply worktree、process id などの git 連携と状態管理を見直したいときに読むべきです。
- 共通エラー整形、サブコマンドログ、経過時間計測、タイムスタンプ生成の実装を横断的に把握したいときに読むべきです。

## Do not read this when

- 個別サブコマンドの業務ロジックや引数定義だけを確認したいときは、`src/sub_commands` を先に読むべきです。
- CLI のエントリーポイントや全体の起動順だけを見たいときは、`src/main.py` 側を確認すべきです。
- 共有処理のうち特定機能だけを追いたいときは、このディレクトリ全体ではなく該当する `codex.py`、`repo.py`、`errors.py`、`subcommand_log.py`、`timing.py`、`timestamps.py`、`indexing.py` を直接読むべきです。
- 自動テストや検証手順だけが目的なら、この共通モジュール群ではなく `tests` を読むべきです。

## hash

- c9e70229953c4187622c53d3cf44b75e60a22082557ed220bd586724eb92852b

# `main.py`

## Summary

- `cmoc` CLI のエントリーポイントで、Typer アプリ本体と `session` / `apply` のサブアプリを組み立てています。
- `init`、`session`、`apply`、`eval-oracles` の各コマンドを定義し、実処理は `src/sub_commands/` 側の実装へ委譲しています。
- Typer / Click の例外処理をまとめて受け、`NoArgsIsHelpError` を含むエラーを `format_error_report()` で整形して終了コード付きで終了します。

## Read this when

- `cmoc` のエントリーポイント、Typer アプリの構成、サブコマンド登録を修正・レビューしたいとき。
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`eval-oracles` とその引数定義を確認したいとき。
- サブコマンドなし起動時の `NoArgsIsHelpError` の扱い、`--help` 相当の挙動、終了コードの伝播を確認したいとき。
- Typer / Click の例外を `CmocError` と共通エラーレポートへ変換する起動経路を確認したいとき。
- `python src/main.py` で直接起動する経路の振る舞いを確認したいとき。

## Do not read this when

- 各サブコマンド本体の処理内容だけを確認したいときは、このファイルではなく `src/sub_commands/` 配下の実装を見るべきです。
- 共通エラー型やエラーレポートの整形だけを確認したいときは、このファイルではなく `src/commons/errors.py` を見るべきです。
- CLI の設計ルールや配置方針だけを確認したいときは、このファイルではなく `oracles/dev_rules/design_rules.md` を見るべきです。
- サブコマンドごとの仕様断片だけを確認したいときは、このファイルではなく `oracles/app_specs/sub_commands/` 配下の文書を見るべきです。

## hash

- fd4b3fe58ddc1bb32e637e83cc5ddca509458ade3b15a69c1c5d5bc677ba138b

# `sub_commands`

## Summary

- `src/sub_commands` は cmoc のサブコマンド実装の入口で、`apply` と `session` の各パッケージ、`init.py`、`eval_oracles.py`、`__init__.py` への案内をまとめる。
- `apply` と `session` はそれぞれ独立したサブコマンド群として、配下の `INDEX.md` から個別実装へたどれる。
- `init.py` と `eval_oracles.py` は単体モジュールとして、初期化処理と oracle 評価処理の入口を担う。

## Read this when

- `cmoc` のサブコマンド実装全体の入口を確認したいとき。
- `apply` や `session` のような複数ファイルの実装群と、`init.py` / `eval_oracles.py` の単体モジュールを見分けたいとき。
- どのサブコマンド実装へ進むべきか、このディレクトリの目次から判断したいとき。
- `src/sub_commands` 配下の個別 `INDEX.md` や実装ファイルの入口を探したいとき。

## Do not read this when

- 個別サブコマンドの実装や手順だけを確認したいときは、対応する配下の `INDEX.md` や実装ファイルを直接読むべきです。
- `cmoc` の共通処理や `commons` 側の仕様だけを確認したいときは、このディレクトリではなく該当する案内を読むべきです。
- サブコマンドの利用手順そのものではなく、実装やテストの詳細を追いたいときは、より下位の文書を読むべきです。
- このディレクトリの役割確認だけで足りるときに、個別モジュールまで読み進める必要はありません。

## hash

- 1bff4db46839c7837f563219170fac803f6a78105e1aa58e283e7367c13a34f0
