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
- `doctor` CLI を対象 worktree で実行するテスト補助と、実行結果の terminal output から primary report のパスを抽出する補助を提供する。`doctor` の CLI テスト実装やレポート出力の検証を始める際の共通入口となる。

## Read this when
- `doctor` CLI をテストから実行する方法を確認するとき
- 対象 worktree の cwd を切り替えて `doctor` の実行結果を検証するとき
- terminal output に表示された primary report のパスをテストで取得するとき

## Do not read this when
- `doctor` コマンド本体の仕様や実装を確認するとき
- `doctor` 以外の CLI コマンドのテスト補助を探すとき
- primary report の生成仕様やログ出力仕様そのものを確認するとき

## hash
- 96f97d1ad9d97701f80a7262d126b0971410176370c1112e8efc26df78067813

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
- TUI 起動用 parameter builder の realization test。元の prompt に依存せず固定の agent call 種別・モデル・推論強度・ファイルアクセス権・作業ディレクトリ・indexing preflight と規範 prompt を設定すること、および一時リポジトリへ editor input を作成しないことを検証する。互換 module の公開 API が現行 builder のみに限定され、正本 builder と同一実装であることも確認する。TUI 起動 builder の parameter、prompt 規範、または互換 module の公開面を変更・検証するときの realization 側テスト入口。

## Read this when
- TUI 起動 builder の固定実行設定や prompt 規範への適合を確認するとき
- acp.builder.tui.launch_tui の互換 module が公開する API や正本 builder との同一性を確認するとき
- TUI 起動処理が indexing preflight や editor input の生成に影響する変更を検証するとき

## Do not read this when
- TUI 起動 builder の正本仕様や実装そのものを調査・変更するときは、対応する oracle または realization の実装を直接読む
- TUI 以外の builder、または一般的な prompt 構築・module 公開面を扱うとき

## hash
- faec93a3fb8b12c6f92fa47c7272a125725f53508dfdedada938512c1bce5da8

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
- TUI 起動直前の CLI 前処理の外部挙動を検証するテスト。編集済みプロンプトの保存・反映、doctor 前処理、Codex TUI 起動パラメータ、既存の Git 差分保持を扱う。
- linked worktree 起動時の editor 入力ログと agent call context の保存先、および repository・worktree 双方での `.cmoc` ignore を検証する。

## Read this when
- TUI サブコマンドの起動フローや、編集済みプロンプトからの Codex TUI 起動挙動を変更・検証するとき。
- doctor 前処理、prompt editor、TUI 起動パラメータ、既存差分の保持を一体で確認するとき。
- linked worktree におけるログ保存先、agent call の作業ルート、`.cmoc` の ignore を確認するとき。

## Do not read this when
- TUI の画面実装そのものや、CLI 前処理以外のサブコマンドを確認するとき。
- プロンプト構築の実装詳細や正本仕様を直接確認するとき。
- 対象テストが検証する外部挙動ではなく、一般的なテスト実行方法だけを確認するとき。

## hash
- 1c75ae6123250cf6799dd3d8403bd7a3cc602e09510a73c1775a2a6e085e00f2

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
- Codex quota 超過後の probe・待機・resume・再実行を検証する回帰テスト群。代表 probe の共有、session ID 復元、quota/capacity 失敗、ログ記録、CODEX_HOME と cwd、並行呼び出し、割り込みや不正出力時の後始末まで、同一の quota retry 状態機械として確認する。Codex 実行の quota 復帰挙動やその観測ログを変更・調査するときの入口。

## Read this when
- quota 超過後に Codex exec が probe を実行して待機・復帰する外部挙動を変更または検証するとき
- resume session ID の復元、session ID 欠落時の再実行、probe 失敗時の伝播を確認するとき
- quota 待機の並行呼び出し、共有 probe、call log・subcommand log の状態や CODEX_HOME/cwd を調査するとき
- quota 待機中の割り込み、無効な JSONL、出力失敗、poll 上限などの回帰を確認するとき

