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

# `test_acp_builder_review_oracle_parameters.py`

## Summary
- review oracle ACP builder の parameter、schema、モデル設定、ファイルアクセスモード、互換公開面を検証する pytest テスト群。enumerate、merge、judge、advocate/challenger validation の canonical/互換 builder 間の一致、schema の oracle source との一致、placeholder・symlink・動的入力保持を確認する。

## Read this when
- review oracle builder の parameter や structured output schema を変更・追加・検証するとき
- review oracle 互換 module の公開 API、モデル選択、reasoning effort、file access mode を確認するとき
- oracle path placeholder、symlink entry path、既知 finding や動的入力の保持に関する挙動を調査するとき

## Do not read this when
- review oracle builder 以外の ACP builder や、builder の実装詳細そのものを直接調査するとき
- schema の正本定義を確認する場合は、このテストではなく対応する oracle schema を読むとき
- テスト実行方法や Python 環境の確認だけが目的のとき

## hash
- 2aef081f6cc54d60e540b9ad798d3b0d6ab4b4012356a4012c0195a52b17226f

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
- TUI の resolve parameter builder と関連 schema を検証するテスト。元の prompt および標準ルールが生成 prompt に埋め込まれること、モデル・推論・アクセスモード・schema path が適切であることを確認する。
- schema の必須項目、追加プロパティ禁止、logical enum 値、boolean flag の構造を検証する。
- 互換 module の公開 API が必要な名前だけを提供し、旧 renderer を公開しないことを確認する。

## Read this when
- TUI resolve parameter の prompt 埋め込み、出力 parameter、structured-output schema、または module の公開 API を変更・検証するとき。

## Do not read this when
- TUI 以外の builder や、resolve parameter と無関係な CLI/TUI 動作を調査するとき。

## hash
- 232eb1d17ac4317f19df655b083f411b4ba54e3add76a732b4c86bdb139b2b6f

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

# `test_cli_tui.py`

## Summary
- TUI 起動直前の CLI 前処理を外部挙動から検証するテスト。編集済みプロンプトの解決、Codex パラメータ、ログ・ignore 配置、既定値、linked worktree での保存先を扱う。TUI サブコマンドの前処理や関連テストを確認する入口。

## Read this when
- TUI サブコマンドの前処理・プロンプト編集・Codex 起動連携を変更またはレビューするとき
- TUI のログ保存先、ignore 設定、linked worktree 対応、ファイルアクセス既定値の挙動を確認するとき
- TUI 起動に関する外部挙動の回帰テストを追加・修正するとき

## Do not read this when
- TUI の内部実装を直接変更・調査する場合は、まず TUI サブコマンド実装と正本仕様を読むとき
- TUI と無関係な CLI サブコマンド、共通ライブラリ、または Codex 出力品質だけを調査するとき

## hash
- ffd4116cbf2131c02c6f5795cc4939c79297106b9ad9d0df19b954ce9bb60478

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
- Codex TUI 実行ラッパーの振る舞いを検証する pytest。prompt の読み込みとアクセス境界、Codex CLI 引数、成功・失敗時の call log／サブコマンドイベント／コンソール出力、timestamp 衝突時のログ保持、CLI 不在・KeyboardInterrupt・非 0 終了を扱う。TUI 実行や Codex 呼び出しログの変更を検証するテスト入口。

## Read this when
- `run_codex_tui` の prompt 読み込み、sandbox／approval 引数、worktree 対応を変更または調査するとき
- Codex TUI 呼び出しの成功・失敗ログ、終了コード、例外処理、コンソール要約を変更または検証するとき
- TUI call log のファイル名衝突や保存内容を扱うとき

## Do not read this when
- Codex TUI の実装詳細そのものを変更・調査する場合は、まず対応する `src` 実装を読む
- TUI 以外の Codex 実行経路や、Codex 出力品質そのものを扱う場合

## hash
- fae628de6565f8b56407d6ab5f3016ac86da600072856e165d760970ae624202

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
- Codex 呼び出し前の indexing preflight を検証するテスト。exec/TUI 経路での実行順序、linked worktree の選択、repository lock 待機、パラメータによる無効化、file access violation 後の recovery indexing 禁止を、git 状態や外部呼び出しの観測を通じて確認する。

## Read this when
- indexing preflight の実行条件・実行順序・lock 制御を変更またはレビューするとき
- Codex exec/TUI 呼び出しと linked worktree の indexing 対象の関係を確認するとき
- file access violation 後に recovery 処理を追加・変更するとき

## Do not read this when
- INDEX.md 生成処理そのものの仕様や実装を確認したいときは、indexing 実装および対応する oracle file を直接読む
- Codex 呼び出し経路と無関係なテストや機能を調査するとき

## hash
- 01f64b45368fc2e43171f5b0089eb952c53d26d45c3a1cfe1a6efc93282f6f18

# `test_packaged_import.py`

## Summary
- packaged layout での import 境界と公開面の崩れを検証するテスト群。oracle 側の正本定義が配布形態でもそのまま参照され、`acp.builder` と `config` の公開 import が余計な実装を漏らさないことを確認したいときに読む。

