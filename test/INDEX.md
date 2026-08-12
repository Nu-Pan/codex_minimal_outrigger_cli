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
- Codex 実行ラッパー関連テストで共用する、認証に依存しないテスト環境、既定パラメータ、CLI 引数解析、Codex override のスタブを提供する。runtime テストから再利用されるテスト支援の入口。

## Read this when
- Codex 実行の runtime wrapper テストを追加・変更し、共通の一時環境や Codex パラメータ、CLI 引数検証用ヘルパーが必要なとき。
- Codex の subprocess 制御をテストする際に、実際の override 生成を固定値へ差し替える方法を確認したいとき。

## Do not read this when
- Codex 実行ロジック自体や本番 CLI の挙動を確認・変更するときは、実装対象のモジュールを直接読む。
- Structured Output schema の定義や一般的なテスト規約だけを確認したいときは、対応する仕様・規約文書を直接読む。

## hash
- 5b56b039a83a8845f85bd3ec2097eb80a803281a4ade7c305575f1887f28e898

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
- editing run workload の canonical builder adapter を検証するテスト。apply builder の実行設定、commit 範囲、oracle raw diff、標準プロンプトの埋め込みを確認する。refactor builder では canonical Structured Output schema、実行設定、対象 path、レビュー条件、決定論的事後条件を確認する。raw diff 内の三連 backtick や境界風見出しを安全に保持できることも検証する。

## Read this when
- editing run の apply または refactor 用 builder の挙動を変更・レビューするとき。
- builder が生成する prompt の commit 情報、oracle diff、標準規則、Structured Output schema、実行設定を確認するとき。
- raw diff のコードフェンスや prompt 境界風テキストの扱いを変更するとき。
- canonical schema の必須項目や変更 path の事後条件を変更するとき。

## Do not read this when
- editing run builder や対応する canonical schema の挙動に関係しない実装を調査するとき。
- 一般的な git fixture、共有 test support、または無関係な agent call parameter のテストを読むとき。
- prompt や Structured Output schema の内容を確認する必要がなく、対象の実装ファイルを直接検証できるとき。

## hash
- a793d55ba07208954044e43a71a822d29dff84c0d82b4fea6144fac0bcaf7ea8

# `test_acp_builder_indexing_parameters.py`

## Summary
- indexing index entry builder のテストであり、builder の parameter 設定、Structured Output schema の必須配列制約、対象本文のコードフェンス保護、互換公開 module の公開面を検証する。indexing builder の挙動や互換 API を変更・レビューするときのテスト入口となる。

## Read this when
- indexing index entry builder の model・reasoning・file access・preflight 設定を確認するとき
- index entry 用 Structured Output schema の semantic 配列制約を変更または検証するとき
- 対象本文を prompt に埋め込む際のコードフェンス境界や互換 module の公開面を確認するとき

## Do not read this when
- index entry builder の正本仕様や prompt の設計意図を確認する場合は、対応する oracle の実装・schema・prompt standard を直接読むとき
- indexing 以外の builder や、テスト実行方法だけを確認するとき

## hash
- d65aa56854587a062111b34d78528a99c3d64edb15fcc1a3a348f27a427d8a01

# `test_acp_builder_oracle_review_parameters.py`

## Summary
- oracle review ACP builder 群の parameter、Structured Output schema、公開 builder 名、共有 review 規範、および動的 prompt の code fence 保護を回帰検証するテスト。review builder の互換契約や入力保持、schema 一致、model・reasoning・file access 設定を確認する入口である。

## Read this when
- oracle review builder の parameter 設定、schema、公開面、canonical builder との互換性を検証または変更するとき
- review builder が動的入力を prompt に埋め込む処理や nested code fence 保護を調査するとき
- review 所見の共有判定規範や validation・merge・enumeration の回帰を確認するとき

## Do not read this when
- review builder の実装そのものを変更・調査するときは、対応する oracle または realization implementation を直接読む
- review builder 以外の ACP builder や一般的なテスト実行方法だけを確認するとき
- oracle review の schema 定義自体を確認するときは、対応する oracle schema を直接読む

## hash
- 46d364d500e788424b82fe992a3a3079e7e3c45284c5272125c5a2299cce7407

# `test_acp_builder_session_join_parameters.py`

## Summary
- session join の conflict resolution builder に関するテスト。公開 export の限定、repo write 権限・モデル・推論設定・prompt 内容などの生成契約、および競合パス内の三連バッククォートを安全に埋め込む処理を検証する。対応する builder 実装の挙動を確認したいときの入口。

## Read this when
- session join の conflict resolution パラメータ生成を変更・レビューするとき
- conflict resolution builder の公開 API、権限設定、prompt 構造、パス埋め込みの契約を確認するとき

