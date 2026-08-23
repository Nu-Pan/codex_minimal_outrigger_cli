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
- editing run workload の canonical builder adapter を検証する pytest。apply、refactor の各 builder が正本 builder、実行設定、Structured Output schema、prompt 内容を正しく利用・再公開することを確認し、raw diff 内のコードフェンスや境界風テキストを保持できるかも検証する。対象 builder の挙動、互換 import 経路、prompt 構築、schema 選択を変更・調査するときのテスト入口である。

## Read this when
- editing run の apply/refactor builder の実装や互換 import 経路を変更するとき
- builder が生成する prompt、実行設定、Structured Output schema、raw diff の埋め込みを検証するとき
- raw diff 内の三連 backtick や prompt 境界風見出しの扱いを確認するとき

## Do not read this when
- builder 実装そのものの責務や canonical prompt の正本を確認する場合は、対応する realization 実装・oracle を直接読む
- editing run と無関係な CLI 機能、一般的なテスト基盤、別 workload の検証だけを扱う場合

## hash
- d9cbfbb2e9175ff9a879c7b3e2260f9f0233fa03af58bb728864e050e2e367a3

# `test_acp_builder_indexing_parameters.py`

## Summary
- index entry builder が生成する parameter のモデル、推論、アクセス権限、作業ディレクトリ、preflight 設定、prompt 収録内容を検証するテスト。
- Structured Output schema の semantic 配列が空でない制約を確認する。
- 対象本文に三連 backtick が含まれる場合の prompt 境界保護と oracle builder との parameter 一致を検証する。
- indexing の互換 module が builder だけを公開する契約を確認する。

## Read this when
- index entry builder の parameter 設定や prompt 生成を変更・検証するとき
- index entry 用 Structured Output schema の必須要素数を変更・検証するとき
- 対象本文にコードフェンスを含む prompt の埋め込み処理や oracle との互換性を確認するとき
- indexing の互換公開面や __all__ を変更・検証するとき

## Do not read this when
- index entry の意味内容そのものや INDEX.md のルーティング規則だけを変更・確認するとき
- indexing builder と無関係な ACP builder の parameter や schema を扱うとき
- builder の公開 API ではなく、個別の index entry 生成結果だけを確認するとき

## hash
- def8798e791871f2c92eaf5046aced1938491fb93d3aca0f1993fb17915e4523

# `test_acp_builder_oracle_review_parameters.py`

## Summary
- 対象は oracle review ACP builder 群の回帰テストで、enumerate・judge・merge・advocate/challenger validation の canonical builder 互換性、公開 API、モデル・reasoning・file access 設定、schema、policy 注入、placeholder 処理、動的 prompt の code fence 境界保護を検証する。review builder の parameter/schema/adapter 契約を横断して確認したいときの入口。

## Read this when
- oracle review 用 ACP builder の builder 実装や互換 module の公開面を変更・レビューするとき
- review builder の Structured Output schema、policy block 注入、動的入力の placeholder 保持、nested code fence 保護の回帰を確認するとき
- enumerate、judge、merge、finding validation の各段階に共通する AgentCallParameter 契約を調べるとき

## Do not read this when
- oracle review builder 以外の ACP builder の挙動だけを調べるとき
- canonical builder の実装詳細や正本 schema 自体を確認する必要があるときは、対応する oracle source・JSON schema を直接読む
- 一般的な review ロジック、所見判定基準、prompt policy の定義だけを確認したいときは、それぞれの正本 policy または builder 実装を直接読む

## hash
- 2337544b220a03f783de310ca1a1347a6c0daaa73d71bb075e13de8f4265d9e8

# `test_acp_builder_session_join_parameters.py`

## Summary
- session join の conflict resolution builder 契約を検証するテスト。公開モジュールの export 範囲と canonical builder との同一性、repo write 権限・モデル・推論設定・プロンプト内容・実行設定を確認する。競合パスに三連バッククォートが含まれる場合も、プロンプト内のコードフェンスが正しく保護されることを検証する。

## Read this when
- session join の conflict resolution 用 builder の公開 API、生成パラメータ、プロンプト契約、または競合パスのコードフェンス処理を変更・検証するとき。

## Do not read this when
- conflict resolution builder 以外の session join 処理を確認するとき。
- builder の正本実装そのものを変更・調査するときは、対応する oracle の正本を直接読む。

