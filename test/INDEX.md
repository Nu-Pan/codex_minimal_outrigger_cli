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
- doctor CLI を対象 worktree のカレントディレクトリで実行するテスト支援関数を提供する。doctor サブコマンドの CLI テストで、実行結果の成功確認と参照に使う共通入口。

## Read this when
- doctor CLI の実行結果をテストから取得したいとき
- 対象 worktree をカレントディレクトリとして CLI を実行するテストを追加・変更するとき

## Do not read this when
- doctor CLI の仕様や前処理の正本を確認したいときは、対応する oracle doc を直接読む
- doctor CLI 以外のテスト支援や CLI 実行処理を変更するとき

## hash
- 04ee47c861ffe5b25223ffec1083362f42f865aca8b550498bd0a06378362cf0

# `_codex_support.py`

## Summary
- テストで共通利用する Codex 実行用の補助関数と最小ダブルを提供する。認証に依存しない一時環境の準備、既定の呼び出しパラメータ生成、CLI 引数からの値・設定抽出、実行制御の override 差し替えをまとめたテスト支援の入口。

## Read this when
- Codex 実行ラッパーや TUI のテストで、共通の呼び出しパラメータ・一時ホーム・CLI override・Structured Output のテストダブルが必要なとき。

## Do not read this when
- 対象の本番実装の挙動や Codex CLI の実際の仕様を確認したいとき。個別テストの検証内容だけを読む場合は、各テストファイルへ直接進む。

## hash
- 5453104f8f54bd043468ac6d161ae7571a7728f86feb7b5482b74cebaa941032

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
- 実経路統合テストで subprocess を起動する際の Python 起動時フックを扱う。対象ディレクトリを PYTHONPATH に追加した場合に、AgentCallParameter のモデル種別と推論強度をテスト用の最小・低設定へ置き換える仕組みへの入口。

## Read this when
- 実経路統合テストの subprocess 環境で、モデル設定がテスト専用値へ変更される仕組みを確認するとき
- 実経路統合テスト実行時の Python 起動フックや AgentCallParameter 初期化差し替えを調査するとき

## Do not read this when
- 通常の AgentCallParameter 設定や builder 実装を確認するとき
- 実経路統合テスト以外の subprocess 起動設定、または個別テストケースの期待動作を調査するとき

## hash
- cd158f0a4b49c6dd806a540691cca3df68de44ef6ee184bb1b82cd0a36a41bbc

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
- editing run workload における canonical builder adapter の互換 import、実行設定、prompt 埋め込み、raw diff の境界保持、Structured Output schema の選択を検証するテスト。apply/refactor fork の builder 実装や対応する oracle builder・schema の変更、またはこれらの検証失敗を調査するときの入口。

## Read this when
- editing run 用 builder の互換再公開が canonical builder と同一関数であることを確認するとき
- apply/refactor builder のモデル設定、ファイルアクセス、preflight、worktree、prompt 内容、raw diff の境界処理を検証するとき
- refactor builder が指定された canonical Structured Output schema と postcondition を使用しているか確認するとき

## Do not read this when
- builder の実装や oracle file 自体を直接変更・調査する場合は、対応する実装または oracle file を直接読むとき
- editing run workload、acp builder、apply/refactor fork の挙動に関係しないテストや文書を扱うとき

## hash
- 3bc4b08473cd2f6e3be79e748105250ba3480ff74331e302567fde338af7ac0c

# `test_acp_builder_indexing_parameters.py`

## Summary
- indexing の index entry builder に対する parameter 選択、Structured Output schema の必須条件、対象本文のコードフェンス保護、および互換 module の公開面を検証するテスト。builder の実装や対応する oracle との互換性を確認する際の入口となる。

## Read this when
- index entry builder の model・reasoning・file access・実行条件を変更または検証するとき
- index entry 用 Structured Output schema の semantic 配列の必須条件を変更または検証するとき
- 対象本文を prompt に埋め込む際のコードフェンス処理を変更または検証するとき
- index entry 互換 module の公開 API を変更または検証するとき

## Do not read this when
- oracle 側の正本実装や schema の内容そのものを確認するだけの場合
- index entry builder と無関係な agent call parameter、prompt、またはテストを扱う場合

## hash
- 0e8df1b4cbc4d9a2c884091a7f661a58a263627c19b878b82743f688fb36b6fb

# `test_acp_builder_oracle_review_parameters.py`

## Summary
- oracle review ACP builder 群の回帰テスト。各 builder の AgentCallParameter、モデル・推論設定、file access、schema、canonical builder との互換性、動的 prompt の placeholder と code fence 保護を検証する。review builder の公開面と共有する所見判定規範を確認する入口となる。

## Read this when
- oracle review の enumerate、judge、merge、validate builder の parameter や Structured Output schema の互換性を検証するとき
- review builder の公開 export、動的入力の保持、prompt section 境界、nested code fence 保護の挙動を変更または調査するとき
- 複数の review builder に共通する所見判定規範や canonical builder との一致を確認するとき

## Do not read this when
- review builder 本体の実装責務や prompt の正本仕様を確認する場合は、対応する realization または oracle file を直接読む
- review builder と無関係な ACP builder、schema、またはテストの作業を行うとき
- 単一 builder の詳細な仕様だけを確認する場合は、対象 builder の実装・schema の直接確認で足りるとき

## hash
- 0831e9890a585044c9392b90cdf922c55f340b56fc8fa5230e81b0086acc8047

# `test_acp_builder_session_join_parameters.py`

## Summary
- session join の conflict resolution builder 契約を検証するテスト。互換モジュールの公開 API が単一 builder へ限定されること、canonical builder との同一性、repo write 用の起動パラメータ、conflict 対象ファイルを含む prompt、routing rule、preflight 無効化、および三連 backtick を含む path の code fence 保護を扱う。

## Read this when
- session join の conflict resolution builder の公開 API や canonical builder との互換性を確認・変更するとき。
- conflict 解消用 agent call のモデル、推論強度、ファイルアクセス権限、作業ディレクトリ、prompt 構成、structured output、indexing preflight の契約を確認するとき。
- conflict 対象 path の prompt 埋め込みで code fence 境界が壊れないことを検証するとき。

## Do not read this when
- session join の conflict 解消ではなく、通常の session join 処理や別の builder の契約だけを確認するとき。
- builder の実装契約を確認せず、一般的な pytest fixture や repository test helper の使い方だけを調べるとき。

## hash
- 2b8d7e4020839c3ba4f7c25a093420db75c67ff702697344f94759929333ccb0

# `test_acp_builder_tui_parameters.py`

## Summary
- TUI 起動 builder の parameter 生成を検証するテストで、固定された agent call 種別・モデル・推論強度・ファイルアクセスモード・実行ディレクトリ・indexing preflight と、元の prompt を含む完了 prompt の規範および routing 条件を確認する。
- 互換 module の公開面が現行の TUI 起動 builder 関数だけであることを検証する。

