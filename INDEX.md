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
- 対象ディレクトリの正本仕様ツリー。自然言語の仕様文書と、Agent call の挙動を定義する実行可能な oracle source を含み、cmoc の実装・検証時に人間意図と設定の根拠を確認する入口となる。

## Read this when
- cmoc の正本仕様、Agent call の oracle source、またはその配下の対象領域への入口を確認するとき。
- 実装やテストの変更に先立ち、仕様と実行定義のどちらを確認すべきか判断するとき。

## Do not read this when
- 通常の realization 実装やテストの具体的な詳細を確認するとき。
- 対象領域が明確で、自然言語仕様または oracle source の配下に直接進めるとき。
- INDEX の生成規則やリポジトリ固有の作業手順を確認するとき。

## hash
- d5bab38e7422f643f2f51dda668deb05d7850cda87c57b7adbfe0c68df36e010

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
- cmoc の realization 実装パッケージ。Typer CLI の主入口、サブコマンド、共通 runtime、ACP/basic/config の互換 import 層を含む。
- CLI 全体の起動・登録契約を確認する場合は主入口へ、共通 runtime の責務を調べる場合は commons へ、サブコマンドの実装を調べる場合は sub_commands へ進む。ACP や互換公開面の調査では acp、basic、config、各 shim が入口になる。

## Read this when
- cmoc の CLI 全体構成、公開 import 経路、または realization 実装の主要な責務分割を確認するとき。
- トップレベル CLI からサブコマンド、共通 runtime、互換層のどこへ進むべきかを判断するとき。

## Do not read this when
- 特定サブコマンドの本体処理だけを調べるときは、該当する sub_commands 配下を直接読む。
- 共通 runtime の個別機能だけを調べるときは、commons 配下の対応する runtime module を直接読む。
- 正本仕様や canonical 実装を確認するときは、oracle 配下を直接読む。

## hash
- ff60d9489835364b8e4e372434d5e462273be33a89c518e53d96bc436df68824

# `test`

## Summary
- cmoc の realization test を集約するディレクトリ。CLI の外部挙動、runtime、Codex 実行、Git・worktree・state lifecycle、indexing、oracle review、feedback、設定、prompt、共通テスト支援を検証する。個別機能の挙動を調査する際のテスト側の入口であり、配下の対象別テストや支援モジュールへ進むために読む。

## Read this when
- cmoc の realization test の対象や、機能別の回帰・統合テストを探すとき
- CLI、runtime、Codex、indexing、oracle review、session、feedback などの外部挙動をテスト側から確認するとき
- テスト用 Git/Ollama/Codex/command helper の責務と入口を確認するとき

## Do not read this when
- 正本仕様、schema、設計意図を確認するときは、対応する oracle doc・oracle src・oracle schema を直接読む
- 実装詳細を変更・調査するときは、配下のテストではなく対応する src の実装を直接読む
- 一般的な pytest 実行方法や環境設定だけを確認するときは、テスト実行規則や開発環境文書を読む

## hash
- a9652ec793520dbed663cf3f37c8e5009bbe16738709d3f98681ba54fea65a89
