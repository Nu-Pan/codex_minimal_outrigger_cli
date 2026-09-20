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

# `_handoff_support.py`

## Summary
- handoffテストで使う項目別入力を共通形式に組み立てるヘルパーと、正本builderによる期待本文の生成入口。

## Read this when
- handoff入力の標準フィールドを使ったテストデータを作成するとき。
- handoff本文の期待値を正本builderから生成する共有処理を確認するとき。

## Do not read this when
- handoff機能本体の仕様や実装を確認したいとき。
- 個別テストの検証内容やアサーションを確認したいときは、利用側のテストを直接読む。

## hash
- 0bf82cfbb81f22d3a0345534414f77b906a61181b469c36b8a9e3d8b260afc31

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
- pytest 全体に自動適用する fixture と、送信側 TUI に結び付いた editor input handoff 用 fixture を提供するテスト共通設定。
- Windows toast の実 transport を一時ディレクトリ上の fake 実行ファイルと monkeypatch された関数へ差し替え、pytest と子 process が利用者の通知履歴へ副作用を残さないよう隔離する。
- handoff_source fixture は一時的な EditorInputHandoffSource を生成し、その MCP context を環境変数へ設定して、送信側コンテキストを必要とするテストの入口になる。

## Read this when
- テスト実行時に Windows toast 通知の外部副作用を隔離する仕組みを確認・変更するとき。
- editor input handoff の送信側 TUI context を使うテスト fixture の生成条件や環境変数設定を確認・変更するとき。

## Do not read this when
- 個別テストの検証ロジックや fixture を使わないテストの挙動を確認したいとき。
- Windows toast 実装そのものや editor input handoff protocol の仕様・実装を確認したいときは、それぞれの実装・仕様ファイルを直接読むべき。

## hash
- 89282cf36f1b504ac55859e2268d465bac3bfaa45fff87a0b807fa3532ca791f

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
- `indexing index entry` builder の parameter 構築、Structured Output schema の非空 semantic 配列制約、互換公開面を検証するテスト。

## Read this when
- indexing 用 INDEX.md エントリー生成の入力、readonly・preflight 設定、プロンプト内容、schema 制約、互換 module の公開範囲を確認したいとき。

## Do not read this when
- 実際の index entry builder の実装や正本仕様を変更・確認する場合。
- INDEX.md のルーティング規定そのものを確認する場合。

## hash
- 7c7a612ceb0fea7d93b9194617a30b8e09dc6d821a83222afc7b9f97cacb9287

# `test_acp_builder_session_join_parameters.py`

## Summary
- session join の conflict resolution builder 契約を検証するテスト
- 互換モジュールの公開 export、repo write 権限を持つパラメータ、prompt の必須方針・完了条件、競合パス内の code fence 保護を確認する

## Read this when
- session join の conflict resolution builder の公開 API やパラメータ生成契約を変更・確認するとき
- conflict resolution 用 prompt の構成、権限、実行条件、または競合パスの code fence 処理を調べるとき

## Do not read this when
- session join の通常の join 処理や conflict resolution 以外の builder を調べるとき
- builder の正本実装そのものの詳細を確認する必要があり、対応する canonical 実装を直接読むべきとき

## hash
- e2905c6eaa80aa691981e7bf3f13bbb09bd4522d617cf57ae72c86b9a367d77a

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
- Codex TUI ランタイム呼び出しの統合テストを集約し、完全な prompt と CLI 引数、アクセス境界、Codex バージョン依存の通知設定、linked worktree、エディタ入力ハンドオフを検証する。
- TUI 呼び出しの成功・CLI 不在・KeyboardInterrupt・非 0 終了時について、call log とサブコマンドイベントの保存内容、終了状態、エラー記録を検証する。
- 同一 timestamp の call log 衝突や並行 TUI 起動時の MCP 送信元・ログ対応を検証し、呼び出しごとの識別情報が混線しないことを確認する。