## Read this when
- TUI 起動 builder の固定実行設定や prompt の生成内容を変更・検証するとき
- TUI 起動 builder の互換 module における公開シンボルを変更・検証するとき

## Do not read this when
- TUI 起動 builder の実装仕様を確認する場合は、対応する正本 implementation を直接読むとき
- TUI 以外の builder の parameter や公開面を確認するとき

## hash
- 86510f74d74f3edfe07400a313d87b630a2efbc47dbd6203fab027e940ab18d7

# `test_basic_runtime.py`

## Summary
- Root/worktree と path model の runtime 契約を検証するテスト。リポジトリ root・linked worktree・run worktree の識別、placeholder path の解決、並列 call と process-wide cwd の分離、memo 判定、Git 設定の隔離、および managed worktree の作成・検索・削除におけるパス境界と symlink・登録状態の拒否を扱う。runtime の path model や run isolation の挙動を確認する際のテスト入口である。

## Read this when
- root/worktree の解決や placeholder path の復元を変更・検証するとき
- 並列 agent call、pushd、process-wide cwd の直列化を変更・検証するとき
- run worktree の管理領域、branch 対応、Git 登録、symlink 安全性、作成・検索・削除の境界を変更・検証するとき
- test repository が global Git 設定の影響を受けないことを確認するとき

## Do not read this when
- path model や worktree runtime の実装詳細を直接確認する必要があり、対応する実装・oracle 文書を読むべきとき
- 上記の runtime 契約と無関係な CLI 機能、仕様、テストを調べるとき

## hash
- 27f3127d15fa0b68c3734967082fa6daffc5b2ca1abfa068accc88afc204537a

# `test_cli_command_tree.py`

## Summary
- 公開 CLI の末端コマンド集合と、Typer/Click の互換性を検証するテスト。CLI ヘルプの描画、および feedback report が固有の引数・オプションを公開しない契約も扱う。CLI コマンド構成や公開 leaf の正本仕様を確認・変更するときの検証入口となる。

## Read this when
- 公開 CLI のコマンド階層、末端コマンド集合、またはコマンド公開契約を変更・確認するとき
- Typer/Click の互換性による help 描画エラーを調査するとき
- feedback report の引数・オプション公開を確認するとき

## Do not read this when
- CLI の個別サブコマンドの詳細な挙動や引数仕様を確認したいとき
- CLI と無関係なテストや実装を調査するとき
- 公開コマンド構成を変更せず、個別コマンドの内部ロジックだけを確認するとき

## hash
- 783df6423bc0c96b9a77d81e1fb9c5bb1117943ba64153810b73d5ea5701a3d6

# `test_cli_tui.py`

## Summary
- TUI 起動直前の CLI 前処理を、実際の Codex TUI 起動まで含めて検証するテスト。
- 編集済み prompt の生成、doctor preprocess の実行順序、起動パラメータ、prompt の保存内容、既存の Git 差分保持を確認する。
- linked worktree では prompt と agent call context をメイン worktree 側へ保存し、repository と linked worktree の `.cmoc` ignore を保証する挙動も検証する。

## Read this when
- `tui` サブコマンドの起動前処理、prompt editor の入出力、Codex TUI 起動パラメータを変更または検証するとき
- linked worktree におけるログ・prompt 保存先や `.cmoc/gu` の ignore 挙動を変更または検証するとき
- TUI 起動時に既存の staged・unstaged 差分を保持する契約を確認するとき

## Do not read this when
- TUI 起動前処理の外部挙動ではなく、TUI 本体の対話処理や表示を直接確認するとき
- prompt builder や CLI 実装の内部詳細だけを確認し、実行時の統合挙動を検証する必要がないとき
- TUI と無関係なサブコマンドやログ処理を確認するとき

## hash
- e80214f02e2708d1a7de8188de43657846e328becce326f2db2b48ca8bd33d7c

# `test_codex_runtime_errors.py`

## Summary
- Codex 実行時の異常系を検証する pytest。JSONL の不正・非 object event、終了コード 0 でも不正出力となるケース、Codex CLI 不在時の例外と失敗ログ、相対 call log path の表示を対象とする。Codex 実行処理・ログ出力・エラー分類の挙動を確認するテストの入口。

## Read this when
- Codex JSONL parser の異常系や malformed event の扱いを変更・調査するとき
- Codex CLI 不在時や実行失敗時の CmocError、コンソール表示、JSONL ログを変更・調査するとき
- Codex call log path の表示形式や失敗イベントの記録を確認するとき

## Do not read this when
- Codex の正常系実行フローだけを変更・調査するとき
- Codex 以外のサブコマンド、ログ、設定のテストを読む必要があるとき
- 実装ではなく正本仕様そのものを確認するときは、対応する oracle doc を直接読む

## hash
- 8be1a60b6bab0eda51507f3de2641061e501230807b4e2390aba3015a1353951

# `test_codex_runtime_exec.py`

## Summary
- Codex CLI 実行ランタイムのテストを集約し、実行時の argv、stdin、作業ディレクトリ、sandbox・approval override、出力保存、リポジトリ書き込み、および CODEX_HOME 設定ファイル非生成を検証する。
- 汎用 model provider の override が適用され、組み込み local provider 用フラグを使わないことを確認する。
- Codex 実行処理や override 引数生成の挙動を変更・調査するときのテスト入口であり、Codex CLI の仕様そのものや provider 設定の正本を確認する場合は参照先として示された oracle 文書を直接読む。

## Read this when
- Codex exec の起動引数、stdin 渡し、sandbox・approval 設定、出力処理、作業ディレクトリ、または CODEX_HOME の扱いを変更・検証するとき。
- Codex model provider の汎用 override や local provider 用 CLI フラグ不使用の挙動を確認するとき。
- Codex 実行ランタイムの回帰テスト対象を特定するとき。

## Do not read this when
- Codex CLI や model provider の正本仕様を確認することが目的で、テスト実装を調べる必要がないとき。
- Codex 実行以外の機能、または共通 test helper 自体の責務を直接調べるとき。

## hash
- c17774b35f2d0061f459a32b6d3670b3d6ed0ddcdf61cb161486155629318994

# `test_codex_runtime_home.py`

## Summary
- Codex 実行時の CODEX_HOME 解決・検証と、Codex subprocess への環境・作業ディレクトリ引き渡しを検証するテスト。欠落・非ディレクトリの home を subprocess 起動前に拒否すること、および auth.json の provider 固有スキーマを前提にしないことを確認する。Codex runtime 実装の挙動変更時に参照するテスト入口。

## Read this when
- CODEX_HOME の既定値・環境変数値・相対パス解決を変更するとき
- Codex subprocess の起動前 preflight、環境変数、working directory、call log の挙動を変更するとき
- Codex home の存在・ディレクトリ検証や auth.json の扱いを変更するとき

## Do not read this when
- Codex runtime の home 解決・検証・subprocess 引き渡しに関係しない機能を変更するとき
- テスト実行方法や共通テストヘルパー自体を確認したいときは、対応する実装・共通ヘルパーを直接読む