## Do not read this when
- session join 以外の builder の契約を確認するとき
- conflict resolution builder の実装詳細そのものを調査するときは、対応する正本または実装を直接読む

## hash
- 1ce9c852ebe12b5de8c5115cf47256dc5b2d7d081a0c8b75ac4aa0eb05e3e050

# `test_acp_builder_tui_parameters.py`

## Summary
- TUI 起動 builder の parameter 生成を検証するテスト。固定された agent call 種別、モデル、推論設定、ファイルアクセスモード、作業ディレクトリ、indexing preflight、および生成 prompt の規範参照と元 prompt の保持を確認する。併せて、互換 module の公開 API が現行 builder のみに限定されることを検証する。TUI 起動 parameter やその公開面の挙動を変更・調査するときのテスト入口。

## Read this when
- TUI 起動 builder が固定 parameter または prompt を正しく構成するか確認するとき
- TUI 起動用互換 module の公開 export を変更・調査するとき
- 関連する builder 実装の変更が既存の prompt 規範参照や parameter 契約に与える影響を確認するとき

## Do not read this when
- TUI 以外の builder の parameter を調査するとき
- builder 実装そのものの責務や正本仕様を確認するときは、対応する実装または oracle を直接読む
- 一般的な TUI 表示・操作のテストを調査するとき

## hash
- ac22c83af87a4bb1c1d9269a739a27fe69d0c8dda7e34dfbe96c3f61438e1baa

# `test_basic_runtime.py`

## Summary
- Root/worktree と path model の runtime 契約を検証するテスト。root placeholder の解決、repo/work/run root の区別、並列 call と cwd の分離、memo 判定、managed worktree の作成・検索・削除におけるパス検証と symlink・未登録・置換状態の拒否を扱う。

## Read this when
- path model、root placeholder、repo root/work root/run root の挙動を変更・調査するとき
- AgentCallPathContext、pushd、worktree の作成・検索・削除、managed path の安全性を変更・調査するとき
- runtime の並列実行、相対 cwd、symlink、Git global config への依存を検証するとき

## Do not read this when
- path model や runtime の root/worktree 契約に関係しない機能を変更・調査するとき
- CLI 出力、branch lifecycle、個別コマンドの業務ロジックだけを確認するとき

## hash
- dc05723bfe22124c0e55a3aec5f678a48667537e04c5a0faa0ce971ea8b235f8

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
- TUI 起動直前の CLI 前処理と、その外部挙動を検証するテスト群。
- エディタ入力の正本初期値、timestamp 衝突時の保持、skeleton のプレースホルダー制約を扱う。
- 編集済み prompt による Codex TUI の直接起動、linked worktree での prompt・agent call context・ログ配置、`.cmoc` ignore の保証を検証する。

## Read this when
- TUI サブコマンドの起動前処理や、エディタ編集後の prompt からの直接起動を確認・変更するとき
- prompt editor input の timestamp 衝突、skeleton 検証、編集前後の prompt 内容を検証するとき
- linked worktree におけるログ配置、起動 context、repository と worktree の `.cmoc` ignore を確認するとき

## Do not read this when
- TUI 前処理ではなく prompt 編集や TUI 起動の実装詳細を調べるときは、対応する正本仕様または実装ファイルを直接読む
- 他の CLI サブコマンド、一般的な git 操作、または TUI 起動後の Codex 実行を調べるとき

## hash
- 5ee6c662797c5659acfb9fea23cc960cdd7eb2d826719780e23cc533a3f569b0

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
- Codex CLI 実行ランタイムと、その設定・結果処理の契約を検証するテスト群。
- argv、stdin、sandbox、approval override、作業ディレクトリ、出力ログ、invalid UTF-8、Codex HOME の分離を扱う。
- 汎用 model provider の override が組み込み local provider 用フラグなしで渡されることも検証する。

## Read this when
- Codex 実行ラッパーの CLI 引数、stdin、sandbox、approval、作業ディレクトリ、出力ログ、結果解析の挙動を確認・変更・回帰検証する場合
- Codex の model provider override や Codex HOME に設定ファイルを生成しない契約を確認する場合

## Do not read this when
- Codex 実行ランタイムの契約ではなく、共通テスト helper、リポジトリ生成 helper、または個別の設定クラスの実装を直接調べる場合
- 対象が検証する CLI 契約を使わず、別の実装・仕様・テスト対象だけを確認すればよい場合

## hash
- 24bf1bf51545e110332d1cc8c6336a9c3dc9ac5c9214ff805b89c90161b83802

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
- Codex quota exceeded 後の probe・待機・resume・再実行を検証する回帰テスト群。quota probe の構築、session ID 復元、共有 probe、retry 状態、ログ・標準出力・CODEX_HOME・cwd、失敗伝播、並行呼び出しを一体として扱い、Codex exec の quota 復帰挙動を確認する入口。

