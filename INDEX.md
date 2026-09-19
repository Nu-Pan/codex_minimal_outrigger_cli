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
- 人間が所有する正本仕様を、意味仕様の文書と、prompt・path・agent call などの正確な構築定義に分けて保持する領域。
- アプリケーション仕様、branch model、開発規則、代替案の検討記録を含み、cmoc の責務・制約・判断基準を定義する。
- prompt builder と ACP builder の oracle 実装が、仕様で委譲された prompt 文面・schema・起動パラメータ・パスモデルを具体化する。

## Read this when
- cmoc の正本仕様、責務分担、branch/run のモデル、サブコマンドの挙動、開発規則を確認するとき。
- oracle doc と oracle src のどちらが対象事項の正本を所有するか判断するとき。
- agent prompt の構築、INDEX エントリー生成、path context、agent call parameter の正確な定義を変更・レビューするとき。

## Do not read this when
- realization の実装やテストの具体的な挙動だけを調べる場合は、まず src または test の該当対象を直接読む。
- 既存仕様を参照せずに一般的な設計・実装方針だけを検討する場合。
- 過去の代替案や検討経緯が不要で、確定した個別仕様だけを確認したい場合は、関連する app_spec または dev_rule の対象を直接読む。

## hash
- f0e068affefb9899a3553bcb7de998603590bf87e1a9468e46beb362d0678db1

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
- cmoc の CLI 起動入口とコマンドツリーを定義し、doctor・tui・session・oracle・realization・run・feedback・indexing などの処理へ振り分ける。
- CLI やサブコマンドから利用される共通 runtime、設定、Git・パス・状態・ログ・Codex 実行・feedback・run などの横断的 helper を提供する。
- acp・basic・config の旧公開 import と oracle パッケージの互換入口を維持し、canonical 実装または正本側 package への導線を提供する。
- サブコマンド固有の処理を目的別ディレクトリにまとめ、各 CLI 入口から lifecycle・workload・report・修復処理などの下位実装へ進む起点を提供する。

## Read this when
- cmoc の CLI コマンド階層、起動経路、引数解析や補完の境界処理を確認・変更するとき。
- 複数のコマンドで共有される runtime helper、設定、状態、ログ、Codex 実行、feedback、Git、パス処理の実装場所を探すとき。
- acp・basic・config・oracle などの互換 import 経路や、src 起動時の正本 package 解決を確認するとき。
- 特定サブコマンドの CLI 入口から対応する下位実装を見つけるとき。

## Do not read this when
- 個別サブコマンドの lifecycle、workload、report、prompt 編集、判定、修復処理の詳細だけを調べるときは、対応する sub_commands 配下を直接読む。
- 共通 runtime helper の個別仕様や内部挙動だけを確認するときは、commons 配下の該当モジュールを直接読む。
- 互換入口ではなく oracle 側の canonical 実装や利用者向け正本仕様を確認するときは、oracle/src/oracle または対応する仕様書を直接読む。

## hash
- 46f58af1d50648e044a0fb8c8fc6612209a3fa32de64705f6eff210ebf251944

# `test`

## Summary
- `test` 配下のテスト群を、共有 fixture・runtime 基盤・Codex 実行・CLI lifecycle・各サブコマンド・正本連携などの回帰検証へ案内する入口。実装や仕様ではなく、外部挙動・境界条件・統合契約をテストから確認するために用いる。

## Read this when
- cmoc の機能変更に対する回帰テスト、外部から観測できる実行契約、エラー・状態遷移・Git・filesystem 境界の検証箇所を探すとき。
- Codex runtime、CLI runner、TUI、doctor、indexing、feedback、session、oracle／realization などの機能ごとのテスト入口を選ぶとき。
- 共有 fixture、テスト用 Git／Codex／外部コマンド環境、実経路統合テストの検証範囲を確認するとき。

## Do not read this when
- 対象機能の正本仕様や実装詳細そのものを確認・変更するときは、対応する oracle または src の対象を直接読む。
- INDEX.md のルーティング規定や、Structured Output schema の定義自体を確認するとき。
- テスト対象と無関係な機能の実装・仕様や、単なる一般的な pytest 実行方法だけを調べるとき。

## hash
- 4366760015601721f39fc73a013e4a1eb7553fe68ce908d60286fbf00d890367
