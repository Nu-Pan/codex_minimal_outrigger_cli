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
- editing run workload の canonical builder adapter を検証するテスト。
- apply と refactor の builder が正本関数・Structured Output schema・実行設定・prompt 内容を適切に利用するかを確認する。
- raw git diff に含まれる三連バッククォートや prompt 境界風文字列を安全に保持できることも検証する。

## Read this when
- editing run の apply または refactor builder の互換 import、prompt 構成、実行設定、schema 選択を変更・確認するとき。
- builder が埋め込む raw diff のコードフェンスや prompt 境界の扱いを調査するとき。
- canonical builder と互換経路の再公開関係を確認するとき。

## Do not read this when
- builder の実装詳細そのものを直接調査する場合は、対応する realization または oracle の builder 本体を先に読むとき。
- builder と無関係な ACP 機能や、一般的な git worktree 処理を調査するとき。
- このテストの検証対象である Structured Output schema の仕様だけを確認するときは、対応する schema ファイルを直接読むとき。

## hash
- 9ce2e1fbff99be78898e9a12725edb8ec64ea3167883bf5d5da37dbee5f175d7

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

# `test_acp_builder_oracle_review_parameters.py`

## Summary
- review 用 ACP builder の parameter、schema、公開 builder 互換性、oracle read 契約を回帰検証するテスト。動的 prompt に埋め込む所見・理由などの code fence や section 風文字列を保護する境界検証も含む。

## Read this when
- oracle review の enumerate、judge、merge、validate builder を変更・レビューするときに、canonical builder との parameter/schema 互換性や公開面を確認したい場合。
- 動的入力を含む review prompt の fence 保護、placeholder、section 境界、renderer の空行正規化に関する回帰条件を確認するとき。

## Do not read this when
- review builder 以外の ACP builder の仕様やテストを確認する場合。
- 個別 builder の実装詳細や oracle schema の正本を直接確認したい場合は、対応する oracle file・schema、または canonical builder を先に読む。

## hash
- 41f223d1c4f48473877baa91190d7590b1309aadbf46cf0180dc09daafadf6b4

# `test_acp_builder_session_join_parameters.py`

## Summary
- session join の conflict resolution builder 契約を検証するテスト群。
- 互換モジュールの公開境界と canonical builder への委譲を確認する。
- 競合解決用パラメータの権限、実行場所、プロンプト構成、ポリシー、indexing preflight 設定を検証する。
- 競合対象パスに三連 backtick が含まれる場合も、プロンプト内のコードフェンスが壊れないことを確認する。

## Read this when
- session join の conflict resolution builder の公開 API や互換モジュールの export 契約を確認するとき。
- conflict resolution 用 agent parameter の file access mode、cwd、schema、prompt、preflight 設定を変更または検証するとき。
- 競合ファイルパスのプロンプト埋め込みと nested code fence の扱いを確認するとき。

## Do not read this when
- session join の conflict resolution 以外の builder の契約だけを調べるとき。
- builder の実装詳細そのものを確認する必要があり、対応する正本実装を直接読むべきとき。
- 競合解決パラメータのテストではなく、一般的な repository fixture や git 操作の仕様だけを確認するとき。

## hash
- 5b2493d8b3453e874d7ecb2703e6ac271a0aa6b27a0933a5734b72f832ecde80

# `test_acp_builder_tui_parameters.py`

## Summary
- TUI 起動 builder がオリジナル prompt に依存せず固定の実行 parameter・ポリシー・prompt 構成を生成することを検証するテスト。
- 互換 module の公開 API が現行の TUI parameter builder のみに限定され、正本 builder を参照することを検証する。

## Read this when
- TUI 起動 builder の固定実行設定、prompt に含める規定・objective・original prompt の配置、または editor input handoff と indexing preflight の検証内容を確認するとき。
- acp.builder.tui.launch_tui の互換 module の公開面や canonical builder との同一性を確認するとき。

## Do not read this when
- TUI 起動 builder の実装仕様そのものを確認したい場合は、対応する oracle の正本実装を直接読むとき。
- TUI 以外の builder の parameter や prompt、または一般的な TUI 挙動を調査するとき。

## hash
- db19a70f5e02f1cc045a258121dcc5add5a57ecb3e8bffeb351459a8ca2233e7

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
- TUI 起動直前の CLI 前処理について、エディタ入力の生成・保存、編集済みプロンプトからの Codex TUI 起動、既存の Git 差分保持を検証するテスト。
- 通常のリポジトリと linked worktree の両方で、doctor 前処理、indexing preflight、agent call context、`.cmoc` の ignore とログ配置を確認するテスト入口。

## Read this when
- `tui` サブコマンドの起動順序や、エディタで編集した依頼文が TUI 起動パラメータへ反映される挙動を確認・変更するとき。
- linked worktree での TUI 実行時に、記録先・作業ディレクトリ・リポジトリルートの扱いを確認するとき。
- TUI 前処理が Git の staged/unstaged 差分や `.cmoc` の ignore、editor input／sub_command ログに与える影響を検証するとき。

