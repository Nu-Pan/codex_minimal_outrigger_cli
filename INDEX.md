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

# `bin`

## Summary

- `bin` は cmoc コマンドの起動用ファイルを置くディレクトリです。
- 主な実体は `bin/cmoc` で、シェル製の CLI エントリーポイントとして `<cmoc-root>` を解決し、`<cmoc-root>/.venv/bin/python` で `<cmoc-root>/src/main.py` を実行します。
- `bin/cmoc` は仮想環境 Python が存在し実行可能な場合、受け取った全引数を `src/main.py` に渡して `exec` します。
- 仮想環境 Python が見つからない、または実行できない場合は、日本語の構造化エラー、復旧用セットアップ手順、必要な実行ファイル、簡易 Call stack を表示して終了ステータス 1 で終了します。
- `bin/INDEX.md` は `bin/cmoc` へのルーティング情報を記載する目次ファイルです。
- `bin/__pycache__` は Python 実行時に生成されるキャッシュ領域であり、通常の仕様確認や実装確認では読む必要はありません。

## Read this when

- cmoc コマンドを起動したときに、最初にどのファイルが実行されるか確認したいとき。
- `bin/cmoc` から `<cmoc-root>/src/main.py` へどのように処理が渡るか調べたいとき。
- cmoc が使用する Python 実行ファイルとして `<cmoc-root>/.venv/bin/python` が前提になっているか確認したいとき。
- 仮想環境が未作成、削除済み、または実行不能な場合のエラー表示や終了ステータスを確認したいとき。
- cmoc の PATH 配置や CLI ラッパーとしての `bin/cmoc` の役割を調べたいとき。
- `bin` 配下で読むべき通常のファイルが `bin/cmoc` であることを判断したいとき。

## Do not read this when

- cmoc の各サブコマンドの具体的な仕様や処理内容を調べたいとき。
- Python 側のコマンドディスパッチ、共通処理、サブコマンド実装を調べたいとき。
- cmoc の自動テスト、Fake Codex CLI、pytest の規約やテストケースを確認したいとき。
- `<repo-root>` 側に生成される `INDEX.md`、`.cmoc`、oracle 評価結果などの仕様を調べたいとき。
- Python パッケージ構成、依存関係、仮想環境作成以外の開発環境ルールを確認したいとき。
- Python キャッシュや生成物の中身を調べたいだけのとき。

## hash

- 670c4146f37c39ca4785c462cbfb31ad730ef6d03952fdf7e4b91474fa2a6264

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

- `oracles` 配下の仕様断片へ案内するルーティング用 INDEX です。
- `cmoc` の実行時仕様として、`codex exec` の呼び出し規約、プロンプト構成、サンドボックス、Model / Reasoning Effort、Structured Output、ログ規則、共通エラーハンドリングをまとめる入口を含みます。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` などの個別仕様への入口をまとめています。
- 採用しなかった設計案や運用案の背景も、別ディレクトリとして案内します。
- `cmoc` 自体の開発ルールとして、Python のコーディング規約、設計方針、開発環境、pytest などのテスト規約への入口も含みます。

## Read this when

- `cmoc` の実行時仕様について、どの個別仕様ファイルやサブディレクトリを読むべきか判断したいとき。
- `codex exec` の呼び出し方法、プロンプト構成、サンドボックス指定、Model / Reasoning Effort、Structured Output、ログ保存、リトライ方針を確認したいとき。
- 標準出力、ファイルログ、進捗表示、経過時間表示の規則を確認したいとき。
- 共通エラーハンドリングや終了ステータスの扱いを確認したいとき。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` の個別仕様への入口が必要なとき。

## Do not read this when

- `cmoc` 自体の Python コーディング規約、設計規約、テスト規約、開発環境など、開発者向けルールだけを調べたいとき。
- `cmoc` の具体的な実装コードやテストコードの場所、ファイル構造、実装パターンだけを調べたいとき。
- 特定のサブコマンド仕様が既に明確で、このディレクトリ全体のルーティング情報が不要なとき。
- `README.md`、`AGENTS.md`、`oracles`、`memo` などの編集可否や運用ルールだけを確認したいとき。

## hash

- 3ebcd833085506b1cc391a4cb6dfbd75fbad48c2da7326758f3d62139fc8d554

# `pyproject.toml`

## Summary

- `pyproject.toml` は `codex-minimal-outrigger-cli` のパッケージメタデータ、実行環境、依存関係、CLI エントリーポイント、ビルド設定を定義するファイルです。
- `cmoc` コマンドがどの Python モジュール・関数に接続されるか、また `src` レイアウトをどう扱うかを確認する入口です。
- 依存追加、Python 要件変更、ビルドバックエンド変更、パッケージ探索設定変更に関わる判断の起点になります。

## Read this when

- cmoc のパッケージ名、バージョン、説明、要求 Python バージョンを確認したいとき。
- 実行時または開発時の Python 依存関係を確認したいとき。
- `cmoc` コマンドのエントリーポイントがどの関数に紐づくか調べたいとき。
- ビルドシステム、setuptools 設定、`src` レイアウト、`main` モジュールの扱いを確認したいとき。
- 依存追加や CLI 起動点の変更を行う前に、パッケージ設定全体を把握したいとき。

## Do not read this when

