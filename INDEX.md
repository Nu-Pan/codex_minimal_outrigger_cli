# `LICENSE`

## Summary
- ソフトウェアの利用・複製・変更・配布・再許諾・販売を許可し、著作権表示と許諾表示の同梱条件、無保証および責任制限を定めるライセンス本文。

## Read this when
- 配布物に含めるべき著作権表示・許諾表示・免責条項を確認したいとき。
- 利用、改変、再配布、販売、再許諾が許される範囲を確認したいとき。
- ライセンス条件や保証・責任制限に関する質問へ答える必要があるとき。

## Do not read this when
- CLI の機能仕様、実装構造、テスト方針を調べたいとき。
- リポジトリ内の作業対象ファイルを探すためのルーティング情報が必要なとき。
- 開発手順、依存関係、コマンド実行方法を確認したいとき。

## hash
- a894f2547af0349f234986eb4661f0146f37b7d82f8b22a27a674d5c1236f08f

# `README.md`

## Summary
- cmoc の概要、初期セットアップ手順、基本ワークフローの参照先、ターミナル操作上の注意を案内する入口文書。
- 開発を始める前に、cmoc が何を補助するツールか、環境をどう用意するか、利用手順をどこから読むかを把握するための導入情報を扱う。

## Read this when
- cmoc の目的や略称を最初に確認したいとき。
- clone 後の Python 仮想環境作成や editable install など、初期セットアップ手順を確認したいとき。
- 基本ワークフローの詳しい仕様を読むための入口を探しているとき。
- ターミナルで Ctrl+S による停止を避けるための設定例を確認したいとき。

## Do not read this when
- 実装やテストの詳細、内部構造、仕様断片そのものを確認したいとき。
- コマンドの具体的な利用仕様や基本ワークフロー本文を確認したいとき。
- リポジトリ内での agent 向け作業規則や編集規則を確認したいとき。

## hash
- c6c3f3c5798ecc63f8611a40982f7bc8100116d8a934616bbd2b2a5b5e0a1afc

# `bin`

## Summary
- cmoc 起動用の薄いシェルラッパーを扱うディレクトリ。リポジトリルート基準で仮想環境 Python を探し、通常起動や補完プローブを Python 実装へ委譲する入口を担う。
- 仮想環境 Python が存在しない、または実行できない場合の利用者向け Markdown エラー、セットアップ手順、簡易 call stack の表示挙動を扱う。

## Read this when
- cmoc コマンド起動時に、どの Python 実装へ委譲されるかを確認したいとき。
- 仮想環境 Python がない場合、または実行不能な場合の起動失敗挙動を確認・変更したいとき。
- シェル補完プローブ時に通常起動と異なる分岐を取る理由や、補完時の失敗コードを確認したいとき。
- 起動前に利用者へ表示されるエラー文面、セットアップ手順、表示用パス、call stack 行番号の組み立てを確認・変更したいとき。

## Do not read this when
- Python 側の CLI サブコマンド、引数解析、業務ロジック、実行後の出力内容を調べたいとき。
- 仮想環境の作成方法そのものやパッケージ設定を変更したいとき。
- oracle file や path model の正本仕様を確認したいとき。

## hash
- bcc444f615624a979df5ebba33008d88c68e9f32a99b58386f9f0158f7e98b02

# `codex_minimal_outrigger_cli.code-workspace`

## Summary
- VS Code workspace configuration for this repository, defining the workspace root, editor exclusions, Python formatting/interpreter settings, analysis search paths, and Markdown indentation behavior.

## Read this when
- Configuring or troubleshooting VS Code behavior for this workspace, including hidden files, Python formatter selection, virtualenv interpreter path, analysis include paths, or Markdown editor indentation.
- Checking how the editor is expected to discover both implementation code and oracle source during Python analysis.

## Do not read this when
- Investigating cmoc runtime behavior, CLI command semantics, tests, or oracle specifications; read the relevant source, test, or oracle document instead.
- Looking for repository routing guidance; use the appropriate directory routing document rather than editor workspace settings.

## hash
- 1938307f70f255710d75d39c07d860ecb381acbb031ca19b2f2b6e565ac41acb

# `oracle`

## Summary
- `oracle` は cmoc の正本仕様断片を集める最上位の入口で、まずこの配下に人間が責任を持つ仕様を置き、実装やテストの前に読むべき領域を切り分けるときに使う。
- 配下の `doc` は実行仕様の横断把握、`src` は builder 系などの正本仕様断片の確認に進む入口で、どちらを読むべきかを先に判断するための案内役になる。

