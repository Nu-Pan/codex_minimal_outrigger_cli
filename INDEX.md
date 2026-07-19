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
- `cmoc` の起動ラッパー。仮想環境の Python を確認し、補完要求か通常起動かを切り替えて `src/main.py` へ渡す。

## Read this when
- `cmoc` の実行前提、特に `.venv` の存在確認と、欠落時に出す案内を確認したいとき。
- シェル補完のときだけ別経路で起動する条件を確認したいとき。
- `cmoc` から実際の CLI 実装へどう入るかを追いたいが、各サブコマンドの処理本体までは不要なとき。

## Do not read this when
- 各サブコマンドの引数解釈や業務ロジックを知りたいときは `src/main.py` や該当サブコマンド実装を読む。
- 仮想環境のセットアップ手順そのものや、利用者向けの運用説明だけが目的なら、このラッパーではなく上位の利用案内を読む。

## hash
- ca144e1b915722cdfe8a460aa67f416f69bc3eac2aea5de84869eaa1f907025e

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
- cmoc の正本仕様を集約する oracle ディレクトリ。利用者向けアプリケーション仕様、正本ソース、設定・パス・構造化文書基盤、プロンプト生成規則への入口を提供する。
- 配下の `doc` は自然言語によるアプリケーション仕様と開発・refactor 関連文書、`src` は正本実装と Structured Output schema、各種基盤・プロンプト構築を扱う。

## Read this when
- cmoc の正本仕様または正本ソースの構成を確認するとき。
- 複数のアプリケーション仕様、agent call、Structured Output、設定・パス・プロンプト生成にまたがる調査の入口を判断するとき。

## Do not read this when
- 具体的な機能仕様、開発規則、テスト規則、プロンプト部品、または realization 側の実装箇所が特定できているときは、対応する下位対象や専用文書を直接読む。
- CLI の具体的な実行経路・入出力や、現行の realization refactor 運用だけを確認するとき。

## hash
- 31b14b74b96f4d44cea578234c2b5f7a2d70fa758e0071811941f30eda1461a9

# `pyproject.toml`

## Summary
- Python プロジェクトのパッケージ metadata、依存関係、CLI エントリポイント、ビルド設定、パッケージ探索、pytest・Ruff・mypy の設定を定義する。プロジェクトの実行・配布・開発ツール設定への入口。

## Read this when
- 依存関係、対応 Python バージョン、`cmoc` CLI のエントリポイント、パッケージ配置やビルド設定を確認・変更するとき
- pytest、Ruff、mypy のプロジェクト共通設定を確認・変更するとき

## Do not read this when
- CLI の具体的な処理や実装を確認するときは `src` 配下を直接読む
- 正本仕様や oracle 側の実装・テストを確認するときは `oracle` 配下を直接読む

## hash
- 41be0de2208bc52d124bffe4dc0a086623184f709aa1d049d18a22ce5601aae2

# `src`

## Summary
- cmoc の realization 側 `src` パッケージ群をまとめる入口。CLI 最上位エントリー、サブコマンド、共通 runtime、互換 import shim、設定・ACP・basic 関連の公開入口を扱い、各責務の実装へルーティングする。

## Read this when
- `src` 配下の実装構成や、CLI 起動経路・サブコマンド・共通 runtime の担当箇所を探すとき。
- 互換 import path、realization 側の公開入口、または対象機能の実装モジュールへの導線を確認するとき。

## Do not read this when
- 特定サブコマンド、runtime 機能、builder、TUI、設定、ACP 型などの詳細が分かっているときは、該当する下位モジュールを直接読む。
- 正本仕様や canonical 実装を確認したいときは、対応する `oracle` 側を直接読む。

## hash
- a78bc770294d91db324bba4096047bb49d5465a26d9ae3aa99becc027e2aa86a

# `test`

## Summary
- テストコードから、ACP builder、CLI、Codex runtime、doctor、indexing、oracle review、session、設定、worktree などの実装契約と外部挙動を検証する pytest 群、および共有テスト補助モジュールへ進むための入口。各テストは対応する機能領域の回帰・統合・公開 API・状態遷移を確認する。

## Read this when
- 対象機能の外部挙動、CLI lifecycle、Codex 実行境界、builder parameter、indexing、oracle review、session/run 状態、設定、worktree のテスト契約を調査・変更するとき。
- テストで共有される CliRunner、fake Codex、fake external command、Git repository、Ollama、oracle schema path の準備方法を確認するとき。

## Do not read this when
- 正本仕様や schema の内容そのものを確認・変更するときは、対応する oracle 文書・schema を直接読む。
- 実装内部の責務や生成ロジックだけを調査するときは、対応する src の実装ファイルを直接読む。
- 特定の機能領域と無関係なテストや、対象テストの外部契約に影響しない一般的な実装を扱うとき。

## hash
- 95cf5adb5313fb4f054f40af2295b8c373727887b254fbc7c0fe64dff0ea33a4