## Read this when
- packaged layout を前提にした import 失敗や公開漏れの回帰を確認したい。
- oracle 側の定義を複製せずに再公開しているか、または配布後の環境でも正本を参照できるかを確かめたい。

## Do not read this when
- 通常の単体ロジックや CLI 挙動だけを確認したい。
- packaged layout ではなく通常のソースツリー上の内部実装を追いたい。
- 個別の builder 実装や config 定義の内容そのものを読みたい。

## hash
- 52612d997cee015efa9da672fc11c668e6ed407722cc2e0d7c56dcab87cd5e1b

# `test_production_cli.py`

## Summary
- 全末端サブコマンドを、実 CLI・独立プロセス・実 Codex CLI・cmoc managed Ollama を用いた本番相当の受け入れ試験で検証するテスト。非対話コマンドの終了 code、report・state・Git・call log と、TUI の PTY 上の応答完了・終了処理を確認する。LLM の回答品質自体は判定しない。

## Read this when
- CLI の全末端サブコマンドに対する本番経路テストを追加・変更・レビューするとき
- 独立プロセス、実 Codex CLI、managed Ollama、call log、report、state、Git の外部観測を確認するとき
- TUI の PTY 操作、端末 capability query、応答完了判定、Ctrl-C による終了処理を調べるとき

## Do not read this when
- 単一サブコマンドの内部実装や単体テストだけを変更・調査するときは、対応する src またはより直接的な test を読む
- LLM の回答品質やプロンプト内容そのものを評価するときは、このテストを読む対象にしない

## hash
- cdb20f1c796df65461652aa6fd381c97693cb45080507cd9b094921ba26473fe

# `test_prompt_parts.py`

## Summary
- 標準 prompt parts と complete prompt の組み立て結果を検証する pytest テスト。各標準ルールのタイトル・主要文言・出力境界、complete prompt への注入条件、root token の保持、既定時の省略を確認する。prompt 部品や complete prompt の挙動を変更・調査する際のテスト入口。

## Read this when
- prompt parts の標準ルール、file access rule、routing rule、INDEX entry standard、realization standard、review standard の検証内容を確認するとき
- complete prompt が各標準ルールを含む条件や、既定時に省略する条件を確認するとき
- root token や oracle file path のコメント規則が prompt に保持されることを確認するとき
- prompt builder 周辺の実装変更による回帰を検証するとき

## Do not read this when
- prompt builder の実装詳細だけを調査するときは、対応する src の prompt 部品または complete prompt 実装を直接読む
- INDEX.md のルーティング仕様そのものを確認するときは、index entry standard の正本を直接読む
- prompt 部品と無関係な CLI 機能やテストを調査・変更するとき

## hash
- d4d1bd7b98cd89415697a6c25264ed1a0795f8a64802d3de261f2ad988c92d36

# `test_review_oracle_loop.py`

## Summary
- review oracle の finding loop を検証するテスト。対象 oracle ごとの finding 分離、検証周回の reason 引き継ぎ、中断時の部分結果保持、merge response の意味検証と再試行・失敗を確認する。隔離 worktree と Codex Structured Output の呼び出しコンテキストも検証する。

## Read this when
- review oracle の finding 列挙・merge・validate・judge loop の挙動を変更または調査するとき
- review agent call の repo root、cwd、worktree 分離を確認するとき
- merge の意味的失敗時の再試行や KeyboardInterrupt 時の結果保持を確認するとき

## Do not read this when
- review oracle loop のテスト対象ではなく、通常の review oracle 実装や prompt 定義だけを確認するとき
- finding schema や設定値の正本仕様を確認したいときは、記載された oracle doc・oracle src を直接読む

## hash
- 0e5acc2c069f56295d9a53f6e7a5780a71a1700f036eebcd82e67e374deb71c1

# `test_review_oracle_merge_operations.py`

## Summary
- `cmoc review oracle` の所見マージ操作の契約を検証するテスト。`delete` / `replace` / `merge` の対象指定や payload 制約、同じ `finding_id` の再利用禁止を確認したいときに読む。

## Read this when
- 所見リストを `delete` / `replace` / `merge` で整理する挙動の契約を確認したいとき。
- merge 操作の入力検証や、複数 operation 間で同じ `finding_id` を再利用した場合の拒否条件を確認したいとき。
- `cmoc review oracle` の所見マージ周辺のテスト追加・修正をするとき。

## Do not read this when
- 所見の列挙・検証・判定の契約を見たいときは、より直接に `review oracle` 本体側の仕様や実装を読む。
- `cmoc review oracle` 全体の実行手順や report 体裁を確認したいだけなら、このテストではなく `review oracle` の正本仕様を読む。
- テスト規約全般を確認したいだけなら、この個別テストではなくテスト方針側を読む。

## hash
- 8f58e561044e98e048ad9d7fcfa64b2d72f97670424a7999f6ed86968dd03976

# `test_review_oracle_report.py`