## hash
- 90644336a4ff674ab3cec2a17d849dc6a717d45a37d1856b96b47308712584d9

# `test_codex_runtime_paths.py`

## Summary
- Codex 実行ランタイムのパス・実行環境を検証するテスト。並列実行時の timestamp 付きログパス予約、指定 cwd の伝播、schema の repo root 配下への保存、ファイルアクセスモードに応じた sandbox 引数、不要な `.agents` 権限注入の不在を確認する。

## Read this when
- `run_codex_exec` の cwd、ログ・schema 出力先、worktree 対応、sandbox 引数、ファイルアクセス権限の挙動を変更または検証するとき。
- Codex 実行のプロセス安全なパス予約や linked worktree での実行結果を調査するとき。

## Do not read this when
- Codex 実行ランタイムのパスや sandbox、ファイルアクセスモードに関係しないテスト・実装を扱うとき。
- Codex のプロンプト生成内容や oracle 仕様そのものを確認する場合は、対応する oracle 文書・実装を直接読む。

## hash
- 204353289cbb77f77b0b1d9131c18217ba2246bf5dc9b5ca3b5afeaf730361b6

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex quota 超過後の probe・待機・復帰・resume／再実行を検証する回帰テスト。代表 probe の共有、session ID 復元、失敗伝播、並行呼び出し、call log・subcommand log、Codex の cwd／CODEX_HOME まで、同一 retry 状態機械の観測点を一体として扱う。quota 待機からの復帰挙動を確認する際の入口となる。

## Read this when
- Codex exec の quota 超過後に、probe の実行条件、待機回数、resume または再実行の選択を確認するとき
- quota probe の失敗・不正な stdout・KeyboardInterrupt・並行呼び出しへの伝播を検証または変更するとき
- quota retry に関する call log、subcommand log、session ID、cwd、CODEX_HOME の外部挙動を確認するとき

## Do not read this when
- 通常の Codex exec 成功経路や quota と無関係な subprocess 実行を確認するとき
- quota probe の prompt 生成仕様そのものを確認するときは、正本の probe builder や Codex exec 仕様を直接読む
- quota retry 実装の内部構造や一般的なテスト実行方法だけを確認するとき

## hash
- eb94cd7a82986cb0906b8fc91d9e3229338afd5a95b83015686612c57e4054e1

# `test_codex_runtime_retry.py`

## Summary
- Codex exec の retry と失敗時ログを検証するテスト群。Structured Output の出力補正、capacity retry、JSONL error、中断、retry 上限、差分保持を、fake subprocess の最終結果・呼び出し回数・call log・subcommand event まで含む外部挙動として一続きに確認する。
- run_codex_exec の retry 状態と共有ログ schema を同じ読み取り文脈で検証するためのテスト入口であり、異常系を個別の責務へ分割せず扱う。

## Read this when
- run_codex_exec の Structured Output 検証失敗、出力補正、capacity retry、未知の JSONL error、中断、retry 上限、または補正時の成果物差分保持を変更・検証するとき
- Codex subprocess の呼び出し回数、session 継続、call log、codex_call event、subcommand event の対応を確認するとき
- fake Codex の応答から最終結果とログ列までを外部挙動として検証するテストを追加・変更するとき

## Do not read this when
- Codex exec の通常成功経路だけを確認するとき
- retry や失敗時ログに関係しない別の runtime 機能を調査するとき
- run_codex_exec の実装責務や正本仕様そのものを確認する必要があり、テスト本文ではなく実装・仕様を直接読むべきとき

## hash
- 173c657a24987edd03acd7527f1104695e6c1e2434795510050b6903618c0559

# `test_codex_runtime_subprocess.py`

## Summary
- Codex subprocess と run process tracking の停止・追跡・cleanup を検証する pytest テスト群。pidfd が使えない場合や PID/PGID 再利用、leader 終了後の descendant、壊れた tracking、signal 割り込み、cleanup 失敗時の kill/reap など、安全側に倒す停止経路を対象とする。Codex 起動時の tracking 環境変数、起動 callback、cwd エラー、tracking path の symlink/FIFO 拒否も検証する。runtime_codex_profile と runtime_run の process identity・group cleanup 実装を変更または検証する際の入口。

## Read this when
- Codex subprocess の process group、pidfd、signal、tracking file、PID/PGID の同一性検証や cleanup 挙動を変更・調査するとき
- run process tracking の不正入力、特殊ファイル、PID 再利用、起動失敗・中断時の安全性を確認するとき
- runtime_codex_profile.run_tracked_codex_subprocess または runtime_run.stop_child_process_group/stop_run_process の回帰を検証するとき

## Do not read this when
- Codex subprocess の停止・追跡や run process tracking に関係しない CLI 機能を変更・調査するとき
- 実装の詳細や正本仕様そのものを確認する必要があり、対応する runtime モジュールまたは Oracle 文書を直接読むべきとき
- 単純なテスト実行結果の確認だけで、対象テストのケース構成を調べる必要がないとき

## hash
- 1a1d122c406117b8779a5809b3f3b8aaa350d53e3c37fc0830d7e3527cc17540

# `test_codex_runtime_tui.py`

## Summary
- Codex TUI の実行を検証するテスト群。完成済み prompt の読み込み、アクセスモードと CLI 引数、linked worktree での実行、成功時の call log・サブコマンドイベント・コンソール要約を扱う。
- Codex CLI 不在、KeyboardInterrupt、非 0 終了、および timestamp 衝突時の失敗記録と call log 保持を確認する。TUI 実装の詳細や一般的な CLI 仕様の入口ではなく、これらの外部挙動をテストから確認するときに読む。

## Read this when
- Codex TUI 呼び出しの prompt・アクセス境界・CLI 引数が期待どおりか確認するとき。
- TUI の成功・CLI 不在・割り込み・非 0 終了における call log、サブコマンドイベント、コンソール出力の検証内容を確認するとき。
- 同一 timestamp の呼び出しで call log が上書きされないことを確認するとき。

## Do not read this when
- Codex TUI の実装を変更または調査する場合は、まず実装側の対象を読む。
- prompt 生成規則、Codex 実行規則、ログ仕様そのものを確認する場合は、各 oracle 文書を直接読む。
- TUI と無関係な Codex 実行経路やテスト対象を確認する場合。

## hash
- 9c9a1dbf05e2fa9409dee9cdbd2511b83ee39f453c19ac6aef801116f969e919

# `test_doctor_cli.py`

## Summary
- doctor preprocess の外部契約を検証する統合テスト。CLI と直接呼び出しの双方を対象に、Git 状態・config・refactor state・`.cmoc/gu`・`.agents` の修復、修復順序、reporter の degraded/error 挙動、共有 lock、linked worktree の境界を一続きの lifecycle として確認する。
- 修復 commit が既存の staged 変更、unstaged hunk、rename、削除、index flag、intent-to-add を壊さず保持すること、および symlink 経由の危険な書き込みを拒否することを検証する。doctor preprocess 実装や関連 fixture・補助関数を調べる際の入口となる。

