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
- 人間が所有し、cmoc の正本仕様断片を集約する領域です。oracle doc・src・test を含み、realization file が従うべき意図、制約、実装・テスト仕様の入口として機能します。

## Read this when
- cmoc の現行仕様、設計規則、実装責務、テスト要件を確認するとき
- realization file の挙動や配置が正本仕様に適合しているか調査するとき
- oracle doc・src・test のどの領域を読むべきか選ぶとき

## Do not read this when
- 対象の oracle file がすでに特定できており、その本文へ直接進めるとき
- realization 側の具体的な実装やテストだけを確認するとき
- 正本仕様を根拠にしない補助ファイルや作業メモを扱うとき

## hash
- ab75fc39c5ef0506473b708353a42f8f205fccea5b7a7aa9d37e195912a909f6

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
- cmoc の実装ツリー。Typer CLI の主要入口、サブコマンド、共通 runtime helper、互換 import shim、ACP builder 群を扱い、CLI から各機能実装へ進むための入口となる。
- ACP・basic・config は canonical 実装や型を再公開する互換層、commons は CLI 実行・Codex・設定・状態・Git・logging・run lifecycle などの共通処理、sub_commands は doctor・indexing・oracle・realization・run・session・TUI の実行入口を担う。

## Read this when
- cmoc の CLI コマンド登録、Typer/Click の引数解析、エラー変換、自動補完、サブコマンドへの委譲を調査・変更するとき
- 共通 runtime の担当領域や、CLI・Codex・設定・状態・Git・logging・run lifecycle の実装入口を特定するとき
- 既存の acp、basic、config、cmoc_runtime、oracle 関連の互換 import 経路を維持・移行するとき
- ACP builder、用途別 adapter、prompt 処理、TUI、quota probe の実装入口を確認するとき

## Do not read this when
- canonical な oracle 実装や正本仕様を確認・変更したいときは、oracle 側の対応対象を直接読む
- 特定サブコマンド、runtime 機能、builder、prompt、TUI の詳細処理を確認したいときは、該当する下位要素を直接読む
- CLI と無関係な個別機能や、互換層ではない利用箇所の公開面を調査するときは、参照元または担当モジュールを直接読む

## hash
- f6a883693b5551fa2d077a956f3c06b13eb290e3c87075e2d07e02dadf11e098

# `test`

## Summary
- cmoc の realization test を集約するディレクトリ。ACP builder、Codex runtime、CLI、indexing、oracle review、session、設定・状態永続化、Git/worktree lifecycle など、実装の外部挙動と回帰条件を検証する。各テストファイルが個別機能の確認入口となる。

## Read this when
- 実装変更に対応する既存の回帰テストや、対象機能の外部契約を確認するとき。
- CLI、Codex 実行経路、indexing、oracle review、session、worktree、設定、状態管理などのテスト対象を探すとき。
- realization implementation が正本仕様に適合しているか、既存テストの検証範囲を確認するとき。

## Do not read this when
- 正本仕様、schema、設計意図そのものを確認するときは、対応する oracle 文書・source・schema を直接読む。
- テスト対象ではない実装の詳細や、一般的なテスト実行方法だけを調べるとき。
- 特定機能の実装を変更する作業で、対応する src や oracle file を直接確認すべきとき。

## hash
- 143a466e63d36ec03263e175375b80b56ca672c145177cbf1ba2f7aa649c3c62
