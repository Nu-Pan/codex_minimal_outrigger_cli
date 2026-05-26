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

- `oracles` 配下全体の入口です。`app_specs`、`dev_rules`、`considered_alternatives` への案内をまとめます。
- `cmoc` の仕様断片を読む前に、どの系統の文書へ進むべきかを切り分けるための目次です。
- 個別の仕様本文ではなく、ルーティングの起点として使う文書です。

## Read this when

- `oracles` 配下のどこへ進むべきかを最初に整理したいとき。
- `cmoc` の仕様断片、開発ルール、採用しなかった代替案のどれを読むべきか判断したいとき。
- `INDEX.md` から各ディレクトリの正本仕様へたどる入口が欲しいとき。

## Do not read this when

- `cmoc` の個別仕様や実装方針を直接確認したいときは、各配下の `INDEX.md` や該当の本文を直接読むべきです。
- `app_specs`、`dev_rules`、`considered_alternatives` のうち、読む先がすでに分かっているときは、この入口を経由する必要はありません。
- 実装コードやテストコードだけで足りる場合は、このルーティング文書を読む必要はありません。

## hash

- 6a41525d345331ff006b1920ffbacdca1b0509c3a41e508a98fe02f3f46471ff

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

- `cmoc` の実装コードをまとめるソースルートです。
- `src/main.py` が CLI エントリーポイント、`src/commons` が共通基盤、`src/sub_commands` が各サブコマンド本体です。
- 共通処理やサブコマンド実装の入口をたどるときの起点になります。

## Read this when

- CLI の起動経路やトップレベルのルーティングを確認したいとき。
- 共通ユーティリティやサブコマンド本体の責務分担を整理したいとき。
- どの実装ファイルへ進むべきかを、`src` 配下の構成から判断したいとき。

## Do not read this when

- 仕様本文や運用ルールだけを確認したいときは `oracles` 側を読むべきです。
- テスト実装だけを確認したいときは `tests` 側を読むべきです。
- 個別の関数やコマンドの細部だけを確認したいときは、対応する `src/main.py`、`src/commons`、`src/sub_commands` の個別ファイルを直接読むべきです。
- README やメモ類の確認だけが目的なら、このディレクトリの目次は不要です。

## hash

- 09e7a9387400d0ca2ceca717dc79d0f72bbb2ce110e83ac640ba618f8ecbd8e2

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

- `tests` 配下の pytest 自動テスト群の入口で、各テストファイルが何を検証するかをまとめる。
- `conftest.py` は `<cmoc-root>/src` を import path に追加し、テストから本体モジュールを直接 import できるようにする。
- `test_codex.py` は `commons.codex.run_codex_exec()` の Structured Output、再試行、ログ通知、`--resume` などを検証する。
- `test_file_naming.py` は旧ルーティングファイル `routing.md` / `ROUTING.md` が残っていないことを確認する。
- `test_indexing.py` は `commons.indexing.maintain_indexes` の `INDEX.md` 生成・更新、gitignore、空ディレクトリ、バイナリ除外などを確認する。
- `test_repo.py` は `commons.repo` の git 共有処理、`.cmoc` の ignore、oracle / 実装ファイル列挙、session state を検証する。
- `test_subcommands.py` は `init`、`session`、`apply`、`eval-oracles`、`main` の CLI 制御ロジックを検証する。
- `test_timestamps.py` はタイムスタンプ生成と経過時間表示の書式を検証する。

## Read this when

- `tests` 配下でどの機能がどのテストに対応しているかを素早く把握したいとき。
- `src` 側の変更がどのテスト群に影響するか見極めたいとき。
- `INDEX.md` やルーティング文書の更新がテスト観点で妥当か確認したいとき。
- `cmoc` の CLI、git 共有処理、インデックス生成、時間表示の回帰テストを探したいとき。

## Do not read this when

- 個別の実装ロジックだけを追いたいときは、この目次ではなく `src` 側の本体コードを読むべきです。
- `oracles` の正本仕様そのものを確認したいときは、この目次ではなく `oracles` 配下の該当文書を読むべきです。
- 特定のテストケースの詳細な期待値だけを見たいときは、対応する `tests/test_*.py` を直接読むべきです。
- `README.md`、`AGENTS.md`、`memo` の運用や編集可否だけを確認したいときは、このテスト目次ではなく別の案内を参照すべきです。

## hash

- b50e0b2ac7891d92572fba7f20a8225711561fa99aa3eb8468b15da80d861d7a