## Read this when
- doctor preprocess の CLI または直接呼び出し時の外部挙動を変更・検証するとき
- `.cmoc/gu`、`.agents`、config、refactor state、Git index の修復・commit・lock・linked worktree 挙動を確認するとき
- reporter の利用不能、割り込み、予期しないエラー、および修復失敗時の扱いを確認するとき
- doctor の修復が既存の staged/unstaged 変更や index metadata を保持することをテスト・レビューするとき

## Do not read this when
- doctor preprocess の外部契約ではなく、個別の低レベル Git ヘルパーや reporter 実装そのものだけを調べるときは、対応する実装・単体テストへ直接進む
- doctor 以外の CLI サブコマンドや、config・refactor state の一般仕様だけを確認するとき
- 統合 fixture、linked worktree、共有 doctor lock、修復 commit の lifecycle に関係しないテストを探すとき

## hash
- bf4dcb898410aa130156f066e408bac5941e91a1773d4e5007e083412e9aac45

# `test_editing_run_cli.py`

## Summary
- workload fork と共通 run lifecycle の統合 realization test を扱う。apply/refactor fork、run join/abandon、session state、run worktree、Git 差分、process tracking、report、割り込み・失敗時の rollback と cleanup を、共有 fixture と CLI 呼び出しで検証する。
- 同じ editing run lifecycle の状態遷移と resource cleanup を横断して確認するため、個別 subcommand の単体テストではなく、fork から join/abandon までの統合挙動を調べる入口となる。

## Read this when
- realization apply fork または realization refactor fork の run 公開、agent 境界、INDEX refresh、commit、joinable/error 遷移を変更・調査するとき
- run join または run abandon の merge、force-resolve、worktree・branch cleanup、state rollback、report 更新を変更・調査するとき
- Codex child の process tracking、停止順序、遅延書き込み・遅延 commit、cleanup warning の挙動を変更・調査するとき
- oracle・INDEX・managed state・rename/delete を含む run 差分の許可判定や rollback を変更・調査するとき
- user interruption、起動途中の失敗、差分検査・report 保存失敗など、editing run の異常系 lifecycle を検証するとき

## Do not read this when
- fork・join・abandon の lifecycle や共通 state を扱わず、単一 helper の局所的な仕様だけを確認するとき
- CLI の通常出力形式や個別の Structured Output schema だけを確認するとき
- INDEX 生成そのもののアルゴリズムや oracle の正本仕様を確認するときは、それぞれの実装・仕様対象を直接読む

## hash
- 86efec0e5383ed25f4663398be5f3c32f9931a9824522afce9d1a6b09998c41f

# `test_feedback.py`

## Summary
- feedback の observation reporter、raw store、report cut、Codex による issue 正規化・検証、active state の atomic publication と cleanup を検証するテスト群。feedback report の状態遷移、再開、冪等性、破損検出、秘密情報マスキング、path 境界、rate limit、ユーザー中断を確認する実装テストの入口。

## Read this when
- feedback の reporter や collector の protocol・schema・context 検証を変更または調査するとき
- feedback report の candidate 集約、verification verdict、checkpoint、publication、cleanup、再開処理を変更または調査するとき
- raw observation、active state、current pointer、generation artifact の整合性や破損時挙動を確認するとき

## Do not read this when
- feedback の正本仕様や prompt builder の契約だけを確認する場合は、対応する oracle file や builder 実装を直接読むとき
- feedback 以外の subcommand、report、state、テストを扱う場合

## hash
- 466b4e1dc79c71eb262fb67c2d8a4667b2eb110d915872ec70ed0db56a97e9ac

# `test_file_inventory.py`

## Summary
- Git の ignore 規則、リポジトリ境界、除外対象、特殊ファイル、シンボリックリンクを考慮した oracle/realization ファイル列挙と、リファクタ状態の同期・ハッシュ更新を検証するテスト群。ファイルインベントリ機能の実装や挙動を確認する際の入口となる。

## Read this when
- oracle/realization ファイルの列挙条件や除外境界を変更・検証するとき
- nested repository、linked worktree、Git ignore source、特殊ファイルや symlink の扱いを確認するとき
- リファクタ状態の同期やファイル SHA 更新に関するテスト結果を調査するとき

## Do not read this when
- ファイルインベントリやリファクタ状態同期に関係しない機能を調査するとき
- テスト実装ではなく、列挙仕様そのものを確認する場合は、先に参照されている正本仕様を読むべきとき

## hash
- bfc3cb26f5be06864246e343e5a5b512ac902447bfe9b12b57f948775defdb33

# `test_indexing_cli.py`

## Summary
- 対象は `cmoc indexing` の CLI、preflight、worktree、INDEX.md 更新、Codex structured output、commit lifecycle の外部挙動を検証するテストスイートです。未初期化・dirty・linked worktree・既存 hash・Git 差分などの条件分岐を扱い、INDEX.md だけを commit する制約も確認します。indexing 実装や仕様変更時の受け入れテストの入口です。

## Read this when
- `cmoc indexing` の事前条件、doctor、preflight、Codex 呼び出し、INDEX.md 更新、commit 条件を変更または検証するとき。
- dirty repository、linked worktree、既存 hash、staged・unstaged 差分、Git 異常終了に対する indexing の外部挙動を確認するとき。

## Do not read this when
- indexing の実装詳細を調査・変更する場合は、対応する src 実装を直接読むとき。
- 正本仕様や Structured Output schema だけを確認する場合は、対応する oracle 文書・schema を直接読むとき。
- indexing と無関係な CLI サブコマンドや、一般的なテスト実行手順だけを扱うとき。

## hash
- 9c71098080c6d203b7aecc61472ff51f850540bee02bbc6162df06d0e4bc9c69

# `test_indexing_common.py`

## Summary
- `commons.indexing` の INDEX.md 生成・解析・更新とディレクトリ走査を、CLI lifecycle から分離して直接検証する回帰テスト群。入力検証、hash による entry 再利用、安定した走査・描画順、並列更新、logger 伝播、cwd lock、memo・symlink・特殊ファイルの扱い、linked worktree 間の lock 共有を確認する。indexing contract の変更や、これらの traversal・更新順・並列実行の挙動を調査するときのテスト側の入口である。

## Read this when
- INDEX.md entry の parse・render・hash 再利用・更新処理を変更または検証するとき
- directory traversal、symlink・特殊ファイル・memo directory の除外、空 directory の扱いを確認するとき
- INDEX 更新の並列実行、pushd 中の worker 制約、Codex event logger、linked worktree lock を確認するとき
- indexing contract に関する回帰テストの対象挙動を把握するとき

## Do not read this when
- indexing の正本仕様や CLI subcommand の利用契約を確認する場合は、対応する app_spec を直接読む
- INDEX entry の生成プロンプト標準や Structured Output schema を確認する場合は、対応する oracle source を直接読む
- indexing と無関係な CLI lifecycle、一般的な runtime、または他機能のテストを調査するとき

## hash
- c5fef2ac6a7290435572c5051d1a8636143fad5de369866df36535f964841c7a

