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
- cmoc の正本仕様と共通実装を収める oracle の入口。アプリケーション仕様は `doc`、ACP builder・prompt builder・設定・パス解決・構造化文書基盤は `src` へ進む。

## Read this when
- cmoc の正本仕様や共通 oracle src の所在を確認するとき。
- アプリケーション仕様と共通基盤のどちらを読むべきか判断するとき。

## Do not read this when
- INDEX.md の自動生成・更新規則だけを確認するとき。
- Python 実行環境、設計ルール、テスト手順などの開発規則だけを確認するとき。
- 対象機能が明らかで、`doc` または `src` の下位対象を直接読めるとき。

## hash
- 157dac4912ece0467ddc624911775416001678918766d5f404ebdab319494417

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
- `acp` は既存の `acp.*` 参照を維持する互換入口で、`oracle` 側の canonical 実装や builder 群への移行経路を扱う。
- `basic` は ACP 型、path model、構造化文書 API を canonical 実装から再公開する互換入口で、実装や正本仕様は複製しない。
- `cmoc_runtime.py` は `commons.cmoc_runtime` の公開名を再公開する互換 import shim。
- `commons` は CLI、Codex、設定、Git、path、logging、state、Ollama、INDEX 更新などの共通 runtime 実装をまとめるパッケージ。
- `config` は canonical 設定定義を再公開する互換 import 入口。
- `main.py` は Typer ベースの cmoc CLI ルートで、共通エラー変換、トップレベル command、session/apply/review command、起動入口を定義する。
- `oracle.py` は `src` 単体起動時に `oracle.*` パッケージを解決する互換 package shim。
- `sub_commands` は session、apply、review、indexing、doctor、eval-oracle、TUI などの CLI サブコマンド実装をまとめる領域。

## Read this when
- `acp.*`、`basic.*`、`config.*`、`cmoc_runtime` の公開 import 互換性や canonical 実装への移行を調べるとき。
- 共通 runtime helper の実装や、複数サブコマンドにまたがる CLI・Codex・Git・state・logging の影響を確認するとき。
- cmoc の command 階層、option、Typer/Click のエラー処理、CLI 起動入口を変更・調査するとき。
- session、apply、review、indexing、doctor、eval-oracle、TUI の実行フローや状態操作を調べるとき。
- `src` 起動時の `oracle.*` パッケージ解決を確認するとき。

## Do not read this when
- 互換入口の内部実体、canonical builder、設定仕様、構造化文書仕様の詳細だけを確認したいときは、対応する定義元を直接読む。
- 特定の runtime helper やサブコマンド単体の実装だけを調査するときは、該当する個別モジュールを直接読む。
- oracle の正本仕様や oracle 側実装を確認するときは、`oracle` ツリーを直接読む。
- CLI の公開入口やサブコマンド接続と無関係な新規 API・設計を検討するとき。

## hash
- 2c56a7a3f75f848c62c0fe2b7e6e391ac63873ab72eed849ebfef794b0e41f21

# `test`

## Summary
- cmoc の pytest テスト群を集約するディレクトリ。ACP builder、CLI サブコマンド、Codex runtime、indexing、review oracle、session/apply、設定、worktree、Ollama などの外部挙動・制御契約を検証し、各機能別テストと共有テスト補助を下位要素への入口として提供する。

## Read this when
- cmoc の機能変更に対応する回帰テストや契約テストを探すとき
- CLI、Codex runtime、indexing、review oracle、session/apply、設定、worktree、Ollama、ACP builder の挙動をテスト観点から確認するとき
- テスト用の共有 Git・Ollama・Codex・CLI 補助を利用または変更するとき

## Do not read this when
- 正本仕様や schema の内容自体を確認するときは、対応する oracle 文書・schema を直接読む
- 実装詳細だけを確認するときは、対応する src の実装を直接読む
- 対象機能と無関係なテストや共有補助を読む必要がないときは、このディレクトリを入口にしない

## hash
- de6e517ef1a053d95f78e7a5fc35cce0103e28510a3953ec022c59fc914a3929
