# `AGENTS.md`

## Summary

- `AGENTS.md` は、cmoc（Codex Minimal Outrigger CLI）開発リポジトリにおける作業上の基本規則を定義する文書です。
- `<cmoc-root>` と `<repo-root>` の意味を明確に分け、cmoc 自体の開発と cmoc を用いた開発を混同しないよう指示しています。
- AI が閲覧・編集してはいけないファイル、および編集してはいけないファイルを列挙しています。
- 正本仕様断片である `<cmoc-root>/oracles` の扱いと、仕様調査時に `INDEX.md` を起点として最低限必要なファイルだけを読むルーティング方針を示しています。
- 実装は `<cmoc-root>/src`、自動テストは `<cmoc-root>/tests` に置くことを定めています。

## Read this when

- このリポジトリで作業を始める前に、最初に読む必要があります。
- `<cmoc-root>`、`<repo-root>`、cmoc 自体の開発、cmoc を用いた開発の違いを確認したいときに読んでください。
- AI が読んではいけないファイル、編集してはいけないファイルを確認したいときに読んでください。
- `oracles` 配下の正本仕様断片を調べる際の入口や読み方を確認したいときに読んでください。
- 実装ファイルやテストファイルをどこに置くべきか確認したいときに読んでください。

## Do not read this when

- cmoc の詳細な仕様断片そのものを確認したいときは、ここではなく `<cmoc-root>/oracles/INDEX.md` から必要な仕様ファイルへ進んでください。
- 既に作業規則を把握しており、特定機能の実装詳細だけを確認したいときは、関連する `src` や `tests` のファイルを読んでください。
- README の利用者向け説明や導入手順を確認したいときは、この文書ではなく README を参照してください。

## hash

- b2f93d440fb91234a2ff90e3b533ff1ba9230037690851040d4d8e5de5d0bf37

# `README.md`

## Summary

- Codex Minimal Outrigger CLI、略称 cmoc のリポジトリ README です。
- AI 向けには詳細な作業ルールを `AGENTS.md` で確認するよう案内しています。
- cmoc は Codex CLI を用いた開発を補助する最小限度の外部ツールであることを説明しています。
- リポジトリの clone、Python 仮想環境作成、編集可能インストール、任意の PATH 設定という初期セットアップ手順を示しています。
- 基本ワークフローの詳細は `<cmoc-root>/oracles/app_specs/usage.md` を参照するよう案内しています。

## Read this when

- cmoc リポジトリの概要を短く把握したいとき。
- cmoc が何をするツールか、正式名称と略称を確認したいとき。
- cmoc の初期セットアップ手順を確認したいとき。
- clone 後に Python 仮想環境を作成し、`<cmoc-root>/.venv/bin/python -m pip install -e .` で開発用インストールする手順を知りたいとき。
- `cmoc` コマンドを実行しやすくするために `bin` を PATH に追加する例を確認したいとき。
- cmoc の基本ワークフロー仕様がどの oracle ファイルにあるか知りたいとき。

## Do not read this when

- cmoc 自体の詳細な開発ルール、ファイルアクセス規則、編集禁止ファイル、作業時の注意点を確認したいとき。
- cmoc のサブコマンド仕様、Codex CLI 連携、出力形式、エラー処理などの正本仕様断片を調べたいとき。
- cmoc の Python 実装方針、設計規約、テスト規約、開発環境ルールを詳しく確認したいとき。
- `src` や `tests` 配下の具体的な実装・テスト構造を調べたいとき。
- cmoc を使った対象リポジトリ側の作業手順や、branch、apply、merge、oracle 評価などの詳細ワークフローを確認したいとき。
- README.md を編集する必要があるとき。

## hash

- c9f160c5a2a14b1dece67dd6f263b3b59a8e586f606eeac39d5ac2239a75d3ff

# `ROUTING.md`

## Summary

