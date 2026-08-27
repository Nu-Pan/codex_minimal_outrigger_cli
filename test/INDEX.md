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
- editing run workload で使用する apply/refactor の canonical builder adapter を検証するテスト。builder が要求されたモデル・推論・ファイルアクセス・preflight・作業ディレクトリ設定を持ち、必要な commit 範囲、raw diff、policy、対象 path、Structured Output schema を prompt と parameter に反映することを確認する。
- 互換 import 経路が canonical builder 関数をそのまま再公開することを確認する。
- raw diff に三連 backtick や prompt 境界風の見出しが含まれても、外側の prompt 境界や diff セクションを壊さず保持することを検証する。
- refactor の file review and fix および change summary builder が canonical schema を使用し、schema の変更 path・changes 制約を満たすことを確認する。

## Read this when
- editing run の apply/refactor builder の parameter 設定や prompt 構成を変更・検証するとき。
- canonical builder と互換 import 経路の同一性を確認するとき。
- raw git diff を prompt に埋め込む際の fence や marker-like content の境界処理を確認するとき。
- refactor builder の Structured Output schema 参照と schema 事後条件を確認するとき。

## Do not read this when
- canonical builder の実装仕様や oracle 側の正本を確認する場合は、列挙された oracle file を直接読む。
- 一般的な git worktree fixture や他の builder の挙動だけを確認する場合は、この対象ではなく対応する実装・テストへ直接進む。
- INDEX.md の既存ルーティングを確認する場合は、このテスト本文ではなく INDEX.md を読む。

## hash
- a8176184f710338d5dce5d1e9dacc7a7986b4a9d7e98565526bcba030d05db1d

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
- 対象ファイルは、oracle review 用 ACP builder 5種について、canonical builder との互換性、公開面、モデル・推論・アクセス設定、policy block 注入、schema 一致、動的入力保持、コードフェンス保護を検証する回帰テスト群である。各 review builder の parameter 契約と prompt 境界保護をまとめて確認する入口。

## Read this when
- oracle review の enumerate、judge、merge、validate advocate/challenger builder の parameter や structured output schema を変更・レビューするとき
- review builder の公開 export、canonical builder 互換性、policy block 注入、動的 prompt の placeholder・nested code fence 保護を確認するとき
- review builder の schema や model class、reasoning effort、file access mode、indexing preflight の回帰を調査するとき

## Do not read this when
- review builder 本体の実装詳細だけを確認する場合は、対応する builder の実装ファイルを直接読むとよい
- review builder の schema 定義そのものの変更を確認する場合は、対象の builder・schema または専用テストを直接読むとよい
- 一般的な ACP parameter の仕様や共通 policy の正本を確認する場合は、この回帰テストではなく対応する oracle・設計文書を読むとよい

## hash
- 90e80b1d9367dcbce1ab5ada479c400e54c2d866a483bfaf37844a97d536314d

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
- 対象ファイルは、TUI 起動 builder がオリジナル prompt に依存せず、固定の agent call 設定・アクセス方針・索引前処理・prompt 見出しを組み立てることを検証するテスト。対応する canonical builder との整合性と、互換 module の公開 API が単一 builder に限定されることも確認する。
- 固定 parameter と prompt ポリシーの実装を確認したいときの入口であり、TUI 起動 builder の挙動検証を扱う。

## Read this when
- TUI 起動用 parameter の固定値、prompt に含める／含めない方針、original prompt の保持を変更・確認するとき。
- acp.builder.tui.launch_tui の公開面や canonical builder への委譲・同一性を検証するとき。

## Do not read this when
- TUI 以外の builder の parameter や prompt を調べるとき。
- builder の実装そのものを変更する場合は、まず対応する canonical 実装を直接読むべきとき。

## hash
- ef8b68144793435fd71b52f561d235d3bfc046f3bb6549258d8476bacc2e93cd

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
- TUI 起動直前の CLI 前処理の外部挙動を検証するテスト。
- エディターで編集した prompt を使った Codex TUI の直接起動、doctor 前処理、起動パラメータ、既存の staged・unstaged 差分の保持を確認する。
- 通常のリポジトリと linked worktree における editor 記録、agent call context、`.cmoc/gu` の git ignore、およびログ配置を検証する。

## Read this when
- TUI サブコマンドの起動順序や、editor 入力から Codex TUI 起動までの CLI 前処理を確認・変更するとき
- linked worktree 起動時の root、agent call cwd、editor 記録先、ログ配置を確認するとき
- TUI 起動に伴う `.cmoc/gu` の git ignore と既存差分保持の外部挙動を検証するとき

## Do not read this when
- TUI 本体の対話処理や、TUI 起動前処理以外のサブコマンドを確認するとき
- prompt 編集処理そのものの正本仕様・実装を確認するときは、対応する仕様または実装を直接読む場合
- TUI 起動前処理の実行結果ではなく、個別の prompt builder の詳細実装だけを確認するとき

## hash
- 215c8cc00ecf9bddecd64f8ec1ba42a116dfdf2fb2aa3358d127050aa845b3e9

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
- quota 枯渇後の Codex exec の probe・待機・resume・再実行を検証する回帰テスト群。保存済み stdout JSONL からの session ID 復元、代表 quota probe の共有と失敗伝播、resume／prompt 再実行、quota polling 上限、capacity retry、無効 JSONL、KeyboardInterrupt、CODEX_HOME/cwd、call log／subcommand log、および待機状態の後始末を一体として扱う。quota retry 状態機械の外部挙動を変更・検証する際の realization test の入口である。

