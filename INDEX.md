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
- cmoc の人間所有の正本ファイルを収める上位ディレクトリ。正本ドキュメントと正本実装を通じて、アプリケーション仕様、設計・開発規則、ACP 呼び出しや prompt 構築、共通モデル、feedback reporter 契約を確認する入口となる。

## Read this when
- cmoc の正本仕様・設計・開発規則を調査するとき
- 正本実装の責務や、ACP・prompt・パス解決・設定・Markdown 変換・feedback 契約を調査するとき
- oracle/doc または oracle/src のどの下位領域へ進むべきか判断するとき

## Do not read this when
- 特定の仕様・設計・開発規則の詳細を確認したい場合は、oracle/doc 配下の該当文書へ直接進む
- 正本実装の詳細を確認したい場合は、oracle/src 配下の対応する下位領域へ直接進む
- realization 側の CLI 挙動や実装、テストコードを確認したい場合は、対応する realization file を直接読む

## hash
- 51026e5ee03e642dc72c2887e959ddb6ad6746f1bbf90530d6eefcceaac4d4ca

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
- cmoc の realization 実装全体をまとめる入口。CLI 起動、ACP 互換公開面、共通 runtime、設定 shim、サブコマンド実装、正本パッケージの解決 shim を扱う。
- トップレベルの CLI 構成から、ACP builder、commons、config、sub_commands などの下位実装へ進むためのルーティングを提供する。

## Read this when
- CLI 全体の実装構成、起動経路、トップレベルのコマンド公開面を確認するとき。
- ACP 互換 API、builder 実装、共通 runtime helper、設定の互換入口の所在を判断するとき。
- doctor、indexing、tui、session、run、realization、oracle、feedback などのサブコマンド実装へ進む入口を探すとき。
- `src` 起動時の `oracle.*` パッケージ解決や realization 側の互換 import 経路を確認するとき。

## Do not read this when
- 特定のサブコマンド、builder、runtime helper、互換 shim の詳細な挙動を調べるときは、対応する下位実装を直接読む。
- ACP 型、設定、CLI 挙動、サブコマンドの正本仕様や canonical 実装を確認するときは、対応する `oracle` 側を直接読む。
- `src` と無関係なテスト、補助ファイル、正本側の実装を調査するとき。

## hash
- 1cfbd9742dacafadf310cdcfce87f5f712fcd3d2da33ed23a83a2aea96e2e3f2

# `test`

## Summary
- test 配下の pytest テストと共通テストヘルパーを集約し、CLI、Codex runtime、indexing、oracle review、session/editing run、設定・状態永続化などの外部挙動と回帰契約を検証する。機能領域ごとの個別テスト、および共通 fixture・テスト支援への入口となる。

## Read this when
- テスト対象の外部挙動や回帰契約を調査するとき。
- 対象機能に対応するテストモジュールや共通テストヘルパーを選ぶとき。

## Do not read this when
- 本番実装の責務や正本仕様の内容だけを確認したいときは、対応する src または oracle 配下を直接読む。
- テスト対象と無関係な機能を調べる場合や、テスト実行手順だけを確認する場合。

## hash
- 5cde2a110cc2deecf0b2c745c049f8e8a7d187c6e25c4c4a9472ca08db29a653
