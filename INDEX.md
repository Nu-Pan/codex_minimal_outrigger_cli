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
- cmoc の正本ドキュメントを、アプリケーション仕様、開発ルール、設計判断などの領域別に選ぶ上位入口。
- oracle のプログラム・設定ファイル向け詳細仕様を、agent call、エディタ入力、フィードバック、共通モデル、prompt 構築へ分類する入口。

## Read this when
- cmoc の仕様、開発ルール、設計判断のどの文書から調査を始めるか判断するときは「doc」を読む。
- oracle の実装・設定レベルの詳細について、agent call 構築、エディタ入力、フィードバック入力、共通モデル、prompt 構築のいずれの領域かを特定するときは「src」を読む。

## Do not read this when
- 特定文書の本文、具体的な実装・テスト規約、または設計案の詳細を確認する場合は、「doc」ではなく該当する下位文書を直接読む。
- 特定領域の実装・設定仕様だけを確認する場合は、「src」ではなく acp_builder、editor_input_handoff、feedback、other、prompt_builder の該当対象を直接読む。
- 実際の CLI ワークフローや realization の実装挙動、または状態ファイルの内容だけを調べる場合は、この oracle 入口ではなく対応する realization・state 対象を直接読む。

## hash
- 6cf319c78af43e855ca28d0dc51403e6f5a6113a39ae6d43815b1e84dff9b8b3

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
- src 直下の互換入口、共有 runtime、CLI トップレベル、サブコマンド実装群を責務別に案内する。
- acp、basic、config、cmoc_runtime、oracle は、互換 import 公開面から正本実装や下位互換モジュールへ進む入口である。
- commons は、CLI、Codex 実行、設定、Git、状態、feedback、report などで共有される runtime 実装を探す入口である。
- main.py は、cmoc CLI のコマンド階層、起動境界、引数解析、補完時の副作用防止を確認する対象である。
- sub_commands は、個別サブコマンドの CLI 入口と実行フローへ進む上位ルーティング対象である。

## Read this when
- src 直下の公開入口、互換 import 経路、または正本側実装への移行関係を確認するとき。
- 共有 runtime helper、設定、Git、状態、feedback、report、Codex 実行などの配置を調べるとき。
- cmoc CLI のトップレベルコマンド階層、Typer／Click 互換処理、引数解析エラー、補完時の副作用防止を確認するとき。
- 特定のサブコマンドの CLI 入口や実行フローを探すとき。
- 互換公開面から対応する正本・下位実装へ移る経路を確認するとき。

## Do not read this when
- 個別 API、型、入出力、描画仕様、または builder adapter の具体的な実装を確認したいとき。
- commons の特定 helper の内部挙動だけを調べるとき。
- 個別サブコマンドの業務ロジック、詳細ワークフロー、TUI、feedback report、INDEX.md 更新規則を確認したいとき。
- src の CLI や互換入口と無関係な処理、または正本仕様そのものだけを調べるとき。

## hash
- 6fb26dab5ebc0cbdfa4b38df0e4da883c866f3985e877f41ed8de688cce8de74

# `test`

## Summary
- cmoc の realization テスト群と共通テスト支援を集約する入口。CLI の各サブコマンド、Codex runtime、session/run state、Git・path・indexing・report・通知などの外部契約や回帰条件を、対象機能別のテストから確認できる。
- 共通 helper は、schema path 解決、doctor・Codex・Git・外部コマンド・PTY 実行、toast 隔離など、複数テストで共有する検証環境と呼び出し境界を提供する。
- 個別テストは、単体の runtime 挙動から実 Codex・独立 process・PTY を用いる本番経路統合まで、対象機能の検証範囲に応じた入口として機能する。

## Read this when
- cmoc の特定機能に対する外部挙動、回帰条件、エラー・中断・cleanup・永続状態の検証方法を調べるとき。
- CLI、Codex exec/TUI、indexing、session、editing run、oracle、feedback、prompt editor、Git/path、report、通知のテスト対象を探すとき。
- 複数テストで使う fixture や helper を利用・変更し、テスト用環境の固定条件や外部 process の扱いを確認するとき。
- 実際の Codex CLI、独立 process、PTY を使う受け入れ経路の検証方法を確認するとき。

## Do not read this when
- 正本仕様、schema、実装本体、または個別機能の具体的なアルゴリズムを確認することが目的で、対応する oracle・src・実装対象を直接読むべきとき。
- テスト対象の外部契約に関係せず、一般的な pytest 実行方法や無関係な機能の調査だけを行うとき。
- schema の内容自体、Codex CLI の一般利用方法、通知や Git の本番仕様だけを確認したいとき。

## hash
- e492a0a52b068f5082b8f9be10015abacdbbdaa5c193699133a5c40b14b9f718
