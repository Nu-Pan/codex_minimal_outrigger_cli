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
- cmoc の CLI 起動境界とトップレベル command tree を定義する入口。引数解析、補完、Click/Typer 互換処理、サブコマンド実装への振り分けを確認するときに読む。
- 共通の基礎型・パスモデル・構造化ドキュメント・oracle import shim を提供する基盤層。実装間で共有されるデータ型や oracle 側公開 API との互換境界を確認するときに進む。
- サブコマンド共通の runtime 層。CLI 実行ライフサイクル、doctor、ログ、エラー、feedback、Git、state、primary report、Codex 実行、run/session 管理など横断的な処理を確認するときに読む。
- session、run、oracle、realization、feedback、indexing、doctor、TUI など利用者向け操作の command 実装群。特定の CLI 操作の事前条件、状態遷移、Git 操作、agent 呼び出しを変更・調査するときは該当する下位パッケージへ進む。
- ACP builder 層は、index entry、feedback、oracle 編集・調査、realization の apply/refactor、session join など agent 呼び出し用パラメータの構築を担う。agent への入力形式や builder 固有の処理を確認するときに読む。
- 設定と公開用互換モジュールを含む cmoc の実装ソース全体。特定の機能を調べる場合は、まず該当する runtime、sub_commands、builder の下位対象を直接読む。

## Read this when
- cmoc の実装全体の責務分担や、CLI 入口から共通 runtime・サブコマンド・ACP builder へ至る構成を把握したいとき
- 複数の command や共通 runtime にまたがる変更箇所を特定したいとき
- トップレベルの import、公開互換層、設定、CLI 起動挙動の所在を確認したいとき

## Do not read this when
- 単一の CLI サブコマンドの詳細だけを調べる場合は src/sub_commands 配下の該当ファイルを直接読む
- 共通 runtime の一機能だけを調べる場合は src/commons 配下の該当 runtime モジュールを直接読む
- agent 呼び出しパラメータの構築だけを調べる場合は src/acp/builder 配下の該当 builder を直接読む
- oracle の正本仕様やテストの内容を確認することが目的の場合は src ではなく oracle または test の該当対象へ進む

## hash
- cd7e7a151a44e143f6bb1b8ac5be052f82da876dc289afb993c14220924b68af

# `test`

## Summary
- pytest による cmoc の実装・CLI・Codex 実行・Git/worktree・session state の回帰検証を集約するテストスイート。
- ACP builder、prompt builder、設定・状態永続化、ファイルアクセス、Windows 通知などの単体契約を検証する。
- doctor、editing run、session fork/join/abandon、oracle 操作、indexing、TUI などの CLI 外部挙動と失敗時のログ・通知・ロールバックを検証する。
- 共有 fixture/helper と、独立プロセス・PTY・実 Codex CLI を用いる受け入れ試験も含む。

## Read this when
- テストスイート全体の責務範囲や、ある実装変更がどの回帰テスト群に影響するかを把握したいとき。
- CLI lifecycle、Codex runtime、Git/worktree、session state、設定、prompt、builder の挙動をテストから確認したいとき。
- 共有 fixture、fake 外部コマンド、Git repository、Codex home、Windows toast 隔離などのテスト実行基盤を確認したいとき。

## Do not read this when
- 特定機能の正本仕様や実装の詳細を確認したいときは、対応する oracle または src 配下を直接読む。
- 単一テストの具体的な期待値や再現手順だけを調べる場合は、該当する test_*.py を直接読む。
- real path integration の個別ルーティングを確認する場合は、test/_real_path_integration/ 配下を直接読む。

## hash
- 903c06eda560e58bd229e20164727e4a95f3cc5ca0f0aac62a2f9386162494ab