## Read this when
- cmoc の正本仕様断片をどの配下から読むべきか判断したいとき。
- oracle 側の仕様を起点に、実装へ進む前の読む範囲を絞りたいとき。
- 配下の `doc` と `src` のどちらを先に読むべきか迷うときの入口として使うとき。

## Do not read this when
- すでに読むべき下位領域が分かっているなら、この入口を経由せず直接その配下を読む。
- oracle と realization の役割分担や編集規則だけを確認したいとき。
- この配下以外の仕様や実装を調べたいとき。

## hash
- 2b279bab62fb859f5577120fce645f80fe2cd1bb02b932e9210997ece7afd976

# `pyproject.toml`

## Summary
- Python パッケージとしての cmoc のプロジェクトメタデータ、実行コマンド、依存関係、ビルド設定、setuptools の探索範囲、pytest の import path を定義する設定ファイル。
- CLI エントリーポイントは `cmoc` コマンドから実装の `main` 関数へ接続され、実装コードと oracle src の両方をパッケージ探索・テスト import の対象にする。

## Read this when
- Python バージョン要件、配布パッケージ名、依存パッケージ、ビルド backend など、プロジェクト全体の packaging 設定を確認・変更したいとき。
- `cmoc` コマンドがどのモジュール関数へ接続されるかを確認・変更したいとき。
- setuptools がどのディレクトリからモジュールやパッケージを収集するか、また JSON などの package data が含まれるかを確認したいとき。
- pytest 実行時の import path を確認し、実装コードや oracle src の import 解決に関する問題を調べたいとき。

## Do not read this when
- 個別サブコマンドの処理内容、CLI 入出力仕様、実行時ワークフローの実装詳細を調べたいとき。
- テストケース自体の期待値や fixture の内容を確認したいとき。
- oracle file の正本仕様断片の本文を確認したいとき。
- リポジトリ内の各ディレクトリやファイルへ進むためのルーティング情報を探しているとき。

## hash
- d01948ab1730e2747d529d49d8c8ca10b84bd6a86e19d7b2810ee87c95ccb904

# `src`

## Summary
- `src` 配下の realization 実装の起点を束ねる上位領域。CLI 入口、共通 runtime、`acp`/`basic`/`config` の公開面、サブコマンド群、正本側 `oracle` への接続を読む前に、どの実体へ進むかを切り分けるための入口として使う。
- 個別機能の実処理は持たず、互換 shim と実装本体の境界、CLI から各 subcommand への配線、共有 helper の配置先を確認したいときに読む。

## Read this when
- `src` 全体の役割分担と、目的の実装がどの下位領域にあるかを判断したいとき。
- CLI 入口、共通 runtime、互換 import 面、サブコマンド群、正本側 `oracle` への接続のどれを読むべきか先に絞りたいとき。
- 新しい実装や変更先を探す前に、公開面と実体の境界を確認したいとき。

## Do not read this when
- 個別コマンドの処理内容、path/setting/ACP の具体仕様、レビューや apply の実行ロジックを知りたいときは、対応する下位モジュールや正本側文書を直接読む。
- 互換入口の有無だけを確認済みで、詳細な配線や委譲先の説明が不要なとき。
- 正本仕様そのものを確認したいときは、`oracle` 側の対応文書や実装へ進む。

## hash
- 09d6fd548732ede590f6dbc02c54e337876e21980fe0ab1855853dcaf63bb2c5

# `test`