## Read this when
- Codex exec の quota 超過後の待機、quota availability probe、resume または同一 prompt の再実行を変更・調査するとき
- quota retry の session ID、probe の失敗処理、poll 上限、capacity retry、並行呼び出しの挙動を検証するとき
- Codex 呼び出しログ、subcommand log、probe の JSONL 出力、CODEX_HOME や Codex cwd の記録に関する回帰を確認するとき

## Do not read this when
- quota retry や Codex exec の復帰制御に関係せず、通常の Codex 実行、別の subcommand、または probe adapter 単体の実装だけを調査するとき
- 対象の具体的な実装責務や正本仕様を確認する必要があるときは、このテストではなく quota retry の実装または codex exec の正本仕様を直接読むとき

## hash
- 48eea6302eabb238b2ace686a8fbf005902d7d67bf9339f42d6381ec73c4d322

# `test_codex_runtime_retry.py`

## Summary
- Codex exec の再試行・失敗処理を、fake subprocess の外部挙動として検証するテスト群。Structured Output の補正、schema 検証、capacity retry、JSONL error、中断、retry 上限、成果物差分保持、共有 call log と subcommand event を扱う。Codex 実行制御やログ契約の変更時に、同じ状態機械の分岐を一続きの文脈で確認する入口となる。

## Read this when
- Codex CLI 実行の retry 状態、subprocess 呼び出し回数、Structured Output 補正、capacity error、未知の JSONL error、中断処理を変更または検証するとき。
- Codex call log、subcommand event、retry 上限・backoff、補正時の session 継続や成果物差分保持の挙動を確認するとき。

## Do not read this when
- Codex exec の通常成功経路だけを確認する場合は、成功経路を直接扱う実装やテストを読む。
- ログ出力全般の仕様を確認するだけの場合は、共有ログ仕様の正本を直接読む。
- Codex exec 以外の subprocess や retry 機構を変更する場合は、このテストを起点にせず対象機能の直接の実装・テストを読む。

## hash
- 26441a62c170af68cead1933f16fda8daba140c589bbbd631c02fe817149a85b

# `test_codex_runtime_subprocess.py`

## Summary
- Codex subprocess と run process の追跡・停止・cleanup に関するテスト群。pidfd、process group、PID 再利用、signal 処理、tracking file の妥当性、不正状態や cleanup 失敗時の fail-closed 動作を検証する。関連する runtime 実装の挙動を確認するための realization test の入口。

## Read this when
- Codex subprocess の起動・追跡・signal 配信・process group cleanup を変更または調査するとき
- run process identity、tracking file、pidfd、PID/PGID 再利用時の安全な停止処理を変更または検証するとき
- editing run の cleanup 仕様に対する runtime 実装のテストカバレッジを確認するとき

## Do not read this when
- Codex subprocess や run process の停止・追跡処理に関係しないテストや実装を扱うとき
- tracking file の通常の読み書き仕様だけを確認する場合は、まず runtime 実装または対応する oracle 仕様を直接読むとき

## hash
- fd2e438163940497e1056974ac1091294881c638634f3c896954394262805014

# `test_codex_runtime_tui.py`

## Summary
- `run_codex_tui` の実行契約を検証するテスト群。prompt の読み込みとファイルアクセスモード、Codex CLI の作業ディレクトリ・引数、成功／失敗時の call log・サブコマンドイベント・コンソール要約を扱う。

## Read this when
- TUI 呼び出しで、完成済み prompt、リポジトリの linked worktree、アクセスモード、CLI 引数が期待どおり維持されることを確認したいとき
- Codex CLI の正常終了、非 0 終了、CLI 不在、KeyboardInterrupt に対するエラー処理とログ記録を確認したいとき
- TUI call log の timestamp 衝突時の保持や、サブコマンドログとの対応を確認したいとき

## Do not read this when
- Codex TUI の実装詳細や正本仕様を確認したいときは、対応する runtime 実装または oracle 文書を直接読む
- TUI ではない Codex 実行経路や、一般的な Git・テストヘルパーの挙動だけを確認したいとき

## hash
- ccd887bb5605fd77e7e7033d089a14e3174a148c8cd12b5e169062bf88eac467

# `test_doctor_cli.py`

