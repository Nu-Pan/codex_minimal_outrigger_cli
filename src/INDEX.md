# `commons`

## Summary

- `src/commons` は、cmoc 全体で共有する基盤処理をまとめたディレクトリの入口です。
- `codex.py`、`command_runner.py`、`errors.py`、`repo.py`、`subcommand_log.py`、`timestamps.py`、`timing.py`、`indexing.py` など、実行制御と周辺ユーティリティを扱います。
- `__init__.py` は package の宣言だけを持ち、実行ロジックは他のモジュールに分離されています。

## Read this when

- `cmoc` の共通処理を横断的に確認したいとき。
- `codex exec` の呼び出し、Structured Output、quota 待ち、`INDEX.md` 生成を扱う共通基盤を確認したいとき。
- リポジトリ探索、cmoc 管理ブランチ、session/apply state、作業用パスの復元など、git と `.cmoc` 周辺の共通処理を確認したいとき。
- サブコマンド共通のエラーレポート、ログ記録、経過時間計測、タイムスタンプ生成を確認したいとき。
- `src/commons` 配下のどのモジュールへ進むべきかを整理したいとき。

## Do not read this when

- `src/commons` 全体の案内ではなく、`codex.py` や `repo.py` など特定モジュールの実装だけを確認したいときは、該当ファイルを直接読むべきです。
- 個別サブコマンドの業務ロジックや CLI 引数の仕様だけを確認したいときは、この共通ユーティリティ群ではなく `src/sub_commands` を読むべきです。
- `INDEX.md` の生成・更新ルールそのものだけを確認したいときは、このディレクトリではなく `oracles/app_specs/indexing.md` を読むべきです。
- テストコードや実装コードの具体的な修正だけが必要なときは、まず該当するモジュールやテストを直接確認すべきです。

## hash

- 264eb5a543bdca67f551780529ef08f7e5200ca36e5916b14cfcfe125c2d540c

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
- 個別サブコマンドの細部ではなく、まず実装の着地点を切り分けるための目次です.

## Read this when

- `src/sub_commands` 配下で、どのモジュールがどのサブコマンドを担当するか整理したいとき。
- `cmoc init`、`cmoc eval-oracles`、`cmoc apply`、`cmoc session` の入口をまとめて把握したいとき。
- このディレクトリ内の `__init__.py`、`apply/`、`eval_oracles.py`、`init.py`、`session/` へのルーティング先を確認したいとき。
- 実装やレビューの前に、目的の処理がどのファイルにあるかを素早く切り分けたいとき。
- `src/sub_commands` を Python パッケージとしてどう構成しているかを見たいとき。

## Do not read this when

- `cmoc sub_commands` 配下の個別サブコマンドの実装詳細が必要なときは、ここではなく各モジュールの `INDEX.md` や `*.py` を直接読むべきです。
- `cmoc apply` や `cmoc session` のうち特定の手順だけを確認したいときは、このディレクトリ全体ではなく該当する子ディレクトリへ進むべきです。
- `cmoc init` や `cmoc eval-oracles` の処理順だけを確認したいときは、この案内ではなく対応する実装ファイルを読むべきです。
- パッケージとしての存在確認だけで足りるときは、`src/sub_commands/__init__.py` だけを見れば十分です。
- サブコマンドの正本仕様だけを確認したいときは、`oracles/app_specs/sub_commands/` 側の該当文書を読むべきです.

## hash

- 55e73a271bdf6736ceaf2665370dce0a534257f2829fecfcf9adb8e3b6757b78
