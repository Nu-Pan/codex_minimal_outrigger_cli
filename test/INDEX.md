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
- editing run workload の canonical builder adapter を検証し、apply/refactor builder の再公開経路、prompt 埋め込み、実行設定、canonical Structured Output schema、raw diff の境界保持を確認するテスト。

## Read this when
- editing run 用の apply または refactor builder の prompt 構成・実行設定・schema 選択・互換 import 経路を変更または検証するとき。
- raw diff にコードフェンスや prompt 境界風のマーカーが含まれる場合の保持を確認するとき。

## Do not read this when
- builder 本体の実装や canonical oracle 側の仕様を直接変更・確認する作業で、まず対象の実装ファイルや oracle file を読むべきとき。
- editing run builder と無関係なテスト、または Structured Output schema の定義自体を調査するとき。

## hash
- 439e6930e836e54f978a4c3ca19223bddb83b1e7f7b6960d363ff265a2107eab

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
- TUI 起動 builder の固定パラメータ、実行ポリシー、prompt 構成、互換 module の公開面を検証するテスト。

## Read this when
- TUI 起動 builder の固定設定や prompt の必須・除外ポリシーを確認・変更するとき。
- TUI 起動用互換 module の公開 API が builder のみに限定されることを検証するとき。

## Do not read this when
- TUI 起動 builder の実装を直接確認すれば足り、テストの期待値や回帰条件を確認する必要がないとき。
- TUI 以外の builder や一般的な prompt 生成のテストを探しているとき。

## hash
- 0409d5c312729f31c38ef045cf2dc26358ee0c6676fdfa24559c135a1104ca61

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
- 公開 CLI の末端 command 集合を正本仕様の列挙と照合し、Typer/Click 互換性を含む help 描画と feedback report の公開引数制約を検証するテスト。
- CLI の command tree 構成や公開 leaf の追加・削除、help 描画互換性、feedback report の引数設計を確認する入口。

## Read this when
- 公開 CLI の command 階層または leaf 集合を変更したとき。
- Typer/Click の互換性に関わる help 描画を変更したとき。
- feedback report の公開引数や option の有無を変更・確認するとき。
- oracle 変更後に公開 CLI 集合が正本仕様と一致するか検証するとき。

## Do not read this when
- 個別 command の実行処理や業務ロジックを変更・調査するとき。
- 各 command の詳細な仕様や oracle 文書の内容を確認するとき。
- CLI 全体の leaf 集合、help 互換性、feedback report の公開引数制約に関係しないテストを扱うとき。

## hash
- ea3eaf19b27e9c445d700a05e03705f0456394082844f77773c218031b164fa5

# `test_cli_tui.py`

## Summary
- TUI 起動直前の CLI 前処理から Codex TUI 起動までの外部挙動を検証するテスト。
- prompt editor による編集済み入力、生成 prompt、doctor 前処理、indexing preflight の順序を検証する。
- linked worktree でも main worktree に editor 記録と agent call context を配置し、リポジトリと worktree の `.cmoc` ignore を維持する挙動を検証する。

## Read this when
- `tui` サブコマンドの起動前処理や Codex TUI 起動パラメータを変更・調査するとき
- TUI の prompt editor 入力、編集記録、生成 prompt の外部挙動を確認するとき
- linked worktree におけるログ・agent call context・`.gitignore` の配置や保持を変更・調査するとき

## Do not read this when
- TUI 以外のサブコマンドの挙動を調査するとき
- TUI の実装や正本仕様を直接確認することが目的で、テストケースの期待挙動を確認する必要がないとき
- prompt editor、doctor 前処理、worktree の記録配置に関係しない共通 CLI 機能だけを調査するとき

## hash
- 047eb5b60faf76b3c49089794bf0117a65219073f9d1d5b56a2364131a29f75e

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
- Codex quota 超過後の probe/resume/retry 状態機械を検証するテスト群。
- quota availability probe の共有、session ID に基づく resume、session ID 欠落時の prompt 再実行を扱う。
- Codex 呼び出し列と call log・subcommand log、CODEX_HOME・cwd、stdout JSONL、待機状態の外部挙動を一体で確認する。