## Do not read this when
- TUI 起動後の対話処理や Codex 本体の内部動作だけを確認したいとき。
- プロンプト編集テンプレートの単体仕様や prompt builder の実装を直接確認する場合は、対応する正本仕様・実装を先に読むとき。
- TUI 以外のサブコマンドの前処理や、一般的な CLI 共通処理だけを調べるとき。

## hash
- 8a808ab42d8ff47be5ae74d45e143b53d9ac98f78e519b91f13903008e6d7a56

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
- Codex exec の実行環境と成果物配置の契約を検証するテスト。
- agent_call_cwd が Codex の cwd と --cd に反映され、PURE_ORACLE_READ や REPO_WRITE の sandbox 設定が適切に変換されることを確認する。
- リンク済み worktree でも schema をリポジトリ root 配下へ保存し、`.agents` の実在パスを個別権限として注入しないことを確認する。
- 並列実行時に timestamp 付きの call、prompt、標準出力・標準エラー、出力ファイルのパスが衝突せず予約されることを確認する。

## Read this when
- Codex exec の cwd、sandbox 引数、schema 保存先、worktree 境界、または並列ログパス予約の挙動を検証・変更するとき。
- runtime 呼び出しが正本仕様のファイルアクセス境界と成果物配置に適合しているか確認するとき。

## Do not read this when
- Codex exec の実装詳細を直接調べる必要があり、まず `commons.runtime_codex` や関連 policy の正本を読むべきとき。
- ログパスや sandbox、schema 配置に関係しないテストや機能を調べるとき。

## hash
- 98c46375b79e6dbeadfd364f713368fafa8f404f0b2226dc1184aea6acfc42a8

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex quota 枯渇後の probe・resume・再実行を含む retry 状態機械の外部挙動を、呼び出し列・ログ・session ID・環境・並行実行で検証するテスト群。
- quota availability probe adapter の canonical prompt、公開面、相対 CODEX_HOME 解決、異常 stdout、poll 上限、probe 失敗、待機状態解除までを確認する回帰テストの入口。

## Read this when
- Codex exec の quota 待機・復帰・retry 制御を変更または検証するとき。
- 代表 probe の共有、resume session ID の復元、probe／subcommand／call log の整合性、並行 quota 呼び出しの挙動を確認するとき。
- quota probe adapter の prompt・call kind・readonly 実行条件、または CODEX_HOME と Codex cwd の関係を調べるとき。

## Do not read this when
- quota retry ではなく通常の Codex exec 実行、一般的な subprocess 起動、または quota probe の実装詳細だけを直接確認したいとき。
- INDEX.md のルーティングや正本仕様の内容を確認することが目的で、テストによる外部挙動の検証が不要なとき。

## hash
- 0648e1f7b2d246f1c87eff154b759cc14879a464627401de07e8ebfb1be14c14

# `test_codex_runtime_retry.py`

## Summary
- `run_codex_exec` の Structured Output 出力補正と retry 状態を検証する。
- capacity failure、JSONL error、中断、retry 上限などの異常系で、subprocess 呼び出し回数、最終結果、CmocError、共有ログ列を一続きの外部挙動として確認する。
- 補正や retry に伴う session、call log、subcommand event、成果物差分の保持・復元を検証する異常系テストの入口である。

## Read this when
- `run_codex_exec` の出力契約違反や Structured Output schema 検証の補正挙動を確認するとき。
- capacity retry、未知の JSONL error、KeyboardInterrupt、retry 上限、backoff の外部挙動を確認するとき。
- Codex call の呼び出し回数、session の継続、call log と subcommand event の対応、補正時の成果物差分を確認するとき。

## Do not read this when
- Codex exec の通常成功経路や基本的な引数生成だけを確認したいとき。
- retry や失敗時ログの実装詳細を変更・調査する場合で、まず `run_codex_exec` 本体やログ出力実装を直接読むべきとき。
- Structured Output の schema 自体の一般的な仕様や検証器の単体挙動だけを確認したいとき。

## hash
- 61cecd4b13db81f7eeaba737680277d058828b75f3d71b9be148330fe81d14ba

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
- Codex TUI 実行経路の代表的な外部挙動を検証するテスト。完全な prompt と CLI 引数、アクセスモード、editor handoff、callback 設定、call log、サブコマンドイベント、失敗時の例外・記録を扱う。

## Read this when
- Codex TUI の呼び出し引数や prompt の引き渡しを変更・確認するとき。
- Codex CLI の検証済みバージョンに応じた callback の有無やアクセス境界を変更・確認するとき。
- TUI call log と codex_call イベントの成功・失敗記録、timestamp 衝突、CLI 不在、KeyboardInterrupt、非 0 終了を変更・確認するとき。

