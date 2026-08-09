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
- Codex 実行関連テストで共有する最小のテストヘルパー群。テスト用ホーム環境、Structured Codex result double、AgentCallParameter、CLI 引数と設定 override の検査補助を提供し、runtime wrapper や TUI のテストから参照する入口となる。

## Read this when
- Codex 実行ラッパーまたは TUI のテストで、隔離した Codex 環境、既定パラメータ、結果 double、CLI override 引数の検証補助が必要なとき。

## Do not read this when
- 本番の Codex 実行処理や CLI override の仕様を確認したいときは、対応する実装または正本仕様を直接読む。
- この共通ヘルパーを利用しないテストや、Codex 実行と無関係なテストを調べるとき。

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
- editing run workload の canonical builder adapter を検証するテスト。apply builder が commit 範囲・raw diff・標準規則を prompt と実行設定へ反映し、refactor builder が canonical Structured Output schema、実行設定、決定論的事後条件を使うことを確認する。
- テスト用 linked worktree を隔離して作成し、raw diff 内の三連 backtick や prompt 境界風マーカーが外側の prompt 境界を壊さず保持されることも検証する。対応する builder 実装と oracle schema の挙動を確認する入口となる。

## Read this when
- apply または refactor の editing run builder の prompt 構成、実行パラメータ、Structured Output schema の利用を変更・検証するとき
- raw diff の埋め込み、prompt 境界のエスケープ、linked worktree 上での builder 動作を確認するとき
- 対応する canonical builder adapter や oracle schema の回帰テストを調査するとき

## Do not read this when
- builder 以外の ACP 実装や一般的な git worktree 操作だけを調査するとき
- Structured Output schema の正本内容そのものを変更・確認するときは、対応する oracle schema を直接読む
- prompt 標準規則の定義や realization の設計意図を確認するときは、対応する oracle 文書を直接読む

## hash
- 275dd9bf6d20cf16b1d14eef2d39e10d576a1cc6a0fe685cd7a9fcba7fde4504

# `test_acp_builder_indexing_parameters.py`

## Summary
- indexing の index entry builder に対するテストで、モデル・推論強度・ファイルアクセス権などの実行パラメータ、Structured Output schema の必須配列制約、対象本文中のコードフェンスやプレースホルダー風見出しの保持、互換モジュールの公開シンボルを検証する。index entry 生成パラメータやその公開面を変更・確認する際のテスト入口。

## Read this when
- index entry builder のパラメータ、Structured Output schema、プロンプト本文境界、互換モジュールの公開 API を変更または検証するとき
- indexing 関連のテスト失敗の原因を調査するとき

## Do not read this when
- index entry の文章生成ルール自体を確認したいときは、対応する oracle の実装・schema を直接読む
- indexing 以外の builder や一般的なテスト実行方法だけを確認したいとき

## hash
- 9ebfc98223d1b38c30d1e12a8f789d1d40fa1b70550dcb2114614d682bbb7833

# `test_acp_builder_oracle_review_parameters.py`

## Summary
- oracle review ACP builder 群の parameter、structured-output schema、公開関数、モデル・アクセス設定、および動的 prompt の code fence 保護を回帰検証するテスト。canonical builder との互換性や oracle schema との一致も確認する。
- review の enumerate、judge、merge、validate advocate/challenger 各 builder に共通する所見判定規範と、動的入力・placeholder・section 境界の保持を検証するレビュー系テストの入口。

## Read this when
- oracle review builder の parameter、schema、公開面、prompt 生成、動的入力の fence 保護を変更または検証するとき。
- review builder の canonical 実装との互換性や、oracle 側 schema との一致を確認するとき。

## Do not read this when
- review builder 以外の ACP builder や、実装詳細そのものを確認したいとき。
- 所見判定規範の正本や schema 定義を変更・確認する場合は、対応する oracle source または prompt builder の正本を直接読むとき。

