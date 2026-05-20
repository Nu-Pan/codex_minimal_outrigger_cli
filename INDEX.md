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

- `/home/happy/codex_minimal_outrigger_cli_stage1/oracles/INDEX.md` を読み、配下の正本仕様を調べる入口としての目次情報だけを整理します。ファイル編集と `memo` へのアクセスは行いません。

## Read this when

- `oracles` 配下の仕様断片を調べ始める前。
- どの仕様ファイルや下位ディレクトリを読むべきか判断したいとき。
- cmoc の正本仕様に基づいて実装やテスト方針を確認したいとき。

## Do not read this when

- cmoc の実装コードそのものを確認したいとき。
- `README.md` や `AGENTS.md` の編集が目的のとき。
- `memo` 配下の情報を探したいとき。

## hash

- ca462c3f2193b29fabe34123925821c5e686ced193984d6e4bd0c59678dcd4ea

# `pyproject.toml`

## Summary

- cmoc 自体の Python パッケージ設定ファイル。
- プロジェクト名、バージョン、説明、Python 要件、依存パッケージを定義している。
- `cmoc` コマンドのエントリーポイントを `main:main` として登録している。
- setuptools を使ったビルド設定、`src` 配下をパッケージルートとする設定、`main` モジュールと `sub_commands` のパッケージデータ設定を含む。

## Read this when

- cmoc のインストール時メタデータ、依存関係、対応 Python バージョンを確認したいとき。
- `cmoc` コマンドがどの Python 関数に接続されているか調べたいとき。
- setuptools のビルドバックエンド、`src` レイアウト、配布対象モジュールやパッケージデータの設定を確認したいとき。
- 新しい実行時依存やパッケージデータを追加する必要があるとき。

## Do not read this when

- cmoc のサブコマンドの詳細仕様やユーザー向け挙動を調べたいとき。
- Python 実装コードの具体的な処理内容やテスト内容を確認したいとき。
- README、AGENTS、oracles、memo などのリポジトリ運用ルールやファイルアクセス制約だけを確認したいとき。
- cmoc を使って開発する別リポジトリ側の設定や仕様を調べたいとき。

## hash

- 74bf4b55ac8815e2d09f225da7f6100ac02ed92e46bc4bb1ebe77c61f049c5f3

# `src`

## Summary

- `src` は cmoc 本体の Python 実装を置くディレクトリです。
- CLI エントリーポイントである `main.py`、横断的な共通処理をまとめる `commons`、各サブコマンド本体を配置する `sub_commands` で構成されています。
- `main.py` は Typer アプリケーション `cmoc` を定義し、`init`、`branch`、`eval-oracles`、`apply`、`merge` の各コマンドを登録して、実処理を `sub_commands` 配下へ委譲します。
- `commons` は Codex CLI 呼び出し、Structured Output 検証、ログ保存、共通エラー整形、repo root 解決、git 操作、`.cmoc` ignore 保証、oracle ファイル列挙、`INDEX.md` 自動メンテナンス、タイムスタンプ、時間計測などの共通部品を提供します。
- `sub_commands` は `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` の具体的な実行フロー、進捗表示、Codex CLI 連携、レポート生成、git 操作の組み立てを実装します。

## Read this when

- cmoc 本体の実装コード全体の入口を把握したいとき。
- CLI エントリーポイント、共通処理、個別サブコマンド実装が `src` 配下でどのように分かれているか確認したいとき。
- `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc apply`、`cmoc merge` の実装ファイルへ進むためのルーティング情報が必要なとき。
- Typer のコマンド登録や Click/Typer 例外の共通エラーレポート変換を確認したいとき。
- Codex CLI 呼び出し、Structured Output、ログ保存、リトライ、INDEX メンテナンス、repo root 解決、git 操作など、複数サブコマンドで共有される実装の所在を調べたいとき。
- サブコマンド単位の進捗表示、commit、oracle 評価、apply 反復、merge conflict 解消などの本体処理へ進む入口を探しているとき。

## Do not read this when

