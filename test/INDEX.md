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

# `_apply_support.py`

## Summary
- apply session state の apply_branch を検証し、管理対象 worktree のパスを組み立てるテスト用補助関数。セッション状態から production worktree を解決する処理の入口。

## Read this when
- apply session state から managed worktree のパスを導出する処理や、その入力検証を確認するとき。

## Do not read this when
- session state の仕様自体を確認するときは、参照される oracle 文書を直接読む。
- worktree 解決以外のテスト支援処理を確認するとき。

## hash
- ad8de2962ec0f4ac6ed391bc83eabcb7ba5cfac37c0930ea94394610f36e4d82

# `_cli_support.py`

## Summary
- Typer CLI テストで共有する CliRunner インスタンスを提供する補助モジュール。CLI テストの実行入口として参照する。

## Read this when
- Typer CLI のテストを追加・修正し、CliRunner を使った実行が必要なとき

## Do not read this when
- CLI テスト以外の実装やテストを扱うとき
- CliRunner を使わないテストの挙動を確認するとき

## hash
- f8067659d5647e5eb7180b42c0741136aba6b2baf99cf70dd459a35da30d4d12

# `_codex_support.py`

## Summary
- Codex 実行ラッパーのテストで共有する補助関数と最小 fake result を定義する。認証済み Codex home、managed Ollama preflight の無効化、既定パラメータ生成、CLI 引数・設定 override の検査、Codex override argv の固定化を提供するテスト用入口。

## Read this when
- Codex subprocess の argv 構築、config override、cwd・file access mode、runtime wrapper のテストを追加・変更するとき。
- Codex 実行テストで一時的な CODEX_HOME や共有 service の stub が必要なとき。

## Do not read this when
- Codex 実行ラッパーの本体実装や正本仕様を確認する作業。
- Codex と無関係なテスト、またはこの共有テスト helper を利用しないテスト。

## hash
- 14ff0ed40e6128820d06b4dd110ed96418d5a2ac73f2d1e88a80e678487c39d9

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
- テスト用 Git repository の初期化・設定・commit と、現在の branch 取得を支援する共有ヘルパー。cmoc CLI の Git 状態や repository 構成を検証するテストから利用する入口。

## Read this when
- cmoc CLI のテストで一時 Git repository を作成する必要があるとき
- テスト対象 repository の checkout 済み branch 名や、追跡対象かつ ignore された oracle file の準備方法を確認するとき

## Do not read this when
- Git repository テストの共通準備や branch 状態の確認を扱わないテストのとき
- cmoc の制御ロジックや oracle 仕様そのものを確認したいときは、対応する実装・oracle file を直接読む

## hash
- e696cf9522455dcc18230828a049a03171d40dbec77215b3e8599a53611a21e2

# `_ollama_support.py`

## Summary
- doctor テストから共有の managed Ollama service を利用するための共通定数・実行 helper。指定 root を cwd にして CLI の doctor を呼び出し、成功結果を返す。

## Read this when
- managed Ollama を使う doctor テストを追加・修正するとき
- doctor 実行時の worktree 指定、production service、固定 endpoint、テスト用モデルの扱いを確認するとき

## Do not read this when
- doctor コマンド自体の実装や仕様を確認するときは、doctor の実装・oracle spec を直接読む
- fake service lifecycle や Ollama service の起動・停止処理を変更するとき

## hash
- 142e4d277c91d98d33dec1ec0fcad02b1118bd3a681727a41753c016980684ed

# `test_acp_builder_apply_parameters.py`

## Summary
- apply fork ACP builder の parameter、prompt、root、file access mode、および oracle schema 参照・適合性を検証する pytest。apply fork builder の import 契約と packaged layout も確認する。

## Read this when
- apply fork の change summary または file review and fix parameter を変更・検証するとき
- apply fork の prompt、root token、realization_write 制約、モデル設定を確認するとき
- 対応する oracle schema との整合性や builder の packaged layout import を調査するとき

## Do not read this when
- apply fork 以外の ACP builder の挙動だけを調査するとき
- 実装や正本 schema の詳細を直接確認する必要があり、対応する builder・oracle schema を読む方が適切なとき
- 単に一般的な pytest 実行方法や共通テスト基盤を確認したいとき

## hash
- 997305818e7538b3206fbcbd3cb960d2d4ed4067024ce110ebfb76dcb7d972c0

# `test_acp_builder_indexing_parameters.py`

## Summary
- indexing 用 INDEX エントリービルダーのパラメータ設定、Structured Output schema の必須条件、互換モジュールの公開面を検証するテスト。indexing のパラメータや schema、互換 export を変更・確認する際の入口。

## Read this when
- indexing 用 INDEX エントリービルダーの model、reasoning、file access、preflight 設定を変更するとき
- INDEX エントリーの Structured Output schema の必須項目や配列制約を変更するとき
- indexing の互換モジュール公開 API を変更・確認するとき

## Do not read this when
- INDEX エントリーの生成ロジック自体を変更・確認するときは、対応する realization implementation や正本を直接読む
- indexing と無関係な builder、schema、公開 API の変更を扱うとき

## hash
- 970cc49aa2c0d2e2141dc376ed218d3ab7cd81a7016068d67403061821059631

# `test_acp_builder_oracle_review_parameters.py`

## Summary
- oracle review ACP builder の parameter builder と schema・adapter 公開面を検証するテスト。各 builder の model、reasoning、file access、preflight 設定、oracle schema との一致、互換 builder の同一性、placeholder・動的入力保持、公開 export 制限を確認する。

## Read this when
- oracle review 用 ACP builder の parameter 生成や structured output schema を変更・検証するとき
- enumerate、merge、judge、validate の各 finding builder の互換性や prompt placeholder 処理を確認するとき
- review compatibility module の公開 API 制限を確認するとき