## hash
- ce405ab6daf7522772aa652afdcdf4fc3c5b7f614eca548c44a5b579f5186cae

# `test_acp_builder_tui_parameters.py`

## Summary
- TUI 起動 builder が固定する agent call parameter・実行ポリシー・prompt の構成と、互換 module の公開面および canonical builder との同一性を検証する pytest である。TUI 起動 builder の設定や prompt 規定、公開 API の適合性を確認する作業ではこのファイルを読む。

## Read this when
- TUI 起動 builder の固定 parameter、実行設定、prompt に含まれる規定を検証・変更するとき
- acp.builder.tui.launch_tui の公開 export や canonical builder との互換性を確認するとき

## Do not read this when
- TUI 起動 builder の実装仕様そのものを確認するときは、対応する oracle の launch_tui.py を直接読む
- TUI 以外の builder、または一般的な repository fixture の挙動だけを確認するとき

## hash
- bfb88796c82379602e5971934ef3b8c617460b9e93035d96453f38f92d5b44c8

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
- TUI サブコマンド起動直前の CLI 前処理を検証するテスト。エディタ入力の生成・保存・反映、doctor 前処理、Codex TUI 起動パラメータ、既存 Git 差分の保持、linked worktree 時の記録先と `.gitignore` を扱う。TUI の前処理やその外部挙動を変更・確認する際のテスト入口。

## Read this when
- `tui` サブコマンドの起動順序、エディタ編集結果、Codex TUI 呼び出し、linked worktree 対応を確認するとき
- TUI 前処理や prompt editor input の実装を変更し、外部挙動への適合を検証するとき

## Do not read this when
- TUI 以外のサブコマンドの挙動を確認するとき
- TUI 前処理の実装詳細そのものを調べるときは、正本仕様または対象実装を直接読む場合

## hash
- 4ec51d8c9ea69e3030d8fd0a7fe6003bcf7e6da6543aa490287e6c65756ccb8c

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
- Codex 実行のランタイム path と権限境界を検証するテスト群。
- 並列実行時の timestamp 付きログ path の衝突回避、agent call の cwd、repo root 配下への schema 保存、sandbox モード変換、`.agents` path の権限設定非注入を確認する。
- Codex 実行経路の path 生成・cwd・schema・sandbox 引数の挙動を、実運用に近い subprocess と linked worktree を用いて検証する入口。

## Read this when
- Codex 実行時の cwd、schema 保存場所、ログ path の一意性、sandbox 引数を確認・変更するとき
- linked worktree や PURE_ORACLE_READ におけるファイルアクセス境界を検証するとき
- Codex CLI 引数に `.agents` の個別権限が注入されていないことを確認するとき

## Do not read this when
- Codex 実行の prompt 生成規則や file access policy の正本仕様そのものを確認するとき
- Codex runtime path 以外の機能や一般的なテスト実行方法を調べるとき

## hash
- 0328ce2ff2e8f6903c74f7d30ee0059247a400f562dc42e1a745c124af509d49

# `test_codex_runtime_quota_retry.py`

## Summary
- quota 枯渇後の Codex exec における probe・待機・復帰・resume／再実行の外部挙動を、実際の subprocess 呼び出し、session ID、stdout JSONL、call log、subcommand log、CODEX_HOME、cwd とともに検証する回帰テスト群。quota retry 状態機械を一体として追跡するため、個別の probe やログ検証へ分散せず、このテストを関連する実装変更の検証入口として読む。

## Read this when
- Codex quota exceeded 後の polling、代表 quota probe、capacity retry、待機中呼び出しの共有、probe 失敗伝播を変更・調査するとき。
- quota 復帰時の session ID 復元、resume と prompt 再実行の分岐、stdout JSONL の妥当性検証を変更・調査するとき。
- Codex exec の call log／subcommand log の purpose・status・エラー記録、probe の最小設定、CODEX_HOME や Codex cwd の扱いを変更・調査するとき。
- quota retry を並行実行、KeyboardInterrupt、quota poll 上限、進捗出力失敗などの境界条件から検証するとき。

## Do not read this when
- quota retry 以外の通常の Codex exec 成功・失敗経路だけを変更・調査するときは、まず通常実行の実装と対応する基本テストを読む。
- quota probe の正本 prompt や builder の仕様そのものを変更・調査するときは、まず quota probe builder とその正本仕様を直接読む。
- ログ形式全般や SubcommandLogger の共通契約だけを変更・調査するときは、まずロガー実装と共通ログのテストを直接読む。

