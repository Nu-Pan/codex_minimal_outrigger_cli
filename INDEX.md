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
- cmoc の正本文書と oracle 実装をまとめた中核領域。CLI・Codex 呼び出し・prompt・ログ・feedback・session／run の挙動仕様、Python 開発・設計・テスト・環境のルール、branch model、採用しなかった設計案を扱う。
- 仕様や開発ルールを確認するときの入口であり、挙動仕様は `doc/app_spec`、開発関連は `doc/dev_rule`、branch／session／run の関係は `doc/branch_model.md`、代替案の背景は `doc/considered_alternative`、oracle の実装は `src` 配下へ進む。

## Read this when
- cmoc の CLI、workflow、Codex 呼び出し、prompt、ログ、feedback、状態管理の正本文書を横断して調査するとき
- 実装やテストの変更に先立ち、アプリケーション仕様、開発ルール、branch model、採用しなかった設計案のどの領域を確認すべきか判断するとき
- oracle の agent call builder、prompt builder、Structured Output、path model、設定などの実装配置を探すとき

## Do not read this when
- 対象の個別仕様書や開発ルール文書が既に特定できており、対応する下位対象へ直接進む方が適切なとき
- 特定の prompt builder、agent call builder、設定モデル、スキーマ、または oracle 実装の具体的内容だけを調査するとき
- realization の CLI 実行制御やテスト実装の具体的内容だけを調査するとき

## hash
- 7afb540a24a07958f67a3d7a17b44467bafcce4dbe32b03e888a2bfec4ecd1e6

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
- cmoc CLI の realization 実装ルート。`main.py` が Typer による最上位 CLI と session・oracle・realization・run・feedback などのサブコマンドを登録し、`sub_commands` の処理へ振り分ける。
- `commons` は設定、Git/worktree、run lifecycle、Codex 実行、ログ、状態、feedback、report、INDEX.md 更新など、複数の CLI 経路で共有する runtime 処理を担う。
- `acp`、`basic`、`config`、`cmoc_runtime.py`、`oracle.py` は、正本側または責務別 runtime module への互換 import 入口・package shim を提供する。個別の builder、サブコマンド、共通 helper の詳細調査は各下位要素へ進む。

## Read this when
- cmoc の最上位 CLI 起動、Typer/Click 互換処理、サブコマンド登録、または console script の入口を確認するとき
- session、oracle、realization、run、feedback、doctor、tui、indexing の実装配置と、対応する下位サブコマンドへの入口を特定するとき
- Git/worktree、run lifecycle、Codex 実行、設定、状態、feedback、report、ログ、INDEX.md 更新など、複数の実行経路に共有される runtime 処理の配置を確認するとき
- `acp.*`、`basic.*`、`config.*`、`cmoc_runtime`、`oracle.*` の互換 import 経路や移行境界を確認するとき

## Do not read this when
- 特定サブコマンドの具体的な処理フローや契約を確認するときは、`sub_commands` 配下の対象実装と対応する仕様を直接読む
- 特定の runtime helper、builder、adapter、型、設定定義の内部実装を確認するときは、`commons`、`acp`、`basic`、`config` または正本側の該当要素を直接読む
- `acp`、`basic`、`config`、`cmoc_runtime.py`、`oracle.py` の互換入口ではなく、正本側の実体や責務別 module の詳細だけを調査するとき
- cmoc の CLI、共有 runtime、互換 import と無関係な処理を調査するとき

## hash
- 3137f09d1f739f8e9887cef9da201bbac133f358148240c2ed3da3a0bd557762

# `test`

## Summary
- `test` ディレクトリは、cmoc の実装に対する realization test を集約する。CLI の外部挙動、Codex runtime、worktree・Git・state 管理、indexing、oracle review、feedback、通知、共通 helper などを対象とし、対応する実装変更や回帰条件を確認するための入口である。
- 個別サブコマンド、runtime 機能、builder、state、INDEX 更新、テスト基盤などの挙動を調べる場合は、同ディレクトリ内の責務に対応する個別テストへ進む。正本仕様や実装詳細を確認する場合は、テストではなく参照先の oracle 文書・実装を直接読む。

## Read this when
- cmoc の realization test から、変更対象の外部契約や回帰条件に対応するテスト入口を特定するとき
- CLI、Codex 実行、worktree・Git・state、indexing、oracle review、feedback、通知、builder などの実装変更に対する検証範囲を確認するとき
- 共通 fixture や test helper、packaged layout、実経路統合テストなど、テスト実行基盤の責務を調べるとき

## Do not read this when
- 正本仕様、設計意図、schema、prompt、実装内部の詳細を確認することが目的で、対応する oracle 文書や実装を直接読む方が適切なとき
- 特定の機能やサブコマンドと無関係なテスト領域を調べるとき
- 単に一般的なテスト実行方法だけを確認したいときは、repository local の test execution skill や直接の実行手順を読むとき

## hash
- fcaabb0715e2540d24caf07bca2183c1885a5f3b39c519ac55e89b7a32213a71
