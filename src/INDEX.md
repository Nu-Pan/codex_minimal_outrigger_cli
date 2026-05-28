# `commons`

## Summary

- `cmoc` 全体で使う共通処理をまとめたパッケージ入口で、`codex`、`command_runner`、`errors`、`indexing`、`repo`、`subcommand_log`、`timestamps`、`timing` を束ねます。
- `codex exec` の共通ラッパー、サブコマンド共通ランナー、共通エラー整形、`INDEX.md` メンテナンス、リポジトリ探索、ログ記録、タイムスタンプ生成、経過時間計測を扱います。
- `__init__.py` はパッケージ宣言のみで、実装本体は各モジュールに分かれています。

## Read this when

- `cmoc` 全体で使う共通処理の役割分担を整理したいとき。
- `codex exec` 呼び出し、`<repo-root>` 探索、共通エラー処理、`INDEX.md` 保守、ログ記録、経過時間計測、タイムスタンプ生成のどのモジュールを読むべきか切り分けたいとき。
- サブコマンド実行制御や共通ユーティリティの実装・修正・レビューの前に、`src/commons` 内の着地点を把握したいとき。
- `src/commons` が Python パッケージとしてどう構成されているか確認したいとき。

## Do not read this when

- `src/commons` 配下のうち特定 1 ファイルだけの実装を確認したいときは、この目次ではなく該当モジュールを直接読むべきです。
- `cmoc` の個別サブコマンドの業務ロジックだけを確認したいときは、このディレクトリではなく `src/sub_commands` 側を読むべきです。
- `oracles` の正本仕様やユーザー向けコマンド説明だけを確認したいときは、この目次は不要です。
- テストコードや CLI の引数定義だけを追いたいときは、この共通モジュール群の入口を読む必要はありません。

## hash

- 192339bf88c2f1b295aa4256d53847a3289dbddbbd7c89c2bcd10db5f2683269

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

- `src/sub_commands` は `cmoc` のサブコマンド実装を集約する入口ディレクトリです。
- `__init__.py` は `src.sub_commands` パッケージの宣言だけを担います。
- `apply/` は `cmoc apply` 系、`session/` は `cmoc session` 系の実装パッケージで、`eval_oracles.py` は `cmoc eval-oracles`、`init.py` は `cmoc init` の本体処理です。

## Read this when

- `src/sub_commands` 配下の CLI 実装の入口を確認し、どのファイルやパッケージへ進むべきか判断したいとき。
- `__init__.py`、`apply/`、`session/`、`eval_oracles.py`、`init.py` の役割分担を整理したいとき。
- `cmoc` のサブコマンド実装全体の配置を把握し、個別実装のルーティング先を決めたいとき。
- `apply` パッケージと `session` パッケージの配下にあるさらに細かい目次へ進む前に、入口だけ把握したいとき。

## Do not read this when

- `cmoc apply`、`cmoc session`、`cmoc eval-oracles`、`cmoc init` の個別仕様だけを確認したいときは、この入口ではなく該当するモジュールや正本仕様を直接読むべきです。
- `src/sub_commands` のうち特定 1 ファイルだけの詳細を見たいときは、この目次ではなく `__init__.py`、`apply/`、`session/`、`eval_oracles.py`、`init.py` の該当箇所を直接参照すべきです。
- `cmoc` の利用手順や正本仕様だけを確認したいときは、このディレクトリではなく `oracles/app_specs/sub_commands/` 側を読むべきです。
- 共通の branch model、ログ、エラーハンドリング、`INDEX.md` メンテナンス規則だけを確認したいときは、このディレクトリを読む必要はありません。

## hash

- 0c81701f7a243c774a7423d04fcc54a43678394f8cda96afa84bf1f4bb64901c