## hash
- 0b7cbd9bc30e732ce1f90de3a42ac1495be9b32674f3b21a7e09a36760f75dfb

# `test_codex_runtime_retry.py`

## Summary
- `run_codex_exec` の再試行・失敗処理と、その外部ログを検証するテスト群。Structured Output の補正、schema 検証、capacity retry、JSONL error、中断、retry 上限、成果物差分の保持・復元を、Codex subprocess の呼び出し回数、session、call log、subcommand event と併せて確認する。これらの状態機械の分岐を横断して検証したい場合の入口となる。

## Read this when
- `run_codex_exec` の Structured Output 不合格時の補正、同一 session の再試行、parse failure、postcondition 違反、retry 上限を確認するとき。
- capacity error や未知の JSONL error の判定、戻り値に依存しない retry、KeyboardInterrupt の失敗記録を確認するとき。
- retry や補正 turn の前後で成果物差分を保持・復元する挙動、Codex call log と subcommand event の対応を確認するとき。

## Do not read this when
- Codex subprocess の通常成功経路や CLI 引数の実装詳細だけを確認したいとき。
- ログ schema の正本定義や `run_codex_exec` の実装そのものを変更・調査するときは、対応する仕様・実装ファイルを直接読む。
- retry 以外のテスト領域や、単純な schema 定義の妥当性だけを確認するとき。

## hash
- 17ee2256b6f20287b791cb547cd86421a2f8d4852d4a71e94375381b38547815

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
- Codex TUI 実行経路のテスト。完全な prompt と CLI 引数、アクセスモード、linked worktree の実行位置、call log とサブコマンドイベントの記録を検証する。Codex CLI 不在、KeyboardInterrupt、非 0 終了、timestamp 衝突時のログ保持も扱うため、TUI 呼び出しや実行結果の記録を確認する際の入口となる。

## Read this when
- Codex TUI の prompt 引き渡し、sandbox/access mode、--cd などの CLI 呼び出し引数を変更または検証するとき
- Codex TUI の call log やサブコマンドイベント、CLI 不在・割り込み・非 0 終了時のエラー記録を変更または検証するとき
- linked worktree での TUI 実行や同一 timestamp の call log 保存を扱うとき

## Do not read this when
- 通常の非 TUI Codex 実行経路や別サブコマンドのテストを調べるとき
- TUI の正本仕様やログ形式そのものを確認する必要があり、対応する仕様書を直接読むべきとき

## hash
- aa2ec2639fe3480424c5b0d1994460fe8925eac0d11d713a7ad535307eb184ec

# `test_doctor_cli.py`

## Summary
- doctor preprocess の CLI 実行と直接呼び出しを通じて、`.cmoc/gu` の ignore・untrack、`.agents/.gitkeep`、runtime config、refactor state の修復 lifecycle を統合的に検証するテスト。
- reporter の事前検証、degraded warning、予期しないエラーや中断、共有 repository lock の待機を扱う。
- 修復 commit が既存の staged index、unstaged hunk、index flag、intent-to-add、rename、削除を保持し、利用者変更を取り込まないことを検証する。
- linked worktree では repository root と current worktree の修復対象を分離し、生成物の追跡・ignore・ログ配置を確認する。doctor preprocess の外部契約をまとめて読むための統合テスト入口である。

## Read this when
- doctor preprocess の外部挙動、修復順序、CLI と直接呼び出しの lifecycle を確認するとき
- Git index の保持、repair commit の対象、既存 staged/unstaged 変更の分離を調べるとき
- `.cmoc/gu`、`.agents`、config、refactor state、linked worktree、reporter、共有 lock の連携を一度に検証するとき

## Do not read this when
- doctor 実装内部の個別関数の詳細や単体ロジックだけを調べるとき
- reporter、Git helper、config、refactor state など単一要素の仕様や実装を直接確認するとき
- doctor preprocess 以外の CLI サブコマンドの挙動を調べるとき

## hash
- f7fc57ae363f853e3c0844054398b440a3997e51f945415cbc609301cdc46882

# `test_editing_run_cli.py`

