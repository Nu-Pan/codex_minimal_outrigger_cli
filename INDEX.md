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
- cmoc の正本 oracle 文書と正本ソースをまとめる入口。アプリケーション仕様、開発規約、ACP・設定・パスモデル・プロンプト・TUI・レビュー・refactor/apply などを扱い、各個別文書・実装へ案内する。

## Read this when
- cmoc の利用者向け機能やサブコマンドの正本仕様を調査・実装・検証するとき。
- 複数仕様にまたがる実行順序、状態管理、出力、エラー処理、session／run／branch／worktree の関係を確認するとき。
- Python 開発環境、CLI 設計、テスト方針などの開発規約を確認するとき。
- ACP 呼び出し条件、設定・パス解決、構造化文書、完全なエージェントプロンプト、TUI、レビュー、refactor/apply の正本を探索するとき。

## Do not read this when
- 個別仕様や個別の prompt builder、schema、設定クラス、パス操作の対象が明確で、対応する下位文書・ソースを直接読めるとき。
- realization code や realization test の内部実装だけを調査するとき。
- oracle の一般原則や INDEX.md のルーティング方針自体を確認するとき。

## hash
- 90357e3a9a51c5c7f26da2801c4738fe93fd929e6e1ac8bc1940942bd6172b58

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
- cmoc CLI の realization 実装を収める src ディレクトリ。Typer のルート定義、サブコマンド、共通 runtime、互換 import shim、設定・型の再公開入口を扱う。
- CLI の実行入口やサブコマンド構成を確認したい場合は main.py と sub_commands から読み進め、横断的な実行時機能は commons、互換 import の挙動は各 shim を入口に確認する。

## Read this when
- cmoc CLI の realization 側の全体構成や公開入口を把握するとき。
- トップレベル CLI、サブコマンド、共通 runtime、互換 import 経路の調査・変更箇所を判断するとき。

## Do not read this when
- 特定サブコマンドの詳細処理だけを調査するときは sub_commands 配下を直接読む。
- 共通 runtime や設定、正本 oracle の具体的な仕様だけを確認したいときは、それぞれの対応モジュールや oracle 側を直接読む。

## hash
- 869289b883012002eeae5ee76d1082dae4d1f29d830dd50b1f6764e52ce321e2

# `test`

## Summary
- テストコードから、ACP builder、Codex runtime、CLI、indexing、oracle review、session/run state、Ollama、prompt、worktree など cmoc の主要機能を検証する pytest 群を提供する。共有 fixture・fake command・Git/Ollama/Codex test helper も含み、各機能の外部契約や回帰挙動を確認する入口となる。

## Read this when
- cmoc の機能変更に伴う realization test の対象、既存の外部挙動、回帰テスト、fixture や共有テスト helper を確認するとき。
- CLI、Codex 実行、indexing、oracle review、session、runtime 設定・state・worktree などの検証観点を横断的に探すとき。

## Do not read this when
- 正本仕様や schema の内容自体を確認・変更するときは、対応する oracle 文書・schema・source を直接読む。
- 実装詳細だけを調査するときは、対応する src の実装ファイルを直接読む。
- 対象機能と無関係なテストや、Codex・Ollama を使わない単体テストの詳細を確認するとき。

## hash
- 1e7c9518ef8ab8fec3bfbb18e472064143c329ea0652da7c351e98fa63b6f9ed
