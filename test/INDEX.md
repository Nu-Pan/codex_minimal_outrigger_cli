# `_acp_builder_support.py`

## Summary
- 対象ファイルは、テストコードから正本 schema を参照するための path 生成 helper を提供する。`acp_builder` 配下の schema 相対 path を受け取り、リポジトリ内の oracle schema の位置を返す。

## Read this when
- `acp_builder` の schema 参照方法や、テストで正本 schema の path を解決する仕組みを確認・変更するとき。

## Do not read this when
- schema の内容自体を確認・変更するときは、oracle 側の schema ファイルを直接読む。
- `acp_builder` と無関係なテスト補助や、実装本体の path 解決を確認するとき。

## hash
- 6fd184bad0b16e6bce9c32dac57e2187a8272303ece3f3c8d350acaeacf5824b

# `_cli_support.py`

## Summary
- `test/_cli_support.py` は、Typer CLI の `doctor` サブコマンドをテストから実行するための共有ヘルパーを提供する。対象 worktree をカレントディレクトリとして実行し、終了成功を検証する `run_doctor` と、端末出力から primary report のパスを抽出する `terminal_primary_report` が入口になる。

## Read this when
- `doctor` CLI のテストで、対象 worktree の cwd を保った実行や共有 runner の利用方法を確認するとき
- doctor 実行結果またはキャプチャ済み端末出力から primary report のパスを取得する必要があるとき

## Do not read this when
- doctor CLI 本体の仕様や前処理の詳細を確認したいときは、コメントに示された app_spec 文書を直接読む
- ログ出力の一般仕様を確認したいだけのときは、console_and_file_log の仕様を直接読む
- doctor 以外の CLI サブコマンドのテスト支援を調べるとき

## hash
- 77fc1a0c23afa228b0235135b24525d1823f6332923c8ea7c430c89dc6871020

# `_codex_support.py`

## Summary
- Codex 実行ラッパーのテストで使う共通ヘルパーを提供する。
- 一時的な Codex 環境、最小の結果 double、AgentCallParameter、CLI 引数の検査、Codex override の stub を扱う。

## Read this when
- Codex 実行ラッパーのテストで、認証に依存しない一時環境や固定された CLI override を準備するとき。
- AgentCallParameter の最小値、Codex 結果の検証対象、または `--config` を含む CLI 引数をテスト用に解析するとき。

## Do not read this when
- Codex 実行ラッパーのテスト支援を必要とせず、対象機能の実装や別のテスト fixture を直接確認するとき。
- Codex CLI の実運用設定や本番の認証環境を確認するとき。

## hash
- 1e5c23abd029819daf4c209ad023bd8ba2f6dc15a2284dd47b6b863c2e296c74

# `_command_support.py`

## Summary
- テスト用の fake external command として実行可能な Python スクリプトを書き込むヘルパー。UTF-8 で内容を保存し、実行権限を付与する。

## Read this when
- テストで外部コマンドの代替スクリプトを作成・実行する処理を確認するとき
- テスト用スクリプトの書き込み時のエンコーディングや実行権限を確認するとき

## Do not read this when
- 本番コードの外部コマンド実行処理を確認するとき
- テスト用スクリプト生成を伴わないテストを読むとき

## hash
- 37672f2473fdf889a2210635d4294e5f807fefd04034b00449f411bffcf86ae8

# `_git_support.py`

## Summary
- テスト用 Git リポジトリを初期化する共通ヘルパーと、現在のブランチ名を取得する関数を提供する。Git のユーザー設定・署名・フック・ignore 設定をテスト環境向けに固定し、最小のコミット済みリポジトリや、ignore 対象だが追跡済みの oracle ファイルを作成するテストの入口となる。

## Read this when
- cmoc CLI の Git 状態やリポジトリ初期化を検証するテストを追加・変更するとき。
- テスト用リポジトリの作成条件や Git の環境依存設定を確認するとき。

## Do not read this when
- Git テスト用リポジトリを使わないテストを扱うとき。
- 個別の CLI 実装や oracle 仕様の詳細を確認したいとき。

## hash
- 1ecaade4dee17221fe4bca8c1837bef8e9d28957fd6bee025a6b52c299aea9e1

# `_real_path_integration`

## Summary
- 実際の Codex CLI と独立 process を使い、全末端サブコマンドの本番経路と TUI 経路を検証する実経路統合テストの入口です。
- CLI の終了結果に加えて、report・state・Git・call log などの外部から観測できる制御結果を確認します。

## Read this when
- 実際の Codex 推論を含む CLI の受け入れ試験を実行・変更・調査するとき。
- 実行可能な全末端サブコマンドの登録漏れや、本番 process・PTY・外部状態の検証方法を確認するとき。

## Do not read this when
- Codex 推論を使わない通常の単体テストやモックベースの CLI テストだけを扱うとき。
- 実装のパス解決ロジック自体を調査するときは、対応する src または oracle の仕様・実装を直接読むとき。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `conftest.py`

## Summary
- pytest 実行時に Windows toast 通知の外部副作用を隔離する共通 fixture。pytest プロセスと子プロセスの双方で fake transport を使わせ、利用者の通知履歴へ実際の toast を残さないためのテスト環境入口。

## Read this when
- pytest の共通 fixture、テスト実行時の Windows toast 通知隔離、または subprocess から呼ばれる toast transport の挙動を確認するとき。

## Do not read this when
- Windows toast の本番実装や通知仕様そのものを調べるときは、toast 実装または正本仕様を直接読む。
- 個別テストの検証ロジックや fixture 以外のテスト共通設定を調べるとき。

## hash
- b3f3b49e68d53aabe2132800ffc6a1c690c6a2188dd64826fa72ead0f29fe6c4

# `test_acp_builder_editing_run_parameters.py`

## Summary
- editing run workload 向けの apply/refactor builder adapter を、正本 builder の再公開、commit 参照を含む apply prompt、canonical Structured Output schema と実行設定の利用という観点から検証するテスト。

## Read this when
- editing run の apply/fork launch_exec または refactor/fork change_summary・file_review_and_fix builder の互換性、prompt 内容、worktree・commit 範囲、Structured Output schema、file access mode、preflight 設定を確認・変更するとき。

## Do not read this when
- builder 本体の一般的な実装詳細や oracle の正本内容を直接調べることが目的のとき。apply/refactor builder の挙動検証ではなく、別 workload や別の builder adapter を扱うとき。

## hash
- 9811a6d8c31daae31e7187ca1374ce39dd66748b6e25b9e2f230cce0ab6a9d6e

# `test_acp_builder_indexing_parameters.py`

## Summary
- indexing index entry builder の parameter 構築と、readonly・cwd・preflight・prompt 内容の契約を検証するテスト。
- INDEX.md エントリー生成用 Structured Output schema の semantic 配列が空でないことを検証するテスト。
- 対象本文に三連 backtick が含まれる場合でも prompt の本文境界を保護し、oracle builder と同一結果になることを検証するテスト。
- index entry 互換 module が builder のみを公開する互換公開面を検証するテスト。

