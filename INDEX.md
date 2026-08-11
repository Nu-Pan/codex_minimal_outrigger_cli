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
- cmoc の人間所有の正本仕様を収める領域。アプリケーション仕様、開発規則、oracle 側ソースコード、構造化出力スキーマなどを扱い、実装やレビュー時に人間定義の挙動・責務境界・生成規則を確認するための上位入口となる。下位の文書・ソース領域へ進む起点。

## Read this when
- cmoc の正本仕様や開発上の規則を確認するとき
- アプリケーション仕様、branch・commit・worktree モデル、開発環境、テスト要件を調べるとき
- agent call、prompt、Structured Output schema、oracle・realization・routing・feedback の規則を調査するとき
- 実装やレビューの前提となる人間定義の責務境界・設計判断を確認するとき

## Do not read this when
- 特定の実装ファイルやテストファイルの具体的な挙動だけを確認すれば足りるとき
- 特定機能の詳細仕様が下位の専用文書に明確に定義されているとき
- collector 側の feedback 保存・集約処理だけを調査するとき
- 採用済み仕様ではなく、実装や実行成果物の形式だけを確認したいとき

## hash
- 0935a095830d78aba11caaab8c32281610e5e8557d0722280e76537e7773eeeb

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
- cmoc の realization 側 Python ソースの入口。Typer/Click による CLI 最上位入口、サブコマンド実装、共通 runtime、互換 import shim、ACP builder、および基本型・設定の公開経路を含む。個別の CLI 処理や runtime の詳細は各下位対象へ分岐する。

## Read this when
- cmoc の CLI 全体の入口、コマンド登録、引数解析、補完、またはサブコマンドへの委譲を確認・変更するとき。
- doctor、tui、indexing、session、oracle、realization、run、feedback の実装入口を特定するとき。
- ACP、basic、config、oracle、cmoc_runtime などの互換 import 経路や、commons 共通 runtime の担当領域を調査するとき。
- 複数のサブコマンドや runtime module にまたがる realization 側の構成を把握するとき。

## Do not read this when
- 特定サブコマンドの業務ロジック、ACP builder の具体的処理、または commons の単一 runtime 機能を確認したいときは、該当する下位実装を直接読む。
- canonical な oracle 側の仕様・実装や正本文書を確認したいときは、oracle 配下の対応対象を直接読む。
- 互換 shim の存廃だけを判断する場合は、該当 shim とその参照元を直接確認する。
- INDEX.md の routing 規則やエントリー生成内容だけを確認するとき。

## hash
- 3f04a1e4f3c374b9f8208d044ad6badb0e33c51fee71ed8651b6a17d374667ca

# `test`

## Summary
- pytest による realization test 群を集約するディレクトリ。CLI、Codex runtime、ACP builder、indexing、oracle review、session lifecycle、設定・状態永続化、Git/worktree、安全性など、cmoc の外部挙動と実装契約を検証する各テストへの入口となる。

## Read this when
- 対象機能の realization test、回帰テスト、統合テスト、または関連する共通 fixture を探すとき。
- CLI lifecycle、Codex 実行、ACP builder、indexing、oracle review、session、runtime 設定・状態などの挙動をテスト側から確認するとき。
- 複数の下位テストにまたがる外部契約や受け入れ経路を確認するとき。

## Do not read this when
- 正本仕様、設計意図、Structured Output schema、または実装責務を確認することが目的の場合は、対応する oracle 文書・schema・src 実装を直接読む。
- テスト実行手順や開発環境の規約だけを確認する場合は、専用の実行手順・開発規約を直接読む。
- 対象機能が明確で、その機能の個別テストへ直接進める場合。

## hash
- e20ccaf3efc04c3e4a8b75b67b18c70421a75df99c9692e7aaeb36a8086555ca
