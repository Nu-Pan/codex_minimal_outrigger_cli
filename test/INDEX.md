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
- test_acp_builder_editing_run_parameters.py は、editing run の canonical builder adapter を対象にした実装テストで、互換 import の再公開、apply/refactor 用 prompt の内容、実行設定、canonical Structured Output schema の参照、raw diff 内の境界風文字列の保持を検証する。builder の adapter 互換性や editing run 向け parameter の変更・調査時に、期待される外部挙動の確認入口として読む。

## Read this when
- editing run の apply または refactor builder の parameter 構築を変更・レビューするとき
- canonical builder の互換 import 経路、prompt に埋め込む commit 範囲・diff・policy、実行設定、Structured Output schema の接続を検証するとき
- raw diff に三連 backtick や prompt 境界風の見出しが含まれる場合の prompt 境界処理を確認するとき

## Do not read this when
- canonical builder 自体の実装仕様や oracle の正本内容を確認することが目的の場合
- editing run と無関係な builder、または一般的な test 実行手順だけを確認する場合

## hash
- 8c643993929ff99ef28bfdd53be5a76438e2090cbf209269df796af723adc326

# `test_acp_builder_indexing_parameters.py`

## Summary
- indexing の index entry builder に対する実装・正本互換性テスト。モデル、推論強度、読み取り専用設定、cwd、preflight、prompt の採用方針を検証する。
- index entry 用 Structured Output schema の semantic 配列に空値を許さない制約を検証する。
- 対象本文に三連 backtick が含まれる場合の prompt 境界保護と、oracle builder との一致を検証する。
- 互換公開モジュールが builder のみを公開する契約を検証する。

## Read this when
- indexing index entry builder の parameter 設定、prompt 生成、schema 制約、または互換公開面を変更・検証するとき。
- 対象本文を prompt に埋め込む際のコードフェンス境界や oracle 実装との互換性を確認するとき。

## Do not read this when
- index entry builder や indexing 互換 module の挙動を扱わず、他の builder・schema・公開 API のテストだけを調べるとき。
- index entry の生成内容そのものやルーティング規則を確認する場合は、対応する正本仕様を直接読むとき。

## hash
- 602f54cd0d960b38d21d0b980b7ff61e5afc20dba958221f2961ce897ddf6791

# `test_acp_builder_oracle_review_parameters.py`

## Summary
- review 用 ACP builder の parameter・schema・adapter 公開面をまとめて検証する回帰テスト。enumerate、judge、merge、validate（advocate/challenger）の canonical builder 互換性、モデル・推論・アクセス設定、policy block 注入、schema 一致、動的入力保持を確認する。
- review builder が生成する動的 prompt の三連 backtick、section 見出し、placeholder 風文字列、連続空行を実際の section 境界と誤認せず fence 内に安全に保持できることを検証する、prompt builder 実装の回帰入口。

## Read this when
- review ACP builder の builder 関数、AgentCallParameter の設定、Structured Output schema、oracle review policy の注入または canonical builder 互換性を変更・検証するとき
- 動的 prompt に findings、finding、advocate、challenger などの入力を埋め込む処理で、code fence や section 境界の保護を確認するとき
- review の enumerate・judge・merge・validate 各段階の公開 adapter が指定 builder のみを公開する契約を調査するとき

## Do not read this when
- 対象が review builder 以外の ACP builder、または schema・prompt・公開 adapter の契約に関係しない実装であるとき
- oracle review の判定仕様そのものや個別の schema 定義を直接確認する必要があり、対応する oracle file を読む方が直接的なとき
- 一般的なテスト実行方法や共通の ACP builder 基盤だけを調査するとき

## hash
- 01d915fb4640f7fca4705af33b7ea6b620d263aed0577042c7f8d5809c2891e3

# `test_acp_builder_session_join_parameters.py`

## Summary
- 対象は session join の conflict resolution builder の契約テストで、互換モジュールの公開 API が builder のみであること、canonical builder との同一性、repo write 権限・モデル設定・最大推論・実行 cwd・prompt 内容・preflight 無効化を検証する。競合対象パスの prompt 埋め込みでは、三連バッククォートを含むパスがコードフェンス境界を壊さないことも確認する。
- session join の conflict resolution parameter builder の公開面、生成パラメータ、prompt のポリシー構成、競合パスのコードフェンス保護を変更・レビューするときの入口。canonical 実装との互換性と、対象 builder 固有の契約をテストから確認できる。