## hash
- 132c1befabbafd5ec40f3e5c8916d29559a97a332da9b38f25465bf999fe5099

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
- TUI 起動 builder が生成する固定実行 parameter と prompt の契約を検証するテスト。元の prompt に依存しないモデル・推論・ファイルアクセス設定、作業ディレクトリ、indexing preflight、生成 prompt の内容と重複抑制を確認し、互換 module の公開 API を単一 builder に限定する。
- TUI 起動 parameter builder の実装や、その固定規範・実行設定・公開面の変更を検証する realization test への入口。

## Read this when
- TUI 起動 builder の parameter、prompt 合成、固定規範の適用、または互換 module の公開 API を変更・レビューするとき。
- TUI 起動経路でモデル、推論強度、ファイルアクセス、作業ディレクトリ、preflight、structured output の設定契約を確認するとき。

## Do not read this when
- TUI 以外の builder や一般的な prompt 生成の挙動だけを調査するとき。
- 実装の詳細や正本仕様を確認する必要があり、対応する builder 実装または oracle source を直接読む方が適切なとき。

## hash
- 2d6b3a362ed00d5ab1a0a2c3740d62b52df6b797afd1b425b6e2a9009c3dc46d

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
- 公開 CLI の末端コマンド集合が oracle 仕様の列挙と一致すること、および Typer/Click の互換性エラーなくヘルプを描画できることを検証する CLI コマンドツリーのテスト。feedback report の公開オプションが --all のみに限定されることも確認する。CLI コマンド構成や help 表示、feedback report のオプション範囲を変更・調査するときの実装テスト入口。

## Read this when
- 公開 CLI の leaf command 集合、サブコマンド階層、help 描画、feedback report のオプション公開範囲を変更または検証するとき。

## Do not read this when
- 個別サブコマンドの実行仕様や oracle 文書の内容を確認したいとき。対応する oracle のサブコマンド仕様を直接読むこと。
- CLI 以外の実装やテストを変更するとき。

## hash
- a65963aa0e35e9bd6d16fb6738b2cb0341188616256c1c554b64f626ad39af0e

# `test_cli_tui.py`

## Summary
- TUI 起動直前の CLI 前処理に関する外部挙動を検証するテスト。プロンプトエディタ入力の初期値・timestamp 衝突・不正 skeleton の扱い、編集後の Codex TUI 起動、linked worktree における prompt とログの配置、`.cmoc` の ignore 設定を対象とする。TUI 前処理や関連する prompt editor の挙動を確認する際の入口。

## Read this when
- TUI サブコマンドの統合的な起動挙動を変更・検証するとき
- prompt editor の入力生成、skeleton 検証、timestamp 衝突処理を確認するとき
- linked worktree での prompt・agent call context・ログ配置を確認するとき
- TUI 実行時の `.cmoc` ignore とログ生成を検証するとき

## Do not read this when
- prompt editor の正本となる初期テキスト生成規則だけを確認したいとき
- TUI 以外のサブコマンドや CLI 前処理を調査するとき
- 実装内部の prompt builder や runtime preflight の詳細を直接確認する必要があるとき

## hash
- ad7ca9e8b2f311112e664db90bc0a0f7fdfe2ef0e10f847eeb4449e1a17aa3e3

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
- Codex exec の実行環境分離、CLI 引数・stdin・出力ファイル契約、リポジトリ書き込み、UTF-8不正出力、汎用 model provider override、および CODEX_HOME 設定ファイル非生成を検証するテスト群。Codex 実行ランタイムや override 引数の挙動を変更・確認するときの入口。

## Read this when
- Codex exec の起動引数、sandbox・approval 設定、stdin 経由の prompt 渡し、出力取得を変更または検証するとき。
- Codex 実行時の HOME/CODEX_HOME 分離、model provider 設定、リポジトリへの生成物、および不正 UTF-8 出力の扱いを確認するとき。

## Do not read this when
- Codex exec ランタイムやそのテストの挙動を扱わず、他の CLI 機能・設定・テストだけを調査するとき。

