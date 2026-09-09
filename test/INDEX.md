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
- editing run workload の canonical builder adapter を検証するテスト。apply/refactor の builder が正本関数を再公開し、commit 参照、実行設定、prompt の規定、canonical Structured Output schema を正しく設定することを確認する。

## Read this when
- editing run 用の acp builder の互換 import 経路、prompt 構成、worktree、commit 範囲、Structured Output schema、所見の changed_paths を検証・変更するとき。

## Do not read this when
- builder の実装自体を変更する場合は、対応する realization または oracle の builder 実装を直接読むとよい。
- editing run と無関係な acp builder、または builder を利用しないテストの仕様を確認する場合。

## hash
- 7b8c305cc2e7ba8cd766c111e188bad18efb7411ec0ae321d18ad8f886a19b1a

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
- root placeholder の解決と AgentCallPathContext による repo root・work root の識別を検証する runtime 回帰テスト
- managed worktree の作成・検索・削除について、branch/path 対応、Git 登録、symlink、管理領域境界を検証するテスト入口

## Read this when
- root placeholder、相対 cwd、linked worktree、submodule、separate git directory、symlink を含む repository path 解決の挙動を確認したいとき
- cmoc 管理下の run worktree を作成・検索・削除する際の path 安全性、branch 対応、Git 登録条件を確認したいとき
- 並列実行時の process-global cwd の直列化や call 単位の path context を確認したいとき

## Do not read this when
- path 解決や managed worktree の runtime 挙動を扱わず、別の CLI 機能や個別の Git 操作だけを調べるとき
- このテストが検証する実装の具体的な仕様や内部処理を直接確認したいときは、参照元の path model・branch model・run isolation の文書や実装を読む

## hash
- 00c402d5a2ccbbf061d7f20052d1fe0ac7438f671b02a57990ce9cfc68313b4a

# `test_cli_command_tree.py`

## Summary
- oracle 変更後に公開 CLI の末端 command 集合を固定し、doctor・indexing・tui・oracle・realization・run・session・feedback の公開構成を検証するテスト。Typer/Click の help 描画互換性と feedback report の引数・固有 option 非公開も確認する。

## Read this when
- 公開 CLI の leaf command 構成が正本仕様の列挙と一致しているか確認・変更するとき。
- CLI help の Typer/Click 互換性、または feedback report の公開インターフェースを確認するとき。

## Do not read this when
- 個別サブコマンドの詳細な挙動や引数仕様を確認するときは、対応する oracle のサブコマンド仕様を直接読む。
- CLI の実装を変更するだけで、公開 command tree の回帰や help・feedback report の公開面を検証しないとき。

## hash
- 59dc9370595498819ae498ddccc3451482b821dd36870885a3e72a26866de882

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
- quota 枯渇後の Codex exec の probe・resume・再実行を検証する回帰テスト群
- 代表 quota probe の共有、失敗伝播、poll 上限、session ID 復元、ログ・cwd・CODEX_HOME 観測を扱う

## Read this when
- Codex exec の quota 待機・復帰・resume または再実行の挙動を変更・調査するとき
- quota probe の prompt、呼び出し設定、並行実行、失敗処理、実行ログの回帰を確認するとき

## Do not read this when
- INDEX エントリーのルーティングだけを確認したいとき
- quota retry 以外の Codex exec 基本仕様や、実装本体ではなく別のテスト対象を直接調べるとき

## hash
- a55306c525f326927a6d357bdbfbb0c0df6e9255dc482f519acb61d580540650

# `test_codex_runtime_retry.py`

## Summary
- Codex exec の Structured Output 補正、capacity retry、JSONL エラー、中断、成果物差分保持を、再試行状態・subprocess 呼び出し・call log・subcommand event の連鎖として検証するテスト群。

## Read this when
- run_codex_exec の出力契約違反や schema validation、capacity failure、未知の JSONL error、KeyboardInterrupt の外部挙動を確認するとき。
- Codex 呼び出し回数、同一 session の補正、retry 上限と backoff、call log および subcommand event の status・診断内容を確認するとき。
- capacity retry や Structured Output 補正の前後で agent の成果物差分を保持・復元する挙動を検証するとき。

