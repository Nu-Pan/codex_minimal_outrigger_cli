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
- 対象は indexing index entry builder のパラメータ、Structured Output schema、および互換公開面を検証するテスト。minimum モデル・low reasoning・readonly 実行設定、semantic 配列の非空制約、正本 builder との prompt/parameter 互換性、公開 API の限定を扱う。
- indexing builder の実装や正本仕様を変更・検証する際のテスト入口であり、個別の prompt 内容や schema 定義そのものを確認したい場合は対応する正本・実装へ直接進む。

## Read this when
- indexing index entry builder の実行パラメータ選択を変更または検証するとき
- index entry 用 Structured Output schema の必須要件や semantic 配列の最小件数を変更または検証するとき
- 互換 builder が正本 builder と同一の parameter を返すこと、または module の公開面を確認するとき

## Do not read this when
- index entry builder 以外の ACP builder を扱うとき
- 具体的な prompt の仕様、schema の全体定義、または builder の実装詳細を直接確認する必要があるとき
- テスト実行方法や一般的な test fixture の規約だけを確認したいとき

## hash
- e6fce1fb902e52d5a22f1412f7fb05e61e96c8ec525174ae116f051749835eef

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
- 公開 CLI の末端コマンド集合が正本仕様の列挙と一致すること、および CLI ヘルプが Typer/Click の互換性エラーなく描画されることを検証するテスト。feedback report がサブコマンド固有オプションを公開しないことも確認する。

## Read this when
- 公開 CLI のコマンド構成や末端コマンド集合が正本仕様と一致しているか確認するとき
- CLI ヘルプ描画時の Typer/Click 互換性を検証するとき
- feedback report の公開オプション有無を確認するとき

## Do not read this when
- 個別サブコマンドの詳細な挙動や引数仕様を確認するときは、列挙されている各サブコマンドの正本仕様を直接読む
- CLI 実装の変更箇所や一般的なテスト実行方法だけを確認するとき

## hash
- 2e841a9654e47e3e6d1ac2ab9362f5bee308af437118450c82e4fb744c3eb4ff

# `test_cli_tui.py`

## Summary
- TUI 起動直前の CLI 前処理に関する外部挙動を検証するテスト。プロンプトエディタ入力の初期値と timestamp 衝突、skeleton 検証、編集済み prompt による Codex TUI 起動、linked worktree での保存先、および `.cmoc` の ignore を扱う。TUI サブコマンドの前処理と起動経路を確認する入口であり、個別の prompt builder や runtime 実装の詳細を調べる前に読む。

## Read this when
- `tui` サブコマンドの起動前処理、エディタ入力、編集済み prompt、Codex TUI の直接起動の外部挙動を確認または変更するとき
- timestamp 衝突時の入力ファイル保持、prompt skeleton の placeholder 検証、または linked worktree におけるログ・prompt 保存先を確認するとき
- TUI 実行時の staged/unstaged 差分保持や `.cmoc` の git ignore 挙動を検証するとき

## Do not read this when
- prompt editor や prompt builder の単体実装だけを確認する場合は、対応する実装または oracle を直接読む
- TUI 以外のサブコマンドの外部挙動を確認する場合は、各サブコマンドのテストを読む
- 一般的な CLI 起動や git worktree の仕様だけを調べる場合は、このテストを入口にしない

## hash
- 13a18baef796e717056913606fbb12a5fcc15f265321cac14203033ac8c9f4fe

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
- Codex TUI 実行ラッパーのテスト入口。完成済み prompt の読み込み、作業ディレクトリ・sandbox・CLI 引数の制約、成功・CLI 不在・KeyboardInterrupt・非 0 終了時の call log／サブコマンドイベント／コンソール要約を検証する。TUI 実行時のアクセス境界やログ仕様のテストを追加・変更・調査するときに読む。

## Read this when
- Codex TUI の実行経路、prompt 読み込み、linked worktree 対応、CLI 呼び出し引数を検証するとき
- TUI 呼び出しの成功・失敗・割り込み時における call log、イベント、コンソール出力の挙動を確認するとき
- TUI 関連の realization test の要件や既存ケースを把握するとき

