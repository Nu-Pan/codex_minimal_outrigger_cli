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
- cmoc の正本文書群を案内する入口。アプリケーション仕様、開発ルール、採用しなかった設計案の検討記録を扱い、CLI・Codex 呼び出し・prompt・Structured Output・logging・feedback・session/run・branch/worktree、および Python 実装・環境・テスト・品質検査に関する下位文書へ進む起点となる。

## Read this when
- cmoc の正本仕様または開発ルールの入口を探すとき
- CLI、Codex 呼び出し、prompt、Structured Output、logging、feedback、session/run、branch/worktree の挙動を確認・変更・レビューするとき
- Python 実装、開発環境、テスト要件、テスト実行手順の根拠を確認するとき
- 現行仕様ではなく、採用されなかった設計案の理由や検討背景を調べるとき

## Do not read this when
- 対象となる個別の仕様書、実装、テスト、または開発手順が既に特定できているとき
- 具体的な実装コードや realization test の挙動だけを調査するとき
- INDEX.md の生成規則や、対象文書に直接記載された詳細手順だけを確認するとき

## hash
- ee31066614aef28429049bea331893d42cc4443219a3ccd76e629a6ac23e2b87

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
- `src` は realization 側の実行コードと互換公開入口を束ねるディレクトリで、最上位 CLI、共通 runtime、設定・ACP 互換層、oracle package shim、各サブコマンドへ進むための全体入口である。`src` 配下の構成や、利用目的に応じた実装入口を確認するときに読む。
- 最上位 CLI の登録・起動やサブコマンド横断の入口は `main.py` と `sub_commands` へ、共通 runtime は `commons` へ、互換 import 経路は `acp`・`basic`・`config`・`cmoc_runtime`・`oracle.py` へ進むためのルーティング対象である。

## Read this when
- cmoc の realization 側にある CLI、共通 runtime、互換公開層、サブコマンドの配置を把握し、次に読む対象を選ぶとき
- 最上位 CLI から個別サブコマンド、共通 runtime、または互換 import 入口へ進む経路を確認するとき
- `src` 配下の複数領域にまたがる実装変更や調査で、対象ディレクトリ・モジュールの入口を特定するとき

## Do not read this when
- 特定のサブコマンド、runtime helper、canonical oracle 実装、または互換 shim の内部挙動が目的で、対応する下位対象を直接読めるとき
- 利用者向けの正本仕様や個別 API の詳細だけを確認するとき
- `src` 配下と無関係な oracle の仕様、テスト、または参照元だけを調査するとき

## hash
- 6e22be0994cd7ecefacc87a2e53b6fc8548f0b25edf99b875b7b8e0a4fb9b858

# `test`

## Summary
- pytest による realization test 群と、テスト実行を支える共通 fixture・helper を収録するディレクトリ。CLI、runtime、Codex 実行、indexing、oracle review、session、prompt editor などの外部挙動・状態遷移・安全境界を検証する入口であり、個別機能の回帰範囲を確認するときに下位テストへ進む。

## Read this when
- cmoc の外部挙動や回帰テストの対象範囲を機能別に把握するとき
- 実装変更に対応する realization test、共通 fixture、またはテスト用 helper の入口を探すとき

## Do not read this when
- 正本仕様や本番実装の責務・詳細を確認することが目的のときは、対応する oracle 文書や実装へ直接進む
- テスト実行手順だけを確認するときは、repository local の test execution 指示を読む

## hash
- dc7f97babe2d3f004e8be8b57cff3331e9186db0db058a69acd43963218ebb16
