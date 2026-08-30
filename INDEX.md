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
- cmoc の正本文書群です。アプリケーション仕様、branch・run の分離モデル、不採用案の背景、実装・環境・テストの開発ルールを扱います。
- cmoc の agent call 構築実装と、その prompt、アクセス制御、Structured Output、設定、パス解決、構造化文書レンダリングを扱います。

## Read this when
- cmoc の機能仕様、状態遷移、session／run の branch・worktree 分離、不採用案、実装・開発環境・テストのルールを確認するとき。
- agent call の prompt、cwd、ファイルアクセス、Structured Output、サブコマンド別の起動定義、構造化文書モデルの実装箇所を探すとき。

## Do not read this when
- 具体的な実装コードやテストの挙動だけを確認する場合は、対応する realization file やテストを直接読む。
- 個別仕様や開発ルールが特定できている場合は、文書群全体ではなく該当する下位文書を直接読む。
- agent call の実行本体やサブコマンドの業務ロジックだけを確認する場合は、対応する実行処理を直接読む。

## hash
- a2a89b7813656d75fbdc2e39320eef2033cdd4b4513257845abf9309046c6059

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
- cmoc の実装側ソースツリー。CLI の起動入口、共通 runtime、互換 import shim、設定公開面、ACP adapter、各サブコマンド実装をまとめ、個別処理の実装へ進む入口を提供する。

## Read this when
- cmoc の CLI 起動経路、サブコマンド配置、共通 runtime、互換 import、または処理領域別の実装入口を特定するとき。
- 対象機能の実装場所が不明で、`main.py`、`commons`、`acp`、`basic`、`config`、`sub_commands` などの下位対象へ振り分ける必要があるとき。

## Do not read this when
- 特定機能の内部挙動、正本仕様、設定型、または oracle 側の実装だけを確認したいときは、対応する下位実装・oracle・仕様定義元を直接読む。
- 個別サブコマンドの処理内容が明確な場合や、`src` 配下と無関係な repository 文書・テストだけを調査するとき。

## hash
- e493350333f20b1e9efc800789377ab1aef121a84606e337cff8e6f5c7264db0

# `test`

## Summary
- pytest による cmoc のテスト群をまとめたディレクトリ。ACP builder、CLI、Codex runtime、Git・state・report、indexing、oracle review、session、realization などの単体・統合・実経路テストを、実装や仕様を確認するための機能別入口として提供する。
- 特定機能の外部挙動、異常系、永続状態、worktree lifecycle、Codex 呼び出し契約、または複数機能の統合結果をテストから確認する際の入口となる。

## Read this when
- cmoc の実装変更や仕様確認に対する回帰テストの入口を、機能領域別に探すとき
- CLI、Codex runtime、ACP builder、indexing、oracle review、session、realization、feedback などの外部契約や統合挙動を検証するとき
- テスト用の共通 fixture・helper、実経路統合テスト、または特定機能の異常系テストを探すとき

## Do not read this when
- 正本仕様や実装そのものの意味・詳細を確認することが目的で、対応する oracle 文書または realization 実装を直接読む方が適切なとき
- テスト対象に含まれない機能や、一般的な pytest 実行手順だけを確認したいとき
- 特定の単一機能について、同階層のテスト群ではなく対応する実装・schema・仕様ファイルを直接確認すべきとき

## hash
- 36f5273fd817bcbe00ee8ae3f9b36b4a0e2b9a76b4a2d9933c5731902c2a03cc