## Summary
- workload fork と共通 run join/abandon の統合 realization test。
- realization apply/refactor の fork lifecycle、共通 session state・run worktree・branch・process tracking、agent 境界、INDEX 更新、commit/rollback、cleanup を検証する。
- fork report と lifecycle report、primary report、通知、feedback observation、interruption、error recovery、force-resolve、merge conflict、rename/delete、異常な path や symlink の扱いまで一連の run lifecycle として確認する。

## Read this when
- realization apply/refactor fork の統合 lifecycle や共通 run state の挙動を変更・検証するとき
- run join または run abandon の merge、cleanup、process 停止、branch/worktree 回収、失敗復旧を確認するとき
- fork・join・abandon の report、通知、INDEX 更新、rollback、user interruption の連携を調査するとき

## Do not read this when
- 単一の realization apply/refactor 実装の詳細だけを確認する場合は、対象実装や専用テストを直接読む
- INDEX.md 生成の一般規則だけを確認する場合は、この統合 lifecycle test を読む必要はない

## hash
- 769b646539819645ba85fe8cd9adf544b57c9fa33747a87b4cab01d366c96de4

# `test_feedback.py`

## Summary
- feedback の pending observation を raw store から収集し、agent normalization・候補比較・verification を経て active issue または machine aggregate に集約する一連の外部挙動を検証するテスト。
- report cut、checkpoint、incomplete/interrupted report、current pointer、generation artifact、cleanup manifest を含む atomic publication と再開・復旧境界を検証する。
- agent-facing reporter の MCP protocol、collector の context/rate limit、path boundary・secret masking、raw observation の妥当性、machine observation の recurrence threshold を検証する。
- feedback の実装変更やテスト要件を追う際は、report subcommand、feedback state、observation、console/file log の正本仕様および normalize/verify builder の oracle 実装から入るための統合テスト入口である。

## Read this when
- feedback report の pending raw 処理、issue candidate の正規化・verification、current evidence に基づく unresolved/resolved 判定を確認または変更するとき
- active state の generation publication、current pointer、report cut の checkpoint、再実行、部分 cleanup、破損検出を確認または変更するとき
- agent reporter と collector の MCP 境界、観測保存、rate limit、context 検証、secret masking を確認または変更するとき
- machine observation の bounded aggregate と recurrence threshold、期限切れ後の active issue 維持を確認または変更するとき

## Do not read this when
- feedback の正本仕様や通常の CLI 実装を直接確認する場合は、この統合テストではなく列挙された oracle 文書または runtime/subcommand 実装を直接読む
- feedback observation/reporting と無関係なテスト、または単純な reporter schema・builder の単体仕様だけを確認する場合は、対象の専用実装・schema・builder を直接読む

## hash
- 844f3bc855ced3a7a4e9d4aa156e2fcbeb981f6d111acdbfa0b3a7c45ac01b93

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
- `cmoc indexing` の CLI と preflight の外部挙動を検証するテスト群。doctor による初期化、clean／dirty worktree の扱い、linked worktree の対象判定、Codex structured output による INDEX.md 生成、既存ハッシュの再利用、INDEX.md のみを対象とする commit、既存差分の保持、失敗時のエラー処理を確認する。indexing の実装や仕様変更時に、サブコマンド全体の lifecycle と commit 条件を確認するための入口となる。

## Read this when
- `cmoc indexing` の CLI 事前条件、doctor、worktree、INDEX.md 更新、Codex 呼び出し、commit lifecycle の外部挙動を確認・変更するとき。
- indexing preflight の設定読み込み、既存差分、fresh な INDEX.md、対象 worktree、INDEX.md 以外の差分保持を検証するとき。

## Do not read this when
- `cmoc indexing` 以外のサブコマンドの挙動を確認するとき。
- INDEX.md の一般的な構造やルーティング規則を確認するとき。
- 実装内部の詳細や正本仕様を直接確認すべきで、CLI の外部挙動テストを読む必要がないとき。

## hash
- 1541e44eb5f31ee5deaa8d5a1955bd5dd96355538f1d140b3f443c56ebebb8a1

# `test_indexing_common.py`

## Summary
- `commons.indexing` の INDEX entry 生成・解析・hash 再利用と、directory traversal／INDEX 更新の直接テストをまとめたファイル。
- malformed entry の再生成、部分書き込みの復元、空ディレクトリ・nested memo・symlink・特殊ファイルの扱い、安定順序、並列更新、logger 伝播、worktree 間 lock、非 UTF-8 ファイル名の hash を検証する indexing runtime 回帰の入口。

