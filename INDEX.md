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
- cmoc の正本仕様・開発規則・運用モデル・設計判断を目的別に案内する文書群の入口。
- アプリケーション仕様や開発ルールなどの正本文書は doc 配下へ、実装・prompt・agent call の処理詳細は src 配下へ進むための起点。

## Read this when
- cmoc の仕様、開発・テスト規則、session/run の隔離モデル、または不採用設計を調査するとき。
- agent call の prompt 構築、Structured Output、feedback、oracle／realization、INDEX.md 生成などの実装文書を探すとき。

## Do not read this when
- 特定機能の仕様本文、開発環境やテスト実行、branch model の具体的契約など、担当する下位文書が明らかなとき。
- 実際の Codex CLI 起動・TUI 実行制御や、個別 schema の詳細を直接確認すべきとき。
- 実装ファイルやテストの具体的な挙動だけを調べるとき。

## hash
- 9c8225c8fdcb71e29afb9d35dda0b665ea834a59ce25be437aa6fb124deb9bef

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
- cmoc の runtime、CLI、Codex 実行、ACP builder、各サブコマンドの外部契約を検証する回帰・統合テスト群と、テスト環境を隔離する共有 helper の入口。
- 実装や正本仕様の変更に対して、終了結果、永続状態、Git/worktree、agent call、report、prompt、path 境界など観測可能な挙動を確認する。

## Read this when
- cmoc の CLI または runtime の外部挙動を変更・検証するとき
- Codex 実行、ACP builder、prompt、file access、worktree、Git、report、state、feedback の契約をテストから確認するとき
- 複数のサブコマンドや共通 runtime にまたがる統合 lifecycle を調査するとき
- テスト用の Git repository、fake external command、Codex 環境、CLI 実行、toast 隔離など共有 test helper の利用方法を確認するとき

## Do not read this when
- 実装責務、正本仕様、schema、prompt 本文、または個別機能の設計を確認することが目的のときは、対応する src または oracle の対象を直接読む
- テスト対象の一機能だけを確認できる専用テストや下位対象が明確なときは、このディレクトリ全体を読む必要はない
- テスト実行手順だけを確認するときは、repository local の test_execution skill を読む

## hash
- 3344040bef5b1ee7c04d9d12a3edcf2cf9840e5e671c4ce416ea05a56661b179
