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
- cmoc の人間所有の正本仕様を集約するディレクトリ。アプリケーション共通仕様、branch・commit・worktree モデル、開発規則、不採用案の検討記録、および参照可能な正本ソースを扱う。仕様領域ごとの文書・ソースへ進むための入口。

## Read this when
- cmoc の正本仕様や正本ソースを探すとき
- アプリケーション挙動、branch・worktree lifecycle、開発規則、テスト・環境構築、設定・パスモデル、規範モデル、構造化文書生成の仕様を確認するとき
- 特定の仕様領域に対応する下位ディレクトリを選ぶとき

## Do not read this when
- 確認対象の具体的な仕様文書や正本ソースがすでに特定されているとき
- realization 実装、具体的なテスト実行、一般的な開発作業だけを調査するとき

## hash
- e908e48f3d2933a9d3a3ec6655628c93423376d399fe6ab681f97692ae241f56

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
- cmoc CLI の realization 実装を集約する src パッケージ。CLI エントリーポイント、サブコマンド、共通 runtime、設定・互換 import 層、oracle 側パッケージへの接続を提供する。
- main.py と sub_commands が利用者向け CLI の登録・委譲・実行入口を担い、commons が横断的な runtime 基盤を担う。acp、basic、config、cmoc_runtime、oracle は既存 import 経路や正本側実装との互換接続を提供する。

## Read this when
- cmoc CLI の全体構成、主要エントリーポイント、サブコマンドへの入口を確認するとき。
- CLI、共通 runtime、設定、Git・状態管理、INDEX 更新などの realization 実装の配置を特定するとき。
- 既存の acp.*、basic.*、config.*、cmoc_runtime、oracle.* import の互換層や移行経路を確認するとき。

## Do not read this when
- 特定サブコマンドの処理詳細を確認したいときは、sub_commands 配下の該当実装を直接読む。
- 特定の runtime helper や設定型の詳細を確認したいときは、commons または対応する定義元を直接読む。
- oracle 側の canonical 実装、正本仕様、テストの内容を確認したいときは、src ではなく oracle 配下の対応対象を直接読む。

## hash
- d80fbe81cdf4ed78d65c038a040d667b03b189da66e9e0895a4f79d104ea4d21

# `test`

## Summary
- test 配下の realization test と共有テストヘルパーを、機能領域ごとの外部挙動・実行契約・安全性検証への入口として整理する。ACP builder、Codex runtime、CLI lifecycle、indexing、oracle review、session/run state、設定、Git、StructDoc などの回帰・統合・受け入れテストを扱う。

## Read this when
- CLI、runtime、Codex 実行、TUI、indexing、oracle review、session/run、設定、Git、prompt、builder、または StructDoc の外部挙動や回帰テストを調査・変更するとき。
- 対象機能の realization test がどこにあり、共有 helper や case-local Ollama をどう使うかを確認するとき。
- 実経路統合テストや全末端サブコマンドの受け入れテストを実行・変更するとき。

## Do not read this when
- 正本仕様、schema、prompt 標準、実装詳細そのものを確認することが目的のときは、対応する oracle file や realization implementation を直接読む。
- 一般的なテスト実行手順だけを確認するときは、対応するテスト実行規則を読む。
- 対象機能と無関係なテスト領域や、共有 helper を使わない局所的な実装を調査するとき。

## hash
- 4e9c2d8479a4304dc4bed33fa07b0cee276be5e7a79f76ca9a8ee74293fe2018