# `test_indexing_preflight.py`

## Summary
- Codex 呼び出し直前の indexing preflight を検証するテスト群。exec と TUI の実行順序、対象 worktree の選択、repository lock 待機、パラメータによる無効化、file access violation 後に recovery indexing を行わない制約を確認する。関連する indexing および Codex preflight 実装の挙動を検証する入口。

## Read this when
- Codex exec または TUI 呼び出し前の indexing 実行順序を変更・調査するとき
- linked worktree を含む indexing 対象 root の選択を変更・調査するとき
- indexing lock の排他制御や待機動作を変更・調査するとき
- preflight 無効化や Codex 失敗時の recovery 方針を変更・調査するとき

## Do not read this when
- INDEX.md の生成・ルーティング文書そのものを変更するとき
- Codex 呼び出しや indexing preflight の実装詳細を直接確認する必要があるときは、対応する実装ファイルを先に読む
- テスト実行方法や共通テストヘルパーだけを確認したいとき

## hash
- 4f09fc522e0c2178ced8610d4c1a74d8ab33cca205045d85ba2630abec3fe933

# `test_oracle_edit_cli.py`

## Summary
- `cmoc oracle edit` が main worktree 上で TUI を起動する際の CLI 制御を検証するテスト。doctor 前処理、prompt 編集、indexing preflight、起動前提検査、TUI 実行順序と引数、成功・失敗時の結果を扱う。
- oracle edit が run lifecycle を変更せず、既存の staged/unstaged 差分と session state を保持したまま oracle の編集結果を反映することを検証する。
- main worktree、session branch、active session などの起動前提違反を利用者向けエラーとして扱う挙動を検証する。

## Read this when
- `cmoc oracle edit` の CLI 制御や main-worktree TUI 起動順序を変更・レビューするとき。
- oracle edit における prompt editor、indexing preflight、起動前提検査、TUI 呼び出し引数の挙動を確認するとき。
- oracle edit が session state、Git の staged/unstaged 差分、run lifecycle に与える影響を検証するとき。

## Do not read this when
- oracle edit の仕様本文や実装責務そのものを確認する場合は、まず対象の仕様書または実装ファイルを読む。
- oracle edit と無関係な CLI、TUI、session state、Git 差分保持の変更を扱う場合。
- 一般的な oracle 編集処理の詳細を知りたいだけで、ここで検証される main-worktree CLI 制御や前提違反を調べる必要がない場合。

## hash
- 8ff8a2e78b4262c889f8bbfd6f65fed72a199bfb8096068c875a71f2cc42724e

# `test_oracle_investigation_cli.py`

## Summary
- 対象は oracle investigation CLI の起動条件と起動前後の処理順を検証する pytest で、session 前提なしの起動、doctor/build/editor/finalize/TUI の連携、生成される prompt と AgentCallParameter の契約を確認する。
- investigation の realization adapter が公開する builder API を限定していることも検証するため、CLI 起動フローやそのテスト契約を変更・調査するときの入口になる。

## Read this when
- `oracle investigation` サブコマンドの CLI 起動条件、main worktree での session 不要起動、または indexing preflight を含む起動順を確認するとき。
- prompt editor 入力、完全 prompt の確定、TUI 起動に渡す AgentCallParameter の値や prompt 内容をテストで確認・変更するとき。
- `acp.builder.oracle.investigation.launch_tui` の公開 API（builder のみ）に関する realization adapter のテスト契約を確認するとき。

## Do not read this when
- oracle investigation の正本仕様そのものを確認する場合は、まず `oracle/doc/app_spec/sub_command/oracle_investigation.md` などの仕様書を読む。
- CLI 共通の doctor、prompt editor、または indexing の一般仕様だけを調べる場合は、それぞれの専用仕様・実装・テストへ直接進む。
- investigation builder の実装詳細だけを確認する場合は、`oracle/src/oracle/acp_builder/oracle/investigation/launch_tui.py` を直接読む。

## hash
- abbf273c94a5245700d671437e85fea1cacbd47b99873da23ab6e238a17dfff9

# `test_oracle_review_loop.py`

## Summary
- oracle review の finding loop を検証する回帰テスト。finding の列挙、関連 finding の引き継ぎ、検証理由の統合、merge の postcondition、judgement、interrupt 時の部分結果保持、および隔離 worktree に対する agent call context を一つの review loop として確認する。

## Read this when
- oracle review の finding 列挙・merge・検証・judgement の連続処理を変更または調査するとき
- review worktree、agent call parameter、Structured Output、finding path の関連付けを変更するとき
- review loop の中断復旧や、完了済み finding・検証理由の保持を確認するとき
- merge 出力の postcondition や補正失敗の伝播を変更するとき

## Do not read this when
- oracle review loop の実装や契約に関係せず、他の sub-command の単独動作だけを調査するとき
- テスト実行方法だけを確認するときは、repository local の test execution 指示を直接読む

## hash
- 0f593f6750c3f5daf20d34f2113730e3c15db86849fa526ce3d083b7d635c85e

# `test_oracle_review_merge_operations.py`

## Summary
- oracle review の finding merge operation 適用契約を検証するテスト。delete・replace・merge の kind ごとの更新結果、finding_id 採番、既知でない target_id の位置付きエラー報告を確認する。

## Read this when
- oracle review の merge operation の挙動や契約を変更・検証するとき
- finding の削除・置換・統合後の内容や追加件数を確認するとき
- merge 操作が未知の finding_id を参照した場合の事後条件を確認するとき

## Do not read this when
- oracle review の merge operation と無関係な実装やテストを調査するとき
- oracle review の仕様本文や実装詳細を直接確認する必要があるときは、対応する oracle 文書・ソースを読む

## hash
- 72576ff9d5f5672d1a5009f090d82c91c8955395d69903dc5d0e9de1ec0dd7a2

# `test_oracle_review_report.py`

## Summary
- oracle review の report 生成と CLI 出力を検証する回帰テスト。report の節構成、finding の severity・verdict 別表示、件数集計、path の alias・symlink・特殊文字処理、frontmatter の安全な文字列化を扱う。
- レビュー中断や処理失敗時の error/interrupted report、完了済み oracle のみの列挙、CLI の scope option、timestamp 重複回避、実行ログ出力を検証する。
- oracle review の report contract と CLI 挙動に関するテストを追加・変更・レビューするときの入口であり、実装本体や正本仕様を確認する場合は対応する review 実装・oracle 文書へ進む。

## Read this when
- oracle review report の表示内容、finding の分類・件数、frontmatter、path 集計の挙動を検証するとき
- oracle review の中断・失敗時に保存される report や CLI の終了結果を確認するとき
- oracle review の回帰テストを追加・変更・レビューするとき

## Do not read this when
- oracle review の実装責務や処理フローを確認したいときは、review および review_report の実装を直接読む
- oracle review の正本仕様や設計上の要件を確認したいときは、対応する oracle 文書を直接読む
- oracle review と無関係な CLI 機能、一般的なテスト規約、他のテスト領域だけを扱うとき

