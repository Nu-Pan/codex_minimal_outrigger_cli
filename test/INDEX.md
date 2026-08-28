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
- Codex 実行ラッパーのテストで共有する最小限の result double、テスト用環境、AgentCallParameter、CLI 引数検査、Codex override のスタブを提供する。
- Codex の認証に依存しない一時ホーム環境の準備と、実行引数に含まれる設定の assertion 用解析が必要なテストへの入口となる。

## Read this when
- Codex 実行の runtime wrapper test を追加・変更・確認するとき。
- テスト内で一時的な CODEX_HOME や AgentCallParameter を準備するとき。
- Codex CLI 引数や override 設定を安定した値で検査するとき。

## Do not read this when
- Codex 実行ラッパーの本番実装を変更・調査するとき。
- 共有テストヘルパーを使わない単体テストや、Codex 実行と無関係なテストを扱うとき。

## hash
- 32cc029d96584138284c6907270d00fe89c9adafb5c7ad072cc5e37acc880a97

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
- editing run workload の canonical builder adapter を検証するテスト。apply と refactor の builder が正本 builder、実行設定、Structured Output schema、prompt 内容、raw diff の境界保持を満たすことを確認する。

## Read this when
- editing run 用の apply/refactor builder の互換 import、canonical builder の再公開、prompt の実行条件や policy、schema path、raw diff 埋め込みを確認したいとき。
- raw diff に三連 backtick や prompt 境界風の見出しが含まれる場合の prompt 生成テストの入口を探すとき。

## Do not read this when
- builder の実装詳細そのものを変更・調査する場合は、対応する apply/refactor builder 実装や oracle file を直接読むとき。
- 一般的な builder テストや editing run と無関係な schema・prompt の検証を探しているとき。

## hash
- 1eb7af4825ffd0a790e1bc9e583df22bfe47beb71e71f19ef3437a8a6a6e46c3

# `test_acp_builder_indexing_parameters.py`

## Summary
- indexing index entry builder の parameter、schema、互換公開面を検証するテスト。readonly・preflight 無効の構築条件、semantic 配列の非空制約、対象本文中のコードフェンス保護、互換 module の公開名を扱う。
- index entry 生成処理の実装や schema、仕様を変更した際に、その parameter と公開契約への適合性を確認するテスト入口。

## Read this when
- indexing の index entry builder が適切な file access mode、cwd、preflight 設定で parameter を構築するか確認するとき
- INDEX.md エントリー用 Structured Output schema の semantic 配列制約を確認するとき
- 対象本文に三連 backtick を含む場合の prompt 境界保護や、互換 module の __all__ と公開面を確認するとき

## Do not read this when
- index entry builder の実装詳細を変更・調査する場合は、対応する builder 実装を直接読むとき
- Structured Output schema 自体の定義や indexing のアプリケーション仕様を確認する場合は、対応する正本を直接読むとき
- index entry 以外の indexing 処理、または一般的なテスト実行手順だけを確認したいとき

## hash
- 7252d012886ba9a82f6575d09d704ee2409f113bab4f21764ab65526ff1151b7

# `test_acp_builder_oracle_review_parameters.py`

## Summary
- oracle review ACP builder 群の parameter 契約、oracle read 権限、Structured Output schema、canonical builder 互換性、policy block 注入、および動的 prompt の code fence 境界保護を検証する回帰テスト。

## Read this when
- oracle review の enumerate、judge、merge、validate builder の公開面や parameter 構成を変更・確認するとき。
- review builder が参照する schema と oracle source の一致、動的入力の保持、prompt の section・code fence 境界を調査するとき。

## Do not read this when
- review builder 以外の ACP builder の契約だけを調べるとき。
- 実装や canonical builder 本体の詳細を直接確認する必要があり、対応する oracle・realization file を読むべきとき。

## hash
- 34b032791cf135962d2985ebc02864826c8142300b528d409ee8a10dd3f27546

# `test_acp_builder_session_join_parameters.py`

## Summary
- session join の conflict resolution builder 契約を検証するテスト。公開 export、repo write 権限、実行時設定、プロンプト方針、および競合パス内の三連 backtick を含むコードフェンス保護を扱う。

## Read this when
- session join の conflict resolution builder の公開インターフェースや生成パラメータの契約を確認・変更するとき。
- conflict 対象ファイルのプロンプト埋め込みや、特殊文字を含むパスのコードフェンス処理を確認するとき。

## Do not read this when
- session join の conflict resolution 実装そのものの詳細を変更・調査する場合は、対応する正本実装を直接読む。
- conflict resolution と無関係な session join builder や一般的なテスト実行だけを扱う場合。