## hash
- f9b08932a5ddebe6733210f7c69ca3df7b816260cc5f5b02d67addb3045ba76f

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
- Codex quota exceeded 後の外部挙動を検証する回帰テスト群。quota availability probe の構築・共有・失敗伝播、session ID による resume と session ID 欠落時の再実行、quota polling 上限、capacity retry、並行呼び出し、CODEX_HOME/cwd、stdout JSONL・call log・subcommand log・コンソール出力を同じ retry 状態機械の観測点として扱う。Codex 実行の quota 復帰処理やそのログ契約を変更・調査するときの入口。

## Read this when
- Codex exec の quota exceeded 後の probe、待機、resume、再実行、retry 制御を変更または検証するとき
- quota probe の失敗・KeyboardInterrupt・不正 JSONL・並行呼び出し時の伝播を確認するとき
- quota retry に関する session ID、CODEX_HOME/cwd、call log、subcommand log、コンソール出力の回帰を調査するとき

## Do not read this when
- 通常の Codex exec 成功・失敗処理だけを変更または調査する場合は、quota retry の実装や直接の実行契約を読む
- quota probe parameter の正本仕様や builder の実装を確認するだけの場合は、正本仕様または builder 実装を直接読む
- quota retry と無関係な Codex CLI 引数、ログ、subcommand 処理を扱う場合は、この回帰テスト群を入口にしない

## hash
- bdb11dc4430a0515fae63b77aa5f52c1918dd3cfd2078776cfc0d51c06e3d629

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
- Codex TUI 実行ラッパーの振る舞いを検証するテスト群。完成済みプロンプトの読み込み、作業ディレクトリ・sandbox・CLI 引数、呼び出しログとサブコマンドイベント、終了結果や例外時のエラー記録を確認する。Codex TUI 実行処理の実装や、そのログ・アクセス制約に関するテストの入口。

## Read this when
- Codex TUI の実行引数、prompt の扱い、agent call のアクセスモードを変更または検証するとき
- Codex TUI の成功、CLI 不在、KeyboardInterrupt、非 0 終了時のログ・コンソール報告を変更または確認するとき
- TUI call log と codex_call サブコマンドイベントの生成契約をテストするとき

## Do not read this when
- Codex TUI 以外の Codex 実行経路や一般的なサブコマンドのテストを扱うとき
- 実装の詳細を確認することが目的で、対応する runtime 実装や oracle 仕様を直接読むべきとき
- prompt 構築規則、ログ形式、通知仕様そのものを変更・確認するとき

## hash
- bfd29666737329453563f4dc1683fcd4286ea87f5519d1b46bf72a84fb8482b7

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
- editing run の統合 realization test。realization apply/refactor fork、run join/abandon の共有 lifecycle を隔離 Git repository で検証し、state・worktree・branch・report・process tracking・INDEX 更新・rollback・cleanup・中断時の復旧を扱う。関連する run lifecycle の挙動を確認するための主要なテスト入口。

## Read this when
- realization apply または refactor fork の lifecycle 挙動を変更・調査するとき
- run join/abandon、run worktree、共有 state、branch merge、cleanup を変更・調査するとき
- Codex child process tracking、INDEX refresh、fork/lifecycle report、rollback、interrupt/error recovery の統合挙動を検証するとき

## Do not read this when
- 単一の実装関数や単独の CLI 出力だけを確認する場合は、対応する src やより直接的な専用 test を読む
- editing run と無関係な機能、または oracle・INDEX の正本仕様そのものを変更・確認する場合

## hash
- eba012d64ac83fcd925f0c6ef9062f3c219b389906122cfe21fbc4c4d1e3f277

# `test_feedback.py`

## Summary
- feedback observation の reporter、collector、保存、rate limit、redaction、idempotency、atomic recovery を検証する受け入れテスト。
- normalization unit と feedback state の整合性、canonical key、schema version、machine rule、revision 選択、writer lock、復旧処理を検証する。
- feedback report の初回・増分生成、fingerprint 再検証、machine issue の抑制、invalid observation、ユーザー中断、publication recovery を一連の fixture lifecycle として検証する。
- feedback subsystem に関する実装・正本仕様の挙動を横断的に確認する test suite であり、個別機能の単体テスト入口ではなく lifecycle assertion の入口である。

