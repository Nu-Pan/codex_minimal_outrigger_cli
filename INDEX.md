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
- `src` は cmoc の realization 側 Python 実装の入口で、互換公開層、共通 runtime、設定 shim、CLI ルート、oracle package shim、各サブコマンド実装を扱う。CLI や realization 側の共通処理を横断して入口を選ぶための上位ルーティング対象。

## Read this when
- cmoc の realization 側 CLI 構成、公開 import 経路、共通 runtime、設定 shim、oracle package shim、またはサブコマンド実装の入口を確認するとき。
- 複数の下位パッケージや CLI サブコマンドにまたがる変更・調査で、個別実装へ進む前に realization 側の構成を把握するとき。

## Do not read this when
- 特定サブコマンドの業務ロジック、個別 runtime helper、builder、設定定義、または正本側 oracle 実装の詳細だけを確認したいときは、対応する下位要素や oracle 側の参照元へ直接進む。
- INDEX.md のルーティング方針や正本仕様を確認するときは、この realization 実装領域ではなく該当する INDEX.md または oracle 文書を読む。

## hash
- 2a2c147cf15b1448d771bb70900156035e58ae6f05aa40fcc9b20cfd8119794e

# `test`

## Summary
- cmoc の realization test を集約するディレクトリ。ACP builder、Codex runtime、CLI、indexing、oracle review、session、設定、Git、通知などの外部挙動・境界条件・安全性を pytest で検証する。各機能の回帰テストへ進む入口であり、個別テストの責務は各ファイル本文で確認する。

## Read this when
- 実装や仕様変更が既存の外部挙動、ライフサイクル、エラー処理、永続状態、Git 操作、Codex 実行、CLI 出力に影響するか確認するとき。
- 対象機能に対応する回帰テストや統合テストを特定するとき。

## Do not read this when
- 正本仕様や実装詳細を確認することが目的の場合は、対応する oracle 文書・schema・src を直接読む。
- テスト実行方法だけを確認する場合は、repository local の test_execution の案内を読む。
- 対象機能と関係しないテストを総覧する必要はなく、対応する個別テストへ直接進む。

## hash
- d1577cf473817e5b8a14f5f396ebaffb0d4a16f1ee2a61be4b9b08f02d03c28e
