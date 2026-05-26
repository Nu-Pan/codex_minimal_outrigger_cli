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

- `bin` 配下の入口として `bin/cmoc` の役割と起動経路をまとめる。
- スクリプト自身の場所から `<cmoc-root>` を解決し、`<cmoc-root>/.venv/bin/python` を実行 Python として使う。
- 仮想環境 Python が利用できる場合は `<cmoc-root>/src/main.py` に全引数を渡して `exec` する。
- 仮想環境 Python が見つからない、または実行不可の場合は、日本語の構造化エラーを標準出力へ出し、セットアップ手順・必要な実行ファイル・Call stack を示して終了ステータス 1 で終了する。
- `line_number_of` はエラー表示の Call stack 用に、このスクリプト内の指定パターンに一致する最初の行番号を求める補助関数である。

## Read this when

- `cmoc` 起動時に、どの Python とどの Python ファイルが実行されるか確認したいとき。
- `.venv/bin/python` が無い場合や実行不可の場合のエラー文面、終了ステータス、復旧手順を確認したいとき。
- `bin/cmoc` から `<cmoc-root>/src/main.py` への引数受け渡し方法を確認したいとき。
- 仮想環境未セットアップ時のユーザー向け案内や Call stack 表示の実装を変更・検証したいとき。

## Do not read this when

- `cmoc` の各サブコマンドの具体的な処理内容を確認したいとき。
- `src/main.py` 以降の Python 実装やコマンドディスパッチの詳細を確認したいとき。
- pytest や Fake Codex CLI など、テスト実装の規約やテストケース本体を確認したいとき。
- `bin/cmoc` ではなく、`src` 配下の本体仕様を調べたいとき。

## hash

- 670c4146f37c39ca4785c462cbfb31ad730ef6d03952fdf7e4b91474fa2a6264

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

- `cmoc` の正本仕様断片をまとめる `oracles` のルート目次です。
- `app_specs`、`considered_alternatives`、`dev_rules` への入口を提供します。
- どの仕様群を読むべきか迷ったときの最初の案内として使います。

## Read this when

- `oracles` 全体の入口と、どの仕様群へ進むべきかを確認したいとき。
- アプリ仕様、採用しなかった代替案、開発ルールのどれを読むべきか整理したいとき。
- 下位の `INDEX.md` や個別仕様へ進む前に、`oracles` の構成を俯瞰したいとき。

## Do not read this when

- 目的の仕様がすでに分かっていて、`app_specs`、`considered_alternatives`、`dev_rules` の下位文書を直接開けば足りるとき。
- 個別サブコマンドや単独の設計判断だけを確認したいとき。
- 実装コードやテストコードだけで十分で、`oracles` の案内が不要なとき。

## hash

- b3d0489bd52c7e3a4b34d1694b46a0401f65851b343712c5490cd59d4be0ee99

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

- cmoc の Python ソースツリーの入口で、CLI 起動点 `main.py` と共通基盤 `commons`、サブコマンド実装 `sub_commands` をまとめる。
- `main.py` は Typer アプリの登録と例外整形付き起動を担い、`commons` は共有ユーティリティ、`sub_commands` は各コマンド本体を収める。
- この階層から個別実装へ辿る場合の起点として使う。

## Read this when

- cmoc の起動フローや `main.py` の役割を確認したいとき。
- 共有処理を `commons` から追うか、各コマンド本体を `sub_commands` から追うかを判断したいとき。
- Python ソース全体の入口だけを把握したいとき。

## Do not read this when

- 特定のサブコマンドや共通モジュールの詳細仕様を知りたいときは、各子ディレクトリの `INDEX.md` を読む。
- `oracles` の仕様断片、`README.md`、`AGENTS.md`、`memo` の運用だけを確認したいとき。
- テスト実装や個別の開発ルールだけを追いたいとき。

## hash

- dcf5800597bdb17a27d2850a5bdfa9755dea10d66edb39493f68ae5c5c5c1d99

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

- `tests` ディレクトリのルーティング索引で、配下の各テストファイルが何を検証するかを案内する。
- `conftest.py` による import path 設定から、Codex 呼び出し、INDEX.md メンテナンス、git 共通処理、サブコマンド制御、タイムスタンプ、命名規則までを対象にする。
- 個別テストの詳細に入る前の入口として、必要なテストファイルへ最短で辿るための目次である。

## Read this when

- `tests` 配下にどのテスト群があり、何を検証しているかを一覧したいとき。
- `conftest.py` の共通設定、`test_codex.py`、`test_indexing.py`、`test_repo.py`、`test_subcommands.py`、`test_timestamps.py`、`test_file_naming.py` の役割を辿りたいとき。
- pytest の共通 fixture、CLI 呼び出し、INDEX メンテナンス、git リポジトリ処理、タイムスタンプ処理のどこにテストがあるか確認したいとき。

## Do not read this when

- `tests` 配下の個別テストの期待値や実装詳細を確認したいときは、対応する各 `test_*.py` を直接読む。
- `cmoc` の正本仕様や `oracles` 側の断片だけを確認したいときは、この索引ではなく `oracles` を読む。
- `README.md`、`AGENTS.md`、`memo` の運用ルールや編集可否だけを知りたいときは、この索引は目的が違う。

## hash

- a67a0a3bae4cb9a7091e6566a91afed9742c4ef33a0286a917062b772df62f3c
