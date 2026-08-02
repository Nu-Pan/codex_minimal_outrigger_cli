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
- cmoc の人間所有の正本仕様を集約するディレクトリ。アプリケーション共通仕様、branch・commit・worktree モデル、開発規則、不採用案の検討記録、および参照可能な正本ソースを扱う。仕様領域ごとの文書・ソースへ進むための入口。

## Read this when
- cmoc の正本仕様や正本ソースを探すとき
- アプリケーション挙動、branch・worktree lifecycle、開発規則、テスト・環境構築、設定・パスモデル、規範モデル、構造化文書生成の仕様を確認するとき
- 特定の仕様領域に対応する下位ディレクトリを選ぶとき

## Do not read this when
- 確認対象の具体的な仕様文書や正本ソースがすでに特定されているとき
- realization 実装、具体的なテスト実行、一般的な開発作業だけを調査するとき

## hash
- e908e48f3d2933a9d3a3ec6655628c93423376d399fe6ab681f97692ae241f56

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
