# `AGENTS.md`

## Summary
- cmoc 自己開発時に、仕様文・agent への指示文・現在の agent への指示文を区別するための注意事項と、agent 向け指示文を単独で理解可能かつ仕様定義を含まない形に保つための基準。

## Read this when
- cmoc 自身のリポジトリを cmoc で開発しており、同じ文面が異なる情報レイヤーに現れる場合の解釈を確認するとき。
- cmoc が呼び出す agent への指示文を作成・確認し、仕様への暗黙の依存や仕様定義の混入を避けるとき。

## Do not read this when
- cmoc の仕様そのものを調べる必要があるとき。
- 具体的な実装、設定、CLI 挙動を確認する必要があり、レイヤー区別や agent 向け指示文の独立性が関係しないとき。

## hash
- da4f29cd7f635f81ead991302bf0b25e687760e47096c1c5efe20318b8c9a8f2

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
- 人間が所有する正本仕様を、文書による意味仕様と、明示委譲された構築・アルゴリズム・schema の oracle src に分けて保持する領域。cmoc の開発規約、アプリケーション仕様、サブコマンド仕様、prompt 構築定義などを含み、realization の根拠を確認する入口となる。

## Read this when
- cmoc の要求、責務、判断基準、goal・non-goal などの意味仕様を確認するとき
- prompt の正確な文面、構築順序、選択値、schema、アルゴリズムの正本を確認するとき
- 実装やテストが従うべき正本仕様を特定するとき
- oracle file と realization file の責務や優先関係を確認するとき

## Do not read this when
- 対象の具体的な実装挙動だけを確認する場合は、対応する realization の src を直接読むとき
- 既に確認対象の oracle doc または oracle src が特定できている場合は、このディレクトリ全体を読む必要がないとき
- 生成済み prompt や INDEX の routing 情報だけを確認する場合は、生成物または対象の INDEX を直接読むとき

## hash
- e26235b9e2c5748cfa4de439e70c694a079ae0a491e010795a0e52469a8ebd9b

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
- cmoc の realization 実装全体を収めるディレクトリ。CLI 起動と Typer/Click 境界、設定・型モデル、共通 runtime、サブコマンドの業務処理、Codex agent 呼び出し用 ACP builder を提供する。
- `main.py` は `doctor`、`tui`、`session`、`oracle`、`realization`、`run`、`feedback`、`indexing` の CLI ツリーを構成し、引数解析エラーを cmoc のエラー表示へ変換する入口である。
- `commons/` は設定、パス、Git、Codex subprocess、process tracking、feedback、run lifecycle、レポート、editor handoff、INDEX 更新など、複数サブコマンドで共有する runtime 責務の入口である。
- `sub_commands/` は CLI サブコマンドごとの orchestration を担い、session・oracle・realization・run・feedback・doctor・tui・indexing の実行処理へ進むときに読む。
- `acp/` は Codex agent に渡す編集・調査・feedback・indexing・realization 用の agent call parameter builder を提供する。
- `basic/` と `config/` は oracle 側で定義された公開型・path model・構造化文書描画・cmoc 設定を realization 側から利用するための公開面と変換処理を提供する。
- `cmoc_runtime.py` は既存利用者向けの互換 import path として共通 runtime の公開名を再輸出し、`oracle.py` は oracle 実装の公開面を提供する。

## Read this when
- cmoc の CLI コマンド構成、実行 lifecycle、共有 runtime、agent 呼び出し境界を横断的に把握したいとき。
- 新しいサブコマンドや runtime 共通処理の配置先を判断するとき。
- INDEX 更新、feedback 報告、run/session 管理、Codex subprocess 実行の入口を探すとき。

## Do not read this when
- 特定コマンドの詳細仕様を確認したい場合は、該当する `sub_commands/` のファイルを直接読む。
- Codex agent parameter の具体的な schema や prompt 構築だけを確認したい場合は、該当する `acp/builder/` を直接読む。
- 設定値の読み書きだけを確認したい場合は `config/` または `commons/runtime_config.py` を直接読む。
- 正本仕様や oracle 実装そのものを確認したい場合は `src` ではなく `oracle/` 配下を読む。

## hash
- 291f4ab49f6ab4c5a48499f025695b4dfb9b87310dbcdb4dc4c186f22f6794b0

# `test`

## Summary
- 実装・CLI・Codex 実行・セッション状態・設定・ファイル分類など、cmoc の正本仕様に対する回帰テストを集約するディレクトリ。
- CLI の外部挙動、runtime の状態遷移や Git worktree、Codex の sandbox・provider・JSONL 処理、prompt と structured output、builder の互換公開面を、隔離用 fixture と共有 helper を使って検証する。
- 仕様ごとの単体テストだけでなく、CLI 起動からログ・エラー・preflight・session 操作までの統合的な契約も扱うため、実装変更の影響範囲と検証方法を確認する入口になる。

## Read this when
- 実装変更が既存の正本仕様、CLI 外部契約、Codex 呼び出し、session/run state、Git ignore/worktree、設定永続化に影響する可能性があるとき。
- 回帰テストの fixture、fake command、Codex home 隔離、Windows toast 隔離、または共有 assertion helper の構成を確認したいとき。
- 複数モジュールをまたぐ CLI lifecycle や session lifecycle の期待動作を、実行可能な検証として確認したいとき。

## Do not read this when
- 正本仕様そのものの意味や要求を確認することが目的のときは、対応する oracle/doc または oracle/src を直接読む。
- 単一の実装関数の現在の処理を確認するだけなら、対応する src の実装を直接読む。
- テストの追加・変更を伴わない一般的な実行方法や、特定のテストケースの詳細だけを調べる場合は、該当する test ファイルまたは共有 helper に直接進む。

## hash
- d35585c836a7be994ab3c01215c34208161d1be42dcd617720bd4339536765d5