## Do not read this when
- TUI 以外の Codex 実行経路や、prompt 生成そのものの仕様だけを確認するとき。
- call log やサブコマンドイベントの共通実装を直接調査・変更するときは、まずその実装側の対象を読むとき。

## hash
- d87c9676e29b74cff3f84c5030a951f8fa1414fe49e3ecb34a4512511b5bdabb

# `test_doctor_cli.py`

## Summary
- doctor preprocess の CLI と直接呼び出しにおける外部契約を検証する統合テスト。
- Git ignore、.agents、config、refactor state の修復と必要な repair commit を、同一の repository/worktree lifecycle として確認する。
- 共有 doctor lock、linked worktree、reporter の degraded/error 挙動、および既存の staged・unstaged な Git index 状態を保持する修復処理を検証する。

## Read this when
- doctor preprocess の修復対象、処理順序、commit 範囲、または修復後の CLI レポートを確認したいとき
- repository と linked worktree にまたがる doctor lock・runtime file・Git ignore の挙動を確認したいとき
- doctor 実行前から存在する staged change、unstaged hunk、rename、index flag、intent-to-add を保持する契約を確認したいとき
- feedback reporter の利用不能を warning として扱う条件、または中断・予期しない例外を伝播する条件を確認したいとき

## Do not read this when
- doctor preprocess の実装詳細や正本仕様の定義を確認したいときは、doctor の実装または列挙された正本仕様を直接読む
- Git 操作の共通 fixture・CLI 実行ヘルパー・Git コマンドの補助実装を確認したいときは、それぞれの補助対象を直接読む
- doctor 以外のサブコマンドや、個別の config・refactor state・feedback reporter 単体の挙動だけを確認したいときは、対応する対象を直接読む

## hash
- c5e51b505a15134402bc7a42f4fe540ef9af34b43f8cd33a17076d9baff903c3

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

# `test_editor_input_handoff.py`

## Summary
- editor input handoff のテストとして、active repository の target 受理、最後の内容による全面上書き、repository 不一致や symlink 化の拒否、受付済み処理完了までの close 待機を検証する。

## Read this when
- editor input handoff の lifecycle、target の受付条件、上書き先の安全境界、または close と受付済み submission の競合をテスト・レビューするとき。

## Do not read this when
- handoff の正本仕様や実装そのものを確認するときは、対応する oracle の仕様文書または realization implementation を直接読む。editor input handoff と無関係なテストを調べるとき。

## hash
- 390adebd6a73c8a0bcea3fa5b6b30345ef50c10a5fb73bf5ad38c202f6881d6b

# `test_editor_input_handoff_mcp.py`

## Summary
- editor input handoff の agent-facing MCP インターフェースを検証するテスト。公開ツールが overwrite のみで正本 schema を使用することと、未検証入力を内容を漏らさず拒否することを確認する。

## Read this when
- editor input handoff の MCP ツール公開範囲、canonical schema の利用、入力検証・拒否時の情報非開示を確認または変更するとき。

## Do not read this when
- editor input handoff の正本仕様や schema 自体を確認するときは、それぞれの oracle ファイルを直接読む。MCP 実装の内部動作を変更するときは実装ファイルを直接読む。

## hash
- bc903262833d02528fc9b873c65d157ebdcc5a33ca6a648e0ca6acdf770761e6

# `test_feedback.py`

## Summary
- 対象は feedback の pending observation から report cut、正規化・verification、active generation の atomic publication、cleanup までを同一 repository fixture で検証する統合テストである。
- agent-facing reporter の canonical submission tool、collector の context・rate・永続保存・redaction、machine observation の idempotency と recurrence threshold を検証する。
- 正常・incomplete・interrupted・corrupted state を含む report 再開と、current pointer・manifest・artifact の整合性検証を扱う。

## Read this when
- feedback observation の raw store、active state、report cut、verification、publication、cleanup の外部挙動を変更または検証するとき。
- feedback report の agent builder、preflight、checkpoint、再開処理、診断 report、atomic publication のテスト範囲を確認するとき。
- reporter/collector protocol、path boundary、secret masking、machine aggregate の threshold や expiration を検証する必要があるとき。

## Do not read this when
- feedback の正本仕様や CLI 実装の責務を確認することが目的で、テストケースの期待挙動を読む必要がないとき。
- feedback report の内部実装を直接変更する作業で、まず report コマンド実装や state/store の実装・仕様を読むべきとき。
- feedback と無関係な subcommand、一般的な CLI fixture、または単純な JSON schema のみを扱うとき。

## hash
- 13e8ddba5637a3f71596004554d166caeba0fc933100df2359b8e630a2a1a037

# `test_file_inventory.py`

