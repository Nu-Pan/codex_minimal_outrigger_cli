# `AGENTS.md`

## Summary
- cmoc 自己開発時に恒常的に適用するリポジトリ固有の指示を定める補足文書。動的生成プロンプトの権限や作業範囲は変更せず、Python 環境、設計、テストの判断時に参照すべき oracle file への入口を提供する。

## Read this when
- cmoc リポジトリ固有の開発ルールや、動的生成プロンプトとの関係を確認するとき
- Python の実行環境・環境構築・pip の扱いを判断するとき
- realization implementation の配置・責務境界を判断するとき
- realization test の実装・実行・変更後の検証方法を判断するとき

## Do not read this when
- 具体的な Python 環境手順を確認する場合は、直接 development_environment.md を読むとき
- 実装の設計責務を確認する場合は、直接 design_rule.md を読むとき
- テスト手順を確認する場合は、直接 test_rule.md を読むとき
- 動的生成プロンプトで指定された作業範囲や権限を確認する場合

## hash
- b168e9259b1693105309f460d4ef248fd19978f0bae5fab8e1617b0f3aeac112

# `LICENSE`

## Summary
- This file is the repository's license grant and warranty disclaimer. Read it when you need to confirm redistribution rights, attribution obligations, or liability terms for using the project in another codebase or release.
- It is the right place to consult for legal permission questions about copying, modifying, sublicensing, or distributing the software.

## Read this when
- You need to know whether the project can be reused, copied, modified, merged, published, sublicensed, or redistributed.
- You need to confirm whether attribution or the license notice must be preserved in derived or distributed copies.
- You need the warranty and liability terms that apply to use of the software.

## Do not read this when
- You are looking for implementation behavior, CLI usage, configuration, or development workflow.
- You need repository structure or routing guidance; a different `INDEX.md` is the better entry point.
- You need project-specific legal exceptions or additional terms, which would have to be stated in another file.

## hash
- a894f2547af0349f234986eb4661f0146f37b7d82f8b22a27a674d5c1236f08f

# `README.md`

## Summary
- Codex Minimal Outrigger CLI（cmoc）の概要、初期セットアップ、基本ワークフロー、ターミナルロック対策を案内するプロジェクト入口。詳細な開発指示は AGENTS.md、運用手順は oracle/doc/app_spec/usage.md へ進むための起点。

## Read this when
- cmoc の目的や略称を確認したいとき
- 初期セットアップや PATH 設定の手順を確認したいとき
- 基本ワークフローの参照先を知りたいとき
- Ctrl+S によるターミナルロックを防ぎたいとき

## Do not read this when
- 詳細な開発規約や恒常的なリポジトリ指示を確認したいときは AGENTS.md を読む
- 基本ワークフローの具体的な運用手順を確認したいときは oracle/doc/app_spec/usage.md を直接読む

## hash
- aee9654cfb1c4d0d9aa963e9f03b8a56f4e5b6cdc7aac1ebeeb478b914f88f11

# `bin`

## Summary
- プロジェクトの仮想環境 Python を検証し、通常実行時および補完プローブ時に CLI の実行入口へ引数を渡す起動ラッパー。仮想環境が利用できない場合のセットアップ手順付きエラーも扱う。

## Read this when
- cmoc コマンドの起動経路、仮想環境 Python の検証、補完プローブ時の挙動、起動失敗時のエラー表示を確認するとき。

## Do not read this when
- CLI サブコマンドの実装や引数処理そのものを調べるときは、直接 src/main.py と該当する実装を読む。
- 開発環境の正本仕様やセットアップ規則を確認するときは、対応する oracle ドキュメントを直接読む。

## hash
- b871bfb0955e588c6b6b7c1ffaadc49609acccff1208cd93ace6f067970ca774

# `codex_minimal_outrigger_cli.code-workspace`

## Summary
- VS Code のワークスペース設定を確認・変更するときに読む。ここには、このリポジトリを開いたときの既定インタプリタ、Python の解析対象、エディタ既定設定、非表示対象の方針がまとまっている。
- 日常的な実装変更やテスト追加では通常読まない。そうした作業は各実装・テスト・関連 `INDEX.md` を優先し、このファイルはエディタ環境やワークスペース構成に関する判断が必要なときだけ参照する。

## Read this when
- このリポジトリを VS Code のワークスペースとして開くとき
- Python の実行環境や解析対象の既定を確認したいとき
- エディタ側でどのファイルを見せるか・隠すかの方針を変えたいとき

## Do not read this when
- アプリケーションの挙動や CLI の仕様を確認したいとき
- 実装やテストの変更先を探したいとき
- 既存の各領域の `INDEX.md` や本文を読むべき作業をしているとき

## hash
- 1938307f70f255710d75d39c07d860ecb381acbb031ca19b2f2b6e565ac41acb

# `oracle`

## Summary
- cmoc の正本仕様ファイルを集約するディレクトリ。CLI 自動補完、Codex CLI 呼び出し、ログ、doctor preprocess、プロンプト、run・session lifecycle、サブコマンドなど、複数機能にまたがる仕様確認の入口を提供する。
- 下位の doc は自然言語による仕様、src は正本ソースを扱う。特定機能の詳細や個別定義を調べる場合は、該当する下位ディレクトリまたはファイルへ進む。