## Read this when
- indexing index entry builder の parameter 設定、prompt 構成、対象本文の fence 保護を確認したいとき。
- INDEX.md エントリー生成 schema の必須配列制約を確認したいとき。
- index entry 互換 module の公開シンボル制約を確認したいとき。

## Do not read this when
- indexing index entry builder の正本実装や schema 定義そのものを変更・確認したいときは、対応する oracle の正本を直接読む。
- INDEX.md エントリー生成以外の builder の parameter や公開面を確認したいとき。

## hash
- fe42771668749a837a24254c023413543d38b4aa68f0a34469fcac96a0e3ffb4

# `test_acp_builder_session_join_parameters.py`

## Summary
- session join の conflict resolution builder に関する互換モジュールの公開範囲、repo write 権限、prompt 構造、conflict path の code fence 保護を検証するテスト。

## Read this when
- session join の conflict resolution 用パラメータ生成、公開 API、ファイルアクセス権限、prompt の契約を変更・確認するとき。
- conflict 対象ファイルの path を prompt に埋め込む際、三連 backtick を含む path の扱いを確認するとき。

## Do not read this when
- conflict resolution builder 本体の実装詳細を変更・調査する場合は、対応する正本実装を直接読むとき。
- session join の conflict resolution 以外の builder や、一般的なテスト実行方法だけを確認するとき。

## hash
- 8c6d839daf58bd270e88c069f8a33cc01c3034f833a7f86ea54cd48c05fdb50d

# `test_acp_builder_tui_parameters.py`

## Summary
- TUI 起動 builder が、元の prompt に依存しない固定の実行 parameter と prompt 構成を組み立てることを検証するテスト。
- prompt に含めるポリシー、objective と original prompt の配置、editor input handoff の副作用がないことを確認する。
- 互換 module の公開面が現行の builder 関数だけであり、正本 builder と同一であることを確認する。

## Read this when
- TUI 起動 builder の固定 parameter、prompt のポリシー構成、objective の内容や配置を変更・検証するとき。
- TUI 起動 builder の互換 module の公開 API や正本 builder との対応を確認するとき。

## Do not read this when
- TUI 以外の builder の parameter や prompt を扱うとき。
- builder 実装そのものの詳細や正本仕様を確認する必要があり、対応する実装・正本を直接読むべきとき。

## hash
- 0d83516074befb39a42b976c723d80e148f3b093554bd1dc4816e009477b7cc3

# `test_basic_runtime.py`

## Summary
- Root/worktree と path model の runtime 契約を検証するテスト群。
- root placeholder、repository root、linked worktree、submodule、separate Git directory の解決境界を確認する。
- 並列な AgentCallPathContext と pushd における cwd の直列化・call 単位の分離を確認する。
- managed run worktree の作成・検索・削除について、管理領域、branch 対応、Git 登録、symlink、安全な置換の境界を検証する。

## Read this when
- root/worktree の解決や root placeholder の挙動を変更・調査するとき
- 並列実行時の process-global cwd 保護や AgentCallPathContext の独立性を確認するとき
- run worktree の path 検証、Git 登録確認、symlink 拒否、作成・削除の安全性を確認するとき

## Do not read this when
- 個別の path_model 実装詳細を直接確認したいとき
- Git fixture の生成補助や、ここで扱わない runtime 機能のテストを調べるとき

## hash
- cd2b23cfd1ebaccb5155151d0e354beb35889ded3412fbe6e3d6cc24aada6298

# `test_cli_command_tree.py`

## Summary
- oracle 変更後に公開 CLI の末端 command 集合と command tree の構造を検証するテスト。
- Typer/Click の help 描画互換性と、feedback report が固有の引数・option を公開しない契約を確認する入口。

## Read this when
- 公開 CLI に command または subcommand を追加・削除・移動し、oracle 列挙との一致を確認するとき。
- CLI 全体の help 描画で Typer/Click 互換性を確認するとき。
- feedback report の公開インターフェースに位置引数や固有 option がないことを確認するとき。

## Do not read this when
- 個別 subcommand の仕様や引数の詳細を確認・変更するとき。
- CLI の公開 leaf 集合や help 描画、feedback report の公開面に関係しない実装を調べるとき。

## hash
- 77aebc373c15cf6692bb9c39a413565fdefa923862c1df11f90e805a52bf85e8

# `test_cli_tui.py`

## Summary
- TUI サブコマンド起動直前の CLI 前処理を、エディター入力の反映、Codex TUI 起動パラメータ、doctor・indexing preflight の実行順、既存 Git 差分の保持を含めて外部挙動から検証するテスト。
- 通常のリポジトリと linked worktree の双方で、editor 入力ログ・agent call context・`.cmoc` ignore の配置先と記録先を検証する。

## Read this when
- `tui` サブコマンドの起動前処理、プロンプトエディター連携、Codex TUI への引き渡し条件を変更または調査するとき。
- linked worktree からの TUI 起動時に、main worktree 側へ保存されるログや agent call context の挙動を確認するとき。
- TUI 実行時の `.cmoc/gu` の ignore、ログ生成、既存の staged・unstaged 差分への影響を確認するとき。

## Do not read this when
- TUI 起動前処理や linked worktree 固有の記録先ではなく、プロンプト本文の組み立て規則そのものを変更・調査するときは、prompt builder や editor input の正本・実装を直接読む。
- TUI 以外のサブコマンドの CLI 前処理や、Codex 実行基盤全般の挙動だけを確認するとき。

## hash
- b82b8112c2ebf8f6faab2cf6619bb2a68a9d85bfe648db36481486a8670dd375

# `test_codex_runtime_errors.py`

## Summary
- Codex JSONL の異常系を検証するテスト群。非 object event、不正 JSON、空行を malformed protocol failure として分類し、Codex runtime が CmocError を返すことを確認する。Codex CLI 不在時には例外内容と失敗した `codex_call` ログを検証する。Codex 実行の正常系や実装本体ではなく、異常時の parser/runtime 境界とログ契約を確認したい場合の入口。

## Read this when
- Codex JSONL の不正入力や非 object event に対するエラー分類を確認するとき
- Codex CLI が見つからない場合の例外および `codex_call` 失敗ログのテストを探すとき

## Do not read this when
- Codex 実行の正常系フローや成功時の出力を確認するとき
- Codex JSONL parser、runtime、ログ出力の実装や正本仕様を直接確認するとき

## hash
- d499de66908c2d372163f1a6bea8610646987bbab9ee4b54cd52f2b6628873d8

# `test_codex_runtime_exec.py`

## Summary
- Codex exec の起動引数、prompt の stdin 渡し、sandbox・approval・override の契約を検証するテスト。
- Codex 実行によるリポジトリ書き込み、出力取得、不正 UTF-8 出力の保持、CODEX_HOME 設定ファイル非生成を確認する。
- 汎用 model provider の override と agent call の model・reasoning 設定が適用される経路を検証する。