## hash
- 74400d3626b226d186d8190820f4e44f63bcb8e35dbaa6b6a7c772d6c663d898

# `test_oracle_review_targets.py`

## Summary
- oracle review の finding path 解決と oracle 対象列挙を検証するテスト。対象範囲、追跡済み ignored file、binary file、Git path、symlink、AGENTS.md/INDEX.md の除外、および session scope の基準 commit を確認する。
- oracle review の no_targets 出力と、finding path の oracle/work-root 解決規則を確認するテストの入口。

## Read this when
- oracle review の対象ファイル列挙、scope 切り替え、対象パス解決、review fork commit 基準を変更または調査するとき
- 追跡済み ignored oracle file、binary oracle file、改行を含む Git path、symlink の扱いを確認するとき
- oracle review の no_targets レポートや Structured Output による finding 列挙の挙動を検証するとき

## Do not read this when
- oracle review の finding 内容の判定ロジック自体だけを変更・調査するときは、対象実装と対応する finding テストを直接読む
- oracle file や realization file の一般的な定義・配置規則だけを確認したいときは、対応する oracle 仕様を直接読む
- oracle review と無関係な CLI サブコマンドやテスト対象を扱うとき

## hash
- 8757338cf196ee4ade11c6c3d124615a06a93057a593aa317532e79f4970e2fb

# `test_oracle_review_worktree.py`

## Summary
- review 用の隔離 worktree と branch の lifecycle、および review で生成された INDEX.md の検証・統合を回帰テストする。
- oracle review の対象 worktree 選択、snapshot からの fork、衝突回避、割り込み・例外時の cleanup、merge rollback、差分制約、preflight path context、report、notification を検証する。
- oracle review の review worktree lifecycle、INDEX 差分の許可範囲、merge conflict 復旧、cleanup 失敗を変更または検証するときの入口である。

## Read this when
- oracle review の隔離 run がどの branch・commit・worktree を使うか確認するとき
- review worktree の作成・cleanup、割り込みや予期しない例外、lifecycle lock の挙動を変更または検証するとき
- review branch から INDEX.md のみを session に統合する条件、差分検証、merge conflict の復旧を確認するとき
- oracle review の report や terminal notification の回帰挙動を確認するとき

## Do not read this when
- oracle review の実装そのものを調べるときは、対応する sub_commands の実装を直接読む
- 一般的な INDEX.md 生成規則だけを確認するときは、indexing の正本仕様を直接読む
- oracle review と無関係な worktree lifecycle、merge、またはテストを扱うとき

## hash
- 8bca1e26933ec2546d6724e29ae447897a85931569345c5d07b769df1d664054

# `test_packaged_import.py`

## Summary
- packaged layout にソースツリーを複製し、隔離環境で Python import を実行して、ACP builder、oracle edit、prompt editor 入力境界、設定再公開の検証を行うテスト。packaged 配布時の import 境界、正本定義の参照、公開 API の限定を確認する実行テストへの入口。

## Read this when
- packaged layout での import、配布後の Python package 構成、または oracle と realization の import 境界を検証・変更するとき。
- oracle review や quota probe の builder が schema と完全 prompt を参照することを確認するとき。
- oracle edit、prompt editor 入力境界、ACP basic の正本型再公開、cmoc config の公開面を packaged 環境で確認するとき。
- このテストの対象となる packaging 設定、canonical builder、prompt editor 入力処理、または設定再公開の実装を変更するとき。

## Do not read this when
- packaged layout や import 境界を扱わず、通常の builder ロジックや prompt 内容だけを検証するときは、該当する個別テストや正本実装を直接読む。
- 配布構成ではなく、oracle の review schema や edit の仕様そのものを確認するときは、対象の schema または仕様書を直接読む。
- 設定定義の値や enum の挙動だけを確認するときは、cmoc config の正本定義または専用テストを直接読む。

## hash
- 16ceb03627945fb0b23a57b255a8b1cadf694266ef02c424af0d83eb23d16312

# `test_production_cli.py`

## Summary
- 対象を利用者向け entrypoint の全末端サブコマンドに対する受け入れ試験として位置づける。独立 process、実 Codex CLI・実推論、隔離環境を使い、非対話コマンドと PTY 上の TUI コマンドを本番経路で実行する。検証範囲は CLI の終了 code、report・state・Git の外部状態、Codex call log、応答完了後の終了操作であり、LLM の回答品質そのものは判定しない。
- 非対話経路では、leaf command の登録集合と固定シナリオを一致させたうえで、doctor、indexing、session、oracle review、feedback report、realization の各 fork、run の join/abandon、session の join/abandon を検証する。indexing の結果は INDEX.md と commit、各 realization は joinable state と worktree、各後処理は state・branch・worktree・report の状態遷移として確認する。
- TUI 経路では tui、oracle edit、oracle investigation を共通の実 PTY harness から実 Codex 応答完了まで実行し、TUI call log の内容、応答の存在、終了時の transcript、Git の不変性を確認する。
- 全体として、公開末端コマンドの追加漏れを検出し、実 executable・隔離された Codex home・実 provider 設定・外部観測可能な永続結果を一続きの本番経路試験で追跡する入口である。

## Read this when
- 利用者向け CLI の末端サブコマンドを追加・変更し、登録された全 leaf が本番経路で検証されているか確認するとき
- 実 Codex CLI と実推論を使う独立 process の受け入れ試験、または Codex call log・report・state・Git の外部結果を確認するとき
- cmoc の TUI コマンドの PTY、端末 capability query、応答完了検知、終了操作を含む本番経路を調べるとき
- realization/session/run の fork・join・abandon に伴う state、branch、managed worktree の遷移を受け入れ条件として確認するとき

## Do not read this when
- LLM の回答内容や文章品質そのものを評価するとき
- 単一の内部関数や mock ベースの制御ロジックだけをテストするとき
- INDEX.md の生成規則や oracle の正本仕様を確認するときは、まず該当する仕様・実装・専用の単体テストを直接読む

## hash
- 28ecfecc65d7ac544292ea5bff58d241ab1f09c1c72d59683934f7c20638b257

# `test_prompt_editor_input.py`

## Summary
- prompt editor input の realization 実装が、正本仕様に沿って動作することを検証するテスト。
- 初期表示文面が canonical builder の出力を使うこと、同一 timestamp の入力を上書きせず保持することを確認する。
- skeleton の placeholder がちょうど 1 箇所であることを検証し、不正時に editor を起動しないことを確認する。
- エディタ選択の優先順（code、nano、vim、vi）と、code 使用時だけ --wait を付ける起動引数を確認する。

## Read this when
- prompt editor input の外部挙動や realization test の検証範囲を確認するとき
- 初期入力文面、timestamp 衝突、placeholder 検証、エディタ選択の仕様適合性を調査するとき

## Do not read this when
- prompt editor input の正確な初期表示文面を確認したいときは canonical builder の実装を直接読む
- prompt editor input の意味仕様を確認したいときは正本仕様を直接読む
- エディタ入力以外の prompt 構築や AI Agent 呼び出しの挙動を調査するとき

