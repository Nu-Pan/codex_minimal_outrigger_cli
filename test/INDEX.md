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
- Codex CLI の実経路・runtime wrapper テストで共有する補助関数と最小テスト用 double を提供する。認証に依存しない隔離 Codex 環境の準備、Codex パラメータ生成、CLI 引数・設定 override の検査、subprocess 制御用 override の固定化が主な責務で、これらのテスト支援が必要な場合の入口となる。

## Read this when
- Codex 実行環境の初期化や test-local Ollama 用設定を含む runtime wrapper テストを読むとき。
- Codex CLI 引数、構造化出力、設定 override の検証ロジックを確認・変更するとき。
- 複数の Codex 関連テストで共通する fixture や stub の挙動を確認するとき。

## Do not read this when
- Codex runtime wrapper の実装そのものや、テスト対象の仕様を確認したいときは、対象の実装・oracle 文書を直接読む。
- Codex と無関係なテストの fixture、assertion、テストケースだけを読むとき。

## hash
- 168e75e83cb8c4a2c5f0e4014606871e8e45101a528f4dd6b06433974f63ac78

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

# `_ollama_support.py`

## Summary
- 実経路統合テスト向けに、case-local Ollama の導入・キャッシュ管理・モデル準備・GPU-only 推論確認・pytest 起動・プロセスグループ終了を一体で担うテスト支援モジュール。
- 共有キャッシュの安全性、排他制御、atomic publish、case ごとの作業領域分離を扱い、統合テストが利用するローカル Ollama 接続情報と設定変換を提供する。

## Read this when
- 実経路統合テストで Ollama を起動・利用する仕組みを調査または変更するとき。
- Ollama のキャッシュ、モデルの materialize／publish、GPU-only 検証、動的 endpoint、process teardown の挙動を確認するとき。
- case-local Ollama を向けた CmocConfig や、この支援モジュール経由の pytest runner を扱うとき。

## Do not read this when
- 通常の Ollama provider 設定や本番実装の挙動だけを確認する場合は、設定・実装側の対象を直接読む。
- Ollama を使わない単体テストや、一般的な pytest 実行方法だけを調べる場合。
- モデル品質や応答内容そのものを評価する場合。

## hash
- 51b074c8cb0b59b3fbb3ee372cdad386653bfe5dc0bfb3fcf84999f5565989f2

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
- TUI 起動 builder が固定するモデル・推論・ファイルアクセス設定、実行前処理、生成 prompt と規範の内容を検証するテスト。互換 module の公開 API が現行 builder のみに限定されることも確認する。TUI 起動 parameter の挙動や公開面を変更・確認する際のテスト入口。

## Read this when
- TUI 起動 parameter の固定値、prompt 生成、規範の埋め込み、実行前処理を変更または検証するとき。
- TUI 起動 builder の互換 module における公開 API の範囲を変更または検証するとき。
- 対応する builder 実装の挙動に対するテスト要件を確認するとき。

## Do not read this when
- TUI 起動 builder の実装詳細を直接確認・変更する場合は、まず対応する実装や正本仕様を読むべきである。
- TUI 以外の builder や、共通 parameter の一般仕様だけを調査する場合。

## hash
- 690dcff632dbbae0554cb917f595d38985d2ddc8eae16c07ed8422dd32814a79

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
- TUI 起動直前の CLI 前処理を外部挙動から検証するテスト。エディタ入力の正本初期値、timestamp 衝突時の保持、編集済み prompt による Codex TUI 起動、agent call パラメータ、prompt 保存先、linked worktree の扱い、`.cmoc` の ignore とログ配置を確認する。TUI 前処理やその統合挙動に関するテストの入口。

## Read this when
- `tui` サブコマンドの起動処理、エディタ入力、Codex TUI 呼び出し、prompt の生成・保存を変更または調査するとき
- linked worktree と main repository 間の prompt・ログ配置や `.cmoc` ignore の挙動を確認するとき
- TUI 前処理の外部挙動に対するテストを追加・変更するとき

