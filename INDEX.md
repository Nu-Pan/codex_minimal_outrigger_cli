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
- cmoc の CLI 起動用シェルラッパー。仮想環境 Python の存在・実行可能性を確認し、通常起動では不足時の標準エラー報告後に `src/main.py` を実行する。補完プローブ時は Python が利用可能な場合のみ転送する。CLI の起動経路、Python 検証、起動失敗時のエラー形式、補完時の挙動を確認・変更するときの入口。

## Read this when
- cmoc コマンドの起動処理や、仮想環境 Python の検証・エラー報告を調査するとき
- シェルラッパーから `src/main.py` への転送条件や、自動補完プローブ時の分岐を変更・確認するとき

## Do not read this when
- CLI の実際の引数処理やアプリケーション動作を調査するときは、直接 `src/main.py` または対応する仕様を読む
- エラー内容の正本仕様や初回セットアップ手順を確認するときは、参照されているエラー処理・開発環境の文書を直接読む

## hash
- 70422bb34b7732bfa99d94d395b5c91f9aba3302293f0edba8366c10e7645dfe

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
- cmoc の正本文書を収める領域。アプリケーション挙動、session／run の branch 分離モデル、不採用案、開発環境・設計・テストのルールを扱い、仕様・設計・実装判断の確認先を提供する。
- 具体的な仕様や開発規則を確認するための入口であり、実装側では agent call の prompt、routing、oracle・realization、feedback、session join、TUI などの責務へ案内する。

## Read this when
- cmoc の機能仕様、状態遷移、branch・worktree 分離モデルを確認するとき。
- 設計上の不採用案や、実装・開発環境・テストに関する正本ルールを確認するとき。
- 具体的な個別仕様や開発規則へ進む前に、読むべき正本文書の領域を判断するとき。

## Do not read this when
- 実装コードやテストコードの具体的な挙動を確認する場合は、対応する realization file やテストを直接読むとき。
- 個別仕様、開発環境、テスト要件など読む対象文書が特定できているとき。
- INDEX.md の生成・更新規則だけを確認するとき。

## hash
- 7faf82cdf740ab1812092f2f2599e9e47ca50e72f243cf1ac7f558781250bcb4

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
- cmoc の実装側ソースツリー。CLI の起動入口、共通 runtime、互換 import shim、設定公開面、ACP adapter、各サブコマンド実装をまとめ、個別処理の実装へ進む入口を提供する。

## Read this when
- cmoc の CLI 起動経路、サブコマンド配置、共通 runtime、互換 import、または処理領域別の実装入口を特定するとき。
- 対象機能の実装場所が不明で、`main.py`、`commons`、`acp`、`basic`、`config`、`sub_commands` などの下位対象へ振り分ける必要があるとき。

## Do not read this when
- 特定機能の内部挙動、正本仕様、設定型、または oracle 側の実装だけを確認したいときは、対応する下位実装・oracle・仕様定義元を直接読む。
- 個別サブコマンドの処理内容が明確な場合や、`src` 配下と無関係な repository 文書・テストだけを調査するとき。

## hash
- e493350333f20b1e9efc800789377ab1aef121a84606e337cff8e6f5c7264db0

# `test`

## Summary
- test 配下の回帰・統合テストを、CLI、runtime、Codex、Git/worktree、INDEX、report、feedback、builder など機能別の検証入口として案内する。各テストは実装変更時に確認すべき外部契約や境界条件を示す。

## Read this when
- 変更・調査対象に対応する外部挙動や回帰条件を検証するテストの入口を探すとき
- CLI lifecycle、Codex 実行、session/run、oracle review、realization、indexing、feedback、通知、設定、Git/worktree、prompt/builder の契約をテストから確認するとき
- 単体テスト、統合テスト、実経路受け入れテストのどの範囲で検証されているかを把握するとき

## Do not read this when
- 正本仕様や実装の意味・アルゴリズムを確認することが目的のときは、対応する oracle 文書または実装を直接読む
- テスト対象と無関係な機能を調べるとき
- 一般的な pytest 実行手順や Python 環境の規約だけを確認するとき

## hash
- 30ec8207b1ff36b8257bed96a3d15af9929b9ab4d6e00c9f421e96a1d1eb6ec2
