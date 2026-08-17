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
- cmoc の正本文書と oracle 実装をまとめた中核領域。CLI・Codex 呼び出し・prompt・ログ・feedback・session／run の挙動仕様、Python 開発・設計・テスト・環境のルール、branch model、採用しなかった設計案を扱う。
- 仕様や開発ルールを確認するときの入口であり、挙動仕様は `doc/app_spec`、開発関連は `doc/dev_rule`、branch／session／run の関係は `doc/branch_model.md`、代替案の背景は `doc/considered_alternative`、oracle の実装は `src` 配下へ進む。

## Read this when
- cmoc の CLI、workflow、Codex 呼び出し、prompt、ログ、feedback、状態管理の正本文書を横断して調査するとき
- 実装やテストの変更に先立ち、アプリケーション仕様、開発ルール、branch model、採用しなかった設計案のどの領域を確認すべきか判断するとき
- oracle の agent call builder、prompt builder、Structured Output、path model、設定などの実装配置を探すとき

## Do not read this when
- 対象の個別仕様書や開発ルール文書が既に特定できており、対応する下位対象へ直接進む方が適切なとき
- 特定の prompt builder、agent call builder、設定モデル、スキーマ、または oracle 実装の具体的内容だけを調査するとき
- realization の CLI 実行制御やテスト実装の具体的内容だけを調査するとき

## hash
- 7afb540a24a07958f67a3d7a17b44467bafcce4dbe32b03e888a2bfec4ecd1e6

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
- src は cmoc CLI の実装入口であり、最上位 CLI、互換 import shim、共通 runtime、ACP builder adapter、サブコマンド群を提供する。
- CLI のコマンド登録と起動は main.py、共通実行基盤は commons、互換公開入口は acp・basic・config・cmoc_runtime.py・oracle.py、個別コマンドは sub_commands から確認できる。
- sub_commands 配下には doctor、feedback、indexing、oracle、realization、run、session、tui の処理入口があり、コマンド固有の実装や下位処理へのルーティング起点になる。

## Read this when
- cmoc CLI の最上位コマンド構成、起動入口、またはサブコマンド登録を確認したいとき。
- ACP builder、互換 import、共通 runtime、またはサブコマンド群の担当領域を俯瞰し、下位対象への入口を選びたいとき。
- doctor、feedback、indexing、oracle、realization、run、session、tui のいずれかの処理入口を特定したいとき。

## Do not read this when
- 特定サブコマンドの業務ロジック、runtime helper、ACP adapter、または互換 shim の内部詳細を確認したいときは、対応する下位ファイルやディレクトリを直接読む。
- canonical な oracle 実装、正本仕様、設定定義、または利用側ロジックを調査・変更するときは、src の入口ではなく対応する正本実装・仕様・参照元を直接読む。
- src 配下の CLI、互換入口、共通 runtime、ACP builder、サブコマンドに該当しない処理を調査するとき。

## hash
- 2ee8decafd95384b03fd734d8282f1d1d5aa1d52bc9e83c493ef68eac58421ba

# `test`

## Summary
- `test` は、cmoc の realization テストを集約する検証入口である。共通テストヘルパー、ACP builder、Codex runtime、CLI lifecycle、indexing、oracle review/edit、session、feedback、設定・state・Git・通知などの外部契約と境界条件を扱う。個別機能の実装変更時に、対応する回帰テストを特定するために読む。

## Read this when
- cmoc の CLI サブコマンドや runtime の外部挙動を変更・検証するとき
- ACP builder、Codex 実行、indexing、oracle review/edit、session、feedback、refactor、state、Git、通知の契約や境界条件を確認するとき
- 共通テストヘルパー、fixture、実経路統合テスト、packaged layout の検証方法を調べるとき

## Do not read this when
- 正本仕様や実装本体の詳細を確認することが目的で、対応する oracle 文書・実装を直接読む方が適切なとき
- テスト対象と無関係な機能や、一般的なテスト実行手順だけを確認するとき
- 単一の schema、prompt、設定形式、ログ形式の定義だけを確認したいとき

## hash
- 251fcc89aae41e206b9cc6ef02ffe6cde7129cb3e07db9bfcb98e991cc1d0df5