## Read this when
- Codex exec の実行契約や override 引数を変更・検証するとき。
- Codex 実行結果の出力解析、prompt の入力経路、CODEX_HOME の副作用を変更・検証するとき。
- 汎用 model provider の設定反映や組み込み local provider 用フラグの扱いを変更・検証するとき。

## Do not read this when
- Codex CLI の一般的な利用方法や、対象テストが検証していない agent call の挙動を調べるとき。
- runtime 実装や正本仕様の詳細を確認することが目的で、テストケース自体の契約を確認する必要がないとき。

## hash
- 749a44c10250eb51e908b459a030fd3de815d281cc9b4f99077fdf8f50958f37

# `test_codex_runtime_home.py`

## Summary
- Codex 実行時の CODEX_HOME の既定値と環境変数の扱いを検証するテスト群。
- 相対 CODEX_HOME の解決基準、および Codex subprocess 起動前の home の存在・ディレクトリ形式の事前検証を確認する。
- auth.json の欠落やファイル種別を provider 非依存の preflight 検証対象に含めない境界を確認する。

## Read this when
- CODEX_HOME の既定値、環境変数で指定した値、相対パスの解決結果を確認したいとき。
- Codex subprocess が起動する前に、存在しない Codex home やディレクトリでない Codex home が拒否される挙動を確認したいとき。
- Codex home の検証が auth.json の provider 固有スキーマに依存しないことを確認したいとき。

## Do not read this when
- Codex subprocess の一般的な引数構築や実行イベント処理を確認したいとき。
- auth.json の認証内容や model provider 固有のスキーマ検証を確認したいとき。
- CODEX_HOME 以外の実行環境設定や、ここで検証されていないエラー経路を調べたいとき。

## hash
- 3cd2943266f8820d8285def29bafb570aa56b1fcdd9caeae51809dc6b395cc18

# `test_codex_runtime_paths.py`

## Summary
- Codex exec の並列実行時のログパス予約、agent call cwd、pure-oracle read の sandbox、repo root 配下の schema 保存、および `.agents` 権限非注入を検証するテスト。

## Read this when
- Codex exec の cwd・sandbox 引数・schema 保存先・ログパス衝突回避の挙動を変更または確認するとき。
- `PURE_ORACLE_READ` と linked worktree を含む Codex 呼び出しの権限境界を検証するとき。

## Do not read this when
- Codex exec の実装や正本仕様そのものを確認する必要があり、テストケースではなく実装・仕様を直接読むべきとき。
- Codex exec と無関係なテストや、ログ・cwd・sandbox・schema 保存の挙動を扱わないとき。

## hash
- 6fada71b05aedce5adcbfa8a1774ac8f7bd21b87b140c96b22a25cddc1423ecf

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex quota 超過後の待機・復帰・再試行を検証する回帰テスト群。
- 代表 quota probe の実行、並行呼び出しでの共有、失敗伝播、poll 上限を検証する。
- session ID による resume と、ID 不在・不正ログ時の prompt 再実行を検証する。
- Codex 呼び出し列、subcommand log、stdout・prompt・stderr・output の記録、および CODEX_HOME/cwd の扱いを検証する。

## Read this when
- Codex quota 超過後の外部挙動や retry 状態機械を確認したいとき。
- 代表 probe、resume、再実行、並行 quota 待機、失敗処理の回帰条件を確認したいとき。
- quota retry に関する call log・subcommand log・実行環境の観測結果を確認したいとき。

## Do not read this when
- quota retry の実装仕様や正本文書を確認したいとき。
- quota probe builder の prompt 生成や互換 module の公開範囲だけを確認したいときは、対応する builder または adapter を直接読む。

## hash
- 779a97dc64711565d78e8cefe44326b5da8d7c5a601b72bc01844348abf59b76

# `test_codex_runtime_retry.py`

## Summary
- Codex exec の Structured Output 補正、capacity retry、JSONL error、中断、成果物差分保持を、subprocess 呼び出し・retry 状態・call log・subcommand event の連続した外部挙動として検証するテスト群。

## Read this when
- run_codex_exec の出力契約違反や parse failure の同一 session 補正、補正時の事後条件・成果物復元、session 欠落時の失敗を確認するとき。
- capacity failure の再試行・指数 backoff・上限、および retry 中も agent diff を保持する挙動を確認するとき。
- 未知の JSONL error、stdout JSONL 外の error marker、KeyboardInterrupt、schema 事前検証について、最終例外と call log／subcommand event の記録を確認するとき。

## Do not read this when
- INDEX.md のルーティングだけを確認したい場合や、run_codex_exec の通常成功経路・別の実装詳細を直接調べる場合。
- 個別の Structured Output schema 定義や汎用的なログ仕様そのものを確認したい場合は、それぞれの正本仕様・実装対象を直接読む。

## hash
- f657c53dab552b1db74e14c2657330725653d50b0f4abda6a899c86efb08bccf

# `test_codex_runtime_subprocess.py`

## Summary
- Codex subprocess と run process の安全な追跡・停止・cleanup を検証するテスト群。pidfd、process group、PID 再利用、leader 終了、tracking file の不正状態、signal 保留、child の停止・reap、継承環境変数の扱いを対象とする。

## Read this when
- Codex subprocess の起動後 tracking 登録、signal 処理、専用 process group の停止、または run process cleanup の安全性を変更・調査するとき。
- pidfd や process identity の検証、stale/reused PID・PGID の fail-closed 動作を確認したいとき。
- tracking file の形式検証、特殊 file・encoding 異常、tracking 更新失敗時の child cleanup を扱うとき。

## Do not read this when
- Codex subprocess や run process の追跡・停止・cleanup に関係しない機能を扱うとき。
- 実装ではなく、通常の Codex CLI 起動仕様や toast 通知の詳細だけを確認したいときは、該当する正本仕様や実装対象を直接読む。
- 一般的な pytest 共通処理や subprocess の基本動作だけを調べるとき。

## hash
- 9b31764b42d859d15d00773bcfb2c969454bdcf789915b1b361e4656d601e06e

# `test_codex_runtime_tui.py`

## Summary
- Codex TUI 実行の統合テスト。完全な prompt と CLI 引数、アクセスモード、linked worktree、エディター引き渡し、通知・hook 設定、call log、サブコマンドイベントを検証する。
- 設定不備や Codex CLI の未検証バージョン、CLI 不在、KeyboardInterrupt、非 0 終了時に、実行前検証・失敗分類・ログ保存・エラー報告が仕様どおりになることを確認する。

## Read this when
- Codex TUI 呼び出しの引数・prompt・sandbox・通知 hook・editor input handoff の挙動を変更または確認するとき。
- Codex CLI 呼び出しの成功・失敗、call log、サブコマンドイベント、設定検証順序をテストする必要があるとき。

## Do not read this when
- Codex TUI 以外の実行経路や、prompt 構築そのものの仕様を直接確認したいとき。
- テスト対象の実装ではなく、TUI の正本仕様や Codex CLI の一般的な利用方法だけを確認するとき。