## Summary
- doctor preprocess の共有 lifecycle を、CLI と直接呼び出しの両方で検証する統合テスト。`.cmoc/gu` の ignore、`.agents`、config、refactor state の修復順序と生成・追跡、reporter の利用不能時や予期しない失敗時の挙動、共有 doctor lock の待機を扱う。さらに、修復 commit が既存の staged index、unstaged 差分、index flag、intent-to-add、rename、削除を保持し、linked worktree と repository root の修復範囲を分離する契約を確認する。doctor preprocess の外部契約と Git index 保全を調査・変更するときの入口であり、個別の実装詳細や単一機能のテストだけを確認する場合は、対応する実装またはより限定的なテストへ直接進む。

## Read this when
- doctor preprocess の CLI または直接呼び出しにおける修復 lifecycle を確認するとき
- `.cmoc/gu`、`.agents`、config、refactor state、reporter の修復・失敗時挙動を一続きの外部契約として検証するとき
- doctor の修復 commit が既存の Git index、staged/unstaged 差分、index flag、intent-to-add、rename、削除を保持することを確認するとき
- repository root と linked worktree の修復責務や共有 doctor lock の動作を確認するとき

## Do not read this when
- doctor preprocess の外部挙動や Git index 保全を扱わず、実装コードや単一の補助 fixture だけを確認するとき
- reporter 単体、config 同期単体、refactor state 単体など、doctor preprocess 全体の lifecycle を必要としない検証を読むとき

## hash
- 2ecafae2ddddae65820ad786a77f31ee77da6ce3a9f708555cb740fd751b0873

# `test_editing_run_cli.py`

## Summary
- workload fork と共通 run join/abandon の統合 realization test。editing run の session state、run worktree、fork report、Codex child tracking、INDEX 更新、merge、cleanup、rollback、process interruption など、apply/refactor fork から run lifecycle 完了までの外部挙動を検証する。
- apply と refactor が共有する lifecycle fixture・branch・state 遷移を一続きで扱い、想定外差分、managed file、agent commit、遅延処理、rename/delete、report 保存、失敗時の resource 保持と recovery も対象にする。

## Read this when
- realization apply/refactor fork と run join/abandon の統合 lifecycle が正しく連携するか確認するとき。
- run state、worktree/branch cleanup、Codex process tracking、INDEX refresh、rollback、merge conflict、report の失敗時挙動を変更・調査するとき。
- agent が作成した差分や commit、user interruption、process tracking 異常、未解決 refactor finding の扱いを検証するとき。

## Do not read this when
- 単一の apply、refactor、join、abandon 実装の詳細だけを確認すれば足り、共通 lifecycle の統合挙動を調べないとき。
- 通知仕様そのもの、正本 app specification、または INDEX 生成ロジック単体の仕様を確認するときは、それぞれの oracle・実装・専用 test へ直接進む。
- テスト共通 helper や個別 command の単純な入出力だけを確認し、この統合 test の lifecycle 境界に関係しないとき。

## hash
- ddc84fc2bbf0b686ec5c51ec179ba4a848fb90a42c8306c1d4f4d5a3b1ad2aae

# `test_feedback.py`

## Summary
- feedback の reporter、collector、observation store、report cut、verification、active state、atomic publication、cleanup を同一 fixture で検証する統合テスト群。
- 正常 publication だけでなく、重複排除、閾値、fingerprint、path 境界、secret masking、不正 artifact、ユーザー中断、再開、部分 cleanup、active state の整合性を確認する入口。

## Read this when
- feedback の raw observation 受理から active issue・machine aggregate への集約、verification、report publication、cleanup の外部挙動を変更・検証するとき
- feedback report の中断・不完全・再開処理、atomic publication、checkpoint、current pointer、generation artifact の整合性を確認するとき
- agent-facing reporter の MCP discovery・collector 転送、schema validation、rate limit、context validation、path boundary、secret masking を確認するとき

## Do not read this when
- feedback の正本仕様や実装 prompt builder 自体を確認することが目的で、外部挙動をテストケースから追う必要がないとき
- feedback report と observation lifecycle に関係しない CLI、session、一般的な test infrastructure の作業をするとき

## hash
- bfd6ea4bb4e1ed2a005e78cdaf724936ceb846c196c5fbff05d1a8e9c96f66ea

# `test_file_inventory.py`

## Summary
- Git 管理下の full-tree 列挙機能を検証するテスト。除外境界、nested repository、ignore source、symlink・FIFO・デバイス等の非通常ファイル、linked worktree、単一パス分類、候補数増加時の Git 処理量を扱う。runtime_git の列挙・分類ロジックや refactor state 同期を変更・検証する際の挙動テスト入口となる。

## Read this when
- oracle・realization ファイルのインベントリ列挙や Git ignore 判定を変更するとき
- 除外ディレクトリ、nested repository、linked worktree、ignore source の扱いを確認するとき
- symlink や FIFO など非通常ファイルの安全な拒否、および列挙処理量の回帰を検証するとき
- refactor state の同期が列挙結果と SHA 更新に追随することを確認するとき

