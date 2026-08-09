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
- cmoc の正本領域で、アプリケーション仕様・開発規則・不採用案の記録を集約する。個別の正本ドキュメントや oracle 側のエージェント呼び出し構築実装へ進むための入口。

## Read this when
- cmoc の正本ドキュメントや oracle 側の agent call 構築実装の所在を確認するとき
- 複数の仕様領域または用途別 builder にまたがる調査対象を特定するとき
- 個別仕様や実装を読む前に、適切な下位領域への入口を判断するとき

## Do not read this when
- 確認対象の個別仕様文書がすでに特定できているとき
- 実際のサブコマンド実行フローや agent call 起動処理を調べるとき
- 個別の schema、基盤モデル、realization 実装、feedback 保存処理の詳細だけを確認するとき

## hash
- d6e770acf938fd75bde9c3c56580a3ee495362f5c55c7dd82a0f3139e78b00c9

# `pyproject.toml`

## Summary
- Python プロジェクトのパッケージメタデータ、実行コマンド、依存関係、ビルド設定、および pytest・Ruff・mypy の開発ツール設定を定義する。Python パッケージ構成、依存関係、CLI エントリーポイント、または開発時の品質検査設定を確認する際の入口となる。

## Read this when
- 依存パッケージや開発用依存パッケージを追加・変更するとき
- cmoc CLI のインストール後に使われる実行エントリーポイントを確認するとき
- Python のビルド・パッケージ探索設定を変更または調査するとき
- pytest、Ruff、mypy のプロジェクト共通設定を確認するとき

## Do not read this when
- 個別の CLI 挙動や内部実装を確認する場合は、src 配下の実装を直接読むとき
- テストケースの具体的な内容やテスト固有の規則を確認する場合
- 正本仕様や開発環境の運用手順を確認する場合は、対応する oracle 文書を読むとき

## hash
- d7e54a5345610218deb1baa5ef4ecf56af5f7bd5cd71249f76a9bbaa99f1bbf1

# `src`

## Summary
- cmoc の realization 側 CLI と互換公開入口をまとめる src パッケージ。トップレベル CLI、サブコマンド、共通 runtime helper、各種 import shim を扱い、具体的なサブコマンドや共通処理へ進むための入口となる。

## Read this when
- cmoc の realization 側 CLI 全体の構成や公開 import 経路を確認するとき。
- トップレベル command、サブコマンド、共通 runtime、設定・状態・Git・feedback などの実装領域を選ぶとき。
- ACP/basic/config/oracle などの互換入口と、下位実装への進み方を確認するとき。

## Do not read this when
- 特定サブコマンドの内部処理や共通 helper の具体的な挙動を調べるときは、該当する下位実装を直接読む。
- 正本仕様、oracle 側実装、テスト内容を確認するときは、それぞれの oracle または test を直接読む。
- 単一の互換 shim の公開名や import 挙動だけを確認するときは、対象モジュールを直接読む。

## hash
- bea5ca054e9f6660bd496b4c1c8cf010b33b57126988d84f2fbb374408f1d876

# `test`

## Summary
- cmoc の realization test を収録するテストディレクトリ。ACP builder、Codex runtime、CLI lifecycle、indexing、oracle review/edit、session、feedback、設定・状態永続化など、実装の外部挙動と正本仕様への適合を pytest で検証する。個別テストは各機能領域の回帰検証への入口となる。

## Read this when
- cmoc の機能変更に伴う realization test の対象範囲や、関連する外部挙動の回帰検証を確認するとき
- 対象機能が CLI、Codex 実行、indexing、oracle review、session、feedback、設定、状態管理など複数の実装領域にまたがり、該当する個別テストを選ぶ必要があるとき
- テスト共通 fixture や fake subprocess、Git worktree、Codex 実行環境などの共通テスト基盤を確認するとき

## Do not read this when
- 正本仕様、schema、prompt 規則、または個別実装の詳細を確認するときは、対応する oracle file や src 実装を直接読む
- 対象機能が明確な場合は、このディレクトリ全体ではなく該当する機能領域の個別テストへ直接進む
- テスト実行手順や品質検査の選択だけを確認するときは、repository local の test_execution の案内を読む

## hash
- 12e938a99effc7e040e822c4e74b5f0fa62489ecb825c9fc19c8a2639d3f25c0
