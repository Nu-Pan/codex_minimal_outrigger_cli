# `commons`

## Summary

- src/commons は、cmoc 本体で共通利用する基盤モジュールを集めたディレクトリです。
- `codex.py` は `codex exec` 呼び出し、Structured Output、JSON 検証、quota 待機、`--resume` 再開などの共通処理を担います。
- `command_runner.py` と `errors.py` は、Typer サブコマンドの実行制御、共通エラーレポート、終了コード処理をまとめます。
- `repo.py` は `<repo-root>` 探索、git 実行、`.cmoc` の追跡外保証、差分抽出などの git 共通処理を提供します。
- `indexing.py` は `<repo-root>` 配下の `INDEX.md` 列挙・再生成・更新・自動コミットを扱います。
- `subcommand_log.py`、`timestamps.py`、`timing.py` は、サブコマンドログ、タイムスタンプ生成、経過時間計測を補助します。
- `__init__.py` は `src.commons` パッケージを宣言する最小モジュールです。

## Read this when

- src/commons のどのモジュールがどの役割を担うかを横断的に確認したいとき。
- `codex exec` 呼び出しの共通化、Structured Output、JSON 再検証、quota 待機、`--resume` 再開を確認したいとき。
- サブコマンドの実行制御、共通エラー処理、終了コードの扱いを確認したいとき。
- `<repo-root>` 探索、git ラッパー、`.cmoc` の追跡外保証、変更差分の扱いを確認したいとき。
- `INDEX.md` の生成・再利用・更新ルールや、自動コミットの流れを確認したいとき。
- サブコマンドログ、タイムスタンプ、経過時間表示の補助機能を確認したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや CLI 引数定義だけを追いたいとき。
- `oracles` 側の正本仕様や個別サブコマンド仕様だけを読みたいとき。
- `tests` の期待値や pytest の補助だけを確認したいとき。
- `README.md`、`AGENTS.md`、`memo` の運用ルールだけを確認したいとき。
- すでに対象モジュールが決まっていて、ディレクトリ全体の案内が不要なとき。

## hash

- 7bea2f8e2e227b7322313040a95a655799c74d099c451a0b20d60a80dcef6cc7

# `main.py`

## Summary

- `src/main.py` は `cmoc` CLI の Typer エントリーポイントで、`init`、`session`、`apply`、`eval-oracles` を登録するルーティング用ファイルです。
- `eval-oracles` は `src/sub_commands/eval-oracles.py` を動的に読み込み、`eval-oracle` という hidden な互換 alias も提供します。
- `main()` は `standalone_mode=False` で Typer / Click の例外を受け取り、共通エラーレポートへ変換して終了コードを決めます。
- `NoArgsIsHelpError` を含め、CLI 起動全体の入口と例外整形の責務をまとめて確認するためのファイルです。

## Read this when

- `cmoc` のトップレベルコマンド登録と、各実装への委譲関係を確認したいとき。
- `eval-oracles` の動的読み込みや `apply` の引数定義など、CLI 入口の挙動を見たいとき。
- Typer / Click の parse error、`NoArgsIsHelpError`、想定外例外の扱いを確認したいとき。
- `python src/main.py` で直接起動した場合の入口処理を確認したいとき。

## Do not read this when

- `src/sub_commands` 配下の各サブコマンド本体の業務ロジックを確認したいとき。
- `commons.errors` の共通エラー整形や終了コード処理の内部だけを追いたいとき。
- `cmoc` の利用手順や `oracles` 側の正本仕様そのものを確認したいとき。
- `src/commons` の共通基盤モジュールを横断的に確認したいとき。

## hash

- 6c1afdc88839f2f29f9ba0fb784da27d6d11ae85ad171c10e1efbb4e02fa24f6

# `sub_commands`

## Summary

- `src/sub_commands` は `cmoc` のサブコマンド実装をまとめたディレクトリである。
- `__init__.py` は `src.sub_commands` パッケージの宣言だけを行う。
- `apply.py` は `cmoc apply` の本体処理を担う。
- `eval-oracles.py` は `cmoc eval-oracles` の本体処理を担う。
- `init.py` は `cmoc init` の本体処理を担う。
- `merge.py` は `cmoc merge` の本体処理を担う。
- `branch.py` は旧来の `cmoc branch` 相当の作業用ブランチ作成処理を担う。

## Read this when

- `src/sub_commands` 配下の入口と役割を確認したいとき
- `cmoc init`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge`、`cmoc branch` の実装位置を探したいとき
- サブコマンドごとのルーティング先を決めたいとき
- パッケージ境界として `src.sub_commands` がどう構成されているかを確認したいとき

## Do not read this when

- `cmoc` 全体の利用手順だけを確認したいとき
- `oracles` 配下の正本仕様だけを確認したいとき
- 共通の設計規約や開発ルールだけを確認したいとき
- `src/commons` など別ディレクトリの共通処理だけを追いたいとき

## hash

- b452342c06af5ea776f36a438ef6a7ee3fb868ab16faf5b8b1deb97972530383