## Do not read this when
- インベントリ列挙や Git ignore・repository 境界に関係しない機能を変更・調査するとき
- refactor state の保存形式だけを扱い、ファイル列挙結果との連携を確認する必要がないとき
- 単一パス分類や linked worktree、特殊ファイルの挙動を直接対象としない通常のテスト実行だけを行うとき

## hash
- 462bacfc2c8ca285fb9e70845896fc12db7249bc3fa6253acc21ff266b4aed69

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
- `commons.indexing` の INDEX entry 生成・解析・更新と directory traversal を直接検証するテスト群。入力検証、hash による entry 再利用・再生成、空ディレクトリや特殊ファイル・symlink の扱い、安定した描画順、並列更新、logger の伝播、lock の共有をまとめて扱う indexing runtime 回帰の入口。

## Read this when
- INDEX entry の render・parse・hash・更新処理を変更または調査するとき
- ディレクトリ走査、symlink cycle、特殊ファイル、INDEX.md symlink の安全な置換を確認するとき
- INDEX 更新の並列実行、cwd lock、linked worktree 間 lock、Codex worker のログ伝播を確認するとき

## Do not read this when
- CLI lifecycle 自体の挙動だけを調査するときは、CLI の直接テストを読む
- indexing の正本仕様や Structured Output schema を確認するときは、参照されている oracle 文書・定義を直接読む

## hash
- f0d124e958bba06428dc11e75bb587b2d51a3b3f9645587f0a1fde6e2202434b

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
- `cmoc oracle edit` の main worktree TUI 制御を検証する pytest テストです。doctor 前処理、プロンプト編集・確定、indexing preflight、起動前提検査、TUI 実行順序と引数、編集結果・既存差分・session state の保持、TUI 失敗時の終了、および main worktree／session 状態の前提違反を扱います。oracle edit の実装や仕様を変更・検証するときに、対応する外部挙動のテスト入口として読みます。

## Read this when
- `cmoc oracle edit` の TUI 起動フロー、起動前提、終了コード、生成 prompt、または既存の Git 差分・session state 保持を変更・検証するとき。
- oracle edit の処理順序や runtime TUI への引数、doctor・indexing preflight 連携をテストで確認するとき。

## Do not read this when
- oracle edit の実装詳細や正本仕様そのものを確認したい場合は、まず対応する oracle 仕様または実装を直接読みます。
- oracle edit と無関係な CLI サブコマンド、一般的なテスト共通処理、他の TUI の挙動だけを調べる場合。

## hash
- bd0d5243ac1dacc1392025159ec77eff07c538ca28c79a77eb550f6b955ab212

# `test_oracle_investigation_cli.py`

## Summary
- `cmoc oracle investigation` の CLI 起動契約を検証するテスト。session なしの main worktree で起動できること、doctor preprocess から TUI 起動までの処理順序、完全 prompt の確定、固定された AgentCallParameter、および builder の公開 API を扱う。oracle investigation の起動経路と対応する realization adapter のテスト入口となる。

## Read this when
- `oracle investigation` サブコマンドの起動前処理、prompt editor 入力、完全 prompt 確定、TUI 起動順序を変更または検証するとき
- `build_oracle_investigation_launch_tui_parameter` の返却パラメータや公開シンボルを変更するとき
- main worktree で session 前提なしに `oracle investigation` を起動できる条件を確認するとき

## Do not read this when
- oracle investigation の prompt 内容や TUI パラメータの正本仕様だけを確認する場合は、対応する oracle 文書・oracle 実装を直接読む
- 他のサブコマンドの起動条件や builder 公開 API を確認する場合は、このテストではなく対象サブコマンドのテストを読む

## hash
- 5890c6ba24dd8dd612dc1afd541f60ec34cc81a90553c42da2f032fef0774b25

# `test_oracle_review_loop.py`

## Summary
- oracle review の finding loop 全体を検証する回帰テスト。finding の列挙、対象 oracle ごとの関連 finding の受け渡し、隔離 worktree の利用、merge、challenger/advocate による理由検証、judge、割り込み時の部分結果保持、merge 出力補正失敗の伝播を一つのテスト群で扱う。
- oracle review の review round と fake Codex call 列を追跡しながら、各段階の Structured Output、prompt context、finding の状態遷移およびエラー契約を検証する下位テストの入口。

## Read this when
- oracle review の finding 列挙・merge・理由検証・judgement の連携を変更または調査するとき
- review worktree への call 再束縛、関連 finding の絞り込み、同一 round の理由受け渡しを確認するとき
- KeyboardInterrupt 時の部分結果や merge の postcondition・補正失敗の挙動を確認するとき

