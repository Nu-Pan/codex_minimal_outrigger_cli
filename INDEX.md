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
- cmoc CLI の realization 実装をまとめる最上位の入口。Typer によるコマンド登録・引数解析・エラー変換を担う CLI エントリーポイントと、互換 import、共通 runtime、設定、サブコマンド実装を含む。下位ディレクトリから個別機能の実装へ進むための起点。

## Read this when
- cmoc の CLI 全体の構成、コマンド登録、引数解析、補完、エラー処理を確認するとき。
- 共通 runtime、互換 import、設定、またはサブコマンド実装の配置と担当範囲を確認するとき。
- 特定のサブコマンドや共通処理の詳細実装へ進む前に、最上位の委譲関係を把握するとき。

## Do not read this when
- canonical な oracle 仕様や oracle 側実装を確認するときは、対応する oracle ツリーを直接読む。
- 特定のサブコマンド、runtime helper、互換 shim の詳細を調査・変更するときは、対応する下位ファイルを直接読む。
- INDEX 更新や TUI など、個別機能の処理本体だけを確認したいときは、該当する実装へ直接進む。

## hash
- 8aed3a9e46290ea50fb0d3977a6d86cc667cd4180b71acc68e897ac0ec019a16

# `test`

## Summary
- テストディレクトリ全体として、cmoc の runtime、CLI、Codex 実行、ACP builder、indexing、oracle review/edit、session、worktree、設定・状態永続化などの外部契約と制御ロジックを検証する realization test 群を収録する。各テストファイルが機能領域ごとの詳細な検証入口となる。

## Read this when
- cmoc の機能変更後に、対象領域に対応する回帰テストや統合テストを特定するとき。
- CLI lifecycle、Codex runtime、indexing、oracle review、session、state、worktree、設定、ACP builder などの挙動を検証するテスト入口を探すとき。
- 実装変更に対して、外部挙動・状態遷移・Git 操作・エラー処理のどのテストを確認すべきか判断するとき。

## Do not read this when
- 対象機能が明確で、対応する個別テストファイルを直接読めるとき。
- 正本仕様や実装詳細そのものを確認することが目的で、対応する oracle または src のファイルを直接読むべきとき。
- Codex や LLM の回答品質そのものを評価したいとき。

## hash
- deedfb30d546e989b7527b7ad0e40dc27e79b41336221bb932b3dbc8407912a5
