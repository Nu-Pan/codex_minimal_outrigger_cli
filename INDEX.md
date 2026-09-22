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
- cmoc CLI の起動点と Click/Typer のコマンドツリーを定義する入口。各サブコマンドの実装は `sub_commands` 配下へ委譲する。
- ACP 型の互換公開、設定定義の互換公開、共通 runtime API の再公開を含む基盤モジュール群。
- CLI サブコマンドの実行ライフサイクル、診断ログ、feedback、primary report、終了結果を統括する runtime 群。
- session・oracle・realization・run・feedback・doctor・indexing・TUI など、cmoc の操作単位ごとの CLI 実装を提供する `sub_commands` 群。
- サブコマンド実装が利用する builder、indexing、oracle/realization 操作、session join、TUI 起動などの処理単位を提供する `acp/builder` 群。
- パス、ACP、構造化文書など、CLI と builder が共有する基本型・補助機能を提供する `basic` 群。
- ログ、設定、git、実行状態、エラー、feedback、レポート、Codex 呼び出しなど、cmoc 全体の共通 runtime 機能を提供する `commons` 群。
- cmoc の設定定義と設定アクセスを提供する `config` 群。

## Read this when
- cmoc の CLI 全体構成、起動入口、サブコマンドの委譲先を把握したいとき
- runtime・builder・共通基盤・サブコマンドのどの領域から調査を始めるべきか判断したいとき
- CLI 実行の終了処理、診断、feedback、レポート連携を横断的に確認したいとき

## Do not read this when
- 特定サブコマンドの詳細な処理手順を確認したいときは `src/sub_commands` または対応する `src/acp/builder` 配下を直接読む
- 共通 runtime の個別責務を確認したいときは `src/commons` 配下の該当モジュールを直接読む
- 設定項目の定義だけを確認したいときは `src/config` 配下を直接読む
- 共有データ型や構造化文書の仕様だけを確認したいときは `src/basic` 配下を直接読む

## hash
- 0a4e70439f532a4c56e33f08cc7c29de2068d64ba1f05996809a4c4735db12f7

# `test`

## Summary
- CLI・ランタイム・Codex 実行系の挙動を検証するテスト群。
- インデックス生成、ファイル分類、Git／worktree、セッション状態、実行ライフサイクルの回帰テストを扱う。
- フィードバック収集・正規化・再確認・公開処理と、エディター入力ハンドオフや MCP 通信の境界挙動を検証する。
- ACP builder、プロンプト、設定、権限、quota retry、subprocess、TUI などの構成契約とエラー処理を検証する。
- `_support.py` と `conftest.py` は、上記テストで共有するリポジトリ、CLI、Codex、handoff 用 fixture・補助処理の入口である。

## Read this when
- 実装変更が CLI やランタイムの公開挙動、エラー処理、状態遷移に影響するか確認するとき。
- Git 管理、worktree、インデックス、ファイルアクセス、セッション／実行ライフサイクルの回帰を調べるとき。
- フィードバック報告、MCP 通信、エディター入力 handoff、Codex subprocess・quota retry の期待挙動を確認するとき。
- 変更箇所に対応する機能別テストファイルを探し、既存の検証ケースから調査を始めるとき。

## Do not read this when
- 正本仕様や builder の意図を確認する必要がある場合は、対応する `oracle` 配下を直接読む。
- 単一の実装詳細だけを確認し、既存の期待挙動や回帰リスクを調べる必要がないとき。
- 共有 fixture の使い方ではなく、個別機能の期待結果だけを確認したい場合は、該当する `test_*.py` を直接読む。

## hash
- 5d6371e727eac5176fba7afa7fb456da1d2aff008f24942426498f9d4724519a