## Do not read this when
- INDEX.md のルーティング情報だけを確認したいとき。
- Codex exec の通常成功経路や、retry・失敗・ログ・差分保持を扱わない機能を調査するとき。
- 実装本体の一般的な仕様や CLI 設定を直接確認する場合。このテスト群より run_codex_exec の実装または対応する正本仕様を読むべき。

## hash
- 92da92a517922b7f07759c9c350a0b948725f73aa4d9feba031ef993bd2faa87

# `test_codex_runtime_subprocess.py`

## Summary
- Codex subprocess と run process の停止・追跡・cleanup に関する回帰テスト群。pidfd、process group、PID 再利用、tracking file の検証、signal 処理、起動失敗時の子プロセス回収など、安全なプロセス管理の境界条件を検証する。runtime_codex_profile や runtime_run の実装変更がこの挙動へ影響する場合に、対応するテストの入口として読む。

## Read this when
- Codex subprocess の process group tracking、signal 配信、停止・reap 処理を変更またはレビューするとき
- run process tracking file の形式検証、壊れた状態、symlink・特殊 file、PID／PGID 再利用への fail-closed 挙動を確認するとき
- Codex 起動時の inherited tracking、process 起動 callback、cleanup 失敗時の子プロセス回収を検証するとき

## Do not read this when
- Codex subprocess や run process の追跡・停止・cleanup に関係しないテストや実装を扱うとき
- 正本仕様や通常の CLI 挙動を確認する必要があり、個別のプロセス管理回帰テストを直接確認する必要がないとき

## hash
- 7b84c061702ec930ad239bf4501125e2be1911a178d762b0e2e442f2cc8cd29d

# `test_codex_runtime_tui.py`

## Summary
- `run_codex_tui` の Codex TUI 呼び出しを、prompt・作業ディレクトリ・sandbox・アクセスモード・editor handoff・override 設定・call log・subcommand event の観点から検証するテスト群。
- 検証済み／未検証 Codex CLI の callback 設定、成功・CLI 不在・KeyboardInterrupt・非 0 終了時の失敗記録、および timestamp 衝突時の call log 保持を扱う。

## Read this when
- Codex TUI 実行ラッパーの引数伝達、アクセス境界、callback の有効化条件、ログやエラー記録の挙動を変更・確認するとき。
- Codex CLI の起動成功・未起動失敗・割り込み・非 0 終了を含む runtime テストの入口を探すとき。

## Do not read this when
- TUI ではなく通常の Codex 実行、prompt 生成、設定値そのもの、toast 通知、または editor handoff protocol の単独仕様を確認したいとき。
- 対象の下位ヘルパーの実装や oracle・仕様文書を直接確認すべきで、`run_codex_tui` の外部挙動を検証する必要がないとき。

## hash
- e5b6673bc8b6deaa18d0da9fb4fb5efd96def98af4ab813431bc3807b44be350

# `test_doctor_cli.py`

## Summary
- doctor preprocess の CLI と直接呼び出しに対する統合テスト。`.cmoc/gu` の ignore、`.agents`、config、refactor state の修復・commit、reporter の degraded/error 挙動、共有 repository lock、Git index の既存 staged・unstaged 差分や index flag・rename・symlink の保持と安全性を検証する。

## Read this when
- doctor preprocess の修復順序、修復 commit、config/state の生成・同期、reporter probe、lock、linked worktree の挙動を変更・調査するとき。
- doctor が呼び出し前の Git index や利用者の staged/unstaged 変更を保持できるか確認するとき。

## Do not read this when
- doctor preprocess の実装詳細そのものや正本仕様を確認することが目的で、外部挙動を検証するテストケースを読む必要がないとき。
- doctor 以外の CLI サブコマンド、feedback reporter 単体、config/state 単体の挙動を直接調査するとき。

## hash
- 305e22be5b02b487405f7da6f1165f799b953743f6f130eeee40af722f29630c

# `test_editing_run_cli.py`