## hash
- 0b8c272c9146c04101b3c74e5cf5077085420878d1f8fd51d8f270fb8967d76e

# `test_doctor_cli.py`

## Summary
- doctor preprocess の CLI と直接呼び出しを対象に、修復 lifecycle の外部契約を検証する統合テスト。
- `.cmoc/gu` の ignore、`.agents/.gitkeep`、config、refactor state、reporter 検証の順序と degraded/error 挙動を確認する。
- 共有 repository lock、linked worktree、既存の staged・unstaged・unmerged Git index 状態を保持したまま修復・commit する境界を検証する。

## Read this when
- doctor preprocess の修復順序、reporter 事前検証、lock 待機、CLI レポートを確認するとき
- config や refactor state の生成・同期、`.cmoc/gu` と `.agents` の追跡状態を確認するとき
- doctor 実行前から存在する staged・unstaged・unmerged 差分、index flag、rename、intent-to-add の保持挙動を確認するとき
- repository root と linked worktree 間で修復対象を分離する挙動を確認するとき

## Do not read this when
- doctor preprocess の外部挙動や Git index 保持を調べる必要がないとき
- doctor 以外のサブコマンド、単体の設定仕様、または個別実装の詳細を直接確認したいとき

## hash
- b3994a1a204bf11f73ad6d9cd229074f8ba06a3b7b4f356336d6d74b7a2a89d8

# `test_editing_run_cli.py`

## Summary
- workload fork と共通 run join/abandon の統合 realization test。editing run の session state、隔離 run worktree、agent 差分、commit、fork report、process tracking、cleanup を同じ lifecycle fixture で検証する。
- realization apply/refactor fork と run join/abandon の成功・失敗・中断・rollback・force-resolve・INDEX/Oracle 差分処理を横断し、実装間で共有される state 遷移と terminal report の契約を確認する。

## Read this when
- realization apply/refactor fork または workload fork の run lifecycle を変更・調査するとき。
- run join/abandon の merge、cleanup、process tracking、post-join 同期、失敗時 rollback を確認するとき。
- agent 境界、INDEX 更新、管理対象外差分、遅延 child・commit、interruption、fork/lifecycle report の挙動を実装に照合するとき。

## Do not read this when
- 単一の production helper や単一サブコマンドの局所仕様だけを確認したい場合は、対応する実装または専用テストを直接読む。
- INDEX 生成の一般的な仕組みや、統合 lifecycle を伴わない単純なテスト実行方法だけを調べる場合は、この対象を読む必要はない。

## hash
- 7e825bb0828e981d69a7ec6be66220f77d69220f6c827b8cf45a1fdce6df73b1

# `test_editor_input_handoff.py`

## Summary
- editor input handoff target の lifecycle と、editor work file への全面上書き境界を検証するテスト。
- repository 不一致、symlink 経由の書き込み、認証前の内容送信、target close 中の accepted submission、接続期限切れ後の後続 submission を確認する。

## Read this when
- editor input handoff の受理・拒否条件や、最後の submission を確定入力にする挙動を確認・変更するとき
- repository 境界、editor work file の symlink 防止、target close の排水、認証・接続期限の安全性を確認するとき

## Do not read this when
- handoff の実装や protocol の詳細を確認したいときは、対応する実装・protocol の正本を直接読む
- prompt editor input の予約・収集・確定処理だけを扱い、handoff submission の lifecycle や安全境界を扱わないとき

## hash
- 3144fff6d2c0656c5524fd8ccb355fd92409ebc6e027b3eb7af68a660580ddf7

# `test_editor_input_handoff_mcp.py`

## Summary
- editor input handoff の agent-facing MCP interface を検証するテスト。公開 tool、canonical schema、JSON-RPC/MCP protocol negotiation、入力検証、domain failure、transport failure 時の status・retryability・情報秘匿、応答 field の公開境界を扱う。

## Read this when
- editor input handoff MCP の公開契約や overwrite tool の agent-facing 応答を変更・確認するとき
- JSON-RPC request validation、protocol version negotiation、tool error の分類、送信結果不確実性、content 非漏洩の挙動を確認するとき

## Do not read this when
- editor input handoff のファイル上書き本体や target のライフサイクルだけを調べるとき
- MCP interface ではなく canonical input schema の定義そのものを確認するときは、正本 schema を直接読む方が適切なとき

## hash
- 94b33cbc1156b60501389bf4a9190cda3a8cfdc658a6a96ee66a075fb815866a

# `test_feedback.py`

## Summary
- feedback reporter と collector の受付・検証・保存、および raw observation から issue candidate、remediation、active state の atomic publication と cleanup までを同一 repository fixture で検証するテスト群。
- MCP/loopback transport、payload・context・rate limit・UTF-8・secret masking・symlink 境界、並行 call、割り込み、rollback、再実行、generation artifact の整合性を確認する feedback report の統合テスト入口。

## Read this when
- feedback observation の reporter または collector の protocol、入力検証、durable raw storage、degraded warning の挙動を確認したいとき
- feedback report の候補正規化・重複判定・threshold、remediation の wave 処理、active state の compact 化、current pointer、generation hash、cleanup、recovery を検証したいとき
- session precondition、run join/abandon、user interruption、rollback、publication failure 後の再開可能性をテスト仕様から確認したいとき

## Do not read this when
- feedback の正本仕様や実装の詳細そのものを読むことが目的で、テストによる外部挙動の確認が不要なとき
- 個別の normalize/remediate oracle schema や builder parameter の形式だけを確認すれば足りるとき
- feedback 以外のサブコマンドや、単独の logging・session 一般仕様を調べるとき

## hash
- 9ecad917a1d12832782bba13ab42b5462c06908418af06a208a0e6b58c120383

# `test_feedback_decision.py`

## Summary
- このテスト対象は、feedback 判定の入力基礎が Git 管理対象・依存設定・oracle/realization を含み、内容や実行モードの変更を検出することを検証する。
- nested な .git 名ディレクトリでは実 Git メタデータを除外しつつ通常ファイルを追跡し、削除済み入力や worktree 外パスを扱わず、相対 worktree パスを正規化する境界を確認する。

## Read this when
- feedback 判定根拠の入力集合が何を含むか、設定・realization・nested Git 構造の変更を検出できるか確認したいとき。
- worktree_inputs のパス安全性、Git mode の扱い、削除済みファイルや相対パスの挙動を変更・調査するとき。

## Do not read this when
- feedback 判定ロジック本体や実装詳細を変更する場合で、入力基礎の回帰条件を確認する必要がないとき。
- feedback 以外の機能のテストや、単に通常の Git メタデータ除外規則だけを調べるとき。

## hash
- f0c7af0ef00a4294b786953306f7914c6ee5e82e2be7b0747ca77f3bf00c4051

# `test_feedback_reconfirmation.py`

## Summary
- feedback の remediation における再確認、根拠変更の検出、checkpoint・artifact の整合性検証、seal 後の publish/recovery 制約を検証するテスト。

