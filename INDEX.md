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
- cmoc コマンドの実行ラッパー。仮想環境の Python を検証し、通常実行では CLI 本体へ引数を渡す。仮想環境が使えない場合の案内と、シェル補完プローブ時の実行可能性確認を扱う。

## Read this when
- cmoc の起動経路、仮想環境 Python の検証、起動失敗時のエラー表示、シェル補完プローブの挙動を確認するとき。

## Do not read this when
- cmoc のサブコマンドや CLI 本体の処理内容を確認するときは、CLI 本体の実装を直接読む。
- Python 仮想環境の作成、依存関係、開発環境の正本仕様を確認するときは、対応する oracle ドキュメントを読む。

## hash
- 9a9a99329708cba2a6d2e35d6a087d2b5b3f3a130027abbf4b6a5fa0696e1e35

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
- cmoc の正本仕様ファイルを集約するディレクトリ。CLI 自動補完、Codex CLI 呼び出し、ログ、doctor preprocess、プロンプト、run・session lifecycle、サブコマンドなど、複数機能にまたがる仕様確認の入口を提供する。
- 下位の doc は自然言語による仕様、src は正本ソースを扱う。特定機能の詳細や個別定義を調べる場合は、該当する下位ディレクトリまたはファイルへ進む。

## Read this when
- cmoc の正本仕様を横断的に探すとき
- CLI 起動、Codex CLI 呼び出し、ログ、プロンプト、run・session lifecycle、サブコマンドなどの仕様の入口を確認するとき
- 正本ソースの責務分担や、エージェント呼び出し・設定・パス・構造化文書・プロンプト関連の下位領域を確認するとき

## Do not read this when
- 特定機能の詳細仕様や個別定義が明らかなとき
- realization の実装・テスト詳細だけを調査するとき
- cmoc の一般的な利用手順だけを確認するとき

## hash
- 6877728871b1241f4ff9e1a35daadd176707bd10caacf4aeefb6c43e9b318157

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
- cmoc CLI の realization 実装をまとめる `src` のルート。Typer による CLI エントリーポイント、互換 import shim、共有 runtime helper、ACP builder、各サブコマンド実装を下位要素への入口として提供する。

## Read this when
- cmoc の CLI 全体の登録・委譲構造を確認したいとき。
- session、oracle、realization、run、doctor、indexing、tui などのサブコマンド実装の配置を探すとき。
- 共有 runtime、ACP builder、互換 import の実装へ進む入口を確認したいとき。

## Do not read this when
- 特定サブコマンドの処理詳細を調査・変更したいときは、対応する `sub_commands` 配下を直接読む。
- 共有 helper の個別仕様や実装詳細を確認したいときは、対応する `commons` 配下を直接読む。
- oracle の正本仕様や canonical 実装の内容を確認したいときは、`oracle` 配下を直接読む。
- 特定の ACP builder の生成ロジックだけを調査したいときは、対応する `acp/builder` 配下を直接読む。

## hash
- b0b824e00be32c86e4cf2d012c0b1b952022b02136b1f0f26268329b046592e2

# `test`

## Summary
- テスト共通ヘルパー、ACP builder、Codex runtime、CLI、indexing、oracle review、session、state など、cmoc の実装・CLI・統合動作を検証する pytest テスト群を収録する。各テストファイルは対応する機能の外部契約や制御ロジックを確認する入口となる。

## Read this when
- cmoc の実装変更に対して、対応する外部挙動・制御ロジック・回帰テストの所在を探すとき
- CLI、Codex runtime、ACP builder、indexing、oracle review、session、state、worktree のテストを追加・修正するとき
- テスト共通の Git、Ollama、Codex、CLI 実行ヘルパーの責務を確認するとき

## Do not read this when
- 正本仕様や実装そのものを確認したいときは、対応する oracle または src のファイルを直接読む
- 特定機能と無関係なテストを調査するとき
- LLM の回答品質自体を評価したいとき

## hash
- f2c858d7419c08ce6a6e8f3bb77bae9c5ad99474e625f96163d484cc3c4d5fbb