## Do not read this when
- TUI 以外のサブコマンドや、TUI 前処理と無関係な prompt builder・runtime preflight の内部実装だけを調査するとき
- 正本仕様そのものを確認する場合は、テストではなく指定された oracle 仕様を直接読むとき

## hash
- 7caff6698462b8d5de5df1bba5a1b6b3298b87b201146255c81513baee8ba1c4

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
- Codex CLI 実行ランタイムと case-local Ollama の統合テストを扱う。pytest 実行環境、Ollama キャッシュ分離・再利用、Codex の argv・override・stdin・出力・schema 配置、リポジトリ書き込み、汎用 model provider の契約を検証する。Codex 実行や Ollama テスト支援の挙動を確認・変更する際のテスト側の入口である。

## Read this when
- Codex CLI 実行ランタイムのテスト仕様や、実際の Codex 呼び出し契約を確認するとき。
- case-local Ollama のキャッシュ、モデル再利用、インストール復旧、pytest 実行環境の分離を確認するとき。
- Codex の provider 設定、sandbox、approval、構造化出力、ログ、作業ディレクトリ、ファイル書き込みを検証するとき。

## Do not read this when
- Codex 実行ランタイムの実装そのものを変更・調査する場合は、まず対応する src 側の runtime 実装を読む。
- Ollama 支援関数の実装やモデル起動処理を直接調査する場合は、支援モジュールを読む。
- 一般的な pytest 実行方法やテスト全体の選択基準だけを確認したい場合は、テスト実行ルールを読む。

## hash
- 568f6512768ca4cd8d72544bb96eb2bbc359a708974b39167e50d42f278db880

# `test_codex_runtime_home.py`

## Summary
- Codex 実行時の CODEX_HOME 検証に関するテストを収録する。未設定時の既定値、設定値の保持、相対パスの解決、存在しないパスやファイル指定の事前拒否、および auth.json の形式に依存しない検証を確認する。

## Read this when
- Codex subprocess 実行前の CODEX_HOME 検証や、Codex 実行環境の初期化に関する挙動を変更・調査するとき。
- runtime_codex の home 引き渡し、相対パス解決、preflight failure のテスト対象を確認するとき。

## Do not read this when
- Codex home 検証以外の Codex 実行制御や、一般的な subprocess 呼び出しの挙動だけを調べるとき。
- 実装の詳細や正本仕様を確認する必要があり、対応する runtime 実装または oracle 仕様を直接読むべきとき。

## hash
- c38202e7a98131ba5573de6b1df0466aaac4ec9648417b330dd17036697393a4

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
- Codex の quota 枯渇後に行う probe・待機・session resume・prompt 再実行の外部挙動を検証する回帰テスト。probe の共有、並行呼び出し、quota 復帰失敗、ログ・コンソール出力、CODEX_HOME と cwd、stdout JSONL からの session ID 復元まで、同一の retry 状態機械に属する観測点をまとめて扱う。

## Read this when
- Codex exec の quota retry、quota availability probe、session resume、quota 待機の並行制御を変更または調査するとき。
- quota retry に関する call log、subcommand log、stdout・prompt・output の保存、エラー伝播、CODEX_HOME/cwd の挙動を確認するとき。

## Do not read this when
- 通常の Codex exec 成功処理や quota と無関係な subprocess 実行を調査するときは、runtime 実装やその直接のテストを読む。
- quota probe adapter の構築仕様だけを確認したい場合は、probe builder の実装・仕様を直接読む。

## hash
- be2c73e3cf6f2d6117a8e205ebcd34123d421068c01f07e934e8657263f5b291

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
- Codex TUI 実行ランタイムの振る舞いを検証する pytest。完成済み prompt の読み込み、作業ディレクトリと sandbox 引数、Codex 呼び出しログ・サブコマンドイベント・コンソール要約、timestamp 衝突時のログ保持、CLI 不在・KeyboardInterrupt・非 0 終了時の失敗処理を扱う。TUI 実行処理やその仕様に関するテストを追加・変更するときの入口。

