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
- Codex 実行関連テストで共有する test double、環境変数付きの一時 Codex 環境、既定パラメータ生成、CLI 引数・設定値の解析、Codex override の stub を提供するテスト支援モジュール。

## Read this when
- 複数の Codex runtime・CLI・indexing テストで共通するセットアップ、引数検証、結果 double、または subprocess 用 override を確認・変更するとき。

## Do not read this when
- 個別テストの業務ロジック、検証対象の CLI 挙動、または本番実装そのものを確認したいときは、利用元のテストや対応する src ファイルを直接読む。

## hash
- 143fb59f7aea70bdf2acb90fdf4cd24e8d1b4f0481ef54983bbfe88dce60d482

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
- 固定された TUI 起動パラメータ、実行ポリシー、prompt 内の objective/original-prompt 配置を検証するテスト。
- 互換 TUI モジュールが現行の builder 関数だけを公開し、正本 builder と同一関数を参照することも確認する。

## Read this when
- TUI 起動 builder の固定設定、ファイルアクセスモード、MCP・索引付け設定、prompt の構成や完了条件を変更または確認するとき。
- 互換モジュールの公開 API や builder 関数のエクスポートを変更するとき。

## Do not read this when
- TUI 起動パラメータや互換モジュールの公開面に関係しない ACP Builder 機能を調べるとき。
- prompt の内容・構造や TUI builder の公開 API を確認する必要がなく、正本実装または別のテストを直接読むべきとき。

## hash
- e60167087fe0542be76036687c3caf8679ddbe8bc90fbaefe0fb27ac2c1a6a97

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
- TUI 起動前の CLI 前処理を外部挙動として検証するテスト群。
- エディタ入力の保存・編集済みプロンプトからの Codex TUI 起動・生成パラメータ・処理順序を検証する。
- linked worktree 使用時のメイン worktree へのログ保存、agent call context、`.cmoc` の ignore 設定を検証する。

## Read this when
- `tui` サブコマンドの起動順序、エディタ入力、プロンプト生成、Codex TUI 呼び出しの期待動作を確認したいとき
- linked worktree から TUI を起動した場合のログ配置や実行コンテキストを確認したいとき
- TUI 実行時にリポジトリ差分を保持し、`.cmoc/gu` を Git 管理対象外にする挙動を確認したいとき

## Do not read this when
- TUI 以外の CLI サブコマンドや一般的なプロンプト生成の挙動を確認したいとき
- TUI の実装詳細や正本仕様そのものを確認したいときは、対応する `src` または `oracle` の対象を直接読むべきとき

## hash
- 76a5fc11a8af047b30c939fdd66e7eadf8ae78b3fc8343d70b8da0a98b89016d

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
- Codex exec の Structured Output 検証失敗、capacity retry、JSONL エラー、中断、成果物差分復元を、再試行状態・subprocess 呼び出し回数・call log・subcommand event の一連の外部挙動として検証するテスト。

## Read this when
- Codex runtime の再試行や出力補正の挙動を確認・変更するとき。
- 出力契約違反、非有限数、不正 JSON、欠落出力、capacity failure、未知の JSONL error、中断、補正時の成果物変更に関する回帰を調べるとき。
- Codex call log の内容、session の継続、イベント status、成果物差分の保持・復元を検証するとき。

## Do not read this when
- retry や失敗時ログを伴わない Codex runtime の機能だけを確認するとき。
- INDEX 生成そのものや、Codex 呼び出し以外の機能を調べるときは、対象実装または専用の別テストを直接読むべき。

## hash
- 3ec06dc112de46898f9d78000d0ce485366e98071ea35ea07e1261d266fa95db

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
- Codex TUI 実行の統合テストを担い、完全な prompt と CLI 引数、アクセスモード、通知フック、設定検証順序、補完時の挙動を検証する。
- TUI 呼び出しの成功・CLI 不在・KeyboardInterrupt・非ゼロ終了時について、call log とサブコマンドイベントの記録およびエラー報告を検証する。
- linked worktree と並行実行時の editor-input handoff、呼び出し識別子、ログ対応、MCP へのコンテキスト伝達を検証する。
- TUI ランタイムの外部から観測可能な実行契約を横断的に確認する入口であり、単一の補助関数や個別のログ形式だけを調べる場合の対象ではない。

