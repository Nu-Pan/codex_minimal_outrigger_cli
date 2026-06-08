# `AGENTS.md`

## Summary

- この `AGENTS.md` のルーティング文書で、リポジトリ全体の作業ルールと参照先の入口を案内します。
- 閲覧・編集の制約、`oracles` 配下の読み方、`src` と `tests` の配置前提を整理するための目次です。
- 作業開始前に、どの規約や仕様断片を読むべきかを切り分けるための入口です。

## Read this when

- このリポジトリで作業を始める前に、基本ルールと役割分担を確認したいとき。
- `cmoc` の開発と `cmoc` を用いた開発の違いを整理したいとき。
- `memo`、`README.md`、`AGENTS.md`、`oracles` の閲覧・編集制約を確認したいとき。
- `oracles` の正本仕様を読む前に、どの `INDEX.md` を起点にたどるか知りたいとき。
- 実装を `<cmoc-root>/src`、自動テストを `<cmoc-root>/tests` に置く前提を確認したいとき。

## Do not read this when

- 個別サブコマンドの引数や終了条件だけを確認したいとき。
- `oracles` 配下の特定仕様断片を直接確認したいとき。
- 実装コードやテストコードの内容だけを見たいとき。

## hash

- 01c836ca6fff27353230dbf64f045cc58b947af22edcf8bc22b5575f80a1e37e

# `LICENSE`

## Summary

- このリポジトリのライセンス本文です。
- 利用、改変、配布の許可条件と、保証および責任の免責を定めています。
- 法的条件の確認が必要なときに参照する入口です。

## Read this when

- このリポジトリに適用されるライセンス条件を確認したいとき。
- 再配布、改変、サブライセンス、免責の扱いを確認したいとき。
- ソフトウェアをコピー・利用・配布する前に、権利と制約を把握したいとき。

## Do not read this when

- このリポジトリの実装方針、CLI 仕様、テスト方針を確認したいとき。
- `cmoc` の使い方や `oracles` のルーティングを調べたいとき。
- ライセンス条文そのものではなく、ファイル構成や開発手順を確認したいとき。

## hash

- a894f2547af0349f234986eb4661f0146f37b7d82f8b22a27a674d5c1236f08f

# `README.md`

## Summary

- このリポジトリの概要、初期セットアップ、基本ワークフロー、作業時の補足事項をまとめた入口です。
- `cmoc` を使い始める前に、何を最初に行うかと、次にどこを読むかを確認するための案内です。

## Read this when

- このリポジトリ全体の概要を短く把握したいとき
- 初期セットアップとして clone、仮想環境作成、`cmoc` への PATH 設定を確認したいとき
- 基本ワークフローの入口として `oracles/docs/app_specs/usage.md` への導線を知りたいとき
- Ctrl+S によるターミナルロックなど、作業時の補足情報を確認したいとき

## Do not read this when

- cmoc の個別サブコマンドの引数や終了条件を確認したいとき
- `oracles` 配下の正本仕様を直接たどって、実装やテストの詳細を確認したいとき
- 実装ルールやテスト規約だけを確認したいとき

## hash

- 4fc977607c700055d3453298512ffdb3a3b257d876f1648f23a1b0dc79781ffc

# `bin`

## Summary

- `bin/` は `cmoc` コマンドのシェル製エントリーポイントを置く場所です。
- `bin/cmoc` は `<cmoc-root>/.venv/bin/python` を使って `src/main.py` を起動し、通常実行では全引数をそのまま渡します。
- 仮想環境 Python が利用できない場合は、日本語の構造化エラー、セットアップ手順、必要な実行ファイル、簡易 Call stack を標準エラーに出します。
- `_CMOC_COMPLETE` が設定された自動補完プローブ時も同じ Python 可否判定を行い、使える場合は `src/main.py` を起動します。

## Read this when

