# `AGENTS.md`

## Summary

- cmoc リポジトリで作業する AI 向けの基本ルールと参照範囲をまとめた最上位の運用文書。
- `oracles` を正本仕様として扱い、必要最小限のファイルだけを読むためのルーティング方針を定める。
- 閲覧・編集禁止領域、実装先、テスト先などの境界を明示する。

## Read this when

- cmoc リポジトリ全体の作業ルールや禁止事項を確認したいとき。
- `oracles` の正本仕様をどう辿るか、どの範囲を読めばよいかを知りたいとき。
- 実装先が `<cmoc-root>/src`、テスト先が `<cmoc-root>/tests` であることを確認したいとき。
- `memo` へのアクセス禁止や、編集禁止ファイルの扱いを把握したいとき。

## Do not read this when

- `oracles` 配下の個別仕様だけを確認したいときは、対応する `INDEX.md` から直接たどる。
- `README.md`、`AGENTS.md`、`memo` の運用ルールそのものを確認したいだけのとき。
- cmoc ではなく、別リポジトリや一般的な開発手順の確認が目的のとき。

## hash

- b2f93d440fb91234a2ff90e3b533ff1ba9230037690851040d4d8e5de5d0bf37

# `LICENSE`

## Summary

- このファイルは、このリポジトリに適用される利用許諾条件を示すライセンス文書です。
- 改変、再配布、再許諾、商用利用の可否と、その際に必要な条件を確認するために参照します。
- 保証の否認と責任の制限が明記されているため、法的条件を確認したいときの入口になります。

## Read this when

- このリポジトリの利用、改変、再配布に関する条件を確認したいとき。
- 著作権表示の保持義務や、許諾文の同梱要件を確認したいとき。
- 無保証条項や責任免除の内容を把握したいとき。

## Do not read this when

- cmoc の実装やテストの挙動を確認したいだけで、利用許諾の条件を確認する必要がないとき。
- `src`、`tests`、`oracles` の仕様やコードを追いたいとき。
- ライセンス表記の要否や再配布条件の確認が不要な通常の開発作業をしているとき。

## hash

- a894f2547af0349f234986eb4661f0146f37b7d82f8b22a27a674d5c1236f08f

# `README.md`

## Summary

- Codex Minimal Outrigger CLI (`cmoc`) の概要を説明する導入文書である。
- `cmoc` は Codex CLI を用いた開発を補助する最小限度の外部ツールとして位置づけられている。
- 初期セットアップの手順と、`cmoc` コマンドへパスを通す任意の設定例が書かれている。
- 基本ワークフローの入口として、`oracles/app_specs/usage.md` への案内がある。

## Read this when

- `cmoc` の全体像、役割、位置づけを最初に把握したいとき。
- 初期セットアップ手順として、clone、`.venv` 作成、`pip install -e .` を確認したいとき。
- `cmoc` コマンドに `bin/` を通す方法を確認したいとき。
- 基本ワークフローの入口として、どの仕様ファイルを先に読むべきか知りたいとき。

## Do not read this when

- `cmoc` の個別サブコマンドの詳細仕様や正本仕様を調べたいとき。
- `oracles` 配下の仕様断片や、実装・テストの細部を追いたいとき。
- README ではなく、`AGENTS.md` の運用ルールや編集可否だけを確認したいとき。
- 初期セットアップではなく、既に構築済みの開発環境や運用手順だけを確認したいとき。

## hash

- c9f160c5a2a14b1dece67dd6f263b3b59a8e586f606eeac39d5ac2239a75d3ff

# `bin`

## Summary

- `bin/cmoc` は cmoc コマンドのシェル製エントリーポイントです。
- スクリプト自身の位置から `<cmoc-root>` を解決し、`<cmoc-root>/.venv/bin/python` を実行 Python として使います。
- 仮想環境 Python が利用可能なときは、全引数を `<cmoc-root>/src/main.py` にそのまま渡して `exec` します。
- 仮想環境 Python が見つからない、または実行不可のときは、日本語の構造化エラーを標準出力へ表示し、セットアップ手順・必要な実行ファイル・簡易 Call stack を示して終了ステータス 1 で終了します。
- `line_number_of` は、エラー表示内の Call stack 用に、このスクリプト内で指定パターンに一致する最初の行番号を求める補助関数です。