## Read this when
- Codex TUI の CLI 引数、アクセスモード、prompt の扱い、実行ログまたはイベントログを検証・変更するとき
- Codex CLI 不在、割り込み、非 0 終了など TUI 呼び出し失敗時の外部挙動を確認するとき

## Do not read this when
- TUI 以外の Codex 実行経路や一般的なログ機能だけを変更・調査するとき
- Codex TUI の実装詳細を変更する作業で、まず実装モジュールや対応する oracle file を直接確認すべきとき

## hash
- caeee66fedc4771b2e991b66cd2bfd3011c2fd01d6b40412f75cfec1e06f52cb

# `test_doctor_cli.py`

## Summary
- doctor preprocess の共有 lifecycle を外部挙動から検証する統合テスト。Git の ignore・tracked runtime・config・refactor state の修復、repair 順序、reporter probe の中断伝播、共有 lock、修復失敗時の index 復元を扱う。CLI と直接呼び出しの両方を通じて、既存の staged 差分・index flag・intent-to-add・rename・削除・unstaged hunk を保持し、修復用 commit が利用者変更を取り込まない契約を確認する。doctor preprocess の外部契約を検証するテスト群への入口であり、実装の詳細や個別の低レベル helper のテストを探す場合は別のテスト対象を読む。

## Read this when
- doctor preprocess の CLI または直接呼び出しにおける修復 lifecycle、Git index の保全、linked worktree と repository の境界を検証・変更するとき
- doctor の lock、config 同期、refactor state 同期、reporter 事前検証、repair commit の外部挙動を一続きの統合テストとして確認するとき
- 既存の staged・unstaged 差分や index metadata を doctor が保持する契約を調査するとき

## Do not read this when
- doctor preprocess の実装ロジックや正本仕様そのものを確認したいときは、実装または指定された oracle 文書を直接読む
- doctor 以外の CLI サブコマンド、または個別 helper の局所的な単体挙動だけを確認したいとき
- Git、config、refactor state の一般的な fixture や共通 test helper の定義を確認したいときは、それぞれの支援モジュールを直接読む

## hash
- 6ff9769ab1050644d4a791da38567da6e08f510e03c71db4eca665d540e69306

# `test_editing_run_cli.py`

## Summary
- editing run の integration test として、realization apply/refactor の fork、run join/abandon、共通 lifecycle state、worktree・branch・process tracking・report の生成と cleanup を検証する。異常系では想定外差分、agent commit、INDEX refresh、副作用、merge/cleanup/rollback 失敗、中断、破損 tracking、競合を扱い、状態遷移と資源保全を確認する。関連する編集 run lifecycle の挙動を一続きで確認する入口となる。

## Read this when
- realization apply または refactor の fork lifecycle を変更・調査するとき
- run join/abandon、worktree・branch cleanup、process tracking、report、rollback の挙動を変更・調査するとき
- editing run の状態遷移や apply/refactor と共通 lifecycle の統合挙動を検証するとき

## Do not read this when
- INDEX 更新単体の仕様や実装を確認するだけのとき
- apply または refactor の agent prompt・単独処理を確認するだけで、run lifecycle との統合挙動を扱わないとき
- 通常の CLI 入口や無関係なコマンドのテストを探しているとき

## hash
- 8fa12dea1fc99606ba072444f0bb300d9ee40b6a02e040ae3d0c47537ce72c0a

# `test_feedback.py`

## Summary
- feedback observation の収集・保存・正規化・状態検証・増分 report を一連の受け入れテストで検証する。
- reporter と collector 間の MCP/JSON-RPC 契約、capability、rate limit、context、redaction、path 境界、冪等性、異常復旧を扱う。
- repository-local な issue state、normalization unit、report manifest、assessment、fingerprint 更新、machine issue の抑制、ユーザー中断時の完了処理を検証する。
- feedback subsystem の実装や oracle 仕様を変更した際に、その lifecycle 全体の外部挙動を確認するためのテスト入口である。

