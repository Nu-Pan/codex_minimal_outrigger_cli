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
- oracle 配下の正本ドキュメントと正本実装を束ねる最上位の入口。cmoc の人間管理の仕様・開発規則と、agent call 用 prompt builder などの正本コード領域へ振り分ける。

## Read this when
- cmoc の正本仕様または正本実装を探し始めるとき
- アプリケーション仕様、開発ルール、agent call・prompt builder の正本を特定するとき

## Do not read this when
- 読むべき個別の文書または実装領域がすでに特定されているとき
- INDEX.md のルーティング情報だけを確認するとき

## hash
- f9de8c87e016532d2558ec4989ab9bda28a1c520ab6c9f113bc3f116436de75a

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
- cmoc の realization 側 Python ソースツリー。Typer CLI のルート、各サブコマンド、共通 runtime helper、設定・互換 import shim、ACP builder adapter を含む。
- CLI の公開入口と command tree はトップレベル実装、個別コマンドの処理はサブコマンド配下、横断的な実行・状態・Git・feedback・INDEX 処理は commons 配下へ進む。
- acp、basic、config、oracle shim は既存 import 経路や正本側実装への接続を担う互換層で、ACP builder の用途別 adapter は acp 配下に整理されている。

## Read this when
- cmoc の CLI 全体の入口、サブコマンド構成、または realization 側の主要な実装領域を確認するとき。
- 共通 runtime と個別 CLI サブコマンドの責務境界を判断するとき。
- ACP builder adapter、互換 import 経路、設定公開面の下位要素へ進む入口を選ぶとき。

## Do not read this when
- 特定のサブコマンド、runtime helper、builder adapter の詳細実装だけを確認したいときは、該当する下位要素を直接読む。
- 正本仕様や canonical な型・処理の定義を確認したいときは、対応する oracle 側を直接読む。
- テストの挙動や検証条件だけを確認したいときは、test 配下の対象を読む。

## hash
- bf6905e26d028a39a06214fbfe595ba84b43e0048ecbebe07d7e15b274d66b2a

# `test`

## Summary
- pytest による realization test 群を収録するディレクトリ。CLI、Codex runtime、ACP builder、indexing、oracle review、session/run state、Git/path/config、通知など、cmoc の外部挙動と永続化契約を検証する統合・回帰テスト、および共通 fixture・テスト支援モジュールを扱う。各機能の実装変更時に、対応する挙動のテスト入口として下位ファイルへ進む。

## Read this when
- cmoc の特定機能について、実装変更に伴う外部挙動・回帰条件・統合 lifecycle の検証対象を探すとき。
- CLI、Codex 実行、ACP builder、indexing、oracle review、session/run、Git/path、config、通知のテスト入口を選ぶとき。
- 複数テストで共有される fixture、fake command、Git repository、Codex/Ollama 支援の責務を確認するとき。

## Do not read this when
- 正本仕様、schema、prompt 規則、設計意図を確認することが目的の場合は、対応する oracle doc・oracle src・oracle schema を直接読む。
- 本番実装の詳細だけを調査する場合は、対応する src ファイルを直接読む。
- 一般的な pytest 実行方法だけを確認する場合は、repository local のテスト実行ルールを読む。

## hash
- 44ec4a6b442ed5eb83ef5be77cb1b45fffa121b56e1464fb2e1ca770b28cca14
