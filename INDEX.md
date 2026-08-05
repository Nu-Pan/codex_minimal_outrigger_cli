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
- cmoc の人間所有の正本仕様を格納するディレクトリ。機能仕様、開発・設計規則、正本実装、agent call 用の prompt や Structured Output schema などを扱う。下位の doc では自然言語の仕様・規則、src では正本実装を確認できる。

## Read this when
- cmoc の機能仕様、開発規則、設計判断を調査・変更・検証するとき
- agent call のパラメータ、prompt、Structured Output schema、oracle の正本実装を確認するとき
- 正本仕様または正本実装の下位入口を選ぶ必要があるとき

## Do not read this when
- 実際の CLI 実装、差分適用、競合解消、git 操作など realization 側の処理を調査するとき
- 確認対象の仕様文書または正本実装の場所が既に分かっているときは、下位の doc または src を直接読む
- INDEX.md の自動生成規則や oracle・realization の一般原則だけを確認するときは、それぞれの専用仕様を直接読む

## hash
- 1aec4df1dcfcda0f9d4e3993e85091f83ff694025cad33e3bd82e6c56916d6fa

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
- cmoc の realization 実装をまとめる src ディレクトリ。CLI の主要入口、サブコマンド、共通 runtime、互換 import shim を扱い、実行経路や公開 import の移行状況を確認するための入口となる。

## Read this when
- cmoc CLI の登録・引数解析・サブコマンド委譲を調査または変更するとき。
- CLI サブコマンド、共通 runtime、互換 import 層の構成や担当箇所を切り分けるとき。
- `oracle.*` や各種公開 import path の realization 側における解決経路を確認するとき。

## Do not read this when
- 特定サブコマンドの詳細な実行フローや状態遷移を確認するときは、サブコマンド実装を直接読む。
- 共通 runtime の個別機能や正本仕様を確認するときは、対応する commons 実装または oracle 文書を直接読む。
- 利用者向け仕様や realization 以外のテストだけを調査するとき。

## hash
- 85d7a0370e44dc2e3358294aeb13061a33582cde428067a0bdea0926573e06b9

# `test`

## Summary
- realization test を集約するディレクトリ。CLI、runtime、worktree・Git・state lifecycle、Codex/Ollama 実行経路、builder・prompt・schema、oracle review/edit、indexing、設定・補助機能など、実装の外部挙動と統合契約を検証する。個別機能の回帰テストや共有テストヘルパーへ進む入口となる。

## Read this when
- 実装変更がどの realization test や共有 fixture に影響するか確認するとき。
- CLI、runtime、Codex 実行、indexing、oracle review/edit、session/run lifecycle、設定、builder の外部契約を検証または変更するとき。
- テスト用 Git repository、fake command、case-local Ollama、Codex 環境などの共有支援機能を利用・変更するとき。

## Do not read this when
- 正本仕様、schema、prompt 規範、CLI 契約そのものを確認・変更するときは、対応する oracle file を直接読む。
- 単一の実装詳細を確認するだけなら、対応する src の realization implementation を直接読む。
- テスト実行全体の選択・品質検査手順だけを確認するときは、test execution の正本仕様を読む。

## hash
- 88e43a9345770eef1163aca195f2e18876d0a430cd9c9d03201b62c02c339bd1
