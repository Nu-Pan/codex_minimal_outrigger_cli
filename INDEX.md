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

- `bin` ディレクトリの入口で、`cmoc` コマンドのシェル製エントリーポイントを案内します。
- `bin/cmoc` は `<cmoc-root>` を解決し、`<cmoc-root>/.venv/bin/python` を使って `src/main.py` を起動します。
- 仮想環境 Python が見つからない、または実行不可の場合の日本語エラー表示と終了処理を扱います。
- `line_number_of` はエラー表示内の Call stack 用に、指定パターンの最初の行番号を求める補助関数です。

## Read this when

- `cmoc` 起動時に、どの Python が実行されるかを確認したいとき。
- .venv が無い、または実行できない場合のエラー文面と復旧手順を確認したいとき。
- `bin/cmoc` から `<cmoc-root>/src/main.py` への引数受け渡しや Call stack 表示を確認したいとき。

## Do not read this when

- `cmoc` の各サブコマンドの処理内容やアプリ仕様だけを確認したいとき。
- Python 実装や `src/main.py` 以降のディスパッチ処理を追いたいとき。
- pytest などのテストケース本体や、`bin/cmoc` 以外の実装を確認したいとき。

## hash

- 5a7c1ad7ae81d60c96cbfc13ff5430f2fe21d49e82a13eb5fe0ca68ce90b9feb
<!-- cmoc-index-kind: directory -->

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
<!-- cmoc-index-kind: directory -->

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

- `src` は cmoc の実装ルートで、CLI 入口・共通処理・サブコマンド実装をまとめるディレクトリです。
- `main.py` で Typer のルートと各サブアプリを組み立て、`commons/` と `sub_commands/` に実処理を分けます。
- 個別ファイルへ進む前に、`src` 配下の責務分担を素早く振り分けるための目次です。

## Read this when

- `src` 配下のどこに CLI 入口、共有処理、個別コマンド本体があるか確認したいとき。
- `main.py` から `commons/` と `sub_commands/` へどうルーティングされるか把握したいとき。
- どの実装ファイルを先に読むべきかを整理したいとき。

## Do not read this when

- 個別サブコマンドの引数、状態遷移、エラー処理の詳細だけを確認したいとき。
- `src/commons` の共通処理だけ、または `src/sub_commands` の個別実装だけを直接追いたいとき。
- `src` 全体ではなく、`oracles` 側の正本仕様や別ディレクトリの目次ルールだけを確認したいとき。

## hash

- 328f2706c60e9714c22bbe5a8459ae340af6e2e5e44d39c6f2bf1311ac19490e
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

- `tests` は cmoc の決定論的な制御ロジックを守る pytest 回帰テスト群の入口です。
- `conftest.py` による import 設定と、`test_codex.py`、`test_file_naming.py`、`test_indexing.py`、`test_repo.py`、`test_report_files.py`、`test_subcommands.py`、`test_timestamps.py` の各テスト領域を案内します。
- CLI 起動、サブコマンド委譲、INDEX.md メンテナンス、Git 共通処理、レポート保存、タイムスタンプ、命名規則など、実装変更の影響範囲を見極めるための目次です。

## Read this when

- `tests` 配下の pytest が何を守っているか、全体の回帰範囲を把握したいとき。
- `src/commons`、`src/sub_commands`、CLI 起動経路、`INDEX.md` 維持、Git まわりの仕様変更がどのテストに影響するか確認したいとき。
- テスト共通設定の `conftest.py` や、`test_codex.py`、`test_indexing.py`、`test_repo.py`、`test_subcommands.py` などの役割を振り分けたいとき。
- 新しい回帰テストを追加する前に、既存のテスト群がどの機能領域をカバーしているか整理したいとき。

## Do not read this when

- cmoc の実装ロジックそのものや、`src` 配下の個別モジュールのコードだけを確認したいとき。
- `oracles` 側の正本仕様やサブコマンド仕様を読みたいだけで、テストの回帰範囲は不要なとき。
- `README.md`、`AGENTS.md`、`memo` などのファイルアクセス規則や、テスト以外の文書だけを確認したいとき。
- Codex CLI や LLM の品質そのものを検証したいのではなく、決定論的な制御ロジックの仕様確認に目的がないとき。

## hash

- 0bcfb23be5a9ec6321edd5e1c66ef5090b09a587323de818d0e8f41ea322290b
<!-- cmoc-index-kind: directory -->