## Do not read this when
- quota retry 以外の Codex 実行仕様や一般的な subprocess 引数だけを調べるときは、実装または正本仕様を直接読む
- quota probe の prompt 構築そのものだけを変更・確認するときは、quota probe builder とその正本仕様を直接読む
- 通常の成功系 Codex exec や quota と無関係なログ形式を扱うときは、このテスト群ではなく対応する実装・テストへ進む

## hash
- 45ae6f9a369faf370879e6a0cc313d02644258d0ac0cacfb9be508380fa14895

# `test_codex_runtime_retry.py`

## Summary
- `run_codex_exec` の異常系における外部挙動を検証するテスト群。Structured Output の補正と検証失敗、capacity retry、未知の JSONL error、中断、retry 上限、共有 call log・subcommand event、成果物差分の保持または補正時の復元を、fake Codex CLI の応答から最終結果まで一続きで確認する。Codex 実行の retry 状態や失敗ログ schema を変更・検証する際の入口であり、個別の正常系や別の CLI 機能だけを扱う場合は直接そのテスト対象へ進む。

## Read this when
- `run_codex_exec` の Structured Output 出力補正、schema validation failure、postcondition failure、capacity retry、未知の JSONL error、KeyboardInterrupt、retry 上限を変更または検証するとき。
- Codex subprocess の呼び出し回数、session の継続、call log、codex subcommand event、retry backoff、失敗診断の外部契約を確認するとき。
- capacity retry 後の agent diff 保持や、Structured Output 補正 turn が成果物を変更した場合の復元・失敗挙動を確認するとき。

## Do not read this when
- `run_codex_exec` の正常終了だけ、または retry・失敗ログ・差分復元に関係しない別の Codex 実行機能を確認するとき。
- 実装ではなく正本仕様そのものを確認する必要があるときは、参照されている oracle の仕様断片を直接読む。
- このファイルの fake subprocess、共有ログ schema、retry 状態機械を伴わない単独の JSON schema validator やログ表示の確認をするとき。

## hash
- c264007778b1b9d99a4cdf238ea7d840f49499e6b511437273b9b4670a9c002e

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
- Codex TUI 実行ラッパーの統合テスト。完全な prompt と CLI 引数、作業ディレクトリ、アクセスモード、通知設定を検証する。
- TUI 呼び出しの call log とサブコマンドイベントについて、成功、CLI 不在、KeyboardInterrupt、非 0 終了、timestamp 衝突時の記録を検証する。
- TUI 実装や Codex 実行・ログ仕様を変更または検証する際のテスト入口であり、個別の共通 fixture や正本仕様の代替ではない。

## Read this when
- Codex TUI の prompt 引き渡し、アクセス境界、作業ディレクトリ、CLI オプションを確認するとき
- Codex TUI 呼び出しの成功・失敗ログ、return code、例外処理、call log 保存を確認するとき
- 同一 timestamp の呼び出しでログを保持できるか確認するとき

## Do not read this when
- Codex TUI の実装仕様や CLI 実行規則を確認する場合は、対応する実装または正本仕様を直接読むとき
- TUI と無関係な Codex 実行経路、ログ機構、テスト共通ヘルパーだけを扱うとき

## hash
- bee9341722a4bc93731960c1ca258d8b8c432cf48285c438d2e4422a338cbc04

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
- workload fork と共通 run join/abandon の統合 realization test。apply/refactor の run lifecycle、worktree・branch・session state、process tracking、INDEX 更新、report、rollback・cleanup を横断検証する。
- 実際の CLI 呼び出しと共通 lifecycle fixture を用い、正常系に加えて禁止差分・agent commit・遅延処理・中断・競合・merge conflict・cleanup 失敗時の state 保持を検証する。
- realization fork、run join/abandon、共通 lifecycle、fork/lifecycle report、refactor state、INDEX refresh の相互作用を確認するための統合テスト入口。

## Read this when
- realization apply/refactor fork の worktree、commit、rollback、INDEX 更新を確認するとき
- run join/abandon の merge、force-resolve、process 停止、resource cleanup、再試行可能な state を確認するとき
- editing run の state 遷移、run kind、branch 所有、report、通知、中断時の挙動を横断的に確認するとき
- agent や INDEX refresh による想定外差分、遅延 commit、process tracking 異常を検証するとき