## Read this when
- cmoc の正本仕様を横断的に探すとき
- CLI 起動、Codex CLI 呼び出し、ログ、プロンプト、run・session lifecycle、サブコマンドなどの仕様の入口を確認するとき
- 正本ソースの責務分担や、エージェント呼び出し・設定・パス・構造化文書・プロンプト関連の下位領域を確認するとき

## Do not read this when
- 特定機能の詳細仕様や個別定義が明らかなとき
- realization の実装・テスト詳細だけを調査するとき
- cmoc の一般的な利用手順だけを確認するとき

## hash
- 6877728871b1241f4ff9e1a35daadd176707bd10caacf4aeefb6c43e9b318157

# `pyproject.toml`

## Summary
- プロジェクトの Python パッケージメタデータ、依存関係、CLI エントリーポイント、ビルド設定を定義する設定ファイル。pytest・Ruff・mypy の実行対象や Python バージョン要件も確認できる。

## Read this when
- 依存関係、対応 Python バージョン、`cmoc` コマンドのエントリーポイント、パッケージ探索、ビルド設定を確認するとき。
- pytest・Ruff・mypy のプロジェクト共通設定や GPU integration テストのマーカーを確認するとき。

## Do not read this when
- CLI の具体的な処理や実装責務を確認したいときは、`src` 配下の実装を直接読む。
- 正本仕様や開発環境・テスト手順を確認したいときは、`oracle` 配下の該当文書を読む。

## hash
- b2f7a17a58e3aa7aac375d93ebf50b342e13e74c4e9bc5ba3b6e8fd88b78edd4

# `src`

## Summary
- cmoc CLI の realization 実装ルート。Typer による CLI 登録、互換 import shim、共通 runtime、ACP builder、basic/config、各サブコマンド実装を含む。目的に応じて下位パッケージまたは主要エントリーファイルへ進む。
- `main.py` は doctor、tui、session、oracle、realization、run、indexing などの CLI コマンドを登録し、引数解析エラーを cmoc 形式へ変換する主要入口。CLI の公開面や委譲先を確認するときに読む。
- `commons` は設定、Git、Codex 実行、プロセス、パス、状態、ログ、結果、run lifecycle、INDEX 更新など、複数コマンドが共有する runtime 実装の入口。共通処理の詳細を確認するときに読む。
- `sub_commands` は doctor、indexing、tui、session、oracle、realization、run などの個別 CLI サブコマンド実装をまとめる。特定コマンドの処理入口やコマンド固有の制御を調査するときに読む。
- `acp` は既存の `acp.*` および `acp.builder.*` import を維持する互換入口と、canonical builder へ接続する adapter 群を提供する。builder、prompt fence、TUI、session、oracle、realization の parameter 構築を確認するときに読む。
- `basic` は ACP 型、path model、構造化文書 API などを実体定義から再公開する互換 import 入口。公開名や import 経路を確認するときに読む。
- `config` は設定型・設定 API の既存 `config.*` import を成立させる互換入口。設定定義そのものではなく、互換公開経路を確認するときに読む。
- `oracle.py` は `src` 起動時に `oracle.*` パッケージを解決する package shim。正本側 oracle package の import 解決を調査するときに読む。
- `cmoc_runtime.py` は `commons.cmoc_runtime` の公開名を再公開する互換 import shim。runtime の旧 import path や移行状況を確認するときに読む。

## Read this when
- cmoc の CLI 公開面、コマンド登録、引数解析、またはトップレベルの realization 構成を確認するとき。
- 共通 runtime、サブコマンド、ACP builder、互換 import 入口のどこから調査を始めるべきか判断するとき。

## Do not read this when
- canonical な oracle 実装や正本仕様そのものを確認したいとき。対応する `oracle` ツリーを直接読む。
- 特定の runtime module、builder、またはサブコマンドの詳細だけを調査するとき。対象の下位要素へ直接進む。

## hash
- 17be98a6710910582ce6d8e3787279615bcb45270ba450f661366e25dd72af91

# `test`

## Summary
- cmoc の realization test を集約するディレクトリ。ACP builder、Codex runtime、CLI、indexing、oracle review、session、state、設定、共通テスト支援など、実装の外部挙動と制御契約を検証するテストへの入口。

## Read this when
- cmoc の実装変更に対応する回帰テストや統合テストを探すとき
- CLI、Codex/Ollama 実行、worktree・Git・state lifecycle、INDEX 生成、oracle review、ACP builder の挙動を検証するとき
- 既存テストの失敗原因や、共通テスト fixture・helper の責務を確認するとき

## Do not read this when
- 正本仕様や開発・テスト手順を確認することが目的のときは、対応する oracle 文書や開発ルールを直接読む
- 対象機能の実装詳細だけを調査するときは、対応する src 配下の実装を直接読む
- LLM や Codex の回答品質そのものを評価するとき

## hash
- 92862028348f51af06b33f3ba699c01f9bb77cfb6566371c7a6f5e8fa465d5a2