## Do not read this when
- oracle review builder の実装詳細そのものを変更する場合は、対応する src の builder module と oracle schema を直接読むとき
- oracle review 以外の ACP builder や、finding のレビュー判定ロジック自体を扱うとき

## hash
- 38df6632769b6723cc781ebb07bdfe3b04953029fd59ae838990dba9b34a6dbc

# `test_acp_builder_session_join_parameters.py`

## Summary
- session join の conflict resolution 用パラメータ生成に関する契約を検証するテスト群。公開モジュールの公開面と、生成されるパラメータの権限・モデル選択・索引前提の有無を確認したいときに読む。

## Read this when
- session join の conflict resolution builder の公開 API が何を返すべきか確認したいとき。
- conflict 対象ファイルを渡したときの生成パラメータの権限、推論強度、モデル選択、プロンプト条件を確認したいとき。
- 公開モジュールが内部実装を露出していないか、エクスポート境界を点検したいとき。

## Do not read this when
- session join の通常 join 処理や別の builder の契約を確認したいとき。
- conflict resolution の実装詳細や prompt 組み立ての内部構造を追いたいときは、対応する実装側の本文を直接読むべきとき。
- ファイルアクセス方針やモデル選択の共通定義そのものを確認したいときは、テストではなく基礎となる定義ファイルを読むべきとき。

## hash
- f1b9f037d93dce9aed913c05500c19041aae57dc069365c274a9e4a73e4f6d51

# `test_acp_builder_tui_parameters.py`

## Summary
- TUI resolve parameter builder の出力内容、生成 schema の必須項目・enum・boolean flag、互換 module の公開名を検証するテスト。対応する builder と schema の変更時に、外部挙動と公開面を確認する入口となる。

## Read this when
- TUI resolve parameter builder の prompt 埋め込み、実行パラメータ、structured output schema を変更・検証するとき
- TUI resolve parameter module の __all__ や公開 API を変更するとき

## Do not read this when
- builder や schema の実装自体を調査・変更する作業で、まず対応する oracle または src ファイルを読むべきとき
- TUI の resolve parameter と無関係な ACP builder、CLI、または一般的なテストを扱うとき

## hash
- c48e18310f467dc6a42b19d889bb157b958f3f5f6a908deebaa512a96df32a66

# `test_apply_abandon_cli.py`

## Summary
- apply abandon CLI の外部挙動を検証するテスト。worktree・branch・state の cleanup、警告扱い、process 停止、実行位置の切替、linked session の dirty 状態、破損・不整合状態の拒否を対象とする。低レベルな process helper の契約は別テストに委譲する。

## Read this when
- `apply abandon` サブコマンドの成功・警告・失敗条件を変更または確認するとき
- apply run の worktree、branch、state、process cleanup や実行位置に関する CLI 挙動を調査するとき

## Do not read this when
- 低レベルな process helper 単体の契約だけを確認するときは、`test_runtime_apply.py` を直接読む
- `apply abandon` 以外の apply サブコマンドの外部挙動だけを確認するとき

## hash
- 64baefce08c0901cafd6caea588e51acc73068d7678219b3d827db838fe7a1b6

# `test_apply_fork_cli.py`

## Summary
- apply fork CLI のライフサイクル、状態遷移、worktree・branch 管理、割り込み時の後処理を検証する回帰テスト。
- doctor 前処理、gitignore の自動修復、設定エラー、state/PID 初期化失敗、abandon による復旧、.gitignore 編集対象の扱いも確認する。
- apply fork の実装や仕様、関連する repository/session fixture・state・worktree 挙動を変更または調査するときのテスト入口。

## Read this when
- apply fork の正常完了・中断・失敗・復旧時の外部挙動を確認するとき
- apply run の state、branch、worktree、PID ファイル、report、ログのライフサイクルを変更するとき
- doctor 前処理や .gitignore/config の apply fork 連携を変更するとき

## Do not read this when
- 対象正規化だけを変更・検証するとき
- apply fork 以外のサブコマンドの lifecycle や state を扱うとき
- 実装詳細ではなく apply fork の仕様本文を確認したいときは、先に oracle の apply fork 仕様を読むべき

## hash
- 15b82a8699705cdd7a011b2b6f02f1932ba0bccb76510b61facf68c7e51f2ab8

# `test_apply_fork_report_cli.py`

## Summary
- apply fork の CLI 統合テストを集約し、レビュー・修正ループ、収束判定、変更ファイルの再検査、rolling fork、commit、join、session state 更新を検証する。
- report の生成内容と front matter、所見推移、変更内容要約、converged・unconverged・error の結果を確認する。
- 変更要約について、未追跡ファイルの扱い、削除済み追跡ファイルの除外、Codex 要約が空の場合の fallback を検証する。

## Read this when
- apply fork の report schema、収束・未収束・error 判定、再検査ループを変更または調査するとき
- apply fork による commit・join・rolling 対象・session state 更新の CLI 挙動を変更または検証するとき
- 変更内容要約の差分抽出や fallback 挙動を変更または検証するとき

## Do not read this when
- apply fork の実装詳細だけを調査し、CLI 統合挙動や report 出力の確認が不要なとき
- session fork や apply join 単体の挙動だけを確認し、apply fork report との連携を扱わないとき

## hash
- 2763b008774e7044600325664fc0a803eb7b3a7f94dcc60beb28ca65b9929fa8

# `test_apply_fork_target_normalization.py`

## Summary
- apply fork の対象 file 正規化を検証する回帰テスト。root 直下 memo や管理用 path、未追跡 ignored file を除外し、入れ子の memo、binary file、tracked ignored file、symlink を repository path に基づいて正しく扱う挙動を確認する。

## Read this when
- apply fork の対象 file 判定・正規化・重複排除を変更または調査するとき
- oracle、realization、memo、管理用ディレクトリ、git ignore、symlink の対象分類に関する回帰を確認するとき