## Summary
- `_acp_builder_support.py` は、acp_builder 関連テストが `<work-root>/oracle/src/oracle/acp_builder` 配下の正本 schema を共通の path 解決で参照するための補助で、schema 参照先をテストごとに重複させたくないときの入口である。
- `_apply_support.py` は、apply セッション状態から管理対象の作業先パスを復元するテスト補助で、状態スナップショットに含まれる branch 表現を直接解釈して期待パスを組み立てる用途に向く。
- `_cli_support.py` は、Typer CLI テストで共通の `CliRunner` 初期化をまとめる補助で、CLI 実行の入出力や終了コードを検証するテストの共通入口である。
- `_codex_support.py` は、Codex 実行系テスト向けの共通補助群で、認証済み `CODEX_HOME`、override argv、`--config` 解析、権限制約の検証補助をまとめる。
- `_command_support.py` は、`test` 配下で PATH 上に置く偽外部コマンドを Python の実行可能スクリプトとして生成する共通補助で、UTF-8 書き出しと実行権限付与を扱う。
- `_git_support.py` は、`git` を使う CLI テスト向けの最小リポジトリ作成ヘルパーで、初期化、現在ブランチ確認、追跡済みだが ignored な oracle file の用意を支える。
- `_ollama_support.py` は、Ollama 関連テストで本番共有の managed service を前提に `doctor` を呼ぶ流れを支える共通補助で、サービス前提と固定エンドポイントを扱う。
- `test_acp_builder_*` 群は、apply / indexing / review oracle / session join / tui の各 ACP builder が返す parameter、公開面、schema 参照、prompt 置換やモデル設定を正本仕様に沿って保つ回帰テストである。
- `test_apply_*` 群は、`apply fork` / `apply join` / `apply abandon` の CLI 挙動、状態遷移、worktree・branch・report・cleanup・境界条件を確認する回帰テストである。
- `test_basic_runtime.py`、`test_runtime_*`、`test_codex_runtime_*` は、path model、file access、config、state、subprocess、retry、quota、TUI、Ollama、preflight などの runtime 契約と Codex 実行境界を固定する回帰テストである。
- `test_cli_tui.py`、`test_doctor_cli.py`、`test_indexing_cli.py`、`test_runtime_cli.py` は、各 CLI の前処理、副作用、report、preflight、linked worktree や git 状態に対する外部挙動を確認する統合テストである。
- `test_review_oracle_*`、`test_session_cli.py`、`test_struct_doc_rendering.py` は、review oracle の対象選定・反復・レポート、session fork/join/abandon の状態遷移、StructDoc の Markdown rendering をそれぞれ検証する入口である。

## Read this when
- acp_builder 関連テストで、正本 schema の参照先を一箇所に集約したい。
- apply セッション状態から作業先パスを導く仕様や、branch 名の妥当性と選択先の対応を合わせたい。
- Typer CLI テストで同じ `CliRunner` 初期化を繰り返したくない。
- Codex 実行ラッパーの argv、`CODEX_HOME`、権限、`--config` 解析、実行系テスト補助を確認したい。
- 外部コマンドを差し替えるテストで、実行可能な stub を共通の方法で作りたい。
- git 初期化、初期コミット済み repo fixture、ignored oracle file の扱いを共通化したい。
- Ollama を本番共有の managed service 前提で起動するテスト補助が必要だ。
- apply / indexing / review oracle / session join / tui の parameter、schema、prompt、公開面の回帰を確認したい。
- `apply fork` / `apply join` / `apply abandon` の外部挙動、cleanup、状態遷移、境界条件を確認したい。
- path model、file access、config、state、subprocess、retry、quota、TUI、Ollama、preflight の runtime 契約を確認したい。
- 各 CLI の前処理、linked worktree、report、preflight、副作用を外部挙動ベースで確認したい。
- review oracle の対象選定、反復、レポート、session CLI の state 遷移、StructDoc の Markdown rendering を確認したい。

## Do not read this when
- oracle schema 本文や structured output の正本仕様そのものを確認したい。
- 通常の作業先探索や実運用の path 解決、apply 以外の状態変換を追いたい。
- CLI 実装本体、`CliRunner` 以外の汎用 fixture、またはコマンド定義そのものを確認したい。
- Codex 以外の一般的なテスト共通処理や、実装側の権限判定ロジックだけを追いたい。
- fake command ではなく、CLI runner や永続的な補助ファイルの設計を探している。
- git 操作そのものの実装や、個別 CLI 挙動だけを追いたい。
- fake Ollama サービスや `doctor` 以外の起動経路を探したい。
- 別サブコマンドの parameter、別領域の schema、または oracle 側の本文そのものを読みたい。
- session fork / apply fork / apply join などの内部実装分割や、他サブコマンドの挙動だけを見たい。
- runtime 実装の細部や oracle 本文だけを確認したい場合は、対応する実装側または正本仕様を読む。
- 個別サブコマンドの業務ロジックや Markdown report の文言ではなく、CLI 全体の他の層を見たい。
- review oracle の prompt 文面、session fork の生成ロジック、あるいは Oracle 本文そのものを確認したい。

## hash
- ed63085354ab55efd8db86fded6d0de8d06322d7571037ccf2fadb45f3a4e392
