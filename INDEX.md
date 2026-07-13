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
- `src` 配下の realization implementation への入口。CLI 本体、共通 runtime、設定、`acp`/`basic` の再公開層、`oracle` 参照、各 `sub_commands` への分岐をたどるために読む。
- ここでは実処理の詳細を追わず、どの責務がどの下位 module にあるかを切り分ける。互換 import 面と実体実装の境界を確認したいときの起点になる。

## Read this when
- `src` 全体の責務分担を把握して、目的に合う下位 module を選びたいとき。
- CLI 入口、共通 runtime、設定、`acp`/`basic` 互換層、`oracle` package shim、各サブコマンド実装のどこへ進むべきか判断したいとき。
- 互換 import 面を残すべきか、実体実装側へ進むべきかの境界を確認したいとき。

## Do not read this when
- 個別処理の仕様、入出力、失敗時挙動を知りたいとき。そうした詳細は `commons`、`sub_commands`、`acp`、`basic`、`config`、`main.py`、`oracle.py` 側を直接読む。
- 新しい機能や公開 API を追加する場所を探しているとき。ここは全体のルーティング入口であり、追加先の候補を絞る場所ではない。
- 実装そのものではなく人間向けの正本仕様を確認したいとき。仕様は oracle 側の文書や src 配下の正本実装に分かれている。

## hash
- c8395450797afabb45ed2f2e9c838a37cebcc10df6e8a27f9f962b7dcc34f226

# `test`

