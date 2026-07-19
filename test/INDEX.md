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
- doctor CLI のテスト実行を補助する共有ヘルパー。production と共有する managed Ollama service に対し、指定した worktree を cwd として doctor を起動し、成功結果を返す。SLM モデル名と固定 endpoint・production 環境を前提とする。

## Read this when
- doctor サブコマンドの CLI テストを追加・変更するとき
- managed Ollama service、production の HOME/PATH、または固定 endpoint を使うテスト境界を確認するとき

## Do not read this when
- doctor 以外のサブコマンドのテスト実装を調べるとき
- managed Ollama service の仕様や doctor の詳細な出力契約を確認するときは、対応する oracle ドキュメントや doctor テストを直接読む

## hash
- 90a73f1e5e9334d867cad3c2e512f3de842d1b85b5426c83803d986aa80491a2

# `test_acp_builder_editing_run_parameters.py`

## Summary
- 新しい editing workload に対応する canonical builder adapter の検証テスト。oracle edit、realization apply、realization refactor の各 builder について、実行パラメータ、ファイルアクセスモード、モデル設定、構造化出力スキーマ、プロンプトへの入力反映を確認する。

## Read this when
- editing workload の canonical builder adapter を変更・追加・レビューするとき
- builder が生成する実行パラメータやプロンプト、構造化出力スキーマの結び付きを検証するとき
- oracle edit、realization apply、realization refactor の fork launch parameter のテスト範囲を確認するとき

## Do not read this when
- builder 実装そのものの責務や生成ロジックを調べるときは、対応する src の builder ファイルを直接読む
- editing workload と無関係な ACP builder や一般的なテスト基盤を調べるとき

## hash
- b38fced9e2a7409cf2336f4c7b4abe8925704f048b83220af073a73e623b31bf

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
- oracle review ACP builder の parameter builder、schema、adapter 公開面に対する互換性テスト。モデル・推論・アクセス設定、schema 一致、placeholder 補正、動的入力保持、互換 module の公開 API を検証する。対応する正本は oracle/src/oracle/acp_builder/oracle/review/。

## Read this when
- oracle review の ACP builder や互換 adapter の挙動を変更・確認するとき
- review 用 parameter の schema、prompt placeholder、動的入力保持、公開 export を検証するとき

## Do not read this when
- review 以外の ACP builder を扱うとき
- 実装や正本 schema の詳細を直接確認する必要があり、対応する src または oracle を読むべきとき

## hash
- 3380468130016786cb49fc97bd2e3f3c112943c1d4deed0ba21d986a359aec8e

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

# `test_basic_runtime.py`

## Summary
- Root/worktree と path model の runtime 契約を検証するテスト。placeholder path の解決、repo root と linked worktree の区別、cwd 変更の直列化、run worktree の作成・削除時における管理領域・branch・symlink・Git 登録状態の検証を扱う。

## Read this when
- path placeholder の解決や repo/worktree root の挙動を変更・調査するとき
- pushd の並列利用や process-global cwd の安全性を確認するとき
- run worktree の作成・削除に関するパス検証、symlink 防止、Git 登録確認を変更・調査するとき
- 対応する runtime 実装の契約をテストから確認するとき

## Do not read this when
- CLI の一般的な入出力や、path model・worktree runtime と無関係な機能を変更・調査するとき
- 具体的な実装詳細を確認する必要があり、対応する runtime 実装を直接読む方が適切なとき

## hash
- 1278a7d1b4fb9f2854bfedaca9903a9b46a9faef558f17c1a5c6f03d2fee7bf3

# `test_cli_command_tree.py`

## Summary
- 公開 CLI の leaf コマンド集合が oracle と一致すること、および Typer/Click 互換性エラーなしにヘルプを描画できることを検証するテスト。CLI コマンドツリー変更やヘルプ生成の回帰確認の入口となる。

## Read this when
- 公開 CLI のコマンド構成を変更・確認するとき
- Typer と Click の互換性や CLI ヘルプ描画を検証するとき

## Do not read this when
- 個別サブコマンドの処理実装や入出力仕様を確認するとき
- CLI 以外の機能のテストを調査するとき

## hash
- a8ee861c39e5e30fa1a309d97c8ed370895fd5bcbed954318bca200f867cc7e3

