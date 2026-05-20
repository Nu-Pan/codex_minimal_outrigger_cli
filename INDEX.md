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

- `bin` は cmoc CLI の実行入口を置くディレクトリです。
- 主な実体は `bin/cmoc` で、POSIX shell 製のラッパースクリプトとして `<cmoc-root>` を解決し、`<cmoc-root>/.venv/bin/python` で `<cmoc-root>/src/main.py` を起動します。
- 仮想環境 Python が存在しない、または実行可能でない場合の日本語エラーレポート、次の対応、セットアップ手順、終了ステータス 1 の挙動も `bin/cmoc` に含まれます。
- `__pycache__` 配下は Python バイトコードキャッシュであり、通常の仕様確認や実装確認で読む対象ではありません。

## Read this when

- cmoc コマンドの実行入口、起動ラッパー、PATH から呼び出されるファイルを確認したいとき。
- `bin/cmoc` が `<cmoc-root>`、`.venv/bin/python`、`src/main.py` をどのように解決して起動するか調べたいとき。
- 仮想環境未セットアップ時や `.venv/bin/python` が実行できない場合のエラー表示、セットアップ案内、終了ステータスを確認したいとき。
- CLI 起動時にユーザー指定の引数が `src/main.py` へそのまま渡されるか確認したいとき。
- cmoc のインストール後に実行ファイル側の導線や起動失敗時のトラブルシュート表示を修正・テストしたいとき。

## Do not read this when

- cmoc のサブコマンド本体、引数解析、Codex CLI 連携、oracle 処理、git 操作など `src/main.py` 以降の実装詳細を調べたいとき。
- cmoc の正本仕様断片を調べたいとき。この場合は `oracles/INDEX.md` から必要な仕様ファイルへ進むべきです。
- cmoc 自体の開発規約、設計規約、テスト規約、開発環境ルールを調べたいとき。
- Python パッケージ設定、依存関係、仮想環境作成手順そのものを詳しく確認したいとき。
- `__pycache__` や `.pyc` の内容を確認したいだけのとき。これらは生成物であり、通常は読む必要がありません。

## hash

- 213eb13279fb46f9abba4786c91a7600836b54da8651823bb8f7d68bbbc5277f

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

- `pyproject.toml` は、cmoc パッケージの Python プロジェクト設定を定義するファイルです。
- プロジェクト名、バージョン、説明、要求 Python バージョン、依存パッケージを管理します。
- `cmoc` コマンドのエントリーポイントを `main:main` として定義します。
- setuptools を使ったビルド設定、`src` 配下をパッケージ探索対象にする設定、`main` モジュールの配布設定を含みます。

## Read this when

- cmoc の Python パッケージメタデータ、依存関係、要求 Python バージョンを確認したいとき。
- `cmoc` コマンドがどの Python 関数へ接続されているか確認したいとき。
- setuptools のビルドバックエンド、`src` レイアウト、配布対象モジュールの設定を確認したいとき。
- 開発環境やインストール時に参照されるプロジェクト設定を変更・確認したいとき。

## Do not read this when

- cmoc のサブコマンド仕様、Codex CLI 呼び出し仕様、ログ保存、Structured Output などのアプリケーション実行時仕様を調べたいとき。
- cmoc の具体的な実装ロジックや CLI 処理内容を読みたいとき。
- 自動テストの具体的なテストケースや Fake Codex CLI の実装を確認したいとき。
- README、AGENTS、oracles、memo などのリポジトリ運用ルールや編集可否だけを確認したいとき。

## hash

- f7e7dcdc72547ff9b03be0135915cb7c3ae47af0b596744238d91061acd8488e

# `src`

## Summary

- `src` は cmoc 本体の Python 実装を置くトップレベルディレクトリです。
- `main.py` は Typer ベースの CLI エントリーポイントで、`init`、`branch`、`eval-oracles`、`apply`、`merge` の各サブコマンドを登録し、実処理を `sub_commands` 配下へ委譲します。
- `commons` はサブコマンド横断の共通処理パッケージで、Codex CLI 呼び出し、Structured Output 検証、ログ保存、`INDEX.md` 自動メンテナンス、共通エラー整形、repo root 解決、git 操作、タイムスタンプ生成、ステップ時間計測を扱います。
- `sub_commands` は cmoc の個別サブコマンド本体を置くパッケージで、初期化、作業ブランチ作成、oracle 評価、oracle 追従 apply、cmoc ブランチ merge の実行フローを実装します。
- `codex_minimal_outrigger_cli.egg-info` や `__pycache__` はビルド・実行時に生成されるメタデータやキャッシュであり、通常の実装調査では主対象ではありません。

## Read this when

