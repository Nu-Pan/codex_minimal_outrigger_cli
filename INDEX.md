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
- cmoc の実行用ソースを構成するトップレベル入口。Typer CLI、サブコマンド、共通 runtime、互換 import shim、設定・基本 API を扱う。個別の CLI や runtime 実装へ進む前のルーティング起点。

## Read this when
- CLI 全体の入口、トップレベルパッケージの役割、互換 import 経路、または複数領域にまたがる実装配置を確認するとき。
- 対象ファイルが `acp`、`basic`、`commons`、`config`、`sub_commands`、`main.py`、`oracle.py`、`cmoc_runtime.py` のどこに属するか判断するとき。

## Do not read this when
- 特定サブコマンド、runtime helper、builder、設定型、または正本 `oracle.*` の具体的な処理を確認・変更するときは、対応する下位実装や正本側を直接読む。
- INDEX の更新処理、Structured Output schema、CLI の個別仕様など、トップレベル構成以外の詳細だけを調査するとき。

## hash
- 1f5429c9449378c803784f54e7296bb800b699c4bc412a0c112f9053ce388e8c

# `test`

## Summary
- test 配下は、cmoc の実装に対する realization test の入口であり、CLI、runtime、worktree・state lifecycle、Codex 実行、oracle review、indexing、builder、通知、設定などの外部契約と回帰条件を検証する。
- 個別機能の専用テスト、複数コンポーネントを横断する統合テスト、共通 fixture・test support、実 Codex を用いる受け入れテストへ進むための案内を提供する。

## Read this when
- 実装変更が既存の CLI 外部挙動、runtime 境界、Codex subprocess、Git/worktree lifecycle、永続 state、indexing、oracle review、builder、通知または設定のテスト契約に影響するか確認するとき
- 対象機能に対応する realization test の入口や、横断的な統合・受け入れテストの所在を特定したいとき
- テスト用の共通 fixture、fake external command、Git repository、Codex 実行環境などの支援機構を確認するとき

## Do not read this when
- 実装の責務や正本仕様、Structured Output schema の内容を確認することが目的のときは、対応する src または oracle 文書・schema を直接読む
- 対象機能が test 配下の検証契約や共通支援機構に関係しないとき
- テスト実行手順や開発環境の規約だけを確認するときは、専用の実行規約・開発規約を直接読む

## hash
- 1ce1967e55fcea2935596f2cb95530f72a56150126e668f4667acd744c4f6ee8
