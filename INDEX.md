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
- cmoc の正本仕様ツリー。自然言語の仕様・設計・開発規則を収める doc と、Agent-call の共通設定・用途別設定・推論や権限設定・Structured Output schema を収める src から成る。個別領域へ進む前の oracle 全体の入口。

## Read this when
- cmoc の正本ファイルから、調査対象に対応する文書またはソース定義の所在を探すとき
- 仕様・設計・開発規則と Agent-call 実装定義の構成を横断的に把握するとき

## Do not read this when
- 対象の個別文書や設定領域が既に特定できており、そこへ直接進めるとき
- realization 実装・テスト、CLI／TUI の実行フロー、または具体的な個別仕様だけを調査するとき

## hash
- 451382392b7a5d3e6dcaad07f9a77cda6ff9acd697648c952b3e4c2e4d6ed4b9

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
- cmoc の realization CLI 実装を集約する `src` パッケージ。ACP 互換入口、共通 runtime、設定 shim、CLI ルート、oracle 解決 shim、サブコマンド実装などを扱う。
- CLI 全体の公開入口から個別サブコマンド、共通 runtime、互換 import 層へ進むための起点となる。

## Read this when
- cmoc の CLI 実装全体の構成や公開入口を確認するとき。
- トップレベル CLI、サブコマンド、共通 runtime、ACP・設定・oracle の互換 import 経路の担当領域を選ぶとき。

## Do not read this when
- 特定サブコマンドや runtime 機能の詳細を確認したいときは、対応する下位要素を直接読む。
- 正本仕様や oracle 側実装の内容を確認したいときは、対応する oracle 文書・ソースを直接読む。

## hash
- 5df9a308b48cd3a1bc9ae952dc4750ee8037fa008606044ecd80cec2e33a5838

# `test`

## Summary
- cmoc の realization test 群を収録するディレクトリ。CLI、runtime、Codex 実行、worktree・Git・state lifecycle、indexing、oracle review、session、feedback、各種 builder とテスト支援を、単体・統合・実経路の外部挙動として検証する。個別テストや共通 helper へ進むための入口。

## Read this when
- cmoc の実装変更に対応する回帰テスト、外部契約、状態遷移、エラー処理の検証先を探すとき。
- CLI サブコマンド、Codex runtime、indexing、oracle review、session、feedback、Git/worktree、設定・永続 state のテストを調査するとき。
- 実経路の Codex CLI・Ollama・PTY を使う受け入れ試験の対象範囲を確認するとき。

## Do not read this when
- 正本仕様、schema、prompt 規則、設計意図を確認・変更するときは、対応する oracle 文書・oracle source を直接読む。
- 実装関数の詳細だけを調査するときは、対応する src 側の実装を直接読む。
- テスト共通 helper の実装や、一般的なテスト実行手順だけを確認するときは、該当する支援モジュールまたはテスト実行規則へ進む。

## hash
- 7c89b02dcf05cae7f4ff39a8154f4aeca3b90101fdc703ae894f854b8b21ab30