## Summary
- oracle/realization file の full-tree 列挙契約と refactor state 同期を検証するテスト。Git ignore、除外境界、nested repository、linked worktree、特殊ファイル、symlink、非 UTF-8 名、ignore source、単一 path 分類、候補数増加時の Git 処理量を扱う。列挙実装や state 同期の挙動を変更・調査するときのテスト入口である。

## Read this when
- oracle/realization file の列挙結果、除外規則、Git ignore の適用範囲、nested repository や worktree の扱いを確認するとき
- refactor state の初期化・同期・SHA 更新が列挙結果と一致することを検証するとき
- symlink、FIFO、socket・device 相当 mode など非通常 file の拒否仕様を変更または調査するとき
- 列挙処理の Git 呼び出し回数や候補数増加時の処理量を確認するとき

## Do not read this when
- 列挙や refactor state の挙動に関係しない機能の実装・テストを扱うとき
- 正本仕様そのものの定義を確認する必要があり、テスト実装ではなく oracle/doc/app_spec 以下の仕様を直接読むべきとき
- 列挙実装の具体的なアルゴリズムや CLI の責務を確認する必要があり、commons/runtime_git.py など実装対象を直接読むべきとき

## hash
- c496a10d66979d6149cd01d3a0ba72ac2031f7a275ff39f554d26b4ec7615331

# `test_indexing_cli.py`

## Summary
- `cmoc indexing` の CLI 実行と preflight の外部挙動を検証するテスト。
- doctor による初期化、worktree の選択、INDEX.md の生成・fresh 判定、Codex 呼び出し、INDEX.md 限定 commit、およびエラー時の扱いを確認する。

## Read this when
- `cmoc indexing` の開始条件、doctor 実行、clean または dirty repository の扱いを確認するとき。
- linked worktree や apply worktree を対象とした indexing、worktree 固有の Codex 設定、非 INDEX 差分の保持を確認するとき。
- INDEX.md の更新結果、既存 hash による Codex 呼び出し省略、INDEX.md だけを commit する条件、primary report の内容を確認するとき。

## Do not read this when
- indexing の具体的な実装手順や仕様の正本を確認する場合は、対応する app spec を直接読む。
- INDEX.md エントリー生成の出力形式だけを確認する場合は、対応する Structured Output schema を直接読む。
- doctor 単体、Git 操作単体、または indexing 以外の CLI の挙動を調べる場合は、このテストを入口にしない。

## hash
- cff0693797d780c35c708bcf213a6acce1de38fc89ffc5af9faf329fc0552ebd

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
- Codex 呼び出し直前の indexing preflight を検証するテスト群。exec・TUI 経路、linked worktree の選択、repository lock 待機、パラメータによる無効化、file access violation 後の recovery indexing 禁止を扱う。

## Read this when
- Codex 呼び出し前の indexing 実行条件や順序を変更・確認するとき。
- preflight の対象 root、linked worktree、repository lock、recovery 動作のテスト要件を確認するとき。

## Do not read this when
- indexing 自体の更新処理や INDEX.md 生成規則を変更・確認するときは、indexing 実装または仕様を直接読む。
- Codex CLI の一般的な実行処理や TUI 実装だけを調べるとき。

## hash
- 908327bd8f7e3c20172beda2f589a6bfcbafe2943c13c8846265f8e4d280f13f

# `test_oracle_edit_cli.py`

## Summary
- `cmoc oracle edit` の main-worktree exec 制御を、成功時と main/reduction 失敗時の共通経路として検証する制御テスト。editor 入力、Git 差分、session state、agent call、通知、レポートの境界をまとめて確認する。
- oracle edit の起動前提違反と、初期 prompt skeleton 構築失敗時の後始末を検証する補助テスト。

## Read this when
- `cmoc oracle edit` の実行順序、main と reduction の agent call 条件、失敗時の差分保持や通知・レポートを確認したいとき。
- oracle edit の起動前提検査、editor work file の予約・cleanup、session branch や main worktree の制約を調べるとき。

## Do not read this when
- oracle edit の実装詳細や正本仕様そのものを確認したいとき。実装は `launch_exec.py`、仕様は `oracle_edit.md` を直接読む。
- 一般的な CLI テスト基盤、Git fixture、Codex fixture の共通仕様だけを調べるとき。各 `_support` モジュールを直接読む。

## hash
- 13d3d585e73b34cd24579b50be41916ef660dd062d51615c26c5c6c194cd452e

# `test_oracle_investigation_cli.py`

## Summary
- 対象は `oracle investigation` CLI の起動経路を、doctor 前処理、prompt editor 入力、launch parameter 構築、indexing preflight、Codex TUI 起動まで含めて検証するテストです。
- session 前提なしの起動順序、生成される prompt skeleton／最終 prompt、AgentCallParameter のアクセスモード・実行設定、editor 入力ファイルの後処理を確認する実行時挙動の検証入口です。
- 同階層の builder 公開面も確認し、investigation 用 realization adapter が所定の builder だけを公開する契約を検証します。

