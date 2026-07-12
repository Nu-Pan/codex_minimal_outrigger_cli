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
- `test/_acp_builder_support.py` は、acp_builder 系テストから oracle tree 内の正本 schema へ辿るための共通 path 解決をまとめる。
- `test/_apply_support.py` は、apply セッション状態から期待する作業先 path を復元するテスト補助で、branch 表現と session state の整合を合わせたいときに使う。
- `test/_cli_support.py` は、Typer CLI テストで共通の `CliRunner` 初期化を共有する。
- `test/_codex_support.py` は、Codex 実行系テスト向けの共通補助で、認証済み `CODEX_HOME`、override argv、引数解析、権限制約の検証を扱う。
- `test/_command_support.py` は、`PATH` 上に置く偽の外部コマンドを Python の実行可能スクリプトとして作る補助をまとめる。
- `test/_git_support.py` は、git を使う CLI テスト向けの最小リポジトリ作成と git 操作の共通補助を提供する。
- `test/_ollama_support.py` は、managed Ollama を前提にしたテスト補助で、`doctor` の呼び出し方と接続前提を固定する。
- `test/test_acp_builder_apply_parameters.py` は、apply fork ACP builder の parameter 生成と正本 schema の対応を回帰確認する。
- `test/test_acp_builder_indexing_parameters.py` は、indexing 用 INDEX エントリー生成の互換ビルダーと公開面を確認する。
- `test/test_acp_builder_review_oracle_parameters.py` は、review oracle 用 parameter builder の公開面、model 設定、schema 一致、prompt 置換を確認する。
- `test/test_acp_builder_session_join_parameters.py` は、`cmoc session join` の conflict resolution 用エージェントパラメータ契約を確認する。
- `test/test_acp_builder_tui_parameters.py` は、TUI 用 `resolve_parameter` ビルダーの返却内容と正本仕様の整合を確認する。
- `test/test_apply_abandon_cli.py` は、`apply abandon` の cleanup、停止順序、警告扱い、拒否条件を CLI から検証する。
- `test/test_apply_fork_cli.py` は、`apply fork` の state 更新、worktree/branch 生成、副作用、失敗条件を CLI から検証する。
- `test/test_apply_fork_report_cli.py` は、`apply fork` の report 生成、変更要約、再調査ループ、rolling 対象選定を CLI から検証する。
- `test/test_apply_fork_target_normalization.py` は、`cmoc apply fork` の調査対象 path 正規化と除外境界を検証する。
- `test/test_apply_join_cli.py` は、`apply join` の完了条件、拒否条件、force resolve、cleanup、report 生成を CLI から検証する。
- `test/test_basic_runtime.py` は、`basic.path_model` と `cmoc_runtime` の境界契約を確認する。
- `test/test_cli_tui.py` は、`tui` 起動前後の編集、プロンプト生成、Codex 起動、ログ保存、保存先選択を検証する。
- `test/test_codex_runtime_errors.py` は、Codex 実行の起動失敗時に例外とログがどう残るかを確認する。
- `test/test_codex_runtime_exec.py` は、Codex 実行引数、override 設定、managed Ollama 前提、`CODEX_HOME` 非永続化を統合確認する。
- `test/test_codex_runtime_home.py` は、Codex 実行ラッパーの `CODEX_HOME` 解決と起動前失敗条件を確認する。
- `test/test_codex_runtime_paths.py` は、Codex 実行時の cwd、出力 schema 保存先、権限オーバーライド境界を確認する。
- `test/test_codex_runtime_quota_retry.py` は、Codex 実行の quota exceeded 後の probe、resume、再試行、停止条件を確認する。
- `test/test_codex_runtime_retry.py` は、`run_codex_exec` の再試行条件と structured output / JSONL エラー処理を確認する。
- `test/test_codex_runtime_subprocess.py` は、Codex CLI subprocess 起動補助の process group と tracking 環境変数の扱いを確認する。
- `test/test_codex_runtime_tui.py` は、`run_codex_tui` の事前チェック、引数、許可領域、ログ記録、エラー表示を確認する。
- `test/test_doctor_cli.py` は、`doctor` の git 修復、設定生成、linked worktree 切替、managed Ollama 準備、差分保持を統合確認する。
- `test/test_indexing_cli.py` は、`indexing` による `INDEX.md` 生成・再生成・衝突解決・コミット条件を検証する。
- `test/test_indexing_preflight.py` は、Codex 実行前の indexing preflight と直列化、無効化条件を検証する。
- `test/test_packaged_import.py` は、packaged 配置での import ルートと re-export 境界を確認する。
- `test/test_prompt_parts.py` は、標準 prompt parts と complete prompt の Markdown 組み立て結果を検証する。
- `test/test_review_oracle_cli.py` は、review oracle の対象選択、列挙、report 生成、失敗復旧を CLI から検証する。
- `test/test_runtime_cli.py` は、CLI の例外整形、報告出力、ログ生成、preflight、completion 副作用回避を確認する。
- `test/test_runtime_codex_conflicts.py` は、session join の conflict 解消時に Codex の追加書き込み許可がどの path を writable にするかを確認する。
- `test/test_runtime_codex_permissions.py` は、`build_codex_override_args` のアクセスモード別 permission root と `extra_writable_paths` を確認する。
- `test/test_runtime_codex_profile.py` は、FileAccessMode ごとの Codex 起動引数、権限境界、モデルプロバイダ選択を確認する。
- `test/test_runtime_config.py` は、`CmocConfig` の既定値、JSON 変換、入力検証、欠損時エラーを確認する。
- `test/test_runtime_file_access.py` は、`FileAccessMode` の永続化値、sandbox 変換、作業 root、binary 判定を確認する。
- `test/test_runtime_ollama.py` は、`commons.runtime_ollama` のサービス管理、接続確認、モデル準備を検証する。
- `test/test_runtime_state.py` は、`commons.runtime_state` の session/apply 状態 JSON と branch からの session id 抽出を検証する。
- `test/test_session_cli.py` は、`session fork/join/abandon` の CLI 挙動と state 遷移を横断して検証する。
- `test/test_struct_doc_rendering.py` は、StructDoc の Markdown renderer の空行整形互換性を確認する。

## Read this when
- 対象のテスト補助を使って、同じ path 解決や fixture 初期化を繰り返したくないとき。
- acp_builder、apply/session、Codex runtime、doctor/indexing、review oracle、prompt rendering のいずれかの CLI 挙動や回帰条件を変える前に、対応する入口を探したいとき。
- 正本仕様そのものではなく、テストが固定している外部挙動・境界条件・公開面を確認したいとき。
- linked worktree、managed Ollama、権限オーバーライド、state file、report 生成など、複数ファイルにまたがる境界を横断して確認したいとき。

## Do not read this when
- 対象機能の正本仕様本文や oracle 側の定義を確認したいだけなら、テストではなく oracle tree 側を読む。
- 実装内部の helper 分割や詳細なアルゴリズムだけを追いたいなら、CLI 回帰テストより対応する実装側を読む。
- 別サブコマンド、別 runtime、別 builder の挙動を確認したいだけなら、この階層の別エントリへ進む。
- INDEX.md のルーティング規則やファイル一覧だけを見たいなら、この本文ではなく上位の案内を読む。

## hash
- cb8daaa6f873ddd00dfcae84cc7b6bf34a94e8741da9cba43f13ef0e47d9ab7e
