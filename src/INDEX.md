# `commons`

## Summary

- `src/commons` は、cmoc 本体で共有する共通処理をまとめたルーティング用ディレクトリです。
- `codex exec` 呼び出し、エラーハンドリング、リポジトリ探索、サブコマンド実行制御、ログ出力、経過時間計測、タイムスタンプ生成、`INDEX.md` 生成・更新を横断的に扱います。
- 個別サブコマンドの業務ロジックではなく、複数の処理から再利用される基盤モジュールへの入口を案内します。

## Read this when

- `src/commons` 配下のどのモジュールを読むべきか迷ったとき。
- `codex exec` の共通ラッパー、Structured Output 検証、リトライ、ログ保存を確認したいとき。
- Git リポジトリのルート探索、`.cmoc` の扱い、差分・commit・ブランチ関連の共通処理を確認したいとき。
- サブコマンド実行時の stdout / stderr の tee、経過時間表示、タイムスタンプ生成を確認したいとき。
- `INDEX.md` の自動生成・更新ロジックや、共通エラー表示の仕様を確認したいとき。

## Do not read this when

- 特定サブコマンドの引数定義や業務ロジックだけを追いたいとき。
- `cmoc` の開発ルールやテスト方針など、開発者向けの規約だけを確認したいとき。
- `README.md`、`AGENTS.md`、`oracles` の運用ルールだけを確認したいとき。
- `src/commons` 以外の実装配置や、個別機能の詳細実装だけを探したいとき。

## hash

- 14453abc6220af48f8a01cdb96a88505a655bf992fe7be2c1ce1d263312dd626

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
- `init`、`branch`、`apply`、`eval-oracles`、`merge` の処理本体と、その周辺の補助関数をまとめて案内します。
- 個別サブコマンドの処理順、前提条件、出力、共通処理との境界を確認するための入口です。

## Read this when

- `src/sub_commands` 配下が何を担当する実装層か確認したいとき。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` のどの実装ファイルを読むべきか判断したいとき。
- サブコマンドごとの処理フロー、引数の扱い、進捗表示、レポート出力、エラー処理の概略を把握したいとき。
- 各サブコマンドの実装が `commons` 側の共通処理とどう分かれているか確認したいとき。

## Do not read this when

- cmoc 全体の開発ルール、テスト規約、ディレクトリ構成の案内だけを調べたいとき。
- CLI のエントリーポイントやサブコマンド登録方法だけを確認したいとき。
- `commons` 配下の共通ユーティリティや基盤処理だけを調べたいとき。
- `oracles` 側の正本仕様そのものや、個別仕様断片だけを確認したいとき。
- `src/sub_commands` の各ファイルではなく、ユーザー向けの実行時仕様だけを知りたいとき。

## hash

- b5c06decb4feff1f2729505bbc16408b6c2f68942fa229187d1bf3a5d40f3aee