## Read this when
- feedback observation の reporter、collector、store、state、normalizer、reporter report の挙動を変更または検証するとき。
- raw observation から ingestion receipt、normalization unit、incremental report までの一連の lifecycle を確認するとき。
- rate limit、secret redaction、path boundary、atomic write、recovery、fingerprint freshness、machine issue suppression の回帰を調査するとき。

## Do not read this when
- feedback subsystem の単一実装関数の詳細だけを確認する場合は、対応する src 実装または oracle 仕様を直接読む。
- feedback と無関係な CLI subcommand、一般的なテスト実行設定、別機能の fixture を扱う場合。

## hash
- 377bce63cfa439e3f5c9f8d34d4100444508a520f4010f4fe170bcf32fbdefc4

# `test_indexing_cli.py`

## Summary
- `cmoc indexing` の CLI と preflight、linked worktree 対応、doctor による未初期化リポジトリ準備、Codex structured output による INDEX.md 生成、hash に基づく再生成省略、INDEX.md のみを対象とする commit lifecycle を外部挙動として検証するテスト群。dirty worktree や既存の非 INDEX 差分、git diff 異常時の拒否・保持も確認する。

## Read this when
- `cmoc indexing` の実装・preflight・worktree 動作を変更または調査するとき
- INDEX.md 更新、Codex index entry builder、commit 対象パス、既存差分の扱いを検証するとき
- indexing 関連テストの失敗原因や期待される CLI 外部挙動を確認するとき

## Do not read this when
- INDEX.md のルーティング生成そのものの仕様を確認したいときは、指定された oracle 文書と Structured Output schema を直接読む
- indexing 以外のサブコマンドや、一般的な Git helper の実装だけを調査するとき

## hash
- c09669de8958f4bc5a0d2d523f0a0e5a7d7f6df3192e1ef89d8b1477d28b6c54

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
- `cmoc oracle edit` の main worktree TUI 起動制御を検証するテスト。TUI 実行順序、oracle 差分の保持、run lifecycle や session state の不変性、モデル・権限・prompt 設定、および起動前提違反時のエラーを扱う。oracle edit CLI 実装とその起動前提を確認する際のテスト入口。

## Read this when
- `cmoc oracle edit` の TUI 起動、実行引数、prompt 注入、差分保持の挙動を変更または検証するとき
- oracle edit の main worktree・session branch・clean worktree 前提やエラー処理を変更または検証するとき

## Do not read this when
- oracle edit 以外のサブコマンドの挙動を確認するとき
- oracle edit の正本仕様や実装詳細そのものを確認するときは、まず対応する oracle 仕様または実装を直接読む場合

## hash
- 497959f379256116990c899ae1320a81251ab407d398dac0a7b54d9833a8d6c0

# `test_oracle_investigation_cli.py`

## Summary
- `cmoc oracle investigation` CLI の起動条件と起動時パラメータを検証するテスト。session なしの main worktree で起動できること、エディタ入力と自動注入指示が適切に扱われること、oracle 専用の読み取り権限・モデル・推論設定・indexing preflight が指定されることを確認する。あわせて investigation の realization adapter が期待する builder だけを公開することも検証する。

## Read this when
- `oracle investigation` サブコマンドの起動可否や session 前提を変更・調査するとき
- oracle investigation 起動時の prompt、editor input、自動注入指示、AgentCallParameter の設定を確認するとき
- investigation の realization adapter の公開シンボルを変更・検証するとき

## Do not read this when
- oracle investigation 以外のサブコマンドの挙動を調査するとき
- 起動条件や builder の公開範囲ではなく、oracle investigation の本体仕様を確認するときは、参照されている仕様書や実装を直接読む

## hash
- bb91be2f9c8e3f01fc18863489d6ea6766753d3d408830b1dba647d0d2c1e4cd

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
- oracle review の対象ファイル列挙と finding path 解決を検証する realization test。placeholder 付きパス、symlink、repository 内の oracle 判定、tracked/ignored file、session/full scope、fork commit 基準、除外対象、対象なしレポートを扱う。oracle review の対象選定・パス解決ロジックを確認する入口である。

