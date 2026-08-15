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
- プロジェクトルートと仮想環境の Python 実行可能性を確認し、Python CLI エントリーポイントへ引数を委譲する起動用シェルラッパー。通常起動時の環境不足エラーと補完プローブ時の簡略的な失敗経路を扱う。

## Read this when
- 起動前の環境検査、仮想環境 Python の利用可否、シェルから Python CLI への引数委譲を確認または変更するとき
- 通常起動と補完プローブ起動で仮想環境が利用できない場合の扱いを確認するとき

## Do not read this when
- CLI の実際のコマンド処理や業務ロジックを調べるとき
- エラー文面の正本仕様や Python 実装の詳細を確認するとき

## hash
- f8265a802567113e11bc0dc3e9a36c679a1f9bc9dce4b43a798d178594f3150d

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
- cmoc の正本文書を領域別に案内するルート。アプリケーション挙動、branch・commit・worktree のモデル、不採用案の検討記録、開発ルールへの入口を提供する。
- `doc` では仕様・設計・開発ルールを、`src` では agent call 構築の共通実装と用途別 builder を確認できる。

## Read this when
- cmoc の仕様・設計・開発ルールを横断して、読むべき文書領域を選ぶとき
- CLI 挙動、session/run の分岐、refactor 方針、Python 実装・環境・テスト手順のいずれかを確認するとき
- agent call の共通 prompt、routing、ファイルアクセス規則、Structured Output 前提、または用途別 builder の責務を調査するとき

## Do not read this when
- 特定機能の実装詳細やテスト実行手順が明確な場合は、対応する下位の realization file、oracle src、または専用手順を直接読む
- INDEX.md の生成・更新仕様を確認する場合は、インデクシング仕様を直接読む

## hash
- 626124ea86a15f5a2246f0dad8310c60eba2b9d4b6409ec80afd26ebe8de8aa2

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
- cmoc の realization 側ソースツリー。Typer による CLI 最上位入口、サブコマンド実装、共通 runtime、正本側パッケージへの互換 import 入口、ACP builder 群をまとめる。
- CLI の起動や最上位コマンド登録は `main.py`、サブコマンドの処理は `sub_commands`、共通実行基盤は `commons`、互換公開入口は `acp`・`basic`・`config`・`cmoc_runtime`・`oracle.py` から下位要素へ進む。

## Read this when
- cmoc の CLI 全体構成、最上位のコマンド登録、Typer/Click 互換処理を調査・変更するとき
- サブコマンド、共通 runtime、ACP builder、または realization 側の互換 import 境界への入口を判断するとき
- `src` 起動時に `oracle.*`、`acp.*`、`basic.*`、`config.*`、`cmoc_runtime` がどのように解決されるかを確認するとき

## Do not read this when
- 特定サブコマンドの内部処理を調査するときは `sub_commands` 配下の対象へ直接進むとき
- 共通 runtime helper、ACP builder、または互換公開モジュールの具体的な実装を確認するときは対応する下位要素へ直接進むとき
- 正本側の仕様や `oracle.*` の実体実装を確認するときは `oracle` 側の対象を直接読むとき

## hash
- 0a587c84d4d7cc6da768ff52f73c9c4e444dfaa870d6d813c1a2a0a721549c1c

# `test`

## Summary
- realization test と共通 test helper を集約し、CLI、runtime、Codex 実行、indexing、oracle、feedback、session、editing run などの外部挙動と回帰条件を検証するテスト領域。
- 機能変更時に、単体・統合・受け入れテストのどの検証入口へ進むべきかを判断するための起点となる。

## Read this when
- 対象機能の外部挙動、ライフサイクル、エラー処理、永続 state、Git 差分、Codex 呼び出し、report をテストで確認または変更するとき。
- 複数のサブコマンドや runtime 境界にまたがる回帰条件を調査するとき。
- 共通 fixture、fake external command、Git repository、Codex 実行環境などのテスト支援を利用・変更するとき。

## Do not read this when
- 正本仕様や本番実装の責務・詳細を確認することが目的の場合は、対応する oracle または realization の実装・仕様へ直接進むとき。
- テスト実行手順だけを確認する場合は、repository local の test execution 指示へ直接進むとき。
- INDEX.md の生成規則や一般的なルーティング構造だけを確認する場合は、indexing の仕様・実装へ直接進むとき。

## hash
- 022ca6a50d5460ecfa7ca0a26d7782cbd408d52854edbe59bace4736e259398e