## Read this when
- quota 超過からの復帰処理や quota polling の上限・待機間隔を確認するとき
- 代表 probe の成功・失敗・capacity retry・KeyboardInterrupt の伝播を確認するとき
- 並行 Codex 呼び出しで probe が共有され、復帰結果が各呼び出しへ反映されることを確認するとき
- session ID、保存済み stdout JSONL、resume／再実行、Codex の cwd と CODEX_HOME の解決を追跡するとき

## Do not read this when
- 通常の Codex exec 成功・失敗や quota と無関係な subprocess 挙動だけを扱うとき
- quota probe の prompt 生成内容だけを確認したいときは、probe parameter builder の正本を直接読むとき
- Codex 呼び出しのログ形式全般だけを確認したいときは、ログ実装または対応する仕様を直接読むとき

## hash
- b75871407adb2e49438f1ff544b45e70056621f5bee42af2b5780abc2d64ad5f

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
- feedback の pending observation を raw store から読み込み、agent issue の同一性判断と verification を経て active state へ集約するテスト群。
- report cut の checkpoint、Codex call の再利用、中断・失敗時の再開、atomic publication、current pointer、generation hash、cleanup の整合性を検証する。
- reporter/collector の MCP 境界、context・rate 制限、path 境界、secret masking、JSON・artifact 破損時の安全な停止を検証する。

## Read this when
- feedback report の raw observation 処理、候補の normalization・verification、machine aggregate の threshold 処理を確認または変更するとき
- report cut の durable checkpoint、ユーザー中断や publication 失敗からの再開、active generation の publication と cleanup を確認するとき
- feedback reporter/collector の入力検証、MCP protocol、repository path、秘密情報マスキング、破損 artifact の扱いをテストするとき

## Do not read this when
- feedback の正本仕様や runtime 実装の責務を直接確認する場合は、対応する oracle 文書または実装対象へ進むとき
- feedback report 以外のテスト、または一般的な CLI・fixture の挙動だけを確認するとき

## hash
- 6c970e0bf2c9140f49f076b25b5b29e68d0a5e807d454da0f4cb31fe4ab29fe1

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
- `cmoc oracle edit` の main-worktree 実行制御を、成功・本命 exec 失敗・仕様削減 exec 失敗・builder 失敗・起動前提違反の経路で検証する制御テスト。
- 2 回の agent call、editor 入力、Git 差分、session state、実行順序、失敗時の残存変更、通知および診断レポートの境界をまとめて確認する。

## Read this when
- `cmoc oracle edit` の exec 呼び出し順、main/reduction の責務分担、editor 入力のライフサイクルを変更または調査するとき。
- oracle edit 実行時の既存 Git 差分・session state 保持、失敗時の変更残存、通知・レポート出力を確認するとき。
- oracle edit の main worktree／session branch／active session 前提や builder 失敗時の挙動を変更または検証するとき。

## Do not read this when
- oracle edit の prompt builder 自体の詳細な文面や parameter 生成だけを直接調査する場合。
- 一般的な Git、session state、terminal report の共通実装を変更または調査する場合は、それぞれの実装・仕様・専用テストを直接読む。
- oracle edit と無関係な CLI サブコマンドや agent call の挙動を扱う場合。

## hash
- bc7d810a7dd9c492c9f761cf6aeec699f1d4cfb4a632e24e0d46ec987d48f0d1

# `test_oracle_investigation_cli.py`

## Summary
- `cmoc oracle investigation` の CLI が、doctor preprocess、prompt editor input、TUI 起動パラメータ構築、Codex CLI TUI 起動までの実行経路を検証するテスト。
- session 前提なしでの起動、indexing preflight、editor input handoff、PURE_ORACLE_READ など、oracle investigation 固有の起動契約を確認する。
- investigation 用 realization adapter が `build_oracle_investigation_launch_tui_parameter` のみを公開することを検証する。