## Summary
- editing run の fork と共通 lifecycle を対象に、realization apply/refactor の処理、run worktree と branch の分離、state 遷移、成果物 merge を統合的に検証する。
- Codex agent の予期しない file 変更・commit・遅延処理、INDEX 更新、process tracking、rollback、cleanup、interrupt、error report を検証する境界条件の入口となる。
- run join/abandon の正常系、force-resolve、merge conflict、cleanup 失敗、既存 resource の回収、および primary/lifecycle report の保存を確認する。

## Read this when
- realization apply/refactor fork と run join/abandon の間で共有される session state、run worktree、branch、process tracking の lifecycle を調査するとき。
- agent または INDEX refresh による想定外差分・commit、遅延 child、rename/delete、symlink、cleanup 失敗、rollback、interrupt の挙動を確認するとき。
- fork report、lifecycle report、primary report、completion reason、feedback observation の記録内容を検証するとき。

## Do not read this when
- 個別の実装関数の通常系だけを確認したい場合は、対応する commons または sub_commands 配下の実装や、より直接的な単体テストを読む。
- editing run と無関係な CLI、INDEX routing、oracle 仕様、一般的な Git 操作の挙動だけを調べる場合は、この統合テストを読まない。

## hash
- 935c80a09dfe80e477e97632f9c2c34d79c5040e1e7fdfbf7d1e2afba9c08661

# `test_editor_input_handoff.py`

## Summary
- editor input handoff target の lifecycle と、MCP submission による最終入力の全面上書きを検証するテスト。
- target ID、repository、認証済み通信、target close の境界を確認し、不正な送信や非アクティブ target を拒否する。
- editor work file とその親ディレクトリの symlink 化を検証し、外部ファイルへの書き込みを防ぐ。
- 未認証・認証済み通信の slow-trickle を絶対期限で打ち切り、後続 submission を処理できることを確認する。

## Read this when
- editor input handoff の仕様・実装を変更し、target の受付状態や close の排他・排水動作への影響を確認するとき
- MCP submission の認証、repository 一致、target ID の経路、入力内容の上書き動作を検証するとき
- editor work file の検証や symlink 対策を変更するとき
- handoff 通信の timeout、slow-trickle、後続接続の処理を確認するとき

## Do not read this when
- editor input handoff と無関係な prompt editor 機能や一般的な MCP 機能だけを変更・調査するとき
- テストが参照する正本仕様の意図や実装の詳細を直接確認する必要があるときは、正本仕様または実装対象を先に読むべき場合

## hash
- 8f8a98447d2a5bd51580e7cfcac012a4dc7281135048314ef83da3a616a861c8

# `test_editor_input_handoff_mcp.py`

## Summary
- editor input handoff の agent-facing MCP interface を検証するテスト。公開ツールの限定、JSON-RPC/MCP protocol version の扱い、入力検証、送信失敗時の状態・再試行可能性、応答フィールドの秘匿と正規化を確認する。

## Read this when
- editor input handoff の MCP interface、overwrite tool、JSON-RPC request validation、canonical input schema の公開、または transport error の状態分類を変更・調査するとき。
- 送信受付後に応答を失った場合や、送信前・送信中の失敗を agent-facing result としてどう報告するかを確認するとき。

## Do not read this when
- MCP interface や editor input handoff の挙動を変更せず、別の editor input handoff 実装、protocol、正本仕様だけを直接調査するとき。
- テスト実行方法や一般的な pytest 設定だけを確認したいとき。

## hash
- 91b93b45922d80236f8f46a2c08c7fc585b7ac345041d3c1686ee2916c9b5147

# `test_feedback.py`

## Summary
- feedback の reporter、collector、raw observation、pending intake、issue candidate、remediation、active state、report cut、atomic publication、cleanup、復旧を一体の repository fixture で検証するテスト。
- agent-facing observation submission の MCP discovery、TCP 転送、payload／collector response／context／rate limit／lifecycle の検証と、path 境界・secret masking・idempotence・不正 raw の拒否を扱う。
- feedback report の preflight、normalization／remediation prompt の安全性と processing version、candidate identity／fingerprint／collision、machine observation の threshold・window・recurrence を検証する。
- session 前提条件、修復 wave と遅延 intake、失敗時の rollback・manual completion・auto-join recovery、current pointer／generation artifact の整合性、publication 後の compact active state と cleanup failure を検証する。

