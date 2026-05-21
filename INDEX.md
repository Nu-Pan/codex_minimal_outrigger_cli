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

- `oracles` 配下の正本仕様断片を全体的に案内するルーティング用ディレクトリです。
- アプリケーション実行時仕様は `app_specs` に、採用しなかった設計案は `considered_alternatives` に、開発者向けルールは `dev_rules` に分かれています。
- 各ディレクトリ内の `INDEX.md` を入口として、必要な正本仕様だけを最小限読むための起点になります。

## Read this when

- `oracles` 配下のどのディレクトリや個別ファイルを読むべきか判断したいとき。
- cmoc の実行時仕様、開発ルール、採用しなかった設計案のどれに属する話かを切り分けたいとき。
- `app_specs`、`considered_alternatives`、`dev_rules` のどれを入口にすべきか確認したいとき。
- 正本仕様断片を全体として俯瞰し、必要な情報だけへ最短で辿りたいとき。

## Do not read this when

- すでに読むべき個別の仕様ファイルが明確で、ディレクトリ全体の案内が不要なとき。
- `oracles` 配下の編集可否やリポジトリ運用ルールだけを確認したいとき。
- cmoc 自体の実装コードやテストコードの配置、具体的な実装手順だけを知りたいとき。
- 開発環境や一般的なコーディング規約だけを調べたいとき。

## hash

- 7f1ada72ab4e7054d33506ecad06100958598980e7ce9df243297c3cf097850d

# `pyproject.toml`

## Summary

- Python プロジェクト `codex-minimal-outrigger-cli` のパッケージメタデータ、実行環境、依存関係、CLI エントリーポイント、ビルドバックエンド、setuptools のパッケージ探索設定を定義するファイル。
- Python 3.12.3 以上を要求し、依存関係として `pytest` と `typer` を指定している。
- `cmoc` コマンドを `main:main` に対応付け、`src` 配下をパッケージ配置場所として扱う設定を含む。

## Read this when

- cmoc の Python パッケージ名、バージョン、説明、要求 Python バージョンを確認したいとき。
- cmoc の実行時または開発時に使う Python 依存関係を確認したいとき。
- `cmoc` コマンドがどの Python 関数をエントリーポイントとして呼び出すか調べたいとき。
- ビルドシステム、setuptools 設定、`src` レイアウト、`main` モジュールの扱いを確認したいとき。
- 依存追加、CLI エントリーポイント変更、パッケージング設定変更に関わる作業をするとき。

## Do not read this when

- cmoc のサブコマンドの詳細仕様や正本仕様断片へのルーティングを調べたいとき。
- `src` 配下の実装コードの具体的な処理内容を確認したいとき。
- `tests` 配下のテストケースや Fake Codex CLI の詳細を調べたいとき。
- README、AGENTS、oracles、memo などのリポジトリ運用ルールや編集可否だけを確認したいとき。
- cmoc を使って開発する別リポジトリ側の `<repo-root>` の設定やファイル構成を調べたいとき。

## hash

- f7e7dcdc72547ff9b03be0135915cb7c3ae47af0b596744238d91061acd8488e

# `src`

## Summary

- `src` は cmoc 本体の Python 実装を格納するディレクトリです。
- トップレベルの CLI エントリーポイントは `main.py` にあり、Typer アプリケーションを定義して `init`、`branch`、`eval-oracles`、`apply`、`merge` の各サブコマンドを登録します。
- `src/sub_commands` は各サブコマンドの本体処理を実装するパッケージで、初期化、作業ブランチ作成、oracle 評価、実装反映、マージ処理の主要フローを扱います。
- `src/commons` は複数サブコマンドから共有される共通処理をまとめたパッケージで、Codex CLI 呼び出し、INDEX.md メンテナンス、git リポジトリ操作、`.cmoc` ignore 保証、共通エラー表示、タイムスタンプ生成、ステップ時間計測を扱います。
- `__pycache__` や `codex_minimal_outrigger_cli.egg-info` は生成物・パッケージメタデータであり、通常の実装調査や仕様追跡では主要な参照先ではありません。

## Read this when

- cmoc 本体実装の入口を探し、CLI 登録、サブコマンド本体、共通処理のどこを読むべきか判断したいとき。
- `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc apply`、`cmoc merge` の実装配置を大まかに把握したいとき。
- Typer の CLI エントリーポイント、サブコマンドへの委譲、parse error や想定外例外の共通エラーレポート化を調べたいとき。
- 個別サブコマンドの処理フローを読む前に、`src/sub_commands` 配下へ進むべきか確認したいとき。
- Codex CLI 呼び出し、INDEX.md 自動メンテナンス、git 操作、`.cmoc` 管理、共通エラー、タイムスタンプ、時間計測などの横断処理を読む前に、`src/commons` 配下へ進むべきか確認したいとき。
- cmoc のテストを書くために、テスト対象となる実装モジュールの大まかな責務分担を確認したいとき。

