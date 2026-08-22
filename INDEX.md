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
- cmoc の正本仕様・開発ルールと、agent call／prompt 生成を支える oracle 実装・schema を集約する領域。`doc` は CLI、workflow、state、feedback、branch／worktree、設計・開発環境・テストの意味仕様を扱い、`src` はその仕様に基づく builder、prompt、policy、設定・パスモデル、構造化文書、feedback 入力の正確な実装定義を扱う。仕様の調査は `doc`、agent call や prompt の実装・schema の確認は `src` から始める。

## Read this when
- cmoc の CLI、workflow、session、run isolation、branch／worktree、feedback、ログ、state、indexing の正本仕様を調査するとき
- Python 実装の設計、開発環境、テスト要件、テスト実行手順を確認するとき
- agent call の用途別パラメータ、prompt の組み立て、policy、placeholder、アクセス制約、oracle／realization の扱いを実装から確認するとき
- 設定モデル、パスモデル、構造化 Markdown、feedback reporter 入力、Structured Output schema の定義を確認するとき
- 採用しなかった設計・作業方式の理由を調査するとき

## Do not read this when
- 特定の仕様文書や実装モジュールが明らかな場合は、`oracle/doc` または `oracle/src` の対象を直接読む
- realization の実装・テストや通常の product 挙動だけを調べる場合
- 既存 INDEX.md の内容やインデックス生成処理だけを確認する場合

## hash
- a2ea7f67ac7c144ac6a13cfd3dbdf821bced144eb84e29eaa6b472d890f6c140

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
- `src` は cmoc の realization 側 Python パッケージ群と最上位 CLI 入口を収める実装ディレクトリ。互換 import shim、共通 runtime helper、CLI サブコマンド、ACP adapter など、利用者向けの実行経路から下位モジュールへ進むための入口となる。

## Read this when
- cmoc の realization 側で、最上位 CLI、共通 runtime、互換 import、ACP adapter、または CLI サブコマンドの実装入口を特定するとき
- `src` 配下のパッケージ構成を把握し、対象機能に対応する下位ディレクトリやモジュールへ進む必要があるとき

## Do not read this when
- 特定機能の内部実装や正本仕様だけを確認したいときは、`src` 直下ではなく対応する下位モジュールまたは oracle 側の対象を直接読む
- `src` 配下にない正本仕様、開発規約、テスト実行手順を確認するときは、それぞれの文書や手順の入口を直接読む
- CLI や realization 側の実装に関係しない調査を行うとき

## hash
- f274c6db1f732598020bdb2ec08876a41bb9350ecb0b4439355ea96f879d7886

# `test`

## Summary
- test ディレクトリは、cmoc の realization テスト群と共有テスト補助を集約する検証入口です。ACP builder、Codex runtime、CLI lifecycle、indexing、oracle review/edit、session/run、feedback、設定・状態・Git・通知など、実装や外部契約の回帰テストを領域別に確認できます。
- 個別機能のテストへ進む前に、対象領域の外部挙動・境界条件・統合 lifecycle を把握するための階層入口です。共有 helper や conftest はテスト環境の共通前提を確認する場合に参照します。

## Read this when
- cmoc の実装変更や仕様確認に対して、対応する realization test、回帰条件、外部契約の検証箇所を特定するとき。
- Codex 実行、CLI、indexing、oracle review/edit、session/run、feedback、設定・状態・Git・通知などの挙動をテスト観点から確認するとき。
- 複数コンポーネントをまたぐ lifecycle、失敗復旧、ログ・report・Git 差分・worktree 境界を一体として検証するテスト入口を探すとき。
- テスト全体に共通する fixture、テスト用 Git repository、fake command、Codex double、toast 隔離などの前提を確認するとき。

## Do not read this when
- 正本仕様、実装本体、Structured Output schema、prompt policy の定義そのものを確認することが目的のときは、各テストが示す oracle・実装・schema を直接読む。
- 特定の単一実装関数の詳細だけを調べる場合や、test ディレクトリの検証対象に関係しない機能を扱う場合。
- テスト実行手順そのものだけを確認したい場合は、repository local のテスト実行手順やプロジェクト設定を直接読む。

## hash
- dfbe8ac07058d4d19ffc12c20daee5ef1d275b2a5d05f9f6daaafd8d5f3b2d84