## Do not read this when
- Codex TUI の実装自体を変更・調査する場合は、まず対応する realization 実装と正本仕様を読む
- TUI 以外の Codex 実行経路、一般的なログ機構、別サブコマンドのテストだけを扱う場合
- テスト実行方法や開発環境の設定だけを確認する場合は、専用の開発ルールを直接読む

## hash
- 31cbc124383f272312f9699cd74e209aef041c0e04e316dbe39546d48a0d1540

# `test_doctor_cli.py`

## Summary
- doctor preprocess の共有 lifecycle を検証する統合テスト群。CLI と直接呼び出しの双方で、Git 状態・config・refactor state・共有 lock・reporter probe の挙動と、既存の staged index／unstaged 差分／index flags の保持を確認する。doctor preprocess の外部契約を調べる際のテスト側の入口。

## Read this when
- doctor preprocess の修復順序、修復対象、commit、lock 待機、割り込み伝播を変更・検証するとき
- doctor が既存の staged／unstaged Git 差分、rename、削除、index flags、intent-to-add を保持する挙動を調べるとき
- CLI 経由と直接呼び出しでの doctor preprocess の統合的な外部挙動を確認するとき

## Do not read this when
- doctor preprocess の実装詳細や正本仕様を確認することが目的の場合は、まず doctor の実装または参照される oracle 仕様を読むとき
- doctor preprocess と無関係な CLI サブコマンド、Git 補助 fixture、一般的な runtime doctor の単体挙動だけを調べるとき

## hash
- 45812bbb5addf62e1e60d970cfaf6458567b43e2722499bca0cf79efb3934cc0

# `test_editing_run_cli.py`

## Summary
- editing run の fork、run worktree、session state、fork report、join、abandon を横断する統合 realization test。
- apply/refactor の agent 境界、INDEX 更新、process tracking、rollback、commit、merge、cleanup、error・interrupt recovery など、共通 lifecycle の外部挙動を検証する。
- fork と join/abandon が共有する branch・state 遷移を一続きの fixture で検証するための、下位 lifecycle 実装テストへの入口。

## Read this when
- realization apply/refactor fork の lifecycle 挙動を変更・検証するとき
- run join または run abandon の state、worktree、branch cleanup、merge rollback を調査するとき
- Codex child process tracking、INDEX refresh、agent の予期しない差分・commit、report 生成を検証するとき
- editing run の中断・失敗・競合開始・復旧時の統合的な挙動を確認するとき

## Do not read this when
- 単一の lifecycle helper や subcommand 実装の詳細だけを調査する場合
- fork/join/abandon と無関係な CLI 機能や通常の unit test を確認する場合
- 正本仕様や通知仕様を確認する場合は、対応する oracle 文書を直接読むとき

## hash
- 6b79b9c581ca43b34d8799098cb0ce1c14ed1f537143f28558b3ff65c9126151

# `test_feedback.py`

## Summary
- feedback の agent-facing reporter、collector、raw observation、report cut、verification checkpoint、active state、atomic publication、cleanup を同一 fixture で検証するテスト群。pending observation が issue または bounded machine aggregate に集約され、publication 後に raw と一時 state が整理される外部挙動を確認する。

## Read this when
- feedback observation の受付・検証・秘匿化・冪等性を変更または調査するとき。
- feedback report の候補統合、verification、checkpoint 再開、atomic publication、current pointer、cleanup を変更または調査するとき。
- active state や report cut の破損検出、path/hash 整合性、未定義 artifact の扱いを確認するとき。
- reporter MCP tool の公開面、collector context、rate limit、KeyboardInterrupt の扱いを確認するとき。

## Do not read this when
- feedback の正本仕様や CLI の契約を確認することが目的で、実装挙動のテストケースを読む必要がないとき。
- feedback report 以外のサブコマンドや、単純な JSON schema 定義だけを変更・調査するとき。
- 既存テストの実行方法や品質ゲートだけを確認するときは、テスト実行手順の対象へ直接進む。

