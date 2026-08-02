# `AGENTS.md`

## Summary
- cmoc 自己開発における恒常的なリポジトリ固有指示を定める文書。動的生成プロンプトの権限・作業範囲を再定義せず、oracle file を優先する原則と、開発環境・設計・テスト・品質検査に関する参照先を示す。

## Read this when
- cmoc リポジトリ固有の開発ルールや、動的生成プロンプトとの関係を確認するとき
- Python 環境、依存関係、realization implementation、realization test、品質検査の進め方を判断するとき

## Do not read this when
- 具体的な実装仕様やテスト仕様そのものを確認したいとき
- 指定された開発作業の詳細が oracle file や repository local skill に直接定義されているとき

## hash
- b68df81da1c2ea21aea0a7fa9182c441085b2ebc1019ff01f7e172de6c61b126

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
- cmoc の実行入口を提供するシェルラッパーを含むディレクトリ。仮想環境 Python の存在・実行可能性を検査し、失敗時にはセットアップ手順と呼び出し位置を表示したうえで、成功時は src/main.py を起動する。

## Read this when
- cmoc コマンドの起動経路、仮想環境 Python の検査、補完プローブ、起動前エラー表示を確認・変更するとき。

## Do not read this when
- Python CLI 本体のコマンド処理や業務ロジックを確認したいとき。起動後の実装は src 側を直接読む。

## hash
- 464142724c5c5ed9b5dfec5aa77b6fb9e839c337859913d6ceced907ae5f5da9

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
- cmoc の正本仕様と、agent 呼び出し用パラメータの正本ソースを機能領域ごとに整理したディレクトリ。doc ではアプリケーション仕様・開発ルール・設計判断を、src では ACP 設定、パス・設定モデル、プロンプト、INDEX 生成、oracle review、realization 操作などの実装入口を扱う。

## Read this when
- cmoc の正本仕様、開発ルール、設計判断を確認するとき
- agent call のパラメータ、プロンプト構築、INDEX 生成、oracle review、realization 操作の正本ソースを調査するとき

## Do not read this when
- 具体的な realization 側の CLI 実装や実行フローだけを調査するとき
- 構築済み環境でのテスト、Ruff、mypy の実行手順だけを確認するとき
- 特定機能の実装詳細・テスト詳細や、一般的な CLI 入出力の細部だけを確認するとき

## hash
- 071f11dc2685edc2d63dab3e7fb0c068d5f5387a3e773037d7a3d06da36554e9

# `pyproject.toml`

## Summary
- プロジェクトの Python パッケージ設定。依存関係、開発用依存関係、`cmoc` CLI エントリーポイント、パッケージ配置、pytest・Ruff・mypy の設定を定義する。

## Read this when
- 依存関係や Python バージョン要件を確認するとき
- `cmoc` コマンドのエントリーポイントやパッケージ構成を変更するとき
- pytest、Ruff、mypy のプロジェクト設定を確認・変更するとき

## Do not read this when
- 個別の CLI 処理や実装ロジックを確認するとき
- テストケースや oracle の正本仕様を確認するとき

## hash
- 62c23b5f8693844b19076cbd7c8e2cc4930ace5468300a33c0b5ae87e3886d9f

# `src`

## Summary
- `acp` 公開 import 経路と `acp.builder` 配下の realization adapter を扱う。既存の `acp.*`／`acp.builder.*` 参照を canonical な `oracle.acp_builder` 実体へ委譲する互換入口と、quota probe、indexing、oracle、realization、session、TUI builder の下位領域への入口。

## Read this when
- `acp` または `acp.builder.*` の互換 import 経路を維持・廃止するとき。
- canonical な oracle builder への委譲や、builder adapter の配置・責務を確認するとき。
- quota probe、indexing、oracle、realization、session、TUI の builder 実装へ進む対象を選ぶとき。

## Do not read this when
- canonical な `oracle.acp_builder` の仕様・実装そのものを確認するとき。
- 個別 builder adapter の処理詳細を調査するときは、対応する下位モジュールを直接読む。
- `acp` 互換入口ではなく、CLI、runtime、または移行先の実体モジュールを直接調査するとき。

## hash
- 9e131b700e5ce8802dd59b08956a8a4a6a0da2a80bcfd97bef69f428b414e860

# `test`

## Summary
- cmoc の realization test 群を収めたディレクトリ。ACP builder、Codex runtime、CLI、indexing、oracle review、session、設定・状態管理などの外部挙動と制御ロジックを検証するテスト、および共有テストヘルパーを提供する。各機能領域の実装変更時に対応する回帰テストの入口となる。

## Read this when
- cmoc の実装変更に伴う realization test の追加・修正・対象テストの選定が必要なとき
- CLI、Codex runtime、ACP builder、indexing、oracle review、session、runtime 設定・状態などの外部挙動を検証するとき
- テスト用 Git リポジトリ、Codex 環境、Ollama、fake external command など共有テスト基盤を確認するとき

## Do not read this when
- 正本仕様や schema の内容を確認するときは、対応する oracle 文書・oracle source・schema を直接読む
- 実装の責務や内部処理だけを変更・調査するときは、対応する realization implementation を直接読む
- 対象領域と無関係なテストや、テスト実行手順そのものだけを確認するときは、このディレクトリ全体ではなく repository local のテスト手順を読む

## hash
- 10a3737482ea960c56940edbb85c9943cfc8e432d06d41c2ad241d6f67978f46
