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
- oracle は cmoc の正本仕様と開発規則をまとめた上位文書群で、アプリケーション挙動・branch／worktree 分離・不採用案・Python 実装／環境／テストの各領域への入口を提供する。
- CLI、session／run、Codex 呼び出し、ログ、feedback、通知などの個別仕様と、実装・開発環境・テストの規則を対応する下位文書へ案内する。
- branch・commit・worktree による隔離モデルや、採用しなかった設計・作業方式の判断理由を確認するための入口でもある。

## Read this when
- cmoc の正本仕様全体から、挙動・設計判断・開発規則に対応する下位文書の所在や境界を探すとき。
- CLI、session／run、Codex、feedback、ログ、通知、INDEX、branch／worktree 分離など複数領域にまたがる仕様を調べるとき。
- Python 実装規約、開発環境、テスト規則や実行手順を確認するとき。
- 現行方針ではなく、不採用となった設計案や作業方式の理由を調べるとき。

## Do not read this when
- 特定の機能やサブコマンドの詳細挙動だけを確認したいときは、対応する app_spec 配下の個別仕様を直接読む。
- branch model の具体的な操作契約だけを確認したいときは、branch model の本文を直接読む。
- Python の実装・環境・テストに関する具体的な規則だけを確認したいときは、対応する dev_rule 配下の文書を直接読む。
- 採用済み機能の仕様や realization の具体的な実装・テスト内容を調べるときは、該当する正本仕様または realization／test を直接読む。

## hash
- 68fd195b54c2751fa1cf2d87011ff5333cb905dbc29bdf5523d3a4c683fe0f2a

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
- `src` は cmoc の realization 側コードを収める実行・互換公開ツリーであり、CLI 起動入口、共通 runtime、互換 import path、サブコマンド実装への上位入口を提供する。
- CLI の起動とコマンドツリーは `main.py`、互換 import の公開面は `acp`・`basic`・`config`・`cmoc_runtime.py`・`oracle.py`、共有実行基盤は `commons`、個別コマンドの実装は `sub_commands` へ進む。

## Read this when
- cmoc の realization 側で、CLI の起動経路、互換 import、共通 runtime、サブコマンド実装の配置を横断して確認するとき
- 対象の責務から、`main.py`、互換パッケージ、`commons`、`sub_commands` のどこを読むべきか判断するとき
- src 起動時の oracle パッケージ解決や、既存公開 import path から正本実装へ移行する構成を確認するとき

## Do not read this when
- 特定サブコマンドの業務ロジック、共通 runtime helper、互換 API、正本仕様の詳細を確認するときは、`sub_commands`、`commons`、各互換対象、または oracle 側の対応実装を直接読む
- CLI の個別挙動や引数解析の詳細だけを調べるときは、`main.py` または対応するサブコマンド実装を直接読む
- src 配下と無関係な正本仕様、テスト固有の期待値、下位 protocol・schema の内容だけを確認するとき

## hash
- c139277eef938a3a623ae9ac9ad4b2aab76ad18778d6aacfe2015c869b821389

# `test`

## Summary
- cmoc の realization テスト群と共通テスト支援を集約する入口。CLI の各サブコマンド、Codex runtime、session/run state、Git・path・indexing・report・通知などの外部契約や回帰条件を、対象機能別のテストから確認できる。
- 共通 helper は、schema path 解決、doctor・Codex・Git・外部コマンド・PTY 実行、toast 隔離など、複数テストで共有する検証環境と呼び出し境界を提供する。
- 個別テストは、単体の runtime 挙動から実 Codex・独立 process・PTY を用いる本番経路統合まで、対象機能の検証範囲に応じた入口として機能する。

## Read this when
- cmoc の特定機能に対する外部挙動、回帰条件、エラー・中断・cleanup・永続状態の検証方法を調べるとき。
- CLI、Codex exec/TUI、indexing、session、editing run、oracle、feedback、prompt editor、Git/path、report、通知のテスト対象を探すとき。
- 複数テストで使う fixture や helper を利用・変更し、テスト用環境の固定条件や外部 process の扱いを確認するとき。
- 実際の Codex CLI、独立 process、PTY を使う受け入れ経路の検証方法を確認するとき。

## Do not read this when
- 正本仕様、schema、実装本体、または個別機能の具体的なアルゴリズムを確認することが目的で、対応する oracle・src・実装対象を直接読むべきとき。
- テスト対象の外部契約に関係せず、一般的な pytest 実行方法や無関係な機能の調査だけを行うとき。
- schema の内容自体、Codex CLI の一般利用方法、通知や Git の本番仕様だけを確認したいとき。

## hash
- e492a0a52b068f5082b8f9be10015abacdbbdaa5c193699133a5c40b14b9f718