## Read this when
- feedback observation の収集・保存・reporter protocol の挙動を変更または検証するとき
- feedback state、normalization unit、issue recurrence、incremental report の整合性を変更または検証するとき
- feedback report の中断時処理、atomic file recovery、invalid input、secret redaction を調査するとき

## Do not read this when
- feedback subsystem 以外の CLI 機能や一般的なテスト実行方法を確認するとき
- 個別実装の詳細を直接調査できる場合。collector、state、report の実装・正本仕様を先に読むべきとき
- feedback の正本仕様そのものを変更・確認するとき。oracle の各仕様ファイルを直接読むべきである

## hash
- 3b37b6741840018e24216e940c60228544acb05eb6f360e619ae36075724e149

# `test_file_inventory.py`

## Summary
- Git 管理下の oracle/realization ファイル列挙契約を検証するテスト群。通常・nested repository・linked worktree・各種 ignore source・除外境界を対象に、列挙結果、refactor state、SHA 更新、非通常ファイルや symlink の拒否、Git 処理量の安定性を確認する。ファイルインベントリ実装の挙動を確認するためのテスト入口。

## Read this when
- oracle/realization ファイルの full-tree 列挙、Git ignore 判定、nested repository 境界、除外ディレクトリ、symlink・FIFO・device mode の扱いを変更または検証するとき
- refactor state の同期やファイル SHA 更新が列挙結果と一致することを確認するとき
- ファイル数増加時の Git 処理量や traversal の計算量を検証するとき

## Do not read this when
- ファイル列挙や runtime_git の挙動に関係しない CLI 機能を変更または調査するとき
- テスト実行方法だけを確認したいときは、repository local の test_execution の案内を先に読むべき

## hash
- 111e740c45761cc98cedac17f6e8113db3e44d3cd80dfe2d0568bdcd7039f307

# `test_indexing_cli.py`

## Summary
- `cmoc indexing` の CLI と preflight の外部挙動を検証するテスト群。doctor による初期化、現在の linked worktree の選択、未コミット差分の拒否・保持、Codex structured output による INDEX.md 生成、fresh hash 時の生成省略、INDEX.md のみの commit と異常時の拒否を扱う。indexing の実装や仕様を確認する際のテスト入口である。

## Read this when
- `cmoc indexing` の正常系・異常系の挙動を変更または調査するとき
- worktree、doctor、preflight、既存の未コミット差分の扱いを確認するとき
- Codex 呼び出し、INDEX.md 更新、fresh hash による省略、commit 対象の制約を確認するとき

## Do not read this when
- indexing の正本仕様や CLI 契約を確認する場合は oracle の indexing 仕様を直接読む
- Codex structured output の項目定義だけを確認する場合は対応する schema を直接読む
- 実装の責務や内部処理を確認する場合は対応する src ファイルを直接読む
- indexing と無関係な CLI やテストを調べる場合

## hash
- c8971ee4d75ccbc5d1309244856b7cb153bc6f39deacce958a3ac285a3d8328e

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
- `cmoc oracle edit` の main-worktree TUI 制御を検証するテスト。
- TUI 起動前の prompt 構築・エディタ入力・indexing preflight・clean worktree 検査の順序、TUI 成否、oracle 差分と session state の保持を確認する。
- main worktree、active session、clean worktree などの起動前提を満たさない場合に利用者向けエラーとなることも検証する。

## Read this when
- `cmoc oracle edit` の TUI 起動フローや起動前提を変更・検証するとき。
- oracle edit 実行時の run lifecycle 非使用、oracle 差分の保持、session state の不変性を確認するとき。
- prompt builder、editor input、indexing preflight、clean worktree 検査の呼び出し順と引数を確認するとき。

## Do not read this when
- `oracle edit` の実装詳細や正本仕様そのものを調べるときは、対応する実装または oracle 仕様を直接読む。
- 他のサブコマンドの TUI 制御や一般的な CLI テストを調べるとき。