- cmoc のサブコマンド仕様や正本仕様断片へのルーティングを調べたいとき。
- `src` 配下の実装コードの具体的な処理内容だけを確認したいとき。
- `tests` 配下のテストケースや Fake Codex CLI の詳細を調べたいとき。
- README、AGENTS、oracles、memo などの運用ルールや編集可否だけを確認したいとき。
- cmoc を使って開発する別リポジトリ側の `<repo-root>` の設定やファイル構成を調べたいとき。

## hash

- c20014553a4e48f3a2f9f5221852179231c76594ccc1bc4c82b8dddc651b203e

# `routing.md`

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

# `src`

## Summary

- `src` は cmoc の実装本体をまとめるルートディレクトリです。
- `main.py` は `cmoc` CLI のエントリーポイントとサブコマンド登録を担います。
- `commons` は `codex exec` 呼び出し、エラー処理、repo 操作、ログ、タイムスタンプ、経過時間計測などの共通基盤をまとめます。
- `sub_commands` は `init`、`branch`、`apply`、`eval-oracles`、`merge` の各サブコマンド実装本体をまとめます。

## Read this when

- `src` 配下で、どのファイルがどの役割を持つかを大づかみに確認したいとき。
- CLI の起点である `main.py` から、各サブコマンド実装への委譲関係を追いたいとき。
- 共通処理を探していて、`commons` 配下のどのモジュールを読むべきか切り分けたいとき。
- 各サブコマンド本体を探していて、`sub_commands` 配下のどの実装ファイルを読むべきか判断したいとき。
- `src` 全体の構成を把握してから、個別モジュールの詳細に進みたいとき。

## Do not read this when

- `oracles` 側の正本仕様そのものや、個別仕様断片だけを確認したいとき。
- cmoc の開発ルール、テスト規約、開発環境など、実装以外の方針だけを調べたいとき。
- 特定モジュールの実装詳細だけを追いたくて、ディレクトリ全体の案内が不要なとき。
- README や AGENTS などの運用ルールだけを確認したいとき。

## hash

- 415cacc196a40fe55ce3a19d7b0926575543b18166d9ac944b7f0d9034a40704

# `test.sh`

## Summary

- `test.sh` は、cmoc 開発リポジトリのルートパスを `CMOC_ROOT` として設定し、ローカルの仮想環境 `.venv/bin` と `bin` を `PATH` の先頭に追加するためのシェル設定断片です。
- このファイル自体はテスト実行ロジックを含まず、cmoc のローカル開発・検証で使用するコマンド探索パスを整える役割を持ちます。

## Read this when

- cmoc のローカル開発環境で、どのパスが `PATH` に追加されるか確認したいとき。
- `cmoc` コマンドや仮想環境内の実行ファイルが、テストや手元実行時にどの順序で解決されるか調べたいとき。
- 開発リポジトリの絶対パスを前提にした簡易的な環境設定スクリプトの内容を確認したいとき。

## Do not read this when

- cmoc のサブコマンド仕様、Structured Output、oracle 評価、マージ処理などのアプリケーション仕様を調べたいとき。
- cmoc の Python 実装、設計規約、テスト規約、個別テストケースの内容を調べたいとき。
- 実際の自動テストの手順、pytest の設定、Fake Codex CLI の挙動を確認したいとき。
- リポジトリ運用上の編集禁止ファイルや AI アクセス制限を確認したいとき。

## hash

- 6fc07bc0dff2b064245772154c4f103ce2d3d0cbe7536ae9124eb49e183c6b44

# `tests`

## Summary

- `tests` は cmoc の自動テスト群の目次で、pytest による決定論的な制御ロジック検証の入口です。
- `conftest.py` は `src` を import path 先頭に追加する共通設定です。
- `test_codex.py` は Codex CLI 呼び出しラッパー、Structured Output、再試行、ログ出力を検証します。
- `test_indexing.py` は `INDEX.md` の自動メンテナンス、再生成、対象ファイル判定を検証します。
- `test_repo.py` は git リポジトリ共通処理、`.cmoc` ignore、差分検出、削除判定を検証します。
- `test_subcommands.py` は CLI 入口と各サブコマンドの制御ロジックを検証します。
- `test_timestamps.py` は timestamp と経過時間表示のフォーマットを検証します。
- `test_file_naming.py` はルーティングファイル名の命名規則を検証します。

## Read this when

- pytest で `src` 配下モジュールを直接 import できる共通設定を確認したいとき。
- `commons.codex` の呼び出し、ログ、JSON 再試行、quota 関連のテストを探したいとき。
- `INDEX.md` の自動生成・再生成・空ディレクトリ処理・対象除外のテストを探したいとき。
- `.cmoc` の ignore、oracle / implementation ファイル列挙、差分検出、削除判定のテストを探したいとき。
- CLI 入口、各サブコマンド、エラーハンドリング、進捗表示のテストを探したいとき。
- timestamp や duration の表示形式、ルーティングファイル名の規則を確認したいとき。

## Do not read this when

- cmoc の正本仕様そのものを知りたいときは `oracles` 配下を読むべきです。
- 本体実装 `src` のコード構造だけを知りたいとき。
- README、AGENTS、memo の運用ルールや編集可否だけを確認したいとき。
- テスト以外の開発ルール、設計規約、実行環境だけを確認したいとき。
- 既に対象のテストファイルが決まっていて、このディレクトリ全体の案内が不要なとき。

## hash

- 0ba195466beea585963b16ef0c4896f48f737450a85ecdaef5942a6368041b26
