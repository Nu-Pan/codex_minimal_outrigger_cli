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
- cmoc の正本仕様と開発ルールを領域別に案内する上位ドキュメント群。CLI のアプリケーション仕様、branch・commit・worktree のモデル、不採用案の検討記録、開発規則への入口を提供し、具体的な仕様・実装・テスト手順へ進むためのルーティング起点となる。

## Read this when
- cmoc の正本仕様を横断して、CLI の外部挙動、状態・branch model、開発環境、実装配置、テスト要件や実行手順の参照先を選ぶとき
- 複数の仕様領域にまたがる変更や調査で、アプリケーション仕様、branch model、開発ルールなどの下位文書へ進む入口を判断するとき
- 採用されなかった realization refactor の方式や検査・状態管理案の背景を確認するとき

## Do not read this when
- 特定のアプリケーション仕様、branch・worktree の用語、開発規則、テスト実行手順だけを確認する場合は、対応する下位文書へ直接進む
- 実装ファイル、テストファイル、Structured Output schema、feedback の専門仕様など、oracle/doc 配下の案内だけでは足りない具体的内容を確認する場合

## hash
- 19ab4bf2d2b856752c44f2ceb91bbf0e5f5b00986162268ed0b2b1a313866b1e

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
- cmoc の realization 側 CLI 実装ルート。Typer のトップレベル入口、session・oracle・realization・run・feedback などのサブコマンド、共有 runtime helper、互換 import shim、ACP builder adapter 群を含む。
- CLI のコマンド構成やサブコマンド実装、共有 runtime と互換公開層の関係を調査する際の上位入口であり、目的の下位 package・module へ進むための導線になる。

## Read this when
- cmoc CLI 全体の実装構成やトップレベル入口を把握するとき
- 特定のサブコマンド、共有 runtime helper、互換 import path、ACP builder adapter の所在を特定するとき
- realization 側から oracle 正本実装や互換公開層へ接続する構成を調査するとき

## Do not read this when
- oracle 側の正本仕様・正本実装の詳細を確認するとき
- 特定サブコマンドや runtime helper の内部挙動が既に分かっており、その実装を直接調査すべきとき
- src 配下と無関係な仕様、テスト、workload 本体を調査するとき

## hash
- 0999b7aa23944effc6da70881a825b071ade03f3be4efa3fce3c28e9605a6f7c

# `test`

## Summary
- cmoc の realization test を集約するディレクトリ。ACP builder、Codex runtime、CLI lifecycle、indexing、oracle review、session、editing run、設定・状態永続化など、実装の外部挙動や回帰契約を検証する pytest と共通テスト補助を含む。各機能の統合・回帰テストへ進むための入口であり、個別対象の詳細確認では配下の対応テストを選ぶ。

## Read this when
- cmoc の realization 実装に対応する回帰テストや統合テストの所在を探すとき
- CLI、Codex runtime、worktree・Git、state、indexing、oracle review、session、editing run などの外部挙動をテスト側から確認するとき
- 複数の機能境界をまたぐ lifecycle、失敗時復旧、永続結果、process・worktree isolation の検証範囲を把握するとき

## Do not read this when
- 正本仕様や実装責務そのものを確認する場合は、対応する oracle 文書または実装ファイルを直接読むとき
- 単一のテスト補助、個別 builder、parser、runtime helper の詳細だけを確認する場合は、対応する配下ファイルへ直接進むとき
- テスト実行手順や開発環境の規則だけを確認する場合は、repository local の test execution 指示や開発規則を読むとき

## hash
- a860c66aff2dfc4800b8a39b24dd06d05a6d6b560abd6b723935c660f81db873