## Read this when
- feedback の wave、report cut、remediation checkpoint、根拠再確認、修復サイクル、join・publish・recovery の挙動を変更または調査するとき。
- 変更後に、根拠変更時の再実行、重複観測の拒否、壊れた checkpoint の扱い、seal 済み結果の保護を確認するとき。

## Do not read this when
- feedback の観測取り込みや候補生成だけを変更・調査し、remediation の再確認や checkpoint 連携に影響しないとき。
- 対象の実装仕様や一般的なテスト実行方法を確認したいだけで、これらの回帰ケースを扱わないとき。

## hash
- e1494d5d117db36e69ac913bd3bc923bdfa07d9eafe59efbfe9f511c5ca7e9fa

# `test_file_inventory.py`

## Summary
- 日本語技術文書のルーティング規定に従い、テスト本文だけを根拠に INDEX.md 向けの案内を整理した。

## Read this when
- full-tree の oracle/realization file インベントリが Git ignore、nested repository、metadata 境界を正しく扱うか確認するとき。
- 通常ファイル・削除済みファイル・非 UTF-8 filename・symlink・FIFO・socket/device 相当 path の分類や拒否条件を検証するとき。
- refactor state の列挙対象、SHA 更新、追加・変更・削除ファイルの同期挙動を確認するとき。
- ignore source の repository 単位の適用、重複検証抑制、候補数増加時の Git 処理量一定性を確認するとき。

## Do not read this when
- 列挙や分類の実装を変更・デバッグする場合は、まず実装コードを直接読む。
- 正本仕様の意図や契約そのものを確認する場合は、参照される仕様書を直接読む。
- INDEX.md や AGENTS.md の運用規定を確認するだけの場合は、このテスト本文を読む必要はない。

## hash
- da73a7c13009bf9a158acb7588923d43cea4dc320c8c451c03f5843438f61fec

# `test_indexing_cli.py`

## Summary
- `cmoc indexing` の CLI 実行、preflight、worktree 対象判定、doctor 初期化、Codex による INDEX.md 生成、ハッシュによる再生成省略、INDEX 更新の限定 commit を外部挙動として検証するテスト群への入口。

## Read this when
- `cmoc indexing` の正常系・初期化・linked worktree・dirty worktree の拒否条件を確認したいとき。
- INDEX.md 更新前後の preflight、worktree 固有設定、Codex 呼び出し、fresh hash の扱いを確認したいとき。
- INDEX.md だけを commit し、既存の staged・unstaged 差分を保持する commit lifecycle や git diff 異常時の失敗処理を調べるとき。

## Do not read this when
- INDEX.md のルーティング規則そのものや生成用 Structured Output schema を確認したいときは、対応する正本仕様・schema を直接読む。
- `cmoc indexing` 以外のサブコマンドや、INDEX 更新処理の実装詳細そのものを調べることが目的のとき。

## hash
- 73ebd8fa4054a36b25c4047c4178951c65411cd8182e6d414b35ba21bef6e627

# `test_indexing_common.py`

## Summary
- `commons.indexing` の INDEX entry と directory traversal を直接検証する共通回帰テスト群。
- entry の render/parse、入力検証、hash の計算と再利用、更新順序、並列生成、失敗時の部分書き込み復元を扱う。
- symlink cycle、特殊ファイル、非 UTF-8 名、空ディレクトリ、nested memo、linked worktree の lock など、INDEX 更新の境界条件を検証する。

## Read this when
- INDEX entry の生成・解析・hash 再利用・更新対象判定を変更または調査するとき
- directory traversal の順序、祖先関係のない更新の並列実行、pushd 中の worker 制約を確認するとき
- entry 生成失敗時の復元、symlink や特殊ファイルの除外、非 UTF-8 filename の hash、nested memo の扱いを確認するとき

## Do not read this when
- CLI lifecycle や indexing サブコマンド全体の統合動作を確認することが目的のとき
- 個別の INDEX entry の正本仕様や生成プロンプトを確認する場合に、実装・仕様そのものを直接読むべきとき
- 一般的なファイル走査や並列処理を調べるだけで、`commons.indexing` の契約が関係しないとき

## hash
- abe89b033c919a9c2b5081e47033cdfb2e0bf160c92211daaf118e4482222840

# `test_indexing_preflight.py`

## Summary
- Codex の exec/TUI 呼び出し直前に実行する indexing preflight の挙動を検証するテスト。
- preflight の実行順序、対象 worktree の選択、repository lock 待機、パラメータによる無効化、file access violation 後の recovery indexing 禁止を扱う。

## Read this when
- Codex 呼び出しへ indexing preflight を統合する処理の挙動を確認・変更するとき。
- preflight の対象 root、git commit、lock 排他、実行スキップ条件を確認するとき。
- file access violation 発生後に追加の indexing を行わない契約を確認するとき。

## Do not read this when
- indexing の通常更新処理や INDEX.md エントリー生成の詳細を調べるとき。
- Codex 呼び出し一般の仕様や preflight 統合に関係しない lock 処理を調べるとき。

## hash
- 8e4c49958ddfb34d504a365dee9746cabb8d8e61bb901055f2465904bfb6a93e

# `test_oracle_edit_cli.py`

## Summary
- 対象は `cmoc oracle edit` の統合的な制御テストで、成功・本命 exec 失敗・仕様削減 exec 失敗を同じ invocation で検証する。
- editor 入力、exec 起動パラメーター、indexing preflight、起動前提、Git 差分、session state、生成物の後始末、通知・レポートの境界を横断して確認する。
- oracle edit の実装や仕様変更で、二段階 exec の順序・失敗時の分岐・未コミット変更の保持・利用者向け結果報告を確認したい場合の入口となる。

## Read this when
- `cmoc oracle edit` の成功時または main/reduction 失敗時の制御フローを変更・調査するとき。
- editor work file と保存コピー、2 回の exec、indexing preflight、Git 差分や session state の不変条件をまとめて検証するとき。
- oracle edit の起動前提違反、通知、terminal report の分類や agent call status の適合性を確認するとき。

## Do not read this when
- oracle edit の具体的な prompt 生成文面だけを確認したい場合は、実装側の builder や prompt の正本を直接読む。
- oracle edit 以外の oracle サブコマンドや、一般的な Git・session state の共通処理だけを調べる場合。
- 単純な editor 入出力や共通 CLI 通知の単体挙動だけを確認する場合は、それぞれの専用テストまたは実装へ直接進む。

## hash
- 6d04630cb695af2bf39166fb62f85b6ce677236ffc18a3e21af8839f9209bf32

# `test_oracle_investigation_cli.py`

## Summary
- `oracle investigation` CLI の起動経路を検証するテスト。セッション前提なしの main worktree で、doctor 前処理、prompt editor 入力、investigation 用パラメータ構築、indexing preflight、有効化後の TUI 起動までの順序と引き渡し内容を確認する。
- investigation の realization adapter が公開する名前を builder だけに限定することを検証する。