## hash
- 95333ba180f77743958859a29abcc792375989cce609bba8d359f61fa50268bb

# `test_file_inventory.py`

## Summary
- oracle と realization の full-tree ファイル列挙契約を検証する realization test。Git ignore、nested repository、除外境界、非通常ファイル・symlink、refactor state の同期と SHA 更新、Git 処理量の不変性を扱う。ファイルインベントリ実装や refactor state 同期の挙動を確認する際のテスト側の入口となる。

## Read this when
- oracle/realization ファイル列挙の対象範囲、Git ignore 判定、nested repository 境界、除外ディレクトリの扱いを変更または検証するとき
- 非通常ファイルや symlink の拒否条件を変更または検証するとき
- refactor state のエントリー同期やファイル SHA 更新の挙動を変更または検証するとき
- 候補ファイル数に対する Git 処理量や走査量の性能契約を確認するとき

## Do not read this when
- 列挙・分類・refactor state 同期の実装を変更する作業で、まず実装側の責務や正本仕様を確認すべきとき
- このファイルが検証する契約と無関係な CLI 機能や別のテスト領域を扱うとき

## hash
- 73fedc47743e84438f302419d6df21d41e75fe09aea6732b5d0eb95b24074db5

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
- 対象 oracle の review loop に対する回帰テストを一箇所で扱う。finding の対象別列挙、関連 finding の引き継ぎ、challenger/advocate の理由連携、merge の入力条件、judge 判定、割り込み時の部分結果保持、merge 失敗伝播を fake Codex call で検証する。
- oracle review の実装や正本仕様そのものではなく、review round と fake call 列の外部契約を検証する realization test への入口である。

## Read this when
- oracle review の finding 列挙・理由検証・merge・judge の回帰挙動を確認するとき
- oracle review の割り込み復旧、部分結果、隔離 worktree の call context、Structured Output の postcondition をテストするとき

## Do not read this when
- oracle review の仕様や設計意図を確認したいときは、列挙された oracle 文書を直接読む
- review loop の実装を変更・調査するときは、まず対応する src の実装とその INDEX.md を読む
- 一般的なテスト規約だけを確認したいときは、テスト規約の oracle 文書を直接読む

## hash
- 05cf957fd8fde8f2c786dacb0539b4c07e5e8e0fed6781e1527438aacba967b0

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
- oracle review の隔離 run と linked worktree lifecycle を検証する回帰テスト。snapshot commit からの fork、branch/worktree の衝突・中断・例外時 cleanup、merge と conflict 復旧、INDEX.md のみの差分検証・統合、preflight の path context、通知・report 出力を扱う。oracle review の実装や関連仕様のテスト入口として読む。

## Read this when
- oracle review の run worktree、session branch、snapshot fork、resource cleanup、merge lifecycle を変更・検証するとき
- oracle review における INDEX.md の生成・差分制約・session への統合や merge conflict 復旧を変更・検証するとき
- oracle review の中断時通知、error report、Codex structured output 呼び出し、preflight context の挙動を確認するとき

## Do not read this when
- oracle review と無関係な subcommand や一般的な worktree lifecycle の実装を扱うときは、対象実装または対応する仕様・テストを直接読む
- INDEX.md の通常の生成規則だけを確認する場合は、indexing の仕様や indexing 実装・専用テストを直接読む
- oracle review の所見判定ロジックだけを変更・検証し、worktree isolation、差分統合、cleanup の挙動に関係しないとき

## hash
- 3d7c4b9fa5d7957a25735741f62172f666799ecc9f8c8fc0595c786fa7ed229b

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
- 全末端サブコマンドを、独立プロセス・実 Codex CLI・実推論を用いた本番経路で検証する受け入れ試験。CLI の終了コード、report・state・Git 状態、Codex call log、TUI の応答完了と終了を確認し、LLM の回答品質自体は判定しない。非対話コマンドと PTY 上の TUI コマンドに共通する隔離環境・実行・観測用ハーネスを含む。