## Read this when
- session join の conflict resolution 用 parameter builder や、その互換モジュールの export 契約を変更・レビューするとき
- conflict resolution builder が使用するモデル、推論強度、repo write 権限、cwd、preflight 設定、prompt の必須内容を確認するとき
- 競合対象ファイルのパスを prompt 内のコードブロックへ埋め込む処理で、バッククォートを含むパスの安全性を確認するとき

## Do not read this when
- session join 以外の builder の契約だけを確認する場合
- conflict resolution builder の実装や正本仕様そのものを直接確認する場合
- 単に一般的な test 実行手順や repository fixture の共通実装を調べる場合

## hash
- 604fcb7843857472d716ad8dee68840128fb2fdbc00d99087865cb29d946e6ba

# `test_acp_builder_tui_parameters.py`

## Summary
- TUI 起動 builder が入力 prompt に依存せず、固定された agent call parameter、実行設定、prompt policy を使用することを検証するテスト。
- TUI 起動用の互換 module が canonical builder のみを公開し、その builder を正しく再エクスポートしていることを検証する。

## Read this when
- TUI 起動 builder の parameter 固定値、prompt に含める policy、元 prompt の保持、indexing preflight の設定を確認するとき
- TUI 起動 builder の互換 module における公開 API と canonical builder との同一性を確認するとき

## Do not read this when
- TUI 起動 builder の実装や正本仕様の詳細を確認するとき
- TUI 以外の builder の parameter や module 公開面を確認するとき
- 実際の TUI 起動処理や editor input の生成動作を調査するとき

## hash
- 09b36f7fd2fda6cd51f85d3f3c963de52a096e36575149b8fcb118aef9ea6877

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
- TUI 起動前処理の外部挙動を検証するテスト。doctor preprocess、エディタ入力、完全プロンプト確定、Codex TUI 直接起動、差分保持、linked worktree と `.cmoc` ignore の扱いを対象とする。TUI サブコマンドの実装変更や挙動確認を始める際の検証入口。

## Read this when
- `tui` サブコマンドの実行順序、エディタ入力の保存・抽出、完全プロンプト生成、起動パラメータ、既存 Git 差分の保持を確認するとき。
- linked worktree 起動時の agent call context、ログ配置、`.gitignore` 更新を検証するとき。
- TUI 起動前の indexing preflight や、editor work file と保存記録の分離に関する外部挙動を確認するとき。

## Do not read this when
- TUI 以外のサブコマンドの挙動だけを調査・変更するとき。
- プロンプト編集の正本仕様や editor input 構築ロジックそのものを確認するときは、先に対応する oracle 文書・oracle 実装を読む。
- TUI 起動パラメータの生成実装そのものを変更するときは、対応する builder 実装と正本仕様を直接読む。

## hash
- 7b8f8f8db6af7b836c1d7c5f6907fbb86f3a7cded31a30e5c98a1a5a2c00873e

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
- editing run の統合 realization test。
- apply/refactor の fork、共通 run state、run worktree、session branch、join/abandon の lifecycle を検証する。
- agent が変更・commit した realization file と cmoc 管理対象（INDEX、refactor state、oracle）の境界、rollback、merge、cleanup、process tracking を検証する。
- refactor の調査 cycle、findings、rename、unresolved target、change summary、永続 state 更新を検証する。
- INDEX refresh、Codex child の追跡・停止、primary report、lifecycle report、terminal result、通知、feedback observation の保存を検証する。
- 個別サブコマンドの実装詳細ではなく、fork から joinable/error、join/abandon 完了までの共有 lifecycle と異常系を横断確認する入口。

## Read this when
- editing run の apply/refactor fork の統合挙動を変更・確認するとき
- run join または run abandon の state 遷移、merge、worktree/branch cleanup を変更・確認するとき
- agent の予期しない file change、commit、遅延処理、process tracking、rollback の安全性を確認するとき
- INDEX refresh や refactor state 同期が run lifecycle に与える影響を確認するとき
- fork、join、abandon の report、primary report、通知、feedback metadata の検証箇所を探すとき

## Do not read this when
- INDEX エントリーの生成以外で、個別実装関数の詳細仕様だけを確認したいとき
- run lifecycle と無関係な通常の unit test や CLI 出力を確認したいとき
- 正本仕様の内容を確認したいときは、対象テストではなく参照される oracle 文書を直接読むとき
- 対象ファイル内の一つの helper の実装を確認したいときは、対応する実装モジュールを直接読むとき

