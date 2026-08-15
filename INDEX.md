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
- cmoc の正本仕様、開発規則、branch model、採用しなかった設計案をまとめた文書群と、oracle 実装の入口。CLI・workflow・agent call・状態管理などの仕様確認から、対応する実装・prompt 構築・共通モデルへ進むために読む。
- oracle/src は、パス・設定・Structured Markdown・標準定義などの共通モデル、agent call の起動パラメータ、prompt 構築、INDEX エントリー生成、feedback・review・realization 関連の oracle 実装を扱う。oracle 側の仕様に対応する実装を調査・変更するときの入口となる。

## Read this when
- cmoc の正本仕様、開発環境・設計・テスト規則、branch・worktree のライフサイクル、または不採用案の背景を確認するとき。
- oracle 実装の共通モデル、設定・パス解決、Structured Markdown、Standard、prompt 構築、agent call パラメータ、feedback・review・realization・indexing の処理を調査・変更するとき。
- 仕様から対応する oracle 実装や prompt 部品へ進む入口を確認するとき。

## Do not read this when
- 特定の仕様本文や特定の実装ファイルが明確で、その対象を直接読めるとき。
- realization 側の具体的な実装・テストや、生成済み prompt・ログ・実行成果物だけを確認するとき。
- oracle と無関係な CLI 業務ロジック、状態管理、TUI の詳細を調査するとき。

## hash
- 7bab1c76acbbaca7225f9f7acc8055169ede75a5526a79a3734da10e9aba4e89

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
- cmoc の realization 側 Python ソースをまとめるルート。Typer による最上位 CLI 入口、サブコマンド実装、共通 runtime、ACP builder、互換 import shim を含み、機能の実装箇所を下位ディレクトリへたどるための入口である。
- CLI のコマンド構成や起動・引数処理は `main.py`、共有 runtime は `commons`、サブコマンド本体は `sub_commands`、ACP builder と互換公開面は `acp`・`basic`・`config`・`oracle.py`・`cmoc_runtime.py` から確認する。

## Read this when
- cmoc の realization 側で、CLI 起動から各サブコマンド・共通 runtime へ至る実装構成を把握するとき
- 最上位 CLI の登録、Typer/Click 互換処理、または console script の起動経路を調査するとき
- ACP builder、共通 runtime、サブコマンド、互換 import 入口のどこから詳細調査を始めるべきか判断するとき

## Do not read this when
- 特定サブコマンド、runtime helper、ACP builder の具体的な入出力や内部実装を調査するときは、該当する下位要素へ直接進む
- oracle 側の正本仕様・実体実装や個別 adapter の詳細を確認するとき
- CLI や realization 側ソースと無関係な仕様・テスト・ドキュメントだけを調査するとき

## hash
- 6280033e7ddccfc08accecd7ac3517f6712d61011b1a9f945f67af572c277667

# `test`

## Summary
- cmoc の realization 側 pytest テスト群を集約するディレクトリ。ACP builder、Codex runtime、CLI lifecycle、indexing、oracle review/edit、session、state、config、prompt、Git/worktree、feedback、Windows toast など、実装の外部挙動と回帰契約を検証する。機能変更時に対応する検証入口を探す起点となる。

## Read this when
- cmoc の realization 実装や外部契約を変更・検証する際に、対応する pytest テストや統合テストの入口を特定するとき。
- CLI、Codex runtime、worktree・Git、indexing、oracle、session、prompt、state、feedback など複数の機能領域にまたがる回帰挙動を調査するとき。
- 個別テストの検証対象や、実経路・受け入れ試験を含む品質検査の範囲を確認するとき。

## Do not read this when
- 正本仕様、oracle implementation、realization implementation、Structured Output schema の内容自体を確認・変更するときは、対応する正本または実装ファイルを直接読む。
- 共通 fixture やテスト補助の責務だけを確認するときは、対象の補助モジュールへ直接進む。
- テスト実行手順だけを確認するときは、repository local の test execution 指示を読む。

## hash
- 5576308446c96bedfcfe411aa406e22eaa7add9e042da6033ec266ab70f88dc6
