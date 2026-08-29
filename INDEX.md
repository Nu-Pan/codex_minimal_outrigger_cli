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
- cmoc の正本仕様・開発規則・運用モデル・設計判断を目的別に案内する文書群の入口。
- アプリケーション仕様や開発ルールなどの正本文書は doc 配下へ、実装・prompt・agent call の処理詳細は src 配下へ進むための起点。

## Read this when
- cmoc の仕様、開発・テスト規則、session/run の隔離モデル、または不採用設計を調査するとき。
- agent call の prompt 構築、Structured Output、feedback、oracle／realization、INDEX.md 生成などの実装文書を探すとき。

## Do not read this when
- 特定機能の仕様本文、開発環境やテスト実行、branch model の具体的契約など、担当する下位文書が明らかなとき。
- 実際の Codex CLI 起動・TUI 実行制御や、個別 schema の詳細を直接確認すべきとき。
- 実装ファイルやテストの具体的な挙動だけを調べるとき。

## hash
- 9c8225c8fdcb71e29afb9d35dda0b665ea834a59ce25be437aa6fb124deb9bef

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
- cmoc CLI の最上位入口とサブコマンド登録を担い、doctor、TUI、session、oracle、realization、run、feedback、indexing などの処理へ振り分ける。
- ACP、basic、config、oracle、cmoc_runtime の互換 import 入口を提供し、既存の公開参照を正本実装や実体モジュールへ接続する。
- 共通 runtime、ACP builder、サブコマンド実装をまとめ、CLI 実行、Codex 連携、feedback、INDEX 更新、session・run 管理などの下位領域へ進むための入口となる。

## Read this when
- cmoc の最上位 CLI コマンド構成、起動入口、Typer/Click の引数解析境界を確認したいとき。
- session、oracle、realization、run、feedback、doctor、indexing、TUI の実装配置を特定し、対応する下位対象へ進みたいとき。
- ACP builder、互換 import、共通 runtime のどの領域を読むべきかを `src` 配下で判断したいとき。

## Do not read this when
- 特定サブコマンド、builder adapter、runtime helper、互換モジュールの具体的な挙動を調査するときは、対応する下位対象を直接読む。
- 正本仕様や oracle 側の実装内容を確認するときは、`src` の CLI・互換入口ではなく対応する正本対象を直接読む。
- 個別の処理に関係しない CLI 構成や `src` 全体の配置だけを確認したいときは、該当する下位ディレクトリまたはファイルへ直接進む。

## hash
- 08d0fc5849250b871d3fa738d32a523e1e6c2eaaf7efc319799f45e15d8970b6

# `test`

## Summary
- `test` 配下は、cmoc の runtime・CLI・Codex 呼び出し・Git/worktree・session/run lifecycle・oracle review・indexing・feedback・通知などの外部契約を検証するテスト群への入口です。
- 単体テストから、独立 process・PTY・実 Codex CLI を使う実経路統合テストまで、成果物・永続 state・Git 状態・ログ・report・終了結果を観測して回帰を確認します。
- 対象機能の実装仕様ではなく、変更された機能に対応する具体的なテスト要件、異常系境界、統合 lifecycle、または packaged import 境界を確認するために進みます。

## Read this when
- cmoc の CLI、runtime、Codex、Git/worktree、session/run、oracle、realization、indexing、feedback、通知の外部挙動を回帰テストで確認するとき。
- 特定機能の成功・失敗・中断・cleanup・report・ログ・永続 state など、利用者から観測できる契約の検証条件を探すとき。
- 実 Codex CLI、独立 process、PTY、または隔離された packaged layout による実経路の受け入れ条件を確認するとき。

## Do not read this when
- 正本仕様、設計、実装アルゴリズム、schema の内容、または prompt 本文を確認することが目的のときは、対応する oracle・実装・schema を直接読む。
- テスト対象の外部挙動を変更せず、一般的な pytest 実行方法や Python 環境の規約だけを確認するとき。
- 対象機能が明確で、その機能専用の下位テストまたは実装・仕様の方が必要な契約へ直接到達できるとき。

## hash
- b4bd2e167e7b9a2eaf0bf63debeb345dde8e14ecf1aca34a2efb06ec99c6f6ba
