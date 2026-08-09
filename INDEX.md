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
- cmoc の正本領域で、アプリケーション仕様・開発規則・不採用案の記録を集約する。個別の正本ドキュメントや oracle 側のエージェント呼び出し構築実装へ進むための入口。

## Read this when
- cmoc の正本ドキュメントや oracle 側の agent call 構築実装の所在を確認するとき
- 複数の仕様領域または用途別 builder にまたがる調査対象を特定するとき
- 個別仕様や実装を読む前に、適切な下位領域への入口を判断するとき

## Do not read this when
- 確認対象の個別仕様文書がすでに特定できているとき
- 実際のサブコマンド実行フローや agent call 起動処理を調べるとき
- 個別の schema、基盤モデル、realization 実装、feedback 保存処理の詳細だけを確認するとき

## hash
- d6e770acf938fd75bde9c3c56580a3ee495362f5c55c7dd82a0f3139e78b00c9

# `pyproject.toml`

## Summary
- Python プロジェクトのパッケージメタデータ、実行コマンド、依存関係、ビルド設定、および pytest・Ruff・mypy の開発ツール設定を定義する。Python パッケージ構成、依存関係、CLI エントリーポイント、または開発時の品質検査設定を確認する際の入口となる。

## Read this when
- 依存パッケージや開発用依存パッケージを追加・変更するとき
- cmoc CLI のインストール後に使われる実行エントリーポイントを確認するとき
- Python のビルド・パッケージ探索設定を変更または調査するとき
- pytest、Ruff、mypy のプロジェクト共通設定を確認するとき

## Do not read this when
- 個別の CLI 挙動や内部実装を確認する場合は、src 配下の実装を直接読むとき
- テストケースの具体的な内容やテスト固有の規則を確認する場合
- 正本仕様や開発環境の運用手順を確認する場合は、対応する oracle 文書を読むとき

## hash
- d7e54a5345610218deb1baa5ef4ecf56af5f7bd5cd71249f76a9bbaa99f1bbf1

# `src`

## Summary
- cmoc の realization 側ソースルート。Typer CLI の最上位入口、CLI サブコマンド、共通 runtime、ACP・basic・config の互換公開入口、正本 oracle パッケージへの shim をまとめる。各機能の詳細実装や正本仕様へ進む前の起点となる。

## Read this when
- CLI 全体の command tree、起動経路、または最上位の引数解析を確認するとき。
- 複数のサブコマンドにまたがる共通 runtime、設定、状態、Git、ログ、feedback、Codex 実行基盤を調査するとき。
- `acp.*`、`basic.*`、`config.*`、`cmoc_runtime`、`oracle.*` の realization 側互換 import 経路を確認するとき。
- 目的のサブコマンド、builder adapter、runtime helper、または互換入口へ進む先を選ぶとき。

## Do not read this when
- 特定サブコマンドや runtime helper の内部処理だけを調査するときは、対応する下位要素を直接読む。
- ACP 型、設定型、path model、構造化文書、oracle package の正本仕様や実装詳細を確認するときは、対応する `oracle` 側を直接読む。
- 特定 builder の用途別処理を確認するときは、該当する `acp/builder` 配下へ直接進む。
- CLI と無関係な正本仕様、テスト、または利用箇所だけを確認するときは、対応する対象を直接読む。

## hash
- 67964e7f1376b9012e8db2acc6fa5c59ba9d3390492ef7905450b1646de3046b

# `test`

## Summary
- pytest による realization test 群と、テスト間で共有する実行・Git・Codex・CLI 用ヘルパーを収録するディレクトリ。cmoc の builder、runtime、各 CLI、session、oracle review、indexing、設定、通知などの外部挙動や境界条件を検証する。個別機能の回帰検証へ進むためのテスト入口であり、共通 fixture や支援処理を確認する場合は補助モジュールへ、正本仕様や実装詳細を確認する場合は対応する oracle または src へ進む。

## Read this when
- cmoc の既存機能について、pytest による外部挙動・回帰条件・異常系・ライフサイクルを調査または変更するとき
- 対象機能に対応する realization test の入口や、複数テストで共有する Codex、Git、CLI、通知などのテスト支援を探すとき
- CLI、runtime、builder、indexing、session、oracle review、config などの変更が既存の統合契約へ与える影響を確認するとき

## Do not read this when
- 正本仕様、Structured Output schema、設計意図を確認することが目的の場合は、対応する oracle doc・oracle src・schema を直接読むとき
- 実装の責務や内部処理を確認する場合は、対象機能の src を直接読むとき
- テスト実行手順だけを確認する場合は、repository local の test_execution の案内へ進むとき
- 対象機能と無関係なテストや共通 helper を総当たりで読む必要がないとき

## hash
- 1df28e62e7042260443603f7f14cc26624c8878a804431d2bfc140e531dd6011
