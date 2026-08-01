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
- cmoc の正本仕様と実装を集約する oracle ツリー。アプリケーション仕様・開発規則を扱う文書群と、設定、パス解決、構造化文書、プロンプト、ACP、レビュー、realization、INDEX 生成などの正本ソースを下位要素として提供する。

## Read this when
- cmoc の利用者向け挙動、状態管理、CLI、agent call、run/session lifecycle などの仕様を探すとき
- branch model、realization refactor、Python 開発環境、CLI 配置、realization test の規則を確認するとき
- 設定・パス解決・StructDoc・プロンプト構成・ACP・oracle review・realization・INDEX 生成の正本実装を調べるとき
- 複数の仕様領域にまたがる変更で、oracle doc と oracle src の参照先を切り分けるとき

## Do not read this when
- 特定の個別仕様や正本ソースの内容が明確で、下位の直接対象を読めば足りるとき
- oracle と realization の一般定義や共通原則だけを確認したいとき
- INDEX.md のルーティング方針自体を確認したいとき

## hash
- 1a81906a4a1727e3d5e9ea1cde94662656fe3b1cfeb6e313e7102439f54e9067

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
- cmoc の realization 実装本体。Typer CLI の起動・サブコマンド登録、互換 import shim、共通 runtime、ACP builder、oracle・realization・run・session・TUI などのサブコマンド実装をまとめる。各配下の具体的な処理へ進むための入口。

## Read this when
- cmoc の CLI 全体構成、公開サブコマンド、実行入口を確認・変更するとき。
- 共通 runtime、互換 import、ACP builder、またはサブコマンド realization の担当領域を特定するとき。
- 特定機能の実装を読む前に、該当する下位パッケージやモジュールへの入口を確認するとき。

## Do not read this when
- 正本仕様や oracle 側の実装を確認したいときは、対応する oracle 配下を直接読む。
- 特定サブコマンドや runtime helper の詳細を確認したいときは、該当する下位モジュールを直接読む。
- INDEX 更新処理そのものや、CLI と無関係な個別実装だけを調査するとき。

## hash
- bbfe73d4ae1b5fdde35d682272976ecba80bf1ec4e2ca21414ff1793bbdcfc92

# `test`

## Summary
- cmoc の realization test 群と共有テストヘルパーを収録するディレクトリ。ACP builder、Codex runtime、CLI、indexing、oracle review、session/run state、Git・設定・prompt などの外部契約と回帰挙動を検証する。各テストファイルおよび `_..._support.py` ヘルパーが個別領域の確認入口となる。

## Read this when
- cmoc のテスト対象や回帰テストの所在を探すとき
- CLI、Codex runtime、indexing、oracle review、session/run lifecycle、設定・状態永続化などの挙動を検証または変更するとき
- 複数テストで共有される Git、Codex/Ollama、外部コマンド、schema path などのテスト支援を確認するとき

## Do not read this when
- 正本仕様や schema の内容自体を確認するときは、対応する oracle doc・oracle src・oracle schema を直接読む
- 実装の責務や内部処理を調査するときは、対応する `src` の実装を直接読む
- テスト実行環境や品質検査手順だけを確認するときは、開発・テスト手順の文書を読む

## hash
- aed099d265c4fe352082ea02d71c27ecee7822af7897dc1972ffa326595b3d69
