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
- プロジェクトルートと仮想環境の Python 実行可能性を確認し、Python CLI エントリーポイントへ引数を委譲する起動用シェルラッパー。通常起動時の環境不足エラーと補完プローブ時の簡略的な失敗経路を扱う。

## Read this when
- 起動前の環境検査、仮想環境 Python の利用可否、シェルから Python CLI への引数委譲を確認または変更するとき
- 通常起動と補完プローブ起動で仮想環境が利用できない場合の扱いを確認するとき

## Do not read this when
- CLI の実際のコマンド処理や業務ロジックを調べるとき
- エラー文面の正本仕様や Python 実装の詳細を確認するとき

## hash
- f8265a802567113e11bc0dc3e9a36c679a1f9bc9dce4b43a798d178594f3150d

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
- cmoc の正本文書群への入口。アプリケーション仕様、branch・commit・worktree のモデル、設計上の代替案、Python・CLI・環境・テストなどの開発規約を領域別に案内し、個別文書へ進むためのルーティングを提供する。

## Read this when
- cmoc の正本仕様・設計資料・開発規約の入口を特定するとき
- アプリケーション挙動、branch model、設計上の代替案、Python・CLI・環境・テスト規約のいずれかを調査するとき
- 個別文書へ進む前に、対象領域の文書群を選びたいとき

## Do not read this when
- 対象の個別仕様や設計・テスト文書が既に特定できており、上位の文書群一覧を確認する必要がないとき
- 具体的な実装配置や CLI 実装の責務だけを確認するとき
- テストの実行手順だけを確認するとき

## hash
- 524a170ceb22695a0058a293eecafd48dff3cf922181feaa4abe69f8ebd48ba5

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
- `src` は realization 側の実行ソースと互換公開入口をまとめ、CLI 起動、サブコマンド、共通 runtime、設定・型の再公開を担う。直下の各要素から、CLI 登録層、サブコマンド実装、共通 helper、互換 shim の詳細へ進むための入口である。

## Read this when
- cmoc の realization 側 CLI 起動経路や直下パッケージの責務分担を確認するとき
- CLI サブコマンド、共有 runtime、設定・型の互換 import 入口の配置を把握するとき
- `src` 直下から、調査対象となる個別実装または公開 shim を選ぶとき

## Do not read this when
- 特定サブコマンドの処理フローや内部ロジックを調査するときは、対応するサブコマンド実装へ直接進む
- 共通 runtime helper の具体的な挙動を調査するときは、`commons` 配下の担当モジュールを直接読む
- oracle 側の正本仕様・実装や、個別 adapter の詳細を確認するときは、対応する oracle 対象を直接読む
- `src` の realization 実装や互換入口と無関係な処理を調査するとき

## hash
- f3d7ec8b81013f6685899b16dea0efed406d025695a0e99934cd8446141bbf09

# `test`

## Summary
- cmoc の realization test を集約するディレクトリ。ACP builder、Codex runtime、CLI lifecycle、doctor、indexing、oracle review、session、refactor、feedback など、実装の外部契約と境界条件を pytest で検証する。個別機能のテスト入口を探す際は、対象機能に対応するファイルへ進む。

## Read this when
- cmoc の実装変更がどの realization test に影響するかを特定するとき
- CLI、Codex 実行、worktree・state・Git 操作、indexing、oracle review などの外部挙動を回帰検証するとき
- 共通テスト fixture、builder 契約、runtime の安全境界を確認するとき

## Do not read this when
- 正本仕様や実装本体の責務・詳細を確認することが目的のとき
- 対象機能が明確で、対応する個別テストまたは oracle 文書へ直接進めるとき
- テストと無関係な CLI 機能やリポジトリ文書だけを調べるとき

## hash
- 947d81c7797e1a3c5d036ddf73c1b3dc4c1f58835d8c14cc85253332ddff7568