## Read this when
- Codex TUI の prompt・CLI 引数・sandbox・通知設定・フック設定の受け渡しを確認または変更するとき。
- TUI 実行前の設定検証、Codex version probe、シェル補完時の分岐を確認するとき。
- TUI 呼び出しの成功・失敗・割り込み時に、call log とサブコマンドイベントがどう記録されるかを確認するとき。
- linked worktree、editor-input handoff、並行 TUI 実行の識別と MCP 連携を調査するとき。

## Do not read this when
- TUI 以外の Codex 実行経路や、単独の設定・ログ・editor-input handoff 実装の内部仕様だけを調査するときは、対応する実装または専用テストを直接読む。
- TUI の実行契約や失敗時の記録、並行 handoff の対応関係を確認する必要がない単純なテスト探索では、この統合テスト全体を読む必要はない。

## hash
- efe03d1ff8bd413810a5dcb72c452b37c9b6a4c4d52a40616d729a07720a2b56

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
- 編集実行 run の統合ライフサイクルを検証する realization テスト。session/run の fork・state 遷移・worktree と変更パスの扱い、apply/refactor の処理単位、index 更新、agent 変更検査、join/abandon、rollback・cleanup・process tracking、report と警告、割り込み・失敗からの復旧までを共通 fixture として扱う。

## Read this when
- 編集実行 run の開始から完了・join・abandon・rollback までのライフサイクルを確認するとき
- apply または refactor の fork、index 更新、変更パス検査、report、cleanup、子プロセス停止の回帰条件を調べるとき
- session branch・run branch・worktree・state の相互作用や、失敗・割り込み後に joinable/error state へ遷移する条件を確認するとき

## Do not read this when
- 編集実行 run の実装仕様そのものを確認したい場合は、参照される realization 実装や oracle 文書を直接読むとき
- 個別の CLI サブコマンドの単純な引数解析・表示だけを調べるとき
- 対象ファイル内の具体的なテストケースや期待値を確認したい場合は、この案内ではなく対象ファイルを直接読むとき

## hash
- 86847e9625e22ae03d30c5fb610e97d3ae3ee861990eb5bb8c35025e7bfc053f

# `test_editor_input_handoff.py`

## Summary
- エディター入力ハンドオフのライフサイクルを検証し、アクティブな対象への最終上書き、終了後の拒否、受付済み処理の完了待ちを扱う。
- リポジトリ不一致、symlink 経由の外部ファイル上書き・削除、認証前の入力送信を拒否する安全性を検証する。
- 未認証・認証済み接続の slow-trickle に対する絶対期限と、その後の新しい submission の処理継続を検証する。

## Read this when
- エディター入力ハンドオフの受付・終了・上書き境界に関する回帰条件を確認するとき。
- 対象 ID、リポジトリ検証、ファイル／ディレクトリの symlink 安全性、認証前の機密入力保護を確認するとき。
- 接続の認証、タイムアウト、slow-trickle 攻撃への耐性と、期限後の処理継続を確認するとき。

## Do not read this when
- エディター入力ハンドオフの実装詳細を確認したいときは、対応する src 側の実装を直接読むとき。
- 正本仕様の要求内容を確認したいときは、参照されている oracle の仕様ファイルを直接読むとき。
- 一般的なプロンプト編集処理やハンドオフ以外のテストを調べるとき。

## hash
- d8b41142a3d7f7d030bd83bacd50559891e9668fa3f96690a6680c87d7e70842

# `test_editor_input_handoff_mcp.py`