- `cmoc` がどの Python を使って起動するか確認したいとき。
- 自動補完プローブ `_CMOC_COMPLETE` の分岐を確認したいとき。
- 仮想環境 Python が見つからない、または実行できない場合のエラー文面、終了ステータス 1、復旧手順を確認したいとき。
- `src/main.py` へ引数をそのまま渡す流れを確認したいとき。
- エラー表示に出る簡易 Call stack の行番号の取り方を追いたいとき。

## Do not read this when

- `src/main.py` のサブコマンド登録や Python 側の実装だけを確認したいとき。
- 仮想環境の作成手順や導入手順だけを確認したいとき。
- `bin/cmoc` ではなく、他のディレクトリのルーティング文書を確認したいとき。

## hash

- 06c5f5f4145b6aa6d3f881761b05f09b4fdf00336454e1336db384b724d37e98

# `codex_minimal_outrigger_cli.code-workspace`

## Summary

- `codex_minimal_outrigger_cli.code-workspace` は、このリポジトリ全体を単一ワークスペースとして開くための VS Code ワークスペース設定です。
- `folders` ではルート `.` を指し、`settings.files.exclude` で `**/__pycache__` と `**/*.egg-info` を非表示にします。
- このファイルの目次は、エディタ起点でリポジトリを開くときの前提設定を素早く確認するための入口です。

## Read this when

- このリポジトリを VS Code などで 1 つのワークスペースとして開く設定を確認したいとき。
- ワークスペースのルートがどこか、どのファイルが表示除外されるかを把握したいとき。
- 開発用エディタ設定の入口を素早く確認したいとき。

## Do not read this when

- cmoc の実装コードやサブコマンド仕様そのものを確認したいとき。
- `src` や `tests` の個別モジュールの役割を調べたいとき。
- `oracles` 側の正本仕様や `INDEX.md` の生成ルールだけを確認したいとき。

## hash

- 6acff2a397cd0c66553c35c5c3f0f45a551ed34bcae704aa612b4b485cce20d0

# `oracles`

## Summary

- `oracles` ディレクトリ全体のルーティング文書で、`docs/` と `schemas/` への入口をまとめたものです。
- `docs/` は仕様断片の目次、`schemas/` は Structured Output schema の置き場です。
- まず目的に応じて仕様本文か schema 定義かを切り分けるための最上位目次です。

## Read this when

- `oracles` 配下で読むべき入口を探したいとき。
- cmoc の仕様本文をたどるために `docs/` 側へ進むか、Structured Output schema を確認するために `schemas/` 側へ進むか判断したいとき。
- `INDEX.md` の更新や配置ルールを確認する前段として、最上位の案内だけ見たいとき。

## Do not read this when

- 目的の文書がすでに分かっていて、`docs/` か `schemas/` の配下へ直接進めるとき。
- `docs/` 配下の個別仕様や `schemas/structured_output/review/oracles/` 配下の個別 schema を直接確認したいとき。
- `README.md`、`AGENTS.md` など、`oracles` 以外の運用ルールだけを確認したいとき。

## hash

- 776cffd8590d802a50e18c70107e21f51d2ad6b65c053cdd79532bbff598b68d

# `pyproject.toml`

## Summary

- このリポジトリの Python パッケージ定義とビルド設定をまとめたファイルです。
- プロジェクト名、バージョン、説明、必要な Python 版、依存関係、CLI エントリポイント `cmoc` が定義されています。
- `setuptools` を使った `src` レイアウトのパッケージ配置設定も含まれています。

## Read this when

- このプロジェクトの名前、バージョン、説明、対応 Python 版を確認したいとき。
- 依存パッケージや `cmoc` のコンソールスクリプト定義を確認したいとき。
- ビルド方式や `setuptools` のパッケージ探索設定を確認したいとき。

## Do not read this when

- CLI の個別サブコマンドの実装や引数仕様だけを確認したいとき。
- テストコードや期待挙動を確認したいとき。
- `src` 配下の内部ロジックや共通処理だけを追いたいとき。