## hash
- d4b789f540a073c1e60b8fff1a4076daf87e92d1135c6f8dc405843b9c4e3f78

# `test_acp_builder_tui_parameters.py`

## Summary
- TUI 起動用 builder が、元の prompt に依存せず固定の agent call parameter・ファイルアクセスモード・実行設定・ポリシーを組み立てることを検証するテスト。
- 互換 module の公開 API が現行の TUI 起動 builder 1 件に限定され、正本 builder と同一オブジェクトを公開することを検証する。

## Read this when
- TUI 起動 builder の固定 parameter、prompt に含めるポリシー、prompt 差し込み、実行時の作業ディレクトリや indexing preflight を確認・変更するとき。
- acp.builder.tui.launch_tui の互換 module における公開シンボルや正本 builder との対応を確認するとき。

## Do not read this when
- TUI 起動 builder 自体の正本実装や prompt の仕様を変更する作業で、まず実装・正本仕様を直接確認すべきとき。
- TUI parameter と無関係な builder、一般的な TUI 動作、またはこの互換 module の公開面以外を調べるとき。

## hash
- 0b6bba16850be4ff56b5a943c50d9bc8de5c70bab81ef78f08c25b6d6b579130

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
- `tui` サブコマンド起動直前の前処理から Codex TUI 起動までの外部挙動を検証するテスト。
- エディター入力の反映、既存の Git 差分保持、doctor 前処理、起動パラメータ、ログ保存先、linked worktree 対応、`.cmoc` の ignore を扱う。

## Read this when
- `tui` サブコマンドの前処理順序や Codex TUI 起動条件を変更・確認するとき。
- エディターで編集した prompt が TUI 起動用パラメータへ反映される挙動を変更・確認するとき。
- main worktree と linked worktree における editor input・agent call context・ログの保存先を変更・確認するとき。
- TUI 起動時の `.cmoc/gu/` の ignore、Git の staged・unstaged 差分保持、doctor preprocess の挙動を変更・確認するとき。

## Do not read this when
- TUI 起動直前の CLI 外部挙動ではなく、prompt builder や editor input の単体実装詳細だけを変更・確認するとき。
- TUI 以外のサブコマンドの前処理や起動挙動だけを変更・確認するとき。
- Codex TUI 本体の内部動作や、テスト対象が扱わない低レベルの Git 操作だけを変更・確認するとき。

## hash
- 6a1705ddd08ba59c234e8f9d033ffd35f104eb9ff9540ed6e9736594a9684563

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
- Codex quota 超過後の probe・待機・resume・再実行を含む quota retry 状態機械の外部挙動を、Codex 呼び出し列、session ID、ログ、subcommand 通知、CODEX_HOME/cwd、並行呼び出しまで一体で検証するテスト群。
- quota probe adapter の canonical prompt・固有 call kind・公開 API、および probe の失敗、壊れた JSONL、poll 上限、KeyboardInterrupt、待機状態の解除を検証する回帰テストの入口。

## Read this when
- Codex exec の quota 待機・復帰・retry、session ID による resume、session ID 欠落時の再実行を調査または変更するとき。
- 代表 quota probe の共有、probe の capacity retry、probe 失敗の並行呼び出しへの伝播、quota polling 状態のライフサイクルを確認するとき。
- quota retry に関する call log、subcommand log、stdout JSONL、prompt、output、CODEX_HOME、Codex cwd の観測結果を確認するとき。
- quota probe の正本 prompt との一致、adapter の公開範囲、READONLY 実行条件を検証するとき。

## Do not read this when
- 通常の Codex exec 成功経路や quota と無関係な subprocess 実行を確認するだけのとき。
- quota probe builder の正本仕様や一般的な Codex exec 契約そのものを変更・確認する場合は、まず対応する oracle または実装対象を直接読むとき。
- INDEX のルーティングだけを確認する場合や、quota retry の個別実装箇所を直接調べる場合。

## hash
- 9e6d747fab4e9e0aedacb5dbe12281791c9423a1baa269664235d25b25a925e3

# `test_codex_runtime_retry.py`

## Summary
- Codex exec の Structured Output 補正、capacity retry、JSONL error、中断、retry 上限、成果物差分保持を、最終結果と共有ログ列まで含む外部挙動として検証するテスト群。
- run_codex_exec の retry 状態、Codex subprocess 呼び出し回数、call log、subcommand event を同一の状態機械の文脈で確認する。

