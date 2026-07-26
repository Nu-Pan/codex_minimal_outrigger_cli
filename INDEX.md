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
- cmoc の実行用ソースツリー。CLI のエントリーポイント、サブコマンド、共通 runtime、ACP 互換 builder、設定・基本型・oracle 接続 shim を含む。各下位ディレクトリは担当領域ごとの実装へ進む入口となる。
- acp は ACP 互換公開入口と builder adapter を提供し、canonical な oracle builder への接続、prompt 補正、indexing・oracle・realization・session・TUI 向け parameter 構築を扱う。
- basic は ACP 型、path model、構造化文書 API の realization 側互換 import を提供する。
- commons は CLI lifecycle、Codex 実行、設定、Git、path、logging、state、run lifecycle、index 更新などの共通 runtime を提供する。
- config は設定型の realization 側互換入口を提供する。
- main.py は Typer による cmoc CLI の登録とサブコマンドへの委譲を担う。
- oracle.py は src 起動時に oracle/src/oracle を解決する package shim である。
- sub_commands は doctor、indexing、oracle、realization、run、session、TUI などの CLI サブコマンド実装をまとめる。

## Read this when
- cmoc CLI のコマンド登録、引数解析、completion、エラー変換を確認・変更するときは main.py を読む。
- 特定のサブコマンドの実行フローや状態・worktree 操作を調査するときは sub_commands と該当する下位実装を読む。
- Codex 実行、index 更新、設定、Git、path、logging、state、run lifecycle など複数機能にまたがる共通処理を調査するときは commons を読む。
- ACP parameter、互換 import、canonical oracle builder との接続、prompt のコードフェンス補正を確認するときは acp または basic を読む。
- src から oracle パッケージを解決する import 経路を確認するときは oracle.py を読む。

## Do not read this when
- 正本仕様や oracle 側の実装内容だけを確認したいときは、対応する oracle ツリーを直接読む。
- 単一サブコマンドの詳細実装が明確な場合は src 全体や commons 全体ではなく、該当する sub_commands 配下を直接読む。
- ACP や設定の互換入口に関係しない API の正本定義を確認するときは basic・config の shim を読む必要はない。
- 利用側の import や CLI 利用方法だけを調査するときは、対応する呼び出し元や利用者向け文書を直接読む。

## hash
- 91fa003c5dbd960ef4c8c298482bd10ddce3851275d1b078442ff6c1ead36601

# `test`

## Summary
- cmoc の realization test 一式を収録するディレクトリ。ACP builder、Codex runtime、CLI、indexing、oracle review、session lifecycle、設定・状態・path model など、実装の外部挙動と制御契約を検証する。個別機能の実装変更時は対応するテストファイルを入口にし、共通テスト基盤や実経路統合テストが必要な場合は専用の support・production test へ進む。

## Read this when
- cmoc の実装や仕様変更に伴う realization test の対象・検証範囲を探すとき
- CLI、Codex 実行、ACP builder、indexing、oracle review、session、runtime state などの回帰テスト入口を選ぶとき
- テスト用 Git・Ollama・Codex・外部コマンドの共通支援機能を確認するとき

## Do not read this when
- 正本仕様や schema の内容を確認・変更するときは、対応する oracle doc または oracle source を直接読む
- 実装詳細を調査するときは、関連する src 配下の realization implementation を直接読む
- LLM の回答品質自体を評価したいとき。このテスト群は主に外部挙動、状態遷移、制御ロジック、実行契約を検証する

## hash
- 0ea2933283a45cd0db4bb0c15484b8f6ba9272fe5e81d13e7fb969c1f5e580c5
