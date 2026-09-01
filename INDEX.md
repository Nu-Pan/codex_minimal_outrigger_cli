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
- cmoc の正本仕様・開発規則と oracle 実装群を束ねる上位入口。仕様領域では doc、agent call・prompt・設定・パス・構造化文書の実装領域では src 配下へ案内する。

## Read this when
- cmoc の仕様または oracle 実装について、目的に応じた下位文書・実装入口を判断するとき
- CLI、session／run、Codex、feedback、ログ、通知、branch／worktree 分離、Python 開発規則、agent call、prompt、設定・パス・構造化文書を横断して所在や責務の境界を確認するとき

## Do not read this when
- 特定の挙動仕様、branch model、Python 開発規則、agent call builder、prompt policy、設定クラス、パス解決、構造化文書モデルの詳細だけを確認したいときは、該当する下位対象を直接読む

## hash
- 2fb3131def0c44cef97897819a2574046bb3e4e7d4c150ab9b58c5ec64e0fe64

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
- cmoc の realization 側ソース全体の公開入口と実行経路を提供する。
- Typer による CLI ルート、互換 import shim、共通 runtime、ACP builder、サブコマンド実装、設定入口を横断して下位対象へ進むための起点。

## Read this when
- cmoc CLI の起動経路、サブコマンド登録、互換 import の配置、または共通 runtime の責務境界を確認するとき。
- ACP builder、設定、oracle package shim、サブコマンドなど、src 配下の複数領域にまたがる実装箇所を探すとき。
- 対象機能の個別実装へ進む前に、realization 側の公開入口と下位パッケージの構成を把握するとき。

## Do not read this when
- 特定のサブコマンド、runtime 機能、builder adapter、設定型、または oracle 正本の詳細実装をすでに特定しているときは、対応する下位対象や正本実装を直接読む。
- 正本仕様や src と無関係な処理だけを調べるとき。

## hash
- f57614489eeed377d522389c0fcbd63aa3e01387a17f82071d918179cec3b481

# `test`

## Summary
- cmoc の実装・CLI・Codex runtime・Git・state・report・通知などの外部挙動を検証する pytest テスト群を収録する。
- 共有 fixture・CLI runner・Git repository・fake command・Codex 環境などのテスト支援と、個別機能の回帰・統合・実経路テストへの入口を提供する。

## Read this when
- 複数の実装領域にまたがる外部契約や回帰条件を確認するとき。
- CLI の command tree、runtime、Codex 実行、indexing、session、oracle、feedback、editor handoff、report、通知などのテスト入口を探すとき。
- 実装変更に対応する pytest テスト、共有 fixture、実経路統合テストの範囲を判断するとき。

## Do not read this when
- 正本仕様、schema、実装本体の責務や詳細を確認することが目的のときは、対応する oracle または realization の対象へ直接進む。
- 特定機能のテスト契約が明らかな場合は、このディレクトリエントリーを経由せず該当する個別テストを読む。
- 一般的な pytest 実行方法だけを確認したいときは、テスト実行規則や専用の実行手順を読む。

## hash
- eb31779aef2972740611788c9cae87de6cb2f6377c758142ca881919f0267372
