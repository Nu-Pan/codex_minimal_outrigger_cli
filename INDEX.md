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
- cmoc の正本仕様を保持する oracle 領域。アプリケーション挙動、branch・commit・worktree のモデル、不採用設計、Python 開発規則を文書として定義し、Agent call、prompt、feedback、レビュー、indexing などの正本ソースも提供する。配下の doc は仕様本文、src はその仕様に基づく prompt・builder・補助処理の実装へ進む入口。

## Read this when
- cmoc の現行仕様、設計上の用語や制約、CLI・session・run・feedback・prompt の挙動を確認するとき
- Python の開発環境、コーディング、CLI 設計、テスト規則や実行手順を確認するとき
- Agent call、Structured Output、prompt 構築、oracle／realization／feedback／INDEX の規範に関わる実装を調査・変更するとき
- 不採用となった設計案の背景や理由を確認するとき

## Do not read this when
- 特定の仕様文書、サブコマンド、開発規則、または実装ファイルが明確な場合は、対応する配下の対象を直接読むとき
- 通常の realization 実装・テストや CLI／TUI の実行処理そのものを調査するとき
- 現行仕様に関係せず、不採用案の検討理由も必要ない単純な作業を行うとき

## hash
- 8055a886f8c133d0f7c09fd8d97613e4655f23380adb448f1c715acf087556b3

# `pyproject.toml`

## Summary
- プロジェクトの Python パッケージ設定。依存関係、開発用依存関係、`cmoc` CLI エントリーポイント、パッケージ配置、pytest・Ruff・mypy の設定を定義する。

## Read this when
- 依存関係や Python バージョン要件を確認するとき
- `cmoc` コマンドのエントリーポイントやパッケージ構成を変更するとき
- pytest、Ruff、mypy のプロジェクト設定を確認・変更するとき

## Do not read this when
- 個別の CLI 処理や実装ロジックを確認するとき
- テストケースや oracle の正本仕様を確認するとき

## hash
- 62c23b5f8693844b19076cbd7c8e2cc4930ace5468300a33c0b5ae87e3886d9f

# `src`

## Summary
- cmoc の realization 実装パッケージ。ACP 互換入口、共通 runtime、設定 shim、CLI ルート、oracle 接続 shim、サブコマンド実装を提供する。
- CLI の公開入口から個別サブコマンド、共通 runtime、互換 import 経路へ進むための起点。

## Read this when
- cmoc の realization 側 CLI 全体の構成や公開 import 経路を確認するとき。
- CLI ルート、サブコマンド、共通 runtime、ACP 互換層の実装箇所を選ぶとき。
- `src` 起動時の oracle パッケージ接続や、設定・runtime の互換入口を調査するとき。

## Do not read this when
- 特定サブコマンドの詳細処理だけを調べる場合は、該当するサブコマンド実装へ直接進む。
- 共通 helper の具体的な挙動だけを確認する場合は、`commons` 配下の対応モジュールを直接読む。
- 正本仕様、oracle 実装、テスト内容を確認する場合は、それぞれの oracle または test 領域を直接読む。

## hash
- 957779aadf44f1bf30d8191367e5d553dab0b1d528dd4723e3436ea0918e3a38

# `test`

## Summary
- pytest による realization test 群を収録し、CLI、runtime、Codex 実行、indexing、oracle review、session、設定、通知などの外部挙動と回帰条件を検証する。個別テストは各機能領域の実装・正本仕様へ進むための入口となる。

## Read this when
- 対象機能の外部挙動、回帰条件、統合契約、エラー処理をテスト側から確認・変更するとき。
- CLI、Codex runtime、indexing、oracle review、session、Git、設定、通知など、対応するテスト領域を特定したいとき。

## Do not read this when
- 正本仕様や実装詳細そのものを確認・変更するときは、対応する oracle または src の対象を直接読む。
- テスト実行方法だけを確認するときは、repository local のテスト実行ルールを読む。
- 対象機能と無関係なテスト領域を調査するとき。

## hash
- 6ede5267a0e99a94302106c7e662ca454cb5d87ed60b3ff2956c8c8a43368bc4