## Read this when
- `commons.indexing` の entry parse・render・hash・update_indexes の挙動を確認するとき
- INDEX 更新における directory traversal、symlink／特殊ファイル除外、空ディレクトリ、nested memo の方針を確認するとき
- INDEX entry 生成順序、部分更新失敗時の復元、並列実行、Codex event の logger 伝播、pushd 中の worker 制約を確認するとき
- INDEX.md symlink の置換、非 UTF-8 filename の hash、linked worktree 間の indexing lock 共有を確認するとき

## Do not read this when
- CLI lifecycle から見た indexing サブコマンド全体の統合挙動だけを確認するとき
- INDEX entry の生成実装や traversal の正本仕様を確認するときは、対応する実装または oracle 文書を直接読むとき
- indexing と無関係なテストや一般的な INDEX.md ルーティング規則を確認するとき

## hash
- 102cebfb2f9201db7108a7a2820a1053b2ade13caf5d88ebd8a2be3de27094ce

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
- 対象は `cmoc oracle edit` の main-worktree 実行制御を検証する pytest です。成功時と main agent call／仕様削減 agent call の各失敗時について、editor 入力、Git 差分、session state、実行順序、通知、診断レポートを比較します。
- テスト用 repository・session state・Codex home を準備し、doctor、editor、indexing preflight、起動前提検査、agent exec、通知を差し替えて観測します。成功時のみ仕様削減用 exec が続き、失敗時も既存差分と editor 入力コピーを保持する契約を確認します。
- builder 失敗時に editor work file を予約しないこと、linked worktree・session 外・inactive session で起動を拒否することも検証します。oracle edit の CLI 実行制御と失敗境界を調べる際のテスト入口です。

## Read this when
- `cmoc oracle edit` の agent exec 回数、実行順序、成功／失敗時の分岐を変更または検証するとき
- oracle edit の editor 入力、Git 差分、session state、通知、診断レポートの保持境界を確認するとき
- oracle edit の起動前提違反や builder 失敗時の後処理をテストするとき

## Do not read this when
- oracle edit の builder や本体実装の詳細を直接調査する場合は、対応する実装・仕様ファイルを先に読むとよい
- oracle edit と無関係な CLI サブコマンド、一般的な indexing、Git、session state の挙動を調べる場合

## hash
- 2414dd4f42657a2b8aa399451d0014c78f9a02c857c003825596829da8a39dfc

# `test_oracle_investigation_cli.py`

## Summary
- `oracle investigation` CLI がセッション前提なしで起動できることを、doctor 前処理、プロンプト編集、入力収集、builder、TUI 起動の順序と引数で検証するテスト。
- 起動時に pure-oracle-read のファイルアクセス、最大推論、indexing preflight などの実行パラメータが設定されることを確認する。
- oracle investigation の launch TUI realization adapter が指定された builder だけを公開することを検証する。

## Read this when
- `oracle investigation` CLI の起動条件や、起動前後の処理順序を変更・確認するとき
- oracle investigation の prompt editor 入力から実行用 agent parameter へ至る経路を確認するとき
- `launch_tui` adapter の公開 API や export を変更するとき
- doctor preprocess、indexing preflight、TUI 起動の連携を回帰検証するとき

## Do not read this when
- oracle investigation の正本仕様や prompt policy の内容自体を確認するときは、参照先の oracle 文書を直接読む
- launch TUI builder の実装詳細を確認するときは、`launch_tui` realization adapter を直接読む
- 他の oracle サブコマンドの起動条件や builder export を確認するときは、それぞれ対応するテストまたは実装を読む

## hash
- d62d80010862e9689a4db3e0a30463898bb9dc4c025c94a4415f9a1ea2b084c5

# `test_oracle_review_loop.py`

## Summary
- oracle review の finding loop を検証する回帰テスト群。review worktree の隔離、oracle ごとの finding 列挙、finding の merge、challenger/advocate による理由検証、judge、Structured Output の postcondition、割り込み時の部分結果保持、および merge 補正失敗の伝播を、fake Codex call と同一の review round で検証する。oracle review loop の実装変更や、これらの外部契約・回帰挙動を確認する際のテスト入口である。

