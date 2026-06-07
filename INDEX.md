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

- `src` ディレクトリのルーティング文書で、cmoc CLI の起点 `main.py` と、共通モジュール群 `commons/`、サブコマンド実装群 `sub_commands/` への入口をまとめる階層です。
- `main.py` は Typer の CLI エントリーポイントで、`init`、`indexing`、`session`、`apply`、`review` の各コマンド登録と共通エラー整形の起点を担います。
- `commons/` は実行基盤や共通処理のまとまりで、`sub_commands/` は各サブコマンド本体へ分岐する入口です。

## Read this when

- `src` ディレクトリ全体の役割と、どの入口ファイル・下位ディレクトリへ進むべきかを整理したいとき。
- cmoc CLI のエントリーポイント `main.py` と、`commons/`、`sub_commands/` の役割分担を把握したいとき。
- `INDEX.md` から `src/main.py`、`src/commons/`、`src/sub_commands/` のどれを読むべきか迷ったとき。
- 実装やテストの前に、`src` 階層の入口構造を短く一覧したいとき。

## Do not read this when

- 読むべき個別モジュールがすでに分かっていて、`main.py`、`commons/`、`sub_commands/` のいずれかへ直接進めるとき。
- `cmoc init`、`cmoc indexing`、`cmoc session`、`cmoc apply`、`cmoc review` の詳細実装だけを確認したいとき。
- `src` 配下のルーティングではなく、`README.md` や `AGENTS.md` などのリポジトリ運用ルールだけを確認したいとき。
- `commons` や `sub_commands` の下位 `INDEX.md` だけを個別に確認したいとき。

## hash

- b9897efbb181ab6f665f6cc79f095a8f9b0214be0989d558b3ca2012f4cc8579

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

- `tests/` ディレクトリのルーティング文書で、`conftest.py` と各回帰テスト群への入口です。
- pytest の共通設定、`commons` の共通ヘルパー、CLI サブコマンド横断の回帰テストをまとめて案内します。
- `INDEX.md` の生成・再利用ルールそのものではなく、`tests` 配下のどのファイルを読むべきか切り分けるための目次です。

## Read this when

- `pytest` の共通設定やテスト補助の入口を探したいとき。
- `commons.codex`、`commons.indexing`、`commons.repo`、`commons.report_files`、`commons.timestamps` の回帰テストの所在を確認したいとき。
- `init` / `session` / `apply` / `review oracles` を横断する CLI テストの入口を探したいとき。
- ファイル命名規則や `INDEX.md` メンテナンス、レポート出力など個別領域のテストを切り分けたいとき。

## Do not read this when

- すでに対象の個別テストファイル名が分かっていて、`tests/` の入口を経由せず直接読めるとき。
- `src/` 側の実装ロジックや `oracles` 配下の正本仕様だけを確認したいとき。
- pytest の実行方法やリポジトリ運用ルールだけを確認したいとき。
- 個別の回帰テスト本体ではなく、設計規約や開発規約の文書を探しているとき。

## hash

- 9dfb9c7f71d4384ac35d430dbe19d1ffed40b5f50081574a2936da3aa1276604
