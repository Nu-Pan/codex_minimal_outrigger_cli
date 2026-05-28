# `commons`

## Summary

- cmoc 全体で使う共通処理をまとめたパッケージ入口で、`command_runner`、`codex`、`repo`、`errors`、`indexing`、`subcommand_log`、`timing`、`timestamps` を束ねます。
- Codex CLI 呼び出し、リポジトリ探索、session/apply ブランチ操作、共通エラー整形、`INDEX.md` メンテナンス、ログ記録、経過時間計測、タイムスタンプ生成を扱います。
- `__init__.py` はパッケージ宣言のみで、実装本体は各モジュールに分かれています。

## Read this when

- cmoc の共通ユーティリティの全体像を確認したいとき。
- `codex exec` 実行、`<repo-root>` 探索、session/apply 状態、共通ログ、タイミング計測のどのモジュールを読むべきか切り分けたいとき。
- サブコマンド実行制御やエラー表示の共通化を実装・修正・レビューしたいとき。
- `INDEX.md` の自動生成や、共通モジュール群の役割分担を把握したいとき。

## Do not read this when

- 個別サブコマンドの手順だけを確認したいときは `src/sub_commands` を読むべきです。
- 共通処理のうち特定 1 ファイルだけが必要なときは、この目次ではなく該当モジュールを直接読むべきです。
- `oracles` の正本仕様やユーザー向けコマンド説明だけを確認したいときは、このディレクトリは不要です。
- 実装コードやテストコードの詳細を追いたいときは、この目次ではなく該当ファイルを読むべきです。

## hash

- 6a58415383ef9a5d82c3bbbe9151e49e9263e6363e9ec7e0c34c65bbf10ac0a5

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

- `src/sub_commands` のパッケージ入口で、`__init__.py`、`apply/`、`eval_oracles.py`、`init.py`、`session/` への案内をまとめます。
- `cmoc init` と `cmoc eval-oracles` の単独モジュール、および `apply` と `session` のサブディレクトリ入口をここからたどれます。
- 個別サブコマンドの細部ではなく、まず実装の着地点を切り分けるための目次です。

## Read this when

- `src/sub_commands` 配下で、どのモジュールがどのサブコマンドを担当するか整理したいとき。
- `cmoc init`、`cmoc eval-oracles`、`cmoc apply`、`cmoc session` の入口をまとめて把握したいとき。
- このディレクトリ内の `__init__.py`、`apply/`、`eval_oracles.py`、`init.py`、`session/` へのルーティング先を確認したいとき。
- 実装やレビューの前に、目的の処理がどのファイルにあるかを素早く切り分けたいとき。
- `src/sub_commands` を Python パッケージとしてどう構成しているかを見たいとき。

## Do not read this when

- `cmoc apply` や `cmoc session` の個別手順だけを確認したいときは、この目次ではなく各サブディレクトリの `INDEX.md` を直接読むべきです。
- `cmoc init` や `cmoc eval-oracles` の処理順だけを確認したいときは、この目次ではなく対応する `*.py` を直接読むべきです。
- パッケージ宣言だけが目的であれば、`src/sub_commands/__init__.py` だけを見れば十分です。
- サブコマンドの正本仕様だけを確認したいときは、`oracles/app_specs/sub_commands/` 側の該当文書を読むべきです。

## hash

- 40e0e6c840435df0a1a74b69985d253441261a769c557648a778d2aedfe3a99f
