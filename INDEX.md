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
- cmoc の正本文書と、それを実現する oracle 側の構築定義を集約する領域。アプリケーション仕様、branch・commit・worktree の運用、採用しなかった設計案、Python 開発・テスト規則、および agent call・prompt・feedback・path・Structured Output の定義を扱う下位領域への入口となる。
- CLI の挙動や状態管理は app_spec、Git 運用は branch_model、採用しなかった設計判断は considered_alternative、開発方法は dev_rule、agent call 構築や prompt の実装は src/oracle 配下へ進むための上位ルーティング対象である。

## Read this when
- cmoc の正本文書を探し、CLI 挙動・session/run・feedback・indexing などの仕様領域を絞り込むとき
- branch・commit・worktree の運用規則や、採用しなかった設計案の背景を確認するとき
- Python のコーディング、設計、開発環境、テスト規則・実行手順を確認するとき
- agent call の builder、prompt policy、path model、Structured Output、feedback reporter の構築定義を調査・変更するとき

## Do not read this when
- 対象となる下位 oracle 文書または個別の src/oracle 実装が明確で、その対象だけを直接確認すれば足りるとき
- 具体的な CLI 実装、個別テスト、realization の正本仕様や実装だけを調べるとき
- collector 側の feedback 保存・集約処理だけを調査するとき

## hash
- 55f2a7d93d1e83ba337934354760a4aeb17626e5c172175b88b6ec132dad4ed7

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
- cmoc の realization test を集約する検証ディレクトリ。CLI の lifecycle、Codex runtime、indexing、oracle review、session・editing run、config・state・Git 境界、builder 契約など、実装の外部挙動と回帰条件を機能領域別のテストから確認する入口となる。
- 共通 fixture と helper は pytest 環境、fake external command、Git repository、Codex 実行、CLI 実行、schema path 解決を支援する。実経路統合テスト用の subprocess 起動フックも含む。
- 配下の個別テストは、対象機能の統合 lifecycle を扱う CLI テスト、runtime・builder・prompt・state などの契約テスト、oracle review・indexing・feedback などの領域別テストに分かれている。

## Read this when
- cmoc の実装変更が、CLI の外部挙動、Codex 呼び出し、Git・worktree・永続 state、indexing、oracle review、session、editing run、feedback、builder 契約のいずれかへ影響する可能性があるとき。
- 変更対象に対応する realization test の入口を特定し、回帰条件や境界ケースを確認するとき。
- pytest の共通 fixture、テスト用 Git repository、fake command、Codex double、または実経路 subprocess 環境を確認するとき。

## Do not read this when
- 本番実装の責務や正本仕様そのものを確認するときは、対応する実装ファイルまたは oracle 文書を直接読む。
- INDEX.md の生成規則や routing 内容そのものを確認するときは、indexing の正本仕様または実装を直接読む。
- 単一の低レベル helper や個別テストの詳細だけを確認する場合は、対応するファイルへ直接進む。

## hash
- 2380c9f38fa6f7bdf757c4e5681996202ec47ff7104581c53f2abf309c33b236