## Read this when
- `oracle investigation` サブコマンドが main worktree で session なしに起動できるか、また起動前後の処理順序や TUI 呼び出し条件を確認・変更するとき。
- oracle investigation の prompt editor handoff、prompt の objective／policy 組み立て、生成パラメータ、indexing preflight の統合挙動を検証するとき。
- investigation launch TUI builder の `__all__` と公開シンボルを含む realization adapter の公開 API 契約を確認するとき。

## Do not read this when
- oracle investigation の一般的な仕様や indexing の文書内容だけを調べる場合は、まず対応する oracle 文書を直接読んでください。
- investigation 以外の oracle サブコマンド、共通 CLI、または個別 builder の単体ロジックだけを確認する場合は、それぞれの対象テストや実装へ直接進んでください。
- prompt editor や Codex TUI の共通機能そのものを変更・調査する場合は、このテストではなく共通機能を扱う対象を読んでください。

## hash
- bee0bbcec80073a70f18dfae77e7e14d7a2b9430ac92da7c2a61f6d471e56fb6

# `test_oracle_review_loop.py`

## Summary
- oracle review の finding loop 回帰テスト。oracle ごとの finding 列挙、関連 finding の引き継ぎ、merge、challenger/advocate による理由検証、judge の判定を fake Codex の Structured Output 呼び出し列で検証する。
- review 用 linked worktree と main repository の分離、agent call の prompt/context、finding ID の postcondition、merge 補正失敗の伝播、中断時の完了済み部分結果を確認する。
- oracle review loop の実装や仕様変更時に、agent call 順序、入力引き継ぎ、merge 契約、理由検証、割り込み復旧を確認する回帰テストの入口である。

## Read this when
- oracle review の finding loop、finding の列挙・merge・理由検証・judge を変更または検証するとき
- review worktree と main repository の隔離や Structured Output による agent call context を確認するとき
- merge の postcondition、finding ID、部分結果保持、KeyboardInterrupt 後の復旧挙動を確認するとき

## Do not read this when
- oracle review loop の実装詳細を調査・変更する場合は、まず対応する sub_commands.oracle の実装を読むとき
- oracle review の正本仕様や agent call 共通契約だけを確認する場合は、oracle/doc/app_spec 配下の仕様を直接読むとき
- finding loop 以外のテストや、一般的な pytest・git worktree の使い方だけを扱うとき

## hash
- 45e83a700f6a0b5c565962a1b9b01374cbe65251240d0aa517949f17da83928f

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
- `oracle review` の report 契約を回帰検証するテスト群。Structured Output からの finding 構築、accepted/rejected finding の severity 別表示、oracle path の件数集計、YAML frontmatter と Markdown table の安全なエスケープを扱う。
- CLI の scope option、正常終了・中断・処理失敗時の report 保存と端末出力を検証する。report path の timestamp 衝突回避と描画失敗時の予約 file cleanup も対象とする。oracle review report の表示仕様と error summary をまとめて確認する入口である。

## Read this when
- `oracle review` の report 出力や CLI 表示の回帰を確認するとき
- finding の accepted/rejected 分類、fatal/minor 件数、oracle file 集計、path 表示を変更または調査するとき
- oracle review の中断・失敗時に、完了済み対象だけを report に含める挙動を確認するとき
- report の予約 path、timestamp 衝突、frontmatter または Markdown のエスケープ処理を確認するとき

## Do not read this when
- oracle review の本体ロジックや report renderer の実装を直接確認する場合は、対応する `sub_commands/oracle` の実装 file を読む
- oracle review 以外のサブコマンドの CLI 挙動や、Structured Output schema 自体の定義だけを確認する場合は、この回帰テストを読む必要はない

## hash
- 555325b6be4c6b5c43858e90fa11e13e20d372ce5cbfac78924d9353a4ccd125

# `test_oracle_review_targets.py`

## Summary
- oracle review の finding path 解決と、review 対象 oracle file の列挙・scope 別集計を検証するテスト。full/session scope の対象境界、追跡済み ignored・binary・改行を含む Git path の保持、AGENTS.md・INDEX.md・symlink の扱いを確認する入口。

## Read this when
- oracle review の finding path 解決または review 対象列挙を確認・変更するとき
- full/session scope の対象範囲、review fork commit 基準、対象件数レポートを確認するとき
- ignored file、binary file、改行を含む Git path、symlink、AGENTS.md・INDEX.md の除外挙動を検証するとき

## Do not read this when
- oracle review の対象列挙や finding path 以外の機能を直接確認すれば目的を満たせるとき
- oracle review の実装詳細ではなく、一般的な oracle 文書や別サブコマンドの挙動を調べるとき

## hash
- 53139d1e83946e461ab8d127a16dc1d59b6b919172a606dcbac3dcfcaff77a85

