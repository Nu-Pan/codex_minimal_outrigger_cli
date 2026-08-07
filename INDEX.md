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
- cmoc の人間所有の正本ツリー。アプリケーション横断仕様、branch・commit・worktree モデル、開発規則、不採用案の検討記録を文書として扱い、Agent-call の共通設定・用途別設定・実行条件・Structured Output schema をソースとして定義する。配下の doc と src が、それぞれ仕様文書と実装定義を確認する入口になる。

## Read this when
- cmoc の正本仕様や開発規則を探すとき
- 複数領域にまたがる仕様文書の所在を確認するとき
- Agent-call の共通設定、用途別 prompt・起動設定、モデル・権限・作業ディレクトリ、Structured Output schema の定義を調査するとき
- 採用済み仕様と不採用案の検討記録を区別して参照するとき

## Do not read this when
- 単一機能の正本仕様や特定用途の prompt・schema が明確で、下位文書や下位ソースへ直接進めるとき
- 具体的な realization 実装の配置やテスト実行方法を確認するとき
- CLI・TUI の実行フローや通常の realization 実装・テストだけを調査するとき

## hash
- b887027971e8b19919dac7fa7c442e1d7787f1d456f7840f89c0acc3d8ffb9a7

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
- cmoc の realization 実装をまとめる src パッケージ。CLI のトップレベル入口、サブコマンド、共通 runtime、互換 import shim など、実行時コードの主要な入口を提供する。
- CLI 全体の command tree を確認する場合はトップレベル入口へ、特定サブコマンドや共通処理を調べる場合は対応する下位ディレクトリ・モジュールへ進むための起点となる。

## Read this when
- cmoc の realization 側実装の構成や、CLI 実行コードの入口を確認するとき。
- トップレベル CLI、サブコマンド、共通 runtime、互換 import 層のいずれかを調査・変更するとき。
- 対象となる下位実装へ進む前に、src 内の責務分担と適切な入口を選びたいとき。

## Do not read this when
- 正本仕様、canonical 実装、または oracle 側のテストを確認したいときは、src ではなく対応する oracle 配下を直接読む。
- 特定モジュールの詳細な挙動やアルゴリズムだけを確認したいときは、src 全体ではなく該当する下位要素を直接読む。
- 利用者向け文書やテスト内容だけを調べるとき。

## hash
- 7227c79badb43afb9365deab4d77e22aed53758b10eb81b7fc7ab393162a5c97

# `test`

## Summary
- test 配下の pytest realization test 群と共通 test helper を、機能領域ごとの外部挙動・契約・回帰検証の入口として案内する。CLI、Codex runtime、indexing、oracle review、session、設定・状態永続化などのテスト対象へ進むためのルート。

## Read this when
- cmoc の外部挙動や回帰条件をテストから確認したいとき
- 特定の機能領域（CLI、Codex、indexing、oracle review、session、runtime、設定、状態など）のテスト入口を探すとき
- 共通 fixture、fake command、Git repository、Ollama、Codex 用 test helper の責務を確認したいとき

## Do not read this when
- 正本仕様、schema、実装詳細を確認したいときは、対応する oracle または src の対象を直接読む
- pytest の一般的な実行方法だけを確認したいときは、テスト実行ルールを読む
- 対象機能と無関係なテスト領域や個別 helper を調べるときは、このディレクトリ全体ではなく該当テストを直接読む

## hash
- 7018ddcf119dd7bfdd699fe9b55ccef3248e4bd13f838b99430aa21ae980a3de
