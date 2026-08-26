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
- cmoc の正本ドキュメントと oracle 側の Python 実装をまとめた領域です。仕様・開発規約・branch model・代替案の背景は `doc`、agent call 構築・feedback・prompt 構築・設定やパス解決などの実装と Structured Output 定義は `src` が入口になります。

## Read this when
- cmoc の仕様または開発規約と、それを扱う oracle 側実装の対応関係を調査するとき
- 対象が `doc` と `src` のどちらにあるか未確定で、適切な下位ディレクトリへの入口を探すとき
- oracle の agent call、feedback、prompt、設定、構造化文書に関する領域全体を確認するとき

## Do not read this when
- 確認対象が個別の仕様書や開発規約として明確なときは `doc` 以下の該当文書を直接読む
- 確認対象が特定の oracle 実装や Structured Output 定義として明確なときは `src/oracle` 以下の該当責務を直接読む
- cmoc の realization 実装やテストの具体的な挙動だけを確認するときは、対応する realization または test の対象を直接読む

## hash
- e4012368b4c75ed22157c361d6814d911f951fb08e84c352e8cb17d84dda77ce

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
- `src` は cmoc の実行側コードをまとめるディレクトリ。Typer CLI の最上位入口、サブコマンド、共通 runtime helper、互換 import shim、ACP builder adapter を提供する。
- `main.py` が doctor、tui、indexing、feedback、session、oracle、realization、run の CLI コマンドを登録し、各サブコマンド実装へ振り分ける。
- `commons` は CLI・Codex・Git・設定・状態・feedback・report などから共有される runtime 処理の入口。`sub_commands` は個別 CLI 処理、`acp` は ACP 互換入口と builder adapter、`basic`・`config`・`cmoc_runtime`・`oracle.py` は既存 import 経路を維持する互換層を担う。

## Read this when
- cmoc の CLI 全体の起動入口、コマンド登録、または最上位の引数解析・エラー変換を確認するとき
- CLI の特定サブコマンド、共通 runtime 処理、ACP builder adapter の実装入口を特定し、対応する下位対象へ進むとき
- 既存の `acp.*`、`basic.*`、`config.*`、`cmoc_runtime`、`oracle.*` import の互換経路や移行境界を確認するとき

## Do not read this when
- 特定サブコマンドの業務ロジックや runtime helper の内部挙動だけを確認したいときは、`sub_commands` または `commons` 配下の対象を直接読む
- 正本仕様や canonical な oracle 実装の内容を確認・変更するときは、対応する oracle 側の仕様・実装を直接読む
- `src` の CLI、runtime、互換層、ACP adapter に関係しない処理を調査するとき

## hash
- 55f27ea584e60444be417dfdd3dd35541f51c60e57cfb5dae373e85420a8a1b6

# `test`

## Summary
- `test/` は、cmoc の realization test と共有 test helper を集約する検証ディレクトリである。ACP builder、Codex runtime、CLI lifecycle、indexing、oracle review、session/run state、feedback、Git/worktree、prompt、report、通知などの外部挙動・境界条件を、専用テストまたは統合テストとして検証する。
- 個別機能の実装変更では、その機能に対応する `test_*.py` を回帰条件と外部契約の入口として読み、複数の lifecycle や subsystem にまたがる変更では統合テストを入口にして関連する専用テストへ進む。
- `_*.py` の共有 helper は、ACP schema path、CLI doctor、Codex 実行、fake command、Git repository、pytest fixture など、複数テストが共通利用するテスト環境・呼び出し経路を確認するための入口である。

## Read this when
- cmoc の実装や仕様変更が、対応する realization test の外部挙動、エラー境界、永続状態、Git/worktree lifecycle、Codex 呼び出し、report、通知、または公開 import 契約に影響するとき。
- 複数のサブシステムをまたぐ CLI lifecycle、統合 run、oracle review、feedback、indexing、session、doctor の回帰条件を確認するとき。
- テストで使う共通の Codex runner、fake command、Git repository、schema path、doctor runner、toast fixture などの準備方法を確認するとき。

## Do not read this when
- 正本仕様、oracle schema、builder 実装、runtime 実装、または CLI 本体の責務・設計を確認することが目的のときは、対応する oracle または realization source を直接読む。
- 変更対象と無関係な機能領域のテストや、特定の単体ロジックだけを調べる場合は、このディレクトリ全体ではなく対応する専用テストまたは実装へ直接進む。
- テストの実行方法や品質検査の手順だけを確認したいときは、repository local の test execution 指示を読む。

## hash
- 770514acc0e1bfbbf8a5e28f2bc3ddbb1e6a4b90720d493c8426fed3d1fe1274
