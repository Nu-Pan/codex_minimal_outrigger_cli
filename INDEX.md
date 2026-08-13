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
- cmoc の正本文書と開発規則を集約する領域。利用者向け仕様、branch・commit・worktree のモデル、設計検討記録、Python 実装・CLI 設計・開発環境・テスト要件・テスト実行手順の確認に進む入口となる。

## Read this when
- cmoc の挙動仕様や機能間の責務境界を確認するとき
- session・run の分岐、commit、worktree の用語や関係を確認するとき
- 採用されなかった作業方式や設計案の理由を確認するとき
- Python 実装、CLI 設計、開発環境、テスト要件、テスト実行手順の正本文書を探すとき

## Do not read this when
- 確認対象の仕様本文、開発ルール、検討記録がすでに特定できており、その対象を直接読めばよいとき
- 実装コード、テスト内容、ログ、実行成果物の詳細を調べるとき
- INDEX.md の生成規則やルーティング情報だけを確認するとき

## hash
- 7855071760c5f262cc01df7c1c8d478064f685b6ef4c8faf473625b8c0937be6

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
- cmoc の実行側コードを収める領域。Typer/Click による最上位 CLI 入口、サブコマンド実装、共通 runtime、設定・互換 shim、ACP builder を提供する。
- サブコマンドには doctor、feedback、indexing、oracle、realization、run、session、tui があり、各処理を共通 runtime と下位実装へ委譲する。
- commons 配下には CLI 実行、Codex exec/TUI、設定、状態、Git/worktree、パス、ログ、エラー、feedback、INDEX 更新などの共有 runtime 機能が集約されている。
- acp、basic、config、cmoc_runtime、oracle は、正本実装や commons 実装への互換 import・再公開経路を担う。ACP builder 配下には feedback、indexing、oracle、realization、session、TUI、quota probe などの adapter がある。

## Read this when
- cmoc の実行側コード全体の構成と、目的の実装領域への入口を確認するとき
- 最上位 CLI のコマンド階層、引数解析、補完、サブコマンド委譲を調査・変更するとき
- 共通 runtime、設定・状態管理、Codex 実行、Git/worktree、feedback、INDEX 更新の所在を特定するとき
- ACP 互換入口や builder adapter から canonical oracle 実装へ進む経路を確認するとき

## Do not read this when
- 特定サブコマンド、runtime helper、互換 shim、または ACP builder の内部挙動だけを調べるときは、対応する下位対象を直接読む
- CLI の利用者向け契約や処理仕様だけを確認するときは、対応する oracle 文書・正本仕様を直接読む
- canonical oracle 実装や正本側の型・設定定義を確認するときは、`oracle` 配下の正本実装を直接読む

## hash
- f75a63cb47753207f740de13191b80a23b75a8fcf0e6627a630961c86efa2731

# `test`

## Summary
- cmoc の realization test を集約するディレクトリ。ACP builder、CLI lifecycle、Codex runtime、Git/worktree、state、feedback、indexing、oracle review、session、TUI などの外部挙動・契約を検証する個別 pytest と、共通 fixture・テスト支援を下位対象への入口として提供する。

## Read this when
- 複数の機能領域にまたがる realization test の対象や、該当する回帰テストの入口を特定するとき。
- CLI、Codex 実行、worktree・Git、永続 state、indexing、oracle review、session、feedback などの外部挙動をテスト側から確認・変更するとき。
- 共通 fixture、fake subprocess、テスト用 Git repository、Codex 呼び出し支援など、複数テストで共有されるテスト基盤を調べるとき。

## Do not read this when
- 単一機能の実装責務や正本仕様を確認することが目的の場合は、対応する src 実装または oracle 文書を直接読む。
- 個別テストの検証内容が明らかな場合は、このディレクトリ全体ではなく該当する test ファイルへ直接進む。
- テスト実行手順だけを確認する場合は、repository local の test execution 指示を読む。

## hash
- 8572fcbcd811d76c272cfcd2899eb5cfa9fceb575ae02bd480f6c4ef55b34a8b