## Read this when
- Codex TUI の起動引数、prompt の受け渡し、sandbox/access mode、通知 hook、設定検証の順序を変更・確認するとき。
- TUI 呼び出しのログ、エラー処理、終了コード、KeyboardInterrupt、CLI 不在時の挙動を変更・調査するとき。
- TUI とエディタ入力ハンドオフ MCP の連携、linked worktree、並行実行時の call mapping を確認するとき。

## Do not read this when
- TUI 以外の Codex 実行経路だけを調べる場合は、対応する非 TUI ランタイムテストを直接読んでください。
- TUI の正本仕様や実装の詳細を確認する場合は、このテストではなく参照される oracle 文書または commons/runtime_codex_tui.py を直接読んでください。
- 共通のログ形式やエディタ入力ハンドオフ単体の仕様だけを確認する場合は、それぞれの専用テスト・実装を直接読んでください。

## hash
- fe703e36769c06d3fce3e7f9c74832fac910d8ab14119a8553a5b8df76fa5523

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
- エディタ入力ハンドオフの一時 target について、active repository に属する target のみを受理し、複数回の全面上書きでは最後の内容を確定入力にする lifecycle を検証する。
- repository 不一致、symlink 化、symlink 経由の作業ディレクトリ、未認証接続を拒否し、外部ファイルへの書き込みや入力内容の漏えいを防ぐ境界を検証する。
- 認証前後の slow-trickle 接続を絶対期限で解放し、受付済み submission の書き込み完了後に target を無効化する close/drain 動作を検証する。

## Read this when
- editor input handoff の target lifecycle、上書き、close/drain、repository/file 境界、IPC 認証または timeout の挙動を変更・確認するとき。
- prompt editor が待機中に MCP 経由の入力を受け取り、最終内容を作業ファイルへ反映する経路の回帰を調べるとき。

## Do not read this when
- 通常の対話型 editor 起動や prompt の保存・抽出だけを確認する場合は、prompt editor や TUI に直接対応するテストを読むとよい。
- Codex runtime の設定、MCP サーバー構成、または editor input handoff 以外の入力処理を調べる場合。

## hash
- 70d7456fdfe3081236df18556572098f8ef566be578c0d4321b748baf57ffc57

# `test_editor_input_handoff_mcp.py`

## Summary
- エディター入力 handoff の agent-facing MCP インターフェースを検証するテスト。
- overwrite ツールの公開、JSON-RPC/MCP 入力検証、正本 schema に基づく入力処理、送信結果と失敗状態の分類、機密入力の非漏洩を扱う。
- 実際のエディター入力 handoff の MCP 境界における受理・拒否・不確実状態と、正本 body・typed reference の生成を確認する下位テスト群への入口。

## Read this when
- エディター入力を MCP の overwrite ツール経由で受け渡す契約や回帰テストを確認するとき。
- JSON-RPC/MCP の検証、transport エラー時の status・retryable 判定、入力内容を結果へ漏洩させない挙動を調べるとき。
- handoff の canonical body、oracle reference、source metadata が反映される条件を確認するとき。

## Do not read this when
- MCP 境界ではなく、エディター入力 handoff のソケット実装や protocol 内部の仕様を直接確認・変更する場合。
- 正本 schema や canonical body の定義そのものを確認する場合は、対応する oracle ファイルを先に読むべきとき。
- MCP 以外の入力経路や一般的なエディター操作のテストを探している場合。

## hash
- 7e467bb3071796bed4bbb3341e9a4f6cd1c6b324dd318e2695505cfee58c034f

# `test_feedback.py`

## Summary
- feedback の reporter、collector、raw observation、issue candidate、remediation、active state、atomic publication、cleanup を同一 fixture で検証する統合テストの入口。
- agent-facing submission の JSON-RPC／TCP protocol、安全な UTF-8・secret masking・path 境界、rate limit、call lifecycle を確認する。
- feedback report の precondition、候補同一性、再発 threshold、wave 処理、Codex remediation、interrupt／failure recovery、active artifact 整合性を検証する。

