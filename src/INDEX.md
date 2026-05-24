# `commons`

## Summary

- `src/commons` は、cmoc 全体で共有する基盤処理を束ねるルーティング用ディレクトリです。
- ここには `__init__.py`、`codex.py`、`command_runner.py`、`errors.py`、`indexing.py`、`repo.py`、`subcommand_log.py`、`timestamps.py`、`timing.py` が含まれます。
- codex exec 呼び出し、共通エラー、git リポジトリ操作、サブコマンドログ、タイムスタンプ、経過時間計測、`INDEX.md` 更新を扱います。
- サブコマンド本体から共通処理を切り離し、再利用可能な土台を提供します。

## Read this when

- cmoc の共通基盤処理を担当するモジュールの境界を確認したいとき。
- `codex exec` の呼び出し、Structured Output、quota 待機、last message 保存の共通処理を確認したいとき。
- サブコマンドの実行ラッパー、終了コード、共通エラー整形、ログ tee、経過時間表示を確認したいとき。
- repo root 探索、git 操作、`.cmoc` や `logs` の除外、タイムスタンプ生成、`INDEX.md` の列挙・再生成規則を確認したいとき。
- package-level の共通モジュール一覧を把握したいとき。

## Do not read this when

- 個別サブコマンドの入出力仕様や業務ロジックだけを調べたいとき。
- 開発ルール、テスト規約、環境構築など `src/commons` 以外の正本仕様だけを確認したいとき。
- ユーザー向け CLI の具体的な画面文言や、サブコマンドごとの処理フローだけを追いたいとき。
- 実装ファイルの詳細やテストコードの期待値を直接確認したいとき。

## hash

- f8c783a3d8fc52b097f5a549b70d165e497749080b63a3982e92e4d27ebaef06

# `main.py`

## Summary

- `cmoc` CLI の Typer エントリーポイントとサブコマンド登録をまとめる目次です。
- `init`、`branch`、`eval-oracles`、`apply`、`merge` の各コマンド定義と、対応する `src/sub_commands` 実装への委譲関係を案内します。
- Typer / Click の parse error、`NoArgsIsHelpError`、想定外例外を共通エラーレポートへ変換して終了コードを決める処理への入口です。
- `python src/main.py` で直接起動される経路も含めて、CLI 起動全体の入口を整理します。

## Read this when

- `cmoc` のトップレベルコマンド一覧や、各サブコマンドの登録箇所を確認したいとき。
- 各コマンドがどの `src/sub_commands` の実装関数へ渡されるかを調べたいとき。
- `apply` の `--repeat`、`--repeat-inveatigate-and-fix`、`--full` などの引数定義や既定値を確認したいとき。
- `eval-oracles` の `--full` や `eval-oracle` の互換 alias を含む CLI 挙動を確認したいとき。
- Typer / Click の parse error や想定外例外が、どのようにエラーレポートと終了コードへ変換されるか確認したいとき。
- `app` オブジェクトや `main()` の起動条件、`python src/main.py` での直接実行時挙動を調べたいとき。

## Do not read this when

- 各サブコマンドの業務ロジックや `src/sub_commands` 配下の本体実装を追いたいとき。
- 共通エラーレポートの本文生成や `commons.errors` の内部を詳しく確認したいとき。
- `src/commons` の共通基盤仕様や `INDEX.md` 自動生成など、CLI 入口以外の横断仕様を調べたいとき。
- `cmoc` の利用手順全体や、`oracles` 側の正本仕様そのものを知りたいとき。

## hash

- cb380259debbaae71cb88e4b9959201e67bf14dedef7073dec0c842bc4ad9a8b

# `sub_commands`

## Summary

- `src/sub_commands` は、cmoc の各サブコマンド本体を置く実装パッケージです。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` の実装入口と、その周辺の補助関数をまとめています。
- 各サブコマンドごとの処理フロー、引数の扱い、出力、共通処理との境界を案内する目次です。

## Read this when

- `src/sub_commands` がどの責務を担うか確認したいとき。
- 各サブコマンドの実装ファイルや補助関数の位置を知りたいとき。
- サブコマンドごとの処理順、前提条件、出力、エラー処理の概略を把握したいとき。
- 共通処理が `commons` 側なのか、サブコマンド側なのか切り分けたいとき。

## Do not read this when

- cmoc 全体の開発ルール、コーディング規約、テスト規約だけを調べたいとき。
- CLI のエントリーポイントやサブコマンド登録方法だけを確認したいとき。
- `src/commons` の共通基盤だけを調べたいとき。
- `oracles` 側の正本仕様そのものや、個別仕様断片だけを確認したいとき。
- `src/sub_commands` の実装ではなく、ユーザー向けの実行時仕様だけを知りたいとき。

## hash

- 70d4cfa828993a1a5d7fd7baa3c5a205e8c520efd297d583822b9f1bfeeccef8