## hash
- 41527f94c3b7981c38bc1f7821d514fe363c91f464b4c29ee38d279efbf5264a

# `test_feedback.py`

## Summary
- feedback の agent-facing reporter と collector の境界から、observation の保存・検証・重複排除・候補化・verification までを検証するテスト群。
- report cut と checkpoint の再開、incomplete/interrupted 処理、active state の atomic publication、generation hash、current pointer、cleanup、raw artifact の破損検出を確認する統合 fixture の入口。

## Read this when
- feedback reporter の公開ツール、collector 転送、rate limit、capability、protocol error、不正応答の扱いを確認するとき
- agent または machine observation の schema 検証、path 境界、symlink 防止、secret masking、canonical JSON、idempotent な保存を確認するとき
- observation から issue candidate への identity、deduplication、fingerprint、threshold、window expiry、verification verdict の処理を確認するとき
- feedback report の report cut、checkpoint recovery、Codex 再呼出し抑止、incomplete/interrupted からの再開を確認するとき
- active generation、current pointer、report artifact、publication cross-reference、hash、未列挙 artifact、部分 cleanup の整合性を確認するとき

## Do not read this when
- feedback の正本仕様や state 契約を確認する場合は、本文中に対応付けられた oracle 文書を直接読む
- normalize または verify の prompt、FileAccessMode、Structured Output schema の定義だけを確認する場合は、対応する builder と schema を直接読む
- feedback report の Markdown 表示仕様だけを確認する場合は、report rendering または subcommand の正本仕様を直接読む

## hash
- 1a8238b45eb18ecbf14167d237cbcb5f0110207a4b567c40b51fbb524a2bdb36

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
- `oracle investigation` サブコマンドがセッションなしの main worktree で起動できることを、doctor preprocess、prompt editor 入力、builder 呼び出し、preflight 登録、TUI 起動の順序と生成パラメーターを通じて検証する CLI テスト。
- investigation の realization adapter が公開する builder を単一の想定名に限定していることを検証する。

## Read this when
- `oracle investigation` の起動前処理、prompt editor との受け渡し、TUI 起動条件、または起動パラメーターを変更・調査するとき。
- investigation の realization adapter の `__all__` や公開シンボルを変更・調査するとき。

## Do not read this when
- oracle investigation 以外のサブコマンドの CLI 起動条件を扱うとき。
- investigation adapter の公開範囲や CLI 起動フローに関係しない、一般的な builder 実装・git 補助・共有 CLI fixture を扱うとき。

## hash
- 1b12086e475b38ad23fd766cbf7594182ba1598770b24a95ffda16565d3a954e

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
- oracle review の report 生成と CLI 出力を、oracle review の report contract に基づいて回帰検証するテスト群。
- report の節順、finding の severity・accept/reject 分類、件数、path 集計、エラー・中断時の完了済み oracle、CLI option、timestamp 予約、YAML エスケープを扱う。
- oracle review の report schema と表示結果の対応を一箇所で確認するための回帰テスト入口であり、実装変更時に report 内容や CLI の成功・失敗出力へ影響する場合に読む。

## Read this when
- oracle review の report 構造、finding の表示分類・件数、または CLI 出力を変更・検証するとき
- oracle review の列挙・判定処理がエラーや Ctrl+C を受けた際の report 内容を確認するとき
- report の oracle path 集計、特殊文字のエスケープ、timestamp 付き出力先、YAML frontmatter の文字列保持を変更するとき

## Do not read this when
- oracle review の report や CLI 出力に関係しない機能を変更・調査するとき
- oracle review の仕様・実装契約そのものを確認する必要があり、まず oracle 文書や実装を直接読むべきとき

## hash
- b9e9424d715178114c995a1f4015fe3c0c9dd72474e9d049998725e6155572a9

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
- 隔離した packaged layout にソースツリーをコピーして実行し、Python パッケージの import 境界と公開面を検証するテスト。
- canonical agent builder が schema・完全 prompt・期待する parameter を参照できること、oracle edit と prompt editor の入力境界が正本を利用することを確認する。
- ACP basic と cmoc config が canonical 定義または設定定義だけを再公開し、意図しない名前を公開しないことを確認する。

## Read this when
- packaged layout での import 失敗や、パッケージ配置・setuptools 設定の変更を調査するとき
- oracle review、quota probe、oracle edit、prompt editor の builder が正本の schema・prompt・入力を参照することを検証するとき
- acp.builder.basic または config.cmoc_config の再公開 API と module namespace の境界を変更・確認するとき