## Summary
- エディター入力ハンドオフ用 MCP インターフェースのテスト。ガイド取得と上書きツールの公開範囲・正本 schema、JSON-RPC/MCP パラメータ検証、入力やエディター内容の漏えい防止、送信前後の transport failure の不確実性、source 検証、正規化された本文生成、対象ファイルを変更しない失敗処理を検証する。エディター入力ハンドオフの agent-facing API 挙動を確認するためのテスト入口。

## Read this when
- エディター入力ハンドオフ MCP のツール一覧・protocol negotiation・入力検証を確認または変更するとき。
- ガイド取得や上書き送信で、private input／エディター内容の漏えい防止、失敗状態、再試行可能性を確認するとき。
- ハンドオフ本文の canonical formatting、typed document references、source metadata の受け渡しを確認するとき。

## Do not read this when
- MCP ではないエディター入力ハンドオフの内部実装だけを調べるときは、runtime や protocol の実装を直接読む。
- エディター入力以外の MCP ツール、一般的な JSON-RPC 処理、または別の本文生成機能を調べるときは、それぞれの専用テスト・実装へ進む。

## hash
- 2827a0446c001fcab1789ba5026e6a1120ed43e24cc81ea7df2e70444a0a4843

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
- `cmoc oracle investigation` が session なしの main worktree で起動する一連の CLI フローを検証する。doctor 前処理、prompt skeleton 生成、エディタ入力の保存・収集・確定、実行用 parameter 生成、TUI 起動順序と各引数・副作用を確認する。
- oracle investigation の realization adapter が公開する API を検証し、builder 関数だけを `__all__` とモジュール名前空間へ公開することを確認する。

## Read this when
- `cmoc oracle investigation` の起動前処理、エディタ入力 handoff、prompt 合成、TUI 起動条件、parameter 設定を変更または回帰調査するとき。
- oracle investigation の launch TUI adapter の公開 API や不要な公開シンボルを確認するとき。

## Do not read this when
- oracle investigation の正本仕様そのものを確認・変更するときは、列挙された oracle 文書を直接読むべきである。
- CLI の一般的な実装、doctor 処理、prompt editor の内部処理だけを調査する場合は、それぞれの src 実装や専用テストを直接読むべきである。

## hash
- 02f09c17909e0dc649b4661559137a264af23c7370ff86971c6a67fd09e6fd39

# `test_packaged_import.py`

## Summary
- 対象は、インストール済みパッケージとしての import が実行環境や作業ディレクトリに依存せず成立することを検証するテストです。
- パッケージング後のモジュール解決や配布物からの読み込みに関する問題を調べる際の入口になります。

## Read this when
- パッケージをビルド・インストールした後の import 成否、または配布物に必要なモジュールが含まれるかを確認するとき。
- パッケージ構成やインストール経路の変更が、この import 検証に影響するか判断するとき。

## Do not read this when
- 通常のソースツリー内での import、個別機能の動作、または他のテストの失敗を調べるだけの場合。
- 配布物の生成手順やメタデータそのものを確認する必要があり、まずパッケージ設定・ビルド定義を直接読むべき場合。

## hash
- a4004f137b12a3d345ce31d64fa39b3a19dc1174de39be98ef2be78c67363bec

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
- 利用者向け `cmoc` console script を独立 process で起動し、非対話の全末端サブコマンドと PTY 上の TUI 末端を、実 Codex CLI・実推論・隔離環境で検証する受け入れテスト。終了コード、call log、report、session/run state、Git 状態、INDEX 更新、PTY 応答完了と終了処理まで確認する。

## Read this when
- CLI の末端サブコマンド追加・変更が本番相当の独立プロセス経路、実 Codex 呼び出し、状態遷移、Git・report・INDEX の外部結果に与える影響を確認したいとき。
- TUI の PTY 起動、端末 capability query、信頼確認、実 Codex 応答完了、終了操作の統合挙動を調査したいとき。
- Codex 呼び出し設定、prompt の引き渡し、call log、feedback remediation の本番経路を検証したいとき。