- リポジトリ直下の主要パスへのルーティング情報を箇条書きでまとめている。
- `<cmoc-root>/bin`、`<cmoc-root>/src`、`<cmoc-root>/oracles/docs` 配下の旧ドキュメント群について、用途や配置先を短く説明している。
- cmoc の公開バイナリ、ソース配置、旧仕様ドキュメントの所在を素早く把握するための入口となる。

## Read this when

- リポジトリ直下で、どのディレクトリや旧ドキュメントを見ればよいか大まかに判断したいとき。
- `bin` や `src` の役割を短く確認したいとき。
- `oracles/docs/app_spec.md`、`code_design.md`、`coding_rule.md`、`development_environment.md` など旧ドキュメント名から目的の文書を探したいとき。
- cmoc の実装ファイルや公開用バイナリの配置先を確認したいとき。

## Do not read this when

- cmoc の正本仕様を調べるために、現在の `oracles/INDEX.md` からルーティングすべきとき。
- サブコマンド仕様、Codex CLI 連携、出力、エラー処理などの詳細なアプリケーション仕様を確認したいとき。
- Python 実装規約、テスト規約、開発環境などの詳細な開発ルールを確認したいとき。
- README、AGENTS、oracles、memo などの編集可否やファイルアクセス制約だけを確認したいとき。

## hash

- 198999eb3bcc5ffd76844a04b55e0ff819f1aadb645b7d54b19c56af6b5a4bb0

# `bin`

## Summary

- Contains the repository-local executable launcher for the cmoc command.
- The `cmoc` Bash script resolves `<cmoc-root>` from its own location and execs `<cmoc-root>/.venv/bin/python` with `<cmoc-root>/src/main.py`, forwarding all CLI arguments.
- `INDEX.md` provides routing metadata for the executable launcher file in this directory.

## Read this when

- You need to understand how invoking `bin/cmoc` starts the Python implementation.
- You are debugging startup failures before `src/main.py` runs, such as incorrect root detection, missing `.venv/bin/python`, executable permissions, or argument forwarding.
- You are changing local command shim behavior, packaging assumptions, or development workflows that rely on the `bin/cmoc` launcher.
- You need routing metadata for files directly under `<cmoc-root>/bin`.

## Do not read this when

- You need the implementation of cmoc subcommands, CLI workflow logic, prompts, or runtime behavior after Python startup; read files under `<cmoc-root>/src` instead.
- You are looking for automated tests; read `<cmoc-root>/tests` instead.
- You need canonical application or development rules; use `<cmoc-root>/oracles/INDEX.md` to route to the relevant specification fragments.
- You are working on README, repository policy, or documentation unrelated to the executable launcher.

## hash

- ca4ac1558575ac1351b53f96c54f72907f00310e5a93d8ba58dd9223eb4a1006

# `codex_minimal_outrigger_cli.code-workspace`

## Summary

- VS Code workspace configuration for opening the cmoc repository root as a single workspace folder.
- Defines editor file exclusion settings for generated Python cache directories and package metadata directories.
- Contains workspace-level settings only; it does not describe cmoc runtime behavior, implementation architecture, or tests.

## Read this when

- You need to understand how the repository is configured when opened as a VS Code workspace.
- You are checking why `__pycache__` directories or `*.egg-info` paths are hidden in the editor file explorer.
- You are updating or auditing workspace-specific VS Code settings for this repository.

## Do not read this when

- You need cmoc application specifications, CLI behavior, subcommand workflows, or oracle routing information.
- You need implementation details from `src` or test details from `tests`.
- You are looking for repository development rules, file access restrictions, or authoritative specification fragments under `oracles`.
- You are not using VS Code workspace metadata or editor-specific configuration.

## hash

- 6acff2a397cd0c66553c35c5c3f0f45a551ed34bcae704aa612b4b485cce20d0

# `oracles`

## Summary