# `test_oracle_review_worktree.py`

## Summary
- oracle review の隔離 run lifecycle と INDEX.md 統合を検証する回帰テスト群。
- linked worktree・session branch・snapshot commit を起点とした review worktree の作成、Codex 実行コンテキスト、run target 衝突、部分作成や中断時の cleanup を扱う。
- review worktree で許可される INDEX.md 差分、対象外ファイルや directory の拒否、rename・Git quoted path、merge conflict の解決と復旧、merge 後の INDEX 統合を検証する。
- oracle review の preflight、active editing run との共存、通知、error/interrupted report、cleanup failure の扱いを確認する。oracle review の worktree 分離または INDEX 差分統合の挙動を変更・調査する際の回帰テスト入口である。

## Read this when
- oracle review の linked worktree、session branch、snapshot commit、run branch、run worktree の lifecycle を変更または調査するとき
- oracle review が生成・統合できる INDEX.md の差分範囲や、対象外ファイル・対象外 directory の拒否を確認するとき
- review branch の merge、INDEX conflict 解決、merge abort、割り込み後の worktree 復旧を確認するとき
- oracle review の preflight context、active editing run、通知、report、cleanup failure のテスト根拠を確認するとき

## Do not read this when
- oracle review の所見列挙・challenger・advocate・judge の判定ロジックだけを変更または調査するとき
- INDEX.md の一般的な生成規則や routing 方針だけを確認するときは、まず indexing の正本仕様または indexing 実装を読むとき
- session fork や通常の editing run の lifecycle だけを扱い、oracle review の隔離 run・merge・INDEX 統合に関係しないとき

## hash
- 50c00dcf7cdfb1e262b834d66a916ca44fb53cc9531ce8c6d1db40b5d50747dc

# `test_packaged_import.py`

## Summary
- packaged layout にコピーした source tree から、canonical builder と関連公開モジュールを隔離環境で import できることを検証するテスト
- oracle review・quota probe・oracle edit の builder が正本の schema、prompt、editor 入力を参照して期待する parameter を生成することを検証するテスト
- ACP basic と cmoc config の realization 側公開面が、正本定義の再公開または設定定義だけに限定されることを検証するテスト

## Read this when
- packaged layout、Python の import 境界、canonical builder の schema・prompt 参照を確認するとき
- oracle edit の prompt editor 入出力 handoff、公開関数、file access mode、preflight の挙動を確認するとき
- ACP basic または cmoc config の再公開 API と module namespace の限定性を検証するとき

## Do not read this when
- 個別の oracle builder や prompt editor の実装詳細を変更・調査する場合は、対応する正本実装を直接読むとき
- packaged layout の import、公開 API の再公開・限定性、または prompt editor 入力境界に関係しないテストを扱うとき

## hash
- db82e692ebd82f7a16e2dacf4367c0fa5585ef0806eab3952e090f5dc0396d8b

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
- 全末端サブコマンドを、独立 process・実 Codex CLI・実推論による利用者向け本番経路で検証する受け入れ試験。
- 非対話 command の終了 code、report、状態遷移、Git、agent call log と prompt を確認し、新しい末端 command の試験漏れも検出する。
- TUI command は実 PTY 上で実 Codex 応答の完了、TUI call log、終了操作、リポジトリ非変更を確認する。

## Read this when
- 利用者向け CLI の全末端サブコマンドが本番経路で正常完了することを検証するとき。
- 独立 subprocess、実 Codex CLI、隔離 Codex home、実 provider、agent call の設定・log を確認するとき。
- oracle edit、realization の fork、run/session の join・abandon、indexing、feedback、oracle review の受け入れ経路をまとめて追うとき。
- TUI の PTY 応答、端末 capability query、信頼確認、完了済み response、終了後の状態を検証するとき。

## Do not read this when
- 個別サブコマンドの内部実装や仕様だけを確認したいときは、対応する command 実装・仕様を直接読む。
- LLM の回答内容や品質を評価する必要があるとき。この試験は応答後の cmoc 制御と外部観測結果を対象とする。
- Codex CLI を使わない単体試験、通常の fixture test、または全末端の利用者向け本番経路を対象にしない試験を読むとき。

## hash
- a2a385d82f4d6e81b80cd2495cd7348f10e0ad24545bf97f2d6aeecbbe108501

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
- prompt builder の各 policy part と complete prompt の組み立て・Markdown rendering・placeholder 展開を検証する回帰テスト
- SDHeader/SDPolicy の構造、policy のカテゴリ順序、選択した policy の注入順序と重複、file access mode ごとの境界を確認する
- complete prompt の objective・feedback instruction・root token・動的 section の保持、および各 policy の主要要求を検証する

## Read this when
- prompt part または complete prompt の構造・順序・rendering・placeholder 展開を変更する場合
- prompt builder policy の注入、file access mode、feedback instruction、root path 定義の挙動を確認する場合
- prompt builder の回帰テストや policy builder の出力契約を調査する場合

