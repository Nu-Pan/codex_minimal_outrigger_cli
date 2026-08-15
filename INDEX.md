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
- cmoc の正本仕様を収める入口。利用者向け CLI・workflow・agent call・session/run lifecycle・prompt・feedback・ログ・通知などの共通契約を扱い、個別仕様や横断的な挙動の確認先を示す。
- oracle 側の agent call・prompt 構築実装群への入口。用途別の呼び出し構築、モデル・推論・アクセス設定、quota probe、prompt 合成、共通 Standard、routing、Structured Markdown、パスモデル、feedback 入力契約を扱い、実装上の構築経路を調べる際の起点となる。

## Read this when
- cmoc の利用者向け挙動や複数機能にまたがる正本仕様を確認するとき
- CLI、workflow、agent call、session/run、prompt、feedback、ログ、通知などの個別仕様へ進む入口を探すとき
- oracle 側の agent call 構築、prompt 合成、共通設定、ファイルアクセス規則、Structured Output、feedback 入力契約を調査・変更するとき

## Do not read this when
- 対象となる個別仕様書が既に特定でき、その本文だけで確認できるとき
- realization implementation や realization test の具体的な実装・テスト手順だけを調べるとき
- 開発環境、テスト実行手順、INDEX.md 生成処理など専用の手順が直接の入口となるとき

## hash
- c85f6052327292e3b1bed1a1d71d05ea5533aafc6915b0b9f39ab4787ceff5a2

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
- cmoc realization 側の CLI と共通 runtime を集約する実装ディレクトリ。Typer のトップレベル入口、session・oracle・realization・run・feedback などのサブコマンド、互換 import 入口を提供し、個別処理や正本実装へ進むための上位ルーティング対象となる。

## Read this when
- cmoc CLI の realization 側エントリーポイントとサブコマンド構成を確認するとき
- 対象の CLI 処理、共通 runtime、互換 import shim が src 配下のどこにあるかを特定するとき
- CLI 実装から個別サブコマンド、runtime module、または oracle 側の正本実装へ読み進む起点を判断するとき

## Do not read this when
- 特定サブコマンドの実行フローや個別 runtime helper の内部挙動を調査するときは、対応する下位モジュールを直接読む
- ACP・basic・config などの互換入口の詳細や、oracle 側の仕様・実装を確認するときは、対応する対象を直接読む
- CLI や src 配下の realization 実装と無関係な仕様を調査するとき

## hash
- 9b5ded7a3e36703d0aad83a235b9900ef3d1bdac5828b5f8ca97541dd85e15d4

# `test`

## Summary
- pytest による realization test 群と共通 test helper を集約するディレクトリ。CLI、Codex runtime、indexing、oracle review、session、state、設定、prompt、Git/worktree lifecycle など、cmoc の外部挙動・永続状態・安全境界を検証する。個別テストや helper へ進む前に、対象機能の回帰テスト入口を探すための階層。

## Read this when
- cmoc の機能変更や不具合調査で、対応する realization test、統合テスト、または共通 fixture/helper の所在を特定するとき。
- CLI lifecycle、Codex 実行、indexing、oracle review、session/run、prompt、設定、Git/worktree、通知などの外部契約を回帰テストから確認するとき。
- 既存のテスト群から、対象機能の検証範囲や安全性・失敗時挙動・永続状態の確認箇所を探すとき。

## Do not read this when
- 正本仕様や本番実装の責務・詳細を確認することが目的で、対応する oracle 文書または realization 実装を直接読むべきとき。
- 単一の helper や個別テストの詳細が既に特定できており、このディレクトリ全体の入口を探す必要がないとき。
- テスト実行手順や開発規約だけを確認したいときは、repository local の test execution 指示や開発規則を直接読むとき。

## hash
- 5ca71e8c022a6ab06ea1e3f0135b219ef6abb98a112cac05c27f4bd138653a3e