## Read this when
- run_codex_exec の出力契約違反や parse failure の補正、同一 session 継続、Structured Output schema 検証、postcondition 検証を確認したいとき。
- capacity error の retry、backoff、上限、stdout JSONL の未知 error、KeyboardInterrupt の失敗記録を確認したいとき。
- retry や補正 turn による agent diff の保持・復元、および call log と codex_call event の対応を確認したいとき。

## Do not read this when
- run_codex_exec の通常成功経路だけを確認したいときは、通常成功を直接扱うテストや実装を読む。
- 共有ログ schema や subprocess の一般仕様そのものを確認したいときは、対応する正本仕様または実装を直接読む。

## hash
- 02ef35486ab1026ce3b326dbcab08f6f5bd12c3232e76c035afdc6ec2ed93cb0

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

# `test_feedback.py`

## Summary
- feedback の reporter、collector、raw observation、pending state、report cut、Codex による normalization/verification、atomic publication、active state、cleanup を同一 fixture で検証する統合テスト。
- 中断・再開、checkpoint の回収、inconclusive report、publication 後の部分 cleanup、machine observation の再発 threshold と期間境界を扱う。
- path 境界、symlink、secret masking、UTF-8、JSON 数値、未定義・改変 artifact、current pointer と hash の整合性を検証する。

## Read this when
- feedback report の外部挙動、publication 可否、active state の compact 化、pending raw の処理結果を確認するとき
- feedback reporter/collector の protocol、capability、rate limit、context validation、degraded fallback を確認するとき
- feedback report の中断・再開、Codex verification checkpoint、診断 report、cleanup recovery を確認するとき
- raw observation や active generation の path・hash・symlink・未定義 artifact 検証を確認するとき

## Do not read this when
- feedback の実装責務や内部アルゴリズムを確認したいときは、runtime_feedback、runtime_feedback_state、runtime_feedback_store、feedback report 実装を直接読む
- feedback の正本仕様や agent call の prompt/schema 契約を確認したいときは、対応する oracle file と builder 定義を直接読む
- feedback と無関係な CLI サブコマンドや一般的なテスト実行手順を確認するとき

## hash
- 34985aba280eace307a7e04a54c5093482515d62cdeb98ef296825e74aa07c74

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
- `cmoc indexing` の CLI 実行全体を外部挙動として検証するテスト。
- doctor による未初期化リポジトリの準備、clean な通常 worktree と linked worktree の対象判定、dirty 差分の拒否を確認する。
- Codex による INDEX.md エントリー生成、fresh hash による再生成省略、worktree 固有設定の preflight 利用を確認する。
- INDEX.md のみを対象とする commit、既存の staged・unstaged 非 INDEX 差分の保持、Git 差分確認失敗の扱いを検証する。

## Read this when
- `cmoc indexing` の CLI 事前条件や doctor・worktree の振る舞いを確認したいとき。
- INDEX.md 更新時の Codex 呼び出し、preflight、hash による省略条件を確認したいとき。
- indexing が生成した INDEX.md だけを commit し、他の差分を保持する lifecycle を確認したいとき。
- indexing の拒否条件や Git 異常系の外部挙動をテスト例から確認したいとき。

## Do not read this when
- indexing の実装責務や正本仕様を確認したいときは、実装または oracle の indexing 仕様を直接読む。
- Structured Output の項目名・型・形式だけを確認したいときは、index entry schema を直接読む。
- INDEX.md のルーティング内容そのものを確認したいときは、生成対象の INDEX.md を直接読む。

## hash
- 7d13bd4f144ab4d839e08da289b7605e2fa95ced426883c9f9f4e198ea0bc27d

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
- `cmoc oracle edit` の main-worktree exec 制御を、成功時と main agent call／仕様削減 agent call の各失敗時で検証する統合テスト。
- 既存の staged／unstaged 差分、session state、editor 入力ファイル、oracle spec の変更、実行順序、agent call parameter、通知および terminal report の境界を比較する。
- builder 失敗時の editor work file 非作成と、linked worktree・非 session branch・inactive session に対する起動前提検査も扱う。

## Read this when
- `cmoc oracle edit` の main-worktree 実行経路、2 回の exec 呼び出し、失敗時の差分保持、仕様削減の開始条件を変更・検証するとき。
- oracle edit の editor 入力処理、indexing preflight、起動前提、session state、Git 差分、通知または terminal report の契約を確認するとき。
- oracle edit 用 launch parameter の file access mode、cwd、indexing 実行有無、purpose、共有 config をテストで確認するとき。

