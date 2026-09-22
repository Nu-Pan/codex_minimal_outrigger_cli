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
- cmoc の実行可能な realization 実装をまとめる最上位ディレクトリ。CLI 起動とサブコマンドの入口、共通 runtime・設定・基本型、ACP builder を束ね、正本 oracle 側の型や実装を互換 import path として再公開する。
- CLI の起動方法や全体構成を確認するときは main.py と sub_commands/、複数のコマンドで共有される実行状態・Codex 呼び出し・Git・ログ・レポート処理を確認するときは commons/、正本由来の公開型・構造化文書・path model・設定を確認するときは basic/ と config/ へ進む。
- ACP 用の agent 呼び出しパラメータ生成、realization/oracle の編集・調査・review、index entry 生成、session・TUI 連携を確認するときは acp/ 配下へ進む。

## Read this when
- cmoc の realization 実装全体の責務分担や、CLI・共通 runtime・ACP builder・互換公開層の入口を把握したいとき。
- 新しいサブコマンドや共有 runtime 処理の配置先を判断するとき。
- 複数の下位パッケージにまたがる処理の起点を特定し、適切な下位ディレクトリへ読み進めたいとき。

## Do not read this when
- 特定の CLI サブコマンドの挙動だけを調べる場合は sub_commands/ の該当項目を直接読むとよい。
- 共有 runtime の個別責務だけを調べる場合は commons/ の該当 runtime module を直接読むとよい。
- ACP の特定の parameter builder や編集フローだけを調べる場合は acp/ 配下の該当 builder を直接読むとよい。
- 正本仕様や oracle 側の実装そのものを確認する場合は src/ ではなく oracle/ 配下を読むべきである。

## hash
- 5728adae456762deff8c5bbfcfa611f220d6cfad5f34f52b82f1c445c368f3c6

# `test`

## Summary
- cmoc の実装・CLI・Codex 実行・セッション管理・ファイル分類・プロンプト生成などを対象に、pytest で挙動と回帰条件を検証するテストスイート。
- 主要な test_*.py は機能領域ごとに分かれ、対応する src 実装の境界条件、エラー処理、状態遷移、入出力を確認する。
- _*.py の補助モジュールは、CLI 呼び出し、Git 操作、Codex 応答、ACP ビルダー、ハンドオフなどのテスト用共通 fixture・stub・ヘルパーを提供する。

## Read this when
- 実装変更が CLI コマンド、Codex ランタイム、セッション／ワークツリー操作、設定・状態管理、ファイルアクセス、プロンプト、フィードバック、インデックス生成の挙動へ影響する場合。
- 既存仕様の回帰条件や、異常系・競合・パス検証・プロセス終了処理の期待動作を確認したい場合。
- テスト用の共通モックや補助関数の利用方法を確認したい場合は、対象テストと併せて test/_*.py を読む。

## Do not read this when
- プロダクトの具体的な実装方法や本体ロジックを確認したい場合は、まず src 配下の対応モジュールを直接読む。
- 正本仕様や要求の定義を確認したい場合は、oracle 配下を読む。
- 単一機能の期待動作が明確で、対応する個別テストファイルが分かっている場合は、このディレクトリ全体ではなくそのテストを直接読む。

## hash
- 13f4d620eb6f97b1451adb909e4061791cc531fd6d3126178a38a28f679697a7