## Read this when
- `oracle investigation` の CLI 起動条件、prompt editor との連携、TUI 起動前後の処理順序を変更・調査するとき。
- investigation 用 launch TUI builder の公開 API や補助名の漏出を確認するとき。

## Do not read this when
- `oracle investigation` の仕様本文や一般的な indexing 規則を確認したいだけのときは、参照元の oracle 文書を直接読む。
- investigation 以外の sub-command の起動経路や builder 公開 API を扱うとき。

## hash
- 5add200a877c12b3d16a4f6f6e1eb5393f4dcfe53dab1dda40f47f5006c7866a

# `test_packaged_import.py`

## Summary
- packaged layout にコピーした ACP・basic・commons・oracle・config の import 境界と公開面を検証するテスト。quota probe、oracle edit／prompt editor 入出力、ACP basic の正本型再公開、cmoc config の公開定義を対象に、隔離実行環境での参照先・名前空間・parameter 内容を確認する。

## Read this when
- パッケージ配置後も canonical な正本や prompt を参照できるか確認したいとき
- ACP builder、oracle edit、prompt editor、config の公開 import・__all__・module namespace の境界を変更または調査するとき
- 実行ディレクトリや外部 site-packages の影響を除いた packaged layout での import 挙動を検証するとき

## Do not read this when
- 対象が単一モジュールの内部ロジックや通常の開発環境での import だけに関する場合
- quota probe、oracle edit／prompt editor、ACP basic、cmoc config の packaged layout 上の公開境界を確認する必要がない場合
- テストの実装詳細ではなく、各 canonical 定義や prompt の正本仕様そのものを読むべき場合

## hash
- 913323e3b0b5f350cfd8f7b402cd00c58649694cc98c8f2f0dcc84dc0bdea6af

# `test_primary_report.py`

## Summary
- 日本語のテスト群として、非対話末端サブコマンドの primary report 完了契約を検証する。
- 処理開始前のエラー、中断、Codex 出力・受理済み observation の保持、refactor 中断、既存 report の更新失敗、未保存 report パスの内部失敗を対象とする。

## Read this when
- 各サブコマンドの primary report に必要な保存先・front matter・完了理由が満たされるか確認するとき。
- ユーザー中断時の invocation summary や、実行出力・feedback observation の report 反映を検証するとき。
- primary report の atomic 更新失敗や保存未確認時の内部失敗処理を確認するとき。

## Do not read this when
- primary report の完了契約や保存失敗処理を扱わず、個別サブコマンドの通常動作だけを確認するとき。
- report 本文の生成実装や runtime logging の詳細を直接調べる必要があり、このテスト群ではなく実装・仕様の対象を読むべきとき。

## hash
- a04b6c7a3c8f90bffc4730eca5f3f377b683ccacf67e191a9778a35e13c38947

# `test_production_cli.py`

## Summary
- 利用者向け entrypoint の全末端サブコマンドを、独立 process・実 Codex CLI・実推論で検証する受け入れ試験。
- 非対話および TUI の本番経路について、終了 code と report・state・Git・call log など外部から観測できる結果を確認する。

## Read this when
- 全末端サブコマンドの本番経路に検証漏れがないか確認したいとき。
- 実 Codex 呼び出し、PTY 上の TUI 完了、状態遷移、Git の副作用を含む統合試験の範囲を確認したいとき。

## Do not read this when
- 個別サブコマンドの通常仕様や内部実装を確認したいとき。
- LLM の回答品質を評価したいとき、または本番 entrypoint 以外の単体・局所テストを探しているとき。

## hash
- ec07e4f302b1a4a533e8c412646bd5599cd1ee058b29fd5293dc661ce2381b89

# `test_production_cli_support.py`

## Summary
- 実経路統合テストで使うPTY操作helperの挙動を検証するテスト。trust確認プロンプト検出後、次のpollで確定し、CR入力を送るまでの状態遷移を扱う。

## Read this when
- 実経路CLIのtrust確認プロンプト処理や、PTY helperのpollタイミング・入力送信を確認または変更するとき。

## Do not read this when
- PTY操作helperではなく、CLI本体のtrust確認実装や、他の実経路統合テストの責務を直接確認するとき。

## hash
- 67687d4517bc714cca1ab03754abb96c90a374dbc48b788c0eed9ca2e6d1e5d1

# `test_prompt_editor_input.py`

## Summary
- prompt editor input の外部挙動を検証するテスト。作業ファイルと保存コピーの分離、編集後の入力抽出、エディタ選択、パス境界、保存先の symlink 防止、異常時の後始末を確認する。

## Read this when
- prompt editor input の予約・編集・入力収集・確定処理を変更または検証するとき
- 作業ファイルと保存コピーの扱い、エディタ起動条件、ファイル種別やパス境界の安全性を確認するとき
- prompt editor input の異常系や handoff target のクリーンアップ挙動を確認するとき

## Do not read this when
- prompt editor input の実装や正本仕様そのものを確認する必要があり、テスト結果ではなく実装・仕様を直接読むべきとき
- prompt editor input と無関係な機能のテストや実装を扱うとき

## hash
- b8b4b66dd01bf391cb9aa5acfb413d0b31af2123cba619bb3fe6b17fdc78898d

# `test_prompt_parts.py`

## Summary
- prompt part 各 policy の SDHeader 構造・カテゴリ順序・主要文言と、complete prompt の組み立て、動的セクション、placeholder 展開、file access 境界を回帰検証するテスト。prompt builder の変更が複数 policy の注入や出力順序、参照境界、モード別制約を壊していないか確認する入口。

## Read this when
- prompt builder の policy 追加・変更、complete prompt のセクション順序や objective 構築、placeholder 定義・競合処理を変更または検証するとき。
- oracle、realization、feedback、index entry、routing、editor handoff、file access 各 policy の rendering と complete prompt への注入結果を確認するとき。
- file access mode ごとの書き込み境界、linked worktree での同一性、prompt の共通 feedback instruction を回帰確認するとき。

## Do not read this when
- prompt builder 本体の実装詳細を変更せず、個別 policy の正本仕様や policy 文面そのものだけを確認するときは、対応する oracle doc または policy builder を直接読む。
- prompt の rendering や complete prompt の組み立て、placeholder 展開、policy 注入に関係しないテストや機能を調査するとき。

## hash
- 9bdd688e0f3c2b8ceef425ae83819af3e80ea1fada4eed76888ae070a7c20e97

# `test_runtime_cli.py`

## Summary
- CLI の共通 runner を通じて、error report、console／file log、doctor preflight、shell completion、終了通知、ユーザー中断の境界を検証するテスト群。
- work root、subcommand event、終了処理を共有する CLI lifecycle の外部契約を横断的に確認する入口。

## Read this when
- CLI の成功・失敗結果、stderr／stdout、終了コード、診断ログの記録を確認したいとき
- doctor preflight、work root 制約、shell completion probe の副作用抑制を確認したいとき
- TUI と非対話 CLI の終了通知、KeyboardInterrupt、Codex subprocess 起動境界を確認したいとき
- timestamp、duration 表示、並列 logger event、UTF-8 ログ保存の CLI 共通基盤を確認したいとき