## hash
- 1a77814920fecf935541f95922ac33c5d9096aa92ef56afc33ef8631747b8399

# `test_oracle_investigation_cli.py`

## Summary
- このテストは、`cmoc oracle investigation` が main worktree かつ session なしでも起動できることを、doctor、prompt editor、prompt 確定、TUI 起動の順序と生成パラメータを通じて検証する。併せて、investigation の realization adapter が builder 以外の公開名を持たないことを確認する。CLI 起動条件と investigation builder の公開面を確認したいときの入口になる。

## Read this when
- `oracle investigation` の CLI 起動可否、session 前提の有無、prompt editor から TUI 起動までの呼び出し順を検証・変更するとき。
- investigation launch TUI builder の公開 API と、生成される AgentCallParameter の設定を確認するとき。

## Do not read this when
- oracle investigation の実装詳細そのものを変更・調査する場合は、参照されている oracle 仕様や launch TUI 実装を直接読む。
- 他の subcommand の起動条件や、一般的な CLI テスト基盤だけを確認する場合は、このテストを入口にしない。

## hash
- b754cb3c1f0ed4f012119528c3bd9c95a9f209c900f27203e5122fd2b3ddd49f

# `test_oracle_review_loop.py`

## Summary
- oracle review の finding loop を検証する回帰テスト。対象 oracle に応じた finding の引き継ぎ、main worktree と review worktree 間のパス対応、challenger/advocate の同一周回理由、interrupt 時の部分結果保持、merge の postcondition と失敗伝播を fake Codex call で確認する。oracle review の検証・実装変更時に、review loop の外部契約を確認するための入口となる。

## Read this when
- oracle review の finding 列挙・検証・merge・judgement の挙動を変更または調査するとき
- review loop の interrupt 復旧、partial progress、worktree context、Structured Output の postcondition を確認するとき
- 関連する oracle review の正本仕様と実装がこの回帰テストを満たすか検証するとき

## Do not read this when
- oracle review 以外のサブコマンドや、finding loop の外部契約に関係しないテストを調査するとき
- テスト実行方法そのものを確認したい場合は、テスト実行規則や直接の実行設定を読むとき
- oracle review の正本仕様や prompt 構築実装を確認することが目的の場合は、記載された oracle 文書や実装を直接読むとき

## hash
- 251e2e2a4de5ab1be5a36fe810621c47261e740bebb346a93d98966e8cc26ae8

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
- oracle review の report 生成・表示と CLI 出力を検証する回帰テスト群。中断・処理失敗時の report、finding の severity/verdict 別分類、評価対象数、path 集計、Markdown/YAML エスケープ、scope option、timestamp 衝突回避などを扱う。oracle review report contract の構築から表示までを一体で確認する入口。

## Read this when
- oracle review の report schema、finding 表示、CLI 出力、エラー／中断時の挙動を変更・調査するとき
- oracle review の回帰テストや Structured Output callback の期待契約を確認するとき

## Do not read this when
- oracle review の通常処理実装そのものを確認したいときは、対応する sub_commands の実装を直接読む
- oracle review の正本仕様を確認したいときは、列挙された oracle doc や schema 定義を直接読む

## hash
- 0b5880a67b77bf66a9fbaca514bd12e082cff340a5a1b919904a81d0d542d9ec

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
- oracle review の隔離 run、linked worktree、snapshot fork、cleanup、merge、INDEX.md 統合、および差分制約を検証する pytest テスト群。oracle review の worktree lifecycle と INDEX 更新経路を確認する入口。

## Read this when
- oracle review の run isolation、session branch からの fork、worktree・branch の cleanup、割り込み処理を変更または検証するとき
- review worktree で INDEX.md のみを統合する仕様、preflight、merge conflict 復旧、差分検証を変更または検証するとき
- oracle review の Structured Output 呼び出しや、関連する lifecycle lock・通知・report のテスト対象を確認するとき

## Do not read this when
- oracle review の実装詳細を変更するだけで、既存の挙動をテストまたは検証する必要がないとき
- INDEX.md の一般的な生成規則だけを確認する場合は、indexing の正本仕様や INDEX 更新実装を直接読むとき
- oracle review と無関係な CLI サブコマンド、通常の編集 run、または一般的な Git 操作を扱うとき

