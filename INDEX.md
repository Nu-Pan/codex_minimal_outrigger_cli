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

- `oracles` 配下の入口であり、仕様の種類ごとに読むべきディレクトリを案内する目次です。
- `app_specs` は利用手順とサブコマンド仕様、`dev_rules` は実装・テスト・環境ルール、`considered_alternatives` は採用しなかった設計案をまとめます。
- 個別の仕様断片を探すときは、この目次から該当ディレクトリへ進みます。

## Read this when

- `oracles` 配下のどこから読み始めるべきかを知りたいとき。
- 仕様の種類ごとに、利用手順・開発ルール・代替案のどれを読むべきか素早く選びたいとき。
- `cmoc` の正本仕様断片を全体として俯瞰し、入口を整理したいとき。

## Do not read this when

- すでに読むべき個別ファイルが決まっていて、該当ディレクトリの `INDEX.md` や各仕様ファイルを直接開く段階にあるとき。
- `app_specs`、`dev_rules`、`considered_alternatives` のうち、特定の 1 系統だけを確認したいとき。
- `oracles` 以外の `<cmoc-root>` 全体ルールや、実装コード・テストコードの内容を探しているとき。

## hash

- 0f2f40674b872cfab4188b38edded8d24dc9cff2b30a616b5ab88a8230363cdc

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

- `src` は cmoc の実装本体を置くルートで、共通処理・CLI 入口・サブコマンド実装をまとめる層です。
- `commons` は横断的な共通処理、`main.py` は CLI の起動点、`sub_commands` は `init` / `session` / `apply` / `review` 系の本体実装への入口です。
- この目次は `src` 配下の役割分担を把握し、必要な詳細モジュールへ素早く辿るために使います。

## Read this when

- `src` 配下にどの実装入口があるかを俯瞰したいとき。
- 共通処理、CLI エントリーポイント、サブコマンド実装の配置を素早く確認したいとき。
- `src/commons`、`src/main.py`、`src/sub_commands` のどこへ進むべきかを判断したいとき。

## Do not read this when

- `src/commons` や `src/sub_commands` の中の個別モジュール仕様だけを確認したいとき。
- CLI の引数定義や実行順だけを見たいときは、`src/main.py` や各サブコマンド本体を直接読むべきとき。
- `src` 全体の入口ではなく、特定の 1 ファイルや 1 パッケージの実装詳細を追いたいとき。

## hash

- 511bdfaee6aca16083fd560a5a444cb2af5021813f571eb6151fc093460b49b4

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

- `cmoc` の pytest テスト群をまとめるディレクトリです。
- `conftest.py` による import path 設定と、`test_codex.py`・`test_repo.py`・`test_indexing.py`・`test_subcommands.py` などの個別テストが入っています。
- CLI の制御ロジック、git リポジトリ共通処理、INDEX 生成、タイムスタンプ、ファイル命名規則を回帰確認するための入口です。

## Read this when

- `tests` 配下の pytest 群が何を検証しているか俯瞰したいとき
- `conftest.py` や各 `test_*.py` が対象にしている共通処理・CLI 挙動・INDEX 更新ロジックを確認したいとき
- 新しい機能追加や挙動変更に対して、どのテストを追加・修正すべきか判断したいとき

## Do not read this when

- cmoc の利用手順やサブコマンド仕様だけを確認したいとき
- `oracles` 配下の正本仕様や `INDEX.md` の生成ルールそのものを確認したいとき
- テスト共通設定ではなく、`src` 側の実装ロジックだけを追いたいとき

## hash

- e3f1ea731e40fe07d5823f6ba6050a0baa1bceed317853d21cd0063f3fb06e3b