## Do not read this when
- apply fork の対象正規化や分類を扱わず、他の apply fork 処理だけを変更・調査するとき
- 対象 file の分類仕様そのものを確認したい場合。対応する oracle 文書・ソースを直接読むべき

## hash
- 8a09d494abb8f29892f6a3333ec796b3ceb5e149cf99d5ef51c10982c7c2a254

# `test_apply_join_cli.py`

## Summary
- apply join CLI の統合テスト。apply run の session への結合、worktree・branch・state・report の後片付け、実行場所による挙動を検証する。
- dirty worktree、想定外の apply/session 差分、realization・oracle・設定・memo 等の分類、tracked/ignored path、rename・delete、merge conflict、force-resolve、lock 中の state 再読込、error process 停止を検証する。
- apply join の成功条件・拒否条件と差分分類の実装・仕様を確認するための入口であり、テスト対象の実装や正本仕様は直接参照先で確認する。

## Read this when
- apply join の外部挙動、終了条件、cleanup、state 更新、report 内容を変更または検証するとき
- apply と session の差分分類、realization file 判定、force-resolve、merge conflict 処理を調査するとき
- apply join の worktree・branch・lock・process 状態に関する回帰を調べるとき

## Do not read this when
- apply join 以外のサブコマンドの挙動だけを調査するとき
- 単純な CLI 共通 runner、git fixture、または doctor の実装だけを確認するときは、それぞれの専用テスト・実装を直接読む
- apply join の正本仕様や実装詳細を確認することが目的で、テストケース一覧が不要なとき

## hash
- da0f1cb98c5d99c029c3b1beb7581642ec00087471243f625b34f3295c0abcf5

# `test_basic_runtime.py`

## Summary
- Root/worktree と path model の runtime 契約を検証するテスト。root placeholder の解決、repo root と linked worktree の区別、並行実行時の cwd 保護、run worktree の作成・削除における管理領域・branch・symlink・Git 登録状態の検証を扱う。
- path model や cmoc runtime の挙動を変更・調査する際の、基本的な回帰テストの入口となる。

## Read this when
- RootPathPlaceHolder、resolve_ph_path、resolve_real_path の仕様や実装を変更するとき
- repo root、run/work root、linked worktree の扱いを変更するとき
- pushd のプロセス全体 cwd とスレッド間排他を変更するとき
- create_run_worktree または remove_worktree のパス検証・symlink 防止・Git worktree 登録検証を変更するとき
- 上記 runtime 契約に関するテスト失敗の原因を調査するとき

## Do not read this when
- CLI の個別コマンド動作や出力形式だけを変更するとき
- path model や worktree lifecycle に関係しない runtime 機能を変更するとき
- 実装詳細ではなく、まず正本仕様そのものを確認すべき場合は oracle の path model または run isolation 文書を直接読む

## hash
- 5c505b6c9d91064ef2b75e95a1c050ea6f9ed1344fe7ea34fd22e37a975c377b

# `test_cli_oracle_edit.py`

## Summary
- `cmoc oracle edit` のエディタ入力生成、TUI 起動パラメータ、oracle file の未コミット変更を検証するテスト。共通エディタテンプレートの保持内容や編集結果の取り込みも確認する。

## Read this when
- `oracle edit` のエディタ連携、TUI 起動境界、固定実行パラメータを変更または検証するとき
- oracle edit 実行後の oracle file の Git 状態や自動 commit の有無を確認するとき
- editor_input の original/complete ファイル生成内容を変更または検証するとき

## Do not read this when
- oracle edit 以外のサブコマンドの挙動だけを変更または検証するとき
- エディタ入力テンプレートや TUI 起動処理を直接変更せず、一般的な CLI テスト基盤だけを確認するとき

## hash
- 96d4aae35ca9f773b594cbaac343540bea6fd3749a0cb3687d69e1e879bff601

# `test_cli_tui.py`

## Summary
- TUI 起動直前の CLI 前処理を外部挙動から検証するテスト。エディタで編集した prompt の解決、Codex TUI 用パラメータ生成、prompt・ログ・ignore の保存、linked worktree での保存先、および既定のファイルアクセスモードを扱う。

## Read this when
- `tui` サブコマンドの起動前処理、prompt 編集・解決、Codex TUI 起動パラメータを変更または調査するとき
- `.cmoc/gu` 配下の editor input・sub-command ログ、ignore 設定、linked worktree 対応の挙動を検証するとき

## Do not read this when
- TUI 起動前処理以外のサブコマンドを変更・調査するとき
- Codex 実行共通処理や prompt 生成仕様そのものを確認するときは、対応する実装・正本仕様を直接読む

## hash
- 2f8a258b918b5798c560d5e0ae6eb6545840fb80a8f3ab2e0a6baeaf4284222f

# `test_codex_runtime_errors.py`

## Summary
- Codex JSONL の異常系と CLI 不在時の実行時挙動を検証するテスト。非 object・不正 JSONL、終了コード 0 でも不正な stdout、Codex CLI 不在時の CmocError と失敗ログを扱う。Codex 実行処理や関連するエラー分類・resume token・サブコマンドログの変更を確認する入口。

## Read this when
- Codex JSONL の parser 境界や malformed event の扱いを変更・検証するとき
- Codex CLI 実行失敗、CLI 不在時の例外、codex_call 失敗ログを変更・検証するとき
- Codex 実行時のエラー分類や resume token 抽出の挙動を確認するとき

## Do not read this when
- Codex の正常系実行や通常の JSONL event 処理だけを変更・確認するとき
- Codex 以外のサブコマンド、ログ形式、設定処理を直接確認するときは、それぞれの実装・テストを読む

