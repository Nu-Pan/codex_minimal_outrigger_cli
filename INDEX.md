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
- oracle 配下の正本仕様・開発ルール・検討資料を、領域横断の入口として案内する。CLI、状態管理、branch/worktree、開発環境、設計、テスト、代替案など、目的に応じた下位文書への導線を提供する。

## Read this when
- cmoc の正本仕様や開発ルールを調べる際に、まず対象領域や適切な下位文書を特定したいとき。
- CLI、session/run、branch、Python 開発、テスト、設計判断など複数領域にまたがる参照先を確認するとき。
- 採用されなかった設計案や判断背景を確認したいとき。

## Do not read this when
- 特定の仕様本文、個別の開発ルール、実装、テスト、prompt builder、schema、サブコマンドの詳細だけを確認したいとき。
- INDEX.md の生成規則、raw observation、repository-local feedback state など、対象が明確な個別仕様を直接確認したいとき。

## hash
- 7731e8e6465875c0dffa4a3d17568d5e3395756973d528b6d5b447bbad1eafa2

# `pyproject.toml`

## Summary
- Pythonプロジェクトのパッケージ metadata、依存関係、CLIエントリーポイント、ビルド・配布設定、およびpytest・Ruff・mypyの開発ツール設定を定義する。

## Read this when
- Pythonのバージョン要件、実行時・開発時依存関係、`cmoc`コマンドのエントリーポイント、パッケージ探索や配布内容を確認するとき。
- pytest、Ruff、mypyの共通設定を確認・変更するとき。

## Do not read this when
- CLIの具体的な処理やランタイム挙動を確認するとき。
- 個別テストの内容やテスト実行手順を確認するとき。

## hash
- 3a783c008041cc5d2791af2abb3cfe1c24d8231f77689b906b36f62158c77455

# `src`

## Summary
- src の実装パッケージと互換入口を束ね、cmoc CLI と oracle／realization の実行経路へ進むための上位入口を提供する。
- CLI トップレベル、共通 runtime、互換 shim、サブコマンド実装、builder／basic／config などの下位要素を含む。

## Read this when
- src 配下の実装構成を横断して確認し、目的の CLI 入口、共通 helper、互換 import、またはサブコマンド実装の配置を特定するとき。
- cmoc の起動入口から oracle／realization、session／run、feedback、indexing、TUI などの処理経路へ進むルーティングを判断するとき。

## Do not read this when
- 特定ファイルの具体的な挙動、個別サブコマンドの処理、共通 runtime の内部実装、または互換 API の移行先だけを確認したいときは、src の入口ではなく該当する下位要素や正本実装を直接読む。
- 正本仕様や INDEX.md の生成規則そのものを調査するとき。

## hash
- 192db88dee9cb243c495fd681156b36a9c08564d3705ab3c5da5a7c1f78c3160

# `test`

## Summary
- CLI、Codex runtime、session/run、feedback、indexing、editor handoff、通知、Git、設定など、cmoc の主要機能を検証する realization テスト群と共有テスト補助の入口。各テストは対応する外部挙動、状態遷移、権限境界、エラー処理、成果物・ログ整合性を確認する。

## Read this when
- cmoc の実装や仕様変更が既存の CLI 外部契約、Codex 実行、run/session lifecycle、feedback、indexing、Git、設定、エディタ handoff、通知などのテスト要件に影響するか確認するとき。
- 対象機能に対応する回帰テスト、統合テスト、実経路テスト、または共有 fixture・helper の利用方法を探すとき。

## Do not read this when
- 正本仕様や実装詳細そのものを確認することが目的で、対応する oracle 文書または realization 実装を直接読むべきとき。
- テスト対象の外部挙動や回帰条件に関係しない機能だけを調査するとき。

## hash
- 9b2804d53de294e9d6451135f93dc23ea3aff9a7ee760e1e10d7c42b9e1df60d
