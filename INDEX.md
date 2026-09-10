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
- cmoc のアプリケーション仕様、設計判断、開発ルールを横断して参照する上位文書群への入口。
- agent 呼び出しの共通設定、prompt 構築、用途別 builder、quota probe、indexing、feedback、session、TUI などを扱う oracle 実装ソースへの入口。

## Read this when
- cmoc の複数機能にまたがる正本仕様や、仕様・設計資料・開発ルールの参照先を判断するとき
- agent call のパラメータ、パス、prompt 構築、policy 注入、用途別の呼び出し経路を確認するとき

## Do not read this when
- 単一機能の具体的な挙動、状態遷移、prompt、実装詳細、契約、またはテスト手順を直接確認したいときは該当する下位対象を読む
- 実装コード、実行結果、診断ログなど、oracle の仕様・実装入口が担わない対象だけを調べるとき

## hash
- 1755af272457d304ecffb1795c9981fb05e6a75d42056750348a0a64d2edc941

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
- cmoc の CLI 起動入口とコマンドツリーを構成し、doctor・tui・session・oracle・realization・run などの実装へ接続する。
- 共通 runtime helper と、CLI・Codex 実行・設定・Git・状態・結果・feedback など複数経路で共有する基盤機能への入口を提供する。
- oracle.*、acp.*、basic.*、config.*、cmoc_runtime の旧 import path を互換入口として維持し、正本実装または責務別 runtime module への移行を支える。
- CLI サブコマンドの実装を領域別に配置し、doctor・feedback・indexing・oracle・realization・run・session・tui への振り分け起点を提供する。

## Read this when
- cmoc の CLI 全体の起動経路、コマンド登録、Typer／Click の互換境界を確認するとき。
- 複数の CLI・Codex・session／run・feedback 経路で共有される runtime 機能の責務と入口を確認するとき。
- 旧 import path の互換性、oracle 正本や責務別 runtime module への移行経路を確認するとき。
- 特定の CLI サブコマンドがどの領域に配置され、どの実装へ進むべきか判断するとき。

## Do not read this when
- 特定サブコマンドの入力、状態遷移、業務処理を確認・変更するときは、対応する sub_commands 配下を直接読む。
- 共通 runtime の個別 API、エラー分類、保存形式、protocol、subprocess 挙動を確認するときは、対応する commons の runtime module を直接読む。
- 互換入口の移行先にある oracle.* の正本仕様・実装や、basic／config／acp の個別公開内容を確認するときは、各再公開元・実体モジュールを直接読む。
- INDEX.md の生成・検査や feedback observation の詳細仕様だけを確認するときは、indexing／feedback の実装または正本仕様を直接読む。

## hash
- b04bb1021bfb8ed4dec259f152ec4328571c9047834a3f102c5b9e1d265a1fbd

# `test`

## Summary
- テスト群は、ACP builder・Codex runtime・CLI・TUI・editor input・session/run state・Git・feedback・indexing など、cmoc の主要機能に対する外部契約と回帰条件を検証する。
- 単体から実経路統合テストまで、prompt・Structured Output・sandbox・process 管理・通知・report・state・worktree・commit の挙動を観測可能な結果として確認する。
- 正常系だけでなく、入力不備、Codex 出力異常、失敗・中断、競合、symlink・特殊ファイル、破損 state、cleanup・rollback などの安全境界を扱う。
- 各テストは、対象機能の実装や正本仕様を直接読む前に、どの外部挙動と回帰条件が既に検証されているかを確認するための入口となる。

## Read this when
- cmoc の CLI、Codex 実行、TUI、builder、editor input、session/run lifecycle、Git、feedback、indexing、report、通知、state の挙動をテスト観点から調査・変更するとき。
- 実際の process・PTY・worktree・branch・commit・filesystem・ログ・report など、複数の外部状態にまたがる統合契約を確認するとき。
- 異常系、再試行、競合解消、権限境界、入力検証、破損検出、復旧、cleanup、rollback の回帰条件を探すとき。
- 複数のテスト領域にまたがる変更について、既存の公開面・実行順序・保存結果・副作用の検証範囲を把握するとき。

## Do not read this when
- 単一モジュールの実装詳細、prompt の正本文面、Structured Output schema、CLI 個別仕様、または state・report の正本データ形式を直接確認することが目的のとき。
- テストが扱わない機能の一般仕様や、個別サブコマンドの局所的な通常系だけを調べるとき。
- テスト fixture・共通 helper・個別ケースの詳細を直接読む必要があり、ディレクトリ全体のテスト責務を把握する必要がないとき。

## hash
- 505673d618cc229f5b330e07023a7cb2f79034d29a6d8a1d272cc325e17887a1