## hash
- e39dc8e131366743e556a39e7f2342680b7c3f721d26540d0d0f8049af594104

# `test_packaged_import.py`

## Summary
- パッケージ化した配置での import 境界と公開 API を検証するテスト。oracle review builder、oracle edit/editor 入力、ACP basic、cmoc config の各実装について、隔離環境での参照先・出力契約・再公開対象を確認する。packaged layout やこれらの公開 import 契約を変更・調査するときの入口。

## Read this when
- packaged layout での import 失敗や Python パッケージ配置を調査するとき
- oracle review/edit、prompt editor 入力、ACP basic、cmoc config の公開 API または再公開契約を変更・検証するとき
- このテストが検証する setuptools の package-dir や packages.find の設定を確認するとき

## Do not read this when
- 上記の packaged import や公開 API 契約に関係しない機能の実装・テストを扱うとき
- 単一の正本定義や実装本体の詳細を確認したいときは、対応する oracle source または realization implementation を直接読む

## hash
- 54dac2ce03dfeab8f3a01ab9a192530996b907144573594eb7316c0cbe02164e

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
- 標準 prompt parts のレンダリングと complete prompt の組み立てを検証する回帰テスト。各 standard の主要文言、選択的な注入、file access mode ごとの規則、placeholder の統合・展開、共通 routing/feedback instruction の存在を確認する。prompt builder 周辺の変更時に、対象挙動を一括確認する入口となる。

## Read this when
- prompt part の構成・レンダリングを変更または検証するとき
- complete prompt に standard、補助 prompt、placeholder、共通 instruction を追加・変更するとき
- file access mode や prompt の注入条件に関する回帰を調査するとき

## Do not read this when
- 個別の prompt part の本文や生成ロジックだけを直接調査する場合
- prompt builder と無関係なテストや実装を変更する場合
- テスト実行方法や環境設定だけを確認する場合

## hash
- 7ff0699cc450721a174a34254789ca573f67ae981364e0a39cd419650f72e596

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
- Codex sandbox argv が permission profile に依存しないことを検証するテスト。`build_codex_override_args` と `prepare_codex_override_args` に path 別の read/write 権限入力を渡す入口が残っていないことを確認する。

## Read this when
- Codex 実行用 argv builder の permission profile 非依存性を検証するとき
- path 別の権限入力を builder API が受け付けないことを確認するとき

## Do not read this when
- argv builder の実装仕様を確認するときは、実装ファイルを直接読む
- Codex 実行ルールやテスト全体の要件を確認するときは、対応する oracle 文書を読む

## hash
- 961873113d6b122317114063f7ccd93ee437f4c39fd5dfe1bab3b4b8b55bd796

# `test_runtime_codex_profile.py`

## Summary
- Codex argv の model、sandbox、provider 上書き契約と、構造化出力 schema の保存・読み取りを検証する realization test。file access mode から専用 sandbox 引数への変換、approval や MCP feedback 設定、通知 callback、provider の TOML 表現、未知・未定義 provider の拒否を扱う。Codex 実行プロファイルの argv 構築・schema 保存・JSON 読み取り挙動を確認したい場合の入口。

## Read this when
- Codex の model、sandbox、approval、provider 上書き argv の契約を変更または検証するとき
- MCP feedback 起動情報や TUI 通知設定が Codex argv にどう反映されるか確認するとき
- 構造化出力 schema の改行保持・SHA256 保存、または不正 UTF-8 出力の扱いを確認するとき

## Do not read this when
- Codex 実行プロファイルの実装詳細を確認する場合は、まず対応する realization implementation を直接読むとき
- 一般的な ACP の agent parameter や CmocConfig の仕様だけを調べるとき
- このテストが対象としない CLI 機能や別の実行経路を調べるとき

## hash
- 3780de299806fd2ed2b0876cbf92f3ad5cd834f13a70677c0137575730987f0f

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
