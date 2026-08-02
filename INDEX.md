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
- Codex Minimal Outrigger CLI（cmoc）の概要、初期セットアップ、基本ワークフロー、ターミナル操作上の注意を案内するプロジェクト入口。開発環境の構築や利用手順を確認したい場合の起点となる。

## Read this when
- cmoc の目的や略称を確認したいとき
- リポジトリの初期セットアップ手順を確認したいとき
- 基本ワークフローの参照先や Ctrl+S によるターミナルロック対策を確認したいとき

## Do not read this when
- 個別機能の詳細仕様や実装を調べるとき
- 通常の開発ワークフローの詳細を確認するときは、案内されている usage 仕様を直接読むとき

## hash
- c9a65ea2bc4ae8a742a22e9ced541f459b3804a77b29a66a7a3513280711137a

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
- cmoc CLI の realization 実装をまとめるソースディレクトリ。CLI 起動、互換 import 入口、共通 runtime、サブコマンド、ACP builder adapter、設定入口を扱い、各機能の詳細は対応する下位ディレクトリまたはモジュールへ進んで確認する。

## Read this when
- cmoc の realization 側 CLI 全体の構成や主要な実装入口を確認するとき。
- CLI 起動処理、共通 runtime、サブコマンド、ACP builder、互換 import の配置先を特定するとき。
- 対象機能の実装へ進む前に、上位の委譲関係や公開入口を把握するとき。

## Do not read this when
- 正本仕様や oracle 側の実装内容を確認するとき。
- 特定のサブコマンド、runtime helper、builder の詳細を確認するときは、対応する下位項目または個別モジュールを直接読む。
- 実装と無関係なドキュメント、テスト、運用ルールを調査するとき。

## hash
- edaeb6eb0870f5a2b087552ddb82cedf0e1ff35f3c8140031f26f872b3710a3e

# `test`

## Summary
- cmoc の realization test を集約するディレクトリ。CLI、runtime、Codex 実行経路、ACP builder、indexing、oracle review、session/run lifecycle、設定・状態永続化などの外部挙動と契約を検証する。個別機能のテストを探す際の入口となる。

## Read this when
- cmoc の機能変更に対応する realization test、回帰テスト、統合テストを探すとき
- CLI、runtime、Codex、indexing、oracle review、session/run、設定・状態管理の期待挙動をテストから確認するとき
- テスト用の共有 helper や、Ollama を使う実経路テストの基盤を確認するとき

## Do not read this when
- 実装の責務や正本仕様そのものを確認するときは、対応する src または oracle の本文を直接読む
- 対象機能が明確な場合は、このディレクトリ全体ではなく対応する個別 test file を直接読む
- テスト実行の標準手順や品質ゲートだけを確認したいときは、対応するテスト実行規則を読む

## hash
- d06b7d96bb4115d2f2f0054c56b5f55acc605d7fbb8b505bb39a81c9937abd8b
