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
- cmoc の正本仕様ツリー。CLI の利用方法、サブコマンド、セッション・run lifecycle、editor input handoff、feedback、indexing、oracle/realization の関係、エラー処理、ログ・状態管理などの要求を oracle/doc に定める。
- cmoc の正本実装・設定・データ定義。prompt builder、ACP builder、editor input、feedback、quota、indexing、session、oracle edit、realization apply/refactor など、仕様を具体化する oracle/src のコードと JSON 定義を扱う。
- 正本仕様に従う開発・テスト規約。環境構築、設計、コーディング、テスト実装、品質検査の選択と実行手順を確認する入口。

## Read this when
- cmoc の機能仕様、CLI サブコマンドの動作、状態遷移、ファイルアクセス、agent call、prompt 構築、feedback、indexing の正本を確認するとき。
- oracle file の要求を realization 側へ反映する方法や、oracle/src の builder・設定・補助処理の責務を調べるとき。
- 開発環境、コーディング規約、テスト要件、品質検査の完了条件を確認するとき。

## Do not read this when
- 既存の realization 実装や realization test の具体的なコードだけを調査するときは、src または test の該当対象を直接読みます。
- 対象となる単一のサブコマンド仕様や単一の oracle/src モジュールが明確な場合は、oracle 配下全体ではなくその正本ファイルを直接読みます。
- INDEX.md や AGENTS.md などの管理用ファイルだけを確認したいとき。

## hash
- 7bc5c9d802468769b64070de45faf89ec723b419d11565e110b78c8dc49e48b6

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
- cmoc CLI の実装ルート。`main.py` が Typer/Click のコマンドツリーと起動時互換処理を定義し、各サブコマンドを `sub_commands` 配下へ委譲する。
- `commons` は CLI 実行、Codex subprocess、Git、設定、状態、ログ、レポート、フィードバック、パスなど複数コマンドで共有する runtime 基盤を提供する。
- `sub_commands` は doctor、indexing、session、oracle、realization、run、feedback、TUI などの利用者向け操作単位を実装する。
- `acp/builder` は oracle 側の ACP builder を realization から利用するための実装・委譲層を構成する。
- `basic` と `config` は oracle 側で定義された ACP 型・設定型や構造化文書機能を再公開し、正本定義の複製を避ける互換層として機能する。
- `oracle.py` は src 起動時に `oracle/src/oracle` を解決する package shim であり、正本側 oracle package への参照を成立させる。

## Read this when
- CLI コマンドの追加・変更、Typer/Click の引数解析、起動時エラー処理を調べるときは `main.py` から確認する。
- 複数のコマンドにまたがる Codex 起動、Git 操作、実行状態、ログ、レポート、設定、フィードバック処理の挙動を調べるときは `commons` から確認する。
- 利用者向けの session、oracle、realization、run、feedback、doctor、indexing 操作の具体的な処理を変更・調査するときは `sub_commands` の該当階層へ進む。
- ACP builder の呼び出し境界や正本側 builder の再公開経路を調べるときは `acp/builder` を確認する。
- oracle 側の型・設定・構造化文書を realization から参照する互換経路を確認するときは `basic`、`config`、`oracle.py` を確認する。

## Do not read this when
- 特定のサブコマンドの内部処理だけが対象で、`sub_commands` 配下の該当ファイルへ直接進めるとき。
- 共有 runtime の単一機能だけが対象で、`commons` 配下の該当モジュールへ直接進めるとき。
- oracle の正本仕様や正本実装そのものを確認する必要があり、`src` の再公開・委譲層では目的を満たせないとき。
- CLI の利用方法ではなく、正本側の ACP builder や設定定義の内容を直接確認すべきとき。

## hash
- 4b4dfdfe6c23c880192b9740c4cf8f46667d2c8305fb9642b6a7c341c5d038b1

# `test`

## Summary
- pytest による単体・統合・受け入れテスト群と共有 fixture/helper を収録する検証ディレクトリ。CLI lifecycle、Codex 実行、Git/worktree・session state、indexing、feedback、editor handoff、prompt、設定、ログ、通知などの外部契約を、oracle の仕様・schema を参照しながら検証する。
- `_real_path_integration` には実際の Codex CLI・独立 process・PTY を用いた実経路統合テストがあり、通常の mock ベーステストとは異なる受け入れ検証の入口となる。
- `_acp_builder_support.py`、`_codex_support.py`、`_git_support.py` などの共有 helper と `conftest.py` が、schema 参照、fake Codex・Git repository、CLI 実行、通知・handoff の副作用隔離を提供する。

## Read this when
- テストスイート全体の構成、対象機能ごとの回帰テストの所在、または共有 fixture・helper の役割を把握したいとき。
- CLI、runtime、Codex、Git/worktree、session、indexing、feedback、handoff などの外部挙動を検証・変更し、対応するテストの入口を探すとき。
- 実際の Codex CLI と独立 process・PTY を使う受け入れ試験を実行・調査するときは、`_real_path_integration` から確認するとき。

## Do not read this when
- 実装の詳細や正本仕様そのものを確認したいときは、対応する `src` または `oracle` のファイルを直接読むとき。
- 特定機能の個別検証内容が既に分かっている場合は、このディレクトリ全体ではなく対応する `test_*.py` を直接読むとき。
- Codex 推論を伴わない通常の単体・mock ベーステストだけを扱い、実経路統合テストの仕組みを確認する必要がないときは、`_real_path_integration` を読む必要はない。

## hash
- a5e0d71af45ea6d173918efe99c0b2f14e080c9c84c6ce9bd975dc404d2618a2