## Read this when
- CLI の公開末端サブコマンドを追加・変更し、本番経路での網羅的な実行検証を更新するとき
- 独立プロセス、実 Codex CLI、実 provider、Codex call log、永続 state、Git 状態を含む統合試験の挙動を確認するとき
- TUI コマンドの PTY 入出力、端末 capability query、応答完了判定、終了処理を調査するとき

## Do not read this when
- 単体テストや、実 Codex/provider を使わない決定論的な制御ロジックのテストだけを変更するとき
- サブコマンドの実装仕様や通常の CLI 挙動を確認したいときは、対象となる実装または対応する正本仕様を直接読む
- LLM の回答内容・品質そのものを評価するとき

## hash
- 9ef9aaa41e0e2b664db778876a6a2f19ff6c28907cc4811a82078a3a09b8f3ef

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
- CLI ライフサイクルの外部契約を検証する大規模な pytest モジュール。共通 runner と work root を介した duration 表示、サブコマンドログ、並列イベント、doctor/pre-log preflight、エラー report、終了コード、KeyboardInterrupt、Windows terminal 通知、CLI 引数解析、work root 制約、shell completion probe の挙動を扱う。CLI 実装や runtime の変更が、これらの境界条件に影響するときの主要な回帰検証入口である。

## Read this when
- CLI の error report、stdout/stderr 出力、終了コード、例外・Ctrl+C 処理を変更または検証するとき
- サブコマンド logger、command lifecycle event、並列 worker 記録、ログ flush、duration 表示を変更または検証するとき
- doctor preflight、pre-log check、work root 判定、worktree 上のログ保存先を変更または検証するとき
- shell completion probe の副作用抑制や CLI parser の公開 option 制約を変更または検証するとき
- 成功・失敗・中断時の terminal/toast 通知境界を変更または検証するとき

## Do not read this when
- CLI lifecycle、logging、preflight、completion、error handling のいずれも関係しない機能を変更または調査するとき
- 個別の実装詳細や正本仕様を確認することが目的で、対応する runtime 実装または oracle 文書を直接読むべきとき

## hash
- 6dd177f64da54ba4da157036ae58c68d1c3a8c7f90642ecfbf16b21aa770de46

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
- Git ignore の安全な更新・判定に関する runtime 機能を検証するテスト。cmoc 用 ignore パターンの追加、literal path の判定、check-ignore 失敗時のエラー化、.gitignore・info/exclude・global excludes の特殊ファイルや symlink に対する安全性、および既存の有効なパターンへの安定した追記を扱う。

## Read this when
- Git ignore 判定や cmoc 用 ignore 設定の実装を変更・レビューするとき
- `.gitignore`、Git の info/exclude、global excludes、symlink・特殊ファイルに対するエラー処理を検証するとき
- runtime の Git 操作に関するテストの期待挙動を確認するとき

## Do not read this when
- Git ignore や runtime Git 操作に関係しない機能を変更・調査するとき
- Git ignore の実装詳細そのものを確認する必要があり、対応する runtime 実装を直接読むべきとき
- doctor preprocess や editing run の仕様だけを確認する場合

## hash
- c1a0f125ced06cab999fea8e72d2c2183a5f9e4899d43cc88c3569ba09904709

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
- Windows toast 通知のテストで、terminal result の短い表示内容、PowerShell transport への安全な JSON 渡し、通知失敗の隔離、Codex callback の turn 単位重複排除、TUI callback state の invocation 内限定を検証する。Windows toast 実装の挙動変更や関連テストの意図を確認する入口。

## Read this when
- Windows toast の表示内容、transport の引数・入力形式、PowerShell 実行境界を変更または調査するとき
- Codex の agent-turn-complete callback、通知重複排除、callback state のライフサイクルを変更または調査するとき
- 通知が terminal result の処理や TUI invocation の終了後に影響しないことを検証するとき

## Do not read this when
- Windows toast や Codex callback の挙動に関係しないテスト・実装を扱うとき
- 通知仕様そのものを確認する必要があり、参照元の oracle 仕様を直接読むべきとき

## hash
- 8c868d432a6fbacdcfe191e01eff3c3a826d2a9198b30a28ba4d0220ea1656b2