## Do not read this when
- INDEX.md 自体のルーティング内容を確認するとき
- 単一 helper や prompt 構築の実装だけを確認するとき
- Windows toast 通知の仕様だけを確認するとき

## hash
- e80c036a029dac6ac682396b462c665f207c4e4a23b7567e1a1079c1f89db28c

# `test_feedback.py`

## Summary
- feedback observation の reporter、collector、raw store、report cut、verification、active state、atomic publication、cleanup を同一 fixture で検証する統合テスト群。
- agent/machine observation の受理・検証・rate limit・冗長化、候補同一性判定、verification verdict、current reference と fingerprint の扱いを確認する。
- Codex 呼び出しの checkpoint 再利用、Ctrl+C・書き込み失敗・部分 cleanup からの再開、publication 後に pending raw が除去され compact な active state だけが残る境界を検証する。
- feedback report の不正 artifact、symlink、path traversal、secret masking、hash mismatch、未定義 artifact など安全性・破損検出も対象とする。

## Read this when
- feedback reporter または collector の agent-facing protocol、observation envelope、保存・rate limit・context 検証を変更または調査するとき。
- feedback report の候補集約、issue identity、verification、report cut、checkpoint、publication、active state、cleanup の挙動を変更または調査するとき。
- feedback の中断・再実行・部分失敗・破損 artifact・path boundary・secret masking に関する外部挙動を確認するとき。

## Do not read this when
- feedback 機能を使わない一般的な CLI、session、logging の変更や調査を行うとき。
- テスト対象の正本仕様や実装詳細を直接確認する必要があり、テストケース自体が入口ではないとき。

## hash
- 3b0a318577007451ce44ff25bee7bc2c7c819abb4a0a2a5d0c44c0456112dbea

# `test_file_inventory.py`

## Summary
- Git の ignore ルール、ネストしたリポジトリ、除外境界、特殊ファイル、シンボリックリンクを含む oracle/realization ファイル列挙と refactor state 同期の契約を検証するテスト群。
- full-tree 列挙結果と Git 判定、state の追加・削除・SHA 更新、非 UTF-8 ファイル名の保持を確認する。
- 単一パス分類、linked worktree、各リポジトリ固有の ignore source、ignore source の重複検証、候補数増加時の Git 処理量不変性も対象とする。

## Read this when
- ファイルインベントリ列挙や oracle/realization 判定の実装を変更・レビューするとき。
- ネストした Git リポジトリ、Git ignore、linked worktree、特殊ファイルまたは symlink の扱いを確認するとき。
- refactor state の同期・SHA 更新や、列挙処理の性能特性を検証するとき。

## Do not read this when
- CLI の一般的な挙動、refactor state 以外の永続状態、またはファイル列挙に関係しないテストを調べるとき。
- 正本仕様や実装の詳細を直接確認する必要があり、このテストファイルを検証入口にする理由がないとき。

## hash
- cde545c62f282b7b46d1685a2110d4fe1222ad6b3c853e0f07c1617d7f859b82

# `test_indexing_cli.py`

## Summary
- `cmoc indexing` の CLI ライフサイクルを外部挙動として検証するテスト群。doctor による初期化、現在の linked worktree の選択、dirty repository の拒否、INDEX.md の生成・更新、Codex structured output と worktree 設定の利用、fresh hash 時の省略、INDEX.md だけを対象にした commit を扱う。`indexing` の実装挙動や回帰を確認する際のテスト入口であり、個別の Git helper や preflight 実装の詳細だけを確認する場合は、それらの実装・専用テストへ直接進む。

## Read this when
- `cmoc indexing` の事前条件、worktree 対象、Codex 呼び出し、INDEX.md 更新、commit 条件を変更または検証するとき
- indexing preflight が既存の staged・unstaged 差分や worktree 固有設定をどう扱うか確認するとき
- INDEX.md の hash による再生成省略や、commit に含めるパスの制約を確認するとき

## Do not read this when
- `indexing` 以外の CLI サブコマンドの挙動だけを扱うとき
- INDEX.md エントリー生成 schema の形式だけを確認するときは、schema 定義を直接読むとき
- Git 操作や Codex 実行の一般的な helper 実装だけを調査し、indexing の外部ライフサイクルを検証しないとき