## Do not read this when
- prompt builder の実装詳細や正本仕様そのものを確認する場合は、対応する oracle/src または oracle/doc を直接読む
- prompt の routing 文書生成規則だけを調べる場合は、index entry policy の正本を直接読む
- prompt builder と無関係な CLI 機能、一般的なテスト基盤、他の rendering 実装を調べる場合

## hash
- 5d373e9c01ab3989fcfd3e62d8a7b77874c372f64086586ad6f60cc95e609da0

# `test_runtime_cli.py`

## Summary
- CLI lifecycle の error、log、preflight、completion 境界を、共通 runner・work root・subcommand event・終了処理の外部契約として検証するテスト。
- duration の表示・拒否、SubcommandLogger の衝突回避と並列記録、成功・失敗・非0終了・例外・KeyboardInterrupt の terminal result とログを扱う。
- doctor preprocess、pre-log check、work root 制約、shell completion probe の副作用抑制、TUI の通知境界を検証する。関連する CLI runtime の挙動を確認するための統合テスト入口。

## Read this when
- CLI の成功・失敗出力、終了コード、stderr/stdout、例外 traceback の扱いを変更・検証するとき
- サブコマンドログの event、logger の並列性・timestamp 衝突、pre-log check または終了処理を変更・検証するとき
- doctor preprocess、work root 判定、completion probe の初期化抑制を変更・検証するとき
- TUI と非対話 CLI の terminal notification、Codex subprocess 起動前後の KeyboardInterrupt を変更・検証するとき
- 共通 runtime の duration 表示または error rendering を変更・検証するとき

## Do not read this when
- CLI の個別コマンド実装や正本仕様だけを確認する場合
- completion の仕様・実装だけを確認する場合は cli_auto_completion の仕様または completion 実装を直接読むとき
- doctor preprocess の仕様・実装だけを確認する場合は doctor_preprocess の仕様または該当実装を直接読むとき
- ログ形式や logger API だけを確認する場合は console_and_file_log の仕様または SubcommandLogger 実装を直接読むとき

## hash
- 8ab88f84ce1238ff2b227e67b21bde85550a9d48c4e370f13991fa8db0de988d

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
- Codex argv の model、sandbox、provider 上書き契約を検証するテスト。file access mode の sandbox 変換、approval・通知・MCP・環境変数設定、hook の組み合わせ、Codex CLI バージョン判定、provider TOML エンコード、未定義設定の拒否、schema 保存と JSON 出力処理を扱う。

## Read this when
- Codex 起動引数や subprocess 環境の構築を変更・検証するとき
- sandbox、model provider、通知 callback、SessionStart hook、feedback/editor MCP の連携を確認するとき
- schema のハッシュ保存や Codex 出力 JSON の読み取り挙動を変更・検証するとき

## Do not read this when
- Codex argv・runtime_codex_profile の挙動に関係しない機能を扱うとき
- 実装詳細ではなく、Codex 実行契約そのものを確認する必要があり、oracle の仕様文書を直接読むべきとき
- provider 設定のデータモデルや全体設定の正本を確認する必要があり、設定定義の対象ファイルを直接読むべきとき

## hash
- 5a6668fbe2dd6b931b0a99b89c26c9a1972867f440101dc420f85b37fb4bc3d9

# `test_runtime_config.py`

## Summary
- CmocConfig の既定値と、codex / oracle_review の直接設定を検証する回帰テスト。
- 設定の JSON 化・ファイル保存・読み込みによる round-trip と、既存メンバー順序・provider-local 値の保持を検証する。
- 不正な型、値、深さ、JSON、パス、symlink、named pipe、および廃止済み設定を設定エラーまたは永続化境界で拒否・除外する。

## Read this when
- CmocConfig の既定値や agent call ごとの model provider・model・reasoning effort を変更・調査するとき。
- 設定の config.json への変換、保存、読み込み、round-trip、メンバー順序、任意の provider settings の保持を確認するとき。
- 設定入力の型検証、JSON/TOML 共通値の受理条件、深い構造、壊れた JSON、異常な設定パス、エラー表示、legacy 設定の除外を確認するとき。

## Do not read this when
- 設定の具体的な既定値や入力拒否、永続化境界の回帰条件を確認する必要がないとき。
- CmocConfig の実装や config の正本仕様そのものを直接確認することが目的で、テストによる外部挙動の確認が不要なとき。

