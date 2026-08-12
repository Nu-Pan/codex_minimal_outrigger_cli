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
- cmoc の正本文書と正確な実装定義をまとめた領域。CLI の利用時挙動、session・run・branch・worktree のライフサイクル、feedback、prompt、INDEX.md、エラー処理、不採用案、開発・テスト規約を扱う。目的に応じて仕様文書、開発ルール、不採用案の記録へ進む入口となる。
- oracle doc は cmoc の要求、判断基準、責務を自然言語で定義する正本であり、アプリケーション仕様、branch model、検討済み代替案、開発規約に分かれる。現行仕様や実装の根拠を確認するときは、該当する doc の本文へ進む。
- oracle src は agent call の prompt builder、Structured Output schema、path・config・structured document などの正確な実装定義を扱う。prompt 文面、agent call の起動条件、出力形式、パスモデルや設定モデルを確認・変更するときの入口となる。

## Read this when
- cmoc の正本仕様の所在を特定し、CLI の利用時挙動やサブコマンドの責務を確認するとき
- session、run、branch、commit、worktree の関係や lifecycle を確認するとき
- feedback の観測・状態管理・報告、prompt 構築、INDEX.md 生成、oracle と realization の境界を調査するとき
- 不採用となった作業方式や状態管理方式の理由を確認するとき
- Python 実装の配置、開発環境、コーディング規約、テスト要件、テスト実行手順を確認するとき
- agent call の prompt、Structured Output schema、パスモデル、設定モデルなどの正確な定義を確認するとき

## Do not read this when
- 目的の個別仕様、開発ルール、検討記録、または oracle src の定義が明確な場合は、その本文へ直接進むとき
- realization implementation や realization test の具体的な挙動だけを確認するとき
- 現行仕様の確認に不採用案を読む必要がないとき
- 通常の CLI 実行処理や collector の実装だけを調査するとき

## hash
- 001ebfdb6db807a844f76a5af8a1e00ec371d11ac0046fbbed958899a3b03c47

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
- cmoc CLI の実行入口と、CLI から委譲される realization 実装・共通 runtime helper・互換 import shim を集約するソースディレクトリ。
- 最上位 CLI のコマンド階層と引数解析は `main.py`、共通 runtime は `commons`、サブコマンド実装は `sub_commands`、互換 import の公開入口は `acp`・`basic`・`config`・`oracle.py`・`cmoc_runtime.py` から確認できる。
- 各サブコマンドの具体的な処理、正本仕様、個別互換 API の詳細へ進むための上位ルーティング入口となる。

## Read this when
- cmoc の CLI 全体の入口、コマンド階層、Typer/Click の引数解析とエラー変換を確認・変更するとき。
- CLI からサブコマンド実装、共通 runtime helper、realization 処理へ委譲される構成を把握するとき。
- `acp.*`、`basic.*`、`config.*`、`oracle.*`、`cmoc_runtime` の互換 import 入口を調査するとき。

## Do not read this when
- 特定サブコマンドの実行フローや業務ロジックを確認したいときは、`sub_commands` 配下の対応実装を直接読む。
- 共通 runtime の個別機能や正本仕様を確認したいときは、`commons` または対応する `oracle` 側の対象を直接読む。
- 互換入口の具体的な再公開関係や移行条件だけを確認したいときは、対応する shim または参照元へ直接進む。

## hash
- edb8645967f71e8d8ac30f331cd9a1fc8fba2b46b8db520af780c4e2b613658a

# `test`

## Summary
- `test` ディレクトリは、cmoc の realization test を集約する検証領域です。CLI、runtime、Codex 実行、indexing、oracle review、session、設定、Git、通知などの外部挙動・契約・安全性を検証し、各テストファイルが機能領域ごとの具体的な回帰検証への入口になります。

## Read this when
- cmoc の実装や仕様変更に対して、どの realization test を確認・追加・変更すべきかを判断するとき。
- CLI lifecycle、Codex runtime、indexing、oracle review、session、設定、Git、通知などの既存の外部契約や回帰条件を調査するとき。
- 対象機能に対応する個別テストの入口を特定した後、そのテストで扱う検証範囲を確認するとき。

## Do not read this when
- 正本仕様、実装責務、Structured Output schema の内容自体を確認することが目的の場合は、対応する oracle 文書・schema・src 実装を直接読む。
- 共通テスト支援や特定の機能領域を扱わない調査では、必要な個別テストまたは実装へ直接進む。
- 実際の本番経路を Codex・実推論・PTY で検証する条件だけを調べる場合は、production-path test を直接読む。

## hash
- b48f6cf841912da94f9a6e928b49c12a1e8931103fcaa052e7b82d839ba8e35a
