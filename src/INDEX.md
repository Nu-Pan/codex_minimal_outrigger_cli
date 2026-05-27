# `commons`

## Summary

- `src/commons` 配下の共有モジュールをまとめた入口で、`codex`、`command_runner`、`errors`、`indexing`、`repo`、`subcommand_log`、`timestamps`、`timing` への案内を提供します。
- 各サブコマンドで共通利用される実行制御、エラー整形、リポジトリ探索、ログ保存、タイムスタンプ生成、時間計測の担当範囲を整理するための目次です。
- 個別実装へ進む前に、どの共通機能がどのファイルにあるかを素早く判断するためのルーティング文書です。

## Read this when

- `src/commons` に置かれた共通ユーティリティの全体像を確認したいとき。
- 共有エラー処理、リポジトリ探索、ログ出力、タイムスタンプ生成、経過時間計測のどこへ進むべきか整理したいとき。
- 各サブコマンドで共通利用される機能の入口をまとめて把握したいとき。
- 個別モジュールへ入る前に、役割分担を先に確認したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックだけを確認したいときは、`src/sub_commands` 側を直接読むべきです。
- `codex exec` や `apply` など、`src/commons` 以外の機能の仕様だけを確認したいときは、この目次を読む必要はありません。
- 特定の共有モジュールの実装詳細を知りたいときは、`codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`subcommand_log.py`、`timestamps.py`、`timing.py` を直接参照すべきです。
- `INDEX.md` の生成・更新ルールそのものだけを確認したいときは、`src/commons/indexing.py` を読むべきです。

## hash

- f7a863e1187f10533477dde8e8d6a062eb83d7d5168dc5a2e184cbf7ef06dc26

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

- `src.sub_commands` パッケージの入口で、`__init__.py`、`apply/`、`session/`、`eval_oracles.py`、`init.py` への案内をまとめます。
- `apply/` と `session/` はそれぞれサブコマンド群の実装ディレクトリで、個別処理の入口をさらに分けています。
- `eval_oracles.py` と `init.py` はディレクトリ直下の個別サブコマンド本体です。

## Read this when

- `src.sub_commands` の全体像を把握したいとき。
- `apply`、`session`、`eval-oracles`、`init` のどの実装へ進むべきかを切り分けたいとき。
- `src.sub_commands` が Python パッケージとして宣言されていることや、配下の実装ファイル一覧を確認したいとき。

## Do not read this when

- 個別サブコマンドの実行手順や状態遷移だけを確認したいときは、該当する `apply/`、`session/`、`eval_oracles.py`、`init.py` を直接読むべきです。
- サブコマンド仕様の正本断片だけを確認したいときは、`oracles/app_specs/sub_commands/` 側を読むべきです。
- CLI 全体の共通規約や開発ルールだけを確認したいときは、このディレクトリの目次は不要です。

## hash

- 896d77e4f4443097c89d36e185ab69125c0f3bddf81b60c8561b2c4b0bed1b47