## Do not read this when
- oracle edit の prompt 内容や launch parameter の生成実装そのものを確認したい場合は、対応する oracle edit builder／launch 実装を直接読むとき。
- 一般的な doctor、Git helper、Codex preflight、runtime state の仕様や共通動作だけを調べる場合は、この個別 CLI 統合テストではなく各実装・仕様の対象を読むとき。
- oracle edit 以外のサブコマンドの挙動や、対象テストに記載されない成功・失敗条件を調べるとき。

## hash
- 26d8a4af016fcc430d25dfa6d26729a5d51a6ff8edded3debfb72d724f12f8cb

# `test_oracle_investigation_cli.py`

## Summary
- `cmoc oracle investigation` の CLI 起動経路を検証し、session なしの main worktree での起動可否、前処理から TUI 起動までの順序、生成パラメータ、入力ファイルの後処理を確認するテスト。
- oracle investigation の realization adapter が公開する補助 API を制限し、builder の公開境界を検証するテスト。

## Read this when
- `oracle investigation` サブコマンドの起動条件や session 前提を確認するとき。
- doctor preprocess、prompt editor input、prompt builder、indexing preflight、TUI 起動の連携順序を変更または検証するとき。
- oracle investigation のファイルアクセスモード、作業ディレクトリ、prompt 内容、入力コピーの後処理に関する CLI 挙動を確認するとき。
- oracle investigation の realization adapter における公開 API の境界を変更または検証するとき。

## Do not read this when
- oracle investigation の oracle 正本仕様そのものを調査するときは、参照されている oracle 文書を直接読む。
- investigation の launch TUI builder 実装の詳細を変更または調査するときは、対応する realization 実装を直接読む。
- CLI 全体の共通起動処理や、oracle investigation 以外のサブコマンドの挙動だけを確認するとき。
- prompt editor input の共通仕様や indexing の一般仕様だけを確認するとき。

## hash
- 361aab4aed3d21a67f310e409d9ced4e92b1423309a74552b8564600b5b2e806

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
- このテストは、ソースツリーを配布時のパッケージ配置へコピーした隔離環境で、主要な ACP builder、prompt editor 入力境界、公開再エクスポート、設定モジュールの import と公開面を検証する。
- packaged layout で正本の schema・prompt・file access mode・実行前処理・agent call cwd が維持され、realization 側の公開 import が正本定義を再利用し、意図しないモジュール名を公開しないことを確認するテストの入口である。

## Read this when
- 配布後のパッケージ配置で oracle/realization の import 境界や canonical builder の動作を確認したいとき
- oracle review、quota probe、oracle edit、prompt editor、ACP basic、cmoc config の公開 API・namespace・設定再エクスポートを検証または変更するとき

## Do not read this when
- 個別 builder の実装詳細、正本 schema や oracle 文書の内容、prompt editor の仕様そのものを確認したいとき
- packaged layout 以外の通常の単体テストや、対象モジュールの実装を直接調査すれば足りるとき

## hash
- dc8512ec48a1af0a34a0f84bbb7b6d739be0331ec57cdae7fef7a6e08b685bee

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
- 実 Codex CLI と実推論を含む独立 process の受け入れ試験として、非対話・TUI の全末端サブコマンドを利用者向け本番経路で検証する。終了 code、report、永続 state、Git 状態、agent call log、PTY 上の応答完了と終了操作を確認し、LLM の回答品質は判定しない。

## Read this when
- 全末端サブコマンドが CLI 登録どおり本番 process 経路で実行されることを確認したいとき。
- 実 Codex CLI の agent call 設定、prompt log、call log、report、session/run の状態遷移、Git・worktree の後処理を受け入れ試験として確認したいとき。
- Codex TUI の PTY、端末 capability query、trust prompt、応答完了、終了操作を含む実経路を検証したいとき。

## Do not read this when
- 個別サブコマンドの実装仕様や通常の単体テストを直接確認したいとき。
- LLM の回答内容や品質の妥当性を評価したいとき。
- 実 Codex・独立 process・PTY を使わないテストや、単一機能の内部ロジックだけを変更・調査するとき。

## hash
- a93afbc6a858977d1b63be86bbb5c5fa044e8d9761501883b720b1582a35e278

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
- prompt part の rendering と complete prompt の組み立てを検証する回帰テスト。各 policy builder の構造・カテゴリ順序・本文、選択した policy block の注入、complete prompt の固定部・動的部・placeholder 展開、file access mode ごとの制約、root context に応じた deny-list を扱う。prompt builder と policy 実装の回帰確認への入口となる。