## Summary
- `_acp_builder_support.py` は、`test` 側で `acp_builder` の正本 schema へ直接つなぐための共通 path helper を置く補助対象。正本 schema をコピーせずに参照経路だけを整えたいテストから入る。
- `_apply_support.py` は、`apply` セッション状態から管理対象の作業先パスを復元する補助対象。状態スナップショットの branch 表現と、それに基づく作業先選択をテスト側で合わせたいときに読む。
- `_cli_support.py` は、Typer CLI テストで共通の `CliRunner` 初期化をまとめる補助対象。CLI 実行の入出力や終了コードを同じ runner で検証したいときに読む。
- `_codex_support.py` は、Codex 実行系テストで使う最小限の共通補助をまとめる対象。偽の結果オブジェクト、`CODEX_HOME` 初期化、引数抽出、権限制御、Ollama 前処理差し替えを共通化したいときに読む。
- `_command_support.py` は、`PATH` 上に置く偽の外部コマンドを現在の Python で起動する実行可能スタブとして作る補助対象。外部コマンド差し替えテストで、同じ作り方を使い回したいときに読む。
- `_git_support.py` は、`git` を使う CLI テスト用の最小リポジトリを作る共通ヘルパー対象。初期化、現在ブランチ確認、追跡済みだが ignore される oracle file の用意を共通化したいときに読む。
- `_ollama_support.py` は、`doctor` CLI テストから指定 worktree を cwd にして実行する補助対象。cmoc managed Ollama を本番共有のまま使う前提で `doctor` を呼びたいときに読む。
- `test_acp_builder_apply_parameters.py` は、`acp.builder.apply.fork` 系の parameter 生成と prompt・schema 参照・root 取り扱い・拒否条件を検証するテスト群。apply fork の builder が正本 schema と標準文面をどう組み立てるかを確認したいときに読む。
- `test_acp_builder_indexing_parameters.py` は、`acp.builder.indexing.index_entry` の互換ビルダーが indexing 用の実行条件を最小権限・低負荷に固定して返すことを確かめるテスト。公開面が互換ビルダーだけに絞られているかも確認したいときに読む。
- `test_acp_builder_review_oracle_parameters.py` は、review oracle ACP builder の公開面と structured output schema を検証するテスト群。互換ラッパーの export 範囲、モデル設定、schema 一致、prompt 置換を確認したいときに読む。
- `test_acp_builder_session_join_parameters.py` は、`acp.builder.session.join.conflict_resolution` の公開面と conflict resolution 用パラメータ契約を検証するテスト。ビルダ以外を export しないことや、権限・推論強度の固定を確認したいときに読む。
- `test_acp_builder_tui_parameters.py` は、TUI 用の `resolve_parameter` ビルダーと返却値の正本仕様対応を確認するテスト群。元プロンプト、モデル系パラメータ、公開モジュール名、schema 整合をまとめて確認したいときに読む。
- `test_apply_abandon_cli.py` は、`apply abandon` の外部挙動を CLI 経由で検証するテスト群。cleanup、警告扱い、稼働中 process の停止、worktree/branch/state 整合、破損 state や stale branch の拒否を確認したいときに読む。
- `test_apply_fork_cli.py` は、`apply fork` の CLI 回帰テスト群。セッション作成後の apply 実行、state/worktree/branch 更新、設定欠落や config 読み込み失敗、`.gitignore` と `.cmoc/local` の扱いを確認したいときに読む。
- `test_apply_fork_report_cli.py` は、`apply fork` の report 生成、収束判定、再検査、rolling 実行、state 更新を確認するテスト群。report 文面、終了コード、再調査条件、変更要約の扱いを確認したいときに読む。
- `test_apply_fork_target_normalization.py` は、`sub_commands.apply.fork` の対象正規化ロジックを回帰検証するテスト群。`oracle` 配下、管理領域、tracked ignored file、symlink などの除外・扱いを確認したいときに読む。
- `test_apply_join_cli.py` は、`apply join` の CLI 挙動を検証するテスト群。成功条件と拒否条件、cleanup と state/report 更新、dirty worktree、stale branch、merge conflict、force 解消をまとめて追いたいときに読む。
- `test_basic_runtime.py` は、`basic.path_model` と `cmoc_runtime` の実行時契約を確認する回帰テスト群。token から実 path への復元、repo root と run/work root の分離、run worktree の受け入れ条件を見たいときに読む。
- `test_cli_tui.py` は、`cmoc tui` の外部挙動を検証するテスト群。エディタ入力、解決済みパラメータ、TUI 起動、保存先、linked worktree 対応、`.cmoc` の ignore を確認したいときに読む。
- `test_codex_runtime_errors.py` は、Codex 実行時の異常系を確認するテスト群。JSONL の不正イベント分類と、Codex CLI 不在時の例外内容や失敗記録を扱う。
- `test_codex_runtime_exec.py` は、Codex CLI 実行時の `run_codex_exec` と override 生成を検証する統合テスト群。実 CLI 呼び出し、Ollama 連携、`CODEX_HOME` への永続設定非作成、権限制御付き実行を確認したいときに読む。
- `test_codex_runtime_home.py` は、`run_codex_exec` の `CODEX_HOME` 解決と preflight validation を扱う回帰テスト群。未設定時の既定値、相対パス解決、`auth.json` 確認、起動前に失敗する条件を押さえたいときに読む。
- `test_codex_runtime_paths.py` は、`run_codex_exec` の cwd 解決、出力 schema 保存先、権限 override 境界を検証する統合テスト群。起動先ディレクトリや許可パス、並列実行時の衝突回避を確認したいときに読む。
- `test_codex_runtime_quota_retry.py` は、quota 枯渇後に probe を一度だけ挟んで resume/retry へ進む制御を確認するテスト群。quota 待機中のログ、resume token 復元、probe 失敗、並行待機の集約を追いたいときに読む。
- `test_codex_runtime_retry.py` は、`run_codex_exec` の再試行判定と失敗時ログを確認するテスト。Structured Output 検証失敗、capacity retry、JSONL error、KeyboardInterrupt、中断後差分保持を外部挙動として押さえたいときに読む。
- `test_codex_runtime_subprocess.py` は、`commons.runtime_codex_profile` の subprocess 実行と tracking 振る舞いを確認するテスト群。process group 記録、`communicate()` 中断時の tracking 維持、継承環境変数の無視を扱う。
- `test_codex_runtime_tui.py` は、`codex_runtime_tui` の呼び出し規約とログ挙動を検証するテスト群。TUI 起動前の権限制約、完成済み prompt、call log、`KeyboardInterrupt` や非 0 終了の記録を確認したいときに読む。
- `test_doctor_cli.py` は、`doctor preprocess` の共有 lifecycle を CLI 経由と直接呼び出しの両方から確認する統合テスト群。`.cmoc/local`、`.agents`、config、managed Ollama、Git index の修復と保持を一続きで見たいときに読む。
- `test_indexing_cli.py` は、`cmoc indexing` の CLI 挙動を検証するテスト群。事前条件確認、doctor 実行、worktree 対象選択、INDEX.md 更新、Codex 呼び出し、commit 条件を外部挙動として扱う。
- `test_indexing_common.py` は、`commons.indexing` の INDEX entry 生成と更新を確認する直接テスト群。入力検証、空/不正 entry、空ディレクトリ、並列更新、memo 配下と symlink cycle の除外を扱う。
- `test_indexing_preflight.py` は、Codex 実行前の indexing preflight が走る条件、順序、worktree 選択、ロック待機、再実行抑止を検証するテスト群。`commons.runtime_codex_preflight` と `commons.indexing` の呼び出し契約を確認したいときに読む。
- `test_packaged_import.py` は、packaged layout での import 境界と公開面を検証するテスト群。`oracle` 配下の正本定義が配布物側で再公開されるか、余計な公開が混入しないかを確認したいときに読む。
- `test_prompt_parts.py` は、標準 prompt parts と complete prompt の Markdown 組み立て結果を検証する realization test。標準文書の主要語句、file access rule、root placeholder、注入制御を確認したいときに読む。
- `test_review_oracle_loop.py` は、`cmoc review oracle` の所見列挙・マージ・検証の周回制御を確認するテスト群。Codex 呼び出しの受け渡し条件、merge operation の適用条件、再試行失敗条件を読む入口にする。
- `test_review_oracle_report.py` は、`cmoc review oracle` のレポート生成と CLI 挙動を検証する統合テスト群。出力順、集計件数、`--scope` 反映、処理失敗時の error report、`eval-oracle` からの委譲を扱う。
- `test_review_oracle_targets.py` は、`review oracle` の対象抽出と `finding` からの oracle path 解決の境界を検証するテスト群。`session` と `full` の対象選定、ignore される追跡済み oracle file、`AGENTS.md` / `INDEX.md` 除外、symlink 分類を確認したいときに読む。
- `test_review_oracle_worktree.py` は、`cmoc review oracle` の worktree 選択と INDEX 統合の振る舞いを確認する統合テスト群。linked worktree での実行、review 用 worktree の分離、INDEX 変更の取り込み、競合時方針、他差分混入時の拒否を扱う。
- `test_runtime_cli.py` は、CLI 実行時の境界を検証するテスト群。エラー整形、work root 判定、preflight と completion の副作用有無、サブコマンドログ生成条件を確認したいときに読む。
- `test_runtime_codex_conflicts.py` は、セッション参加の conflict 解決で、Codex の追加書き込み許可がどのパスに付与されるかを検証するテスト群。書き込み許可ルート解決、予約済みパス拒否、`CmocError` 条件を変えるときに読む。
- `test_runtime_codex_permissions.py` は、`build_codex_override_args` の書き込み許可境界を確認するテスト。読み取り専用モード、`extra_writable_paths` の受理条件、保護対象パス、各 permission mode の差を追いたいときに読む。
- `test_runtime_codex_profile.py` は、`build_codex_override_args` の `FileAccessMode` ごとの sandbox 生成、`CmocConfig` による model/provider 切り替え、linked worktree での追加 read 許可を検証するテスト群。
- `test_runtime_config.py` は、`CmocConfig` と設定入出力の仕様を検証するテスト群。既定値、JSON 変換、読み込み失敗時の案内、型・値検証、復元用数値の保持を確認したいときに読む。
- `test_runtime_content.py` は、`commons.runtime_content.is_binary` の判定が通常のテキストと NUL 文字を含む内容で分かれることを検証するテスト。バイナリ判定境界を確認したいときに読む。
- `test_runtime_file_access.py` は、FileAccessMode の永続化値と Codex sandbox への変換の対応関係を固定するテスト群。モードの追加・改名・値変更、sandbox 変換の見直しをするならここを読む。
- `test_runtime_ollama.py` は、`commons.runtime_ollama` のサービス管理・接続確認・モデル準備の挙動を検証するテスト群。Ollama の再起動条件、systemd ユーザーサービス生成、疎通確認、モデルロード確認が中心。
- `test_runtime_state.py` は、`session` / `apply` の状態ファイル形状と branch 名から session id を取り出す境界条件を確認するテスト群。破損した branch 名や不正な state/payload 値を拒否する挙動、`session_fork_lock` の排他を扱う。
- `test_session_cli.py` は、`cmoc session fork` / `join` / `abandon` の CLI 外部挙動を横断して確認するテスト群。session branch の作成・完了・破棄、linked worktree での branch/state、dirty worktree や precondition 失敗時の拒否をまとめて扱う。
- `test_struct_doc_rendering.py` は、StructDoc の Markdown renderer が通常テキストとコードブロック内の連続空行をどう畳むかを検証する単体テスト。整形互換性と空行圧縮境界を確認したいときに読む。

## Read this when
- 対象 helper の挙動や共通テスト基盤を変えたいときは、その helper に対応する `test_*` から読む。
- CLI や runtime の外部挙動を変えるときは、該当サブコマンド名や runtime 名が入ったテスト群から読む。
- 正本 schema や oracle 仕様そのものを確認したいときは、`oracle/src` または `oracle/doc` 側を読む。
- packaged layout での import 契約や公開面を確認したいときは、`test_packaged_import.py` を読む。
- prompt 文面、file access rule、root placeholder の保持を確認したいときは、`test_prompt_parts.py` を読む。

## Do not read this when
- 個別の実装本文だけを確認したいときは、対応する `src` 側を読む。
- 正本仕様の内容そのものを読みたいときは、対応する `oracle` 側を読む。
- 別サブコマンドや別 runtime の挙動だけを追いたいときは、該当する別テストへ進む。
- INDEX.md のルーティング方針そのものを確認したいときは、この配下の test ではなく上位の案内を読む。

## hash
- 3ce238029ac5770070fd3b5310a989a27301148b6aea0dd3c43e5334537aa2f3