## hash
- abedb136ef607321f71e5248fdbc351edf28c50422a67a564cafd4bc84243e7b

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
- Codex の exec/TUI 呼び出し直前に実行される indexing preflight の挙動を検証するテスト群。通常の indexing 実行、linked worktree の選択、repository lock 待機、パラメータによる無効化、file access violation 後の recovery indexing 禁止を扱う。対象機能の変更や検証時に、外部から観測される呼び出し順序と git commit・clean 状態を確認する入口となる。

## Read this when
- Codex exec または TUI 経路に indexing preflight を追加・変更するとき
- preflight の対象 root、linked worktree の扱い、repository lock の待機動作を確認するとき
- indexing の無効化条件や、Codex 呼び出し失敗後に recovery 用 indexing を行わない制約を確認するとき

## Do not read this when
- indexing の生成内容や INDEX.md ルーティング規則そのものを確認するとき
- Codex 呼び出しや preflight の実装詳細を直接確認する必要があるとき
- 単純な Codex CLI 実行結果や、indexing preflight と無関係な git 操作を調べるとき

## hash
- bfa16ec7d9dba1f9d76f723589c4e441c694613cbc54d05ee054ffc38fe4b3ee

# `test_oracle_edit_cli.py`

## Summary
- `cmoc oracle edit` の main-worktree 実行制御を検証する制御テスト。成功時と main exec・仕様削減 exec の各失敗時について、editor 入力、起動パラメータ、Git 差分、session state、indexing preflight、通知および失敗境界を一連の invocation で比較する。
- oracle edit の起動前提である main worktree、session branch、active session state を満たさない場合に、利用者向けエラーとなることも検証する。

## Read this when
- `cmoc oracle edit` の実行フロー、2 回の agent exec、仕様削減、editor 入力、失敗処理または完了・失敗通知を変更・レビューするとき。
- oracle edit の main-worktree 制約や session state に関する起動前提を変更・レビューするとき。

## Do not read this when
- oracle edit 以外のサブコマンドの実装やテストを扱うとき。
- 共通の Git、Codex 起動、session state、CLI runner の一般仕様を直接確認する必要があり、この制御テストではなく対応する実装・仕様を読むべきとき。

## hash
- 764f1609a32e7fc7a451b72ffc90b75bcda2968a7a0a47bec8bf4ad74ace9c1e

# `test_oracle_investigation_cli.py`

## Summary
- `cmoc oracle investigation` の CLI 起動契約を検証するテスト。session 前提のない main worktree での起動、doctor preprocess から prompt editor、parameter build、work file cleanup、Codex TUI 起動までの順序と受け渡しを確認する。
- oracle investigation 用 launch TUI builder の公開 API が意図した builder のみに限定されることを検証する。

## Read this when
- `oracle investigation` サブコマンドの起動条件、session 前提、indexing preflight、prompt editor handoff、TUI 起動順序を変更または調査するとき。
- oracle investigation の launch TUI realization adapter の公開範囲を変更または確認するとき。

## Do not read this when
- oracle investigation の本文仕様や prompt skeleton の内容だけを確認したいときは、参照されている oracle 文書を直接読む。
- 他のサブコマンドの CLI 起動経路や builder の公開範囲を調査するとき。

## hash
- d0bf430c9af99a040dc331f06903712c121a941f94fbfd2d86043be12b209b31

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
- oracle review の report 生成・表示・エラー処理を検証する回帰テスト群。正常完了・中断・処理失敗時の結果、評価対象 oracle、finding の severity／判定別分類と件数、report 節順、CLI 出力、パスや YAML のエスケープ、timestamp 重複回避を対象とする。oracle review の report contract や CLI 出力の挙動を変更・確認するときのテスト入口である。

## Read this when
- oracle review report の schema、finding 表示、評価対象集計、判定結果、エラー／中断時の出力を変更または検証するとき
- oracle review CLI の scope option、report 保存、標準出力・標準エラーの挙動を確認するとき
- oracle path の alias・symlink・特殊文字処理、YAML frontmatter の値の引用、timestamp 付き report の衝突回避を変更または検証するとき