## Read this when
- feedback 機能全体の外部挙動を、agent reporter から collector、report、remediation、active state 公開まで通しで確認したいとき。
- pending observation の受理・正規化・重複統合・machine threshold 判定、または report cut と current state の境界を調べるとき。
- atomic publication、generation hash、cleanup／recovery、raw artifact 検証など、report 実行失敗時の保持・復旧条件を確認するとき。

## Do not read this when
- feedback の実装詳細を直接変更・調査する場合は、対象の runtime、store、state、report、remediation 実装を先に読むべきとき。
- feedback 以外の subcommand や、単一の CLI 共通機能だけを検証したいとき。
- テスト fixture や assertion ではなく、feedback の正本仕様そのものを確認・変更したいとき。

## hash
- b5b41f732759e3a8385517e6bdd044656384913b6586ff8d0514b12ff7148481

# `test_feedback_decision.py`

## Summary
- feedback 判定の入力基礎を検証する pytest テスト。依存設定、nested realization、通常の入力ファイル、Git のモード変更を判定対象として扱う。
- Git 出力のパス検証、相対 worktree パスの正規化、nested Git 配下の非メタデータ入力の保持、検証済み nested Git メタデータの除外を確認する。

## Read this when
- feedback 判定の根拠に設定・realization・通常入力の変更が反映されるか確認するとき
- worktree_inputs の Git モード差分、nested Git 入力、Git メタデータ除外、作業ツリー外パス拒否、相対パス正規化を検証するとき

## Do not read this when
- feedback 判定実装の詳細を確認したいとき
- feedback の別機能や、このテストで扱わない CLI 挙動を調べるとき

## hash
- fc5bf49e03c544301783f2ee25cea8152ce4328137ebb9b20341ab89681b2d24

# `test_feedback_reconfirmation.py`

## Summary
- feedback.md と feedback_state.md の根拠変更・再確認・封印を、テスト用の実行環境で検証するテスト。wave の high-watermark 連続性、依存変更や機械的同期後の再確認、追加証拠の取り込み、修復サイクルの収束、checkpoint 参照復旧、封印後の不正な公開・復旧拒否、active issue の decision basis 具体化を扱う。

## Read this when
- feedback remediation の結果が依存ファイル変更や生成物同期をまたいで再確認される条件を確認したいとき。
- 観測証拠・checkpoint・sealed result・active issue の根拠が、公開や復旧の可否にどう影響するかをテストから確認したいとき。
- feedback の wave 境界、再修復サイクル、参照復旧の回帰ケースを変更・調査するとき。

## Do not read this when
- feedback の実装ロジックそのものを変更・理解することが目的で、テストケースの期待挙動を確認する必要がないとき。
- 一般的な issue 受付や remediation の初期入力形式だけを確認したいときは、対応する実装または基礎テストを直接読む。

## hash
- bc8c252849f99c19ef9199bace74a387b79a66e3768ad99ade03cb9b7dcc5364

# `test_file_inventory.py`

## Summary
- oracle・realization file の full-tree 列挙と refactor state 同期を検証するテスト。
- Git ignore、nested repository、linked worktree の metadata 境界を含むファイル分類を扱う。
- symlink、FIFO、socket、device などの非通常パス拒否と、候補数増加時の Git 処理量不変性を検証する。

## Read this when
- oracle・realization file の列挙対象、除外境界、Git ignore 判定、または refactor state の SHA 更新を確認するとき。
- nested repository や linked worktree を含む実ファイル分類の挙動を確認するとき。
- 列挙処理が非通常パスを拒否し、候補数に対して一定の Git 処理量を保つことを検証するとき。

## Do not read this when
- 列挙処理の正本仕様や実装の詳細を確認したい場合。
- このテストが扱う列挙・分類・state 同期以外の機能を調べる場合。

## hash
- b4efe4647289425b8ce87f82a78629b81640850bd7e750e4799ac2715559b9ef

# `test_indexing_cli.py`

## Summary
- `cmoc indexing` の CLI と indexing preflight の外部挙動を検証するテスト。doctor による未初期化リポジトリの準備、通常および linked worktree の対象判定、dirty 状態の拒否、worktree 固有設定の利用、fresh hash の再生成省略を扱う。
- INDEX.md 更新結果を Codex の Structured Output から反映し、INDEX パスだけを commit して報告する lifecycle と、Git diff 異常時・既存非 INDEX 差分時の失敗境界を検証する。