## hash
- cbde29d6c3a596fca3f31434a5a16f599b860a3ec77a95e19fe49a39ee16ebd7

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 実行ランタイムの結合・契約テスト。実 Codex またはスタブ Codex に対する argv、stdin、sandbox、approval、override 設定、ローカル SLM 用 managed Ollama provider、出力スキーマ、ログ、CODEX_HOME 非変更、リポジトリ書き込み結果を検証する。

## Read this when
- Codex exec の呼び出し契約、override 引数、ローカル SLM / managed Ollama 連携を変更または調査するとき。
- Codex 実行結果、出力スキーマ配置、プロンプトログ、CODEX_HOME の副作用を検証するとき。

## Do not read this when
- Codex 実行ランタイムの挙動やテスト契約を扱わず、他の CLI 機能・設定・テストだけを変更または調査するとき。
- 単体の補助関数の内部実装を確認するだけで、Codex exec の外部契約を確認する必要がないとき。

## hash
- 7810bcd202e133caeaf3feb8cb249161c595f6f7c981bcaa337292bf7061256d

# `test_codex_runtime_home.py`

## Summary
- Codex 実行時の CODEX_HOME 解決・引き継ぎと、Codex 起動前の home/auth.json 検証を確認する pytest。Codex subprocess が正しい環境・作業ディレクトリで呼ばれること、および不正な認証環境を事前に拒否して起動しないことを検証する。

## Read this when
- run_codex_exec の CODEX_HOME、認証情報、preflight validation、または Codex subprocess 起動条件を変更・調査するとき
- Codex 実行失敗時の CmocError 内容や、相対 CODEX_HOME の解決基準を確認するとき

## Do not read this when
- Codex 実行環境や home 検証に関係しない CLI 機能・テストを変更するとき
- 実装の詳細ではなく、Codex 実行全体の仕様を確認したい場合は、対応する oracle doc を先に読む

## hash
- 841e4926e3a25131ea850d93bdfc16acb9bed4e8de82c492b8ad95a4d4161964

# `test_codex_runtime_paths.py`

## Summary
- Codex 実行時のパスと sandbox 境界を検証するテスト。並列実行時のログパス予約、cwd の選択、リンク worktree における schema 保存先、PURE_ORACLE_READ の read-only sandbox、`.agents` パスを権限設定へ注入しないことを扱う。

## Read this when
- `run_codex_exec` の cwd、ログ・出力・schema の保存先、sandbox 引数、並列実行時のパス衝突回避を変更・検証するとき。

## Do not read this when
- Codex 実行パス以外のプロンプト生成、設定、CLI 動作を調査するとき。sandbox 変換の単体ロジックだけを確認する場合は、対応する実装・oracle file を直接読む。

## hash
- 1c68ace616ef78a31fd6db76c9787cb1cf9d111ea166a926e7fb00849dc502a0

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex quota exceeded 後の probe・待機・resume・再実行を検証する回帰テスト群。quota probe の共有、resume token 復元、並行呼び出し、失敗伝播、ログ・出力・CODEX_HOME・cwd の観測を扱う。Codex 実行の quota retry 制御を変更・調査する際の入口。

## Read this when
- Codex exec の quota 待機、quota availability probe、resume または prompt 再実行の挙動を変更・検証するとき
- quota retry の並行実行、probe 失敗、poll 上限、KeyboardInterrupt、ログ記録を調査するとき
- Codex 呼び出しの call log、subcommand log、CODEX_HOME、cwd の回帰を確認するとき

## Do not read this when
- quota retry 以外の Codex exec 基本仕様や単独の CLI 入出力を調査するときは、対応する実装・仕様・テストを直接読む
- quota probe の prompt 構築そのものだけを変更・調査するときは、probe builder の実装と専用テストを先に読む

## hash
- 0878c1655899b637441b6e8000e83f2c44e4938bb46920073410521819e3544c

# `test_codex_runtime_retry.py`

## Summary
- Codex exec の再試行・失敗処理と関連ログを外部挙動として検証するテスト。Structured Output の意味的失敗や解析失敗、capacity retry、未知の JSONL error、中断、retry 上限、差分保持、stdout 外エラーマーカーの扱いを対象とする。run_codex_exec の状態、subprocess 呼び出し回数、call log、subcommand event を一続きの責務として確認する。

## Read this when
- run_codex_exec の retry 条件、backoff、上限、失敗結果を変更または調査するとき
- Codex 呼び出しの call log や subcommand event の schema・status・保存内容を変更または検証するとき
- Structured Output の検証失敗、JSONL error、KeyboardInterrupt、capacity failure、agent diff 保持の挙動を確認するとき

## Do not read this when
- Codex exec の通常成功経路だけを変更・調査するとき
- retry や失敗時ログに関係しない Codex 実行設定・プロンプト生成を扱うとき

## hash
- cba7a9b0499545ecf4b9e9033c6ac6718506e48f75b4f79ea047e303360367de

# `test_codex_runtime_subprocess.py`

## Summary
- Codex サブプロセス実行と apply 用プロセス追跡の挙動を検証するテスト。専用 process group の記録、member pidfd によるシグナル送信、SIGTERM の遅延、leader 終了後や割り込み後の tracking 保持、継承 tracking 環境変数の無視を扱う。runtime の subprocess 制御実装を確認・変更する際のテスト入口。

## Read this when
- Codex subprocess の起動・終了・シグナル処理や apply tracking を変更するとき
- プロセスグループ、pidfd、SIGTERM、KeyboardInterrupt、環境変数継承に関する不具合を調査するとき
- commons.runtime_codex_profile の実装変更後に対応する外部挙動を検証するとき

## Do not read this when
- Codex subprocess や apply tracking と無関係な CLI 機能を変更・調査するとき
- テスト対象の実装詳細ではなく、別のサブコマンド固有の入出力だけを確認するとき

