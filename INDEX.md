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
- `bin/cmoc` は `<cmoc-root>` を解決し、`<cmoc-root>/.venv/bin/python` を実行 Python として使って `src/main.py` を起動します。
- 仮想環境 Python が見つからない、または実行不可の場合の日本語エラー表示と終了処理を扱います。
- `line_number_of` はエラー表示内の Call stack 用に、指定パターンの最初の行番号を求める補助関数です。

## Read this when

- cmoc コマンド起動時に、どの Python とどの Python ファイルが実行されるか確認したいとき。
- `.venv/bin/python` が無い場合や実行不可の場合のエラー文面、終了ステータス、復旧手順を確認したいとき。
- cmoc の配布用または開発用 CLI ラッパーの挙動を調べたいとき。
- `bin/cmoc` から `<cmoc-root>/src/main.py` への引数受け渡し方法を確認したいとき。
- 仮想環境未セットアップ時のユーザー向け案内や Call stack 表示の実装を変更・検証したいとき。

## Do not read this when

- cmoc の各サブコマンドの具体的な処理内容やアプリケーション仕様を確認したいとき。
- `src/main.py` 以降の Python 実装やコマンドディスパッチの詳細を追いたいとき。
- pytest や Fake Codex CLI など、テスト実装やテストケース本体を確認したいとき。
- `<repo-root>` 側で cmoc が生成・管理するファイルや別の `INDEX.md` の仕様を確認したいとき。

## hash

- 160e19df3f9b3de96dc5dc79fea7fa0837b099f6220d61742a9b8c141cd23d51

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

- `cmoc` の正本仕様断片をまとめた入口で、`app_specs`、`considered_alternatives`、`dev_rules` への案内をまとめます。
- `app_specs/INDEX.md` から共通仕様や個別サブコマンド仕様へ、`considered_alternatives/INDEX.md` から採用しなかった設計案へ、`dev_rules/INDEX.md` から実装・テスト規約へ進めます。
- `oracles` 配下のファイルは人間が所有する正本仕様であり、AI は読み取りはできても編集しない前提を整理します。

## Read this when

- cmoc の正本仕様断片をどこから辿るか確認したいとき。
- `oracles` 配下の各ディレクトリの役割を切り分けたいとき。
- 実装やテストに進む前に、参照すべき仕様群を整理したいとき。
- 採用案と不採用案の判断材料を、仕様断片として横断的に見直したいとき。

## Do not read this when

- 個別仕様本文だけを確認したいときは、この `INDEX.md` ではなく各ディレクトリの `INDEX.md` や個別の `*.md` を直接読むべきです。
- 実装コードやテストコードだけで足りるときは、この案内は不要です。
- `INDEX.md` の生成・更新ルールだけを確認したいときは、`app_specs/indexing.md` を読むべきです。
- `oracles` ファイルの編集可否や所有権だけを確認したいときは、`app_specs/oracles.md` を読むべきです。

## hash

- 4f29fb4b2b5dda110ddfe6391a7e6ec0b8e034dc7244bbef970a7053a9ae13bf

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

- `src` は `cmoc` の Python 実装の入口で、CLI エントリーポイント、共有基盤、サブコマンド実装への案内をまとめるディレクトリです。
- `main.py` は `cmoc` CLI の起動口で、Typer アプリの組み立てとコマンド登録を担います。
- `commons/` は共通処理群、`sub_commands/` は `init`、`eval-oracles`、`session`、`apply` などのサブコマンド実装群への入口です。

## Read this when

- `src` 配下の全体構成を把握して、どの入口ファイルへ進むべきか判断したいとき。
- `cmoc` の CLI 起動口、共通基盤、サブコマンド実装の役割分担を整理したいとき。
- `main.py`、`commons/`、`sub_commands/` のどれを読むべきか、このディレクトリの目次から素早く切り分けたいとき。
- ソースコード全体のルーティングを確認してから、個別モジュールの実装やレビューに進みたいとき。

## Do not read this when

- 個別サブコマンドの動作だけを確認したいときは、`src/main.py` や `src/sub_commands/` の該当モジュールを直接読むべきです。
- 共有処理の実装詳細だけを確認したいときは、この目次ではなく `src/commons/` 配下の個別モジュールを読むべきです。
- `INDEX.md` の生成・維持ルールだけを確認したいときは、`src/commons/indexing.py` と `oracles/app_specs/indexing.md` を読むべきです。
- CLI の利用手順やユーザー向け仕様だけを確認したいときは、`oracles/app_specs/` 配下の文書を優先して読むべきです。

## hash

- 9dad4660cc15ca5091d6855a875cbb66f1fd27502a8a3b8393b8e5affe1440e1

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

- `tests` 配下の pytest ベース回帰テスト群への入口で、共通設定の `conftest.py` と各 `test_*.py` を案内します。
- `test_codex.py` は Codex CLI 呼び出しラッパー、`test_indexing.py` は `INDEX.md` メンテナンス、`test_repo.py` は git 共通処理、`test_subcommands.py` はサブコマンド制御ロジックを扱います。
- `test_timestamps.py` はタイムスタンプと経過時間表示、`test_file_naming.py` は旧ルーティングファイルや配置規則の回帰を確認します。

## Read this when

- `tests` 配下でどのテスト群が何を検証しているかを、入口から素早く把握したいとき。
- pytest 実行時の import path 設定を含む `conftest.py` の役割を確認したいとき。
- `test_codex.py`、`test_indexing.py`、`test_repo.py`、`test_subcommands.py`、`test_timestamps.py`、`test_file_naming.py` のどこへ進むべきか整理したいとき。
- `cmoc` の共通処理、`INDEX.md` メンテナンス、git リポジトリ処理、サブコマンド制御、タイムスタンプ仕様の回帰テストをまとめて見渡したいとき。

## Do not read this when

- 個別の実装ロジックや関数本体だけを追いたいときは、`src` 配下の該当モジュールを直接読むべきです。
- `oracles` 配下の正本仕様や `INDEX.md` 生成ルールそのものを確認したいときは、このテスト目次ではなく仕様側の文書を参照すべきです。
- pytest の共通設定や各テストファイルの役割分担ではなく、単一のテストケースの期待値だけを確認したいときは、この案内を読む必要はありません。

## hash

- 7c287036db2cbfef6d6144c3e8580ca55ce861787ce388c43bd844e80da60698