## Read this when
- `cmoc indexing` の実行前提、worktree 選択、preflight、Codex index-entry builder 呼び出し、INDEX.md 更新、commit、または完了レポートの挙動を変更・確認するとき。
- indexing が staged・unstaged の既存差分を保持しつつ INDEX.md だけを commit する条件や、fresh hash による再実行省略を検証するとき。

## Do not read this when
- indexing の正本仕様や CLI 仕様そのものを確認する場合は、まず oracle の indexing 仕様文書を読むとよく、このテストは実装された外部挙動の検証が必要な場合に限る。
- index-entry Structured Output の項目や schema を変更・確認するだけの場合は、専用 schema を直接読む。
- indexing 以外のサブコマンド、または INDEX 更新を伴わない一般的な Git commit 挙動だけを扱う場合。

## hash
- 03b7ee990d53a5d2f32d12008f813a4ad85ee4d2aab44243dcd732bc15702163

# `test_indexing_common.py`

## Summary
- `commons.indexing` の INDEX entry 生成・解析・更新を直接検証する runtime 回帰テスト。入力検証、malformed entry の再生成、hash 一致時の再利用、更新失敗時のロールバックを扱う。
- directory traversal の境界と更新順を検証する。空ディレクトリ、nested memo、symlink cycle、INDEX symlink、特殊ファイル、非 UTF-8 名、linked worktree の lock、非祖先ディレクトリの並列更新、worker logger 伝播を対象とする。

## Read this when
- `commons.indexing.update_indexes`、`render_index_entry`、`index_target_hash`、`target_content_for_indexing`、`indexing_lock_path` の挙動を変更・調査するとき
- INDEX 更新の並列化、cwd lock、symlink・特殊ファイル処理、hash の安定性、Codex event ログ、部分書き込み復元を確認するとき

## Do not read this when
- CLI lifecycle や indexing サブコマンド全体の仕様・統合動作だけを確認する場合
- INDEX entry の作成条件や traversal 方針の正本仕様を確認する場合は、参照されている app specification と schema を直接読むとき

## hash
- c8f16cdab76a8b0ac23b7144068a0ee4e6fc3f66db049e90da9f94c212a10473

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
- `cmoc oracle edit` の main worktree exec 制御を、成功時と main/reduction 失敗時の共通制御テストで検証する。
- editor 入力、2 回の agent call、indexing preflight、Git 差分、session state、通知、レポートの境界を比較する。
- oracle edit の skeleton 構築失敗と、linked worktree・非 session branch・inactive session による起動前提違反も検証する。

## Read this when
- `cmoc oracle edit` の main worktree 実行順序や、成功・各失敗時の agent call 制御を確認したいとき。
- oracle edit が既存の staged/unstaged 差分、session state、editor work file、通知、診断レポートをどう保持・後処理するかを確認したいとき。
- oracle edit の起動前提違反や skeleton 構築失敗時の利用者向けエラー境界を確認したいとき。

## Do not read this when
- oracle edit 本体の仕様や実装を直接確認したいときは、oracle の sub-command 仕様または launch exec 実装を読む。
- 一般的な Git 差分保持や session state の共通処理だけを調べるときは、それぞれの共通機能のテストまたは実装を直接読む。
- INDEX.md の構造や対象ファイルの機械的な所在だけを確認したいとき。

## hash
- bd21ee389d0615a346965d42d296d126cb537152209f1a8a6038cbf29f990fbb

# `test_oracle_investigation_cli.py`

## Summary
- `oracle investigation` CLI の起動条件と、doctor・prompt editor・builder・preflight・TUI の連携順序を検証するテスト。
- セッションなしの main worktree での起動、生成される launch parameter、editor 入力の反映、作業ファイルの後処理を検証する。
- investigation の launch TUI realization adapter が builder だけを公開し、補助名を公開しないことを検証する。