## Read this when
- oracle review の finding 列挙・merge・理由検証・judgement のループを変更またはレビューするとき
- review worktree の call context、finding の関連付け、同一周回の理由伝播、Structured Output postcondition を検証するとき
- KeyboardInterrupt 復旧時の完了済み judgement・検証理由の保持や、merge 出力補正失敗の伝播を確認するとき

## Do not read this when
- oracle review loop の実装や仕様を直接確認する必要があり、テスト結果や回帰条件ではなく正本仕様・実装本体を読むべきとき
- oracle review と無関係なテスト、または単純な Codex call 共通処理の挙動だけを確認するとき

## hash
- 42271bbc345bd0cb19d9de85a0b29f9d6119bf838d89bf730c1380d36f341ded

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
- 対象は oracle review の report と CLI 出力を一体で検証する回帰テストで、report の節順・finding の受理／棄却分類・件数・path 集計・YAML／Markdown エスケープ・timestamp 予約、CLI の成功・中断・処理失敗時の出力と error report を扱う。oracle review の挙動や report contract を変更・確認する際のテスト入口である。

## Read this when
- oracle review の report 形式、finding 表示、評価対象 oracle file の集計、CLI の完了・中断・失敗時の出力を変更または検証するとき
- report の path alias、symlink、特殊文字、YAML 文字列化、同一 timestamp の保存競合を扱う実装を確認するとき
- oracle review の列挙・検証・merge・judge 呼び出しや、未完了処理を含む report の回帰挙動を確認するとき

## Do not read this when
- oracle review の実装ロジック自体を変更・調査するだけで、report や CLI 出力の契約を確認する必要がないとき
- Structured Output schema の項目定義や prompt policy の内容だけを確認するとき
- oracle review と無関係な CLI サブコマンド、report、または一般的な Git／session 処理を扱うとき

## hash
- b5217b17aab1d9109c5b55ad6fd52e478d758a63ca1d3cff8da2492461f4c91b

# `test_oracle_review_targets.py`

## Summary
- oracle review のパス解決とレビュー対象列挙を検証する pytest テスト。finding の oracle path 解決、symlink・外部パスの境界、session/full scope の対象集合、tracked/ignored・binary・改行を含む Git path の保持、対象外ファイルや非 regular file の扱いを対象とする。
- oracle review の対象列挙または finding path 解決を変更・検証する際の挙動確認の入口。

## Read this when
- oracle review の session/full scope における対象ファイル集合や差分終点を変更・検証するとき
- finding の oracle path、work-root/oracle-root alias、symlink、外部パスの扱いを変更・検証するとき
- AGENTS.md・INDEX.md・非 regular file の除外または拒否契約を確認するとき

## Do not read this when
- oracle review の出力表示や finding 評価ロジックだけを確認するとき
- 対象列挙・パス解決に関係しない CLI やセッション機能を変更するとき
- テスト対象の挙動を変更しない単なる INDEX.md 更新を行うとき

## hash
- 5fe6b880e87222f7aee54f88fa39c4964edbbce1781f35d8fabcae7c4f4e10ad

# `test_oracle_review_worktree.py`

## Summary
- oracle review の回帰テスト群。linked worktree の session branch と oracle を対象にした隔離 review run の lifecycle、snapshot fork、run target 衝突、作成・中断・cleanup、lock 直列化、失敗 report を検証する。
- review worktree で生成された INDEX.md のみを session に統合する契約を検証する。INDEX.md 以外の差分や indexing 対象外の INDEX.md を拒否し、preflight の更新先、nested path、rename、Git quoted path、merge conflict の解決・復旧を確認する。
- oracle review 実装や review worktree lifecycle、INDEX 差分の統合・競合処理を変更するときの回帰テスト入口であり、一般的な INDEX 生成仕様や無関係な CLI のテスト入口ではない。

## Read this when
- oracle review の隔離 worktree、session branch、snapshot commit、run branch、run target の作成または cleanup を変更・検証するとき
- oracle review の KeyboardInterrupt、BaseException、lock 待機、merge 中断、cleanup failure、error/interrupted report の挙動を確認するとき
- review worktree の agent call cwd、preflight、INDEX.md 差分検証、対象外 INDEX の拒否、session への merge を確認するとき
- INDEX.md の追加・削除・rename、nested directory、Git が quote するパス、INDEX 競合の復旧処理を変更するとき

