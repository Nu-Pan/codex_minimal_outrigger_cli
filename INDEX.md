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
- cmoc の CLI 起動用シェルラッパー。仮想環境 Python の存在・実行可能性を確認し、通常起動では不足時の標準エラー報告後に `src/main.py` を実行する。補完プローブ時は Python が利用可能な場合のみ転送する。CLI の起動経路、Python 検証、起動失敗時のエラー形式、補完時の挙動を確認・変更するときの入口。

## Read this when
- cmoc コマンドの起動処理や、仮想環境 Python の検証・エラー報告を調査するとき
- シェルラッパーから `src/main.py` への転送条件や、自動補完プローブ時の分岐を変更・確認するとき

## Do not read this when
- CLI の実際の引数処理やアプリケーション動作を調査するときは、直接 `src/main.py` または対応する仕様を読む
- エラー内容の正本仕様や初回セットアップ手順を確認するときは、参照されているエラー処理・開発環境の文書を直接読む

## hash
- 70422bb34b7732bfa99d94d395b5c91f9aba3302293f0edba8366c10e7645dfe

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
- cmoc の正本文書と oracle 実装をまとめる上位ディレクトリです。
- 意味仕様・開発規則・branch model・検討資料は doc、agent call 構築・prompt 生成・設定・パスモデル・構造化文書・feedback 処理の実装は src から確認します。

## Read this when
- cmoc の正本文書と oracle 実装のどちらを入口にするか判断するとき。
- 仕様領域または実装領域の下位ディレクトリへ進む前に、oracle 全体の構成を確認するとき。

## Do not read this when
- 確認対象の仕様文書や実装領域が明確で、doc または src 配下の対象を直接読めるとき。
- 実装の具体的な挙動、個別の agent call、または特定仕様の詳細だけを調べるとき。

## hash
- acc67dba53c97311d3bbc6245e5cc3ff895fe7409ca14d9b28d40e66bfbb1808

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
- `src` は cmoc CLI の realization 側ソースツリーで、console script `cmoc` から起動する最上位入口と、共通 runtime、互換 import shim、サブコマンド実装、ACP builder adapter を収める。
- `main.py` が doctor、tui、feedback、indexing、session、oracle、realization、run の CLI 階層を登録し、各処理を `sub_commands` へ振り分ける。`commons` は設定・パス・Git・状態・ログ・Codex 実行・feedback・run lifecycle・INDEX 更新などの共有 runtime を担当する。
- `acp`、`basic`、`config`、`cmoc_runtime.py`、`oracle.py` は既存の公開 import 経路を保つ互換入口で、canonical な oracle 実装や共通 runtime の正本を複製せず再公開・委譲する。`acp.builder` 以下には共通プロンプト、feedback issue、indexing、session、oracle review/edit/investigation、realization、TUI などの処理別 adapter がある。
- CLI サブコマンド固有の実行フローや状態遷移を調べる場合は `sub_commands` 以下へ、共有 runtime の責務を調べる場合は `commons` 以下へ、ACP builder の処理別接続を調べる場合は `acp.builder` 以下へ進むための上位入口となる。

## Read this when
- cmoc CLI の起動入口、最上位コマンド構成、サブコマンド登録、Typer/Click 互換処理を確認・変更するとき
- 複数のサブコマンドで共有される runtime、Codex 実行、設定、状態、Git、feedback、ログ、run lifecycle、INDEX 更新の配置を確認するとき
- `acp.*`、`basic.*`、`config.*`、`cmoc_runtime`、`oracle.*` の互換 import 経路や canonical 実装への委譲を調べるとき
- 処理領域に対応するサブコマンド実装または ACP builder adapter の下位対象を特定するとき

## Do not read this when
- 特定サブコマンドの詳細な挙動や引数仕様だけを確認したいときは、対応する `sub_commands` のファイルまたはディレクトリを直接読む
- 共有 runtime helper の内部仕様だけを確認したいときは、`commons` の該当モジュールを直接読む
- ACP builder の個別プロンプト生成・検証・review・session・realization 処理だけを確認したいときは、対応する `acp.builder` 下位対象を直接読む
- canonical な oracle 実装、正本仕様、出力契約を調査・変更するときは、対応する oracle 側や仕様ファイルを直接読む
- `src` の互換入口や CLI 実装と無関係な利用側ロジックを調査するとき

## hash
- 0b743aff5aeef0214551e88bead63026d160766cff07c042beae5538b4106b55

# `test`

## Summary
- `test` ディレクトリは、cmoc の realization test を集約する検証入口である。ACP builder、CLI lifecycle、Codex runtime、Git/worktree、session/run state、indexing、oracle review、feedback、prompt、設定、通知、wrapper など、主要機能の外部挙動・境界条件・失敗復旧をテストする。
- 個別機能の実装や正本仕様を読む前に、変更対象の外部契約を確認するための下位テストへ進む入口として利用する。共通 fixture・helper は `_cli_support.py`、`_codex_support.py`、`_git_support.py`、`conftest.py` など、対象機能の回帰テストは対応する `test_*.py` を読む。

## Read this when
- cmoc の主要機能について、利用者から観測できる挙動、エラー分類、状態遷移、Git/worktree 境界、Codex 呼び出し、report、cleanup の回帰契約を確認するとき。
- 複数の機能にまたがる統合 lifecycle、共通 runner、fixture、subprocess、通知、ログ、永続 state のテスト対象を探すとき。
- 変更対象に対応する realization test の具体的なファイルと、そこから実装・oracle 仕様へ進むルートを特定するとき。

## Do not read this when
- 正本仕様、設計規則、schema、実装アルゴリズムそのものを確認することが目的のときは、対応する oracle または realization の対象ファイルを直接読む。
- 単一テストの共通補助だけを確認したいときは、該当する `_support.py` や `conftest.py` を直接読む。
- 対象機能と無関係なテストを広く確認する必要はなく、対応する `test_*.py` へ直接進める場合。

## hash
- 5f5bc283fda13093be381eb1c0925486a37a5d508262337191f17e812c1046db
