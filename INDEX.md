# `AGENTS.md`

## Summary

- `cmoc` リポジトリ全体の作業ルールとルーティング方針をまとめた入口です。
- `cmoc` の開発と `cmoc` を用いた開発を区別し、参照してよい・よくないファイルの扱いを示します。
- `oracles` 配下の `INDEX.md` を起点に必要最小限の仕様断片だけを読むための案内です。
- 実装は `<cmoc-root>/src`、自動テストは `<cmoc-root>/tests` に置く前提を明示します。

## Read this when

- このリポジトリで作業する前に、基本ルールと役割分担を確認したいとき。
- `cmoc` 自体の開発と `cmoc` を使った開発を区別したいとき。
- `memo` や `README.md` などの閲覧・編集制約を確認したいとき。
- `oracles` の正本仕様を読む前に、どの `INDEX.md` を起点にたどるか知りたいとき。
- 実装を `<cmoc-root>/src`、テストを `<cmoc-root>/tests` に置く前提を確認したいとき。

## Do not read this when

- 個別サブコマンドの引数や終了条件だけを確認したいとき。
- `oracles` 配下の特定仕様断片を直接確認したいとき。
- 実装コードやテストコードの内容だけを見たいとき。

## hash

- b2f93d440fb91234a2ff90e3b533ff1ba9230037690851040d4d8e5de5d0bf37

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

- `bin/cmoc` は cmoc コマンドのシェル製エントリーポイントです。
- スクリプト自身の位置から `<cmoc-root>` を解決し、`<cmoc-root>/.venv/bin/python` を実行 Python として使います。
- 仮想環境 Python が使えるときは、全引数を `<cmoc-root>/src/main.py` にそのまま渡して `exec` します。
- 自動補完プローブでも、Python が使える場合は同じく `src/main.py` を起動し、使えない場合は終了ステータス 1 で終わります。
- 仮想環境 Python が見つからない、または実行できないときは、日本語の構造化エラー、セットアップ手順、必要な実行ファイル、簡易 Call stack を標準エラーに出します。
- `line_number_of` は、エラー表示用の Call stack に必要な行番号を求める補助関数です。

## Read this when

- `cmoc` がどの Python で `src/main.py` を起動するか確認したいとき。
- `_CMOC_COMPLETE` が設定された自動補完プローブ時の分岐を確認したいとき。
- 仮想環境 Python が無い、または実行できない場合のエラー文面、終了ステータス、復旧手順を確認したいとき。
- `src/main.py` へ引数をそのまま渡す流れを確認したいとき。
- エラー表示に出る簡易 Call stack の行番号の取り方を追いたいとき。

## Do not read this when

- `src/main.py` 以降の Python 実装や共通処理の仕様だけを確認したいとき。
- `cmoc` の各サブコマンド本体や引数解析の仕様だけを確認したいとき。
- pytest などのテスト観点やテストケースの整理だけを確認したいとき。
- `oracles` 側の仕様断片や `INDEX.md` の生成ルールだけを確認したいとき。
- 仮想環境の作成手順そのものではなく、依存関係や Python パッケージ構成を確認したいとき。

## hash

- 266af899cfd1d573ae1697ad75b016e90b859fb186f232969b030804a465f247

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

- この `oracles` ディレクトリのルーティング文書で、`docs/` と `schemas/` への入口を案内します。
- `docs/` は人間向けの正本仕様断片、`schemas/` は Structured Output schema の置き場として扱います。
- 個別文書に入る前に、参照先の系統を切り分けるための目次です。

## Read this when

- `oracles` 配下で、人間向けの仕様と機械向けのスキーマのどちらへ進むべきか整理したいとき。
- `docs/` にある仕様断片と、`schemas/` にある Structured Output schema の役割分担を把握したいとき。
- 目的に応じて、どの下位ディレクトリの文書を読むべきか迷ったとき。

## Do not read this when

- すでに目的の文書やスキーマの場所が分かっていて、`docs/` や `schemas/` の下位ファイルへ直接進めるとき。
- `oracles` 配下の個別仕様や Structured Output schema だけを確認したいとき。
- この階層ではなく、リポジトリ全体の運用ルールや別ディレクトリの目次だけを確認したいとき。

## hash

- 138646edaf0942b63715d5888a0f9c984718ab72b096f9caf6f5c09e70bc4c42

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

- `src` は cmoc 本体の実装をまとめるルートディレクトリです。
- `main.py` に CLI の起点があり、`commons/` に共通基盤、`sub_commands/` に各サブコマンド実装が入っています。
- このディレクトリは、機能ごとの実装へ進むための最上位ルーティング地点です。

## Read this when

- `cmoc` 本体の実装入口として、`src` 全体の役割と構成を把握したいとき。
- CLI エントリポイント、共通基盤モジュール、サブコマンド実装の配置を俯瞰したいとき。
- `main.py`、`commons/`、`sub_commands/` のどこを読むべきか切り分けたいとき。

## Do not read this when

- cmoc の利用手順や `oracles` 側の正本仕様だけを確認したいとき。
- 個別の実装ファイル 1 つだけを追いたいときで、ディレクトリ全体の案内が不要なとき。
- テストコードや README など、`src` 以外の資料を確認したいとき。

## hash

- 39ad2bfdba6deedd287fea2f1f934b0a60a9e6b026a8c61fd68b59222a51b5f9

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

- `tests` は cmoc の pytest 回帰テストをまとめるディレクトリで、共通設定と機能別テストを置きます。
- `conftest.py` は `src` を import path に追加し、テストから本体モジュールを直接 import できるようにします。
- `test_codex.py` は `commons.codex` の `run_codex_exec`、Structured Output、再試行、quota / resume、oracle 保護を検証します。
- `test_indexing.py` は `INDEX.md` 自動生成と更新、除外条件、再利用判定、排他 lock を検証します。
- `test_repo.py` は repo root 検出、`.cmoc` の ignore 保証、差分検出、session / apply 状態管理を検証します。
- `test_subcommands.py` は `init` / `session` / `apply` / `review` の制御フローと CLI 登録を検証します。
- `test_report_files.py` と `test_timestamps.py` はタイムスタンプ生成、経過時間表示、レポート保存の境界を検証します。
- `test_file_naming.py` は旧ルーティングファイルの残存がないことを検証します。

## Read this when

- pytest の共通設定や `src` への import path 追加方法を確認したいとき。
- `commons.codex`、`commons.indexing`、`commons.repo`、`commons.report_files`、`commons.timestamps`、`commons.timing` の回帰テスト範囲を確認したいとき。
- `cmoc` のサブコマンド群や `INDEX.md` メンテナンスの期待挙動を変更・レビューしたいとき。
- 旧 `routing.md` / `ROUTING.md` を使わない方針や、テスト命名の前提を確認したいとき。

## Do not read this when

- 実装本体のロジックだけを追いたいとき。
- `oracles` の正本仕様や個別サブコマンドの利用手順だけを確認したいとき。
- テストの具体的な fixture、mock、補助関数の実装詳細だけを探したいとき。
- `memo` や編集禁止ファイルの扱いを確認したいとき。

## hash

- 9bef87e975733f09fb4f2e1e1e1df16c3eb44235b5b7c1a46dc2d273c1b2a7ad