## Read this when
- prompt part または complete prompt の組み立て、rendering、section 順序、placeholder 定義を変更・調査するとき
- oracle、realization、feedback、file access、index entry、routing などの prompt policy builder を変更・調査するとき
- policy block の重複注入、カテゴリ順序、SDHeader・SDPolicy 構造、root-specific なアクセス制約を検証するとき

## Do not read this when
- prompt builder や policy の挙動に関係しないテスト、実装、仕様を扱うとき
- 個別 policy の本文や complete prompt の実装を直接確認する必要があり、対応する builder または正本ファイルへ進むとき
- テスト実行方法や共通の開発環境だけを確認するとき

## hash
- 2b96d4888e2a48186c2a451cc499c920817064b950c781c8ef8a7c62592fd321

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
- Codex argv の model、sandbox、provider 上書きと feedback MCP 環境の分離を検証するテスト。schema のバイト保持と不正 JSON 入力の扱いも確認する。

## Read this when
- Codex 起動時の file access mode と sandbox、approval、model/provider 設定の変換を変更・調査するとき。
- feedback reporter の環境変数を Codex argv・subprocess env・MCP 設定へ渡す境界を変更・調査するとき。
- provider 設定の TOML argv エンコード、schema の保存ハッシュ、Codex 出力 JSON の読み取りを変更・調査するとき。

## Do not read this when
- Codex の実装詳細だけを確認し、argv・provider・feedback・schema/output の契約を変更または検証しないとき。
- 対象機能の挙動テストを追加・変更する場合でも、個別の実装契約を直接確認する必要がなく、より具体的な下位テストや仕様書へ進めるとき。

## hash
- ce0ebe137caacb7ac9798341d4db9bb0b68cc536725ed2d662668e32d69ec793

# `test_runtime_config.py`

## Summary
- CmocConfig の既定値と agent call ごとの Codex provider・model・reasoning effort の直接設定を検証するテスト。
- config.json の section・map 順序、全設定値の round-trip、旧形式設定の除外を検証する。
- JSON/TOML 共通値、必須文字列、整数、object 構造、深い入れ子、有限性などの入力検証と利用者向けエラー変換を検証する。
- config path の欠落・非通常ファイル・named pipe・symlink を安全に扱い、doctor の案内や link 先非変更を確認する。

## Read this when
- cmoc config の読み込み・書き込み・変換仕様に対するテスト挙動を確認するとき
- CmocConfig の既定値、Codex provider、agent call 設定、oracle_review 設定の永続化を確認するとき
- 不正な設定値や壊れた JSON に対する CmocError と UTF-8 安全なエラー報告を確認するとき
- config path の安全性や、旧 config 形式の互換的な除外を確認するとき

## Do not read this when
- CmocConfig の実装詳細や正本仕様そのものを確認する必要があるときは、設定実装または対応する oracle 文書を直接読む
- config 永続化・入力検証以外のランタイム機能や、他のテスト領域を調べるときは、このテストを入口にしない

## hash
- 14001a43fd34eff5d41b32d930f11121102d14d32b77e94ef2513d7de1e773f6

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
- session fork・join・abandon における CLI の外部挙動を、session branch と永続 session state のライフサイクルとして検証する回帰テスト。fork の branch/state 作成、session-id 衝突、rollback、linked worktree 対応を扱う。abandon と join の home branch 切替、state 遷移、cleanup、失敗時の復元、dirty worktree・欠損/破損 state・home branch 不在の拒否も対象とする。
- session join の conflict 解消では、Codex agent の sandbox と prompt の境界、対象外差分や conflict file の不要変更の拒否、削除・特殊文字や改行を含む path の扱い、conflict marker 検出、merge 後の branch 削除と警告、linked worktree の main worktree context を検証する。repository-local feedback state を join の merge/rollback 対象外として保持する挙動も確認する。

## Read this when
- session CLI の fork・join・abandon の外部契約を変更・確認するとき。
- session branch、session state、home branch、linked worktree のライフサイクルや cleanup/rollback を調査するとき。
- session join の conflict 解消、Codex 呼び出しの sandbox、対象 file 限定、特殊 path、merge 後処理を確認するとき。
- session CLI のエラー出力、report、state field 保持、dirty worktree や branch 不在時の拒否を回帰確認するとき。

## Do not read this when
- session CLI 以外の機能を扱うとき。
- 単一サブコマンドの正本仕様や実装詳細だけを確認する場合は、対応する session サブコマンド仕様・実装へ直接進む。
- session state の正規形式そのものや共通 CLI 出力契約を確認する場合は、session_state または共通出力の正本仕様を直接読む。

## hash
- a97510e4c45a2268613306c7dfa2c425b29b33e2650114e32450c501547fe8c7

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
