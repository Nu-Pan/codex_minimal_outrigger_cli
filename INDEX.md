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
- cmoc のアプリケーション仕様、branch・commit・worktree モデル、開発・テスト規約、採用しなかった設計案を集約する正本文書群への入口。機能仕様は app_spec、開発・テスト関連は dev_rule、branch 関係は branch_model.md、代替案の背景は considered_alternative 配下へ進む。
- src は oracle ソース全体の責務と、agent call 構築、prompt・policy、feedback 入力契約、設定・パス解決、構造化文書モデルに関する下位対象への入口。

## Read this when
- cmoc の正本文書を横断的に探し、仕様、branch モデル、開発規約、テスト規約、設計代替案の領域を判断するとき
- 複数の機能領域にまたがる調査・変更で、適切な下位文書群への入口を特定するとき
- agent call 構築、prompt 統合、policy、feedback 入力契約、設定・パス解決、構造化文書モデルを調査するとき

## Do not read this when
- 個別仕様、branch・worktree 用語、開発環境、実装配置、テスト要件、テスト実行手順が明らかで、該当する下位文書を直接読めるとき
- 実装コード、既存の INDEX.md、Structured Output schema、外部契約の検証結果だけを確認したいとき
- 実際の Codex CLI 呼び出しや実行基盤、個別の oracle 文書、realization 実装・テスト、feedback state、CLI サブコマンドの具体的挙動だけを確認したいとき

## hash
- a98709111b4efdc4a40777ca37431822628dab691c0e3f37936b646d9384bb67

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
- `src` は cmoc の realization 側 Python パッケージ群と最上位 CLI 入口を収める実装ディレクトリ。互換 import shim、共通 runtime helper、CLI サブコマンド、ACP adapter など、利用者向けの実行経路から下位モジュールへ進むための入口となる。

## Read this when
- cmoc の realization 側で、最上位 CLI、共通 runtime、互換 import、ACP adapter、または CLI サブコマンドの実装入口を特定するとき
- `src` 配下のパッケージ構成を把握し、対象機能に対応する下位ディレクトリやモジュールへ進む必要があるとき

## Do not read this when
- 特定機能の内部実装や正本仕様だけを確認したいときは、`src` 直下ではなく対応する下位モジュールまたは oracle 側の対象を直接読む
- `src` 配下にない正本仕様、開発規約、テスト実行手順を確認するときは、それぞれの文書や手順の入口を直接読む
- CLI や realization 側の実装に関係しない調査を行うとき

## hash
- f274c6db1f732598020bdb2ec08876a41bb9350ecb0b4439355ea96f879d7886

# `test`

## Summary
- `test` ディレクトリは、cmoc の realization test と共有 test helper を集約する検証入口である。ACP builder、Codex runtime、CLI lifecycle、indexing、session/run、oracle review、feedback、設定・状態永続化などの外部契約と境界条件を扱う。
- 個別テストは対応する実装や oracle 仕様へ進む前に、変更対象の回帰挙動、統合 lifecycle、エラー処理、Git・worktree・process・report の境界を確認するために読む。

## Read this when
- cmoc の CLI、runtime、Codex 呼び出し、ACP builder、indexing、session/run、oracle review、feedback、設定、永続 state の外部挙動を変更・検証するとき。
- 複数コンポーネントにまたがる lifecycle、worktree 隔離、Git 差分、report、ログ、通知、cleanup、失敗復旧の回帰条件を確認するとき。
- 変更対象に対応する realization test や共有 fixture の入口を特定するとき。

## Do not read this when
- 正本仕様、prompt policy、Structured Output schema、builder 実装、runtime 実装の詳細だけを確認する場合は、対応する oracle 文書・schema・実装ファイルを直接読むとき。
- 単一の補助関数や個別実装の内部ロジックだけを調べる場合は、該当するテストまたは実装へ直接進むとき。
- test と無関係な機能、または一般的なテスト実行手順・品質規約だけを確認するとき。

## hash
- 7121b1484172dae6b7bbd3d2dc788499c3269de57f7f15947571a265b3839682
