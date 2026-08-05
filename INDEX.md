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
- `src` は cmoc CLI の realization 実装をまとめる入口で、Typer による主要 CLI、サブコマンド、共通 runtime、互換 import shim、設定・ACP 関連の公開経路を扱う。CLI の登録と委譲は主要エントリーポイント、個別コマンドの処理はサブコマンド群、横断的な実行時機能は共通 runtime、互換性の確認は各 shim へ進む。

## Read this when
- cmoc の realization 側 CLI 実装全体の構成や、主要な入口から各サブコマンド・共通 runtime へ進む先を判断するとき。
- CLI の公開入口、サブコマンド、共通 runtime、互換 import 層の責務を切り分けるとき。

## Do not read this when
- 特定サブコマンドの実行フローや処理内容だけを確認したいときは、対応するサブコマンド実装を直接読む。
- 共通 runtime の単一機能、設定・ACP などの正本定義、または互換 shim の詳細だけを確認したいときは、対応する下位モジュールや oracle 側を直接読む。
- 利用者向け仕様や realization 以外の正本を確認するとき。

## hash
- 437ad27db4feb1286ef4fd33ca1360856111371e4d29c2aacddb2c6ef57c299e

# `test`

## Summary
- 各種 pytest による realization test と、テスト間で共有する実行・Git・Codex・Ollama・fake command 用ヘルパーを集約する。CLI、runtime、indexing、oracle review、session、editing run、設定、packaging などの外部挙動・統合契約を確認する入口であり、個別テストや補助モジュールへ進むためのディレクトリ。

## Read this when
- 実装変更に対応する回帰テストや統合テストの所在を探すとき。
- CLI、runtime、Codex 実行、indexing、oracle review、session、editing run、設定、packaging などの外部契約をテスト観点から確認するとき。
- テスト用の Git、Codex、Ollama、fake command、schema path、doctor 実行ヘルパーを確認するとき。

## Do not read this when
- 正本仕様、Structured Output schema、prompt 規範、設定契約そのものを確認するときは、対応する oracle 文書・schema・source を直接読む。
- 実装の内部詳細だけを調査するときは、対応する src の realization implementation を直接読む。
- テスト実行全体の選択・品質検査手順だけを確認するときは、test execution の正本仕様を読む。
- 対象機能と無関係なテストや共有ヘルパーを総当たりで読む必要があるとき。

## hash
- 944bf59492607d62cde7904a419e1045108dd035d49ef8e4cf2ef4d1120ecc25
