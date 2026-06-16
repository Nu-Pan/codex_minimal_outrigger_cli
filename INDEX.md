# `AGENTS.md`

## Summary

- この `AGENTS.md` のルーティング文書で、リポジトリ全体の作業ルールと参照先の入口を案内します。
- 閲覧・編集の制約、`oracle` 配下の読み方、`src` と `tests` の配置前提を整理するための目次です。
- 作業開始前に、どの規約や仕様断片を読むべきかを切り分けるための入口です。

## Read this when

- このリポジトリで作業を始める前に、基本ルールと役割分担を確認したいとき。
- `cmoc` の開発と `cmoc` を用いた開発の違いを整理したいとき。
- `memo`、`README.md`、`AGENTS.md`、`oracle` の閲覧・編集制約を確認したいとき。
- `oracle` の正本仕様を読む前に、どの `INDEX.md` を起点にたどるか知りたいとき。
- 実装を `<cmoc-root>/src`、自動テストを `<cmoc-root>/tests` に置く前提を確認したいとき。

## Do not read this when

- 個別サブコマンドの引数や終了条件だけを確認したいとき。
- `oracle` 配下の特定仕様断片を直接確認したいとき。
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
- `cmoc` の使い方や `oracle` のルーティングを調べたいとき。
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
- 基本ワークフローの入口として `<work-root>/oracle/docs/app_specs/usage.md` への導線を知りたいとき
- Ctrl+S によるターミナルロックなど、作業時の補足情報を確認したいとき

## Do not read this when

- cmoc の個別サブコマンドの引数や終了条件を確認したいとき
- `oracle` 配下の正本仕様を直接たどって、実装やテストの詳細を確認したいとき
- 実装ルールやテスト規約だけを確認したいとき

## hash

- 4fc977607c700055d3453298512ffdb3a3b257d876f1648f23a1b0dc79781ffc

# `bin`

## Summary

- この `bin` ディレクトリのルーティング文書で、`cmoc` コマンドの入口です。
- `<work-root>/bin/cmoc` の役割、Python 実行ファイルの選択、補完プローブ時の分岐、エラー時の案内へ進むための目次です。

## Read this when

- `<work-root>/bin` 配下の入口文書として、どのファイルへ進むべきか確認したいとき。
- `cmoc` のシェル製エントリーポイントの役割や、起動時の分岐を把握したいとき。
- 仮想環境 Python の有無によって `cmoc` がどう振る舞うかを知りたいとき。

## Do not read this when

- `<work-root>/bin/cmoc` の実装内容を直接確認したいとき。
- `bin/` 配下ではなく、`src/` や `oracle/` の別ディレクトリの文書を探しているとき。
- `cmoc` コマンドの利用手順全体ではなく、個別の実行ファイルだけを追いたいとき。

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
- `oracle` 側の正本仕様や `INDEX.md` の生成ルールだけを確認したいとき。

## hash

- 6acff2a397cd0c66553c35c5c3f0f45a551ed34bcae704aa612b4b485cce20d0

# `oracle`

## Summary

- `<cmoc-root>/oracle` 配下のルーティング文書で、`docs/` と `schemas/` への入口を案内する。
- `docs/` は利用手順・共通仕様・開発規約・パス表記・branch モデルの案内を扱う。
- `schemas/` は Structured Output schema の置き場所と役割分担を案内する。

## Read this when

- cmoc の利用方法、共通仕様、パス表記、branch モデルの入口をまとめて把握したいとき。
- 採用しなかった設計案や、その理由を確認したいとき。
- Structured Output schema の置き場所や役割分担を確認したいとき。
- どの下位ディレクトリの文書や個別仕様を読むべきか迷ったとき。

## Do not read this when

- `docs/` や `schemas/` の配下ファイルがすでに決まっていて、そこへ直接進むとき。
- この階層ではなく、下位ディレクトリの `INDEX.md` や個別仕様だけを確認したいとき。
- `README.md` や `AGENTS.md` など、`oracle` 以外の運用ルールを探しているとき。

