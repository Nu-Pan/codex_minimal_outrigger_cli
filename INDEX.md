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
- cmoc CLI の realization 実装ルート。Typer による CLI エントリー、互換 import shim、ACP builder adapter、共通 runtime、doctor・indexing・oracle・realization・run・session・tui の各サブコマンドを扱う。
- 配下の下位ディレクトリは、互換 API、共通 runtime、ACP parameter builder、または個別サブコマンドの処理を確認するための入口となる。

## Read this when
- CLI のコマンド登録、引数解析、エラー変換、自動補完、またはサブコマンドへの委譲を調査・変更するとき。
- `acp.*`、`basic.*`、`config.*` などの互換 import 経路や、canonical な oracle 実装への adapter を確認するとき。
- 複数のサブコマンドが利用する Git、設定、状態、Codex 実行、ログ、パス、run lifecycle などの共通処理を確認するとき。
- doctor、indexing、oracle、realization、run、session、tui の実行フローを調査・変更するとき。

## Do not read this when
- canonical な oracle 実装や正本仕様を確認したいときは、対応する `oracle` 配下を直接読む。
- 特定の共通 helper、builder、またはサブコマンドの詳細だけを確認したいときは、対応する下位モジュールへ直接進む。
- CLI や realization 実装と関係しない仕様調査を行うとき。

## hash
- 878530fb9f77decadfd8e9e3a55acd0a07b5280cf43ce7e0b7d75c2fd17f6f46

# `test`

## Summary
- テストコードから利用する共通支援モジュールと、ACP builder、Codex runtime、CLI、indexing、oracle review、session、state などの pytest テストを集約するテストディレクトリ。各テストは対応する実装の外部契約・制御ロジック・失敗時挙動を検証する入口となる。

## Read this when
- テスト対象の機能を変更・調査し、既存の回帰テストや共通 fixture の配置を確認するとき
- ACP builder、Codex 実行、CLI lifecycle、indexing、oracle review、session、runtime state などの外部挙動を検証するとき
- テスト用 Git/Ollama/Codex 環境や fake external command の共通支援を利用・変更するとき

## Do not read this when
- 正本仕様や schema の内容を確認することが目的の場合は、対応する oracle 文書・schema を直接読む
- 特定機能の実装詳細を確認する場合は、対応する src の実装を直接読む
- 対象領域と無関係なテストや共通支援を調査するとき

## hash
- 48f4b40fc9786fb5dfaee65de88679fa70f2cc303bdc8d6a0e8b9b6c2a8d87dd
