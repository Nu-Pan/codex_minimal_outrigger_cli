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

- `bin` ディレクトリは `cmoc` コマンドのシェル製エントリーポイントを置く場所です。
- `bin/cmoc` は `<cmoc-root>` を解決し、`.venv/bin/python` で `src/main.py` を起動します。
- 仮想環境 Python が使えない場合は、日本語の構造化エラーを出して終了します。
- `line_number_of` は、エラー出力の Call stack に必要な行番号を求める補助関数です。

## Read this when

- `bin/cmoc` がどの Python で `src/main.py` を起動するか確認したいとき。
- .venv/bin/python` が無い、または実行できない場合のエラー文面・終了ステータス・復旧手順を確認したいとき。
- シェル製 CLI エントリーポイントとしての挙動を把握したいとき。
- `bin/cmoc` から `src/main.py` へ引数をそのまま渡す流れを確認したいとき。
- エラー表示内の Call stack を組み立てる `line_number_of` の役割を確認したいとき。

## Do not read this when

- `src/main.py` 以降の Python 実装や共通処理の仕様だけを確認したいとき。
- `cmoc` の各サブコマンド本体や引数解析の仕様だけを確認したいとき。
- pytest などのテスト観点やテストケースの整理だけを確認したいとき。
- `oracles` 側の仕様断片や `INDEX.md` の生成ルールだけを確認したいとき。
- 仮想環境の作成手順そのものではなく、依存関係や Python パッケージ構成を確認したいとき。

## hash

- a39e49691047ca09c700d3e3e104a7c020389ca8f5c4857f3fd0479efbb23443

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

- `cmoc` の正本仕様断片をまとめる `oracles` ディレクトリの入口です。
- 配下の `docs` から、開発ルール、アプリ仕様、代替案、各種共通仕様へたどれます。
- このディレクトリ自体はルーティング用で、詳細仕様は下位の文書に分かれています。

## Read this when

- `cmoc` の正本仕様断片がどこにあるか、全体の入口を把握したいとき。
- `oracles` 配下の `docs` 以下へどの順で進むべきかを整理したいとき。
- `oracles` 全体の役割や、仕様断片の配置場所を俯瞰したいとき。

## Do not read this when

- 個別のサブコマンド仕様や設計判断だけを確認したいときは、このディレクトリではなく配下の該当文書を直接読むべきです。
- 実装コードやテストコードの作業だけで足りるときは、この目次を読む必要はありません。
- `oracles` 配下のどの仕様を読むべきか自明な場合は、入口ではなく目的のファイルへ直接進むべきです。

## hash

- fa379c76438c952476ee4ff0ca92f2a3c97fbb392e45c3043f50318524144f11

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

- `src` は cmoc の Python 実装を置くソースルートです。
- `main.py` は CLI 入口、`commons` は共通基盤、`sub_commands` は各サブコマンド実装の入口です。
- このディレクトリは、CLI 入口、共通処理、サブコマンド実装へ進むためのルーティング起点です。

## Read this when

- `src` 全体の役割と、どの入口から各配下へ進むべきか確認したいとき。
- cmoc の CLI 入口、共通基盤、サブコマンド実装の配置を俯瞰したいとき。
- `src/INDEX.md` の案内先や、配下の目次を保守・更新したいとき。
- 実装を読む前に、`main.py`・`commons`・`sub_commands` の関係を整理したいとき。

## Do not read this when

- `src/commons`、`src/sub_commands`、`src/main.py` の個別実装だけを確認したいとき。
- `oracles` 側の正本仕様だけを確認したいとき。
- `__pycache__` や `*.egg-info` などの生成物を追いたいとき。
- `src/INDEX.md` の生成・保守ルールそのものだけを確認したいとき。

## hash

- 77659effa0531a6f973a7711d5fc7255c7934a6a919ed621fd42302279d11d9d

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

- `tests/conftest.py` は pytest 実行時に `<cmoc-root>/src` を import path に追加する共通設定です。
- `tests/test_codex.py` は Codex CLI 呼び出しラッパーの再試行、Structured Output、ログ、通知、workspace-write 時の oracle 保護、quota/resume 復旧を検証します。
- `tests/test_file_naming.py` はルート直下の命名規則と、旧ルーティングファイルの不在を確認します。
- `tests/test_indexing.py` は `INDEX.md` メンテナンス処理、再生成条件、hash、gitignore、symlink、binary、並列化、ロック、コミット挙動を検証します。
- `tests/test_repo.py` は git リポジトリ共通処理、`.cmoc` の ignore 保証、ファイル列挙、差分検出、session state、active session 判定を検証します。
- `tests/test_report_files.py` はタイムスタンプ付きレポート保存の上書き回避と再試行を検証します。
- `tests/test_subcommands.py` は `init`、`session`、`apply`、`review oracles` を含む CLI 統合フローと決定論的な制御ロジックを検証します。
- `tests/test_timestamps.py` はタイムスタンプ生成、継続時間表示、関連ヘルパーの並び順などの時刻系仕様を検証します。

## Read this when

- pytest の共通設定、個別テスト、回帰対象の範囲を素早く把握したいとき。
- `INDEX.md` メンテナンス、git 共通処理、CLI 実行、サブコマンド統合挙動のどれをどのテストが守っているか確認したいとき。
- `cmoc` の実装変更に対して、どのテストファイルを優先的に読むべきか判断したいとき。
- テスト群全体の責務分担を、ファイル単位の入口として確認したいとき。

## Do not read this when

- `src` 側の実装ロジックや、個別関数の内部処理だけを追いたいとき。
- `oracles` 配下の正本仕様や、`INDEX.md` の生成ルールそのものを確認したいとき。
- README や AGENTS、memo などのファイルアクセス規則だけを確認したいとき。
- 特定のサブコマンド仕様だけを知りたいときは、この配下ではなく対応する仕様文書や実装を読むべきです。

## hash

- f28119cceddaa02dc194838a77d3ad2260424cf417f2548e9aa1677d9d9925db
