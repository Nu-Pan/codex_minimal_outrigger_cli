# `AGENTS.md`

## Summary
- cmoc 自己開発で恒常的に適用するリポジトリ固有の補足指示を定義する文書。動的生成プロンプトの権限・作業範囲は変更せず、Python 環境、設計、テスト、テスト実行に関する oracle file の参照先を案内する。

## Read this when
- cmoc リポジトリ自身の開発に関する作業を行うとき
- Python 環境や依存関係、realization implementation、realization test、品質検査の標準参照先を確認するとき
- 動的生成プロンプトとリポジトリ固有指示の関係を確認するとき

## Do not read this when
- 動的生成プロンプトが定める作業範囲・ファイルアクセス・oracle/realization 規則だけを確認したいとき
- 特定の実装やテストの詳細仕様を確認する必要があり、案内された oracle file を直接読むべきとき
- cmoc 自己開発に関係しない一般的な作業を行うとき

## hash
- 89bee9d7c2af278bbd665139abcc639290db77ce14190f9d84c74505d635448d

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
- Codex Minimal Outrigger CLI の概要、初期セットアップ、基本ワークフローへの入口、運用上の注意点を案内するプロジェクトの導入文書。リポジトリを初めて使う場合や開発環境を構築する場合の起点となる。

## Read this when
- プロジェクトの目的や略称を確認したいとき
- 初期セットアップ手順を確認したいとき
- 基本ワークフローの参照先を知りたいとき
- ターミナルロックなどの運用上の注意を確認したいとき

## Do not read this when
- 基本ワークフローの具体的な仕様や操作手順を確認したいときは、リンク先の仕様文書を直接読む
- 恒常的なリポジトリ開発ルールを確認したいときは、開発指示文書を直接読む

## hash
- 6b9b1484c0f145d96180325067b4b8552f696e6ed12e84990ab90ed87d713cb6

# `bin`

## Summary
- cmoc の CLI 起動用シェルラッパー。仮想環境 Python の存在・実行可能性を確認し、通常起動では不足時の標準エラー報告後に `src/main.py` を実行する。補完プローブ時は Python が利用可能な場合のみ転送する。CLI の起動経路、Python 検証、起動失敗時のエラー形式、補完時の挙動を確認・変更するときの入口。

## Read this when
- cmoc コマンドの起動処理や、仮想環境 Python の検証・エラー報告を調査するとき
- シェルラッパーから `src/main.py` への転送条件や、自動補完プローブ時の分岐を変更・確認するとき

## Do not read this when
- CLI の実際の引数処理やアプリケーション動作を調査するときは、直接 `src/main.py` または対応する仕様を読む
- エラー内容の正本仕様や初回セットアップ手順を確認するときは、参照されているエラー処理・開発環境の文書を直接読む

## hash
- 70422bb34b7732bfa99d94d395b5c91f9aba3302293f0edba8366c10e7645dfe

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
- cmoc の正本文書と oracle 実装をまとめる上位ディレクトリです。
- 意味仕様・開発規則・branch model・検討資料は doc、agent call 構築・prompt 生成・設定・パスモデル・構造化文書・feedback 処理の実装は src から確認します。

## Read this when
- cmoc の正本文書と oracle 実装のどちらを入口にするか判断するとき。
- 仕様領域または実装領域の下位ディレクトリへ進む前に、oracle 全体の構成を確認するとき。

## Do not read this when
- 確認対象の仕様文書や実装領域が明確で、doc または src 配下の対象を直接読めるとき。
- 実装の具体的な挙動、個別の agent call、または特定仕様の詳細だけを調べるとき。

## hash
- acc67dba53c97311d3bbc6245e5cc3ff895fe7409ca14d9b28d40e66bfbb1808

# `pyproject.toml`

## Summary
- Python プロジェクトのパッケージ metadata、依存関係、CLI エントリーポイント、ビルド設定、pytest・Ruff・mypy の開発ツール設定を定義する正本設定。Python パッケージ構成や開発・品質検査の実行条件を確認する入口となる。