- cmoc の正本仕様断片を確認したいとき。その場合は `oracles/INDEX.md` から必要な仕様ファイルへ進むべきです。
- cmoc 自体の開発規約、テスト規約、設計規約、開発環境ルールだけを調べたいとき。その場合は `oracles/dev_rules` 配下を確認するべきです。
- 自動テストの具体的なケース、pytest 設定、Fake Codex CLI など、テスト実装だけを調べたいとき。
- README、AGENTS、oracles、memo などの編集可否やリポジトリ運用ルールだけを確認したいとき。
- cmoc を用いて開発する対象リポジトリである `<repo-root>` 側の oracle や `INDEX.md` の内容だけを調べたいとき。
- 特定の実装ファイルを読むべきことが既に明確で、`src` 全体の構成やルーティング情報が不要なとき。

## hash

- 8ccebecaceab590ec5b213604cce71482dd5ef3377efd7939a6ad81b8da5b155

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

- `tests` は cmoc 自体の pytest ベース自動テストを格納するディレクトリです。
- `conftest.py` で `<cmoc-root>/src` を import path に追加し、インストールなしで `commons` や `sub_commands` の実装をテストできるようにしています。
- `test_codex.py` は `commons.codex.run_codex_exec` の Codex CLI 呼び出し、Structured Output、リトライ、ログ保存、stdout 進捗表示、INDEX メンテナンス呼び出しを検証します。
- `test_indexing.py` は `commons.indexing.maintain_indexes` による `INDEX.md` 生成・更新、除外規則、空ディレクトリ、`build`・`tmp`、バイナリ、`memo`、Structured Output リトライ、自動コミット対象を検証します。
- `test_repo.py` は git リポジトリ共通処理として、repo root 探索、`.cmoc` ignore 保証、oracle ファイル列挙、gitignore 判定、oracle 変更・削除検出、cmoc ブランチ判定、base commit 記録パスを検証します。
- `test_subcommands.py` は `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc apply`、`cmoc merge`、Typer main、`bin/cmoc` ランチャーの決定論的な制御ロジックを検証します。
- `test_timestamps.py` は `commons.timestamps.make_timestamp` と `commons.timing.format_duration` の出力形式を検証します。
- テストでは一時 git リポジトリ、fake `codex` 実行ファイル、pytest `monkeypatch`、`capsys`、`subprocess` を使い、外部 Codex CLI や git 状態を隔離して期待挙動を固定しています。

## Read this when

- cmoc 自体の実装変更に対して、既存の自動テストがどの振る舞いを固定しているか把握したいとき。
- pytest が `<cmoc-root>/src` の実装をどのように import しているか、テスト環境の bootstrap を確認したいとき。
- Codex CLI 呼び出しラッパー、Structured Output schema、JSON parse・schema・意味検証のリトライ、ログ保存、stdout 進捗表示の期待値を確認したいとき。
- `INDEX.md` 自動メンテナンスの対象、除外規則、ハッシュ最新時のスキップ、無効 Structured Output の扱い、自動コミット対象をテストから確認したいとき。
- repo root 探索、`.cmoc` ignore、oracle ファイル列挙、gitignore semantics、oracle 差分・削除検出、cmoc ブランチ関連の共通処理を変更するとき。
- `cmoc init`、`branch`、`eval-oracles`、`apply`、`merge` のサブコマンド実装変更後に、回帰テストの期待挙動を確認したいとき。
- CLI エントリーポイント、Typer 関数の委譲、`cmoc --help`、サブコマンドエラー時の終了コード、`bin/cmoc` の venv 必須挙動を確認したいとき。
- タイムスタンプ文字列や経過時間表示のフォーマットを変更または確認したいとき。
- 一時 git リポジトリ作成、fake Codex CLI、pytest `monkeypatch` を使った既存テストパターンを流用したいとき。

## Do not read this when

- cmoc のユーザー向け仕様や正本仕様断片を確認したいだけのとき。その場合は `oracles/INDEX.md` から必要な仕様へ進むべきです。
- 実装コードそのものの構造や処理内容を直接読みたいとき。その場合は `<cmoc-root>/src` 配下の対象モジュールを読む方が適切です。
- README、AGENTS、oracles、memo の編集可否など、リポジトリ運用ルールだけを確認したいとき。
- Codex CLI や git の一般的な使い方を調べたいだけで、cmoc 固有のテスト期待値が不要なとき。
- pytest の一般的な書き方や Python 標準ライブラリの使い方だけを知りたいとき。
- `__pycache__` 配下の生成済み `.pyc` ファイルを調べたいとき。これらはテストソースではなく、目次作成や仕様確認の対象ではありません。

## hash

- b56eae6878c154b74c39d9fdff3cedbe9214be7c411bc7b9f35f5db9918e6f52
