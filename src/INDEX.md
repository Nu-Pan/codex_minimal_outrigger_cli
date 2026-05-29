# `commons`

## Summary

- `src/commons` は、cmoc 全体で使う共通基盤モジュール群をまとめたディレクトリです。
- `codex.py` は Codex CLI 呼び出し、Structured Output の JSON 解析と検証、リトライ、ログ保存、`INDEX.md` 事前メンテナンスを担います。
- `command_runner.py` はサブコマンドの共通実行ラッパー、`errors.py` は共通例外と stdout 向けエラーレポート整形を担います。
- `indexing.py` は `INDEX.md` の自動生成・更新・自動コミットを扱い、`repo.py` は git リポジトリと `.cmoc` の状態管理を扱います。
- `subcommand_log.py` は JSON Lines ログ、`timestamps.py` は `<time-stamp>` 生成、`timing.py` はステップ経過時間計測を扱います。
- `__init__.py` は `src.commons` パッケージを宣言する最小モジュールです。

## Read this when

- 共通処理の役割分担をまとめて把握したいとき。
- repo root 探索、branch 判定、session/apply 状態管理などの git 共通処理を確認したいとき。
- Codex CLI 呼び出し、エラー整形、サブコマンドログ、タイムスタンプ、経過時間計測、`INDEX.md` メンテナンスの実装を追いたいとき。

## Do not read this when

- cmoc の個別サブコマンドの引数、状態遷移、実行手順だけを確認したいとき。
- `INDEX.md` の生成・維持ルールそのものを確認したいとき。
- `src/commons` の外にある CLI 本体やテストコードだけを確認したいとき。

## hash

- 5f832824aa560db29f71412404bd99a6e9066928d50b8b830f9ecca3d878584f

# `main.py`

## Summary

- cmoc CLI のエントリーポイントで、Typer のルート app と `session` / `apply` / `review` のサブアプリを組み立てます。
- `init`、`session fork/join/abandon`、`apply fork/join/abandon`、`review oracles` の登録と、それぞれのオプション既定値やエイリアスをまとめます。
- サブコマンド未指定時の利用者向けエラー、Click/Typer 例外の共通整形、`python src/main.py` 直実行の起動経路を扱います。

## Read this when

- cmoc の起動点やサブコマンド登録を修正・レビューしたいとき。
- `init` / `session` / `apply` / `review` のコマンド名、エイリアス、オプション既定値を確認したいとき。
- サブコマンドなし起動時の利用者向けエラー、終了コード、`--help` への誘導を確認したいとき。
- `python src/main.py` で直接起動する経路と、その例外ハンドリングを確認したいとき。

## Do not read this when

- 各サブコマンドの本体ロジックや `src/sub_commands/` 配下の処理だけを確認したいとき。
- 共通エラー型や `format_error_report` の整形仕様だけを確認したいとき。
- `INDEX.md` の生成ルールや共通ユーティリティの設計だけを追いたいとき。

## hash

- 725244cd04649c14efdc472340862818b2eabfb76416af919258408edf3121cc

# `sub_commands`

## Summary

- `src/sub_commands` は `cmoc` のサブコマンド実装の入口で、パッケージ宣言と個別コマンド実装へのルーティングをまとめるディレクトリです。
- `apply` と `session` はそれぞれ開始・統合・破棄のサブコマンド群をまとめたディレクトリで、詳細は下位の `INDEX.md` に分かれています。
- `eval_oracles.py` は `cmoc review oracles`、`init.py` は `cmoc init`、`__init__.py` はパッケージ宣言のみを担います。

## Read this when

- `src/sub_commands` 配下で、どのサブコマンド実装ファイルやサブディレクトリに進むべきか整理したいとき。
- `cmoc apply`、`cmoc session`、`cmoc review oracles`、`cmoc init` の入口をまとめて把握したいとき。
- サブコマンド群全体の役割分担と、個別実装の配置を確認したいとき。

## Do not read this when

- `cmoc apply fork/join/abandon` や `cmoc session fork/join/abandon` の詳細仕様だけを確認したいとき。
- `cmoc review oracles` の評価手順や `oracles` 側の仕様断片だけを確認したいとき。
- `src/sub_commands` のパッケージ宣言だけで足りるときは、`__init__.py` を直接見れば十分です。

## hash

- 5d311957c584ab26fccc4a11917fe1ad0d5ca5febd7e52924343d934a3903999
