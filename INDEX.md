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
- cmoc の人間所有の正本仕様を収めるディレクトリ。CLI や共通 lifecycle、Codex CLI 呼び出し、prompt、feedback、ログ、状態管理、worktree、開発規則などの仕様文書と、ACP・prompt builder・設定モデル・パスモデル・feedback 入力契約などの正本実装を扱う。仕様文書は機能領域別の doc、正本実装は ACP builder・prompt builder・other・feedback などの src 配下が入口になる。

## Read this when
- cmoc の正本仕様、仕様間の関係、現行の CLI・workflow・状態管理・feedback・Codex CLI 呼び出し規約を確認するとき
- oracle src の ACP 呼び出し設定、agent prompt、oracle・realization 規範、パスや設定の共通モデル、構造化文書変換、feedback reporter 入力契約を確認するとき
- 採用しなかった設計案や作業方式の理由を確認するときは、正本ドキュメント内の considered_alternative へ進むとき
- 特定の仕様領域や実装責務が明らかな場合に、doc または src の対応する下位ディレクトリへ進む入口を選ぶとき

## Do not read this when
- 特定の CLI サブコマンドや個別機能の詳細仕様を確認する場合は、doc 配下の対応する個別文書へ直接進むとき
- 特定の ACP builder、prompt builder、feedback、other 実装の詳細を確認する場合は、src 配下の対応する下位領域へ直接進むとき
- realization 側の CLI 挙動や実装を確認する場合は、oracle ではなく realization implementation を直接読むとき
- 一般的な利用手順、単一の開発手順、provider 固有の稼働・認証・推論品質を調査する場合は、対応する利用手順書・開発規則・外部サービスの資料へ直接進むとき

## hash
- 6dff54a232ed7ee6f4ef149c2dbec5de10267da8879d3284ee96a26491cd1505

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
- `src` は cmoc の実行側コードをまとめる入口で、Typer による CLI 起動、トップレベルおよび階層型サブコマンドの登録、引数解析エラーの cmoc 形式への変換を扱う。
- CLI の処理本体は `sub_commands`、共通 runtime は `commons`、互換 import 入口は `acp`、`basic`、`config`、`cmoc_runtime.py`、正本 package 解決は `oracle.py` に分かれている。対象領域ごとの実装へ進むための最上位ルーティング入口である。

## Read this when
- cmoc の CLI 起動経路、Typer アプリケーション構成、トップレベルおよびサブコマンドの登録を確認・変更するとき。
- CLI 引数解析エラー、補完、終了処理がどの実装へ委譲されるかを調べるとき。
- `src` 配下で、共通 runtime、互換 import shim、またはサブコマンド実装の入口を選ぶとき。
- `oracle.*`、`acp.*`、`basic.*`、`config.*`、`cmoc_runtime` の import 解決経路を確認するとき。

## Do not read this when
- 特定サブコマンドの処理内容を調査・変更するときは、`sub_commands` 配下の対応する実装を直接読む。
- 共通 runtime の個別 helper や lifecycle の挙動を確認するときは、`commons` 配下の対象 module を直接読む。
- `acp`、`basic`、`config`、`cmoc_runtime.py` の互換入口の詳細を確認するときは、該当する対象を直接読む。
- 正本仕様または正本側 `oracle.*` の実装内容を確認するときは、`src` の shim ではなく `oracle` 配下を直接読む。
- CLI から呼び出される個別機能の生成ロジックや内部アルゴリズムだけを調べるとき。

## hash
- 265235e77456fd1f35ef30cf010a81969fe0ea7e3a22f7175c1bef909697700a

# `test`

## Summary
- pytest による realization test 群を収録するディレクトリ。CLI、runtime、Codex 実行、Git/worktree、indexing、oracle review、session、feedback、設定、通知などの外部契約と安全性を検証する。個別機能の回帰テストや共通テストヘルパーへ進む入口となる。

## Read this when
- 対象機能の外部挙動、CLI lifecycle、Codex runtime、Git/worktree lifecycle、indexing、oracle review、session、feedback、設定、通知のテストケースを調査・変更するとき。
- テスト用の共通 fixture や fake subprocess、Git repository、Codex 環境の構築方法を確認するとき。
- 複数のテストモジュールにまたがる回帰契約や統合挙動の入口を探すとき。

## Do not read this when
- 正本仕様、Structured Output schema、実装詳細そのものを確認するときは、対応する oracle または src ファイルを直接読む。
- テスト実行方法だけを確認するときは、repository local の test_execution の案内を読む。
- 対象機能と無関係なテストや、個別実装の単独確認だけを行うとき。

## hash
- 55504c51904622d9a1ca54fa5f1960ee75fc727a63996640884a6f02cebc6dcf