## Read this when
- oracle review の対象列挙や finding の oracle path 解決を変更・調査するとき
- session/full scope、tracked ignored file、symlink、fork commit 基準の挙動を確認するとき
- oracle review CLI の対象なし結果や Codex 呼び出し回数を検証するとき

## Do not read this when
- oracle review 以外のサブコマンドや、対象列挙・パス解決と無関係な CLI 処理を変更するとき
- Codex CLI の実推論や出力品質を検証する実経路統合テストを探しているとき
- oracle review の所見マージ・妥当性検証・採否判定の詳細実装を直接確認したいとき

## hash
- 9113e685069c202fce5d8a6896ad9e71cbe5268f33057e218a8d36c42cce0271

# `test_oracle_review_worktree.py`

## Summary
- oracle review の隔離 run における linked worktree・session branch・snapshot commit の利用と、作成失敗・中断時の branch/worktree cleanup を検証する統合テスト。
- review worktree で生成された INDEX.md だけを session に merge し、非 INDEX 差分・merge conflict・削除・rollback residue・cleanup failure を適切に扱うことを確認する。
- indexing preflight の実行コンテキスト、Structured Output、run lifecycle lock、active editing run との共存、report 結果を検証する。

## Read this when
- oracle review、review worktree、run isolation、session branch、preflight commit の挙動を変更または調査するとき
- oracle review における INDEX.md の merge、差分制限、merge conflict 復旧、cleanup を変更または検証するとき
- oracle review の中断・例外処理、run lifecycle lock、agent call のテスト方法を確認するとき

## Do not read this when
- oracle review の通常の CLI 引数仕様や所見判定ロジックだけを確認したいときは、対応する実装または oracle review 仕様を直接読む
- INDEX.md の一般的な生成・更新規則だけを確認したいときは、indexing の仕様・実装・専用テストを直接読む
- 他のサブコマンドの worktree lifecycle や cleanup だけを扱うとき

## hash
- bb24e8f1e29da826cfe03ea61429d73eed522f7fca0e9c4dc3277fc47c83a974

# `test_packaged_import.py`

## Summary
- packaged layout での import 境界と公開 API の契約を検証するテスト。oracle review の builder、oracle edit と prompt editor、ACP basic、cmoc config について、正本参照・再公開・`__all__`・生成結果を隔離環境で確認する。packaging やこれらの import/export 契約を検証する realization test の入口。

## Read this when
- packaged layout での import 失敗や package 配置を調査するとき
- oracle と realization の公開 API 再公開、`__all__`、canonical 定義の同一性を変更・検証するとき
- oracle review/edit builder または prompt editor の packaged 実行契約をテストするとき

## Do not read this when
- packaged import、公開 API、または対象 builder の出力契約に関係しない実装を変更するとき
- 正本の builder・schema・設定定義そのものを確認する必要があり、対応する oracle source を直接読むべきとき
- 通常の機能挙動や packaged layout を伴わないテストだけを調査するとき

## hash
- f9793ebf99c08dcc0bc2b32653f4df3466e65aa7534c84661345ed760b31fd80

# `test_production_cli.py`

## Summary
- 実 Codex CLI と case-local Ollama を使う独立 process の本番経路受け入れ試験。
- doctor、indexing、oracle review、realization apply/refactor、run/session の join・abandon、TUI・oracle edit・investigation など全末端サブコマンドを対象に、終了 code、report、state、Git、call log、PTY 上の応答完了と終了を検証する。
- LLM の回答品質ではなく、応答後の cmoc の制御と外部から観測可能な副作用を確認するテスト領域の入口。

## Read this when
- CLI の全末端サブコマンドが実 Codex・実行環境・隔離された Ollama を通る本番経路を検証または変更するとき
- 独立 process、Codex call log、セッション／run state、report、Git 状態、または TUI の PTY 操作に関する受け入れ試験を調べるとき
- 新しい公開末端コマンドの追加により、本番経路試験の網羅性を確認するとき