## hash

- 202767e17d08cbb937c3732d418bf1f409b46ff60b614eaf55f918bf811bb5ac

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

- この `<work-root>/src` ディレクトリのルーティング文書で、`main.py`、`commons/`、`sub_commands/` への入口です。
- `main.py` は cmoc CLI のエントリーポイントで、Typer のルートアプリと各サブコマンド登録をまとめます。
- `commons/` は共通基盤、`sub_commands/` は `cmoc init` / `indexing` / `session` / `apply` / `review` の実装群です。

## Read this when

- cmoc の起動経路やサブコマンド全体の構成を最初に把握したいとき。
- `main.py`、`commons/`、`sub_commands/` のどこへ進むべきか迷ったとき。
- CLI 入口から共通基盤と個別サブコマンド実装への分岐を整理したいとき。

## Do not read this when

- 読みたい対象がすでに `main.py` や `commons/`、`sub_commands/` の個別ファイルで決まっているとき。
- 共通基盤や個別サブコマンドの実装詳細だけを直接確認したいとき。
- 生成物や補助ディレクトリではなく、この階層の入口だけを再確認したいとき。

## hash

- 10564b5b29da7f76c99f9606d199438907977b2227fb3bd0e242be501bf8d2b4

# `test.sh`

## Summary

- `test.sh` は `<cmoc-root>` を `CMOC_ROOT` として固定し、`<work-root>/.venv/bin` と `bin` を `PATH` の先頭側に通すための環境初期化スニペットです。
- cmoc コマンドや関連ツールを、このリポジトリのローカル環境で実行できる状態にすることが目的です。

## Read this when

- `CMOC_ROOT` を固定し、`PATH` に `<work-root>/.venv/bin` と `bin` を追加する環境設定を確認したいとき。
- cmoc 関連コマンドをこのワークツリーで実行する前の最小セットアップ手順を知りたいとき。
- シェルから cmoc を使うための前提環境を素早く把握したいとき。

## Do not read this when

- cmoc の実装本体やサブコマンド仕様を確認したいとき。
- pytest や個別テストケースの内容を確認したいとき。
- `oracle` の正本仕様や `INDEX.md` 生成ルールだけを確認したいとき。

## hash

- 9d5f6059b4a5acd4ec851223fc85c0acc2d9ae1ea244ff40ee48993217f1d9fc

# `tests`

## Summary

- `<cmoc-root>/tests` ディレクトリのルーティング文書で、pytest 共通設定と主要な回帰テスト入口をまとめる。
- `conftest.py` は `<cmoc-root>/src` を import path 先頭に追加する共通設定で、各テストから本体モジュールを直接 import できるようにする。
- `test_codex.py`、`test_file_naming.py`、`test_indexing.py`、`test_repo.py`、`test_report_files.py`、`test_timestamps.py` は共通機能や規約の回帰テスト入口で、`test_subcommands/` はサブコマンド横断の回帰テスト群への入口である。

## Read this when

- `<cmoc-root>/tests` 配下のどの回帰テストに進むべきか迷っているとき。
- pytest 共通設定、`commons.codex`、`commons.indexing`、`commons.repo`、`commons.report_files`、`commons.timestamps`、ファイル命名規則、サブコマンド回帰の入口をまとめて把握したいとき。
- 個別テストへ入る前に、`tests` ディレクトリ全体の役割分担を確認したいとき。

## Do not read this when

- 目的の個別テストファイルや `test_subcommands/` 配下の特定ファイルがすでに分かっていて、そこへ直接進むとき。
- `<cmoc-root>/src` の実装ロジックや `<cmoc-root>/oracle` の仕様断片だけを直接確認したいとき。
- `INDEX.md` の自動生成ルールやハッシュ管理だけを確認したいとき。

## hash

- 7024c90870d8bcf1012848617a94fdd75dd104b26dda0a08292af08d21cc390b