## Do not read this when
- oracle review の実装詳細や正本仕様だけを確認したいときは、対応する oracle review 仕様・実装を直接読む
- oracle review 以外のサブコマンド、または report contract と無関係なテストを扱うとき

## hash
- c3502c9f6af44bdcf88cde5b1ca31bf8a40d718034487a8bc81c875d5ea8f27c

# `test_oracle_review_targets.py`

## Summary
- oracle review の finding path 解決とレビュー対象 oracle file 列挙を検証するテスト。相対・絶対・placeholder 付きパス、symlink、repository 外パス、session/full scope の対象範囲、Git path の改行、対象外ファイルの除外、Codex 呼び出しとレビュー結果の集計を扱う。
- oracle review の対象列挙や finding path の解決仕様を変更・確認するときに、実装側のテスト挙動と期待される境界条件を確認する入口となる。

## Read this when
- oracle review の対象ファイル数、scope ごとの対象選択、レビュー fork commit 基準の差分、ignored/tracked file の扱いを確認するとき
- finding の oracle_path 解決、oracle alias、work-root、symlink、外部パス拒否の挙動を変更または検証するとき
- oracle review の対象から AGENTS.md・INDEX.md・symlink などを除外する仕様を確認するとき

## Do not read this when
- oracle review 以外のサブコマンドや、finding path 解決・oracle file 列挙に関係しないテストを扱うとき
- レビュー対象の内容評価や finding の文章生成そのものを確認したいときは、対象列挙ではなく oracle review の評価処理や Structured Output 定義を直接読むとき

## hash
- 6c8e651a50962b0f4d7e53e13321cfec7234c88f9324d4887703842fdccc74c8

# `test_oracle_review_worktree.py`

## Summary
- oracle review の隔離 run と linked worktree を対象に、review branch の fork、preflight、Codex agent call、差分検証、INDEX.md のみの統合、merge、cleanup、割り込み・異常終了時の復旧を検証する回帰テスト群。oracle review の worktree lifecycle、INDEX 統合、競合解決、cleanup failure の挙動を変更・調査するときの主要なテスト入口である。

## Read this when
- oracle review が session branch または snapshot commit から正しく隔離されるか確認するとき
- review worktree の作成・再利用防止・cleanup、branch 所有権、割り込みや例外時の復旧を変更するとき
- review 結果として生成された INDEX.md だけを session に統合し、その他の差分や対象外 INDEX を拒否する挙動を確認するとき
- review branch の merge、INDEX 競合解決、merge 中断・失敗後の worktree 復旧を検証するとき

## Do not read this when
- oracle review の通常の所見判定ロジックや Structured Output schema の詳細だけを確認したいときは、review 実装または対応する仕様を直接読む
- 一般的な INDEX.md 生成・更新の仕様だけを確認したいときは indexing の正本仕様や indexing 実装を直接読む
- session fork や editing run の一般仕様だけを確認したいときは、それぞれの正本仕様・専用テストを直接読む

## hash
- 83afb430311ec05d416f52f45c3d5c3953e29c8fdd6cea528b675c29eb79d450

# `test_packaged_import.py`

## Summary
- packaged layout にコピーした ACP・oracle・basic・commons・config の import 境界と公開面を検証するテスト。setuptools の package 配置、canonical builder の schema・prompt 参照、oracle edit と prompt editor の入出力境界、basic 型の再公開、config の限定的な再公開を扱う。
- packaged layout やインストール後の import 可否、正本定義と realization 側の再公開関係、builder が生成する parameter の設定、モジュール公開面を変更・検証するときのテスト入口となる。

## Read this when
- Python パッケージを source tree から分離した packaged layout で import する挙動を確認するとき
- ACP builder、oracle review/edit、quota probe、prompt editor の packaged import 境界を変更・検証するとき
- canonical 定義の再公開や __all__・module namespace の公開範囲を確認するとき

## Do not read this when
- packaged layout の import 境界や公開面を扱わず、個別機能の通常動作だけを検証するとき
- 正本 builder・schema・prompt editor の実装や仕様を直接変更・確認する場合は、対応する実装または oracle 文書を先に読むとき