## Do not read this when
- oracle review の実装詳細そのものを確認する場合は、review loop の実装と oracle review の正本仕様を直接読むとき
- oracle review 以外のサブコマンド、または単一の Structured Output schema の仕様だけを確認する場合

## hash
- 3639d3450e742c0fedafe34db8b1ecd418e5e2b611bb230a0d570c522c3f7f8d

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
- 日本語の pytest テストファイルとして、oracle review の隔離 run lifecycle、linked/snapshot worktree、割り込み時の cleanup、INDEX.md の preflight・差分検証・merge、競合復旧、cleanup 失敗報告を検証する回帰テスト群を収録する。oracle review の review worktree と INDEX 統合に関する挙動を確認する入口であり、個別の実装や仕様本文ではなく、この領域の回帰テストを追加・変更・調査するときに読む。

## Read this when
- oracle review の linked worktree、snapshot commit、run target 衝突、worktree/branch cleanup、割り込み・例外処理を検証するテストを確認するとき。
- review worktree で生成された INDEX.md の preflight、許可された差分、session への merge、INDEX 競合解決を検証するテストを確認するとき。
- oracle review の worktree lifecycle や INDEX 統合に関する回帰テストの失敗原因を調査するとき。

## Do not read this when
- oracle review の実装仕様や run isolation・branch model・indexing の正本を確認することが目的のときは、参照先として明記された oracle 文書を直接読む。
- oracle review 以外のサブコマンドや、一般的な pytest 実行方法・共通テスト支援の確認だけが目的のとき。
- INDEX.md の生成ルールそのものを確認するだけで、oracle review における生成・差分検証・merge の回帰挙動を調べないとき。

## hash
- 7c1c90429baf12948bd6fc679e0e9620bf7f39a48294f8899addb0e7bb0ae5ec

# `test_packaged_import.py`

## Summary
- `packaged layout` に隔離したソースツリーをコピーし、外部 site-packages やユーザー設定の影響を排除した Python 実行で import 境界を検証するテスト群。oracle review builder、oracle edit/editor 入力、ACP basic の canonical 定義再公開、config の公開面を対象とし、packaging 設定・出力契約・`__all__`・module namespace・正本参照を確認する。

## Read this when
- packaged layout での Python import、setuptools の package 配置、oracle/realization 間の公開 import 境界を変更または検証するとき
- oracle review の enumerate finding、oracle edit の launch TUI、ACP basic、config の公開 API が隔離環境でも正本と出力契約を満たすか確認するとき

## Do not read this when
- 通常の機能実装や単体ロジックの挙動だけを確認する場合
- 対象の公開 import、packaging 設定、隔離 packaged layout、またはここで扱う出力・再公開契約に関係しないテストを読む場合

## hash
- 381953699b0fc8d6f76afd61812604d09137d904cd4600a156a60975601949da

# `test_production_cli.py`

## Summary
- 独立 process、実 Codex CLI、実推論、PTY を用いて、利用者向け CLI の全末端サブコマンドが本番経路で完了することを検証する受け入れ試験。
- 終了 code、report・state・Git の状態、Codex call log、TUI の応答完了と終了操作を確認し、LLM の回答品質自体は判定しない。
- 非対話サブコマンドと TUI サブコマンドの共通隔離環境、実行条件、外部状態検証を一続きの試験として扱う。

## Read this when
- CLI の末端サブコマンドを追加・変更し、利用者向け本番経路での代表正常系を確認するとき。
- 実 Codex CLI や実推論を含む production-path integration test の実行条件、隔離環境、call log 検証を確認するとき。
- 非対話 command の終了状態・report・session/run state・Git 状態、または TUI の PTY 応答完了と終了処理を検証するとき。

## Do not read this when
- LLM の回答内容や品質そのものを評価するとき。
- 単一サブコマンド内部の実装詳細や、実推論を使わない単体テストの仕様を確認するときは、対象サブコマンドの実装・専用テストを直接読む。
- Codex CLI を使わない通常の CLI 操作や、production path 全体を対象としない局所的な状態検証だけを行うとき。

## hash
- d2c43aea2340d16947623881cde5333ff689edf15a0b4257fffaef7afd884c10

# `test_prompt_parts.py`

## Summary
- 標準 prompt parts の render 結果と complete prompt の構成・placeholder 展開を検証する回帰テスト群。各標準規則の単体 render、選択的な注入、既定での省略、file access mode 別の内容、feedback instruction の一意性、placeholder の統合・競合検出を扱う。prompt builder の挙動を変更・検証する際のテスト入口であり、標準規則本文や prompt builder 実装そのものを読む代替ではない。

