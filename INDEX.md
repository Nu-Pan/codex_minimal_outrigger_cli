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
- cmoc の正本仕様・開発規約・設計判断記録と、それらを実装へ反映する oracle 側の agent call 定義をまとめた参照群への入口。
- app spec、branch model、開発・テスト規約、採用しなかった代替案を通じて、cmoc の共通仕様と設計上の判断根拠を確認できる。
- quota、indexing、feedback、oracle・realization、session join、TUI などの調査・編集・修正処理に対応する prompt、構造化入力、Python 実装の参照起点。

## Read this when
- cmoc の正本仕様や開発規約、設計判断の背景を確認し、複数の専門領域にまたがる参照先を選びたいとき。
- agent call の prompt 構成、ファイルアクセス方針、Structured Output、editor input handoff、または用途別の起動条件を調べるとき。
- oracle・realization・feedback・indexing・session join などの調査や編集を、仕様と実装の両面から追跡したいとき。

## Do not read this when
- 特定機能の詳細仕様、個別の設定や schema、実装 module、テスト要件が明らかな場合は、対応する下位対象を直接読むとき。
- 実際のログ、成果物、個別の不具合所見、feedback observation、oracle／realization の具体的な調査結果だけを確認するとき。
- INDEX.md の生成規則や既存の目次内容だけを確認したいとき。

## hash
- cca6d5cd4253d08a6c2ce1918661c62376332b7448fc4b605889a3a0b428e878

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
- CLI の起動入口と Typer/Click 境界処理を定義し、doctor・tui・session・oracle・realization・run・feedback などのサブコマンドを接続する。
- acp.* の旧公開 import を維持する互換名前空間。oracle 側の acp_builder やその配下を複製せず、既存参照を正本または実体モジュールへつなぐ。
- basic.* の旧公開 import を維持する互換名前空間。ACP 基本型、path model、構造化文書などの正本側 API への互換入口を提供する。
- 複数の cmoc 実行経路で共有される runtime helper と lifecycle 境界をまとめる。設定、CLI、Codex 実行、Git、ログ、パス、状態、結果、feedback、report、editor handoff などの責務別 runtime への入口となる。
- 共通 runtime API を互換 import path から再公開し、既存呼び出し元を commons 側の runtime 実装へ接続する。
- oracle 側の設定型を config.* として再公開する互換入口。
- cmoc の各サブコマンド実装をまとめ、feedback・oracle・realization・run・session の個別処理へ進むための上位入口となる。

## Read this when
- cmoc の CLI コマンド階層、起動経路、引数解析エラー、補完、Typer/Click 互換処理を確認・変更するときは main.py を読む。
- 既存の acp.* import を維持・削除する条件や oracle.acp_builder への移行経路を確認するときは acp を読む。
- 既存の basic.* import を維持・削除する条件や正本側 API への委譲経路を確認するときは basic を読む。
- 複数の実行経路で共有する runtime の責務や、設定・Codex・Git・state・feedback・report・editor handoff などの下位実装への進み先を判断するときは commons を読む。
- cmoc_runtime という互換 import path の公開面や commons 側への移行状況を確認するときは cmoc_runtime.py を読む。
- config.* から oracle 側設定型へ至る互換 import 経路を確認するときは config を読む。
- サブコマンド全体の構成や、feedback・oracle・realization・run・session の実装へ進む起点を確認するときは sub_commands を読む。

## Do not read this when
- 特定の CLI サブコマンドの業務処理や内部ワークフローだけを調べるときは main.py ではなく対応する sub_commands 配下を読む。
- acp の具体的な builder 実装、入力制約、生成結果、または正本側 oracle.acp_builder の詳細だけを確認するときは acp ではなく対応する下位要素や正本実装を直接読む。
- basic の個別 API の定義・仕様や利用箇所だけを確認するときは basic 全体ではなく再公開元または参照元を直接読む。
- commons の単一 runtime module の内部挙動、個別 CLI の業務フロー、schema 定義そのものだけを確認するときは commons 全体ではなく該当対象を直接読む。
- 共通 runtime の実装内容や個別 API の責務だけを確認するときは cmoc_runtime.py ではなく commons.cmoc_runtime または責務別 runtime module を読む。
- 設定型の定義や設定値の仕様そのもの、config.cmoc_config の新規参照経路を確認するときは config の互換入口ではなく正本または実装を直接読む。
- 特定サブコマンドの具体的な処理詳細やサブコマンド外の共通 runtime・永続 artifact の仕様だけを確認するときは sub_commands の入口を経由せず対象を直接読む。

## hash
- 44a510dea6a11ddf6761fee617d65911aa5a5011cbbd069469320a4b6afff143

# `test`

## Summary
- cmoc のテストスイートへの入口。CLI、Codex runtime、session/run lifecycle、feedback、indexing、oracle/realization、設定、Git・path・通知など、実装の外部契約と安全境界を回帰検証する。
- 個別機能の単体テストから、独立 process・実 Codex CLI・PTY を用いる本番経路統合テストまでを含み、状態・report・Git・ログなど観測可能な結果を横断的に確認する。

## Read this when
- cmoc の実装変更が既存の CLI 外部挙動、Codex 呼び出し、state/report、Git・filesystem 安全性、MCP、通知、prompt、indexing、oracle/realization に影響する可能性があるとき。
- 特定機能の回帰条件や、対応するテストの責務・検証範囲を探すとき。
- 実推論や PTY を含む本番経路の受け入れ試験範囲を確認するとき。

## Do not read this when
- 正本仕様、schema、実装本体の詳細を確認することが目的で、テストの期待挙動を調べる必要がないとき。
- 単一の実装関数や仕様書を直接読む方が適切で、テストスイート全体の回帰範囲を確認する必要がないとき。
- 対象機能と無関係なテストや、単純なテスト実行方法・機械的なファイル配置だけを確認したいとき。

## hash
- 80fe195683ffbc532903a3cc4569dd5302a03a6116f96a6bfc14cae2d23f7115
