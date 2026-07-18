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
- cmoc の正本仕様を担う oracle 文書・実装群への入口。アプリケーション機能、branch モデル、設計判断、開発規則、および ACP agent call・prompt・Structured Output schema・共通モデルの oracle src を扱う。

## Read this when
- cmoc の利用者向け機能、CLI、run・session、branch・worktree、prompt、Codex CLI 呼び出し、ログ、補完、managed ollama などの正本仕様を調査・実装・レビューするとき。
- cmoc が採用した設計の背景や不採用案、Python 開発・CLI 配置・環境構築・テスト規則を確認するとき。
- oracle review・apply・indexing・session join などの ACP agent call 設定、Structured Output schema、共通 prompt、設定・パス・構造化文書モデルを調査するとき。

## Do not read this when
- 対象の機能、コマンド、prompt、schema、モデル、実装詳細が明確な場合は、このディレクトリ全体ではなく該当する個別文書または下位ディレクトリを直接読む。
- realization 側の具体的なコードや INDEX.md 生成方法だけを確認したい場合は、oracle ではなく対応する実装本文または専用 routing 文書を読む。
- cmoc 以外の通常の git 運用や、現在の file access rule・差分検査・permission profile を確認したい場合は、該当する直接の仕様・実装対象を読む。

## hash
- 53d6425447ea4e02008eee869997dbccbf2e25fb7c2b47ca47ca4fad66b52689

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
- cmoc の realization 実装を集約する src ディレクトリ。CLI の起動入口、サブコマンド、共通 runtime、ACP・設定・基本 API の互換入口、oracle パッケージ shim への導線を扱う。

## Read this when
- cmoc の realization 側で CLI 公開入口、サブコマンド、共通 runtime、互換 import shim の実装箇所を選ぶとき。
- 複数の実装領域にまたがる変更で、src 配下の責務分担や下位モジュールへの入口を確認するとき。

## Do not read this when
- 正本仕様や canonical implementation の内容だけを確認したいときは、対応する oracle 配下を直接読む。
- 特定の runtime helper、サブコマンド、ACP builder などの詳細だけを調査するときは、対応する下位モジュールを直接読む。

## hash
- bab634c7bf90939beeace3867a9365473f8b4dacab3747bfeffb83331007c57c

# `test`

## Summary
- cmoc の realization test を集約するディレクトリ。ACP builder、CLI、Codex runtime、doctor、indexing、oracle review、session/apply、runtime 共通機能などの外部挙動・契約・回帰を pytest で検証する。個別テストは各機能の変更時に読む入口となり、共有テスト helper は該当するテスト準備を提供する。

## Read this when
- 特定の CLI サブコマンド、Codex 実行、indexing、oracle review、session/apply、runtime、ACP builder の外部挙動や回帰を変更・調査するとき。
- 該当機能の入力検証、状態遷移、Git/worktree、process、sandbox、report、schema、公開 API などのテスト契約を確認するとき。
- テストで使う共有 CliRunner、Git repository、Codex、Ollama、fake command などの準備方法を確認するとき。

## Do not read this when
- 正本仕様、schema、prompt、実装責務そのものを確認することが目的の場合は、対応する oracle または realization implementation を直接読む。
- 一般的な pytest 実行方法や、対象機能と無関係なテストの挙動を調べる場合。
- 特定の共有 helper の内部実装だけを確認したい場合は、該当する support module を直接読む。

## hash
- c874091dd20a6862cebc68af979364744a01f98935dad439ffb4b991fa0e0e2e
