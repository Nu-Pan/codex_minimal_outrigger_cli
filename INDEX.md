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
- cmoc のアプリケーション仕様、状態管理、branch・commit・worktree、Python 開発規則などを扱う oracle 文書群への入口です。共通仕様や個別機能の正本文書を確認する際に参照します。
- 参照可能な正本ソースの有無を確認するための入口です。具体的な実装仕様や処理内容の確認先ではありません。

## Read this when
- cmoc の共通挙動、CLI、状態管理、ログ、プロンプト、run/session lifecycle を調査するとき
- session fork、run 隔離、branch・commit・worktree の責務やライフサイクルを確認するとき
- Python 実装、CLI 配置、開発環境、pytest テストの規約を確認するとき
- realization refactor で採用しなかった作業方式や設計案の理由を確認するとき
- 参照可能な正本ソースの有無を確認するとき

## Do not read this when
- 特定の realization code や realization test の内部実装だけを調査するとき
- 個別機能の詳細仕様を確認する場合は、対象機能の oracle 文書を直接読むとき
- 一般的な INDEX.md の読み方やルーティング方針を確認するとき
- README だけで足りる一般的な利用方法を知りたいとき
- 具体的な実装仕様や処理内容を確認したいとき

## hash
- cce14f1e525f9016575ebeeb252b9cbe7f36068d17e9587bca37b332c7b7b173

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
- cmoc CLI の realization 実装をまとめる src ディレクトリ。CLI ルート、サブコマンド、共通 runtime、設定、互換 import shim、canonical 実体への公開入口を含み、各下位パッケージ・モジュールへのルーティング起点となる。

## Read this when
- cmoc の CLI 構成や realization 側の主要モジュールを探すとき。
- CLI 入口、サブコマンド、共通 runtime、互換 import 経路の調査・変更先を判断するとき。

## Do not read this when
- 特定機能の詳細実装や正本仕様を直接確認したいときは、対応する下位モジュールまたは oracle 側を直接読む。
- src 配下と無関係な仕様・テスト・開発環境を調査するとき。

## hash
- 680f97f590a521779e79abcd6e71a2ae69eab353b4e7d81c02c8325c3321d3b2

# `test`

## Summary
- cmoc の realization test を集約するディレクトリ。CLI、runtime、Codex 実行、ACP builder、INDEX 生成、oracle review、session/run lifecycle など、実装の外部挙動・制御ロジック・公開契約を検証するテストと、複数テストで共有する Git・Codex・Ollama・コマンド実行ヘルパーを扱う。特定機能の挙動や回帰を調査する際は、該当するテストファイルを入口として読む。

## Read this when
- cmoc のテスト構成や、変更対象機能に対応する realization test の入口を探すとき
- CLI、runtime、Codex 実行、INDEX、oracle review、session/run、ACP builder の外部契約や回帰検証を確認するとき
- 複数のテストで共有される Git、Codex、Ollama、fake command などのテスト支援を確認するとき

## Do not read this when
- 実装本体や正本仕様の詳細だけを確認したいときは、対応する src または oracle を直接読む
- LLM の回答品質そのものや、対象機能と無関係なテスト実装を調査するとき

## hash
- 3ab89651ad1e2cf74f66b2d6474b659f36abf052508ddeb865a165085a0658aa