## Read this when
- feedback observation の受付から report publication・active state 更新・raw cleanup までの一連の挙動を変更または確認するとき。
- reporter／collector protocol、context capability、durable storage、並行 call、入力検証や degraded warning の回帰を調べるとき。
- feedback report の候補 normalization、remediation、再検証、遅延 intake、run recovery、atomic publication の境界を確認するとき。
- active generation、current pointer、report cut、cleanup manifest の corruption 検出や復旧動作を確認するとき。

## Do not read this when
- feedback の個別実装や正本仕様の詳細を直接確認したい場合は、対応する runtime／subcommand 実装または oracle specification を先に読むとき。
- feedback 以外の subcommand、一般的な session／run lifecycle、または unrelated な MCP protocol の挙動だけを調べるとき。
- 単純な fixture・テスト実行方法や、テスト対象の機械的なファイル配置だけを確認したいとき。

## hash
- 033d608871a089569bf9b8dcad9159e6a69186fc980f6aff2f3462bc9aba6414

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
- `commons.indexing` の INDEX entry 生成・解析・hash 再利用・directory traversal・並列更新を、CLI lifecycle から分離して直接検証する回帰テスト。入力検証、更新失敗時の復元、symlink・特殊ファイル・memo 境界、Codex worker のログ伝播と linked worktree 間の lock 共有を扱う。

## Read this when
- INDEX entry の malformed/fresh hash 処理、semantic acceptance、render/build contract を確認するとき
- `update_indexes` の directory traversal、空 directory、memo 除外、symlink cycle、特殊ファイル、INDEX symlink 置換の挙動を確認するとき
- INDEX 更新の順序・部分書き込み復元・非祖先 directory の並列実行・pushd 中の worker 制約を確認するとき
- Codex entry 生成への対象本文や既存 INDEX の非注入、subcommand logger の伝播、linked worktree 間の indexing lock を確認するとき

## Do not read this when
- CLI の indexing subcommand lifecycle や利用者向けコマンド仕様だけを確認したいときは、CLI 実装または subcommand 仕様を直接読む
- INDEX entry のプロンプト構築そのものを確認したいときは、`build_indexing_index_entry_parameter` とその正本仕様を直接読む
- INDEX 更新以外の runtime、ログ、Git worktree の一般挙動を確認したいときは、このテストではなく該当する実装・テストを読む

## hash
- d3cf3c7f0c1a35a4bce7ef500d7ef0d2c1cc15e11ff4c2a39ca25d78b3b0af3c

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
- `cmoc oracle edit` の editor 入力確定、準備処理、2 回の agent exec、失敗時の境界、既存 Git 差分・session state・通知・レポート保持を検証する統合テスト。
- oracle edit の起動前提違反、準備失敗、builder 失敗時の後始末、およびユーザー入力・ログ参照を含む prompt の保持も検証する。

## Read this when
- `cmoc oracle edit` の実行順序、2 回の編集呼び出し、失敗時の状態保持や通知・レポートを確認または変更するとき。
- oracle edit の main worktree/session 前提、準備段階の失敗処理、editor 作業ファイルの後始末、prompt 生成を確認するとき。

## Do not read this when
- oracle edit の実装詳細そのものを確認したい場合は、このテストではなく `src` 側の oracle edit 実装を直接読むとき。
- oracle edit と無関係な CLI サブコマンドや一般的な Git・session state の挙動だけを調べるとき。

## hash
- 9ce3f0b684b4eac892a7af5ebb3d5fd7d2047abb8c254ccb9194e2ad3ef5627a

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
- 隔離した packaged layout へソースをコピーし、外部環境の影響を抑えた Python 実行によって、配布後の import 境界と公開 API を検証するテスト群。
- quota probe、oracle 編集・prompt editor 入力境界、ACP builder の正本定義再公開、cmoc config の公開面を対象に、import 成功、正本参照、`__all__`、不要な namespace 公開の不在を確認する。

## Read this when
- パッケージ化・インストール後の配置で各パッケージが import できるか確認するとき。
- realization 側が oracle 側の定義や prompt を正しく参照・再公開しているか調べるとき。
- `__all__` やモジュール namespace に意図しない内部実装が露出していないことを検証・変更するとき。

