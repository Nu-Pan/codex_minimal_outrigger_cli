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
- cmoc の実行時実装を集約するディレクトリ。CLI のコマンドツリーと起動境界、サブコマンド本体、共通 runtime のライフサイクル・エラー・ログ・Git・設定・フィードバック処理、ACP builder、互換 import path を扱う。
- main.py が Typer/Click の CLI 入口と互換処理を定義し、sub_commands が各コマンドの入口、commons が横断的な実行基盤、acp/builder が Codex 実行を伴う生成・編集・調査処理を担うため、実行時の責務分担を確認する際の入口となる。
- INDEX.md の検査・生成・commit lifecycle は commons/indexing.py にまとまり、sub_commands/indexing.py がその処理を work root と CLI の実行ライフサイクルへ接続する。

## Read this when
- CLI コマンドの登録、引数解釈、Typer/Click 互換処理、または cmoc の起動入口を確認したいとき
- サブコマンドの実行順序、doctor preprocess、ログ、feedback、primary report、終了結果、エラー処理を追いたいとき
- INDEX.md の生成・検査・ハッシュ検証・更新・commit の実装を確認したいとき
- Codex exec を使う oracle、realization、session、TUI、feedback builder の実行経路を確認したいとき
- 設定、パス、Git、Codex subprocess、Windows 通知などの共通 runtime API の責務を調べたいとき

## Do not read this when
- 正本仕様や人間の意図を確認したいときは oracle 配下を直接読む
- テストケース、fixture、回帰条件を確認したいときは test 配下を直接読む
- INDEX.md の利用者向けルーティング情報だけが必要なときは INDEX.md を読む
- 特定コマンドの詳細実装だけが必要で、CLI 全体の登録や共通 runtime の挙動を追う必要がないときは該当する sub_commands または commons のファイルを直接読む

## hash
- 0a482bd65aeb988ec0687e47247adab67815a03ef5d89737fa311595d4b7956e

# `test`

## Summary
- cmoc の実装全体を対象にした pytest テストスイートで、CLI コマンド、実行時設定、Codex subprocess/TUI 連携、プロンプト生成、ファイルアクセス、パス・Git worktree 境界を検証する。
- インデックス生成、oracle 編集・realization 実行、セッション管理、run の fork/join/apply/abandon、エラー復旧とロールバックなど、主要な開発ワークフローの状態遷移を検証する。
- feedback の MCP 通信、観測の正規化・保存・検証、再発判定、レポート生成、破損・中断時の復旧を検証する。
- 共通 fixture と補助モジュールはテスト環境の隔離、CLI 実行、Codex 応答、Git 操作、handoff を支え、特定機能の検証へ進むための入口となる。
- _real_path_integration は実パスを用いた統合検証を分離して扱う。

## Read this when
- 実装変更が CLI、ランタイム、Codex 連携、インデックス、feedback、セッション処理の既存動作に影響しないか確認したいとき
- 複数コンポーネントをまたぐ状態遷移、エラー処理、ロールバック、セキュリティ境界の回帰を調べたいとき
- どの機能領域のテストから読み始めるべきか判断したいとき

## Do not read this when
- 正本仕様や要求の根拠を確認したいときは oracle/doc または oracle/test を直接読むべきとき
- 単一機能の具体的な実装や一つのテストケースの詳細を確認したいときは対応する src または test ファイルへ直接進むべきとき
- 実パス依存の統合動作だけが目的のときは test/_real_path_integration へ直接進むべきとき

## hash
- b40d11c85bbf8d620797db79d6d6015d9646c24ff664f3a7984cbb7f9644ac4c
