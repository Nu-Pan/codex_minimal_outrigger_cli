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
- cmoc の正本資料と実装を束ねる最上位入口。アプリケーション仕様、branch・session 分離モデル、設計検討資料、開発ルールを機能別に選べる。
- oracle 実装の入口。agent call 構築、prompt 構築、入力 handoff、feedback、設定・パス・構造化文書の下位領域へ振り分ける。

## Read this when
- cmoc の仕様または oracle 実装について、最初に読むべき下位領域を選ぶとき。
- アプリケーション挙動、session・run の隔離、設計判断、Python 開発ルール、agent call、prompt、入力契約、設定・パスの複数領域を横断して調査するとき。

## Do not read this when
- 確認対象の個別仕様書、branch model、considered alternative、dev rule、または oracle 実装の下位領域が特定できているときは、その対象を直接読む。
- 特定の CLI 入出力契約、prompt 構築規則、入力形式、feedback 契約、設定モデル、パス解決、構造化文書の実装だけを確認するとき。

## hash
- a9fd1ca6799ff1eb68dd51811bc1edce624396263d0784791f04a601658e2f0e

# `pyproject.toml`

## Summary
- Python プロジェクトのパッケージ metadata、依存関係、CLI エントリーポイント、ビルド設定、pytest・Ruff・mypy の開発ツール設定を定義する正本設定。Python パッケージ構成や開発・品質検査の実行条件を確認する入口となる。

## Read this when
- 依存関係、対応 Python バージョン、`cmoc` CLI の公開エントリーポイント、パッケージ配置、ビルド方式を確認するとき
- pytest、Ruff、mypy のプロジェクト共通設定や開発用依存関係を確認するとき

## Do not read this when
- CLI の具体的な処理やランタイム挙動を確認したいときは、実装モジュールを直接読む
- テストケースの内容や仕様上の期待動作を確認したいときは、該当する仕様・テストを直接読む

## hash
- 6fb45f79a560a43b8ae51d23bdb53e4dc711587caffea78ce1020d595036510e

# `src`

## Summary
- cmoc の実行側ソースをまとめる最上位入口。Typer による CLI 登録と引数解析エラーの cmoc 形式変換を担い、doctor、TUI、session、oracle、realization、run、feedback、indexing などの処理へ振り分ける。
- 共通 runtime、互換 import shim、設定・基本型の公開入口、およびサブコマンド実装群を含む。各機能の実装や共通処理を調査するときの下位要素への入口となる。

## Read this when
- cmoc CLI の最上位コマンド構成、起動入口、Typer/Click 互換処理、または引数解析エラーの変換境界を確認したいとき。
- src 配下で、共通 runtime、互換 import、設定・基本型、または特定サブコマンドの実装へ進む入口を特定したいとき。

## Do not read this when
- 特定サブコマンドの処理フローや業務ロジックだけを確認したいときは、対応するサブコマンド実装を直接読む。
- 共通 runtime の個別処理、oracle の正本実装、設定・基本型の定義、または下位パッケージ固有の仕様だけを調査するときは、それぞれの定義元を直接読む。

## hash
- 1a7b87727a5936853aa4e0c9ba54ac6050a25680ed800ad51e5b520b6f44fea6

# `test`

## Summary
- cmoc の実装・CLI・Codex 実行・oracle/realization lifecycle・設定・Git・prompt・通知などを、単体テスト、統合テスト、実経路テストで検証するテスト群への入口。
- 各テストは個別機能の外部挙動、実装境界、正本仕様との適合、異常系や安全性の回帰条件を担当する。

## Read this when
- cmoc の特定機能を変更・調査し、その外部契約や回帰テストの対象範囲を把握したいとき。
- CLI lifecycle、Codex runtime、indexing、session、oracle review/edit/investigation、realization、feedback、設定、Git、prompt、TUI、通知などの検証入口を探すとき。
- 実経路・subprocess・PTY・worktree・永続 state・report まで含む統合挙動を確認したいとき。

## Do not read this when
- 正本仕様や実装の定義そのものを確認することが目的で、対応する oracle 文書または実装を直接読むべきとき。
- テスト対象に含まれない機能の詳細、一般的なテスト実行手順、または単一の実装内部アルゴリズムだけを調べるとき。

## hash
- 88026f3f2465bede4675627993d82d9e8a881b699279e2495a248da7b61a1207