## hash
- 6df388bf8a7ca92bd23b1f2672d01af4d38b2d6e2779a3eedb77dd2a34c380f7

# `test_codex_runtime_tui.py`

## Summary
- Codex TUI 実行の統合テスト。完成済み prompt の読み込み、作業ディレクトリと sandbox・アクセス設定、Codex CLI 引数を検証する。
- 成功・CLI 不在・KeyboardInterrupt・非 0 終了時について、TUI call log、サブコマンドイベント、コンソール要約、エラー処理を検証する。
- timestamp 衝突時に call log を上書きせず保持する挙動も検証する。

## Read this when
- Codex TUI の実行引数、prompt 読み込み、アクセスモード、linked worktree 対応を変更・調査するとき
- Codex 呼び出しのログ、終了状態、例外・失敗時のコンソール出力を変更・検証するとき

## Do not read this when
- Codex TUI 以外のサブコマンドや、Codex 呼び出し実装そのものの詳細を直接調査するとき
- prompt 生成規則や設定仕様の正本を確認するときは、対応する oracle file を先に読むべき場合

## hash
- fe6c8c0fb3724bfe888d68982f70e32fdaa0281aa1aac3d7b9f691a0b99add1d

# `test_doctor_cli.py`

## Summary
- doctor preprocess の外部契約を検証する統合テスト。CLI と直接呼び出しの双方で、Git の共通状態修復、config の生成・同期、managed Ollama の準備、linked worktree と共有 lock の扱い、修復 commit の境界を確認する。
- 修復失敗時や既存の staged・unstaged 差分、rename、`.cmoc/gu` の既存追跡ファイルを保持する Git index のライフサイクルも検証する。doctor 関連の外部挙動と回帰テストの入口となる。

## Read this when
- doctor または `dector` の CLI 挙動を変更・レビューするとき
- doctor preprocess の Git 修復、config、managed Ollama、linked worktree、lock、修復 commit を調査するとき
- 既存の staged/unstaged 差分や index 保持に関する回帰を調べるとき

## Do not read this when
- doctor preprocess と無関係な CLI、設定、Ollama、Git 操作だけを調査するとき
- doctor の内部実装や正本仕様を確認する場合。このテストから実装責務や仕様全体を推測せず、対応する oracle 文書や実装を直接読むこと

## hash
- e4546f907dc0ad47ab6967c145e3d3c844bac5a1c3a6e2337432b095960fb357

# `test_indexing_cli.py`

## Summary
- `cmoc indexing` の CLI と preflight、worktree 対応、Codex による INDEX.md 生成、hash による再生成抑制、INDEX.md のみを対象とする commit lifecycle を外部挙動として検証するテスト。

## Read this when
- `cmoc indexing` の CLI 事前条件・doctor 実行・worktree 選択・dirty 状態の拒否を確認または変更するとき。
- INDEX.md の生成、Codex structured output の利用、fresh hash 時の Codex 呼び出し省略を確認するとき。
- INDEX.md だけを commit し、既存の非 INDEX 差分を保持する preflight と commit 条件を確認するとき。

## Do not read this when
- INDEX.md エントリーのレンダリング仕様そのものを確認する場合は、指定された Structured Output schema と indexing の仕様文書を直接読む。
- indexing CLI 以外のサブコマンドや、Codex 実行基盤そのものの内部実装だけを調べる場合。

## hash
- 18f6f2e15bd0dc91ad5aab6124407919ef9da1b31a6bc5859be15fdc1068f90e

# `test_indexing_common.py`

## Summary
- `commons.indexing` の INDEX.md エントリー生成・解析・更新とディレクトリ traversal を直接検証するテスト。入力検証、hash 再利用・不正エントリー再生成、空ディレクトリ、安定した兄弟順序、並列更新、cwd lock、memo・symlink・特殊ファイルの扱い、symlink 置換、linked worktree 間の lock 共有を扱う。CLI lifecycle から indexing の挙動を切り離して確認する入口。

## Read this when
- INDEX.md の render/parse/update_indexes の仕様や入力検証を変更・調査するとき
- INDEX 更新の traversal、並列実行、cwd lock、symlink、特殊ファイル、memo 除外の挙動を変更・調査するとき
- INDEX 更新に関する回帰テストを追加・修正するとき

## Do not read this when
- CLI lifecycle やサブコマンド全体の統合挙動を確認する場合
- INDEX entry の生成仕様そのものを確認する場合は、まず oracle の indexing 仕様・schema・entry standard を読む

## hash
- df66bf63ee43656c807a40fdebf51e8d5061e90bb16d97696223fb11c651ead7

# `test_indexing_preflight.py`

## Summary
- Codex 呼び出し前の indexing preflight を検証する統合テスト。exec/TUI 経路での実行順序、対象 root と linked worktree の選択、git commit・作業ツリー clean 状態、repository lock 待機、パラメータによる preflight 無効化、file access violation 後に recovery indexing を行わない制御を扱う。

## Read this when
- indexing preflight、Codex exec/TUI 呼び出し前処理、linked worktree の indexing 対象選択、repository lock、recovery indexing の挙動を変更・レビュー・検証するとき。

## Do not read this when
- indexing preflight や Codex 呼び出し前処理ではなく、通常の indexing 実装、Codex 実行本体、または一般的な CLI 入出力だけを調べるとき。

## hash
- 35c2adf8b7396a5784a59bf79ae209b4d169a3f8c49624b543f55839716c587a

# `test_oracle_review_loop.py`

## Summary
- oracle review の finding loop に対するテスト群。対象 oracle ごとの finding 分離、検証 prompt への理由引き継ぎ、隔離 worktree の実行コンテキスト、割り込み時の部分結果保持、merge 応答の意味検証と再試行・失敗を検証する。

