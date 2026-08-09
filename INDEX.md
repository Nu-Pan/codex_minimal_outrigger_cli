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
- Python プロジェクトのパッケージ metadata、依存関係、CLI エントリーポイント、ビルド設定、pytest・Ruff・mypy の開発ツール設定を定義する正本設定。Python パッケージ構成や開発・品質検査の実行条件を確認する入口となる。

## Read this when
- 依存関係、対応 Python バージョン、`cmoc` CLI の公開エントリーポイント、パッケージ配置、ビルド方式を確認するとき
- pytest、Ruff、mypy のプロジェクト共通設定や開発用依存関係を確認するとき

## Do not read this when
- CLI の具体的な処理やランタイム挙動を確認したいときは、実装モジュールを直接読む
- テストケースの内容や仕様上の期待動作を確認したいときは、該当する仕様・テストを直接読む

## hash
- 6fb45f79a560a43b8ae51d23bdb53e4dc711587caffea78ce1020d595036510e

# `src`

## Summary
- `src` 配下の realization 実装をまとめる Python ソースツリー。CLI ルート、互換 import shim、共通 runtime、設定入口、各サブコマンド実装を扱い、個別領域へ進むための realization 側の入口となる。
- 既存の `acp.*`、`basic.*`、`config.*`、`oracle.*` などの互換公開経路と、`commons`・`sub_commands` に分かれた実行実装を確認できる。

## Read this when
- realization 側の CLI 全体構成、公開 import 経路、共通 runtime、またはサブコマンド実装の所在を判断するとき。
- トップレベル CLI から個別サブコマンドや共通 helper へ進む前に、`src` 配下の責務分担を把握したいとき。

## Do not read this when
- 正本仕様や canonical な実装内容を確認したいときは、`oracle` 配下の対応する文書・ソースへ直接進む。
- 特定サブコマンド、runtime helper、互換 shim の具体的な挙動を調査・変更するときは、該当する下位要素を直接読む。

## hash
- 5498171c7d96f84ac64b9f8cbc241b8a0853d4e8f5b5cc2fd0520342c53ee67b

# `test`

## Summary
- pytest による realization test 群を収録するディレクトリ。ACP builder、Codex runtime、CLI lifecycle、indexing、oracle review、session/run state、Git/path 安全性、設定、通知など、cmoc の各機能に対する外部挙動・境界条件・回帰契約を検証する。個別テストは対象機能の実装や正本仕様へ進むための入口となる。

## Read this when
- cmoc の機能変更に対して、対応する外部挙動・回帰テスト・境界条件の検証対象を探すとき。
- CLI、Codex 実行、indexing、oracle review、session、runtime state などの統合的な挙動を調査するとき。
- 対象機能に対応する個別テストの検証範囲や、利用すべき共通テストヘルパーを確認するとき。

## Do not read this when
- 正本仕様や Structured Output schema の内容そのものを確認・変更するときは、対応する oracle doc・oracle src・schema を直接読む。
- 単一の実装関数の詳細だけを調査するときは、対応する src 実装を直接読む。
- テスト実行方法や共通 fixture だけを確認するときは、対象のテスト実行規則または共通ヘルパーを直接読む。

## hash
- 4b3b75e7d9da4b9a4b18986715770887d4d378782f88e1e84eef4741362e4540
