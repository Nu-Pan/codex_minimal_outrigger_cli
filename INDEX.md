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
- cmoc の正本仕様を収録するディレクトリ。機能仕様、ライフサイクル、ブランチモデル、INDEX 生成、開発環境・CLI・テストなどの開発規約を確認するための入口。
- CLI、Codex 呼び出し、ログ、doctor、prompt、run/session、branch model、INDEX 生成、Python 開発規約などの個別仕様は doc へ、agent call パラメータ、パス解決、プロンプト構築、INDEX 生成や realization 操作の正本ソースは src へ進む。

## Read this when
- cmoc の機能・共通仕様や個別 oracle doc の所在を確認するとき
- branch・commit・worktree、session・run の関係やライフサイクルを調査するとき
- Python 開発、CLI 設計、開発環境、pytest などの開発規約を確認するとき
- agent call の設定・パス解決・prompt 構築・INDEX 生成・oracle review・realization 操作の正本ソースを探すとき

## Do not read this when
- 既に確認対象の仕様文書や開発規約文書が特定できており、その本文だけで目的を満たせるとき
- 実装構造やテスト実装、一般的な Codex CLI・model provider の仕様を直接調査するとき
- 既存の INDEX.md のルーティングだけを更新するとき

## hash
- 91d04de8eeb1114758d97aa495cb405bac04a4095519565a0386adb71ff71988

# `pyproject.toml`

## Summary
- プロジェクトの Python パッケージメタデータ、依存関係、CLI エントリーポイント、ビルド設定を定義する設定ファイル。pytest・Ruff・mypy の実行対象や Python バージョン要件も確認できる。

## Read this when
- 依存関係、対応 Python バージョン、`cmoc` コマンドのエントリーポイント、パッケージ探索、ビルド設定を確認するとき。
- pytest・Ruff・mypy のプロジェクト共通設定や GPU integration テストのマーカーを確認するとき。

## Do not read this when
- CLI の具体的な処理や実装責務を確認したいときは、`src` 配下の実装を直接読む。
- 正本仕様や開発環境・テスト手順を確認したいときは、`oracle` 配下の該当文書を読む。

## hash
- b2f7a17a58e3aa7aac375d93ebf50b342e13e74c4e9bc5ba3b6e8fd88b78edd4

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
- `test` ディレクトリは、cmoc の実装に対する pytest テスト群と共有テストヘルパーをまとめた検証領域です。ACP builder、Codex runtime、CLI、indexing、oracle review、session、state、config、Git、TUI などの外部挙動・制御ロジックを対象とし、個別機能の回帰テストから実 Codex CLI を使う受け入れテストまでを含みます。機能領域ごとのテストファイルが、対応する realization implementation や oracle 仕様を確認する入口になります。

## Read this when
- cmoc の機能変更に対して、該当する外部挙動・制御ロジックのテストや回帰範囲を特定するとき
- ACP builder、Codex runtime、CLI、indexing、oracle review、session、state、config、Git、TUI などのテスト対象を探すとき
- 実装変更後の統合テスト、実経路テスト、または受け入れテストの入口を確認するとき
- 共通テストヘルパー、test-local Ollama、Git fixture、fake external command の利用方法を確認するとき

## Do not read this when
- 正本仕様や Structured Output schema の内容を確認するときは、対応する oracle 文書・schema・oracle source を直接読む
- 実装の責務や内部設計を変更・調査するときは、該当する src 側の realization implementation を直接読む
- テスト対象と無関係な機能の挙動を調べるときは、このディレクトリを総覧せず、該当する機能別テストへ直接進む
- Codex や LLM の回答品質そのものを評価するときは、実経路テストの品質判定を目的にしない

## hash
- 1a59ea61fe24ecaf0b889c90c2c97f08dfc455064eda2fa55a645449bbea8e0d
