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
- cmoc の正本を集約する oracle 領域。利用者向け仕様、branch・commit・worktree のモデル、不採用設計の記録、開発ルールを提供する。
- app_spec は CLI の挙動、prompt、session・run、feedback、indexing、ログ、エラー処理などのアプリケーション仕様を扱う。
- branch_model は cmoc が管理する branch、commit、worktree の用語と関係を定義する。
- considered_alternative は realization refactor などで採用しなかった作業方式や設計案の理由を記録する。
- dev_rule はコーディング、設計、開発環境、テスト実装、テスト実行に関する開発ルールを定義する。
- src は oracle 側の実装基盤であり、agent call parameter、用途別 builder、prompt 構築、パス・設定・構造化文書モデル、feedback reporter 入力スキーマを扱う。配下の app_spec、branch_model、considered_alternative、dev_rule、src が個別確認の入口になる。

## Read this when
- cmoc の利用者向け仕様やサブコマンドの挙動を確認するとき。
- session・run の状態、branch・commit・worktree の関係、作業隔離を確認するとき。
- prompt、agent call、feedback、indexing、ログ、エラー処理などの正本仕様を探すとき。
- 採用されなかった設計案や realization refactor の判断理由を確認するとき。
- Python 実装、agent call builder、prompt builder、設定、パスモデル、構造化文書、feedback 入力スキーマの配置や責務を確認するとき。

## Do not read this when
- 確認対象の仕様本文、開発ルール、検討記録、または実装ファイルがすでに特定できているときは、その対象を直接読む。
- realization 側の実装やテスト、実行ログ、生成成果物の詳細を確認するとき。
- INDEX.md の生成規則やルーティング情報だけを確認するとき。

## hash
- 6920339227acbe4e3dbc1066608ce2694e73f0b83b8b7881aff4b8652f07bb08

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
- cmoc の realization 側実装を束ねる入口。Typer/Click による CLI の最上位入口、サブコマンド実装、共通 runtime、ACP/basic/config/oracle の互換公開経路を扱い、各領域の具体的な処理や正本実装へ進むための起点となる。

## Read this when
- cmoc realization 側の CLI 入口、サブコマンド構成、共通 runtime、互換 import shim の全体像を確認するとき。
- 特定の下位実装へ進む前に、src 内の公開入口と領域間の委譲関係を切り分けるとき。
- CLI、runtime、ACP/basic/config/oracle の互換経路を横断して調査・変更するとき。

## Do not read this when
- 特定サブコマンドの処理ロジック、個別 runtime helper、設定型、ACP 型、または正本 oracle 実装の詳細だけを確認したいときは、対応する下位実装や oracle 側を直接読む。
- 利用者向け仕様や Structured Output の定義を確認するときは、src 全体ではなく該当する正本仕様を読む。
- src と無関係な領域を調査・変更するとき。

## hash
- 9920fb4101ea1ed1fa24e979f70956f01d6fc6a2510fdab3977cef99b1a9da18

# `test`

## Summary
- cmoc の realization test 群を集約するディレクトリ。ACP builder、Codex runtime、CLI lifecycle、oracle review、session/run state、indexing、設定、通知など、実装の外部契約と回帰挙動を検証するテストへの入口である。個別機能の実装ではなく、対象機能のテスト範囲・受け入れ条件・境界挙動を把握するために読む。

## Read this when
- 実装や仕様の変更が、既存の外部挙動・状態遷移・エラー処理・Git/worktree 境界に与える影響をテスト側から確認するとき。
- 対象機能に対応する回帰テスト、統合テスト、または production-path test の位置を特定するとき。
- Codex 実行、CLI、indexing、oracle review、session/run lifecycle、設定、通知などの検証対象を横断的に把握するとき。

## Do not read this when
- 正本仕様や実装責務そのものを確認することが目的の場合は、対応する oracle 文書または src 実装を直接読む。
- 個別テストの詳細なケース構成が不要で、単にテスト実行手順だけを確認したい場合は、repository local の test execution 指示を読む。
- 対象機能と無関係な領域の挙動を調査する場合は、このディレクトリを総当たりせず、対応する実装・仕様・個別テストへ直接進む。

## hash
- e99ec694cc4d60f3a10f23dc90684db09548ca921d096f30c4cb5235230ee417