## Do not read this when
- 通常のソースツリー上での個別機能のロジックや、packaged layout を介さない単体動作を調べるとき。
- 対象テストが参照する具体的な実装仕様や正本定義そのものを確認したい場合は、対応する `src` または `oracle` のファイルを直接読むとき。

## hash
- 5a3fd1e9fcb93731b20c32bec29b248ca32a0e00092abdd08a5c7f3fad807fc3

# `test_primary_report.py`

## Summary
- 非対話末端サブコマンドの primary report 完了契約を検証するテスト。処理開始前エラー、中断、Codex 出力・feedback observation の保持、fallback report、既存 report の保全、保存未確認時の internal failure を対象とする。

## Read this when
- 非対話サブコマンドのエラー・ユーザー中断時に primary report が保存される契約を確認または変更するとき。
- primary report の front matter、サブコマンド固有フィールド、実行出力・観測結果の保持、保存失敗時の扱いを検証するとき。
- runtime_cli の terminal result 完了処理や primary report 保存基盤の回帰テストの入口を探すとき。

## Do not read this when
- サブコマンド本体の正常系処理や個別ドメインロジックだけを変更・調査するとき。
- primary report の生成仕様そのものを確認したい場合は、まず対象テストではなく対応する正本仕様や生成実装を直接読むべきとき。
- feedback observation の送信・受付仕様だけを調査し、terminal report への反映や完了契約を扱わないとき。

## hash
- b79c947a242aa1ba0becf608e296fc8ac05a47056bf2e55d30bf5e449e5ac32c

# `test_production_cli.py`

## Summary
- 実際の cmoc と Codex CLI を独立プロセスで起動し、全末端サブコマンドの本番経路を受け入れ検証するテスト。非対話系では agent call、INDEX・report、セッション／worktree の状態遷移、Git の結果を確認し、TUI 系では PTY 経由の応答完了、editor input handoff、通知、ログ連携を確認する。

## Read this when
- CLI の公開末端コマンドを追加・変更し、全末端が本番プロセス経路で実行可能か確認するとき。
- 実 Codex 呼び出しの設定、call log、実推論後の report・INDEX・Git・session・run 状態、または TUI の PTY／handoff／通知連携を変更するとき。

## Do not read this when
- CLI 内部の単体ロジックだけを確認したいときは、対応する src 側の実装や専用テストを直接読む。
- LLM の回答品質や個別サブコマンドの詳細仕様だけを調べるときは、この本番経路統合テストではなく該当する仕様・実装・専用テストを読む。

## hash
- d50163821580d7a1a1a92b17adedc1b0fc8a444604255254801a9542f234abc8

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
- prompt editor input の外部挙動を検証するテスト。可変な作業 file と保存コピーの分離、入力抽出、エディタ選択、handoff の後始末を扱う。
- 不正な skeleton、非通常 file、作業領域外 path、symlink された保存先、保存コピー先違反を拒否し、既存データを保護する境界を検証する。
- エディタ失敗や確定後の cleanup 失敗時に復旧可能な作業 file と保存記録を保持する挙動を確認する。

## Read this when
- prompt editor input の外部挙動を変更または検証するとき。
- 作業 file と保存コピーのライフサイクル、timestamp 衝突回避、最終入力の抽出を確認するとき。
- エディタ起動、handoff target、保存先の symlink 防止、path 境界、失敗時の安全性を確認するとき。

## Do not read this when
- prompt editor input の正本仕様や実装の詳細だけを確認したいとき。
- prompt editor input と無関係な機能のテストや実装を扱うとき。
- 個別のエラー実装を直接調査する場合で、まず実装または正本仕様を読む方が適切なとき。

## hash
- a6f7918e3c8933bb2863937dfe8df4bb9b3f3a8e79ac042e866b38b7ec797cb8

# `test_prompt_parts.py`

