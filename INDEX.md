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
- cmoc の正本仕様を担う oracle ツリーの入口。自然言語仕様を収録する doc、正本ソースを収録する src など、アプリケーション仕様・開発規約・Structured Output schema・プロンプト生成の確認先を案内する。

## Read this when
- cmoc の正本仕様や正本実装の所在を確認したいとき。
- CLI、session/run、branch・commit・worktree、開発規約、agent call、Structured Output schema、プロンプト生成を調査するとき。

## Do not read this when
- 特定機能の詳細仕様や実装箇所が判明しており、下位の doc・src を直接読めるとき。
- realization 実装やテストの詳細を調査したいとき。
- INDEX.md の読み方やルーティング方針自体を確認したいとき。

## hash
- 81f566a79fae1445c3072a4029c688e2c35cad69c3640198923943b3fb144ab4

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
- src は cmoc の realization 実装ルートで、最上位 CLI エントリー、互換 import shim、共通 runtime、設定公開入口、CLI サブコマンド実装を含む。個別機能の調査では、ここから対応する package または module へ進む。

## Read this when
- cmoc の realization 側における CLI 起動経路、公開入口、共通 runtime、設定互換層、またはサブコマンド実装の配置を確認するとき。
- 対象機能の実装箇所が未特定で、最上位の実装構成から読む先を選ぶ必要があるとき。

## Do not read this when
- 特定のサブコマンド、runtime 機能、互換 shim、または設定クラスの詳細が対象なら、対応する下位 module を直接読む。
- oracle 側の正本仕様や canonical 実装を確認したい場合は、src ではなく対応する oracle 配下を読む。

## hash
- 39596bb414ad2c60af8c96874be17aa8bcd210c5c134f0bd351ac8688ff2c4f2

# `test`

## Summary
- cmoc の realization test 群をまとめたディレクトリ。CLI サブコマンド、ACP builder、Codex/Ollama runtime、INDEX 更新、oracle review、session・worktree・state lifecycle などの外部挙動と制御契約を検証し、各機能の変更時に対応するテストを入口として参照する。

## Read this when
- cmoc の realization test を追加・修正・実行するとき。
- 特定機能の外部挙動、失敗条件、CLI lifecycle、runtime 契約をテストから確認するとき。
- 対応する実装変更の回帰範囲や、既存テストへケースを統合できるか確認するとき。

## Do not read this when
- 正本仕様や Structured Output schema の内容自体を確認・変更するときは、対応する oracle 文書・schema を直接読む。
- 実装の責務や内部構造を調査するときは、対応する src の実装ファイルを直接読む。
- Codex や Ollama の出力品質そのものを評価するとき。

## hash
- 4adfb7d32e3685f3333b35db20b2dc90a8dad25044f75ea074feb21887419241
