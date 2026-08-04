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
- 人間が所有する cmoc の正本仕様を収める領域。CLI の挙動、Codex 連携、プロンプト、session・run の状態と隔離、ログ・エラー処理、branch・commit・worktree モデル、開発・テスト規則、採用しなかった設計案を扱う。
- 自然言語の仕様文書はアプリケーション仕様、開発規則、branch model、代替案に分かれ、正本ソースは agent 呼び出し、プロンプト生成、設定、パス、構造化文書、レビュー・ルーティング規範を定義する。各下位領域の詳細を確認するための入口となる。

## Read this when
- cmoc の正本仕様を横断的に調査・変更・レビューするとき。
- CLI、Codex 連携、session・run、ログ、エラー処理、プロンプト、インデクシングの仕様を確認するとき。
- Python 開発環境、設計、コーディング、テスト規則やテスト実行手順を確認するとき。
- session・run に関わる branch、commit、worktree の関係を確認するとき。
- 採用されなかった作業方式や設計案の背景・不採用理由を確認するとき。
- agent 呼び出しパラメータ、共通設定、パスモデル、構造化文書、プロンプト部品の正本定義を確認するとき。

## Do not read this when
- 特定のアプリケーション仕様、開発規則、branch model、代替案、または正本ソースの本文を直接確認できる場合。
- 実装構造、realization 側のコード、テストコード、具体的なテスト結果を確認するとき。
- cmoc の利用手順だけを確認するときは、利用手順に対応する仕様文書を直接読む。
- INDEX.md の生成・更新規則そのものを確認するとき。

## hash
- bc529f41e2ab627cc88356b97defa62cdc35eaf7f90eaee2031b5fc3c2a1782b

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
- `src` は cmoc の realization 実装を配置する Python ソースツリーで、CLI エントリーポイント、サブコマンド、共通 runtime、互換 import shim を含む。
- CLI 全体の登録と委譲は `main.py`、サブコマンド実装は `sub_commands`、横断的な runtime 処理は `commons` を入口とする。
- `acp`、`basic`、`config`、`cmoc_runtime.py`、`oracle.py` は既存の import path や正本側 package を接続する互換入口である。

## Read this when
- cmoc の realization 実装全体の構成や、CLI の起動入口を把握するとき。
- CLI の登録・引数処理・サブコマンド委譲を確認するとき。
- 共通 runtime の構成、または既存 import path の互換維持・移行状況を調査するとき。

## Do not read this when
- 特定サブコマンドや runtime helper の詳細だけを確認したい場合は、対応する下位実装を直接読む。
- 正本仕様や oracle 側の実装内容を確認する場合は、`oracle` ツリーの対応文書・ソースを直接読む。
- CLI や realization 実装と無関係な利用者向け公開面を調査する場合は、このツリーを入口にしない。

## hash
- 644a4c575504ad15a2ac49a5231c8a83b4db523c26a67f3703962ed618492f67

# `test`

## Summary
- realization test を集約するディレクトリ。ACP builder、runtime、CLI、indexing、oracle review、session、state、Codex 実行経路など、実装の外部挙動・契約・境界条件を検証するテストを扱う。
- 個別機能の実装変更時に、その外部挙動や回帰検証の入口として下位の専用テストへ進むための起点となる。

## Read this when
- 実装変更に対応する既存の realization test、回帰テスト、統合テストの所在と検証範囲を確認するとき。
- CLI、Codex runtime、indexing、oracle review、session/run lifecycle、設定、Git・worktree・state などの外部契約をテストから確認するとき。
- テスト用の Codex、Ollama、Git repository、fake external command など共有支援の使い方を確認するとき。

## Do not read this when
- 正本仕様や Structured Output schema の内容を確認・変更するときは、対応する oracle doc または oracle source/schema を直接読む。
- 実装の詳細を確認・変更するときは、対応する src の realization implementation を直接読む。
- テスト実行全体の手順だけを確認するときは、専用の test execution 仕様を読む。

## hash
- 1bedec1c2f97780c12deaa5ce31b91d1cca5d28b0b3ea1a1b8f86ce14e4165d1
