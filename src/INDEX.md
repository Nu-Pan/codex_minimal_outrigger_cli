# `commons`

## Summary

- `cmoc` の共通ユーティリティをまとめた入口で、エラー処理、Codex CLI 呼び出し、リポジトリ探索、サブコマンド実行制御、ログ、計測、タイムスタンプ生成への案内を集約します。
- `indexing.py` は `INDEX.md` メンテナンスの中核で、各ディレクトリの目次生成と更新ルールを扱います。
- `codex.py` と `repo.py` と `command_runner.py` は、外部コマンド実行、作業リポジトリの特定、共通実行制御を支える中心モジュールです。
- `errors.py`、`subcommand_log.py`、`timing.py`、`timestamps.py` は、エラーレポート、ログ保存、経過時間表示、時刻文字列生成をそれぞれ担当します。

## Read this when

- `cmoc` 全体で使う共通処理の入口を確認したいとき。
- 共通エラー処理、`codex exec` 呼び出し、リポジトリ探索、サブコマンド実行制御、ログ、経過時間計測、タイムスタンプ生成のどこへ進むべきか整理したいとき。
- `src/commons` 配下の各モジュールが何を担当しているかを横断的に見直したいとき。
- `INDEX.md` の対象になる共通ユーティリティ群の役割分担を把握したいとき。

## Do not read this when

- `src/commons` 配下の個別モジュールの実装詳細だけを確認したいときは、該当する `*.py` を直接読むべきです。
- `cmoc` のユーザー向けサブコマンド仕様だけを確認したいときは、この共通モジュール群ではなく `oracles/app_specs` 側を読むべきです。
- `INDEX.md` の生成・更新ルールそのものだけを確認したいときは、`src/commons/indexing.py` を読むべきです。
- `src/commons` 以外の CLI 本体やテストだけを追いたいときは、このディレクトリの案内は不要です。

## hash

- c521b7966cc4004d43e592eade15e5e0f6c93e8bd913843100d1586debcde735

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

- `cmoc` の個別サブコマンド仕様への入口で、`apply`、`session`、`eval-oracles`、`init` それぞれの正本仕様へ案内するディレクトリです。
- `apply` と `session` は複数の詳細仕様に分かれているため、この目次から目的の文書へ素早く進めます。
- ここではサブコマンド全体の俯瞰と案内だけを扱い、実行手順そのものは各詳細仕様に委ねます。

## Read this when

- cmoc の個別サブコマンドの入口をまとめて確認したいとき。
- `apply`、`session`、`eval-oracles`、`init` のどの仕様断片を読むべきか整理したいとき。
- サブコマンドごとの目的、前提条件、状態遷移、終了条件を俯瞰したいとき。
- まず全体像を掴んでから、各詳細仕様へ進みたいとき。

## Do not read this when

- 個別サブコマンドの手順や前提条件だけを確認したいときは、該当する詳細仕様を直接読むべきです。
- 実装コードやテストコードだけで足りる作業では、この目次を読む必要はありません。
- `branch_model`、`codex_call`、ログ、エラーハンドリング、`oracles` 全体の扱いなど、他の共通仕様を確認したいときは別の入口文書を読むべきです。

## hash

- fd84b3deab9334a99976b308ca7323b44dd24f9584778c3179dcb57124c64990