- `oracles/INDEX.md` は、cmoc の正本仕様断片群の最上位ルーティング文書です。
- アプリケーション実行時仕様を扱う `app_specs` と、cmoc 自体の開発ルールを扱う `dev_rules` への入口を提供します。
- `app_specs` は Codex CLI 連携、コンソール出力、共通エラーハンドリング、対象リポジトリ探索、`.cmoc` 管理、タイムスタンプ、`INDEX.md` 自動メンテナンス、各サブコマンド仕様、利用者向けワークフローを調べるための仕様ディレクトリです。
- `dev_rules` は Python 実装規約、CLI 設計規約、共通処理配置、開発環境、pytest や Fake Codex CLI を含むテスト規約など、cmoc 開発者向けルールを調べるための仕様ディレクトリです。
- cmoc の仕様調査では、このファイルを起点に、目的に応じて `app_specs/INDEX.md` または `dev_rules/INDEX.md` へ進みます。

## Read this when

- cmoc の正本仕様断片を調べ始めるとき。
- アプリケーション仕様と開発者向けルールのどちらを読むべきか判断したいとき。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` などのユーザー向け CLI 挙動やワークフロー仕様への入口を探しているとき。
- Codex CLI 呼び出し、Structured Output、ログ保存、リトライ、stdout 表示、共通エラー処理、終了ステータスなど、cmoc 実行時仕様への入口を探しているとき。
- `<repo-root>` 探索、oracle ファイル列挙、`.cmoc` 管理、タイムスタンプ、対象リポジトリ側 `INDEX.md` 自動メンテナンスなど、サブコマンド横断仕様への入口を探しているとき。
- cmoc 自体の `src` 実装、CLI 構成、共通処理、開発環境、テスト規約を確認するために、開発者向け仕様の場所を知りたいとき。

## Do not read this when

- 読むべき個別仕様ファイルまたは下位 `INDEX.md` が既に明確で、最上位の振り分け情報が不要なとき。
- cmoc の実装コードそのものを直接読みたいだけで、仕様断片のルーティングが不要なとき。
- 対象が cmoc ではなく、cmoc を用いて開発する別リポジトリの固有仕様だけであるとき。
- Codex CLI、git、pytest、Python などの一般的な使い方だけを調べており、cmoc 固有仕様が不要なとき。
- README、AGENTS、memo などのリポジトリ運用上のファイルアクセス制約だけを確認したいとき。

## hash

- adfd35a0932d9643e66db9f5283c9457680c866a5511f8c16ff9e0e3fbe0daf7

# `pyproject.toml`

## Summary

- `pyproject.toml` は cmoc の Python パッケージ設定とビルド設定を定義するファイルです。
- プロジェクト名、バージョン、説明、対応 Python バージョン、依存関係として `pytest` と `typer` を指定しています。
- CLI エントリーポイントとして `cmoc = "main:main"` を登録し、`src` 配下の `main.py` を単一モジュールとしてパッケージ化する設定を含みます。
- setuptools をビルドバックエンドに使い、`src` 配下のパッケージ探索と、`sub_commands` パッケージデータとして `eval-oracles.py` を含める設定を持ちます。

## Read this when

- cmoc のインストール可能な Python パッケージ設定、ビルドバックエンド、setuptools 設定を確認したいとき。
- `cmoc` コマンドがどの Python 関数に接続されているか確認したいとき。
- 依存ライブラリや必要 Python バージョンを確認・変更する必要があるとき。
- `src` 配下のモジュールやパッケージがどのように配布対象へ含まれるか調べたいとき。
- `sub_commands/eval-oracles.py` のようなパッケージデータの同梱設定を確認したいとき。

## Do not read this when

- cmoc のサブコマンドごとの実行時仕様やユーザー向けワークフローを調べたいとき。
- Python コードの具体的な実装ロジックやテストケースの中身を確認したいとき。
- README、AGENTS、oracles、memo などのリポジトリ運用ルールや編集可否だけを確認したいとき。
- cmoc を使って開発する対象リポジトリ側の設定や仕様を調べたいとき。
- 依存関係やパッケージングではなく、CLI の stdout、エラーハンドリング、Codex CLI 呼び出し仕様を確認したいとき。

## hash

- 74bf4b55ac8815e2d09f225da7f6100ac02ed92e46bc4bb1ebe77c61f049c5f3

# `src`

## Summary

- `/home/happy/codex_minimal_outrigger_cli_stage1/src` は cmoc の Python 実装を置くルートディレクトリです。
- `main.py` は Typer ベースの CLI エントリーポイントで、`init`、`branch`、`eval-oracles`、`apply`、`merge` を登録し、実処理を `sub_commands` 配下へ委譲します。
- `commons` はサブコマンド間で共有される基盤処理のパッケージで、Codex CLI 呼び出し、Structured Output 検証、`INDEX.md` 自動メンテナンス、git リポジトリ操作、`.cmoc` 管理、共通エラー整形、実行ラッパー、タイムスタンプ生成、時間計測を扱います。
- `sub_commands` は cmoc の各サブコマンド本体実装を集約するパッケージで、初期化、作業ブランチ作成、oracle 評価、oracle 反映、マージ処理をファイル単位で分担します。
- `codex_minimal_outrigger_cli.egg-info` は Python パッケージング用の生成メタデータで、配布名、依存関係、エントリーポイント、ソース一覧などを含みます。
- `__pycache__` 配下のファイルは Python 実行時に生成される bytecode キャッシュであり、通常の実装調査や仕様確認の対象ではありません。

## Read this when

- cmoc の実装コード全体で、CLI 入口、共通処理、個別サブコマンド実装のどこを読むべきか判断したいとき。
- 新しいサブコマンドを追加する、既存サブコマンドの登録を変更する、または Typer のトップレベル引数・オプション定義を確認したいとき。
- `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc apply`、`cmoc merge` の実装ファイルへの入口を探しているとき。
- Codex CLI 連携、Structured Output、`INDEX.md` 自動メンテナンス、git 操作、`.cmoc` 管理、共通エラー処理、タイムスタンプ、時間計測など、サブコマンド横断の helper 実装を探しているとき。
- cmoc の Python パッケージ構成、CLI エントリーポイント、依存関係メタデータ、生成済みキャッシュの位置関係を把握したいとき。
- `src` 配下を修正する前に、変更対象が `main.py`、`commons`、`sub_commands`、パッケージング生成物のどれに属するか切り分けたいとき。

## Do not read this when

- cmoc の正本仕様断片を確認したいとき。仕様調査では `/home/happy/codex_minimal_outrigger_cli_stage1/oracles/INDEX.md` から必要な仕様ファイルへ辿る必要があります。
- cmoc 自体ではなく、cmoc を用いて開発する対象リポジトリ側の実装や `<repo-root>` 側のファイル構成を調べたいとき。
- README、AGENTS、oracles、memo などの編集可否やリポジトリ運用ルールだけを確認したいとき。
- 自動テストの fixture、Fake Codex CLI、pytest の期待値、テストケース配置を調べたいとき。テスト側は `tests` 配下を読むべきです。
- Codex CLI、git、Typer、Click、JSON Schema、Python packaging など外部技術の一般的な使い方だけを知りたいとき。
- `__pycache__` や egg-info などの生成物を通常の手書き実装として読もうとしているとき。

## hash

- ed6d9d5314184de1f41f166982f23ff61d3a702b46972dca26a2270ce283c0ae

# `test.sh`

## Summary

- `test.sh` は、シェル環境の `PATH` 先頭に `/home/happy/codex_minimal_outrigger_cli_stage0/bin` を追加するための短い環境設定スクリプトです。
- cmoc のテストや手動確認で、現リポジトリではなく stage0 側の `bin` 配下にあるコマンドを優先して参照したい場合の入口になります。

## Read this when

- `test.sh` を source したときに `PATH` がどのように変わるか確認したいとき。
- テスト実行や手動検証で、どの cmoc コマンド実体が優先的に呼び出されるかを確認したいとき。
- stage0 の `bin` ディレクトリを使う前提のローカル環境設定を調べたいとき。

## Do not read this when

- cmoc のサブコマンド仕様や正本仕様断片を調べたいとき。
- cmoc 本体の Python 実装、設計規約、テスト規約を調べたいとき。
- 通常のテストケース内容や pytest の期待結果を確認したいとき。
- stage0 の実装内容や `bin` 配下の個別コマンドの挙動を調べたいとき。

## hash

- 0ca9877993ee802249d52f98317a029f6b9f5e32a4ff92729fd78d983ced47a3

# `tests`

## Summary

- cmoc 自体の pytest ベース自動テストを収めるディレクトリです。
- `conftest.py` は `<cmoc-root>/src` を import path に追加し、テストから実装モジュールを直接 import できるようにします。
- `test_codex.py` は `commons.codex.run_codex_exec` の Codex CLI 呼び出し、Structured Output、JSON/schema/意味的バリデーション失敗時のリトライ、ログ出力、INDEX メンテナンス連携を検証します。
- `test_indexing.py` は `commons.indexing.maintain_indexes` による `INDEX.md` 自動生成・更新、gitignore 除外、空ディレクトリ、build/tmp、memo、既存エントリ再生成、Structured Output リトライ、自動コミット範囲を検証します。
- `test_repo.py` は `commons.repo` の git リポジトリ探索、`.cmoc` ignore 保証、oracle ファイル列挙、変更 oracle 抽出、oracle 削除検出、未コミット差分制約、cmoc ブランチ判定、base commit 記録先を検証します。
- `test_subcommands.py` は `cmoc init`、`branch`、`eval-oracles`、`apply`、`merge` と Typer エントリーポイント周辺の決定論的制御ロジックを、主に一時 git リポジトリと monkeypatch で検証します。
- `test_timestamps.py` は `commons.timestamps.make_timestamp` が `YYYY-MM-DD_HH-MM_SS_mmm` 形式のゼロ埋めタイムスタンプを生成することを検証します。

## Read this when

- cmoc 自体のテスト全体の配置と、どのテストファイルを読むべきか判断したいとき。
- `run_codex_exec`、Structured Output、Codex CLI 呼び出しログ、リトライ、INDEX メンテナンス連携の回帰テストを確認したいとき。
- `INDEX.md` 自動メンテナンスの対象選定、除外規則、再生成条件、Structured Output schema、自動コミットのテストを確認したいとき。
- git リポジトリ共通処理、`.cmoc` 管理、oracle ファイル列挙・差分抽出、cmoc ブランチ判定の期待挙動をテスト側から調べたいとき。
- `init`、`branch`、`eval-oracles`、`apply`、`merge` などサブコマンド実装を変更し、既存テストが期待する終了条件、ファイル生成、commit、エラー条件を確認したいとき。
- pytest の import path 設定、一時 git リポジトリ作成、fake Codex CLI、monkeypatch、`pytest.raises` など、このリポジトリのテストパターンを参照したいとき。
- タイムスタンプ文字列形式の仕様や、`make_timestamp` の期待値を確認したいとき。

## Do not read this when

- cmoc のユーザー向け CLI 仕様や正本仕様断片だけを調べたいとき。この場合は `<cmoc-root>/oracles/INDEX.md` から必要な仕様へ辿るべきです。
- cmoc の実装本体を直接読みたいとき。この場合は `<cmoc-root>/src` 配下の該当モジュールを読むべきです。
- README、AGENTS.md、oracles、memo などのリポジトリ運用ルールや閲覧・編集可否だけを確認したいとき。
- cmoc を使って開発する対象リポジトリ側、つまり `<repo-root>` のファイル構造や仕様を調べたいとき。
- pytest や git の一般的な使い方だけを知りたいとき。
- `__pycache__` 配下の生成済みバイトコードや、テスト実行時のキャッシュ内容を確認したいだけのとき。

## hash

- bc89180c9363dc9ab30f8fc7fd94aa19c68056ccaa777eea7eb70c980fb3e62f