## hash
- f0878a4cdc6bc9e813bb663e7a74836c43ab303519d59c4d879c2ca68eca5f81

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
- Git ignore の更新・判定を安全に行う `cmoc_runtime` の挙動を検証するテスト。`.gitignore` と `info/exclude` への cmoc 用パターン追加、既存パターンや例外の保持、tracked/untracked 状態の分類を扱う。
- 通常ファイル以外や symlink の ignore ファイルを変更・参照しないこと、global excludes や nested `.gitignore` の異常をエラーとして扱うこと、`git check-ignore` の判定失敗を未 ignore と誤分類しないことを確認する。Git ignore 機能の安全性に関するテスト群への入口となる。

## Read this when
- Git ignore の更新または判定ロジックを変更・レビューするとき
- `.gitignore`、`info/exclude`、global excludes、nested `.gitignore`、symlink、特殊ファイルへの安全な対応を確認するとき
- tracked と untracked の ignore 判定、literal path 名の扱い、`git check-ignore` 失敗時のエラー処理を確認するとき

## Do not read this when
- Git ignore の実装詳細や仕様上の根拠を確認する場合は、対応する `cmoc_runtime` 実装または列挙・doctor・editing_run の仕様を直接読むとき
- Git ignore の安全性・判定挙動と無関係なテストや機能を調べるとき

## hash
- 020d8416988d100aa9497629e0f931ea85a36dd840ff3058e784e92c1af8914a

# `test_runtime_refactor.py`

## Summary
- `test_runtime_refactor.py` は、realization refactor の永続 state について、対象ファイル集合の同期、調査履歴の保持と変更時の再調査化、state schema の検証、安全な読み書き、調査対象の選択規則を検証するテスト入口です。oracle と realization のファイル分類、パス正規化、symlink・特殊ファイル・Gitlink・path escape の拒否、timestamp と調査結果の形式も扱います。

## Read this when
- realization refactor の state 同期・永続化・schema 検証を変更または調査するとき
- oracle／realization 対象ファイルの分類や、symlink・特殊ファイル・Gitlink・親ディレクトリ脱出に関する挙動を検証するとき
- 未調査対象および古い調査時刻を基準とする refactor target 選択規則を確認するとき

## Do not read this when
- refactor state や対象選択ではなく、別の runtime 機能だけを変更・調査するとき
- テスト実装の詳細ではなく、正本仕様そのものの意味や変更を確認するときは、列挙規則・timestamp・realization refactor の oracle 文書を直接読むとき

## hash
- 5d09ccedae23bb9098152a688a5ea68dae27e322a44c7fffa364fbbb7d57eb58

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
- session fork、join、abandon における branch と session state のライフサイクルを、CLI の外部挙動として横断的に検証する回帰テスト。
- fork の session branch・state 作成、session-id 衝突、保存失敗時の rollback、linked worktree を扱う。
- abandon の home branch 復帰、state の abandoned 遷移、cleanup、dirty worktree・欠落 branch・競合時の拒否と復元を扱う。
- join の通常 merge、conflict 解消、対象外差分の拒否、削除解消、linked worktree、branch 削除、失敗報告を扱う。
- doctor preprocess、repository-local feedback state、Codex conflict-resolution 呼び出し境界、特殊文字を含む conflict path も検証する。

## Read this when
- session fork・join・abandon の外部挙動や state 遷移をまとめて確認するとき
- session branch、home branch、linked worktree、state file の整合性や cleanup を調査するとき
- dirty worktree、missing branch、ID 衝突、cleanup failure、conflict resolution の回帰を確認するとき
- session join が Codex に conflict 解消を委譲する条件、変更範囲の検証、報告出力を確認するとき

## Do not read this when
- session の branch/state ライフサイクルに関係しないサブコマンドや一般的な Git 挙動だけを調べるとき
- 個別の fork・join・abandon 実装の詳細や正本仕様を直接確認すべきとき
- テスト実行手順、Python 環境、一般的なテスト規約だけを確認したいとき

## hash
- dc3d2a84d834edf835c19fda53d91e210f9db816fa347e5aada9ab4f324eff05

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
- Windows toast の terminal 通知内容と transport 境界を検証するテスト。短い表示項目、JSON stdin による安全な PowerShell 呼び出し、通知失敗の非伝播を扱う。
- Codex TUI callback の session 記録、root turn の一度だけの通知、子 session の除外、invocation 終了時の状態破棄、standalone hook/callback の動作を検証する。

## Read this when
- Windows toast 通知の表示内容や PowerShell transport の入力境界を変更・確認するとき。
- Codex TUI の SessionStart hook、agent-turn-complete callback、root/child session 判定、通知重複防止を変更・確認するとき。
- callback 用一時状態のライフサイクルや standalone 実行時の stdin・argv・終了結果を変更・確認するとき。

## Do not read this when
- Windows toast や Codex callback の実装挙動を調べる必要がなく、別機能のテストを確認するとき。
- 通知本文の正本要件や設計意図そのものを確認するときは、この検証テストではなく参照仕様を直接読むとき。

## hash
- 9d0e7cc65dd50d20dd759f04074add3dd9a5980c2262bfc92cc69308760ed7f3
