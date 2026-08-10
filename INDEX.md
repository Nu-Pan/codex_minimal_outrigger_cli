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
- cmoc の正本仕様を収める領域への入口。アプリケーション仕様、branch・commit・worktree モデル、開発規則、不採用案の記録、および正本実装群を扱う。詳細確認では、仕様文書または用途別の実装下位領域へ進む。

## Read this when
- cmoc の正本仕様や正本実装を調査・変更するとき
- アプリケーション挙動、branch・commit・worktree のモデル、開発規則を確認するとき
- oracle src の共通実装やサブコマンド別の prompt・ACP 設定を確認するとき

## Do not read this when
- 特定機能の詳細仕様を確認する場合は、該当する oracle/doc の下位仕様書を直接読む
- 個別の実装責務が明らかな場合は、対応する oracle/src の下位領域を直接読む
- realization 側の CLI 挙動や実装を確認する場合は、対応する realization implementation を直接読む
- INDEX.md 生成規則や oracle／realization の一般原則を確認する場合は、専用の正本仕様を直接読む

## hash
- b9cbd5d1e32b9bfc26677afc5b302abcd4dce5a1ec7b1ccf1709e40a4c128049

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
- cmoc CLI の realization 側実装をまとめる最上位入口。CLI 起動、共通 runtime、ACP互換公開層、設定・互換 shim、各サブコマンドの実装を扱い、下位要素へのルーティングを提供する。

## Read this when
- realization 側実装全体の構成や、CLI・共通 runtime・ACP互換層・サブコマンドの入口を確認するとき。
- トップレベル CLI の起動経路、共通 helper の所在、サブコマンド実装の配置を判断するとき。

## Do not read this when
- 特定サブコマンドの詳細処理を調査するときは、対応する `sub_commands` 配下を直接読む。
- 共通 helper の具体的な挙動を確認するときは、`commons` 配下の該当モジュールを直接読む。
- ACP 型や builder の個別実装を確認するときは、`acp` 配下を直接読む。
- 設定定義や正本仕様を確認するときは、互換入口ではなく oracle 側の対応ファイルを直接読む。

## hash
- ec5e8dbcd0f497efbae4b7252e4cf230152fc74c5a91e4fcd756860732d92548

# `test`

## Summary
- pytest による realization test 群を収めるディレクトリ。CLI、runtime、Codex 実行、indexing、oracle review、session lifecycle などの外部挙動・永続状態・Git worktree・Structured Output 契約を検証し、個別テストファイルが各機能領域への入口となる。

## Read this when
- 実装変更や仕様確認に伴い、対象機能の外部挙動を検証する realization test を選ぶとき。
- CLI lifecycle、Codex runtime、indexing、oracle review、session、設定、通知などの回帰テストの所在を判断するとき。
- 複数の統合テストが扱う lifecycle、worktree、Git 差分、ログ、state の検証範囲を把握するとき。

## Do not read this when
- 正本仕様、設計意図、Structured Output schema の内容を確認するときは、対応する oracle 文書・schema を直接読む。
- 実装責務や処理フローの詳細を確認するときは、対象領域の src 実装を直接読む。
- 対象機能と関係しないテスト領域や、一般的な pytest 実行方法だけを調べるとき。

## hash
- 0a263f9f493ee824aca963bcef80918e5114850984fb158ae4dab4d683270bca