## Read this when
- `oracle investigation` の起動前処理、prompt editor 入力の受け渡し、indexing preflight、または TUI 起動パラメータの挙動を変更・確認するとき
- investigation の launch TUI builder の公開範囲や `__all__` の契約を変更・確認するとき

## Do not read this when
- oracle investigation の一般的な調査手順や本体仕様だけを確認したいとき
- doctor、prompt editor、indexing preflight、または TUI の個別実装を直接変更・確認するため、対象実装の専用テストや仕様を読むべきとき

## hash
- a8b2aeef3e6f800b29529e71a45bcc28ad7c351401fa68780d0211bb950932c7

# `test_packaged_import.py`

## Summary
- packaged layout 上で主要パッケージを隔離実行し、正本 builder・prompt editor・ACP basic・cmoc config の import 境界、公開 API、設定参照、および prompt 生成を検証するテスト。

## Read this when
- packaging 後の import 経路、setuptools の package 配置、oracle と realization の公開定義の再公開境界を変更・確認するとき。
- quota probe、oracle edit、prompt editor 入出力、ACP basic、cmoc config の packaged layout 上の挙動や module namespace を検証するとき。

## Do not read this when
- packaged layout や import 境界に関係しない単一機能の実装・テストを扱うとき。
- 正本 builder や prompt editor の仕様そのものを確認する必要があり、対応する oracle source または app specification を直接読むべきとき。

## hash
- 824bdbfcc2443bd379c5d5d83d3508e14c8f6565cf2926afd34df97f6f351e88

# `test_primary_report.py`

## Summary
- 非対話末端サブコマンドの primary report 完了契約を検証するテスト。処理開始前エラー、中断、Codex 出力・受理済み observation の保持、refactor 中断理由、未保存 report の内部失敗化を確認する。

## Read this when
- runtime_cli の各サブコマンドで、エラーや中断時の primary report 保存契約・front matter・診断ログを確認または変更するとき。
- primary report と fallback report に実行出力や feedback observation を残す挙動、report 保存失敗の terminal result を検証するとき。

## Do not read this when
- primary report の生成・完了契約ではなく、個別サブコマンドの通常処理やドメインロジックだけを確認するとき。
- テスト実装の詳細ではなく、根拠となるアプリケーション仕様そのものを確認したいとき。

## hash
- 52290834aa28f4c4deaccbd6095641cb8fa31025e9fc4b8ebc5e951425c0af99

# `test_production_cli.py`

## Summary
- 全末端サブコマンドを、利用者向け console script・実 Codex CLI・実推論・独立 process の本番経路で受け入れ検証する統合テスト。
- 非対話コマンドでは終了 code、Codex call log、prompt/config、INDEX.md・report・session/run state・Git の外部状態遷移を確認し、Codex 不要経路の agent call 不発も検証する。
- TUI コマンドでは実 PTY と Codex 応答完了までの経路を使い、端末 query 応答、完了応答、終了、TUI call log、Git 非変更を確認する。
- Click に登録された末端コマンド集合と固定シナリオの一致を検査し、新しい公開末端の本番経路試験への追加漏れを検出する。

## Read this when
- CLI の全公開末端が独立 process と実 Codex CLI を通る本番経路で検証されているか確認したいとき。
- indexing、oracle edit、feedback report/remediation、realization の run、session fork/join/abandon の状態遷移や call log 契約を調べるとき。
- tui または oracle investigation の実 PTY 操作、応答完了判定、終了処理、Git 非変更を確認するとき。
- 新しい末端サブコマンドを追加し、受け入れシナリオ集合の更新要否を確認するとき。

## Do not read this when
- 個別サブコマンドの通常の単体仕様や内部実装を直接確認したいときは、それぞれのサブコマンド仕様・実装・専用テストを読む。
- LLM の回答品質やプロンプト内容そのものを評価したいとき。
- 実 Codex や PTY を使わない高速なユニットテスト、fixture、共通テスト補助の挙動だけを調べるとき。

## hash
- 4f27b1f1abe154d220aa69a2554608d9722ec9c0c27b395304972af6eff0b27f

# `test_production_cli_support.py`

## Summary
- 実経路統合テストで使用する PTY 操作 helper の trust 確認処理を検証するテスト。プロンプト検出直後では確定せず、次の poll で確認入力を送信する挙動を扱う。