## hash
- ce0bb9f0f7c73c54782ecabf1e6507c6db9b06ab658cf1ab48deff35f3733bf5

# `test_prompt_parts.py`

## Summary
- 標準 prompt parts と complete prompt の統合を検証する回帰テストです。
- Standard の不変性・入力検証・重複排除・競合検出と、StructDoc への描画結果を確認します。
- 各標準規則の個別生成、file access mode ごとの内容、complete prompt への条件付き注入、標準規則の既定値、placeholder 展開・保持・競合検出を一つの検証入口にまとめています。

## Read this when
- prompt builder の標準規則、prompt parts、complete prompt の描画または注入挙動を変更・検証するとき
- Standard、StandardCollection、StandardGroup の合成・描画・不変性・競合検出に関する回帰を確認するとき
- file access mode、oracle investigation、review、conflict resolution、routing、INDEX entry などの標準規則が complete prompt に正しく含まれるか確認するとき
- root placeholder の定義、literal token の保持、placeholder の重複・競合処理を検証するとき

## Do not read this when
- prompt builder の実装詳細や正本仕様の意味を直接確認することが目的の場合は、対応する oracle または realization の実装・仕様を先に読むとよい
- prompt builder と無関係な機能のテストや、個別の標準規則本文だけを確認する場合
- INDEX.md エントリーの出力形式そのものを確認する場合は、対象テストではなく index entry standard の正本を読むべきとき

## hash
- 2557603427d299b2b9c3a015ce5ad74db6d57b6bd7b4bf315d5eca43e9530208

# `test_runtime_cli.py`

## Summary
- CLI 共通 runner の error report、JSON Lines サブコマンドログ、doctor preprocess、completion probe、Windows toast 通知の境界を検証するテスト群。通常完了、非0終了、例外、KeyboardInterrupt、TUI 起動境界、通知失敗、および work root・worktree の扱いを横断的に確認する。CLI lifecycle の外部契約をまとめて検証する入口であり、個別の実装詳細や単一仕様の確認は対応する runtime 実装または oracle 仕様へ進む。

## Read this when
- CLI の終了コード、stdout の Markdown error report、stderr 非出力、call stack、例外終了の挙動を確認したいとき
- サブコマンドログの生成場所、イベント順序、flush、timestamp 衝突、並列 worker、pre-log check、doctor preprocess 失敗を確認したいとき
- _CMOC_COMPLETE による completion probe が通常の前処理・副作用・通知を回避することを確認したいとき
- 非対話 CLI と TUI の terminal result 通知、正常完了・失敗・ユーザー中断・起動前中断の境界を確認したいとき

## Do not read this when
- duration の表示形式や error report の仕様だけを確認する場合は、対応する oracle 仕様または runtime 実装を直接読むとき
- completion の候補生成内容だけを確認する場合は、自動補完仕様を直接読むとき
- doctor preprocess の個別修復手順だけを確認する場合は、doctor preprocess 仕様を直接読むとき
- パス placeholder の導出規則だけを確認する場合は、path model を直接読むとき

## hash
- ff78c277ec2b110682e814641995a79017890ac1885a154b0f7992a1154d779e

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
- Codex sandbox の argv builder が permission profile に依存しないことを検証するテスト。最小の AgentCallParameter と CmocConfig を用いて、path 別の read/write 例外を builder API が受け付けない契約を確認する。

## Read this when
- Codex override argv の builder API を変更・レビューするとき。
- permission profile や path 別の read/write 例外を builder の引数として扱わないことを検証するとき。
- runtime Codex permissions に関する realization test の対象範囲を確認するとき。

## Do not read this when
- argv builder の実装や permission profile の仕様そのものを確認したいときは、対応する実装または oracle 仕様を直接読む。
- Codex sandbox permissions と無関係なテストや AgentCallParameter の一般的な利用方法を調べるとき。

## hash
- 1e79dc80a0c9011af727643dd92c4ec3d855b3d0a1176410f044360e5b691cb3

# `test_runtime_codex_profile.py`

## Summary
- Codex argv の model、sandbox、provider 上書き契約を検証するテスト。file access mode から sandbox への変換、approval・TOML override・MCP feedback 設定、provider 選択と欠落時の失敗を扱う。
- Codex subprocess への feedback context 継承防止、schema の元バイト保持と SHA256 保存、invalid UTF-8 出力の扱いも検証する。Codex override 構築や runtime profile の挙動を確認する際のテスト入口となる。

## Read this when
- Codex argv の sandbox、model、reasoning effort、provider override の契約を変更または検証するとき
- MCP feedback の call context が Codex argv や subprocess environment に漏れないことを確認するとき
- schema の保存時ハッシュや Codex 出力 JSON のエラー処理を変更または検証するとき

## Do not read this when
- Codex override の実装詳細そのものを調査するときは、対応する runtime profile 実装と正本仕様を直接読む
- 他の runtime 機能や一般的な test 実行手順だけを確認するとき

## hash
- 2ed948eb91813f84cb0a95bf97e507b6f41cb328ce715f467409f57ea5bb5e09

# `test_runtime_config.py`

## Summary
- CmocConfig と config_from_dict/load_config/write_config/config_to_dict の挙動を検証するテスト。既定値、JSON 永続化、設定ファイル不在・破損・非通常ファイルのエラー、入力型・値・深さの検証、provider-local 設定の保持、UTF-8 や symlink/named pipe 境界を扱う。設定処理やエラー処理の実装・仕様を確認する際のテスト入口であり、個別の CLI 機能や一般的なテスト実行方法を調べる対象ではない。

## Read this when
- CmocConfig の既定値、model class と reasoning effort の対応、codex recovery 回数、oracle review の loop 回数を確認するとき
- config.json の読み込み・書き込み・JSON 化、設定不在や破損時の利用者向けエラーを確認するとき
- model provider、model spec、reasoning effort、各 section、整数項目、provider-local 値の入力検証を変更または検証するとき
- 設定パスの symlink、named pipe、ディレクトリなど非通常ファイルに対する安全な境界挙動を確認するとき

## Do not read this when
- 設定処理の実装詳細そのものを読む場合は、対応する oracle implementation を直接読むとき
- 設定仕様全体やエラー分類の正本を確認する場合は、関連する app_spec 文書を直接読むとき
- 設定処理と無関係な CLI 機能、実行フロー、または別のデータ構造のテストを調べるとき
- テストスイート全体の実行手順や品質検査の選択だけを確認するとき

## hash
- 2242fc73c5ac4a3709474108baf14695766033cc75f47a8e1bed145a912c927c

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
- FileAccessMode の永続化値が JSON schema 共有用の文字列として定義されていることと、各アクセスモードが Codex sandbox mode へ正しく変換されることを検証するテスト。

## Read this when
- FileAccessMode の値や file access mode から Codex sandbox mode への変換契約を変更・確認するとき。