# `test_cli_tui.py`

## Summary
- TUI 起動前の CLI 前処理を外部挙動で検証するテスト。エディタ入力の保存、prompt 解決、Codex TUI 起動パラメータ、既定のファイルアクセスモード、linked worktree でのログ・schema・ignore 配置を扱う。TUI サブコマンドの前処理や linked worktree 対応を変更・調査する際のテスト入口。

## Read this when
- TUI サブコマンドの起動フロー、prompt 編集・解決、Codex 実行パラメータを変更または検証するとき
- editor input の timestamp 衝突時の保存や complete prompt の生成先を確認するとき
- linked worktree におけるログ・schema・`.gitignore` の挙動を確認するとき

## Do not read this when
- TUI 以外のサブコマンドや、TUI 実装内部の単体ロジックだけを調査するときは、対応する実装・専用テストを直接読む
- Codex 出力品質や一般的な CLI テスト基盤の挙動を調査するとき

## hash
- e0ad03d2444b7defa570eb2a283385da622b13543e3d892e3ff4328ffe4e009e

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
- Codex サブプロセス実行と apply 用プロセス追跡のテスト。専用 process group の記録、member pidfd によるシグナル送信、SIGTERM の遅延、leader 終了後や割り込み後の追跡保持、継承 tracking 環境変数の無視を検証する。

## Read this when
- Codex subprocess の process group 管理や apply abandon の cleanup 挙動を変更・検証するとき
- run_codex_subprocess または run_tracked_codex_subprocess の追跡・シグナル処理を確認するとき

## Do not read this when
- Codex subprocess の実装詳細ではなく、apply abandon の正本仕様を確認したいときは oracle 側の仕様を直接読む
- 対象が CLI 出力や別の subprocess 機能に限定されるとき

## hash
- 6fbaec44d70c3932f12b659e286f214d9b64ea297b9a60bb8cd3198020bc1549

# `test_codex_runtime_tui.py`

## Summary
- Codex TUI 実行ラッパーの統合テスト。完成済み prompt の読み込み、ファイルアクセスモードと CLI 引数、作業ディレクトリ、call log・サブコマンドイベント・コンソール要約の出力、timestamp 衝突時のログ保持、CLI 不在・KeyboardInterrupt・非 0 終了時の失敗処理を検証する。Codex 実行境界や TUI ログ仕様を変更・確認する際の realization test の入口。

## Read this when
- Codex TUI の subprocess 呼び出し、sandbox・approval・作業ディレクトリ引数を変更または確認するとき
- TUI の call log、サブコマンドイベント、コンソール出力、失敗時の例外処理を変更または確認するとき
- Codex CLI 不在、割り込み、非 0 終了、timestamp 衝突へのテスト影響を確認するとき

## Do not read this when
- Codex TUI 以外のサブコマンドや、TUI の prompt 生成仕様そのものを調査するときは、対応する実装または oracle 文書を直接読む
- 単にリポジトリ全体のテスト構成や共通テスト補助関数を確認したいだけのとき

## hash
- 1f8c2d8abf12c3d353dccae586906aa5d3ba923673b9344ee3f2f14923ddbf56

# `test_doctor_cli.py`

## Summary
- doctor preprocess の共有 lifecycle を外部挙動から検証する統合テスト。CLI と直接呼び出しの両方を対象に、Git 状態の修復・commit、設定生成と同期、managed Ollama の導入・model pull、linked worktree の扱い、共有 lock 待機、失敗時の staged index 保持を検証する。doctor preprocess の関連テストを読む入口。

## Read this when
- doctor preprocess、doctor CLI、managed Ollama、config 修復、linked worktree、共有 doctor lock の挙動を変更・調査するとき
- doctor の修復 commit が既存の staged/unstaged 差分、rename、削除、`.cmoc/gu` の追跡状態へ与える影響を確認するとき
- doctor preprocess の外部契約を一連の lifecycle として検証するテストを探すとき

## Do not read this when
- doctor preprocess 以外のサブコマンド単体の挙動を調査するとき
- doctor の内部実装や設定・Ollama の詳細を直接確認したい場合は、対応する realization implementation や正本仕様を先に読むとき
- 単一の Git helper、CLI runner、Ollama fixture の実装だけを確認する必要があるとき

