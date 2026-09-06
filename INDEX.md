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
- oracle 配下の正本仕様・開発ルール・検討資料を、領域横断の入口として案内する。CLI、状態管理、branch/worktree、開発環境、設計、テスト、代替案など、目的に応じた下位文書への導線を提供する。

## Read this when
- cmoc の正本仕様や開発ルールを調べる際に、まず対象領域や適切な下位文書を特定したいとき。
- CLI、session/run、branch、Python 開発、テスト、設計判断など複数領域にまたがる参照先を確認するとき。
- 採用されなかった設計案や判断背景を確認したいとき。

## Do not read this when
- 特定の仕様本文、個別の開発ルール、実装、テスト、prompt builder、schema、サブコマンドの詳細だけを確認したいとき。
- INDEX.md の生成規則、raw observation、repository-local feedback state など、対象が明確な個別仕様を直接確認したいとき。

## hash
- 7731e8e6465875c0dffa4a3d17568d5e3395756973d528b6d5b447bbad1eafa2

# `pyproject.toml`

## Summary
- Pythonプロジェクトのパッケージ metadata、依存関係、CLIエントリーポイント、ビルド・配布設定、およびpytest・Ruff・mypyの開発ツール設定を定義する。

## Read this when
- Pythonのバージョン要件、実行時・開発時依存関係、`cmoc`コマンドのエントリーポイント、パッケージ探索や配布内容を確認するとき。
- pytest、Ruff、mypyの共通設定を確認・変更するとき。

## Do not read this when
- CLIの具体的な処理やランタイム挙動を確認するとき。
- 個別テストの内容やテスト実行手順を確認するとき。

## hash
- 3a783c008041cc5d2791af2abb3cfe1c24d8231f77689b906b36f62158c77455

# `src`

## Summary
- src 側の CLI 起動入口と互換 package shim、および処理種別・共通 runtime の実装群をまとめた realization の上位入口。
- cmoc のコマンドツリー、互換 import、builder、commons、config、sub_commands など、src 配下の実装領域へ進むためのルーティングを提供する。

## Read this when
- src 配下の realization 実装の構成を確認し、CLI 起動入口・互換層・共通 runtime・サブコマンドのどの領域から調査を始めるか判断するとき。
- cmoc の CLI コマンド登録や個別サブコマンド、acp／basic／config／oracle などの互換入口、または共通 runtime の実装入口を確認するとき。

## Do not read this when
- 個別ファイルの具体的な挙動、正本仕様、Structured Output schema、または特定サブコマンドの詳細だけを確認したい場合は、src の上位案内ではなく該当する下位実装や仕様を直接読む。
- INDEX.md の生成規則や正本側 oracle 実装そのものだけを調べる場合は、src 全体ではなく indexing 関連の実装または oracle 側の対象を直接読む。

## hash
- d5b50b19a2d1c8435b731f89f62c81558aae7ab4829bd3483221f2370099082d

# `test`

## Summary
- cmoc の CLI、runtime、Codex 実行、session/run、feedback、indexing、TUI などについて、外部から観測できる挙動と回帰条件を検証する realization test 群。
- 単体・統合・実経路のテストを通じて、状態遷移、Git・worktree、process、report、ログ、権限境界、エラー処理を確認するためのテスト入口。

## Read this when
- 公開 CLI の command tree、共通 runner、doctor、indexing、oracle、session、editing run、feedback などの外部挙動を横断して確認するとき。
- Codex exec/TUI、sandbox・provider 設定、JSONL 異常系、quota retry、process cleanup、call log の回帰条件を調べるとき。
- Git ignore、worktree、branch、session/run state、refactor state、INDEX 更新、prompt editor、MCP handoff、primary report の検証契約を確認するとき。
- 実際の Codex CLI、独立 process、PTY を使う本番経路または実経路統合試験の対象範囲を確認するとき。

## Do not read this when
- 正本仕様、Structured Output schema、実装アルゴリズム、CLI の個別仕様そのものを確認したいときは、各テストが示す oracle・schema・realization・実装対象を直接読む。
- 特定の機能に関係しない一般的なテスト実行手順や、対象テストが検証していない挙動を調べるとき。
- LLM の回答品質や推論内容そのものを評価したいとき。

## hash
- 46728ca38b5feb6f7993530dbd93dba876c855e7cce1efadf8c5628449628d61
