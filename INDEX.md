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
- 仮想環境内の Python を検証し、cmoc の Python CLI 本体へ委譲する起動ラッパーを含む。通常実行時のエラー表示、補完プローブ、ユーザー向けパスとコールスタック行番号の組み立てを扱う。cmoc の起動経路やラッパーの表示・エラー処理を確認する際の入口。

## Read this when
- cmoc の起動経路、仮想環境 Python の検証、補完プローブ、ラッパーのエラー出力や表示パスを確認・変更するとき。

## Do not read this when
- Python CLI 本体のコマンド挙動やドメインロジックを調べるときは、委譲先の実装を直接読む。開発環境の正本仕様を確認するときは、参照されている oracle 文書を読む。

## hash
- 2b049993c6378dede2a9d759c9dd13b8795479d1bc900a42c174e227e8ce2e0b

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
- CLI 起動用の realization 実装をまとめる領域。Typer の主要エントリーポイント、サブコマンド実装、ACP 互換公開入口、共通 runtime、設定・oracle の互換 shim を扱う。CLI 全体の構成や実行入口を確認した後、個別機能は対応する下位要素へ進むための起点となる。

## Read this when
- cmoc の CLI 登録、サブコマンドへの委譲、引数解析や自動補完の挙動を調査・変更するとき。
- doctor、indexing、tui、session、run、oracle、realization などのサブコマンド実装への入口を探すとき。
- ACP、設定、oracle パッケージ、共通 runtime の realization 側互換入口や横断基盤の構成を確認するとき。

## Do not read this when
- 特定サブコマンドの処理詳細を確認したい場合は、サブコマンド配下の該当実装へ直接進む。
- 共通 runtime helper、設定定義、oracle の正本実装、ACP builder の個別挙動を確認したい場合は、それぞれの直接の実装または oracle 側定義を読む。
- CLI や互換入口と無関係な仕様・実装を調査するとき。

## hash
- 97c036a2705f6d7c78502ea6f061c6b44d7c0630e43fa38c608c396729c0c2cb

# `test`

## Summary
- `test` ディレクトリは、cmoc の realization test を集約する。CLI の各サブコマンド、runtime、Codex 実行経路、Git・worktree・state・config、indexing、oracle review、prompt、builder、packaged import などの外部挙動と境界条件を検証する。個別機能の回帰テストや統合テストへ進むための入口である。

## Read this when
- cmoc の実装変更に対応する realization test、回帰テスト、統合テストの対象を探すとき。
- CLI、Codex runtime、worktree・state・Git、indexing、oracle review、prompt、builder、設定などの外部契約や境界条件を検証するとき。
- 実装変更後に、対象機能に対応する既存テストと検証範囲を確認するとき。

## Do not read this when
- 正本仕様、schema、prompt 規則、実装詳細そのものを確認することが目的のときは、対応する `oracle` または `src` のファイルを直接読む。
- テスト実行手順だけを確認したいときは、テスト実行用の正本仕様を読む。
- 対象機能と無関係なテストを総覧する必要がないときは、このディレクトリ全体ではなく対応する個別テストへ直接進む。

## hash
- 905ab8d30ebed765651fa14935ba834ce43e2e0a553843dfd9f7f1cf05edb6e2