## Do not read this when
- 個別サブコマンドの単体ロジックや内部関数だけを確認したいときは、対応する実装テストや仕様を直接読む。
- LLM の回答品質や prompt 内容そのものの妥当性を評価したいときは、このテストでは判定対象外のため、該当する仕様・専用テストを読む。
- 実 Codex CLI や PTY を使わない高速な正常系・異常系の検証だけが必要なときは、この本番経路受け入れテストを起点にしない。

## hash
- 35c274f4d232487f24897917497b2a7868e406577f81f03d1c9b43fd177cc5e7

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
- プロンプト編集用の作業ファイルと保存コピーの分離、衝突回避、最終入力の単一読み取りを検証するテスト。
- エディタ選択の優先順位と `code` 使用時の待機オプションを検証するテスト。
- 作業ファイル・保存先のパス境界、通常ファイル性、シンボリックリンク経由の保存、保存コピーの安全性を検証するテスト。
- handoff target の後始末、エディタ失敗時や確定後の削除失敗時に復旧可能な作業ファイルを保持する挙動を検証するテスト。

## Read this when
- プロンプト編集フローのファイル保存、入力抽出、エディタ起動、handoff の終了処理を変更・レビューするとき
- 作業ファイルや保存コピーへの不正なパス、シンボリックリンク、ファイル種別変更に対する安全性を確認するとき
- エディタ失敗時・後始末失敗時の復旧可能性や回帰テストの期待値を確認するとき

## Do not read this when
- プロンプト編集の実装詳細だけを調査し、テストが定義する外部挙動や安全境界を確認する必要がないとき
- handoff MCP の通信プロトコルや CLI 全体の統合動作を直接確認したいときは、それぞれの専用テストを読むとき

## hash
- c71cacb86ebb61aca7395cb753c5cc4ce42921346f3207e1a8a3225ecbf72e07

# `test_prompt_parts.py`

## Summary
- prompt 部品と complete prompt の組み立て結果を検証する回帰テストです。各 policy builder のカテゴリ構造・順序・本文、policy flag による挿入、objective や placeholder の展開、file access mode ごとの境界、linked worktree の一貫性を対象にします。
- プロンプト生成実装や正本仕様の変更が、render 結果・policy の注入・ファイル分類およびアクセス制約に与える影響を確認するテスト入口です。

## Read this when
- prompt builder の policy 部品、complete prompt の構成、flag による policy 挿入を変更・調査するとき。
- placeholder、objective の省略・順序、root 定義の統合・競合、prompt render 結果の回帰を確認するとき。
- file access policy、oracle/realization の分類境界、editor handoff、routing policy の出力を検証するとき。

## Do not read this when
- prompt builder の実装詳細や正本仕様そのものを確認したい場合は、対応する src または oracle 側の対象を直接読むべきです。
- prompt 部品以外の機能テストや、単にテスト実行方法だけを確認したい場合。

## hash
- 2330cc39b839ccb18243aaf7a11b30cd967363a13bb5efbd3f144c42959a3594

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
- Codex 起動時の argv・sandbox・model/provider・MCP・hook 上書き契約を検証する回帰テスト群。
- Codex subprocess 環境の call context 分離、検証済み CLI バージョン判定、schema 保存と出力 JSON 読み取りの失敗処理も対象とする。
- Codex プロファイル構築の入力検証や provider 設定の TOML エンコードを確認したい場合の入口となる。

## Read this when
- Codex 起動引数や sandbox、model/provider の上書き仕様が変更されたとき。
- feedback・editor input handoff MCP、SessionStart hook、legacy notification callback の連携を確認するとき。
- Codex CLI バージョン判定、schema のハッシュ保存、出力 JSON の異常系を回帰確認するとき。

## Do not read this when
- 通常のランタイム実装の詳細を調べるときは、対応する src 側の runtime_codex_profile 実装を直接読むとき。
- Codex の正本仕様や要求理由を確認するときは、参照されている oracle/doc の仕様を読むとき。
- Codex プロファイル以外の機能やテスト fixture の挙動だけを調べるとき。

## hash
- 8f7ee1e5010db8e559f8c77556f7bf7bde5ab2068620ff79392f574671bf6ca5

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