## Read this when
- prompt builder の標準 prompt parts または complete prompt の構成を変更し、既存の render 内容・注入条件・既定値への影響を確認するとき
- 標準規則の追加・分離・選択注入、file access mode、placeholder 展開や競合検出の回帰を調査するとき
- prompt builder 関連のテスト実行箇所を特定するとき

## Do not read this when
- 一般的な INDEX 案内文書の構成や prompt 標準の正本を確認したいとき
- prompt builder と無関係なテストや、単一の標準規則の詳細仕様だけを確認する場合
- 実装の責務や設計判断を確認する場合

## hash
- 0fa041092ec246271b4434a5135e1f2ccb0fe05fe0440bcb3d795a9525f44e93

# `test_runtime_cli.py`

## Summary
- CLI の error、log、preflight、completion 境界を検証する統合テスト。共通 runner と work root、subcommand event、終了処理を共有する外部契約を一箇所で扱い、CLI lifecycle 全体の回帰検証の入口になる。
- duration 表示、サブコマンドログの衝突・並列記録、error report、KeyboardInterrupt、terminal notification、doctor preprocess、work root 制約、引数解析、shell completion probe、pre-log check を検証する。

## Read this when
- CLI lifecycle の共通 runner、終了コード、command event、サブコマンドログ、cleanup、terminal notification の挙動を変更・検証するとき
- CLI error report の stdout 出力、Click 引数解析エラー、CmocError の Markdown 整形、KeyboardInterrupt の扱いを確認するとき
- doctor preprocess、pre-log check、current work root 制約、shell completion probe の副作用境界を確認するとき
- CLI の duration 表示や SubcommandLogger の timestamp 衝突・並列 worker 記録を変更・検証するとき

## Do not read this when
- 個別機能の実装詳細だけを確認する場合は、対応する runtime 実装を直接読むとき
- error、log、preflight、completion の外部契約に関係しないサブコマンドやデータ処理を調査するとき
- テスト仕様ではなく、CLI の正本仕様を確認する場合は参照されている oracle 文書を直接読むとき
- completion の補完候補生成そのものだけを確認する場合は、completion 実装または正本仕様を直接読むとき

## hash
- d2f55368451952d71aeed1380c33c4ef95186bc72282df7c71c7ce5d85ff83c7

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
- Codex argv 構築と subprocess 環境、schema 一時保存、JSON 出力読込を検証する realization test。file access mode ごとの sandbox、model/provider 上書き、TOML エンコード、通知 callback、feedback context の扱いと、異常系での起動前検証を対象とする。runtime Codex profile の実装を変更・レビューするときの挙動確認入口。

## Read this when
- Codex の sandbox、model、provider、通知、feedback MCP 設定を argv または環境へ変換する処理を変更するとき。
- schema のハッシュ保存や Codex 出力 JSON の読込処理を変更するとき。
- Codex 起動前の不正な file access mode や未定義 provider の検証を確認するとき。

## Do not read this when
- Codex runtime profile の実装・契約を変更せず、他の agent call や CLI 引数変換とは無関係なテストを扱うとき。
- schema 検証そのものや一般的な JSON schema の互換性を確認するときは、schema 専用の仕様・テストを直接読む。

## hash
- 868fe3c3f60b14fda88f4809f6307a3b8ebd08d4d0d3a33b5977689783c11bc1

# `test_runtime_config.py`

## Summary
- CmocConfig の既定値、JSON 化時のメンバー順、設定ファイルの読み書き、永続化境界の安全性を検証するテスト。
- config_from_dict による codex・oracle_review 各 section、model provider、model 定義、reasoning effort、整数項目、provider-local 値の入力検証とエラー変換を検証する。
- 設定値の読み込み・書き出し時に、不正 JSON、非通常ファイル、named pipe、symlink、UTF-8 非互換値を安全に拒否する挙動を確認する。

## Read this when
- cmoc config の既定値、永続化形式、設定項目の入力検証を変更またはレビューするとき。
- config_from_dict、config_to_dict、load_config、write_config、render_error の挙動を変更または検証するとき。
- 設定ファイルのパス安全性や不正値に対する CmocError の内容を確認するとき。

## Do not read this when
- 設定の実装詳細そのものを確認する場合は、まず {{work-root}}/src/config/cmoc_config.py または {{work-root}}/src/cmoc_runtime.py を読む。
- CmocConfig の正本仕様やエラー方針を確認する場合は、テストではなく {{work-root}}/oracle/src/oracle/other/cmoc_config.py と {{work-root}}/oracle/doc/app_spec/error_handling.md を読む。
- このテストが対象としない CLI 操作、oracle review の制御、モデル実行処理だけを調べる場合。