## Do not read this when
- FileAccessMode の実装自体を変更するときは basic.acp の定義を直接確認する場合。
- Codex 実行時の sandbox 制約全般を確認するときは、対応する実行規則や変換実装を直接読む場合。

## hash
- 4115b2fd0a1a6350e8acec4a57b5a039c8f768d3660b0b75a0579ed96addb571

# `test_runtime_git_ignore.py`

## Summary
- Git ignore 関連のランタイム処理を検証する pytest。`.cmoc/gu` 用 ignore 設定の追加、tracked/untracked 状態を考慮した ignore 判定、check-ignore の失敗時処理を扱う。`.gitignore`、info/exclude、global excludes、親ディレクトリの ignore ファイルに対する特殊 file や symlink の安全な扱い、および既存 pattern・cmoc 管理 state の保持を確認する。Git ignore の更新・判定ロジックや、その安全性を変更・調査する際のテスト入口。

## Read this when
- `.gitignore` または Git の info/exclude・global excludes を用いた cmoc ignore 更新処理を変更するとき
- tracked/untracked ファイルに対する Git ignore 判定、check-ignore 失敗時のエラー処理を変更・調査するとき
- 特殊 file、symlink、既存 ignore pattern の保持など、ignore source の安全性を確認するとき

## Do not read this when
- Git ignore 機能に関係しないランタイム処理や CLI 挙動を扱うとき
- テスト対象の実装詳細を直接確認する必要があり、対応する runtime 実装や仕様書を読む方が適切なとき
- Git ignore のテスト実行方法だけを確認するとき

## hash
- 4d6c4bcf8983bb425b23a302419e0893cf3e2331b08e00ffea23959a54124d71

# `test_runtime_refactor.py`

## Summary
- 対象は、realization refactor の永続 state 同期・検証・target 選択に関する pytest である。oracle と realization の対象ファイル集合の追跡、調査履歴の保持と変更時の再調査化、state schema・path・timestamp・文字コード・特殊ファイルの拒否、oracle/realization 判定の安全性、未調査または古い対象を優先する選択規則を検証する。refactor state の読み書きや対象選択規則を変更・確認するときの実装テスト入口となる。

## Read this when
- refactor state の同期、読み込み、書き込み、schema 検証、path 安全性を変更または検証するとき
- oracle・realization ファイルの分類規則や branch 上の対象判定を変更または検証するとき
- refactor target の未調査・調査時刻による優先選択を変更または検証するとき

## Do not read this when
- refactor 以外の runtime 機能や、state・対象分類・target 選択に関係しないテストを扱うとき
- 実装の詳細を直接確認する必要があり、対応する commons.runtime_refactor などの実装ファイルへ進むべきとき

## hash
- b30756687154cd6d254de76e6cf75a73a46ac3e21eaa024353571ff654dd4671

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
- bin/cmoc の起動時に仮想環境の Python が利用できない場合のエラーレポートを検証するテスト。missing venv、通常ファイルでない venv パス、Python として起動できない実行ファイルを対象に、終了コード・stdout の report 構造・call stack の root token path・次のアクションを確認する。

## Read this when
- bin/cmoc の仮想環境検査、起動失敗時のエラーレポート、wrapper の call stack 表示を変更または検証するとき。

## Do not read this when
- 通常の CLI 機能や補完プローブの挙動だけを変更・調査するとき。仮想環境検査と wrapper の失敗 report に直接関係しないテストを扱うとき。

## hash
- 777dd4f6844721c51f36f16bb80f4c7d61c30c4c8853372891e7c4e3874c7335

# `test_session_cli.py`

## Summary
- session fork・join・abandon の CLI 外部挙動を、branch と永続 session state のライフサイクルとして一体的に検証する回帰テスト群。
- session branch の作成・衝突・保存失敗時の rollback、home branch への復帰、state 更新・cleanup・復元を扱う。
- linked worktree、dirty worktree、preprocess、home branch 不在、state 不正、conflict 解消、差分検査、エラー報告、session branch 削除警告など、session 操作の境界条件を検証する。
- session コマンドの挙動、session state の遷移、branch/worktree 操作、join 時の conflict resolution を確認したい場合の回帰テスト入口。

## Read this when
- session fork・join・abandon の仕様変更や不具合調査を行うとき。
- session branch、session state、linked worktree のライフサイクルや rollback を変更するとき。
- join の conflict resolution、変更範囲検査、Codex 呼び出し境界、エラー出力を確認するとき。
- doctor preprocess と session 操作の前後関係、dirty worktree や home branch 不在時の挙動を検証するとき。

## Do not read this when
- session CLI の実装詳細だけを確認したい場合は、対応する session サブコマンド実装を直接読む。
- session state の正本形式や遷移規則だけを確認したい場合は、session state 仕様を直接読む。
- conflict resolution のプロンプト生成規則だけを確認したい場合は、conflict resolution の実装・仕様を直接読む。
- session と無関係な CLI、Git 操作、一般的なテスト支援機能を調べる場合。

## hash
- 46f4688370451d46da3b01ab09b6e39e3fe7f0895ea8a39ff5bf72aa7e1246d7

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
- StructDoc の Markdown renderer に対する単体テスト。空行の縮約、code block の fence 処理、StructBlock の互換 re-export、描画済み Markdown の透過埋め込み、cmoc_ref の検証エラーを確認する。renderer の外部挙動を確認する際の入口であり、実装詳細や Oracle 原典そのものを読む対象ではない。

## Read this when
- Markdown renderer の空行処理や code block の fence 生成を確認・変更するとき
- StructBlock の互換公開や描画済み Markdown の埋め込み挙動を確認するとき
- cmoc_ref の欠落・重複・不正記法に対するエラー挙動を確認するとき

## Do not read this when
- renderer の実装詳細を直接調査するとき
- Oracle の StructDoc 定義や prompt standard の仕様を直接確認するとき
- 対象挙動と無関係なテストや機能を調査するとき

## hash
- 47d5a4c7a1dd53b0987d65acbc89ee232459d35a49eeca8c34d150fd5760a8a5

# `test_windows_toast.py`

## Summary
- Windows 通知機能のテストで、終端結果通知の短い表示内容、PowerShell transport への JSON stdin 渡しと入力混入防止、通知失敗の非伝播を検証する。Codex callback については、turn 単位の重複排除、callback 本文の非使用、TUI invocation ごとの一時 state 管理、実 argv による単独実行を検証する。

## Read this when
- Windows toast の表示内容や機密情報の露出防止を変更・確認するとき
- PowerShell transport の引数、stdin、timeout、失敗処理を変更・確認するとき
- Codex callback の重複排除、turn 識別、TUI callback の一時 state と実行形式を変更・確認するとき

## Do not read this when
- Windows toast や Codex callback の挙動に関係しないテストや実装を扱うとき
- 通知機能の実装詳細そのものを確認する必要があり、対応する実装ファイルを直接読むべきとき

## hash
- b1e479cc79b3de4af4be05d7afac596db7ff97763d85ef9bf6d1a34f81363e76
