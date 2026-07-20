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
- cmoc の正本仕様を担う oracle 文書・ソース群への入口。アプリケーション仕様、開発規約、ACP builder、プロンプト生成、TUI、oracle review、realization・session 処理、設定・モデル・ルート探索などを扱う。
- 配下の doc と src から、共通仕様・開発方針および正本ソースの責務別実装へ進むためのルーティング起点となる。

## Read this when
- cmoc の共通仕様、CLI 利用者向け挙動、状態管理、ログ、プロンプト、run/session lifecycle を確認するとき
- session fork、run の隔離、branch・commit・worktree、基準 commit の関係を調査するとき
- Python 実装規約、CLI の責務配置、開発環境、pytest 方針を確認するとき
- ACP 呼び出し、TUI、oracle・realization 操作、設定、ルート探索、構造化文書や完全なプロンプト生成の正本実装を探すとき
- realization refactor や不採用設計案の理由を調査するとき

## Do not read this when
- 特定の realization code または realization test の内部実装だけを調査するとき
- 個別機能の具体的な挙動・出力仕様を確認するときは、doc/app_spec 配下の対応文書を直接読むとき
- 単一のプロンプト部品、特定の ACP 呼び出しパラメータ、個別の標準文書だけを調べるときは、対応する下位対象を直接読むとき
- 一般的な INDEX.md の読み方やルーティング方針を確認するとき

## hash
- 221d37c212a9323de33595c30495e6e44af426e1cf6460b8a177d7d70251486e

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
- cmoc の realization 実装ルート。Typer CLI の起動入口、互換 import shim、共通 runtime helper、CLI サブコマンド実装を含む。
- CLI 入口から doctor・indexing・tui、session／oracle／realization／run の各ワークフローへ委譲し、共通処理は Codex 実行、Git、設定、状態、パス、ログ、結果、INDEX 更新などの runtime module に分担されている。
- acp・basic・config・cmoc_runtime・oracle の各 shim は既存 import 経路を保ち、canonical な oracle または共通実体を再公開する。具体的な機能変更では、対応するサブパッケージまたは runtime module が下位要素への入口になる。

## Read this when
- cmoc CLI のトップレベル構成、サブコマンド登録、起動時の引数エラー処理を確認するとき。
- 特定の session・oracle review／edit／investigation・realization apply／refactor・run lifecycle の実行フローを調査・変更するとき。
- 共通 runtime helper の配置や、互換 import shim から canonical 実装への委譲関係を確認するとき。

## Do not read this when
- 個別 runtime helper の詳細だけを確認したいときは、対応する commons module を直接読む。
- canonical な正本仕様や oracle 実装そのものを確認したいときは、oracle 配下を直接読む。
- 特定サブコマンドの内部処理だけを調査するときは、対応する sub_commands 配下へ直接進む。

## hash
- 607df3687b88c449341de20977bc7a5af8fd1d4d00133239a867c079fc55915c

# `test`

## Summary
- cmoc の realization test を集約するディレクトリ。ACP builder、Codex 実行、CLI、doctor、indexing、oracle review、session/run state、設定、prompt、worktree などの外部挙動・制御ロジックを検証する。個別機能の回帰テストや共通テスト支援を探す入口であり、実装や正本仕様そのものは対応する src または oracle を読む。

## Read this when
- cmoc の realization test を追加・修正・調査するとき
- 対象機能の外部挙動、CLI lifecycle、Git/worktree 副作用、Codex subprocess、状態遷移の検証範囲を把握するとき
- 共通テスト支援や、対象機能に対応する既存テストを探すとき

## Do not read this when
- 実装の責務や内部処理を確認するときは、対応する src の実装を直接読む
- 正本仕様、schema、prompt、file access 規則を確認するときは、対応する oracle file を直接読む
- テスト対象が明確な場合は、このディレクトリ全体を読むのではなく該当するテストファイルへ進む

## hash
- 990ceb4b84649efb4df5d029528bb418adaff7ab960db23ac54441feb6dd242d