## Do not read this when
- LLM の回答品質やプロンプト内容そのものを評価するとき
- 単一サブコマンドの内部ロジックや unit test を直接調べるとき
- 実 Codex CLI や Ollama を使わないテスト、または一般的なテスト実行方法だけを確認するとき

## hash
- 1285426fefe037a4a7e40fd8020adfc92a689519a285d87aaeca3a6e157defd8

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
- CLI の error report、console/file log、doctor preflight、shell completion、work root 境界を検証する統合テスト。共通 runner と終了処理を通じた外部契約の入口として、runtime CLI 周辺の挙動を確認する。
- duration 表示、並列 subcommand logger、doctor preprocess・pre-log check・callback・KeyboardInterrupt の終了処理、stdout error report、Click 引数解析、scope 制約、completion probe の副作用抑制、worktree ごとの処理対象を扱う。

## Read this when
- CLI lifecycle の error report、ログ生成・終了イベント、doctor preflight、completion probe、work root 制約の実装または仕様を検証するとき
- runtime_cli、runtime_logging、error rendering、CLI parser、completion 初期化の変更が既存の外部契約に適合するか確認するとき

## Do not read this when
- CLI の通常機能や個別サブコマンドの成功系だけを確認する場合
- duration・logger・error rendering の実装詳細を直接調べる場合は、それぞれの実装または正本仕様を先に読むとき
- CLI lifecycle と無関係なテストデータ、Git 操作、他パッケージの挙動を調べる場合

## hash
- 6a1ddc1af9c5586c87fb02ee6657a9541b14f703ff50521aab334d6fdfd938f8

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
- Codex CLI の sandbox argv 生成を検証するテスト。permission profile に依存する path-based 引数が builder API に残っていないことと、各 FileAccessMode 向けに生成した sandbox 引数を実 Codex CLI が受理することを確認する。runtime_codex_profile と Codex CLI parser の境界を確認したい場合の入口。

## Read this when
- Codex CLI 起動引数の生成・変更が sandbox 指定や permission profile に影響する場合
- build_codex_override_args または prepare_codex_override_args の API 契約を確認する場合
- FileAccessMode ごとの Codex CLI parser 互換性を検証・変更する場合

## Do not read this when
- Codex CLI の通常の実行処理や permission profile の正本仕様を確認したい場合は、実装・仕様の直接対象へ進む
- Codex CLI を使わないテストや、sandbox argv 生成に関係しないテスト変更の場合

## hash
- 67cb600edd5ca3c074353d664b5163183194f681e2ed93803f15c14637127b11

# `test_runtime_codex_profile.py`

## Summary
- Codex argv の model、sandbox、provider 上書き契約と、フィードバック MCP 設定の安全な伝達を検証するテスト。未知の file access mode や未定義 provider の拒否、任意 provider 設定の TOML 化、schema のバイト保持、invalid UTF-8 出力の扱いも対象とする。runtime_codex_profile の Codex 起動前構築・schema 保存・出力解析の挙動を確認する realization test。

## Read this when
- Codex の model、sandbox、provider 上書き引数の生成または変更を検証するとき
- Codex 起動時の MCP フィードバック設定、secret の argv 非露出、provider 設定の TOML 変換を確認するとき
- schema のハッシュ保存や Codex 出力 JSON の異常系を変更・調査するとき

## Do not read this when
- Codex argv や runtime_codex_profile の挙動を変更・検証しない一般的なテスト作業
- 正本仕様そのものを確認・変更する作業では、このテストから始めず oracle の app_spec 文書を直接読むとき

## hash
- d43052038e0b562dc89c79e4fa76edda9e8d0a399bf3bd3028cff490652a90de

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
- Git ignore の安全な更新・判定処理を検証するテスト。cmoc 用 ignore pattern の追加、literal path の判定、特殊ファイル・symlink 化された .gitignore／info/exclude／global excludes／階層 .gitignore の拒否を扱う。