## Read this when
- 実経路統合テストの PTY 操作 helper が、trust prompt 検出後の poll 間隔と確認入力の送信タイミングを満たすか確認するとき。

## Do not read this when
- trust 確認処理そのものの実装や本番 CLI の挙動を調べるときは、対応する実装または本番 CLI のテストを直接読む。

## hash
- d9d566558ddab2d388a8d45f171c1dbdf7a3bd90ce5e50bc62140d9f769d24e3

# `test_prompt_editor_input.py`

## Summary
- prompt editor input の予約・編集・最終収集・確定処理を、保存先の分離、入力抽出、editor 選択、異常系の安全性までテストする。

## Read this when
- prompt editor input のファイル配置、timestamp 衝突回避、skeleton の placeholder 検証、editor 起動引数、最終入力の収集、異常時の作業 file 保持を確認・変更するとき。

## Do not read this when
- prompt editor input の実装や正本仕様そのものを直接確認すれば足り、テストケースの期待挙動や回帰検証を調べる必要がないとき。

## hash
- d24e3977dcebff440617ed12b59c88e3dc47a000b3b9dd51cff790ef84f7f81c

# `test_prompt_parts.py`

## Summary
- prompt part の rendering と complete prompt の組み立てを検証する回帰テスト。各 policy のカテゴリ順序・重複防止・内容境界、objective と動的セクションの配置、placeholder 展開、file access mode ごとの制約、INDEX 案内要件を確認する。

## Read this when
- prompt builder の policy、prompt part、complete prompt の構成や rendering を変更・調査するとき
- prompt の placeholder、objective、policy 注入、file access 境界に関する回帰を確認するとき
- prompt builder 関連のテスト失敗から、期待される出力構造や policy の責務を確認するとき

## Do not read this when
- prompt builder の実装詳細そのものを確認したい場合は、対応する oracle の仕様や prompt_builder 実装を直接読むとき
- prompt builder と無関係なテストや、単一 policy の仕様本文だけを確認する場合
- INDEX.md エントリーの出力形式だけを確認する場合

## hash
- 96c97bd4148c1594d5e3c06203519cd3799bd4d3f3819edd77f4327de02593da

# `test_runtime_cli.py`

## Summary
- CLI lifecycle における error report、console/file log、preflight、completion、終了通知の共通契約を検証するテスト群。
- 共通 runner を通じた成功・handled failure・internal failure・非0終了・ユーザー中断の表示、ログ記録、終了コード、通知境界を確認する。
- work root 制約、doctor preprocess、pre-log check、shell completion probe、TUI 起動前後の Ctrl+C を調査するための横断的な入口。

## Read this when
- CLI の stdout/stderr 形式、error report の簡潔さ、traceback の扱い、終了コードを確認したいとき
- サブコマンドログの生成・イベント分類・flush failure 耐性や terminal notification のタイミングを確認したいとき
- doctor preprocess、pre-log check、work root 判定、completion probe の副作用抑制、TUI の中断境界を調査したいとき

## Do not read this when
- 特定サブコマンドの内部処理や個別 runtime モジュールの実装詳細を直接調べるとき
- CLI lifecycle の共通外部契約ではなく、Codex subprocess の単体挙動、git 操作、設定値、個別のエラーモデルだけを確認するとき

## hash
- 0b11f2c5fa5c56f454f81867e5829917baf0820e3752fa8a8d21425bcc2e0aa8

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
- Codex argv の model・sandbox・provider 上書きと、関連する MCP／環境変数／hook／TUI 通知設定を検証する realization test。Codex 起動前の設定検証、schema 保存、output JSON 読み取りの境界も扱う。

## Read this when
- Codex の file access mode から sandbox への変換、model/provider の選択・TOML エンコード、未定義設定の拒否を変更または確認するとき。
- feedback や editor input handoff の MCP 注入、call context の環境変数分離、SessionStart hook と legacy notification callback、Codex CLI バージョン検証を変更または確認するとき。
- schema のバイト保持・ハッシュ保存や、不正 UTF-8 output の扱いを変更または確認するとき。