## hash
- 9c25d2d46e3af05c7f5c2ae6c6cf2eb7c76a518183bb7ed39ac3dad58a0a2cd4

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
- Git ignore の安全な更新と判定を検証するテスト。cmoc 用 ignore パターンの追加、index-aware／untracked-aware な判定、特殊ファイル・symlink・判定失敗時のエラー処理を対象とする。runtime の Git ignore 実装やその回帰を確認する入口。

## Read this when
- Git ignore パターンの追加・更新処理を変更または検証するとき
- is_git_ignored、is_untracked_git_ignored、ensure_cmoc_ignored、ensure_cmoc_ignored_in_exclude の挙動を確認するとき
- 特殊ファイル、symlink、global excludes、check-ignore 失敗時の安全性を扱うとき

## Do not read this when
- Git ignore 以外の runtime 機能を扱うとき
- テスト対象の実装や仕様を直接確認したいときは、runtime 実装または根拠として示された仕様・プロンプト定義を先に読むべき場合

## hash
- d8841b7ae36f232f45c82847ea7fb9f8fda21bf534bbdba559959193d394a62d

# `test_runtime_refactor.py`

## Summary
- realization refactor の永続 state 同期・検証・target 選択を検証するテスト。oracle と realization の正確な file 集合、履歴保持、変更時の再調査化、優先順位付き選択を扱う。path escape、非通常 file、symlink、gitlink、特殊 path、state schema・UTF-8・timestamp などの安全性と入力拒否も確認する。

## Read this when
- refactor state の同期、読み書き、schema 検証、調査履歴の扱いを変更または確認するとき
- oracle/realization file の分類規則や refactor target の選択ロジックを変更または検証するとき
- state path や repository path の symlink・非通常 file・path escape 対策を確認するとき

## Do not read this when
- refactor 以外の runtime 機能や、state・target 選択に関係しないテストを扱うとき
- 正本仕様の内容を確認することが目的のときは、まず参照先として示された oracle 仕様を読む

## hash
- 8f31764a0c1fd5af9a11d8cebcc100c7cddcb5d969b2b4e8e4230522032afe8a

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
- session fork・join・abandon の CLI 外部挙動をまとめて検証する回帰テスト。session branch と永続 state の生成・遷移・cleanup・rollback、linked worktree、dirty worktree 拒否、preprocess、conflict 解消を扱う。session ライフサイクルに関するテストの入口。

## Read this when
- session fork、join、abandon の外部挙動を確認するとき
- session branch、session state、linked worktree のライフサイクルや cleanup・rollback を検証するとき
- session join の conflict 解消、変更範囲検証、出力先、dirty worktree 拒否を確認するとき

## Do not read this when
- session サブコマンドの実装や正本仕様を確認するときは、対応する src または参照された oracle 文書を直接読む
- session 以外の CLI 挙動や一般的な Git ヘルパーを確認するとき

## hash
- bdbe6b1446a4386312f1c290558c4fdc5be5b976d8d933aea7673fa772406db6

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
- StructDoc の Markdown renderer に対する単体テスト。連続空行の縮約、コードブロック内の整形、StructBlock の互換公開と埋め込み、無効な参照・重複 block ID の拒否を検証する。renderer の整形挙動や参照解決のテストへ進む入口。

## Read this when
- Markdown renderer の空行処理やコードブロック出力を変更・確認するとき
- StructBlock の再公開、描画済み Markdown の埋め込み、cmoc_ref の検証挙動を変更・確認するとき
- StructDoc renderer の関連テストを追加・修正するとき

## Do not read this when
- StructDoc のモデル定義や renderer 本体の実装を直接調査する場合
- Markdown 以外の出力形式や、renderer と無関係な CLI 挙動を調査する場合

## hash
- d83e1e717144f9f42e6e9e616890340046a41f72d404f732b73314c152ad921c

# `test_windows_toast.py`

## Summary
- Windows toast の終端通知内容、PowerShell transport の安全な JSON/stdin 受け渡し、通知失敗の非伝播、Codex callback の turn 単位重複排除、TUI callback の一時 state と standalone 実行を検証するテストスイート。これらの通知・callback 境界や `runtime_windows_toast` の変更を確認するときの入口。

## Read this when
- Windows toast の表示内容や秘密情報の非露出を変更・検証するとき
- PowerShell transport の引数、標準入力、timeout、shell 無効化を確認するとき
- Codex の turn 完了 callback の重複排除や本文の扱いを調査するとき
- TUI callback の invocation-local state、cleanup、実行コマンド互換性を確認するとき

## Do not read this when
- toast や Codex callback の実装詳細を直接確認する場合
- Windows toast と無関係なテストや CLI 挙動を調査する場合

## hash
- 853e8c0b3d5b0b9d70d4f38b85db12ae02d77d839fb21573f6f7d7a1c8a89a01