## Read this when

- `bin/cmoc` がどの Python を使って `src/main.py` を起動するか確認したいとき。
- .venv/bin/python` が存在しない、または実行できない場合のエラー文面、終了ステータス、復旧手順を確認したいとき。
- シェル製の CLI エントリーポイントとして `bin/cmoc` の挙動を把握したいとき。
- `bin/cmoc` から `src/main.py` へ引数をそのまま渡す流れを確認したいとき。
- エラー表示内の Call stack を組み立てる `line_number_of` の役割を確認したいとき。

## Do not read this when

- `src/main.py` 以降の Python 実装や共通処理の仕様だけを確認したいとき。
- `cmoc` の各サブコマンド本体や引数解析の仕様だけを確認したいとき。
- pytest などのテスト観点やテストケースの整理だけを確認したいとき。
- `oracles` 側の仕様断片や `INDEX.md` の生成ルールだけを確認したいとき。
- 仮想環境の作成手順そのものではなく、依存関係や Python パッケージ構成を確認したいとき。

## hash

- 6b2ad008646b163ca4bd7bd4ced6f60b6cd655c9c1d0e19d068820da0bbab7b2

# `codex_minimal_outrigger_cli.code-workspace`

## Summary

- `codex_minimal_outrigger_cli.code-workspace` は `<cmoc-root>` を単一フォルダとして開く VS Code ワークスペース設定ファイルである。
- `settings.files.exclude` で `**/__pycache__` と `**/*.egg-info` を非表示にする設定を持つ。
- アプリ実行仕様ではなく、開発環境の入口と表示設定をまとめるためのファイルである。

## Read this when

- VS Code で `<cmoc-root>` を開くワークスペース設定を確認したいとき
- `**/__pycache__` や `**/*.egg-info` の除外設定を確認したいとき
- このリポジトリの開発用 workspace の入口を確認したいとき

## Do not read this when

- `cmoc` の実装やサブコマンド仕様を調べたいとき
- `tests` の期待値や `oracles` の正本仕様を確認したいとき
- `README.md` や `AGENTS.md` の運用ルールだけを確認したいとき

## hash

- 6acff2a397cd0c66553c35c5c3f0f45a551ed34bcae704aa612b4b485cce20d0

# `oracles`

## Summary

- `oracles` 配下の正本仕様断片をまとめた入口です。
- `app_specs`、`considered_alternatives`、`dev_rules` の各目次へ案内します。
- 人間が仕様を更新し、AI が実装を追従する前提で使います。

## Read this when

- `oracles` 全体の構成を素早く把握したいとき。
- 必要な正本仕様がどのディレクトリにあるかを確認したいとき。
- `cmoc` の仕様群を入口から辿りたいとき。

## Do not read this when

- 個別の仕様ファイルをすでに特定できているとき。
- 子ディレクトリの詳細だけを確認したいとき。
- 仕様ではなく実装やテストの作業だけを進めたいとき。

## hash

- 3cad3889683cae9eabe6ef48e9ad3d27ec353923c25e7c3c64799f145e40f74e

# `pyproject.toml`

## Summary

- `codex-minimal-outrigger-cli` のプロジェクト定義、バージョン、説明、Python 要件をまとめる。
- 実行時依存関係として `jsonschema`、`pytest`、`typer` を定義している。
- `project.scripts` で `cmoc` を `main:main` に接続し、`setuptools` による `src` 配置のビルド設定を持つ。

## Read this when

- パッケージ名、バージョン、説明文、Python 要件を確認したいとき。
- `jsonschema`、`pytest`、`typer` などの依存関係や追加・更新方針を確認したいとき。
- `cmoc = "main:main"` の実行エントリーポイントや、`src` 配置のパッケージ設定を確認したいとき。
- setuptools を使ったビルド設定や、`src/main.py` を中心とする配布・起動構成を確認したいとき。

## Do not read this when

- `cmoc` のコマンド挙動、サブコマンド仕様、エラーメッセージの内容を確認したいとき。
- `src/` 配下の実装ロジックや `tests/` の期待値を追いたいとき。
- 依存関係やビルド設定ではなく、README や `oracles/` の仕様断片だけを確認したいとき。

## hash

- c20014553a4e48f3a2f9f5221852179231c76594ccc1bc4c82b8dddc651b203e

# `src`

## Summary

- cmoc の Python 実装が集まるルートで、CLI 入口の `main.py`、共通基盤の `commons/`、サブコマンド本体の `sub_commands/` をまとめています。
- `main.py` は Typer のアプリ構成と例外整形を担当し、`commons/` は共有処理、`sub_commands/` は `init`・`session`・`apply`・`review oracles` の実装を含みます。
- このディレクトリは、cmoc の起動点と機能別実装の配置を把握するための入口です。

## Read this when

- cmoc の CLI 入口やサブコマンド群の全体構成を確認したいとき。
- `main.py`、`commons/`、`sub_commands/` のどこに何があるかを素早く振り分けたいとき。
- 共通処理と個別サブコマンドの責務分担を俯瞰してから実装や修正に入りたいとき。

## Do not read this when

- 個別のサブコマンド仕様だけを確認したいときは、この目次ではなく該当する `src/sub_commands/...` のモジュールを直接読むべきです。
- `commons/` の特定モジュールだけを追いたいときは、このディレクトリ全体ではなく対象ファイルを直接見るべきです。
- `INDEX.md` の生成ルールや `oracles` 側の正本仕様だけを確認したいときは、このディレクトリではなく該当する仕様文書を読むべきです。

## hash

- d24b817bae0fb8c13083927bfca5b7ba0a913e471df524339f7be12336b2a6a5
<!-- cmoc-index-kind: directory -->

# `test.sh`

## Summary

- `cmoc` 開発用のシェル初期化スクリプトで、`CMOC_ROOT` を固定し、`.venv/bin` と `bin` を `PATH` に追加する。
- `<cmoc-root>` のローカル実行環境で `cmoc` や仮想環境内のコマンドを優先して使うための補助ファイルである。
- テストや手動実行の前に、`cmoc` ルートを前提にしたコマンド探索環境を整える役割を持つ。

## Read this when

- `<cmoc-root>` 配下の `.venv` や `bin` を優先する実行環境を用意したいとき。
- `cmoc` コマンドや仮想環境内のツールを同じ `PATH` で使いたいとき。
- 手元のシェルやテスト実行で `CMOC_ROOT` を固定したいとき。

## Do not read this when

- cmoc 本体の仕様、サブコマンド仕様、`oracles` の内容を確認したいとき。
- Python 実装や pytest のテストコードを読みたいとき。
- リポジトリ全体の初期化や Git 運用ルールだけを確認したいとき。

## hash

- 6fc07bc0dff2b064245772154c4f103ce2d3d0cbe7536ae9124eb49e183c6b44

# `tests`

## Summary

- pytest ベースの回帰テスト群をまとめた入口です。`conftest.py` による import path 設定を含め、`commons` と `sub_commands` の主要ロジックを検証します。
- `test_codex.py`、`test_indexing.py`、`test_repo.py`、`test_subcommands.py` で、Codex 呼び出し、INDEX.md 保守、git 共通処理、CLI 入口の制御を確認します。
- `test_file_naming.py`、`test_report_files.py`、`test_timestamps.py` で、命名規則、レポート保存、タイムスタンプ仕様の回帰を押さえます。

## Read this when

- `tests` 配下でどの回帰テストがどの責務を持つかを俯瞰したいとき。
- `commons` や `sub_commands` の変更がどのテストに効くかを判断したいとき。
- pytest の共通設定や各テストファイルの守備範囲を確認したいとき。

## Do not read this when

- `src` 側の実装ロジックや `oracles` の正本仕様だけを確認したいとき。
- 個別テストの期待値やモック実装だけを読みたいとき。
- `INDEX.md` 生成ルールそのものや、リポジトリ全体のルーティング方針だけを確認したいとき。

## hash

- af81d2f4c777e4bdeceb2b66b1e9724952757241deb6a1d7c093f67f52abba7e
<!-- cmoc-index-kind: directory -->