## hash
- 2ae3c14ef434d2ed2b83240f30482511308911f99d79fc6d481c218b1f60f3ec

# `test_editing_run_cli.py`

## Summary
- workload fork と run join/abandon の統合的な realization test。各種 fork 操作、共通 run 状態、変更の join・強制解決・ロールバック、abandon、割り込み時の復旧を CLI 外部挙動として検証する。

## Read this when
- realization apply fork、oracle edit fork、realization refactor fork、run join/abandon のライフサイクルや共通状態を変更・調査するとき
- fork 後の worktree、ブランチ、永続状態、許可されたファイルアクセス、完了レポートの統合挙動を検証するとき

## Do not read this when
- 単一サブコマンドの内部実装だけを変更し、fork・run 状態・join/abandon の統合挙動に影響しないとき
- 通常の session 作成や oracle investigation の単独仕様を確認する場合は、まず対応する実装テストを直接読む

## hash
- 35b4a26ed5468b5b61835b867dac2ec23b71acb14bb56cabf6b6424d45b2c897

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
- Codex 呼び出し前の indexing preflight を検証する pytest 集。exec/TUI 経路での実行順序、linked worktree の選択、repository lock 待機、パラメータによる無効化、file access violation 後に recovery indexing を行わない制約を扱う。indexing や Codex 実行は fake に差し替え、git commit・作業ツリー状態・呼び出し回数も確認する。

## Read this when
- Codex exec または TUI 呼び出し直前の indexing preflight の挙動を変更・調査するとき
- preflight の lock 制御、worktree 判定、無効化条件、recovery 禁止を検証するとき

## Do not read this when
- INDEX.md 生成ロジック自体や Codex preflight の実装詳細を確認したいときは、対応する realization implementation を直接読む
- preflight と無関係な CLI 機能や一般的な indexing テストを扱うとき

## hash
- 7e920e91e709ef697599353052752757cd365e3d5cdbdabd50e15fc082ca7a13

# `test_oracle_review_loop.py`

## Summary
- oracle review の finding loop を検証するテスト群。対象 oracle ごとの finding 絞り込み、worktree 実行コンテキスト、challenger/advocate の reason 連携、割り込み時の部分結果保持、merge response の意味検証と再試行・失敗を確認する。

## Read this when
- oracle review の finding 列挙・検証・judge・merge loop の挙動を変更または調査するとき
- oracle review の worktree 分離、finding path の関連付け、割り込み時の結果保持を確認するとき
- merge の意味的な不正 response に対する再試行条件や上限を確認するとき

## Do not read this when
- oracle review の実装詳細ではなく、正本仕様そのものを確認したいときは oracle/doc/app_spec/sub_command/oracle_review.md を読む
- Codex 実行や Structured Output の一般規則だけを確認したいときは oracle/doc/app_spec/codex_exec_rule.md を直接読む
- finding loop と無関係なサブコマンドやテストの挙動を調査するとき

## hash
- 394574d8cff57158e33461e3fc952a467746b59691c50a8c024c8a1fd807243b

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
- oracle review の report 生成と CLI 出力を検証する realization test。レビュー対象 oracle file の列挙、Structured Output を用いた finding の判定、fatal/minor 別の report 構成・件数・path 集計、短縮 scope option、処理失敗・ユーザー中断時の report とログを扱う。oracle review の report 仕様や実装の変更時に、外部挙動を確認するテストの入口。

## Read this when
- oracle review の report 形式、finding の accepted/rejected 分類、scope option、エラー・中断時の出力を変更または検証するとき
- oracle review の report path 集計や oracle-root alias、symlink の扱いを確認するとき
- oracle review の agent call、Structured Output schema、失敗時の終了挙動をテストするとき

## Do not read this when
- oracle review の本体実装や正本仕様を確認する場合は、対応する sub_command 実装または oracle/doc を直接読むとき
- oracle review と無関係な CLI command、report、テストの変更を行うとき

## hash
- e6dc4654a5ab1078adb787c54ff6ec385a3114514c93f210456099eaac1ec6d5

# `test_oracle_review_targets.py`