## Read this when
- `cmoc oracle investigation` の起動前提、処理順序、editor input の lifecycle、TUI 起動パラメータ、oracle-only の読み取り境界を確認するとき。
- oracle investigation の CLI 起動契約または対応する launch TUI builder の公開面を変更・検証するとき。

## Do not read this when
- oracle investigation の意味上の仕様を確認したい場合は、対応する oracle sub-command 仕様を直接読む。
- TUI 起動パラメータの構築実装を確認したい場合は、investigation の launch TUI builder を直接読む。
- 他の oracle sub-command の CLI 起動条件や builder 公開面だけを確認する場合。

## hash
- dc212ae0069441a7d7b8fbac19dbf16bed8aeef44f9acde6d6c24df107b4bca5

# `test_packaged_import.py`

## Summary
- packaged layout へソースツリーをコピーし、隔離した Python 実行環境で import 境界と公開 API を検証するテスト。
- quota probe、oracle edit、prompt editor 入力、ACP basic、cmoc config の正本参照・再公開・公開面を確認する下位テストへの入口。

## Read this when
- パッケージ配置後の import が正本実装を参照することを確認したいとき。
- quota probe や oracle edit の prompt 生成、prompt editor の入力引き渡し、ACP basic または cmoc config の公開境界を検証・変更するとき。
- 外部 site-packages や実行者の設定に依存しない packaged layout テストの構成を確認するとき。

## Do not read this when
- 個別の quota probe、oracle edit、prompt editor、ACP basic、cmoc config の実装仕様だけを確認する場合。
- packaged layout 以外の一般的なテスト実行方法や、各正本モジュールの詳細実装を直接確認する場合。

## hash
- 2eac7131a1c17e799f6e2573ca32d52363dc77aabfe7bd75a6324ccc07800424

# `test_primary_report.py`

## Summary
- 非対話サブコマンドの primary report 完了契約を検証するテスト。処理開始前のエラー、中断、refactor 中断、report 未保存時の内部失敗について、保存先・front matter・診断内容・終了状態・ログ記録を確認する。
- 各サブコマンド固有の report 項目と、feedback report の publication 状態や中断時の checkpoint を検証するテスト群への入口。

## Read this when
- 非対話サブコマンドのエラー・中断時に primary report がどう確定されるかを調査するとき。
- report の保存先、必須メタデータ、terminal classification、completion reason、feedback invocation summary、保存失敗時の内部失敗を変更・検証するとき。
- runtime CLI の完了処理やサブコマンド固有 report 契約に対するテストカバレッジを確認するとき。

## Do not read this when
- primary report の生成仕様そのもの、エラー文面、サブコマンドの通常処理仕様を確認したいだけで、完了契約のテスト実装を読む必要がないとき。
- 特定サブコマンドの業務ロジックや Git 操作だけを調査するときは、対象サブコマンドの実装・仕様を直接読む。
- テスト実行方法や共通 fixture の詳細だけを確認したいときは、テスト実行規則または共通テスト支援ファイルを直接読む。

## hash
- 48cc223a404c96eff19a2c4af3d1fa69a3e87ca809314e7904173c9f4e9e8769

# `test_production_cli.py`

## Summary
- 利用者向け entrypoint の全末端サブコマンドを、独立 process と実 Codex CLI で検証する受け入れ試験。
- 実推論後に観測できる終了 code、report、永続 state、Git 状態、Codex call log、および TUI の PTY 応答完了・終了を確認する。

## Read this when
- 本番経路で全末端サブコマンドの代表的な正常完了と、実 Codex 呼び出しの設定・記録を検証するとき
- 非対話 command の session、run、indexing、oracle、feedback 経路や、TUI の実応答後の終了動作を横断的に確認するとき

## Do not read this when
- LLM の回答品質や内容の妥当性を評価するとき
- 特定サブコマンドの内部実装、個別仕様、または単体レベルの制御ロジックだけを確認するとき