## Read this when
- oracle review の finding 列挙・merge・challenger/advocate 検証・judge の制御を変更またはレビューするとき
- Codex 実行コンテキスト、worktree 分離、割り込み時の復旧可能な部分結果を確認するとき
- merge や finding validation の再試行・意味的不正応答の扱いを変更するとき

## Do not read this when
- oracle review の prompt 定義や設定値そのものを変更・確認するだけのときは、対応する oracle 文書や設定実装を直接読む
- finding loop と無関係な CLI サブコマンド、永続化、一般的なテスト規約を調べるとき

## hash
- 9b6f3674162f7b9aa1f44ce4f242461cfda1c187db51fba3d6887e6d2ddb4ecc

# `test_oracle_review_merge_operations.py`

## Summary
- oracle review の merge operation 適用処理を対象とするテスト。delete・replace・merge の kind 契約、finding 更新と採番、追加件数、不正な payload・対象・重複 target の拒否を検証する。

## Read this when
- oracle review の finding merge operation の契約や適用結果を変更・確認するとき
- apply_finding_merge_operations の入力検証、対象再利用防止、finding 生成をテストするとき

## Do not read this when
- oracle review の merge operation 以外の処理を変更・確認するとき
- 実装本体の責務や CLI 全体の仕様を確認するときは、まず対応する oracle 仕様または実装ファイルを読む

## hash
- eaa1dc20ee2f54edab5af2bf2d23511177ba13df99ac87b446831e01aaf747f8

# `test_oracle_review_report.py`

## Summary
- oracle review の report 生成と CLI 実行を検証するテスト。中断・処理失敗時の report、finding の severity・判定別分類と件数、対象 oracle file の集計、scope オプション、`eval-oracle` の委譲、出力節順を確認する。

## Read this when
- oracle review または eval-oracle の report 出力・失敗時挙動・中断時挙動を変更または検証するとき
- finding の accepted/rejected 分類、severity 別件数、oracle path・symlink の集計を変更または検証するとき
- oracle review CLI の scope オプションや実行委譲を変更または検証するとき

## Do not read this when
- oracle review の実装や report 生成処理そのものを変更する場合は、まず対応する実装モジュールと oracle 仕様を読むとき
- oracle review と無関係な CLI、report、oracle file 列挙機能を変更または検証するとき

## hash
- 162913f2977c477a8317990c41aad04040608c9f75dc85fe481c8c6d4861fcb1

# `test_oracle_review_targets.py`

## Summary
- oracle review の対象列挙と finding path 解決を検証するテスト。相対・絶対・{{work-root}} パス、symlink、tracked/ignored oracle file、session/full scope、fork commit 固定、AGENTS.md・INDEX.md の除外を扱う。

## Read this when
- oracle review の対象範囲や oracle path 解決を変更・検証するとき
- session/full scope における tracked・ignored・symlink ファイルの扱いを確認するとき
- oracle review の対象列挙テストを追加・修正するとき

## Do not read this when
- oracle review の finding 内容生成や prompt 構築だけを変更するとき
- 対象列挙・path 解決と無関係な CLI サブコマンドを調査するとき
- oracle review の実装詳細を直接確認する必要があり、まず review_paths.py や review_targets.py を読むべきとき

## hash
- 93ace4b4fa06c2ba5a16042aa94f4994c434b6b61e79e113fc15e2c767f9453a

# `test_oracle_review_worktree.py`

## Summary
- oracle review の linked worktree・session branch・snapshot commit を対象にした run isolation を検証する pytest 群。未コミット差分や INDEX.md 以外の変更を拒否し、review worktree と preflight で生成された INDEX.md の統合、削除側を含む INDEX.md の競合解決まで確認する。

## Read this when
- oracle review の worktree 分離、session snapshot からの fork、差分検証、INDEX.md 統合または競合解決の挙動を変更・確認するとき。
- oracle review と indexing preflight の連携や、review worktree の後処理を調査するとき。

## Do not read this when
- oracle review の finding 判定ロジックや通常の CLI 出力だけを確認する場合。
- INDEX.md の生成規則そのものを確認する場合は、まず indexing の仕様・実装・専用テストを読む。

## hash
- dd5e67673536018b1a87fb873753976b909593bad381c4fcf13531dd35c64503

# `test_packaged_import.py`

## Summary
- packaged layout 上で主要な ACP、oracle、config モジュールの import 境界と公開 API を検証するテスト。隔離した一時環境へパッケージをコピーし、設定定義・schema・prompt・file access mode・再公開された型の互換性を確認する。

## Read this when
- パッケージ配置や setuptools の package-dir/packages 設定を変更するとき
- ACP builder、oracle review/edit adapter、config の公開 import や再公開 API を変更するとき
- packaged layout、PYTHONPATH、外部 site-packages 分離、prompt/schema 参照のテスト挙動を確認するとき

## Do not read this when
- 単一の oracle builder 実装や schema 定義の詳細だけを変更し、packaged import 境界や公開 API に影響しないとき
- 通常の CLI 実行フローや packaged layout と無関係なテストを調査するとき
- 対象モジュールの正本仕様や実装詳細を直接確認すべき場合。このファイルは import と出力契約の統合検証が入口である

## hash
- 411babcfda3fec2e1ed9b441a1a0760642b9c17ecd4e09a4b88575e408f687a4

# `test_production_cli.py`

## Summary
- 利用者向け console script と実 Codex CLI・managed Ollama を使い、全末端サブコマンドの本番経路を独立 process または PTY で検証する受け入れテスト。終了 code、report・state・Git の状態、Codex call log、TUI の応答完了と終了を確認し、LLM の回答品質自体は判定しない。

## Read this when
- CLI の末端サブコマンド追加・変更や、本番 process 経路の回帰を確認するとき
- 独立 process、実 Codex CLI、managed Ollama、PTY 上の TUI、call log・report・state・Git の検証方法を調べるとき

