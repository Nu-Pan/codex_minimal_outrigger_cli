# `commons`

## Summary

- `src/commons` は、cmoc 全体で共有する基盤処理をまとめるディレクトリです。
- `codex.py` は `codex exec` の共通ラッパー、`command_runner.py` はサブコマンドの共通実行制御、`errors.py` は共通例外とエラーレポートを扱います。
- `repo.py` は `<repo-root>` 探索と git 操作、`indexing.py` は `<repo-root>` 配下の `INDEX.md` 保守、`subcommand_log.py` は tee ログを担当します。
- `timestamps.py` は `<time-stamp>` 生成、`timing.py` はステップ別経過時間表示を担当します。
- `__init__.py` は `src.commons` パッケージの入口だけを定義します。

## Read this when

- 共通処理のうち、どのモジュールを読むべきか切り分けたいとき。
- `codex exec` の共通引数、Structured Output、JSON 検証、リトライ、ログ保存を確認したいとき。
- 共通エラーハンドリング、`<repo-root>` 探索、git 操作、`INDEX.md` 保守、サブコマンドログ、タイムスタンプ、経過時間表示を確認したいとき。
- CLI サブコマンドの共通実行制御や終了コードの扱いを確認したいとき。
- `src/commons` 全体の役割をパッケージ境界として把握したいとき。

## Do not read this when

- 個別サブコマンドの業務ロジックや CLI 引数定義だけを追いたいとき。
- `src/commons` の中でも特定モジュールの実装詳細だけを見たいときで、ディレクトリ全体の案内が不要なとき。
- `src` 全体の設計規約やテスト規約、`oracles` の正本仕様だけを調べたいとき。
- `README.md`、`AGENTS.md`、`memo` などの運用ルールだけを確認したいとき。

## hash

- d0d623ae83f44c8819e7ec6392c664646773f99c6ba8678c7df980475496e706

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

- このディレクトリは cmoc のサブコマンド実装をまとめたルーティング用目次です。
- `__init__.py` はパッケージ境界の説明だけを持つ最小ファイルです。
- `init.py` は `cmoc init` の初期化処理と `.cmoc` の追跡対象外保証を扱います。
- `branch.py` は `cmoc branch` の作業ブランチ作成、命名、記録を扱います。
- `apply.py` は `cmoc apply` の調査・修正ループ、改善、適用、レポートを扱います。
- `eval_oracles.py` は `cmoc eval-oracles` の oracle 評価、集約、Markdown レポート生成を扱います。
- `merge.py` は `cmoc merge` のマージ、自動解決、コンフリクト処理、ブランチ削除判定を扱います。

## Read this when

- src/sub_commands 配下のどのファイルに各サブコマンド実装があるかを素早く把握したいとき。
- 各サブコマンドの本体実装の入口を探したいとき。
- サブコマンドごとの責務境界や、どの処理をどのモジュールが持つかを確認したいとき。
- サブコマンド実装の追加・修正・テストで、まず読むべきファイルを選びたいとき。

## Do not read this when

- cmoc の実行時仕様そのものや、`oracles` の正本仕様を調べたいとき。
- 開発ルール、テスト規約、設計規約などの開発者向けルールだけを確認したいとき。
- CLI の引数定義やエントリーポイント登録だけを確認したいとき。
- `README.md`、`AGENTS.md`、`oracles`、`memo` の運用ルールだけを確認したいとき。
- 個別サブコマンドの詳細仕様が既に明確で、この目次全体が不要なとき。

## hash

- c977cb8ba00dceb3735d4b047ce5c7e23ea5456275d632c77924c3ec6250dc93