## Summary
- 各 prompt policy builder の SDPolicy 構造、カテゴリ順序、Markdown 見出しの平坦性を検証する回帰テストです。
- complete prompt の各 policy flag が対応する policy block だけを一度追加することを検証します。
- oracle、realization、feedback、editor handoff、file access、index entry、routing などの policy 内容が、正本責務・参照境界・レビュー境界・ルーティング要件を保持して render されることを確認します。

## Read this when
- prompt builder や各 policy builder の構造、カテゴリ順序、render 結果を変更するときに読みます。
- complete prompt の policy flag の有効化や、policy 文面の回帰テスト失敗を調査するときに読みます。
- SDHeader、SDPolicy、PlaceholderMap を用いた prompt 構築テストの期待値を確認するときに読みます。

## Do not read this when
- prompt builder の実装詳細を確認する場合は、対応する src 側の builder と正本仕様を直接読みます。
- INDEX.md の生成ルールそのものを確認する場合は、このテストではなく routing または index-entry の正本仕様を直接読みます。
- prompt policy と無関係な機能のテストや共通 Git fixture の挙動を調べる場合は、該当するテスト・実装を直接読みます。

## hash
- 03c14856edd5c09004c612d8611635ce040adff89e4d297d0f1099e2cae9a4f2

# `test_runtime_cli.py`

## Summary
- CLI runner の error、ログ、preflight、completion、終了通知の外部契約を検証するテスト群。共通 runner・work root・subcommand event にまたがる境界条件を一箇所で確認する。

## Read this when
- CLI の成功・失敗時に stdout/stderr へ出す terminal result、終了コード、エラー詳細、ログ記録を確認・変更するとき。
- doctor preprocess、work root 制約、pre-log check、current worktree の扱いを確認するとき。
- shell completion probe が通常の preflight・初期化・command callback・副作用を回避する挙動を確認するとき。
- TUI を含む Ctrl+C の扱い、終了通知、通知失敗時の境界を確認するとき。
- duration/timestamp の表示形式や SubcommandLogger の並列記録・UTF-8・timestamp 衝突を確認するとき。

## Do not read this when
- CLI の個別サブコマンド固有ロジックや、そのサブコマンド専用の入出力だけを確認・変更するとき。
- Codex TUI の内部実装や feedback detector 単体の詳細を直接確認するとき。
- CLI の共通 runner、終了処理、preflight、completion、ログ契約に関係しないテストや実装を扱うとき。

## hash
- ea014f2b2a6c5756d5978e08b846b21f5fe17b89821874bdf22de4a13d5be09c

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
- Codex 実行プロファイルの回帰テスト。sandbox、model/provider 上書き、MCP と環境変数、通知 hook、Codex CLI 版判定、schema 保存、出力 JSON 解析の契約を検証する。

## Read this when
- Codex 起動引数や実行環境の構築を変更するとき
- model/provider、MCP context、通知 hook、schema または output JSON 処理の回帰を調べるとき

## Do not read this when
- 正本仕様そのものを確認したいときは oracle/doc 配下の該当仕様を直接読む
- Codex 実行プロファイル以外の runtime 機能や、個別の設定値の定義だけを確認したいとき

## hash
- 8fef9d3389b47451b2310071507b40af04e7fee5458dba8e0d4bc9e98fbad7cb

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
- session fork・join・abandon の CLI 外部挙動を、session branch/state のライフサイクルとして横断検証する回帰テスト。linked worktree、state cleanup、conflict 解消、dirty worktree 拒否、競合・失敗時の rollback と報告出力を扱う。

## Read this when
- session の fork、join、abandon に関する外部挙動や session state 遷移を確認・変更するとき。
- linked worktree 対応、conflict 解消、branch/state cleanup、失敗時の復元、CLI の stdout/stderr・report 出力を検証するとき。

## Do not read this when
- session の内部実装や単一関数の仕様を直接確認する場合は、対応する session サブコマンド実装または正本仕様を先に読む。
- session 以外の CLI、一般的な Git 操作、feedback state 単体の挙動を確認する場合。

## hash
- 4f91fb472ef9369857c024c47ae72d39187f148c2d9ce7b1f51f2e8a707eb93a

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