## Read this when
- Codex quota 超過後の polling、代表 probe、resume、再実行の挙動を変更または調査するとき
- quota retry における session ID、probe の共有・失敗伝播、capacity retry、poll 上限の回帰を検証するとき
- Codex の呼び出し列、引数、CODEX_HOME／cwd、stdout・prompt・output・call log・subcommand log の観測結果を確認するとき
- quota 待機開始時の例外処理や共有待機状態の解除を変更・検証するとき

## Do not read this when
- quota retry の実装詳細そのものを変更・調査する場合は、まず codex runtime 実装と正本の codex exec 仕様を読むとき
- quota probe parameter の正本 builder や probe prompt の仕様だけを確認したい場合
- quota と無関係な通常の Codex exec、CLI、設定、または一般的なテスト実行を扱う場合は、この回帰テストへ直接進む必要はない

## hash
- 75126b7a0aae9bafa8f4f2dcf3e3f30186222d88f17145e965ad0b81d5c66c8d

# `test_codex_runtime_retry.py`

## Summary
- `run_codex_exec` の再試行・失敗処理を、Codex subprocess の呼び出し、call log、subcommand event、最終結果まで含めて外部挙動として検証するテストファイル。
- Structured Output の parse/schema/postcondition 違反に対する同一 session 内の出力補正、補正失敗時の成果物差分復元、retry 上限と backoff を扱う。
- capacity error、未知の JSONL error、中断、stdout JSONL 外のエラーマーカー、retry 中の agent diff 保持など、Codex CLI 失敗状態機械の分岐を確認する。

## Read this when
- `run_codex_exec` の Structured Output 補正、capacity retry、retry 上限、session 継続、成果物差分保持または復元の挙動を変更・検証するとき。
- Codex subprocess の呼び出し回数、call log の内容、codex_call event の status/error/returncode、構造化出力検証 exhausted 診断を確認するとき。
- Codex CLI の JSONL error、KeyboardInterrupt、失敗時ログの外部契約に関するテストを追加・変更するとき。

## Do not read this when
- Codex exec の通常成功経路や、retry・失敗状態機械に関係しない別の CLI 機能だけを調べるとき。
- 実装の詳細ではなく、Structured Output の schema 形式そのものを確認したいときは、schema の正本仕様や検証実装を直接読む。
- ログの一般的な形式や全サブコマンド共通の仕様だけを確認したいときは、共有ログ仕様または logger 実装を直接読む。

## hash
- 49fd991e96420448de34e486c681b41e10b8a7540347713fe7f0cc8bc44b55d2

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
- doctor preprocess の共有 lifecycle を、CLI 呼び出しと直接呼び出しの両方から検証する統合テスト。`.cmoc/gu` の ignore、`.agents`、config、refactor state の修復、reporter の degraded/error 挙動、共有 lock、repair commit を扱う。
- Git の pre-existing index を保つ契約も対象とし、staged/unstaged 差分、index flag、intent-to-add、rename、削除、symlink、不足 index、既存ローカルファイルなどの状態を修復前後で検証する。
- doctor preprocess の外部契約に関するテスト入口であり、共通 fixture・linked worktree・doctor lock・副作用を前提とする関連ケースをまとめて確認する。

## Read this when
- doctor preprocess の CLI または直接呼び出し時の修復 lifecycle を確認・変更するとき
- `.cmoc/gu`、`.agents`、config、refactor state の修復や reporter 検証の挙動を確認するとき
- doctor が既存の Git index、staged/unstaged 差分、index flag、linked worktree をどう保持するか確認するとき
- doctor の共有 lock、repair commit、symlink 安全性に関する外部契約を確認するとき

## Do not read this when
- doctor preprocess の実装詳細だけを確認する場合は、まず `commons.runtime_doctor` など該当 realization を直接読むとき
- doctor 以外のサブコマンドや、一般的な Git fixture・CLI 実行ヘルパーの仕様だけを確認するとき
- 正本仕様そのものを確認・変更するときは、列挙された oracle 文書を直接読むとき

## hash
- 836cae096809ee939b46d6a711a601a73d782198b9911070ef5048256b951a3c

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
- `test_packaged_import.py` は、隔離した packaged layout 上で ACP・oracle・config の import 境界と公開面を検証するテスト入口です。正本の builder、prompt editor、設定定義が期待する schema・prompt・enum・再公開関係を保つことを確認します。

## Read this when
- packaged layout での import 失敗や、setuptools の package 配置・モジュール境界を調査するとき
- oracle review、quota probe、oracle edit、prompt editor の builder が正本ファイルを参照することを検証するとき
- ACP basic や cmoc config の公開 API と `__all__` の意図しない露出を確認するとき

## Do not read this when
- packaged layout や import 境界ではなく、個別 builder の本体仕様・schema 定義・prompt 内容そのものを調査するときは、対応する oracle の実装・仕様・schema を直接読む
- 通常の機能テストや、packaging と無関係な CLI 挙動の検証だけが目的のとき

## hash
- 6bdf3d6c812315b08f3f21d86e08d9aa36df47b1dd2c28104969d70afe3ed938

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