## Do not read this when
- oracle review の対象外である一般的な CLI 機能、通常の run lifecycle、または一般的なテスト規約だけを確認するとき
- INDEX.md の生成ルールやルーティング内容そのものを確認することが目的で、review worktree からの差分検証・統合契約を扱わないとき
- Codex agent call の finding schema や所見判定だけを変更し、隔離 worktree、INDEX 差分、report、cleanup の挙動に影響しないとき

## hash
- b410bb049a91948723137c40b39964065182f25102a70aba9f317e2c6cc2e6eb

# `test_packaged_import.py`

## Summary
- packaged layout にソースツリーをコピーし、隔離環境での import と実行を検証するテスト。
- oracle review・quota probe・oracle edit・prompt editor・ACP basic・cmoc config のパッケージ配置、正本参照、公開 import 境界、prompt/schema 生成、公開定義を確認する。

## Read this when
- packaged layout での import、setuptools の package 配置、正本 oracle と realization 側の再公開境界を調査するとき
- oracle review/edit の builder や prompt editor 入力境界が隔離環境で正本の schema・prompt・設定を参照することを確認するとき
- ACP basic または cmoc config の公開面と再公開定義を検証・変更するとき

## Do not read this when
- 個別 builder の prompt 内容や schema 定義そのものを変更・確認する場合は、対象の builder 実装または schema ファイルを直接読むとき
- packaged layout や import 境界に関係しない単体ロジック、CLI 挙動、一般的なテスト実行を調べるとき

## hash
- 9e8e919a4a508ba8b0915cfaea72beaed63dbfba4e3a6cc2b37517ea3d086f78

# `test_primary_report.py`

## Summary
- 非対話末端サブコマンドの primary report 完了契約を検証するテスト。doctor、indexing、session、oracle、realization、run、feedback report の早期エラーで、固有保存先・必須 front matter・診断内容・終了コードを確認する。
- feedback report のユーザー中断、realization refactor の fallback 中断、保存未確認時の internal failure も検証し、report publication と invocation summary の境界および未保存パスの非表示を担保する。

## Read this when
- 非対話サブコマンドの primary report 保存契約や terminal classification を変更・検証するとき
- 早期エラー、中断、fallback、primary report 未保存時の共通終了処理を調査するとき

## Do not read this when
- 各サブコマンドの通常成功時の処理や個別業務仕様だけを確認するとき
- primary report の生成実装そのもの、または各サブコマンド固有の詳細仕様を直接確認すべきとき

## hash
- cf2bb62898357a0e6e155da27b15aa9678e42e3a7a2a15ae68a25c35dd0bdd9f

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
- prompt part の各 policy builder と complete prompt の組み立て・Markdown rendering を検証する回帰テスト。policy の構造・カテゴリ順・注入順・重複防止、feedback/file-access 指示、placeholder 展開と競合検出、root/path context ごとの挙動を扱う。prompt builder 周辺の実装変更や回帰確認の入口となる。

## Read this when
- policy builder、complete prompt、SDHeader/SDPolicy の rendering や注入順を変更・調査するとき。
- placeholder の統合・競合検出、root token の保持、path context に応じた file access policy を確認するとき。
- oracle/realization policy、findings、conflict resolution、index-entry policy の注入内容と重複防止を回帰検証するとき。

## Do not read this when
- prompt builder や policy に関係しない機能領域だけを扱うとき。
- policy の詳細な正本要求を確認する場合は、対応する policy builder や oracle 文書を直接読むとき。

## hash
- e8f4ccdce5f2b10363fbf8b78d8e7eef496a6c6d02ff9e4024ffda9ad6709fdd

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
- テスト対象の Codex 実行プロファイル境界を検証する。file access mode から専用 sandbox 引数への変換、model/provider 上書きの TOML 表現と選択 provider の検証、通知・feedback 環境の argv/env への漏洩防止、schema のバイト保持、出力 JSON の不正 UTF-8 処理を扱う。Codex 起動引数や runtime_codex_profile の契約を変更・確認するときのテスト入口であり、一般的な agent 呼び出しロジックや他の実行経路のテストからは直接始めない。

## Read this when
- Codex argv の sandbox、model、provider、notification、feedback context の上書き契約を変更または検証するとき
- Codex 用 schema の保存形式や output JSON の読み取り失敗処理を変更または検証するとき
- runtime_codex_profile の実装変更が既存の argv、環境変数、TOML encoding に適合するか確認するとき