## Read this when
- 依存関係、対応 Python バージョン、`cmoc` CLI の公開エントリーポイント、パッケージ配置、ビルド方式を確認するとき
- pytest、Ruff、mypy のプロジェクト共通設定や開発用依存関係を確認するとき

## Do not read this when
- CLI の具体的な処理やランタイム挙動を確認したいときは、実装モジュールを直接読む
- テストケースの内容や仕様上の期待動作を確認したいときは、該当する仕様・テストを直接読む

## hash
- 6fb45f79a560a43b8ae51d23bdb53e4dc711587caffea78ce1020d595036510e

# `src`

## Summary
- `src` は cmoc の実行側ソースルートであり、Typer CLI の最上位入口、互換 import shim、共通 runtime、基本型、ACP builder、サブコマンド実装をまとめる。
- `main.py` は doctor、tui、feedback、indexing、session、oracle、realization、run の CLI 入口を登録し、Typer/Click の互換処理と引数解析エラーの cmoc 形式への変換を担う。
- `commons` は CLI lifecycle、Codex 実行・TUI、設定、Git/worktree、path、state、logging、report、feedback など複数経路で共有する runtime helper の入口である。
- `acp` と `basic` は既存 import path を維持する互換入口であり、`acp` 配下には処理別 builder adapter、`basic` 配下には ACP 型・path model・構造化文書 API の入口がある。
- `sub_commands` は doctor、feedback、indexing、oracle、realization、review、run、session、tui のサブコマンド実装をまとめ、各処理の実行フローを下位対象へ分ける。
- `oracle.py` と `cmoc_runtime.py` は、それぞれ正本側 oracle package と `commons.cmoc_runtime` への互換 import を提供する薄い shim である。

## Read this when
- cmoc CLI の起動入口、サブコマンド構成、Typer/Click 互換境界を調査・変更するとき。
- 共通 runtime、互換 import、ACP builder、基本型、またはサブコマンド実装の担当領域を特定して下位対象へ進むとき。
- `acp.*`、`basic.*`、`cmoc_runtime`、または `oracle.*` の realization 側 import 経路を確認するとき。

## Do not read this when
- 特定サブコマンドの処理内容だけを調べるときは、`sub_commands` 配下の対応実装を直接読む。
- runtime helper、ACP builder、基本型、設定、または正本 oracle の詳細だけを確認するときは、対応する下位対象や正本実装を直接読む。
- CLI と無関係な正本仕様や利用側ロジックだけを調査するとき。

## hash
- 53370343427ac574045e68b2bdaf2268ebbbe1744ec782b87f40f2686a9355c7

# `test`

## Summary
- cmoc のテストスイート全体への入口。ACP builder、CLI、Codex runtime、doctor、indexing、oracle review、session、feedback、prompt、state、Git/worktree、通知など、実装領域ごとの外部契約・回帰条件を検証するテストを収録する。
- 対象機能の外部挙動や回帰条件を、個別テストへ分岐して確認するための上位ルーティング先。単体・統合・実経路受け入れ試験まで、機能境界に応じた検証入口を提供する。

## Read this when
- cmoc の既存挙動をテストから確認したいとき
- 変更対象の機能領域に対応する回帰テストや統合テストの入口を探すとき
- CLI、Codex 実行、worktree、Git、state、report、通知などの外部契約を検証するとき

## Do not read this when
- 正本仕様や実装責務そのものを確認したいときは、対応する oracle 文書または実装ファイルを直接読む
- Structured Output schema の項目・型・形式だけを確認したいときは、対応する schema を直接読む
- テスト実行方法や開発環境の共通手順だけを確認したいときは、該当する開発規定・テスト実行手順を読む

## hash
- 3f3a6ac1e3d49bef39a33a64e667f41a0bc39a75ba25ecf7276369f014c9439e
