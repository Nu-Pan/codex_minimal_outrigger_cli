# `AGENTS.md`

## Summary
- cmoc 自己開発時に、仕様文・agent への指示文・現在の agent への指示文を区別するための注意事項と、agent 向け指示文を単独で理解可能かつ仕様定義を含まない形に保つための基準。

## Read this when
- cmoc 自身のリポジトリを cmoc で開発しており、同じ文面が異なる情報レイヤーに現れる場合の解釈を確認するとき。
- cmoc が呼び出す agent への指示文を作成・確認し、仕様への暗黙の依存や仕様定義の混入を避けるとき。

## Do not read this when
- cmoc の仕様そのものを調べる必要があるとき。
- 具体的な実装、設定、CLI 挙動を確認する必要があり、レイヤー区別や agent 向け指示文の独立性が関係しないとき。

## hash
- da4f29cd7f635f81ead991302bf0b25e687760e47096c1c5efe20318b8c9a8f2

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
- cmoc の正本仕様を、自然言語仕様と、それをプロンプト・ACP 呼び出し・補助モデルとして具体化する oracle ソースに分けて保持する。
- branch_model.md は oracle ツリーの構成・ブランチ運用に関する仕様を確認する入口。
- doc はアプリケーション仕様、開発規則、サブコマンド、フィードバック、oracle/realization の扱いを確認する入口。
- src は oracle 仕様を反映したプロンプト生成、ACP ビルダー、パス・設定モデル、入力引き渡し、フィードバック関連の構造を確認する入口。

## Read this when
- cmoc の正本仕様全体の構成や、仕様とそのソース実現物の対応を把握したいとき。
- ブランチ運用の仕様を確認するときは branch_model.md から読み始める。
- 機能要件・開発規則・サブコマンドの仕様を確認するときは doc から読み始める。
- プロンプト生成や ACP 呼び出し、構造モデルの正本ソースを確認するときは src から読み始める。

## Do not read this when
- 正本仕様ではなく、AI が具体化した現行実装やテストだけを確認したいとき。
- 特定の仕様文書または src 配下の特定モジュールが明確な場合は、この oracle ルート全体からではなく該当ファイルを直接読む。

## hash
- 5d4ec6b2f8047d2b36067e7cc7f22659d9adf6fa9a9bbf319a391cdede303eed

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
- cmoc CLI の実装ルート。`main.py` が Typer/Click のコマンドツリー、互換処理、引数エラー変換を定義し、`sub_commands/` の各コマンド実装へ接続する。
- `commons/` は CLI 実行ライフサイクル、Codex 起動、ログ・設定・パス・Git・フィードバック・レポート・リカバリなどの共通 runtime サービスを分担する。
- `acp/` はフィードバック、INDEX 更新、oracle 編集・調査、realization 適用・リファクタ、session、TUI などを起動する builder 群を含む。
- `basic/`、`config/`、`cmoc_runtime.py`、`oracle.py` は公開 API や互換 import path、設定、oracle 側型・path model の再公開を担う。

## Read this when
- CLI コマンドの追加・変更や、Typer/Click の起動・エラー処理を確認するときは `main.py` から読み始める。
- サブコマンドの実行手順、診断ログ、フィードバック、終了結果、共通前処理を確認するときは `commons/` を読む。
- oracle・realization・session・indexing など特定機能の CLI 接続や実行委譲を追うときは `sub_commands/` と対応する `acp/builder/` を読む。
- 互換公開名、設定、基本型、oracle package の解決経路を確認するときは `basic/`、`config/`、`cmoc_runtime.py`、`oracle.py` を読む。

## Do not read this when
- INDEX.md の生成やディレクトリ全体の役割把握では、個別コマンドの内部処理まで読む必要はない。
- 特定サブコマンドの挙動だけを調べる場合は、`src` 全体ではなく `sub_commands/` の該当実装と、それが直接呼び出す builder・runtime に進む。
- oracle の正本仕様やテストを確認したい場合は、`src` ではなく `oracle/` または `test/` の該当対象を直接読む。

## hash
- 1824cb2179c104e9b51340753f72ae42ed944cf5d795ea350bfd43b0aec32e2d

# `test`

## Summary
- cmoc の realization 実装を対象に、runtime のパス・Git・状態・設定・Codex 実行・権限制御、CLI サブコマンド、ACP builder、prompt、editor input handoff、feedback、indexing、構造化文書、Windows 通知などの仕様契約と回帰条件を pytest で検証する。
- 共有 fixture・helper はテスト用 repository、Codex 実行環境、CLI 呼び出し、editor input handoff、Git 操作、外部コマンドを隔離・構築し、個別テスト群が同じ検証条件を再利用できるようにする。
- oracle 側の builder・schema・文書を参照しながら、compatibility export、parameter、prompt 内容、structured output、ファイル分類、session/refactor lifecycle、CLI 外部挙動を realization 側と照合するテスト入口である。

## Read this when
- 実装変更が runtime、CLI、Codex 呼び出し、ACP builder、prompt 生成、Git 状態管理、session/refactor、feedback、indexing、handoff、通知のいずれかの契約に影響する可能性があるとき。
- 変更後に oracle の仕様に対する realization の回帰条件を横断的に確認したいとき。
- テスト用 repository・Codex 環境・CLI 実行・外部通知をどう隔離して検証しているかを調べるとき。

## Do not read this when
- 特定の実装関数の内部処理だけを確認したいときは、まず対応する src ファイルを読むべき。
- 一つの不具合の期待値や fixture だけを確認する場合は、test 配下の該当する test_*.py と共有 helper を直接読むべき。
- 正本仕様の意味や要求そのものを確認したいときは、test ではなく oracle/doc または oracle/src を読むべき。

## hash
- b870f0c64965e0a8848270bdb6ca23372944797601b0e643b7f309e3f8aeeb64
