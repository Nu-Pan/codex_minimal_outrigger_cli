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

- `oracles` 配下の入口となる目次で、各ディレクトリの役割と読むべき場面を案内する。
- `app_specs` は、`cmoc` の呼び出し方と `init` から `session` / `apply` の反復へ進む全体フローをまとめた手引きである。
- `considered_alternatives` は、採用しなかった設計案とその不採用理由をたどるための入口である。
- `dev_rules` は、Python の書き方、CLI の構成、仮想環境、テスト実装規約などの開発ルールをまとめた入口である。

## Read this when

- `cmoc` の呼び出し方法や、最初に一度だけ行う手順を確認したいとき。
- `oracles` の修正、`review oracles`、`apply`、`session` の一連の流れを俯瞰したいとき。
- `cmoc` を使った日常の開発フローを、人間と AI の役割分担込みで理解したいとき。
- `cmoc` 全体のコーディング規則、設計方針、開発環境、テスト規約をまとめて確認したいとき。
- `src` と `tests` に実装を書く前に、共通の開発ルールを整理したいとき。

## Do not read this when

- 個別サブコマンドの引数や状態遷移など、特定の仕様断片だけを確認したいとき。
- `PATH` 設定や作業フローではなく、`branch_model` や `error_handling` などの共通仕様だけを確認したいとき。
- 実装コードやテストコードの修正だけで足りるとき。

## hash

- 3a562f250264740314cdf260da440ecfd82ed2b5f81445b92a6a9c88d789c2ab

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

- `cmoc` の実装コードをまとめるルートディレクトリです。
- `main.py` に CLI 起動とサブコマンド登録、`commons` に共通処理、`sub_commands` に各サブコマンド実装があります。
- この目次は、実行入口と共通基盤、個別サブコマンドのどこを読むべきかを素早く振り分けるための案内です。

## Read this when

- `cmoc` の起動入口やサブコマンド登録を追いたいときに読むべきです。
- 共通処理、エラー整形、git / session 操作などの実装の所在を探したいときに読むべきです。
- `apply` / `session` / `review` 系の実装本体へ最短でたどりたいときに読むべきです。
- `src` 配下の各領域の役割分担を俯瞰してから詳細ファイルを読む前段として使うべきです。

## Do not read this when

- 個別サブコマンドの引数や状態遷移などの詳細仕様を確認したいときは、このディレクトリではなく `src/sub_commands` を直接読むべきです。
- 共通ユーティリティだけを掘りたいときは、このディレクトリではなく `src/commons` を直接読むべきです。
- `cmoc` の利用手順や運用フロー全体を知りたいだけなら、このディレクトリではなく `oracles/app_specs` を読むべきです。
- テスト実装を探しているときは、このディレクトリではなく `tests` を見るべきです。

## hash

- 057fb02c3cfdc079d89dc626d03dcfc0ba5de3d206a1644cb3e71dcc53979c04

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

- `conftest.py` は pytest 共通設定として `<cmoc-root>/src` を import path 先頭へ追加します。
- `test_codex.py` は Codex CLI ラッパーの再試行、ログ出力、workspace-write 時の oracle 保護、session id 抽出を検証します。
- `test_file_naming.py` は旧ルーティングファイルの不存在と、サブコマンド実装の階層的な配置を確認します。
- `test_indexing.py` は `INDEX.md` の生成・更新、gitignore / exclude、symlink、binary、memo の扱いを回帰確認します。
- `test_repo.py` は git リポジトリ共通処理、oracle / implementation 列挙、session state、差分検出を検証します。
- `test_subcommands.py` は CLI 入口と `init` / `session` / `apply` / `eval-oracles` の制御ロジックを確認します。
- `test_timestamps.py` は timestamp 形式と duration 表示の書式を確認します。
- 全体として、一時 git リポジトリ・monkeypatch・capsys を使い、CLI の副作用と回帰ポイントをまとめて守るテスト群です。

## Read this when

- `tests` 配下の役割分担や、どのテストが何を守っているかを確認したいとき。
- `INDEX.md` 生成・更新、repo/oracle 判定、Codex CLI 呼び出し、サブコマンド起動の回帰観点を確認したいとき。
- pytest 共通設定や、時刻・経過時間表示などの補助仕様を確認したいとき。

## Do not read this when

- `src` の実装ロジックそのものを追いたいとき。
- `oracles` 配下の正本仕様を確認したいとき。
- `README.md`、`AGENTS.md`、`memo` の運用や編集可否だけを確認したいとき。
- 個別機能の詳細だけを知りたいときは、対応する `src` や `oracles` を直接読むべきです。

## hash

- da682faab6ebf555e7db267f58b7a53a1402c1f91600fc770caf3b21a63561ba
