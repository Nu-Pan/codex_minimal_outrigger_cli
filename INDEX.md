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
- 仮想環境内の Python を検証し、cmoc の Python CLI 本体へ委譲する起動ラッパーを含む。通常実行時のエラー表示、補完プローブ、ユーザー向けパスとコールスタック行番号の組み立てを扱う。cmoc の起動経路やラッパーの表示・エラー処理を確認する際の入口。

## Read this when
- cmoc の起動経路、仮想環境 Python の検証、補完プローブ、ラッパーのエラー出力や表示パスを確認・変更するとき。

## Do not read this when
- Python CLI 本体のコマンド挙動やドメインロジックを調べるときは、委譲先の実装を直接読む。開発環境の正本仕様を確認するときは、参照されている oracle 文書を読む。

## hash
- 2b049993c6378dede2a9d759c9dd13b8795479d1bc900a42c174e227e8ce2e0b

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
- cmoc の正本仕様と、その仕様を具体化する oracle 実装定義・Structured Output schema を集約する領域。利用者向け挙動、session・run・branch のモデル、開発・設計・テスト規則、不採用案の記録、および agent call・feedback・prompt 構築に関する実装定義を扱う。
- 利用者向け挙動、workflow、状態遷移、サブコマンド、ログ、feedback、prompt、Codex 呼び出しの正本を確認するときは doc/app_spec へ進む。
- branch・commit・worktree と session/run の関係を確認するときは doc/branch_model.md へ進む。
- Python 環境、CLI 設計、コーディング、テスト要件、テスト実行手順を確認するときは doc/dev_rule へ進む。
- realization refactor などで採用しなかった作業方式や設計判断の理由を確認するときは doc/considered_alternative へ進む。
- agent call の起動定義、feedback の検証・正規化、共通モデル、prompt 構築の実装定義や schema を確認するときは src/oracle 配下の acp_builder、feedback、other、prompt_builder へ進む。

## Read this when
- cmoc の正本仕様を探し、アプリケーション仕様・開発ルール・設計ルール・テスト規則・検討記録の入口を選ぶとき
- session、run、branch、commit、worktree の用語や lifecycle の関係を確認するとき
- agent call、feedback、共通設定・構造化文書、または prompt 構築の oracle 実装定義を調査するとき
- realization refactor の現行方針と、不採用となった代替案の理由を確認するとき

## Do not read this when
- 確認対象の個別仕様、開発ルール、検討記録、または oracle 実装定義がすでに特定できており、その対象を直接読めるとき
- realization の実装コード、realization test、実行ログ、実行成果物の詳細を調べるとき
- INDEX.md の生成規則やルーティング情報だけを確認するとき

## hash
- be1073a73f20d1b4df4709a80cbe1267e27352d71eaa392b976af05cd992d71c

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
- cmoc の realization 側ソースツリー入口。`acp` や `basic` などの互換公開層、`commons` の共通 runtime、CLI トップレベル、各サブコマンド実装へ進むための構成を示す。正本側 `oracle.*` への互換 shim と、個別サブコマンドの実装配置を横断して確認する起点となる。

## Read this when
- realization 側の CLI 全体構成や、主要な互換公開層・共通 runtime・サブコマンド実装の配置を把握するとき
- `acp`、`basic`、`config`、`commons`、`oracle` shim、または `sub_commands` の下位実装へ進む入口を判断するとき
- トップレベル CLI の登録から個別サブコマンド実装までの接続構成を調査するとき

## Do not read this when
- 正本側 `oracle.*` の仕様・実装・処理ロジックだけを確認したいとき
- 特定サブコマンド、runtime helper、互換 shim の詳細だけを確認したいときは、対応する下位対象へ直接進む
- `src` 配下と無関係な正本仕様、テスト、workload 本体を調査するとき

## hash
- 17990e46890ef7f16afb95d2bfb5b274d0ccb6fcebd412cc51d3ca916c58b2d6

# `test`

## Summary
- `test` ディレクトリは、cmoc の realization 実装に対する pytest 回帰・統合・実経路テストをまとめた検証入口です。CLI の各サブコマンド、Codex runtime、worktree・Git・state 管理、indexing、oracle review、prompt・ACP builder、通知、packaging の外部挙動を確認します。
- 個別テストは、doctor・session・editing run・oracle 操作・feedback・indexing などの lifecycle、Codex の exec/TUI・retry・quota・process cleanup・権限、設定・refactor state・ファイル列挙、prompt rendering と builder 契約に分かれています。共通 fixture と fake subprocess、テスト用 Git repository、実経路 subprocess 用補助もここから参照できます。

## Read this when
- cmoc の変更に対応する realization test、統合 test、または本番経路受け入れ test の対象を特定するとき。
- CLI lifecycle、Codex subprocess、worktree・branch・Git 差分、永続 state、indexing、oracle review、prompt builder の外部契約をテストから確認するとき。
- 単一機能のテストだけでなく、fork から join/abandon、preflight から Codex 実行、失敗から cleanup までの横断的な回帰範囲を確認するとき。
- テスト共通の Codex double、Git repository fixture、fake external command、toast 隔離、packaged import または実経路 subprocess の支援方法を確認するとき。

## Do not read this when
- 正本仕様、schema、oracle implementation、または realization implementation の意味を確認することが目的の場合。対応する oracle または src ファイルを直接読む。
- 特定の単一テストケースの実装詳細だけを調べる場合。該当する個別 test ファイルへ直接進む。
- テストの実行手順や品質検査の選択だけを確認する場合。repository local の test execution 指示を読む。

## hash
- 715d51b6c599f2ca10e350d81340e1d340d81014638dd23f23fe4d341a0f7557