## hash

- bc854625f7c4de175d9450ec605a6b8bfdc6254b85c01a8ea41684dd1b943ff8

# `src`

## Summary

- この `src` ディレクトリのルーティング文書で、`main.py`、`commons/`、`sub_commands/` へ案内する入口です。
- `main.py` は CLI エントリーポイント、`commons/` は共通基盤、`sub_commands/` は各サブコマンド実装の入口です。
- 個別モジュールへ進む前に、cmoc の実装全体の役割分担を切り分けるための目次です。

## Read this when

- cmoc のソースコード全体で、どの入口ファイルや共通基盤から読むべきか整理したいとき。
- `src/main.py`、`src/commons/`、`src/sub_commands/` のどこへ進むか迷っているとき。
- CLI の起点、共通処理、サブコマンド実装の役割分担を先に把握したいとき。
- 個別実装を読む前に、`src` 配下の構造を一度俯瞰したいとき。

## Do not read this when

- 読む対象がすでに `main.py` や `commons/`、`sub_commands/` の個別モジュールに決まっているとき。
- `src` 全体の目次ではなく、特定ファイルの実装詳細だけを確認したいとき。
- `oracles` 側の正本仕様や利用手順だけを確認したいとき。
- CLI の入口ではなく、共通ユーティリティや個別サブコマンドだけを直接追いたいとき。

## hash

- 41212b57a913164e8e43e7550c881a46b22c5a09ab37537555e66878a7222ad5

# `test.sh`

## Summary

- `test.sh` は `<cmoc-root>` を `CMOC_ROOT` として固定し、`.venv/bin` と `bin` を `PATH` の先頭側に通すための環境初期化スニペットです。
- cmoc コマンドや関連ツールを、このリポジトリのローカル環境で実行できる状態にすることが目的です。

## Read this when

- `CMOC_ROOT` を固定し、`PATH` に `.venv/bin` と `bin` を追加する環境設定を確認したいとき。
- cmoc 関連コマンドをこのワークツリーで実行する前の最小セットアップ手順を知りたいとき。
- シェルから cmoc を使うための前提環境を素早く把握したいとき。

## Do not read this when

- cmoc の実装本体やサブコマンド仕様を確認したいとき。
- pytest や個別テストケースの内容を確認したいとき。
- `oracles` の正本仕様や `INDEX.md` 生成ルールだけを確認したいとき。

## hash

- 9d5f6059b4a5acd4ec851223fc85c0acc2d9ae1ea244ff40ee48993217f1d9fc

# `tests`

## Summary

- この `tests` ディレクトリのルーティング文書で、pytest 共通設定と各回帰テスト群への入口をまとめます。
- `conftest.py`、`test_codex.py`、`test_file_naming.py`、`test_indexing.py`、`test_repo.py`、`test_report_files.py`、`test_timestamps.py` を案内し、`test_subcommands/` へも分岐します。
- 上位の観点からは、CLI 呼び出し、INDEX メンテナンス、git 共通処理、レポート保存、タイムスタンプ、命名規則の確認先を切り分けるための目次です。

## Read this when

- pytest の共通設定や、`tests` 直下のどの回帰テストへ進むべきかを整理したいとき。
- Codex 呼び出し、INDEX メンテナンス、git 共通処理、レポート保存、タイムスタンプ、命名規則のどれを確認するか切り分けたいとき。
- `tests/test_subcommands/` 配下の CLI 横断テストへ進む前に、入口だけ把握したいとき。

## Do not read this when

- 個別テストケースのアサーションや補助関数の詳細を確認したいとき。
- `src/commons/` や `src/sub_commands/` の実装本体を直接追いたいとき。
- すでに目的のテストファイルが分かっていて、`tests/INDEX.md` ではなく該当ファイルへ直接進むとき。

## hash

- d6f28f8724269928c4eb497913406686adfe8495bf073f6f6e8ac3b24e03e53d