## Summary
- oracle review の finding path 解決と oracle 対象列挙を検証するテスト。相対・絶対・{{work-root}} パス、symlink、追跡済み ignored file、session/full scope、fork commit、除外対象の扱いを確認する。

## Read this when
- oracle review の対象ファイル列挙、scope 判定、finding path 解決、symlink や git ignore の扱いを変更・調査するとき。
- oracle review の対象数、no_targets、review fork commit 基準の差分、AGENTS.md・INDEX.md 除外を検証するとき。

## Do not read this when
- oracle review の finding 内容生成やレポート形式だけを変更・調査するとき。
- oracle review 以外のサブコマンドや、対象列挙・パス解決に関係しない一般的なテストを扱うとき。

## hash
- 3f73d397fdc20b91268b9be1477c7421d87239f6a9c7e3fdc3d6044e34d0741f

# `test_oracle_review_worktree.py`

## Summary
- oracle review の worktree 分離、snapshot commit からの fork、未コミット差分の拒否、INDEX.md のみの統合、preflight 生成物の統合、INDEX.md の競合解決を検証する pytest。oracle review の実行結果、対象 worktree、branch、commit、report、差分制約を外部挙動として確認する。

## Read this when
- oracle review の run worktree、session branch、snapshot commit、oracle 対象範囲を変更または調査するとき
- oracle review による INDEX.md の生成・統合・競合解決や、INDEX.md 以外の差分拒否を変更または検証するとき
- oracle review の構造化出力、preflight、report の統合結果を確認するとき

## Do not read this when
- oracle review 以外のサブコマンドだけを変更・調査するとき
- INDEX.md の生成ロジック自体を直接変更・調査する場合は、まず indexing の実装・仕様・専用テストを読むとき
- Codex CLI や Ollama の一般的な出力品質のみを調査するとき

## hash
- d14f92b083f9460e6f538cc50ff0f907cf6dcb0fcb9e3a3e83949e3996f3fdbc

# `test_packaged_import.py`

## Summary
- packaged layout 上での import 境界と公開 API を検証するテスト。oracle review/edit builder、ACP basic、cmoc config のパッケージ配置・再公開・出力契約を扱う。

## Read this when
- packaged layout での Python import、setuptools の package 配置、oracle 定義の再公開、builder の prompt/schema 契約を変更または検証するとき。

## Do not read this when
- 個別 builder や config の実装詳細だけを変更・確認する場合は、まず対応する src または oracle 定義を直接読む。packaged import や公開境界に関係しないテスト変更では読まなくてよい。

## hash
- 00f7157da388231702a7d56a020bc45f861b8fb31ee4364d9def57bc769c5bdd

# `test_production_cli.py`

## Summary
- 実 Codex CLI と cmoc managed ollama を使い、独立 process・PTY 上で全末端サブコマンドの本番経路を受け入れ検証するテスト。終了 code、report・state・Git 状態、Codex call log、TUI の応答完了と終了を確認し、LLM の回答品質自体は判定しない。

## Read this when
- CLI の全末端サブコマンドが本番相当の独立 process 経路で動作するか確認するとき
- Codex call log、managed ollama 設定、session/run の状態遷移、report 生成、Git の副作用を横断して検証するとき
- TUI の PTY 起動、端末 capability query、応答完了、終了操作を調査・変更するとき

## Do not read this when
- 単一サブコマンドの内部実装や単体レベルのロジックだけを調べるとき
- LLM の回答内容や推論品質を評価するとき
- 実 Codex CLI・cmoc・managed ollama を使わないテストや、独立 process を必要としない検証を行うとき

## hash
- 5704045bd1e025830e6d57eb8cf446e989482cedb42b2eb15359d779e6bcc5a7

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

# `test_runtime_cli.py`

## Summary
- CLI の実行境界と共通ランタイム挙動を検証するテスト。error report の stdout 出力、サブコマンドログ、duration 表示、並列 logging、doctor/preflight、completion probe、work root 制約、gitignore 更新、worktree ごとの処理対象を扱う。runtime CLI・logging 実装や関連 oracle 仕様を確認する際のテスト入口。