## hash
- b7d735be635084de00aca7cf1979bac112b941e5f2a100b6c15bf1ae4707d8e2

# `test_production_cli.py`

## Summary
- 実 Codex CLI と実推論を用い、全末端サブコマンドの利用者向け本番経路を独立 process で検証する受け入れテスト。終了 code、report・永続 state・Git 状態、Codex call log を確認し、非対話 command と PTY 上の TUI command の完了・終了操作まで扱う。LLM の回答品質は評価対象外とする。

## Read this when
- 全末端サブコマンドの本番経路に対する受け入れ試験を確認するとき
- 独立 process、実 Codex CLI、隔離環境、実推論を含む CLI 統合テストの検証方法を確認するとき
- 非対話 command の状態遷移や report・Git・call log の外部観測結果を確認するとき
- TUI command の PTY 応答、terminal query、Codex response 完了、終了処理を確認するとき

## Do not read this when
- 個別サブコマンドの実装詳細や単体テストだけを確認するとき
- LLM の応答内容や推論品質を評価するとき
- Codex CLI を使わない内部ロジックのテスト方法だけを確認するとき

## hash
- a2c0d94598f1888771b544dfe7368fb58ddb430d5a918495f91a4f43f1e6d4f7

# `test_prompt_editor_input.py`

## Summary
- prompt editor input の外部挙動を検証するテスト。可変作業ファイルと保存記録の分離、入力抽出時の最終読み取り、skeleton の placeholder 制約、エディタ選択優先順位、ファイル種別・パス境界の拒否、失敗時の作業ファイル保持を扱う。prompt editor input の実装変更や、その外部契約に対するテスト要件を確認する際の入口となる。

## Read this when
- prompt editor input のファイル予約・編集・入力収集・確定処理を変更または検証するとき
- エディタ起動、skeleton 置換、入力保存、異常系の外部挙動を確認するとき

## Do not read this when
- prompt editor input の正本仕様や実装の詳細を直接確認することが目的のとき
- prompt editor input 以外の機能のテストや実装を扱うとき

## hash
- 04c84b17350b6392f5105e7ef6bd242ac2821e0572c1e7d3fb572f84196a0341

# `test_prompt_parts.py`

## Summary
- prompt builder の標準規範、各 prompt part、complete prompt の構築をまとめて検証する回帰テスト。Standard の不変性・rendering・統合、oracle/realization/review などの標準選択、file access mode、routing、feedback、placeholder 展開と競合を扱う。
- 単一の prompt part の実装詳細ではなく、複数の標準と complete prompt の組み合わせが正しいことを確認するための集約されたテスト入口。

## Read this when
- prompt builder の standard または prompt part を追加・変更し、complete prompt への注入条件や rendering への影響を確認するとき
- placeholder、root path、file access mode、routing rule、feedback instruction の prompt 出力を回帰確認するとき
- oracle・realization・review・conflict resolution・editor handoff など複数の標準の統合境界を確認するとき

## Do not read this when
- 単一の標準または prompt part の本文・実装だけを直接調査すれば足りるとき
- prompt builder と無関係な機能のテストや、CLI の実行経路そのものを確認するとき

## hash
- 2157b67dae0f2b35192bc5a33f744db81e2a9753c69cf99ccc07cd4512cce627

# `test_runtime_cli.py`

## Summary
- CLI 共通 runner の error、log、preflight、completion、終了通知を横断的に検証する統合テスト。duration 表示、サブコマンドログの並行性・終了記録、handled/internal failure の表示と traceback 隔離、KeyboardInterrupt、doctor preprocess、非 0 終了、TUI 通知、CLI 引数解析、work root 制約、shell completion の副作用抑制を扱う。
- CLI lifecycle の複数境界を同一 runner と subcommand event の観測で検証するため、個別 runtime 実装ではなく外部挙動の変更・回帰を確認するときの入口となる。

## Read this when
- 共通 CLI runner の成功・失敗・中断時の console 出力、終了コード、terminal notification を確認するとき
- サブコマンドログの生成、イベント順序、失敗情報、traceback 保存、並行 worker 記録を変更・検証するとき
- doctor preprocess、pre-log check、work root 制約、CLI parse error、completion probe の実行境界を確認するとき
- TUI と非対話 CLI の終了通知や KeyboardInterrupt の扱いを確認するとき

