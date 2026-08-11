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
- cmoc の正本文書を集約する領域。CLI の挙動仕様、session・run・branch・commit・worktree のモデル、開発・テスト規則、および採用しなかった設計案を扱う。
- 実装・テスト・環境構築・状態管理・agent call の判断では、目的に対応する仕様または oracle 側定義へ進む入口となる。

## Read this when
- CLI の自動補完、サブコマンド、出力、session・run の分離、feedback、状態管理などの現行挙動を確認するとき
- branch・commit・worktree の関係や、cmoc の開発環境・設計・コーディング・テスト規則を確認するとき
- 採用しなかった実装方式や設計案の背景、不採用理由を調査するとき
- agent call の prompt、Structured Output schema、oracle・realization・routing・feedback の定義を調査するとき

## Do not read this when
- 特定の CLI 挙動、出力、通知、状態、サブコマンド、テスト要件、または agent call の定義が明らかな場合は、対応する下位文書へ直接進むとき
- テストや品質検査の実行手順だけを確認するときは、テスト実行手順へ直接進むとき
- 現行の realization 実装、ログ、実行成果物、または具体的な状態ファイルの形式だけを確認するときは、対応する直接の対象へ進むとき
- 採用済みの現行仕様や実装の根拠を確認するときは、不採用案の検討記録を入口にしないとき

## hash
- a104f006ba157ec5f84dfca1778f554cc9f1d961f514b6edceb401feceb6060b

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
- cmoc の実行コードをまとめる最上位ソース領域。Typer/Click による CLI の最上位入口、互換 import shim、共通 runtime helper、CLI サブコマンド、ACP・basic・config・oracle 関連の下位実装への入口を提供する。
- CLI 全体のコマンド登録や引数解析を確認する場合は `main.py`、共通 runtime の責務を確認する場合は `commons`、サブコマンドの処理を確認する場合は `sub_commands`、互換 import 経路を確認する場合は該当する shim または `acp`・`basic`・`config`・`oracle.py` へ進む。

## Read this when
- cmoc のソースコード全体の構成や、CLI 入口から下位実装へ進む経路を把握するとき。
- 最上位 CLI のコマンド登録、Typer/Click の引数解析、補完、CLI エラー変換を確認・変更するとき。
- 共通 runtime、互換 import、ACP builder、basic 型、設定 shim、oracle package 解決、またはサブコマンド実装の配置を特定するとき。

## Do not read this when
- 特定サブコマンドの業務ロジック、個別 builder、または個別 runtime helper の詳細を確認したいときは、対応する下位実装を直接読む。
- oracle 側の正本仕様や canonical 実装を確認したいときは、`oracle` 配下の対応する正本ファイルを直接読む。
- CLI や共通 runtime と無関係な正本仕様、テスト、設定の内容だけを確認したいときは、それぞれの直接の対象へ進む。

## hash
- 8116c5c1f8dbde49a5f760e57ccfb40ef0ce2a4f3e594a91a4fb2be7de7ab790

# `test`

## Summary
- テストコード全体を対象に、cmoc の runtime・CLI・ACP builder・Codex 実行・indexing・oracle review・session・feedback などの外部契約と回帰条件を検証する realization test 群への入口。個別機能の実装や正本仕様ではなく、対応する挙動テストを探すために読む。

## Read this when
- 既存の外部挙動や回帰条件を確認するため、対象機能に対応する realization test を探すとき。
- CLI、runtime、Codex、indexing、oracle review、session、feedback、設定、通知などの統合・単体テストの検証範囲を確認するとき。
- 特定の実装変更が既存テストのどの契約に影響するかを調べるとき。

## Do not read this when
- 実装の責務や処理詳細を確認・変更するときは、対応する src の実装を直接読む。
- 正本仕様、設計規則、Structured Output schema、エラー仕様を確認するときは、対応する oracle 文書または schema を直接読む。
- 共通テスト補助だけを調べる場合は、対象の support helper を直接読む。

## hash
- 19a875834659a0f001c092286810135ba37db4d2a9c2ed86a5686af8920e35c0
