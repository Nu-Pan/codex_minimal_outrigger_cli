# `commons`

## Summary

- `src/commons` は、`__init__.py` を含む cmoc 全体で共有する基盤モジュール群をまとめたディレクトリです。
- `codex exec` 呼び出しの共通ラッパー、Structured Output の検証、リトライ、quota 待機などの実行制御を扱います。
- git リポジトリ root の探索、`.cmoc` の追跡外保証、変更ファイル列挙、部分評価・部分適用向けの path 判定を扱います。
- 共通エラー整形、サブコマンド実行の共通制御、tee ログ、経過時間計測、タイムスタンプ生成をまとめています。
- 複数のサブコマンドから再利用される横断処理の置き場であり、個別サブコマンド本体そのものは置きません。

## Read this when

- `src/main.py` や `src/sub_commands/*.py` から呼ぶ共通処理の役割を確認したいとき。
- repo root 検出、`git` 操作、`.cmoc` の追跡外保証、差分収集の仕様を確認したいとき。
- `codex exec` の共通ラッパー、JSON schema 検証、`INDEX.md` 生成、ログ、タイミングの共通仕様を確認したいとき。
- 共通例外、終了コード、サブコマンド実行の報告形式を確認したいとき。
- 共有ユーティリティを追加・修正する前に、既存の責務分担を確認したいとき。

## Do not read this when

- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` のユーザー向け手順や入出力仕様だけを知りたいとき。
- `src/sub_commands` の個別業務ロジックだけを探したいとき。
- 開発ルール、テスト方針、環境設定だけを確認したいとき。
- `oracles` の正本仕様や `INDEX.md` メンテナンス全体のルールだけを見たいとき。
- `README.md`、`AGENTS.md`、`memo` の運用規則だけを確認したいとき。

## hash

- c1ad5023553202bf03537bd020a611961d27bd03b1f400c24e8c20f063e8229a

# `main.py`

## Summary

- `cmoc` CLI の Typer エントリーポイントを定義するファイルです。
- `init`、`branch`、`eval-oracles`、`apply`、`merge` を `app` に登録し、それぞれ対応する `src/sub_commands` 実装へ処理を委譲します。
- `main()` で Typer / Click の起動を包み、parse error や想定外例外を共通エラーレポート形式に整えて終了コードを決めます。
- `python src/main.py` で直接実行された場合の起動経路も、このファイルでまとめています。

## Read this when

- `cmoc` のトップレベルコマンド一覧と、各サブコマンドの登録箇所を確認したいとき。
- 各コマンドがどの `src/sub_commands` 実装関数へ渡されるかを調べたいとき。
- `apply` の `--repeat` や `--full`、`eval-oracles` の `--full` などの Typer 引数定義や既定値を確認したいとき。
- Typer / Click の parse error、`NoArgsIsHelpError`、想定外例外がどのように終了コード付きのエラーレポートへ変換されるか確認したいとき。
- `app` オブジェクトや `main()` の起動条件、`python src/main.py` での直接実行時挙動を調べたいとき。

## Do not read this when

- 各サブコマンドの業務ロジックや `src/sub_commands` 配下の本体実装を追いたいとき。
- 共通エラーレポートの本文生成や `commons.errors` の内部を詳しく確認したいとき。
- `INDEX.md` 自動生成、repo 探索、ログ保存などの共通基盤の仕様を調べたいとき。
- `cmoc` の利用手順全体や各サブコマンドの正本仕様を知りたいとき。

## hash

- d8532edf006b5e6a2d51210f24708a8edb537cc004a848ebe834777bdb456caa

# `sub_commands`

## Summary

- `src/sub_commands` は cmoc の各サブコマンド実装モジュールをまとめるルーティング用ディレクトリの目次です。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` の各本体実装への入口を案内します。
- `__init__.py` はサブコマンド実装パッケージであることを示す最小限の初期化ファイルです。
- 各モジュールは、それぞれのサブコマンドの処理順、事前条件、出力、終了条件、共通処理との接続点を担います。
- この目次は、個別実装を読む前に「どのファイルを参照すべきか」を切り分けるための案内です。

## Read this when

- `src/sub_commands` 配下のどのファイルがどのサブコマンドに対応するかを確認したいとき。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` の個別実装へ進む入口が必要なとき。
- サブコマンド実装パッケージ全体の境界や、各モジュールの役割分担を把握したいとき。
- 特定のサブコマンドの処理本体ではなく、まず参照先のファイルを絞り込みたいとき。

## Do not read this when

- 個別サブコマンドの引数、実行フロー、エラー処理などの詳細仕様だけを調べたいとき。
- `cmoc` 自体の開発ルール、設計規約、テスト規約、開発環境を調べたいとき。
- コマンド全体の共通仕様や `INDEX.md` 自動生成ルールだけを確認したいとき。
- `README.md`、`AGENTS.md`、`oracles`、`memo` の運用ルールだけを確認したいとき。

## hash

- 9ddaec08786aab24d4839d678ebf4e76e9bbc8c48fa4ada4d84aa72f82efc67c