## Do not read this when
- Codex の実行プロファイル、上書き引数、schema/output 処理に関係しない agent 呼び出しや一般的な設定を扱うとき
- 対象の具体的なテストケースや期待値を直接確認する必要があり、実装または正本仕様を読む方が適切なとき

## hash
- fd57397ab4bd2c27f6aa6e7aa845f769276cdc416ad76862db195a9d23db5268

# `test_runtime_config.py`

## Summary
- CmocConfig の既定値、JSON 永続化、読み込み・書き込み境界、入力検証を検証するテスト群。論理 model class と reasoning effort の既定値や定義順、設定ファイルの round-trip、欠落・破損・過度なネスト・不正なパスのエラー変換を扱う。
- Codex の model provider、model spec、provider-local settings、oracle review の設定について、型・値・JSON/TOML 表現の妥当性、不正な値の拒否、互換性のための廃止項目の除外を確認する。
- 設定ランタイム実装や設定仕様の変更時に、対応する外部挙動と安全なファイル境界を確認するための入口となる。

## Read this when
- CmocConfig の既定値、設定の JSON 化・復元、config.json の読み書き挙動を変更または調査するとき。
- model provider、model 名、reasoning effort、oracle review 回数、provider-local settings の入力検証やエラー処理を変更するとき。
- 設定パスの symlink・named pipe・非通常ファイル、破損 JSON、過度なネストなどの境界挙動を確認するとき。

## Do not read this when
- 設定の実装詳細や正本仕様そのものを確認する必要がある場合は、先に config 実装または設定仕様の対象を直接読む。
- CmocConfig や設定ファイルの挙動に関係しない CLI 機能、他のデータ形式、一般的なテスト基盤だけを調査するとき。

## hash
- 1cf5b26973c5cc169cbd899ae29c4fee3511a7aa2e0215dd7f48a8f07d822f0e

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
- session fork・join・abandon の CLI 外部挙動をまとめて検証する回帰テスト。session branch と永続 state の作成、状態遷移、cleanup、rollback、linked worktree、dirty worktree や欠損 state の拒否を扱う。
- session join における conflict 解消、Codex 呼び出し境界、対象外変更の拒否、特殊な conflict path、削除・mode 変更の扱い、merge 後の branch cleanup を検証する。
- session サブコマンドの実装挙動や app specification とテスト要件の対応を確認したい場合の入口であり、個別の fork・join・abandon 実装詳細は対応する sub_commands モジュールを読む。

## Read this when
- session fork、join、abandon の外部挙動を変更・検証するとき
- session state、session branch、linked worktree のライフサイクルを調査するとき
- session join の conflict 解消や Codex 実行時のファイルアクセス境界を確認するとき
- dirty worktree 拒否、preprocess、rollback、cleanup 失敗時の挙動を確認するとき

## Do not read this when
- session CLI の単一サブコマンド実装だけを確認する場合は、対応する sub_commands.session の実装を直接読む
- doctor preprocess 単体の仕様や実装を確認する場合は、doctor preprocess の仕様・実装を直接読む
- session state のデータ形式だけを確認する場合は、session_state の正本仕様を直接読む

## hash
- dd07e9312ef147ae36ef1658f0295d3c935744ed0d61a8b2511c165835f7f8b7

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
- 構造化文書の Markdown renderer の単体テスト。空行縮約、コード fence、見出し深度、参照 block、参照検証を行い、SDPolicy の描画と basic.struct_doc 互換 API、child 型検証も確認する。renderer の整形挙動や互換性の変更時に、このテストを実装側の参照先として読む。

## Read this when
- Markdown renderer の出力整形、コード block の fence、見出し深度、SDTagBlock の参照表現を変更・調査するとき。
- SDPolicy のカテゴリ描画順や空カテゴリの扱いを変更・調査するとき。
- basic.struct_doc の canonical 型再公開や構造化ノードの child 型検証を変更・調査するとき。

## Do not read this when
- renderer の実装仕様や内部アルゴリズムを確認する場合は、テストではなく oracle の struct_doc 実装を直接読む。
- Markdown renderer と無関係なテストや、構造化文書ノードの生成規則だけを確認する場合は、このテストを入口にしない。

## hash
- 74f66d1c3c2c7a3f1cc0fc799ad54ad3f43ea1aaaff9e5ea222269c0d228f0f1

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