## Summary
- review oracle の report 生成と CLI 出力を検証するテスト。中断時の評価済み oracle の扱い、eval-oracle の委譲、report の節順・件数・finding 分類、path alias や symlink の集計、短縮 scope option、処理失敗時の error report を対象とする。review oracle や関連 CLI の挙動を変更・調査する際のテスト入口。

## Read this when
- oracle review の report 形式、finding の accepted/rejected 分類、scope option、中断・失敗時の出力挙動を確認するとき
- review oracle または eval-oracle の実装を変更し、既存の外部挙動への影響を検証するとき
- review oracle 関連テストの失敗原因を調査するとき

## Do not read this when
- review oracle の内部実装そのものを確認したい場合は、まず対応する実装モジュールと oracle 文書を読むとき
- oracle review と無関係な CLI、設定、git、session 機能を変更・調査するとき

## hash
- ee0819916396779ffded41b3248ad9f29a8261663dbc9599bdfd2761a3ba6af6

# `test_review_oracle_targets.py`

## Summary
- review oracle の finding path 解決と oracle 対象列挙を検証するテスト。相対・placeholder・絶対 symlink の path 処理、外部 oracle path の除外、full/session scope の対象数・変更範囲・Codex 呼び出し、AGENTS.md/INDEX.md の除外、symlink の repository path 分類を扱う。review oracle の対象判定や scope 差分挙動を変更・調査する際の検証入口。

## Read this when
- oracle review の対象列挙、scope、review fork commit、追跡済み ignored oracle file、symlink、finding path 解決を変更または調査するとき
- review oracle コマンドの対象数、no_targets 結果、Codex 呼び出し条件を検証するとき

## Do not read this when
- review oracle の実装や path helper の変更と無関係なテスト・機能を扱うとき
- CLI 共通 runner、git fixture、Ollama doctor の詳細を直接調査する場合は、それぞれの support module を先に読む

## hash
- f4db5d51daccf3bc0597680b4514cf8a684fe8826d3b1e4b664d87616319db03

# `test_review_oracle_worktree.py`

## Summary
- review oracle の worktree 分離・ブランチ／oracle 対象選択・未コミット変更拒否を検証するテスト。
- review worktree で生成された INDEX.md と preflight の INDEX.md を session に統合し、INDEX.md の削除競合を解決できることを検証する。
- review worktree が INDEX.md 以外を変更した場合に拒否することを、未追跡・未ステージ・ステージ済みの各状態で検証する。

## Read this when
- oracle review の worktree 分離、session branch、レビュー対象 commit の挙動を変更・確認するとき
- oracle review と INDEX.md 更新・統合・競合解決の連携を変更・確認するとき
- review worktree の変更検証や、INDEX.md 以外の差分拒否を変更・確認するとき

## Do not read this when
- oracle review の実装詳細ではなく、INDEX.md 生成単体の仕様や実装を確認するだけのとき
- session fork や branch model の一般仕様を確認するだけで、review oracle の統合挙動を扱わないとき

## hash
- a0bc66d6d4148c84c2bd2309d215162fcc5f0f2e16493317e45582b996f285e6

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
- CLI 実行基盤の外部挙動を検証するテスト。duration 表示、サブコマンドログの衝突・並列記録・失敗時記録、構造化エラー出力、CLI 解析エラー、work root 制約、completion probe の副作用抑制、preflight と .gitignore 更新、worktree ごとの処理対象を扱う。runtime_cli・runtime_logging・cmoc_runtime・CLI 全体の変更時に、対応する挙動確認の入口となる。

## Read this when
- CLI のエラー表示、終了コード、stdout/stderr 境界を変更・調査するとき
- サブコマンドログ、doctor/pre-log check、completion probe のライフサイクルや副作用を変更・調査するとき
- work root・worktree 判定、.cmoc の ignore 設定、duration 表示を変更・調査するとき

## Do not read this when
- 特定サブコマンドの業務ロジックや oracle 文書の内容だけを確認する場合
- CLI 基盤のログ・エラー・preflight・completion 挙動に関係しないテストや実装を変更する場合

## hash
- ecf9e8998a2ea19ef522f934c0054edbdc808963c03c91b8e03cc3145a18c627

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
- CmocConfig の既定値、JSON 化時の定義順、設定ファイルの読み込み、入力値の型・内容検証、Codex の recovery 試行回数の保持を検証するテスト。設定ランタイムや CmocConfig の挙動を変更・確認する際の入口。

## Read this when
- CmocConfig の既定値や Codex model・reasoning effort の対応を変更するとき
- 設定の JSON 入出力、欠落時エラー、section・map・数値項目の入力検証を変更するとき
- 設定ランタイムのエラー案内や recovery 試行回数の保持を確認するとき

## Do not read this when
- 設定機能の実装詳細を直接確認する必要があるときは、テストの根拠として示された oracle src や設定実装を先に読むとき
- 設定とは無関係な CLI、fork、oracle review、ACP の挙動だけを調査するとき

## hash
- a39a98af225c33ce88ae6a34c67d4e27e2f9836cdffaec3607d38cf1659c4f55

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