## Do not read this when
- Codex argv の構築や runtime_codex_profile の境界挙動を扱わず、他の runtime 機能だけを変更・確認するとき。
- 実装ではなく、Codex の一般的な仕様や oracle 文書そのものを確認するときは、参照先の正本を直接読むとき。

## hash
- bc202c6e31be5faa64b96036c718758c2b2a675d3001f7f09acddd10437c09fa

# `test_runtime_config.py`

## Summary
- CmocConfig の既定値、JSON 変換・ファイル永続化、merge、入力検証、互換性のない旧設定の除外を一つの回帰テストとして検証する。

## Read this when
- 設定 schema の既定値や agent call の直接設定を変更するとき
- config.json の読み書き、JSON/TOML 共通値、パスの安全性、入力拒否、利用者向け設定エラーを変更するとき
- 旧 config 項目の互換性や公開 JSON 面への影響を確認するとき

## Do not read this when
- 設定処理ではなく、agent call の実行、doctor の一般的な動作、または設定以外の CLI 機能を変更・調査するとき
- CmocConfig の実装詳細や正本仕様そのものを確認する必要があり、対応する実装・仕様ファイルを直接読むべきとき

## hash
- 19e86b83909fb434f6c56699046b9d2c27ed4d8bab76595d9c04d09443cd6dbf

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
- realization refactor の永続 state が oracle・realization の正確な file 集合を追跡し、調査履歴と変更時の再調査状態を同期する挙動を検証する。
- state の schema、path・timestamp の正規性、symlink・特殊 file・Gitlink・path escape の拒否、および未調査・最古優先の target 選択を検証する。

## Read this when
- realization refactor の state 同期、読み書き検証、対象 file の分類、調査対象の選択規則を確認または変更するとき。
- oracle・realization file 集合の境界や、work-root 外・非通常 file を拒否する安全性を確認するとき。

## Do not read this when
- realization refactor 以外の state や target 選択を扱うとき。
- 実装の一般的な Git 操作や、正本仕様そのものの内容を確認したいときは、対応する実装または oracle 文書を直接読む。

## hash
- 38f5711945036ec1c4eea0b53c619ce48280235966e65cf1b46c47deeb8b4e2e

# `test_runtime_state.py`

## Summary
- session/run state の永続化 schema と managed branch 解析を検証する realization test。branch 名の canonical 形式、state payload の型・必須項目・未定義 field、JSON 読み込みエラー、通常 file と symlink の扱い、session 部分の部分検証、session fork lock の process 間共有を扱う。

## Read this when
- session state または run state の schema、保存・読み込み、branch からの state 解決を変更・レビューするとき
- managed branch の命名規則や session/run の識別子解析を変更するとき
- state file の path 安全性、JSON エラー変換、symlink・directory の拒否を確認するとき
- session fork lock の process/thread 間同期動作を変更・検証するとき

## Do not read this when
- CLI 出力や session/run state 以外の永続化を変更するとき
- state schema の実装詳細ではなく、正本仕様そのものを確認するときは oracle の session state 文書を直接読む
- branch 操作や lock 機構に関係しないテスト・実装を調査するとき

## hash
- 7704ec65a7ccb2ca1eb887987ff4d0658a605fdc0e76abf1e7cb8cb20e30980e

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
- Windows toast通知の端末結果表示とPowerShell transportを検証するテスト。通知内容を短く制限し、JSON stdinによる安全なデータ受け渡しと通知失敗の非伝播を確認する。
- Codex TUI callbackのroot session記録、turn単位の重複排除、入力待ち通知、standalone hookの実行とinvocation終了時の状態破棄を検証する。

## Read this when
- Windows toast通知の表示内容、transport境界、失敗時の扱いを変更・確認するとき
- Codex TUI callbackやSessionStart hookのsession判定、重複通知防止、状態管理、standalone実行を変更・確認するとき

## Do not read this when
- 通知の正本仕様や利用者向け要件を確認したいとき
- Windows toastやCodex callback以外のruntime機能を調べるとき
- 実装ではなく一般的なpytest実行方法だけを確認したいとき

## hash
- ea5cc7268e5c77efed80f70cdaefe4beaf69f9e4aea734755736b3d8b040e0ef