## Do not read this when
- 個別サブコマンド固有の業務処理や、そのコマンドだけの入力・出力を確認したいとき
- error、log、preflight、completion の実装詳細や正本仕様を直接調べるときは、対応する runtime モジュールまたは oracle 仕様書へ進む
- CLI lifecycle をまたがない単独のユーティリティやテストデータの挙動だけを確認したいとき

## hash
- b5c552db2767c9b0d4121953446f754550721f65264738803e20a4cdb355080f

# `test_runtime_codex_conflicts.py`

## Summary
- session join の conflict path が prompt にのみ反映され、path 別の sandbox 設定や Codex override argv に変換されないことを検証するテスト。conflict 対象が oracle 配下でも src 配下でも、repo write と共通の workspace-write sandbox を使い、対象 path が argv や権限設定へ漏れないことを確認する。

## Read this when
- session join の conflict resolution、prompt 生成、sandbox/権限引数への変換を変更・検証するとき
- conflict 対象 path の扱いや Codex override 設定の回帰を調査するとき

## Do not read this when
- session join の conflict path と無関係な runtime Codex 機能を変更・調査するとき
- sandbox 設定や prompt への conflict 対象の反映を確認する必要がなく、対象の実装・正本仕様を直接読むべきとき

## hash
- 8a87436b654938a146bd3624bb6125d96a016fc954bfaec1f63c87a6fe83d99c

# `test_runtime_codex_permissions.py`

## Summary
- Codex の argv builder が permission profile に依存せず、path 別の read/write 例外を受け付けないことを検証するテスト。

## Read this when
- Codex override 引数生成 API の引数制約や、ファイルアクセス権限に関する回帰を確認するとき。

## Do not read this when
- Codex override 引数生成 API の実装詳細を直接調べるときは、対象の実装ファイルを読む。
- permission profile と無関係なテストや、通常の AgentCallParameter 構築を調べるとき。

## hash
- 647b0984d15205ef401da1ccdb65378808a7ad39e4b303a152cbf4809a4a278b

# `test_runtime_codex_profile.py`

## Summary
- Codex argv の model・sandbox・provider 上書き引数を、各 FileAccessMode と agent call 設定に基づいて検証するテスト。
- MCP context の環境変数隔離、editor input handoff の条件付き注入、SessionStart hook と legacy notification の組み合わせを検証する。
- Codex CLI の検証済みバージョン判定、provider TOML のエンコード、未定義設定の fail-closed、schema のハッシュ保存と不正 JSON 出力の扱いを検証する。

## Read this when
- Codex 起動時の sandbox、approval、model、provider、MCP、notification または hook の argv 契約を変更・確認するとき。
- Codex subprocess の環境変数継承や editor input handoff の注入条件を変更・確認するとき。
- Codex CLI バージョン判定、provider 設定の TOML 化、未定義設定の起動前エラー、schema/output の入出力境界を変更・確認するとき。

## Do not read this when
- Codex argv の上書き契約やその検証対象に関係せず、runtime_codex_profile の実装本体を直接調べるとき。
- Codex の model/provider 仕様そのものを確認する必要があり、参照先の正本仕様を直接読むべきとき。
- 一般的な pytest 実行方法や、対象テストが扱わない別の runtime・MCP 機能を調べるとき。

## hash
- e5b196651877a28704aea0701e21c400034bad1ba98f661d43ad2331662fad30

# `test_runtime_config.py`

## Summary
- CmocConfig の既定値、JSON 変換・ファイル永続化、merge、Codex model provider／agent call 設定の入力検証を検証する設定回帰テスト。

## Read this when
- 設定の既定値や JSON round-trip、config.json の読み書き、旧配置・旧設定との互換境界を確認したいとき。
- Codex の model provider、agent call、recovery 試行回数、provider-local 設定の受理条件や不正入力時の利用者向けエラーを確認したいとき。
- 壊れた JSON、深すぎる値、非通常ファイル、named pipe、symlink、UTF-8 出力など設定ファイル境界の安全性を確認したいとき。

## Do not read this when
- CmocConfig の実装仕様そのものや設定項目の正本定義を確認する場合は、まず設定実装・正本仕様を直接読むとき。
- 設定以外の runtime 動作、agent call の実行処理、一般的なエラー表示の仕様だけを調べるとき。

## hash
- 66e4add2d47e76b67bd878d165dcaba70171c29428419fee85cf3aec7ba2623a

# `test_runtime_content.py`

## Summary
- runtime_content の補助関数を検証するテスト。内容が NUL byte を含むかによる binary 判定と、hash ベースの保存時に既存 symlink のリンク先を上書きせず置換する挙動を扱う。runtime_content の保存処理や binary 判定を変更・調査するときのテスト入口。

## Read this when
- runtime_content の is_binary または write_hashed_file を変更・レビュー・デバッグするとき
- テキスト／binary 判定や、hash path が symlink の場合の安全な保存挙動を確認するとき

## Do not read this when
- runtime_content の実装詳細を確認したいだけで、テストケースや期待挙動の確認が不要なとき
- runtime_content と無関係な機能の実装・テストを調査するとき

## hash
- 1d7cd925d0b731ec53366c6eb796bed8c9be466df205b88ae5f6b9f8f07ad5c3

# `test_runtime_file_access.py`

## Summary
- FileAccessMode の永続化値と、cmoc のファイルアクセス権限を Codex sandbox mode へ変換する契約を検証するテスト。
- READONLY・PURE_ORACLE_READ は read-only に、書き込み系および NO_POLICY は workspace-write に変換されることを確認する。ファイルアクセスモードと sandbox 変換の挙動を変更・検証する際のテスト入口。

## Read this when
- FileAccessMode の JSON 用永続化値を変更または確認するとき。
- file_access_to_sandbox_mode の対応関係や repo_write を含む書き込み権限の変換を変更・検証するとき。

## Do not read this when
- プロンプトのファイルアクセス規則そのものを確認するときは、対応する oracle の仕様文書を直接読む場合。
- FileAccessMode や sandbox 変換に関係しないテスト・実装を扱う場合。

## hash
- cbbb2e829ce17df28aa8f61a44c8978c34f2f90b4d0c24406732cbd6c2843f63

# `test_runtime_git_ignore.py`

## Summary
- Git ignore の安全な更新と判定を検証するテスト。`.cmoc/gu/` の ignore 追加、既存パターンとランタイム状態の保持、tracked/untracked の判定、特殊ファイル・symlink・global/nested exclude の拒否、`git check-ignore` 判定失敗時のエラー化を対象とする。

## Read this when
- Git ignore 判定や `.cmoc/gu/` の ignore 設定処理を変更・検証するとき。
- `.gitignore`、Git の `info/exclude`、global excludes、nested `.gitignore` の安全なファイル種別・symlink 扱いを確認するとき。
- `is_git_ignored` または `is_untracked_git_ignored` の tracked/untracked 分類と `git check-ignore` 失敗時の挙動を確認するとき。