## Do not read this when
- 単体の CLI 実装や内部 helper の詳細を変更・調査するとき
- LLM の回答内容・品質そのものを評価するとき
- 本番実行環境を使わない parser・設定・状態処理の局所テストだけを扱うとき

## hash
- 1231a268c46ac863ee6dd1e791798cb41899693c260c07dd1d728ca05ab3338d

# `test_prompt_parts.py`

## Summary
- 標準 prompt parts と complete prompt の組み立て結果を検証するテストファイル。各 standard のタイトル・主要文言・出力内容、file access mode ごとの規則、complete prompt への標準文書の注入可否、root placeholder の保持、既定値での省略を確認する。prompt parts や complete prompt の挙動を変更・調査する際のテスト側の入口となる。

## Read this when
- prompt parts の本文・タイトル・主要規則を変更したとき
- complete prompt の標準文書注入、省略、root token 展開の挙動を変更・検証するとき
- file access mode、routing rule、index entry standard、oracle/realization standard のテストを確認するとき

## Do not read this when
- prompt の実装詳細だけを調査し、テスト期待値の変更が不要なとき
- このテストが対象とする標準文書や complete prompt と無関係な機能を変更するとき
- 具体的な standard の正本仕様を確認したいとき（対応する oracle source を直接読む）

## hash
- 1b9212587256b870f1375a0ac202ce570f593d22eafa867ae62059809c0b0530

# `test_runtime_apply.py`

## Summary
- apply 実行時のプロセス追跡・停止契約を、CLI を介さず低レベル API で検証するテスト。PID ファイル、advisory lock、agent-read runtime state、pidfd、PID reuse 防止、process group 停止、親終了後の child 再読込、競合終了時の扱いを対象とする。apply abandon の CLI 外部挙動は扱わず、対応する CLI テストへ進むための基盤テスト入口である。

## Read this when
- apply runtime のプロセス追跡、PID ファイルや lock の配置・同期、pidfd による停止、child process group の停止、PID reuse や競合終了時の制御を変更・検証するとき。

## Do not read this when
- apply abandon コマンドの引数・終了コード・CLI 出力など外部挙動を確認するときは、直接 `test_apply_abandon_cli.py` を読む。

## hash
- 31cb4884b8071f5f1aff87d25c22cbaa96db9c1adeaa859a3181217fefc45d4e

# `test_runtime_cli.py`

## Summary
- CLI の error、log、preflight、completion 境界を検証するテスト。duration 表示、サブコマンドログの衝突・並列書き込み、doctor/pre-log 失敗時の記録、Markdown error report、stdout 出力、CLI 引数解析、work root 制約、completion probe の副作用抑制、.gitignore 更新、worktree ごとの処理対象を扱う。

## Read this when
- CLI のエラー表示、終了コード、stdout/stderr の境界を変更・検証するとき
- サブコマンドログ、doctor preprocess、pre-log check、worktree 処理の挙動を変更・検証するとき
- CLI completion probe や引数 scope 検証の副作用・解析境界を確認するとき
- duration 表示、.cmoc ignore 設定、起動 wrapper の call stack 表示を変更・検証するとき

## Do not read this when
- 対象が個別サブコマンドの主処理や oracle の内容そのもので、CLI 共通の error・log・preflight・completion 境界を扱わないとき
- 単純な実装内部の helper 変更で、ここに示される外部挙動や制御境界に影響しないとき

## hash
- 8dfac46018fddc21c11a5b7969c8a6b0a88867a542f6b5914d60c51cbec30c07

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
- Codex CLI の sandbox argv 生成を検証する pytest。全 FileAccessMode で permission profile や path 別例外を注入しないこと、作業ツリー内容に依存しないこと、生成された sandbox 引数を実 Codex CLI が受理することを確認する。

## Read this when
- Codex の sandbox argv、permission profile、path 別 read/write 例外の扱いを変更・検証するとき
- build_codex_override_args または prepare_codex_override_args の API・出力を変更するとき
- Codex CLI parser との sandbox 引数互換性を確認するとき

## Do not read this when
- Codex sandbox argv や permission profile に関係しない機能のテストを調査するとき
- 実装本体の一般的な設定処理や、個別の CLI サブコマンドの挙動を直接確認するとき

## hash
- d69dabe02e2acbadf3e6a25fde436391e442f073d3b5393199757f65daf8c5fd

# `test_runtime_codex_profile.py`

## Summary
- Codex 起動引数における model、sandbox、provider 上書き契約を検証するテスト。各 FileAccessMode の sandbox 変換、承認設定、reasoning effort、未知 mode の拒否、通常 provider での worktree 非走査、cmoc 管理 Ollama provider の設定を確認する。

## Read this when
- Codex argv の sandbox・model・provider 上書き仕様を変更または検証するとき
- FileAccessMode と Codex 起動引数の対応を確認するとき
- cmoc 管理 Ollama provider の Codex 設定を変更または検証するとき

## Do not read this when
- Codex argv の構築実装そのものを変更・調査するときは、参照されている runtime 実装と oracle 仕様を先に読む
- Codex 起動引数と無関係なテストや設定を扱うとき

## hash
- ef8efcced62957c7c008e9f2ab391f208d1db6ff2d4099f12161c4ed701c8c9c

# `test_runtime_config.py`

## Summary
- CmocConfig の既定値、JSON 永続化時のメンバー順、設定ファイル未作成時の案内、および設定値の型・内容検証をテストする。cmoc_runtime の設定変換・読み込み処理と CmocConfig の挙動を確認するためのテスト入口。

## Read this when
- CmocConfig の既定値や codex モデル・reasoning effort の設定を変更するとき
- 設定の JSON 化、読み込み、永続化形式、または設定エラーの挙動を変更・調査するとき
- 設定項目の型検証や不正値の拒否条件を確認するとき

