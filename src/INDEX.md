# `commons`

## Summary

- `cmoc` の共通基盤モジュールをまとめたディレクトリで、Codex 呼び出し、コマンド実行制御、エラー整形、`INDEX.md` メンテナンス、git/セッション状態、ログ、時刻、経過時間計測を担当します。
- `codex.py` は Codex CLI の起動、Structured Output 検証、quota 待機、出力パースを扱います。
- `repo.py` は git リポジトリ探索、`cmoc/session/*` と `cmoc/apply/*` の判定、`session state` の読み書きを扱います。
- `command_runner.py`、`subcommand_log.py`、`errors.py` はサブコマンド実行の共通制御、tee ログ、共通エラーレポートを支えます。
- `indexing.py` は `INDEX.md` の自動配置・更新と、目次情報の生成・検証を担当します。
- `timestamps.py` と `timing.py` は `cmoc` で使うタイムスタンプ生成と経過時間表示を定義します。

## Read this when

- サブコマンドから共通の `codex exec` 呼び出しや Structured Output を実装・修正したいとき。
- リポジトリルート探索、`cmoc/session/*` と `cmoc/apply/*`、`session state` の扱いを確認したいとき。
- サブコマンドの共通ラッパー、終了レポート、tee ログ、エラー表示を確認したいとき。
- `INDEX.md` の自動更新ルール、ハッシュ計算、除外条件を確認したいとき。
- 時刻文字列や経過時間表示の仕様を確認したいとき。

## Do not read this when

- 個別サブコマンドの引数や業務フローだけを確認したいときは、`src/sub_commands` 側を読むべきです。
- `oracles` や `dev_rules` の仕様本文だけを確認したいときは、このディレクトリを読む必要はありません。
- git や Codex 呼び出しの共通処理が関係しない小さな実装変更では、ここから入る必要はありません。
- 特定モジュールの単独挙動だけを追いたいときは、`codex.py` など該当ファイルを直接読むべきです。

## hash

- 6cf7b311807b19187b3de349bb6500442aeb1e70030f2d96831fe81ab4926d10

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

- `src/sub_commands` は `cmoc` のサブコマンド実装群の入口です。
- `__init__.py` はパッケージ宣言のみを担い、`apply` と `session` はそれぞれ専用のサブディレクトリに分かれています。
- `eval_oracles.py` は `cmoc eval-oracles` の本体、`init.py` は `cmoc init` の本体です。
- この目次から、`apply/INDEX.md` と `session/INDEX.md` へ進んで、それぞれの詳細実装へたどれます。

## Read this when

- `src/sub_commands` 配下のサブコマンド実装全体を、どのファイルに何があるかという観点で把握したいとき。
- `apply`、`session`、`eval-oracles`、`init` の実装入口をまとめて整理したいとき。
- 各サブコマンドの個別モジュールへ進む前に、役割分担と配置方針を確認したいとき。
- `src/sub_commands` 以下の入口案内として、どの INDEX や実装ファイルへ進むべきかを判断したいとき。

## Do not read this when

- 個別の `cmoc apply` 実装だけを確認したいときは、この目次ではなく `apply/INDEX.md` を直接読むべきです。
- 個別の `cmoc session` 実装だけを確認したいときは、この目次ではなく `session/INDEX.md` を直接読むべきです。
- `cmoc eval-oracles` や `cmoc init` の処理内容だけを確認したいときは、この目次ではなく `eval_oracles.py` や `init.py` を直接読むべきです。
- `src/sub_commands` が Python パッケージとして宣言されているかだけを確認したいときは、`__init__.py` だけで足ります。

## hash

- 9a0d7d5af087c5fc768acb3eb8b4da92f8ed61023ed700b0b122876c877e170c