## Do not read this when
- Git ignore や runtime_git の挙動ではなく、他のサブコマンド、oracle/realization file 列挙、または無関係なテストを直接調べるとき。
- ignore 設定の実装詳細そのものを変更・調査する必要があり、まず runtime_git の実装や正本仕様を直接読むべきとき。

## hash
- cd4002d7f6293b03a9d07d5d099490cc545f8643d83156258709df390981e93f

# `test_runtime_refactor.py`

## Summary
- realization refactor の永続 state 同期・検証と対象選択をテストする入口。oracle／realization のファイル集合、パス分類、symlink・特殊ファイル・Gitlink の拒否、履歴保持と変更時の再調査、state schema／安全な読み書き、調査優先順位を確認する。

## Read this when
- realization refactor の state 同期や target 選択の挙動を変更・調査するとき。
- oracle／realization ファイルの分類境界、state の入力検証、symlink や非通常ファイルに対する安全性を確認するとき。

## Do not read this when
- refactor state の実装詳細そのものを変更・理解する必要があり、実装コードを直接読むべきとき。
- realization refactor と無関係な Git 操作、別の state、または一般的なテスト基盤だけを調べるとき。

## hash
- 0782067babf20fc6d1f9498735f73e52de508cbe1c569e1bc9fe813472839e86

# `test_runtime_state.py`

## Summary
- session/run state schema の永続化・読み込み検証と、managed branch からの session state 解決をテストする。
- 不正な branch 形状、state payload、JSON、path、symlink、非通常 file/directory を利用者向けエラーへ変換する境界を検証する。
- session fork lock が process 間で共有されることを検証する。

## Read this when
- runtime state の schema 検証、state file の read/write、managed branch 解析の挙動を変更・確認するとき
- 不正入力や filesystem 境界で raw exception を漏らさないことを確認するとき
- session fork lock の process 間排他を調査するとき

## Do not read this when
- runtime state の実装仕様や本体処理を確認したいとき
- 個別テストの fixture、期待値、テスト手順の詳細を直接確認したいとき

## hash
- 32811ae0b83c739ed0c9b39d68097f7c1070c6b84ba11da5216b054ca0ba8c48

# `test_runtime_wrapper.py`

## Summary
- bin/cmoc の仮想環境検査、Python probe、本番 main.py への引数転送、補完プローブ時の特別な転送、および失敗時の cmoc 形式エラーレポートを検証するテスト。wrapper の起動経路や venv 欠損・不正実行ファイル・補完動作を確認したい場合の入口。

## Read this when
- bin/cmoc の起動時に必要な .venv/bin/python の検査や probe 動作を変更・調査するとき
- wrapper が main.py、引数、_CMOC_COMPLETE をどのように転送するか確認するとき
- 起動失敗時または補完プローブ時の stdout・stderr・終了コードを検証するとき

## Do not read this when
- CLI コマンド本体の通常動作や個別サブコマンドを確認する場合
- エラーレポート仕様そのものを変更・確認する場合は、まず正本のエラーハンドリング仕様を読むとき
- 補完機能の仕様や実装全体を確認する場合に、このwrapper検査だけでは不十分なとき

## hash
- 707b3f26990edb78254d6b4a9b15a2b50f704cf7f8afd6c89b609f3ce72be6d5

# `test_session_cli.py`

## Summary
- session fork・join・abandon の CLI 外部挙動を、branch／state のライフサイクル、linked worktree、cleanup、rollback、dirty worktree 拒否、conflict 解消まで横断して回帰検証するテスト群。
- session 状態遷移や conflict 解消処理の変更・不具合を、実際の CLI 実行と永続 state、Git branch、report、標準出力／標準エラーの観測から確認する入口。

## Read this when
- session fork／join／abandon の仕様変更や回帰を調査するとき。
- session state、linked worktree、branch cleanup／rollback、preprocess、dirty worktree 制約の CLI 挙動を検証するとき。
- session join の conflict marker 解消、Codex 呼び出し境界、対象外差分拒否、特殊な path 処理を確認するとき。

## Do not read this when
- session CLI 以外のサブコマンドや、単体の内部実装だけを調べるとき。
- session の正本仕様や実装そのものを直接確認すべきで、回帰テストの観測例が不要なとき。
- 一般的な Git 操作や session state と無関係なテスト fixture を探しているとき。

## hash
- e90d065467a287774d670afba2a8b1cfed81c302b072e71933246106519035f9

# `test_skill_metadata.py`

## Summary
- Repository local skill の SKILL.md にある YAML frontmatter の必須 metadata とディレクトリ名の一致を検証するテスト。skill 追加時の metadata 契約を確認する入口。

## Read this when
- Repository local skill の frontmatter 契約、必須 name・description、または skill 自動検査の挙動を変更・確認するとき。

## Do not read this when
- skill 本文の設計や実装手順を確認するとき。個別 skill の SKILL.md を直接読むべき場合。

## hash
- bf735875997b038795c375af2a689094f308e7a286145efe3996c3ce9cd796d8

# `test_struct_doc_rendering.py`

## Summary
- 構造化文書 Markdown renderer の整形挙動を検証するテスト。連続空行の縮約、可変長 fence、タグ block と参照表記、参照未検証、policy のカテゴリ順、互換 API の再公開、不正 child の拒否を扱う。

## Read this when
- 構造化文書ノードの Markdown 描画結果や空行・code block・fence の仕様を変更または確認するとき
- SDTagBlock、SDPolicy、canonical node、basic.struct_doc の互換 renderer の挙動を検証するとき
- 構造化文書ノードの child 型検証や参照表記の描画挙動を調査するとき

## Do not read this when
- Markdown renderer の実装詳細や正本仕様を確認したいだけで、テストケースの期待挙動を調べる必要がないとき
- 構造化文書以外のテストや、renderer を介さないデータ構造の変更を扱うとき

## hash
- 59777795fc220c56f39c46ca4ee6aa2b3d9cb6b4f47edec071c540bc15734205

# `test_windows_toast.py`

## Summary
- Windows toast 通知の表示内容と安全な transport 境界を検証するテスト。
- Codex TUI callback の root session 判定、重複抑止、終了時の排出・cleanup、standalone hook の異常系を検証する入口。

## Read this when
- Windows toast の通知文面、機密情報の非露出、PowerShell への JSON stdin 渡しを確認・変更するとき。
- Codex callback と SessionStart hook の session 管理、turn 単位の通知、並行実行時の一度きり保証を確認するとき。
- 通知初期化の completion probe 挙動、callback の invocation-local state、終了時の待機と cleanup を確認するとき。

## Do not read this when
- Windows toast や Codex callback の実装そのものを変更する場合は、まず実装と正本仕様を直接読むとき。
- 通知以外の UI、transport、または callback 機能のテストを探しているとき。
- 単に通常の terminal result の状態遷移を確認するだけで、通知境界の検証が不要なとき。

## hash
- 89f0cf57ba1d258d5355d60731bd03d20be0b8aaf008deeb38e0494173394cfb