## Do not read this when
- duration formatting 単体や error 表示関数単体だけを変更・確認する場合は、対象 runtime 実装またはその直接の単体テストを読む
- CLI lifecycle と無関係なサブコマンド固有処理、Codex 呼び出し内部、Windows toast の実装詳細だけを確認する場合は、各対象の直接テストへ進む
- 正本仕様や CLI の設計意図を確認する場合は、この検証ファイルではなく参照される app_spec 文書を読む

## hash
- 711454cff71d60d408a39596bc3ecd2d430a824ed59885c86639c62bab5093c6

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
- `bin/cmoc` 起動 wrapper の仮想環境検査と失敗時エラーレポートを検証するテスト。仮想環境の Python が存在しない場合、通常ファイルでない場合、または Python として起動できない場合に、フルパスを含む簡潔な失敗報告が出力されることを確認する。

## Read this when
- `bin/cmoc` の起動時における仮想環境検査、失敗時の stderr 出力、終了コード、スタックトレース抑制を変更・検証するとき。
- wrapper の通常経路と補完プローブ環境を分離したテスト条件を確認するとき。

## Do not read this when
- 補完候補生成そのもの、CLI の一般的なコマンド処理、または仮想環境検査を伴わないエラーハンドリングを確認するときは、対応する実装・仕様・テストを直接読む。

## hash
- 13d69d4548a5658fd9fc29080b20cf2e14416688f94cdf8ac45e186ceb6ad592

# `test_session_cli.py`

## Summary
- session fork・join・abandon の CLI 外部挙動をまとめて検証する回帰テスト。session branch と永続 session state のライフサイクルを中心に、作成・再試行・衝突・ロールバック・abandon・join・cleanup を扱う。
- linked worktree を含む branch 切替と home branch の扱い、doctor preprocess、dirty worktree や欠損・破損 state の拒否、state と branch の整合性を検証する。
- session join の conflict 解消では、Codex の sandbox・prompt 境界、対象外変更の拒否、conflict marker・特殊 path・削除の扱い、merge 後の branch cleanup と診断出力を検証する。session CLI の状態遷移と回帰挙動を横断的に確認する入口であり、個別実装や正本仕様の詳細は参照先へ進む。

## Read this when
- session fork・join・abandon の外部挙動を変更または回帰確認するとき。
- session state、session branch、linked worktree のライフサイクルや cleanup を確認するとき。
- dirty worktree 拒否、preprocess、state 破損、session-id 衝突、失敗時ロールバックを確認するとき。
- session join の conflict 解消、Codex 呼び出し境界、対象外差分の拒否、特殊な conflict path を確認するとき。

## Do not read this when
- session CLI 以外の機能を調査するとき。
- 個別コマンドの実装責務や正本仕様を確認するときは、対応する実装・仕様ファイルを直接読むとき。
- 共通のテスト実行方法や fixture の詳細だけを確認したいときは、対応する補助モジュールや開発規則を直接読むとき。

## hash
- ccaaabe402a915e1237578808bbed08a4af5799993c78e816775ae5a957909b0

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
- Windows toast の端末結果通知について、command・repository 名・状態だけを短く表示することを検証するテスト。
- PowerShell transport への JSON stdin 受け渡し、通知失敗の隔離、Codex callback の turn 単位重複排除、TUI callback の一時 state と standalone 実行を検証する。

## Read this when
- Windows toast 通知の表示内容や失敗時の扱いを変更・検証するとき
- PowerShell transport の引数・stdin・タイムアウト境界を確認するとき
- Codex callback の通知重複排除、TUI invocation ごとの state 管理、callback コマンドの単独実行を確認するとき

## Do not read this when
- Windows toast や Codex callback の実装・仕様を直接確認できる対象を読むべきとき
- 通知機能および callback と無関係なテストや機能を扱うとき

## hash
- 84d0bd768306cab5673028df7dde85de3da5ef75966aca5580f39d807942ba19