## Read this when
- Git ignore 判定や cmoc 用 ignore pattern 更新のテストを追加・変更するとき
- 特殊ファイルや symlink に対する安全性、既存 pattern と追記内容の安定性を確認するとき

## Do not read this when
- Git ignore の実装そのものを変更・調査するときは、まず対応する runtime 実装と oracle file を読むとき
- Git ignore と無関係な CLI 機能やテストを扱うとき

## hash
- 51a3bb513cc9e203fd066e67a06b39ca91c764ee2c1cba48c2ca5943ae3bb8e4

# `test_runtime_refactor.py`

## Summary
- realization refactor の永続 state について、対象ファイル集合の同期、調査履歴の保持・再調査判定、調査対象の優先選択、state schema 検証をテストする。oracle と realization の file 判定、path escape・特殊 file・symlink・gitlink など境界条件も扱う。refactor state の挙動や回帰を確認する realization test の入口である。

## Read this when
- refactor state の同期・読み書き・schema 検証を変更または調査するとき
- oracle/realization file classifier や refactor target selection の挙動を確認するとき
- refactor 機能の境界条件に関する realization test を探すとき

## Do not read this when
- refactor state や target selection の挙動を扱わないテストを探しているとき
- 正本仕様そのものを確認するときは、参照先として示された oracle 文書を直接読むべきである

## hash
- 537d98f1cb502fd793e165dbe1200c01d8d4ae1a426830152b63b03020cce035

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
- session の fork・join・abandon に関する CLI 外部挙動を、session branch と永続 state のライフサイクルとして一括検証する回帰テスト。
- 通常の branch/state 作成・遷移に加え、state 保存失敗や session-id 衝突、cleanup 失敗時の rollback、破損 state、home branch 欠落を検証する。
- linked worktree での session 操作、doctor preprocess、dirty worktree 拒否、state cleanup、sub-command log、stdout/stderr のエラー報告も対象とする。
- session join の conflict 解消について、Codex 実行境界、REPO_WRITE sandbox、対象外変更の拒否、marker 検出、削除・mode・改行を含む path の扱い、branch 削除警告を検証する。
- session CLI の実装や仕様を直接変更するファイルではなく、関連する外部挙動をまとめて確認する realization test として、session 状態遷移の回帰検証の入口になる。

## Read this when
- session fork、join、abandon の CLI 挙動や回帰テストを調査・変更するとき。
- session branch、session state、linked worktree のライフサイクルや rollback を確認するとき。
- session join の conflict 解消、Codex 呼び出し境界、sandbox、差分検証を確認するとき。
- doctor preprocess、dirty worktree、state cleanup、エラー出力やログの session CLI 連携を検証するとき。

## Do not read this when
- session サブコマンドの実装詳細だけを確認する場合は、対応する src の実装ファイルを直接読む。
- session state や join の正本仕様を確認する場合は、列挙された oracle doc・oracle src を直接読む。
- session CLI と無関係なコマンド、一般的な Git helper、Codex prompt 全般のテストを調査する場合。

## hash
- 99597bfe90a4093c54bd4e5279c1b5f3f01a568b9059fff29cc7d9c80c22a233

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
- StructDoc の Markdown renderer における整形挙動を検証するテスト。通常の本文と code block 内で連続する空行を一つに縮約すること、および互換モジュールから再公開された StructBlock が renderer で利用できることを確認する。

## Read this when
- Markdown renderer の空行縮約仕様を変更・検証するとき
- StructDoc、StructBlock、StructCodeBlock、render_as_markdown の互換公開や出力形式を変更するとき

## Do not read this when
- renderer 以外の StructDoc 機能や CLI の挙動を確認するとき
- 実装の詳細を調べる必要があり、対応する basic.struct_doc の実装を直接読むべきとき

## hash
- 650a3dab8a023eb6c55dd32e6ed5ce178f4641d3f81b8805b33c18bce039c1db
