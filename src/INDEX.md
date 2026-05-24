# `commons`

## Summary

- `src/commons` は、cmoc 本体で使う共通基盤モジュールをまとめたルーティング用ディレクトリです。
- `command_runner.py` と `errors.py` は、Typer サブコマンドの共通実行制御と stdout 向けエラーレポート整形を扱います。
- `repo.py` は `<repo-root>` の探索、git 共通処理、`.cmoc` の追跡外保証、差分収集を提供します。
- `codex.py` と `indexing.py` は、`codex exec` 呼び出しの共通化と `<repo-root>` 配下の `INDEX.md` メンテナンスを扱います。
- `subcommand_log.py`、`timestamps.py`、`timing.py` は、サブコマンドログ、タイムスタンプ生成、経過時間表示の補助機能を提供します。
- `__init__.py` は `src.commons` パッケージを宣言するだけの最小モジュールです。

## Read this when

- `src/commons` のどのモジュールがどの役割を担うかを横断的に確認したいとき。
- `codex exec` 呼び出し、Structured Output、quota 待機、`--resume` 再開の共通処理を探したいとき。
- サブコマンドの実行制御、共通エラー処理、終了コード処理を確認したいとき。
- `<repo-root>` 探索、`git` ラッパー、`.cmoc` の追跡外保証、変更差分の扱いを確認したいとき。
- サブコマンドの tee ログ、タイムスタンプ、経過時間表示、`INDEX.md` の生成・更新ロジックを確認したいとき。

## Do not read this when

- `src/sub_commands` の個別 CLI ロジックだけを追いたいとき。
- `oracles` 側の正本仕様や個別サブコマンド仕様だけを読みたいとき。
- `tests` の期待値や pytest の補助だけを確認したいとき。
- `README.md`、`AGENTS.md`、`memo` の運用ルールだけを確認したいとき。
- すでに対象モジュールが決まっていて、ディレクトリ全体の案内が不要なとき。

## hash

- 7197348853d5b95f90a570f9f0bdeaabd82fe7b0d3ace3820e1950eae85d2a7d

# `main.py`

## Summary

- `src/main.py` は `cmoc` CLI の Typer エントリーポイントをまとめるルーティング用ファイルです。
- `init`、`branch`、`eval-oracles`、`apply`、`merge` の各サブコマンド登録と、対応する `src/sub_commands` 実装への委譲関係を案内します。
- Typer / Click の parse error、`NoArgsIsHelpError`、想定外例外を共通エラーレポートへ変換して終了コードを決める入口です。
- `python src/main.py` で直接起動される経路も含めて、CLI 起動全体の入口を整理します。

## Read this when

- `cmoc` のトップレベルコマンド一覧や、各サブコマンドの登録箇所を確認したいとき。
- 各コマンドがどの `src/sub_commands` の実装関数へ渡されるかを調べたいとき。
- `apply` の引数定義や既定値、`eval-oracles` の `--full` や互換 alias を含む CLI 挙動を確認したいとき。
- Typer / Click の parse error や想定外例外が、どのようにエラーレポートと終了コードへ変換されるか確認したいとき。
- `app` オブジェクトや `main()` の起動条件、`python src/main.py` での直接実行時挙動を調べたいとき。

## Do not read this when

- 各サブコマンドの業務ロジックや `src/sub_commands` 配下の本体実装を追いたいとき。
- 共通エラーレポートの本文生成や `commons.errors` の内部を詳しく確認したいとき。
- `src/commons` の共通基盤や `INDEX.md` 自動生成など、CLI 入口以外の横断仕様を調べたいとき。
- `cmoc` の利用手順全体や、`oracles` 側の正本仕様そのものを知りたいとき。

## hash

- 364d4061be59dadf7450ca3f98e034994463ff03257cae90b47575d6d9941568

# `sub_commands`

## Summary

- `src/sub_commands` は cmoc の各サブコマンド実装の入口を集めたディレクトリです。
- `init.py`, `branch.py`, `apply.py`, `eval-oracles.py`, `merge.py` が個別サブコマンドの本体処理を担います。
- `__init__.py` はサブコマンド実装パッケージの入口です。
- 各ファイルはサブコマンド固有の実行フロー、事前条件、エラー処理、`commons` との連携を確認するための起点になります。

## Read this when

- `cmoc init` の実行前提、`.cmoc` の ignore 保証、初期化コミットの挙動を確認したいとき。
- `cmoc branch` のブランチ作成、命名規則、base commit 記録を確認したいとき。
- `cmoc apply` の不整合調査・修正ループ、レポート出力、終了コードを確認したいとき。
- `cmoc eval-oracles` の oracle 評価モード、レポート生成、結果保存を確認したいとき。
- `cmoc merge` の merge 前提条件、conflict 解消支援、ブランチ削除条件を確認したいとき。
- 各サブコマンドの本体処理がどのファイルにあるかを特定したいとき。

## Do not read this when

- `commons` 配下の共通処理やユーティリティの仕様だけを調べたいとき。
- サブコマンド以外の CLI 入口やアプリ全体のルーティングだけを調べたいとき。
- テスト仕様や開発ルール、`oracles` の正本仕様だけを調べたいとき。
- `README.md`、`AGENTS.md`、`memo` などの運用ルールだけを確認したいとき。
- 特定のサブコマンド仕様がすでに確定していて、このディレクトリ全体の目次が不要なとき。

## hash

- 35fa03990808d8196570a80cc0cf4b80d62ca3fbf66a5bbf0babef791e2d7cbb