## hash
- 45d35e5f2c5b698e4fa8a230de1f18eb00f76ea00b1c2778cb2238b7410a56ec

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
- prompt part の各 policy builder が生成する SDHeader の構造、カテゴリ順序、rendering を検証する回帰テスト。
- complete prompt の policy 注入、objective の順序、placeholder 展開、feedback 指示、file access 境界を検証する。
- prompt builder の出力変更や policy の責務・注入条件を確認するときのテスト入口。

## Read this when
- prompt part または complete prompt の rendering 結果を変更・調査するとき。
- policy flag ごとの注入、共通 feedback 指示、objective セクション、placeholder の統合・展開を確認するとき。
- file access mode、oracle/realization の境界、INDEX entry・routing policy の prompt 表現を検証するとき。

## Do not read this when
- prompt builder の実装責務や正本仕様そのものを確認したいとき。
- 個別 policy の詳細な生成ロジックだけを調査するときは、対応する policy 実装を直接読むとき。
- prompt の動作ではなく、他の機能や一般的なテスト実行手順だけを確認するとき。

## hash
- fe15d71afb02cc331695a8e84027ac0b5f77efe963ae97c35ebbb9c6ce6e5c45

# `test_runtime_cli.py`

## Summary
- CLI の error、log、preflight、completion 境界を、共通 runner・work root・subcommand event の外部契約として検証するテスト。
- 成功・handled failure・internal failure・非 0 終了・ユーザー中断における terminal result、stderr/stdout、終了コード、診断ログ、通知境界を確認する。
- doctor preprocess、pre-log check、work root 制約、completion probe の副作用抑制、TUI 起動前後の Ctrl+C と通知を検証する。
- duration 表示、サブコマンドログの timestamp 衝突・並列 worker event、error rendering の簡潔性と traceback 非公開も対象とする。

## Read this when
- 共通 CLI runner の error handling、終了処理、terminal notification、subcommand log の挙動を変更または検証するとき。
- doctor preprocess、pre-log check、work root 判定、shell completion の初期化・副作用境界を調査するとき。
- 非対話 CLI と TUI の成功・失敗・Ctrl+C の扱い、または stdout/stderr の出力契約を確認するとき。
- SubcommandLogger、duration/error rendering、並列 event 記録の外部挙動を確認するとき。

## Do not read this when
- CLI lifecycle の共通 runner や error・log・preflight・completion 境界に関係しない機能だけを変更するとき。
- 特定サブコマンドの実装内部ロジックや個別ドメイン処理のテストを直接確認したいとき。
- Codex TUI の subprocess 実装詳細、toast transport の詳細、path model の仕様自体を確認するときは、それぞれの実装または正本仕様を直接読む。

## hash
- 465bf3de5f6ac8f910d7bb1b3db75e58ed062a7a6acc6b2f62293596562e101c

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
- CmocConfig の既定値と agent call ごとの直接設定を検証する回帰テスト。
- config の JSON 変換、ファイル保存・読み込み、round-trip、および定義順の保持を検証する。
- 不正な型・値・構造、深い JSON、危険な config path、旧設定項目の扱いを検証する設定境界の入口。

## Read this when
- CmocConfig の既定値、Codex provider、agent call 設定、または config schema を変更・調査するとき。
- config_from_dict、config_to_dict、load_config、write_config、render_error の設定入出力やエラー契約を変更・調査するとき。
- config.json の永続化、JSON/TOML 共通値、入力拒否、symlink・named pipe などの path 安全性を確認するとき。

## Do not read this when
- 設定以外の runtime 機能や、config schema・設定ファイルの入出力に関係しないテストを扱うとき。
- CmocConfig の実装詳細や正本仕様そのものを確認する必要があり、まず oracle の設定定義・仕様を直接読むべきとき。

## hash
- e4c7205b3a6230b66004fb7d3bcd33997a1b5a7748e12cfbcdaaa215f073dc17

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
