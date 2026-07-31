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
- cmoc の実行入口を提供するシェルラッパーを含むディレクトリ。仮想環境 Python の存在・実行可能性を検査し、失敗時にはセットアップ手順と呼び出し位置を表示したうえで、成功時は src/main.py を起動する。

## Read this when
- cmoc コマンドの起動経路、仮想環境 Python の検査、補完プローブ、起動前エラー表示を確認・変更するとき。

## Do not read this when
- Python CLI 本体のコマンド処理や業務ロジックを確認したいとき。起動後の実装は src 側を直接読む。

## hash
- 464142724c5c5ed9b5dfec5aa77b6fb9e839c337859913d6ceced907ae5f5da9

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
- cmoc の実装コードを配置する src パッケージ。CLI エントリーポイント、サブコマンド、共通 runtime、互換 import shim、設定・ACP・basic の公開入口を含み、各機能の realization 実装へ進むための入口となる。

## Read this when
- cmoc の realization 実装全体の構成や、CLI・runtime・互換入口の配置を確認したいとき。
- 特定の実装を読む前に、CLI の主要入口、共通 runtime、サブコマンド、互換 package のどこへ進むべきか判断したいとき。

## Do not read this when
- 特定サブコマンド、runtime 機能、互換 shim の具体的な挙動を確認したいときは、対応する下位要素を直接読む。
- 正本仕様や oracle 実装の内容を確認したいときは、oracle 配下の対象を直接読む。

## hash
- 597791cfb235636b4700b726e2238ff2034b18c6f857f501bf61fd416269d064

# `test`

## Summary
- `test` ディレクトリは、cmoc の realization test を集約するテスト入口である。ACP builder、Codex runtime、CLI lifecycle、indexing、oracle review、session/run state、Git・設定・worktree・prompt・renderer など、実装の外部契約や制御ロジックを領域別テストで検証する。各テストファイルから、変更対象に対応する具体的な実装契約・回帰ケースへ進む。

## Read this when
- cmoc の実装変更に対する回帰テストや、外部挙動・制御ロジックの検証対象を探すとき。
- 対象が ACP builder、Codex 実行、CLI サブコマンド、indexing、oracle review、session/run state、Git、設定、prompt、worktree などのいずれかに関係するとき。
- 共通テスト支援、case-local Ollama、fake external command、テスト用 Git repository などの準備処理を確認するとき。

## Do not read this when
- 正本仕様や実装詳細だけを確認したいときは、対応する oracle file または realization implementation を直接読む。
- テスト対象がこのディレクトリの領域と無関係な場合。
- Codex や LLM の回答品質そのものを評価したい場合。

## hash
- be83a66f0bc482e1c513d9dfe0455a0533fbd0969a56fbc56f564ed4699122a9