## Do not read this when

- cmoc の正本仕様断片を調べたいとき。その場合は `oracles` 配下の `INDEX.md` から必要な仕様ファイルへ進むべきです。
- cmoc 自体の開発規約、Python コーディング規約、テスト規約、開発環境ルールだけを確認したいとき。その場合は `oracles/dev_rules` 側のルーティングを読むべきです。
- README、AGENTS、oracles、memo などの編集可否やリポジトリ運用ルールだけを確認したいとき。
- `<repo-root>` 側の oracle や実装ファイルの内容を調べたいとき。ここは cmoc 自体の `<cmoc-root>/src` 実装ディレクトリです。
- 特定サブコマンドの詳細な処理ファイルが既に明確で、トップレベルの実装配置を確認する必要がないとき。
- pytest fixture、Fake Codex CLI、テストデータなど、自動テスト側の構造だけを調べたいとき。その場合は `tests` 配下を確認するべきです。
- ビルド生成物、キャッシュ、インストール済み egg-info の中身だけを調べたいとき。通常の実装理解では `__pycache__` や `codex_minimal_outrigger_cli.egg-info` は読まなくてよいです。

## hash

- 48b45dbac33e81e77ad8c2881a625b9366a512217b8f278daee19532377c2556

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

- `tests` は cmoc 自体の pytest ベースの自動テストを配置するディレクトリです。
- サブコマンド、Codex CLI 呼び出しラッパー、INDEX.md メンテナンス、git リポジトリ共通処理、タイムスタンプ・経過時間表示、pytest import path 設定のテストを含みます。
- `test_subcommands.py` は `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc apply`、`cmoc merge`、Typer エントリーポイント、`bin/cmoc` ランチャー周辺の決定論的な制御ロジックを検証します。
- `test_codex.py` は `commons.codex.run_codex_exec` の Codex CLI 引数、Structured Output、リトライ、ログ保存、validator、quota resume、INDEX メンテナンス呼び出しを検証します。
- `test_indexing.py` は `commons.indexing.maintain_indexes` の INDEX 生成対象、除外規則、Structured Output schema、壊れた INDEX の再生成、最新判定、自動コミット範囲を検証します。
- `test_repo.py` は `commons.repo` の repo root 探索、`.cmoc` ignore 保証、oracle・実装ファイル列挙、cmoc ブランチ基準の変更・削除検出、apply 前提条件を検証します。
- `test_timestamps.py` は cmoc timestamp と stdout 用経過時間表示のフォーマットを検証し、`conftest.py` は `<cmoc-root>/src` を pytest import path に追加します。

## Read this when

- cmoc 自体の実装変更に対して、既存 pytest が固定している期待挙動や回帰範囲を確認したいとき。
- `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc apply`、`cmoc merge`、CLI エントリーポイント、ランチャーのテストを探しているとき。
- Codex CLI 呼び出し、Structured Output、JSON schema 検証、validator、リトライ、ログ保存、quota resume、進捗表示のテストを確認したいとき。
- INDEX.md 自動メンテナンスの対象ディレクトリ、除外規則、ハッシュによる最新判定、壊れた INDEX の再生成、Structured Output 依頼条件をテストから把握したいとき。
- oracle ファイル列挙、実装ファイル列挙、`.gitignore` 解釈、cmoc ブランチ base commit からの変更・削除検出、`.cmoc` ignore 保証のテストを確認したいとき。
- タイムスタンプ文字列、経過時間表示、pytest 実行時の `src` import path 設定に関する既存テストを確認したいとき。
- 一時 git リポジトリ、fake Codex CLI、`monkeypatch`、`capsys`、`tmp_path` を使った cmoc テスト実装例を参照したいとき。

## Do not read this when

- cmoc の正本仕様断片を確認したいとき。仕様は `oracles` 配下を読み、ここは実装検証用のテストとして扱います。
- cmoc の本番実装コードそのものを直接読みたいとき。実装は `src` 配下を確認します。
- README、AGENTS、oracles、memo の編集可否やリポジトリ運用ルールだけを確認したいとき。
- cmoc を使って別リポジトリを開発する `<repo-root>` 側の作業手順やプロジェクト固有ルールを調べたいとき。
- pytest、git、Typer、Codex CLI、JSON schema の一般的な使い方だけを知りたいとき。
- テスト期待値ではなく、ユーザー向けドキュメントや利用手順だけを確認したいとき。

## hash

- aad7413907bc7f01f9f0786e4a849818ef7726049b95a8d201719a8ff38aa1cd