- cmoc 本体実装の入口として、CLI エントリーポイント、共通ユーティリティ、個別サブコマンド実装のどこを読むべきか判断したいとき。
- `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc apply`、`cmoc merge` がどの Python モジュールに実装されているか把握したいとき。
- Typer のコマンド登録や CLI 引数受け取り部分を確認するために `main.py` へ進むべきか、サブコマンド本体を見るために `sub_commands` へ進むべきか判断したいとき。
- Codex CLI 呼び出し、Structured Output、ログ保存、INDEX メンテナンス、git/repo 操作、エラー整形、タイマーなどの横断処理を探して `commons` へ進むべきか判断したいとき。
- cmoc 自体の実装を修正・調査する前に、`src` 配下の大まかな責務分担を確認したいとき。

## Do not read this when

- cmoc の正本仕様断片を調べたいとき。その場合は `oracles` 配下の `INDEX.md` から必要な仕様ファイルへ進んでください。
- cmoc の自動テスト、pytest fixture、Fake Codex CLI、期待出力などを調べたいとき。その場合は `tests` 配下を確認してください。
- README、AGENTS、oracles、memo などの編集可否やリポジトリ運用ルールだけを確認したいとき。
- cmoc を使って開発する別リポジトリの `<repo-root>` 側アプリケーションコードや oracle 内容を調べたいとき。
- 生成物である `__pycache__` や `codex_minimal_outrigger_cli.egg-info` の内容だけを確認したいとき。

## hash

- c45817f97a70901e83511441ab840de74a8133313bd9a74d40b0541cb887e51a

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
- `conftest.py` は `<cmoc-root>/src` を import path に追加し、インストールなしで実装モジュールをテストから読み込めるようにします。
- `test_codex.py` は `commons.codex.run_codex_exec` の Codex CLI 呼び出し、Structured Output、リトライ、ログ出力、stdout 進捗表示、INDEX メンテナンス連携を検証します。
- `test_indexing.py` は `commons.indexing.maintain_indexes` による `INDEX.md` 自動生成・更新、gitignore 除外、空ディレクトリ、build/tmp、memo、Structured Output schema、再生成条件、自動コミット範囲を検証します。
- `test_repo.py` は `commons.repo` の repo root 探索、`.cmoc` ignore 保証、oracle ファイル列挙、変更 oracle 抽出、削除検出、cmoc ブランチ判定、`cmoc apply` 前提条件を検証します。
- `test_subcommands.py` は `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc apply`、`cmoc merge`、Typer エントリーポイント、`bin/cmoc` ランチャーの決定論的な制御ロジックを検証します。
- `test_timestamps.py` は `commons.timestamps.make_timestamp` と `commons.timing.format_duration` の出力フォーマットを検証します。

## Read this when

- cmoc 自体の自動テスト全体の配置や、どのテストファイルを読むべきか判断したいとき。
- 実装変更後に影響を受ける pytest の範囲を把握したいとき。
- Codex CLI 呼び出し、Structured Output、ログ、リトライ、INDEX メンテナンス連携のテストを確認したいとき。
- `INDEX.md` 自動メンテナンス、gitignore 除外、空ディレクトリ、build/tmp、memo、再生成条件、自動コミット範囲の期待挙動をテストで確認したいとき。
- repo root 探索、oracle ファイル列挙、oracle 変更検出、oracle 削除検出、`.cmoc` ignore、cmoc ブランチ判定など `commons.repo` の回帰テストを探しているとき。
- `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc apply`、`cmoc merge` のサブコマンド実装変更に対応するテストを確認したいとき。
- Typer の CLI 委譲、`cmoc --help`、`bin/cmoc` ランチャー、venv 要求に関するテストを確認したいとき。
- タイムスタンプや経過時間表示の出力形式に関するテストを確認したいとき。
- 一時 git repository、fake Codex CLI、`monkeypatch`、`tmp_path` を使った cmoc テストの書き方を参考にしたいとき。

## Do not read this when

- cmoc の正本仕様断片を確認したいとき。仕様は `<cmoc-root>/oracles` 配下をルーティングに従って読むべきです。
- cmoc の実装コードそのものを読みたいとき。実装は `<cmoc-root>/src` 配下を確認してください。
- cmoc のユーザー向け概要、インストール手順、基本ワークフローだけを確認したいとき。
- README、AGENTS、oracles、memo などの編集可否やリポジトリ運用ルールだけを確認したいとき。
- pytest の一般的な使い方や Python 標準のテスト技法だけを調べており、cmoc 固有の期待挙動が不要なとき。
- `__pycache__` 配下のバイトコードキャッシュを調べたいとき。通常の開発・仕様確認では読む必要はありません。

## hash

- 4a5562c42dcdd08f9b1571c142bd802faf202c325370da7b68fdce825317aa7b