## Do not read this when
- 設定処理ではなく、他の runtime 機能や CLI コマンドの挙動だけを調査するとき
- 設定の正本仕様そのものを確認する必要があり、oracle の設定仕様を直接読むべきとき

## hash
- 98cd65c2bac1c72a736e0f588494f365150de60f288d8a23ee20f321af5812e9

# `test_runtime_content.py`

## Summary
- `is_binary` が通常のテキスト内容と NUL バイトを含む内容を正しく判定することを検証するテスト。indexing における binary file 除外判定の挙動確認への入口。

## Read this when
- indexing の content 判定や binary file 除外処理を変更・検証するとき
- `is_binary` のテキスト／binary 判定に関するテストを確認するとき

## Do not read this when
- indexing の仕様根拠そのものを確認したいときは、参照先の oracle doc を直接読む
- `is_binary` の実装詳細を確認したいときは、実装モジュールを直接読む

## hash
- c6132bad711dc59ae537534245564ab610bea5f1cbf873635394d54ee99c8046

# `test_runtime_file_access.py`

## Summary
- FileAccessMode の JSON 永続化値と Codex sandbox mode への変換契約を検証するテスト。READONLY 系と各種 write mode の対応を確認する。

## Read this when
- FileAccessMode の値、または file_access_to_sandbox_mode の変換結果を変更・調査するとき
- sandbox モード変換や関連する runtime テストを追加・修正するとき

## Do not read this when
- ACP の FileAccessMode 定義そのものを変更・調査するときは、oracle の根拠ファイルを先に読む
- prompt のファイルアクセス規則を変更・調査するときは、oracle の根拠ファイルを直接読む
- FileAccessMode や sandbox 変換と無関係なテスト・実装を扱うとき

## hash
- 0f39773aec1b938ee1f0a4dbca60b301082daf452c8f045e08f086ea979eb1d8

# `test_runtime_ollama.py`

## Summary
- Ollama の systemd サービス復旧、サービスプロセス検証、HTTP 応答、listener のプロセス整合性、モデルのロード順序、GPU 推論確認に関する pytest。commons.runtime_ollama の内部制御をモックし、成功条件と利用者向けエラー条件を検証する。

## Read this when
- Ollama の systemd サービス起動・再起動条件や実行ファイル指定を変更するとき
- Ollama のサービス検証、listener 判定、HTTP 応答処理、モデルロード、GPU VRAM 確認を変更するとき
- runtime_ollama の関連テストケースや失敗条件を確認するとき

## Do not read this when
- Ollama と無関係な CLI 機能や runtime モジュールを変更するとき
- 正本仕様そのものを確認する必要があるときは、コメントに示された oracle 文書を直接読む

## hash
- 3d3ac726ec0be07c8ab3502926915bdb31bbed782c75d70802388d4830bec4f1

# `test_runtime_state.py`

## Summary
- session/apply state の入力形状検証、branch 名解析、状態ファイル読み込み時の不正形式検出を担うテスト。session fork lock の process 間共有と直列化も検証する。runtime state 実装や session fork 仕様の挙動確認に入るためのテスト入口。

## Read this when
- session/apply state のフィールド型・null 許容・不正値処理を変更または確認するとき
- session branch や apply branch の解析規則、状態ファイルの branch 対応付けを変更または確認するとき
- session fork lock の repository 単位の process 間排他を変更または確認するとき

## Do not read this when
- session/apply のサブコマンド本体の処理フローだけを確認したいときは、対応するサブコマンド実装や oracle 仕様を直接読む
- runtime state の実装詳細を確認したいときは、まず commons.runtime_state の実装を直接読む

## hash
- fbf9b2216eb0685b34c2b417691c61d2450c18a06114603fa4837f9e842e2ce8

# `test_session_cli.py`

## Summary
- session の fork・join・abandon CLI における外部挙動を、実 Git リポジトリと linked worktree を使って検証する回帰テスト群。branch と永続 state の生成・遷移・cleanup、rollback、session-id 衝突、dirty worktree や破損 state の拒否、oracle conflict 解消、Codex 実行時の sandbox・prompt・root/cwd 境界、stdout/stderr の error report を扱う。session 状態ライフサイクル全体を観測するテスト入口。

## Read this when
- session fork、join、abandon の CLI 挙動や回帰テストを変更・調査するとき
- session branch、session state、linked worktree、state cleanup、rollback の仕様や不具合を確認するとき
- session join の conflict resolution、Codex sandbox、prompt、repo root/cwd の受け渡しを検証するとき
- session CLI の出力先、終了コード、preprocess、dirty worktree 拒否を確認するとき

## Do not read this when
- session CLI 以外のサブコマンドや、session の実装詳細だけを直接調査する場合
- session state の正本仕様を確認する場合は、対応する oracle doc を直接読む
- 共通テスト補助関数や Git/Ollama test fixture の実装を確認する場合は、それぞれの support module を直接読む

## hash
- 3ef6f1b66b65cdf83f9ff4b65cfdea2d98144d8c3201123d00abc33c22aef2a7

# `test_struct_doc_rendering.py`

## Summary
- StructDoc の Markdown renderer における整形挙動を検証するテスト。通常の本文と code block 内で連続する空行を一つに縮約すること、および互換モジュールから再公開された StructBlock が renderer で利用できることを確認する。

## Read this when
- Markdown renderer の空行縮約仕様を変更・検証するとき
- StructDoc、StructBlock、StructCodeBlock、render_as_markdown の互換公開や出力形式を変更するとき

## Do not read this when
- renderer 以外の StructDoc 機能や CLI の挙動を確認するとき
- 実装の詳細を調べる必要があり、対応する basic.struct_doc の実装を直接読むべきとき

## hash
- 650a3dab8a023eb6c55dd32e6ed5ce178f4641d3f81b8805b33c18bce039c1db
