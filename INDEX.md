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
- cmoc の人間所有の正本仕様群を収めるディレクトリ。アプリケーション仕様、設計・開発規則、ACP や prompt などの正本実装、正本テストを扱い、領域別の下位文書・実装・テストへ進む入口となる。

## Read this when
- cmoc の正本仕様、設計・開発規則、正本実装、または正本テストの所在を確認するとき。
- 特定の仕様・実装・テストへ進む前に、oracle 配下の領域構成を把握するとき。

## Do not read this when
- 対象が特定の正本ドキュメント、実装、またはテストに明確に限定されている場合は、該当する下位領域へ直接進む。
- realization 側の CLI 挙動や実装、テストの具体的内容を確認する場合は、対応する realization 側の直接の参照先を読む。

## hash
- 005639bec6a3f84f5ec3e09de92996960a0d9da1a08faab9870e798a6519f567

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
- cmoc の realization 実装をまとめる src ルート。CLI 起動入口、互換 import shim、共通 runtime、ACP adapter、設定、サブコマンド実装を含み、実際の処理領域へ進むための起点となる。
- CLI 全体の command tree と引数処理は main.py、共通実行基盤は commons、ACP 互換層は acp、互換公開 API は basic と config、サブコマンド固有処理は sub_commands、正本側 oracle パッケージの解決は oracle.py を読む。

## Read this when
- cmoc の realization 側 CLI 構成、公開 import 経路、共通 runtime、またはサブコマンド実装の入口を特定するとき。
- 対象となる機能が main.py、acp、basic、commons、config、sub_commands のどこに実装されているか判断するとき。
- src 起動時の cmoc_runtime または oracle パッケージ shim の解決経路を確認するとき。

## Do not read this when
- 正本仕様、正本実装、または oracle 側の builder の詳細を確認したいときは、oracle 配下の該当ファイルを直接読む。
- 特定サブコマンドや runtime helper の内部挙動だけを調べるときは、対応する下位ディレクトリまたはモジュールへ直接進む。
- テストや生成済みキャッシュ、パッケージメタデータだけを確認する場合。

## hash
- 20de7c48830c8a846f1e0c4c57bd28da14aeef06b1a3f90f529b06f376aa449b

# `test`

## Summary
- pytest による realization test suite。ACP builder、Codex runtime、CLI lifecycle、indexing、oracle review、session/editing run、設定・Git・state・通知などの外部挙動と回帰条件を検証する。各機能領域の実装変更時に、対応する個別テストへ進むための入口。

## Read this when
- 実装変更に伴う外部挙動・回帰条件・統合 lifecycle の検証対象を選ぶとき
- CLI、Codex runtime、indexing、oracle review、session、editing run、設定、Git、state、通知などの realization test を調査するとき
- 共通 fixture やテスト用 Git repository、fake subprocess、Codex double の利用方法を確認するとき

## Do not read this when
- 正本仕様や schema の内容自体を確認・変更するときは、対応する oracle doc・oracle source・oracle schema を直接読む
- 実装の詳細や単一関数の挙動だけを確認するときは、対応する src ファイルまたは専用テストを直接読む
- テスト実行方法だけを確認するときは、repository local の test_execution の案内を読む

## hash
- bfe1f245827e7145b4dc9a6ad35c96087172111d2ab7841018577ab653ae750f