## Do not read this when
- packaged layout、Python import 境界、builder の正本参照、または再公開 API に関係しない機能のテストを読むとき
- 通常の単体ロジックだけを検証し、隔離環境でのパッケージ配置や公開面を扱わないとき

## hash
- b715c6d5a9ab0a6383d8048fe018444dc4576cb41082cd5813bd44da8759a2c8

# `test_primary_report.py`

## Summary
- 非対話末端サブコマンドの primary report 完了契約を検証するテスト。処理開始前のエラー、ユーザー中断、refactor fallback、primary report 未保存時の internal failure を対象とし、保存先、front matter、端末出力、診断ログ、コマンド固有の完了情報を確認する。

## Read this when
- 非対話末端サブコマンドの完了処理、エラー処理、中断処理、primary report 保存確認のテストを追加・変更・調査するとき。
- doctor、indexing、session、oracle、realization、run、feedback の各サブコマンドで、処理開始前エラー時の primary report 契約を確認するとき。

## Do not read this when
- 個別サブコマンドの通常処理や引数仕様だけを確認する場合は、対応するサブコマンド仕様を直接読む。
- primary report の一般的な形式やエラー分類の仕様だけを調べる場合は、console_and_file_log.md または error_handling.md を直接読む。

## hash
- 6feef722be26b641285fbed5b9a02668da485eb399adb02e315a08523cf858be

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
- prompt policy 各部品の rendering と complete prompt の組み立てを検証する回帰テスト。policy のカテゴリ・順序・個別注入、prompt の section 配置、feedback 指示、placeholder 展開、file access mode 別の境界、root 定義の競合、主要 policy 内容を対象とする。
- prompt builder や policy builder、StructDoc rendering、complete prompt の構成・placeholder 処理を変更またはレビューする際のテスト入口であり、関連する prompt policy の挙動を横断的に確認できる。

## Read this when
- prompt policy または complete prompt の rendering・section 注入・順序を変更するとき
- policy flag、file access mode、placeholder、root path context、feedback 指示の挙動を変更するとき
- prompt builder 関連の回帰テストや、各 policy builder の出力契約を確認するとき

## Do not read this when
- prompt builder や policy の挙動に関係しない機能を変更・調査するとき
- 個別 policy の正本仕様そのものを確認する必要があり、テストではなく対応する oracle 文書を直接読むべきとき
- prompt builder 実装の詳細を変更せず、一般的なテスト実行方法だけを確認するとき

## hash
- 1d3a6dc4c69d63d58680010c2dd28088ea59f6d4e5c145d4836317a05252d0d3

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
- session fork、join、abandon の CLI 外部挙動と session branch/state のライフサイクルを、通常経路・失敗時の rollback・競合・linked worktree・dirty worktree 拒否まで含めて検証する回帰テスト。
- session CLI の状態遷移、永続 state cleanup、home branch との切替、conflict resolution の sandbox と対象差分制約を確認する必要がある場合の入口。

## Read this when
- session fork、join、abandon の外部挙動を変更または調査するとき
- session state の active・joined・abandoned 遷移や branch cleanup の回帰を確認するとき
- linked worktree、dirty worktree、home branch 検証、session join の conflict resolution を扱うとき

## Do not read this when
- CLI 以外の session 内部実装だけを調べるとき
- session state の正本仕様やサブコマンド単体の仕様を確認する場合は、先に対応する oracle 仕様を読むとき
- 一般的な CLI テスト基盤や session と無関係なコマンドの挙動を調べるとき

## hash
- 9b8d29d1442451d67c21b00b3354d089f6379ad38c85ac6dd0aa716f3fd6b6d1

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
- StructDoc の Markdown renderer の単体テスト。連続 blank line の縮約、code block の fence 長、StructBlock の再公開と opaque child、参照未検証、単一 child の型検査を検証する。renderer の整形挙動や互換性を確認する際のテスト入口である。

## Read this when
- Markdown renderer の整形結果、code block の fence、StructBlock の互換性、参照検証の扱い、または構築時の child 型検査を変更・確認するとき。
- StructDoc または StructBlock に関する realization test の期待挙動を確認するとき。

## Do not read this when
- renderer の実装詳細を調べるときは、まず basic.struct_doc の実装を読む。
- 正本仕様や oracle 側の挙動を確認するときは、テストではなく参照先の oracle 文書・実装を直接読む。

## hash
- 48e185c85c704d518b145a959075fff2b27112e00efd7ea289daa07cf41e3f80

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