## Read this when
- CLI の error 表示、終了コード、stdout/stderr 振り分けを変更・調査するとき
- サブコマンドログ、logger の並列性、timestamp 衝突、pre-log failure を変更・調査するとき
- doctor preflight、shell completion、work root 検証、gitignore 初期化、worktree の root 処理を変更・調査するとき
- CmocError、format_duration、ensure_cmoc_ignored、runtime_cli の挙動を検証するとき

## Do not read this when
- 個別サブコマンドの正常系ロジックや専用の oracle review/indexing/editing-run 挙動だけを変更・調査するときは、対応するサブコマンド実装・テストを直接読む
- oracle の正本仕様そのものを確認するときは、このテストではなく根拠として記載された oracle 文書・ソースを読む

## hash
- 294fabe8cabc50c83fe61c573dd0d34462342755545cba9a3fa719cc1dc4b80f

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
- CmocConfig の既定値、JSON 化時のメンバー順、設定ファイル未作成時の doctor 案内、設定値の型・値検証、falv recovery 試行回数の永続化を検証するテスト。runtime config の変更や不正入力時のエラー挙動を確認する入口。

## Read this when
- CmocConfig の既定値や Codex モデル・reasoning effort の対応を変更するとき
- config_from_dict、config_to_dict、load_config の入力検証・シリアライズ・未作成時エラーを変更するとき
- 設定 JSON のキー順や recovery 試行回数の扱いを確認するとき

## Do not read this when
- 設定値の実装詳細そのものを変更・調査する場合は、対応する src の設定実装と oracle file を直接読む
- 設定以外の runtime エラーや CLI コマンドの挙動だけを扱う場合

## hash
- 48056ebf5942aadf92e12af1d6492fbd64c87d527c9c48c91f3f78efac452332

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

# `test_runtime_refactor.py`

## Summary
- realization refactor の永続 state について、oracle・realization 対象集合との同期、調査履歴の保持、変更ファイルの再調査化、調査対象の優先選択、パス逸脱の拒否を検証するテスト。runtime_refactor の state 管理・対象選択実装を変更または検証する際の入口。

## Read this when
- refactor state の同期や読み書き、調査履歴の更新規則を変更・検証するとき
- 未調査対象や最古の調査対象を選ぶ優先順位を変更・検証するとき
- refactor state におけるパス逸脱などの不正入力処理を変更・検証するとき

## Do not read this when
- runtime_refactor の実装詳細を直接変更・調査する場合は、まず対応する実装ファイルを読むとき
- refactor state と無関係な CLI 機能やテストを扱うとき

## hash
- 9be17fbe6f0e1d3b704f7ba152cf8595674ecb695314d803d247b3a4ebd9a135

# `test_runtime_state.py`

## Summary
- session/run 状態スキーマの検証と managed branch 解析に関する realization test。branch 形式の妥当性、状態データの型・必須項目・未知 field の拒否、run branch からの session 特定、プロセス間で共有される session fork lock を検証する。

## Read this when
- session/run 状態ファイルの形式・バリデーション・読み込み挙動を変更または調査するとき
- managed branch の session ID 解析や run branch の扱いを変更するとき
- session fork lock のプロセス間排他を変更または検証するとき

## Do not read this when
- CLI 出力や実行フローのみを変更し、runtime state のスキーマ・branch 解析・fork lock に影響しないとき
- 対象機能の実装詳細を確認する必要があるときは、対応する realization implementation を直接読む

## hash
- 980bfcc59e1e7d64ec890a20c99358fe074377d9bb7a801582c28115f0d2705d

# `test_session_cli.py`

## Summary
- session の fork、join、abandon CLI における branch・state のライフサイクルを、外部出力と Git/worktree 状態を通じて検証する回帰テスト群。state cleanup、rollback、conflict resolution、dirty worktree 拒否、linked worktree 対応も扱う。

## Read this when
- session fork/join/abandon の挙動、session branch や state file の作成・更新・削除を確認するとき
- session の cleanup、rollback、事前条件、conflict resolution、linked worktree 対応を変更・検証するとき

## Do not read this when
- session CLI の実装詳細だけを確認したいときは、対応する session サブコマンド実装を直接読む
- doctor preprocess や Codex 実行規則そのものを確認したいときは、対応する oracle または実装を直接読む

## hash
- 4378202275cfc5b8b3dcf02fb6754c4f1a5e9f405d393cd4af7f8d01e7789a8c

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
