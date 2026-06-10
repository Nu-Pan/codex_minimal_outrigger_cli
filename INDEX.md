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

- `<cmoc-root>/oracles` 配下全体のルーティング文書で、自然言語の仕様断片をまとめる `docs/` と、Structured Output の JSON schema をまとめる `schemas/` への入口です。
- `oracles` の中でどの系統の文書に進むべきかを判断するための最上位目次として使います。

## Read this when

- `oracles` 配下全体の役割分担と、`docs/` と `schemas/` のどちらへ進むべきかを整理したいとき。
- 自然言語の正本仕様断片と Structured Output の JSON schema を切り分けて確認したいとき。
- `oracles` の入口として、次に読むべき下位ディレクトリや個別文書を素早く決めたいとき。

## Do not read this when

- `docs/` や `schemas/` の配下で読むべき文書がすでに決まっていて、該当の `INDEX.md` や個別ファイルへ直接進めるとき。
- `oracles` 全体の入口ではなく、個別の仕様断片・JSON schema・開発ルールだけを確認したいとき。
- `README.md` や `AGENTS.md` など、`oracles` 以外のリポジトリ運用ルールだけを確認したいとき。

## hash

- a7eaf3b05105aa2814780238007facb84cadb886e81ede8ebb93259628276a35

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

- `src` ディレクトリのルーティング文書で、cmoc 本体の共通基盤、CLI 入口、各サブコマンド実装への入口をまとめる。
- `commons/`、`main.py`、`sub_commands/` に分岐して、次に読むべき下位モジュールを切り分けるための目次です。

## Read this when

- cmoc の本体ソース全体の入口構造を把握したいとき。
- 共通基盤 `src/commons`、CLI エントリーポイント `src/main.py`、サブコマンド実装 `src/sub_commands` の役割分担を確認したいとき。
- `src` 配下のどの下位ディレクトリやモジュールへ進むべきか迷ったとき。

## Do not read this when

- すでに読む先が `src/commons/`、`src/main.py`、`src/sub_commands/` のどれかに決まっていて、直接そのファイルや下位 `INDEX.md` へ進めるとき。
- `src` 全体ではなく、個別モジュールの実装やテストだけを確認したいとき。
- CLI の利用手順や正本仕様だけを追いたいとき。

## hash

- 9535a9286b44dd3310ca4cece53c7430826d12cc01da357f4e1ff75153a7ced3

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

- pytest 用の共通設定 `conftest.py` と、`commons.codex`、命名規則、インデックス保守、リポジトリ操作、レポート保存、タイムスタンプ処理を検証する回帰テスト群をまとめたディレクトリです。
- この階層には `test_codex.py`、`test_file_naming.py`、`test_indexing.py`、`test_repo.py`、`test_report_files.py`、`test_timestamps.py` が並びます。
- `test_subcommands/` は `cmoc` のサブコマンド横断テストの入口で、個別の apply / session / review / CLI / 共通基盤の回帰を収めます。
- この INDEX は、どのテストファイルがどの責務を持つかを素早く引ける目次です。

## Read this when

- pytest 実行時の共通設定や `src` の import path を確認したいとき。
- `commons.codex`、`indexing`、`repo`、`report_files`、`timestamps` のどの回帰テストを読むべきか切り分けたいとき。
- `cmoc` のサブコマンド回帰を探す前に、`tests/test_subcommands/` へ進むべきか判断したいとき。
- 個別テストファイルの責務を一覧で把握したいとき。

## Do not read this when

- すでに目的の個別テストファイルが分かっていて、この階層の目次を経由する必要がないとき。
- `src` 側の実装ロジックだけを追いたいとき。
- `test_subcommands/` 配下の個別テスト本体や、その下位の INDEX を直接読むとき。
- テスト以外のリポジトリ運用ルールや仕様断片だけを確認したいとき。

## hash

- 20fb57ab4d081947c91b080385d93e46b31d07ac9fae6dbe9fb4cd9ed43c7c6a
