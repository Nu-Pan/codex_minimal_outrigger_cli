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
- 対象ファイルは、Codex 実行経路テストで共有する最小ヘルパー群を提供します。テスト用 Codex ホームの準備、test-local Ollama 向け設定、既定の AgentCallParameter 生成、Codex CLI 引数・設定 override の解析、実行経路ごとの override 差し替えを扱います。

## Read this when
- Codex runtime wrapper または TUI の subprocess 制御テストを追加・修正するとき
- テスト用 Codex 環境、Codex CLI 引数、構造化出力の最小 fake result を確認するとき
- test-local Ollama を使う実経路試験の隔離設定を確認するとき

## Do not read this when
- Codex 実行経路の本体実装や oracle 仕様を確認することが目的のとき
- 共有テストヘルパーを使わない一般的なテストを読むとき

## hash
- db0b25029c11871292d2b05dac95f7bc3ef88c9a5f64f74d9c406acf3e5241c1

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
- 実経路統合テスト専用の case-local Ollama を準備するテストヘルパー。共有キャッシュの安全性検証、Ollama バイナリとモデルの取得・atomic publish・case-local materialize、GPU-only 推論の事前確認、動的 provider 設定、pytest 起動、case 単位の process group teardown を一つのライフサイクルとして扱う。test 配下から、Ollama を使う実経路統合テストの実行基盤へ進む入口。

## Read this when
- Ollama を必要とする実経路統合テストの実行方法や前提条件を確認するとき
- test case 専用の Ollama process、model working set、cache、GPU 推論確認の挙動を調査・変更するとき
- case-local Ollama を Codex の model provider 設定へ接続する方法を確認するとき
- Ollama キャッシュの lock、atomic publish、materialize、破損時の再構築を調査するとき
- テスト終了時の専用 process group の停止処理を確認するとき

## Do not read this when
- Ollama を使わない通常の単体テストや統合テストの実装・実行を扱うとき
- Ollama 本体やモデルの一般的な仕様を確認したいとき
- テスト実行全体の標準手順や品質ゲートを確認したいときは、先に対応するテスト実行規則を読むとき
- model provider や CmocConfig の正本仕様・一般的な実装を確認したいとき
- 対象の具体的な統合テスト case の期待挙動を確認したいときは、その test file を直接読むとき

## hash
- e894318b9984bb7d0d44d0b7c5ac8288aacb34e68bea50f845d6cafff03b90ee

# `test_acp_builder_editing_run_parameters.py`

## Summary
- editing run workload の canonical builder adapter を検証するテスト。apply builder の commit 範囲・raw diff・標準設定、ネストしたコードフェンスの保持、refactor builder の canonical structured-output schema・実行設定・prompt 内容、および差分内の境界風テキストの安全な保持を確認する。

## Read this when
- ACP builder の editing run 用 apply/refactor fork parameter の実装や canonical schema、prompt 境界処理を変更・レビューするとき。
- 関連する oracle builder 実装または structured-output schema とテストの適合性を確認するとき。

## Do not read this when
- editing run workload や ACP builder の parameter 生成に関係しない機能を調査するとき。
- builder 実装ではなく、個別の CLI 実行処理や一般的なテスト基盤だけを確認するとき。

## hash
- 97790644222cbc2ef25b9412fe42013cef9114efef02f8c398c61169f1507c36

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
- oracle review ACP builder の parameter、schema、adapter 公開面を検証する回帰テスト。review 各段階の共有規範、モデル・推論設定、oracle schema との一致、互換 builder、公開 export、動的入力の保持を確認する。
- 動的 prompt に埋め込む本文中の Markdown fence や section・placeholder 風マーカーを、prompt の境界と誤認せず保護できることを重点的に検証する。

## Read this when
- oracle review builder の parameter、schema、公開 API、互換 adapter を変更または検証するとき。
- review prompt の動的入力埋め込み、nested code fence、section 境界保護の実装を変更またはデバッグするとき。
- review builder と対応する oracle schema・canonical builder の互換性を確認するとき。

## Do not read this when
- review builder 以外の ACP builder の挙動だけを調査するとき。
- prompt の fence 保護や review builder の公開面に関係しない一般的なテスト・実装を扱うとき。
- 正本 schema や canonical builder の定義そのものを変更するときは、まず対応する oracle source を直接読む。

## hash
- a0ef67aa6bcec04c5c274de927a0a31f9307e6c30d5b8da1961ed6fa41f06c4b

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
- 公開 CLI の Click/Typer コマンドツリーを検証するテスト。oracle 変更後に定められた末端コマンド集合と実際の CLI を照合し、主要グループを含む help が互換性エラーなく描画されることを確認する。

## Read this when
- 公開 CLI のサブコマンド追加・削除・階層変更を実装またはレビューするとき
- Typer と Click の互換性や CLI help の描画問題を調査するとき
- oracle の CLI コマンド列挙と実装の整合性を検証するとき

## Do not read this when
- CLI の個別コマンドの実装詳細や入出力仕様を確認したいとき
- CLI 以外のテストや機能の変更を調査するとき
- コマンドツリーや help 描画に関係しないテストを読むとき

## hash
- cffc47f8ab96e3302d3f3478add14aaa2e1ad86d0722ba6bf95dfd6595e029ab

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
- Codex exec 実行基盤のテスト。pytest 実行環境、Ollama キャッシュ分離、current worktree の import、Codex HOME 隔離、CLI 引数・override・provider・schema・出力処理を検証する。runtime_codex とその周辺テストの入口。

## Read this when
- Codex exec の起動契約、ファイルアクセスモード、モデル provider、構造化出力 schema、prompt の stdin 渡しを確認・変更するとき
- Ollama を用いた Codex 実行の統合動作や、テスト用 HOME・CODEX_HOME・一時ディレクトリの分離を確認するとき
- runtime_codex、runtime_codex_profile、テスト用 Ollama runner の挙動を検証するとき

## Do not read this when
- Codex exec やテスト実行基盤に関係しない機能の実装・テストを扱うとき
- Codex CLI の正本仕様そのものを確認するときは、対応する oracle 文書を直接読む

## hash
- fdc57cfbb77facb7744178f263cd8cf087542b9fd8c5533c9bfc0374b55b51fc

# `test_codex_runtime_home.py`

## Summary
- Codex 実行時の CODEX_HOME 解決・引き渡し・記録と、Codex CLI 起動前の home 検証を検証する pytest テスト。既定値、環境変数による相対パス、作業ディレクトリ基準の解決、存在しない home やディレクトリでない home の事前拒否、auth.json の provider 非依存な扱いを対象とする。

## Read this when
- Codex 実行ラッパーの CODEX_HOME 処理、実行前検証、関連エラー挙動を変更または確認するとき。

## Do not read this when
- Codex home や runtime 実行経路を扱わず、他の CLI 機能や個別の設定検証だけを変更するとき。

## hash
- 740b5b3a00a5126bd02cef64f4029305a074beaefd9f3720e46c46a95eb7ee23

# `test_codex_runtime_paths.py`

## Summary
- Codex 実行時のパスと sandbox 設定を検証するテスト。並列実行時のログパス予約、agent call の cwd、リンク済み worktree における schema 保存先、PURE_ORACLE_READ の read-only sandbox 変換、`.agents` パス権限の非注入を扱う。

## Read this when
- Codex 実行ラッパーのログ・出力・schema 保存先を変更または検証するとき
- agent call の cwd、worktree、sandbox 権限の動作を変更または検証するとき
- Codex 実行のプロセス間競合や timestamp 付きパスの一意性を調査するとき

## Do not read this when
- Codex の prompt 生成規則そのものを変更または調査するとき
- Codex 実行時のパスや sandbox 引数に関係しないテストを変更するとき

## hash
- 7ce907d7b5bf714bfa514e10ed2765eb6caad9f99af8ffb4dba0ed5703359230

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex quota exceeded 後の probe・待機・resume・再実行を検証する回帰テスト群。代表 probe の共有、resume token の復元、quota/capacity の再試行、失敗伝播、ログ・出力・CODEX_HOME・cwd の観測を一体として扱う。

## Read this when
- Codex exec の quota 待機、quota availability probe、resume または同一 prompt の再実行を変更・調査するとき
- quota retry の並行実行、probe 失敗、KeyboardInterrupt、poll 上限、ログ記録、相対 CODEX_HOME の挙動を検証するとき

## Do not read this when
- quota retry 以外の Codex 実行仕様や通常の subprocess 呼び出しを調査するときは、対応する実装・正本仕様を直接読む
- Codex runtime の実装変更を伴わない一般的なテスト構成や別サブコマンドのテストを調査するとき

## hash
- af23cb81b1f04beebcc6489ce24e3cb6393ff2b69fbdb5726690db33d8161fb3

# `test_codex_runtime_retry.py`

## Summary
- Codex exec の retry、失敗、中断、Structured Output 検証、JSONL error、差分保持を外部挙動として検証するテスト群。fake Codex の応答、subprocess 呼び出し回数、call log、subcommand event、最終結果を同じ状態機械の文脈で確認する。

## Read this when
- run_codex_exec の retry 条件、retry 上限・backoff、capacity／semantic failure の扱いを変更または調査するとき
- Codex 呼び出しの call log、JSONL error、subcommand event、KeyboardInterrupt の記録を変更または検証するとき
- Structured Output schema の検証失敗、未知の JSONL error、retry 中の agent diff 保持を確認するとき

## Do not read this when
- Codex exec の実装詳細そのものを変更・調査する場合は、まず対応する realization implementation と正本仕様を読むとき
- Codex exec と無関係な CLI、ログ、schema、retry 機能の変更を扱うとき
- 単に通常成功時の Codex 出力形式だけを確認したいとき

## hash
- 84b0b2cfe79705c6f315d07a3f3acee5d05341788c6dfd9e5987d8f5d9d3b86c

# `test_codex_runtime_subprocess.py`

## Summary
- Codex サブプロセスと run process tracking の停止・追跡・再利用防止を検証するテスト。pidfd、専用 process group、leader 終了後の descendant、PID/PGID 再利用、tracking file の不正内容・特殊ファイル、シグナル保留、cleanup 失敗時の停止と reap、継承環境変数や cwd エラーを扱う。runtime_codex_profile と runtime_run のプロセス安全性に関するテスト入口。

## Read this when
- Codex subprocess の起動・追跡・シグナル処理・cleanup を変更またはレビューするとき
- run process tracking、pidfd、process group、PID/PGID の同一性検証を変更するとき
- Codex subprocess 終了時の例外処理、reap、tracking file 検証を確認するとき

## Do not read this when
- Codex subprocess や run process tracking の停止・追跡挙動に関係しないテストを探しているとき
- CLI の通常の入出力、編集処理、プロファイル設定そのものを確認するときは、対象の実装・専用テストを直接読む

## hash
- 20b53eb1c13189bfcaa51a6aa93c9fa6f84c74dd0f4641683d86a87e5f37b73a

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
- doctor preprocess の共有 lifecycle を検証する統合テスト。CLI と直接呼び出しの双方で、Git 状態・config・refactor state・lock・linked worktree の修復、副作用、失敗時の index 保持を確認する。doctor preprocess の外部契約を検証するテストの入口。

## Read this when
- doctor preprocess の修復順序、共有 lock、config/state 同期、linked worktree 対応を変更・調査するとき
- doctor が既存の staged/unstaged 差分、index flag、rename、intent-to-add、symlink を保持・拒否する挙動を確認するとき
- doctor の修復 commit に利用者の事前 staged 変更を含めない契約を検証するとき

## Do not read this when
- doctor preprocess 以外の CLI サブコマンドや Git helper の実装を直接調査するとき
- doctor の内部実装詳細だけを確認したい場合は、対応する runtime doctor 実装と正本仕様を先に読むとよい

## hash
- dda671fcb93055d51d0813a6c07f4a0d0541814d51c376364cb9b4b04b4b3091

# `test_editing_run_cli.py`

## Summary
- workload fork と run join/abandon にまたがる editing run lifecycle の統合テスト。apply/refactor fork、共通 session state、run worktree、fork/lifecycle report、Codex child tracking、INDEX 更新、merge・cleanup・rollback・中断・失敗時の状態遷移を検証する。

## Read this when
- realization apply/refactor fork の lifecycle 挙動を変更・調査するとき
- run join または run abandon の merge、force-resolve、worktree/branch cleanup、process tracking を変更・調査するとき
- fork report、lifecycle report、refactor state、INDEX refresh、異常時 rollback の統合動作を確認するとき

## Do not read this when
- 個別の実装関数や単一サブコマンドの局所的な仕様だけを確認する場合
- editing run と無関係な CLI、oracle、INDEX 生成処理のテストを探している場合

## hash
- 8aa66132f4a8dcf4e61d270e9fc628e04a04fe6e8c9e1a96ea6cb221296e7951

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
- `commons.indexing` の INDEX entry 生成・解析・更新と directory traversal を検証する回帰テスト群。入力検証、hash による entry 再利用・再生成、空ディレクトリ、安定した描画順、並列更新、logger 伝播、cwd lock 下の実行を扱う。
- memo 除外やネストした memo、symlink cycle・特殊ファイル・INDEX symlink の安全な扱い、linked worktree 間の indexing lock 共有も検証する。indexing runtime contract の実装変更や関連仕様の確認時に読む入口である。

## Read this when
- INDEX.md の parse/render/update、hash 再利用、traversal、symlink、安全なファイル更新を変更または調査するとき
- indexing の並列実行、Codex worker の logger 伝播、pushd/cwd lock、worktree lock の回帰を検証するとき
- `oracle/doc/app_spec/indexing.md` などの indexing contract に対する realization test を確認するとき

## Do not read this when
- CLI lifecycle や indexing 以外のサブコマンドの挙動だけを調査するとき
- INDEX entry の正本スキーマや prompt 標準そのものを確認するときは、対応する oracle source または仕様文書を直接読む

## hash
- 186d44c1ff7661b34fab8cafc83db9af5200e925112a02912853cb069a0102f8

# `test_indexing_preflight.py`

## Summary
- Codex 呼び出し直前に実行される indexing preflight の統合テスト。exec/TUI 経路での実行順序、対象 worktree の選択、repository lock 待機、preflight 無効化、file access violation 後の recovery indexing 非実行、および indexing commit と作業ツリー状態を検証する。

## Read this when
- Codex 呼び出し前の indexing preflight の挙動を変更・調査するとき
- exec または TUI の Codex 実行順序、worktree 選択、lock 制御を変更するとき
- file access violation や preflight 無効化時の indexing 回数を検証するとき

## Do not read this when
- indexing の生成ロジック自体を変更・調査するときは、対応する commons indexing 実装とその専用テストを読む
- Codex 呼び出し preflight と無関係な CLI 機能や一般的なテスト基盤を扱うとき

## hash
- a810d7d5439cbc195e2c278369349a1cc90aa31015ac3000db918cd3e1e3cfd4

# `test_oracle_edit_cli.py`

## Summary
- `cmoc oracle edit` の main-worktree TUI 制御を検証するテスト。doctor 済みの隔離リポジトリと session state を準備し、TUI 実行時の preflight・clean worktree 検査・呼び出しパラメータ・oracle 差分保持・失敗時挙動・session state 非変更を確認する。あわせて、linked worktree、非 session branch、inactive session、未コミット差分に対する起動前提違反を検証する。

## Read this when
- `cmoc oracle edit` の TUI 起動順序、実行パラメータ、oracle 編集結果の保持、run lifecycle 非使用を変更・検証するとき
- `oracle edit` の起動前提チェックや session state との連携を変更・検証するとき

## Do not read this when
- `oracle edit` 以外のサブコマンドの挙動だけを調査するとき
- TUI 実装そのものや oracle edit の仕様本文を確認する必要があるときは、対応する実装・oracle 仕様を直接読む

## hash
- 9b71d0963534ba293a3fe838402cdf5962c1c68ad9d30e61898de3e7dec07938

# `test_oracle_investigation_cli.py`

## Summary
- `cmoc oracle investigation` CLI の起動条件と、セッションなしの main worktree での動作を検証するテスト。エディタ入力の自動注入指示、Codex 呼び出し時の oracle 専用読み取りモード、生成プロンプトの内容を確認する。

## Read this when
- `oracle investigation` サブコマンドの起動条件や session precondition を変更・調査するとき。
- oracle file／realization file のアクセス制約を自動注入する処理を変更・検証するとき。
- Codex TUI 呼び出しパラメータや oracle standard を含む生成プロンプトを確認するとき。

## Do not read this when
- `oracle investigation` 以外のサブコマンドの挙動だけを変更・調査するとき。
- CLI 共通の runner や doctor の実装を直接確認したいときは、対応する `_cli_support` や共通実装を先に読む。
- oracle investigation の実装詳細そのものを変更・調査する場合は、このテストではなく `sub_commands/oracle/investigation` の実装を直接読む。

## hash
- 198b2b7e3c0b1488400f3dfce0aa911760f0823cc0fcf3461343531b69105763

# `test_oracle_review_loop.py`

## Summary
- oracle review の finding loop を対象とする回帰テスト群。finding の対象別引き継ぎ、main worktree とのパス対応、challenger と advocate の同一周回連携、judge・advocate 中断時の部分結果保持、semantic retry と上限到達時の失敗を fake Codex 呼び出しで検証する。

## Read this when
- oracle review の finding 列挙・検証・判定 loop を変更または調査するとき
- finding の prompt 引き継ぎ、worktree 隔離、interrupt 復旧、merge retry の挙動を確認するとき

## Do not read this when
- oracle review の実装詳細だけを確認する場合は、まず対応する sub_commands の実装を読む
- oracle review と無関係なテストや一般的なテスト実行方法を調べる場合

## hash
- 1cd3af13d55c94a61e3a1e8dbe48a421b8a70cb964dbce82e8f7a70fd5cb1578

# `test_oracle_review_merge_operations.py`

## Summary
- oracle review の finding merge operation について、delete・replace・merge の kind 契約、finding 更新、採番を検証する pytest。対象 ID・payload の不正、ID の重複利用も拒否されることを確認する。

## Read this when
- oracle review の merge operation の仕様変更や実装変更を検証するとき
- finding の削除・置換・統合、採番、入力検証のテストを確認するとき

## Do not read this when
- oracle review の通常の CLI 入出力や merge operation 以外の処理を確認するとき
- 正本仕様そのものを確認するときは、参照されている oracle review 文書を直接読む

## hash
- 8e42fe28e2b74c0ad87780ea4beaa26109a196a0df587aa2d7ec155cf8296478

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
- packaged layout 上での import 境界と公開 API を検証するテスト。oracle 側の正本定義を参照する builder、editor input、ACP basic、config の再公開、schema・prompt・設定値・__all__ の契約を隔離実行で確認する。

## Read this when
- packaged layout、PYTHONPATH、setuptools の package 配置、oracle と realization の import 境界を変更または検証するとき
- ACP builder、oracle review/edit、prompt editor input、config の公開 import や再公開契約を変更するとき
- 正本定義の参照、structured output schema、prompt 内容、agent call parameter の契約をテストするとき

## Do not read this when
- 単一モジュール内部の実装詳細や通常の機能挙動だけを変更・調査するとき
- packaged layout や公開 import 境界に関係しないテストを追加・修正するとき

## hash
- fb66b4d678655d53e9ce9394a52d98ee66d4ba6e159ddda2fccf6037b3943321

# `test_production_cli.py`

## Summary
- 実 Codex CLI と case-local Ollama を使い、独立 process・PTY 上で全末端サブコマンドの本番経路を検証する受け入れテスト。CLI 終了 code、report・state・Git・call log、TUI の応答完了と終了処理を確認し、LLM の回答品質は判定しない。

## Read this when
- 全末端サブコマンドの本番経路、独立 process 実行、実 Codex CLI、local Ollama、call log、状態遷移を変更または調査するとき。
- 非対話 command の正常完了、session/run の join・abandon、TUI の PTY 応答完了や終了処理を検証するとき。

## Do not read this when
- 単体テストや mock provider の制御だけを変更・調査するとき。
- LLM の回答品質や個別サブコマンド内部実装を直接検証するときは、対応する実装・より狭いテストを先に読む。

## hash
- aaf76c02aae5a469140980ba6e6b220dee1bd3910e601671b2a8ba372c3dc4ad

# `test_prompt_parts.py`

## Summary
- 標準 prompt parts と complete prompt の組み立て結果を検証するテスト。各標準規則の rendering、prompt への選択的注入、placeholder 展開、file access mode ごとの内容、既定値による省略を回帰検証する。

## Read this when
- prompt builder の標準規則や complete prompt の注入条件を変更するとき
- StructDoc の markdown rendering、placeholder の統合・競合検出、file access mode の出力を検証するとき
- prompt parts に関する回帰テストを追加・修正するとき

## Do not read this when
- prompt builder の実装詳細だけを調査し、テストケースや期待される外部挙動を確認する必要がないとき
- prompt parts や complete prompt と無関係な CLI、パスモデル、StructDoc の変更を扱うとき

## hash
- cda92aecbeee4f02ba3b86cd329065db789d325e3ab3f0a69984b82a6aad5596

# `test_runtime_cli.py`

## Summary
- CLI の error report、console/log 出力、duration 表示、サブコマンドログ、doctor preflight、work root 検証、completion probe の外部契約を検証するテスト。共通 runner における終了コード、例外処理、ログ flush 失敗、Ctrl+C、並列イベント記録、現在の worktree の扱いまで確認する。

## Read this when
- CLI のエラー表示や終了コードを変更・調査するとき
- サブコマンドログ、console log、duration 表示の仕様を変更・調査するとき
- doctor preflight、pre-log check、work root 検証、completion の副作用境界を変更・調査するとき
- 共通 CLI runner の例外処理や終了処理を検証するとき

## Do not read this when
- CLI の個別サブコマンドの業務ロジックだけを変更・調査するとき
- CLI と無関係な parser、状態管理、Git 操作の単体挙動だけを確認するとき
- error、log、preflight、completion の外部契約を経由しない実装を直接確認するとき

## hash
- 2d758f5d6623c0c319c723aaefa6a539f938dbac9e1126493102566ca679f24c

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
- Codex CLI の sandbox argv 生成を検証するテスト。全 FileAccessMode で permission profile や path 別権限設定を注入しないこと、builder API に不要な path 権限引数がないこと、生成した sandbox 引数が実 Codex CLI の parser で受理されることを確認する。

## Read this when
- Codex override 引数、sandbox 設定、permission profile の生成や変更を調査・修正するとき
- FileAccessMode ごとの Codex CLI 実行引数や path 別権限 API の回帰を検証するとき

## Do not read this when
- Codex override 実装そのものの責務や仕様を確認したいときは、参照先の実装・oracle 文書を直接読む
- sandbox や permission 設定と無関係なテスト、CLI 機能、一般的なテスト実行方法を扱うとき

## hash
- c74b31ed3e75231b941ec5ba95d015c193c2eb99abf1f8338728567033e9d560

# `test_runtime_codex_profile.py`

## Summary
- Codex 実行時プロファイルのテスト。file access mode から sandbox・approval・model を含む argv 上書きへの変換、provider 設定の TOML エンコードと未定義 provider の拒否、schema のバイト保持・ハッシュ保存、JSON 読み込み失敗時の扱いを検証する。runtime_codex_profile の契約変更や Codex model/provider 上書き挙動を確認するためのテスト入口。

## Read this when
- Codex argv の model、sandbox、approval、provider 上書き契約を変更または検証するとき
- runtime_codex_profile の schema 保存や output JSON 読み込み挙動を変更するとき
- Codex model provider の未定義・任意キー・再帰 TOML 値に関するテストを確認するとき

## Do not read this when
- Codex 実行時プロファイルや schema/output 処理に関係しない機能を変更・調査するとき
- Codex の正本仕様そのものを確認したいときは、参照されている oracle 文書を直接読む

## hash
- 54867cf498f40b53957007f1ca6f35ba64a01f0da03c24605446bdc0a8fba141

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
- realization refactor の永続 state 同期・検証・target 選択をテストするファイル。oracle/realization file 集合の追跡、履歴保持と変更検出、path・symlink・特殊 file・state schema の拒否、および未調査・最古順の選択規則を扱う。

## Read this when
- realization refactor の state 同期、state の読み書き検証、対象 file の分類、調査対象選択ロジックを変更またはレビューするとき
- refactor state の path 安全性、schema 検証、symlink や特殊 file の扱いを確認するとき

## Do not read this when
- realization refactor の実装詳細ではなく、正本仕様そのものを確認したいときは oracle/doc/app_spec/sub_command/realization_refactor.md と oracle/doc/app_spec/misc_spec.md を直接読む
- refactor state や target 選択に関係しない CLI 機能・別サブコマンドのテストを調べるとき

## hash
- ba1d4a580fe1720514b8d55f0669ee5ec0bcb53aeebbc2f51a133492ea4aebea

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
- bin/cmoc の起動時に、仮想環境の Python 実行ファイルが不足・不正な場合のエラーレポートを検証するテスト。missing venv、通常ファイルでない venv path、Python として起動できない executable を対象とする。

## Read this when
- bin/cmoc の仮想環境検査、起動失敗時の終了コード、標準出力のエラーレポート、Call stack 表示を変更・調査するとき。
- wrapper が仮想環境の異常をどのように利用者へ通知するかを確認するとき。

## Do not read this when
- 補完プローブ環境や通常の CLI 補完挙動だけを変更・調査するとき。
- bin/cmoc 以外の実行経路のエラー処理や、仮想環境検査を伴わない CLI 機能を扱うとき。

## hash
- 3f095faa60df18e5840c6d8e1b7db9df4376d874d974d4b06ea51c439cca62fa

# `test_session_cli.py`

## Summary
- session fork・join・abandon の CLI 外部挙動を統合的に検証する回帰テスト。session branch と永続 state のライフサイクル、rollback・collision・cleanup、linked worktree、dirty worktree、preprocess、merge conflict 解消と安全性を扱う。
- session 状態遷移や関連する CLI エラー報告、Codex conflict-resolution 呼び出しの境界を確認するテストへの入口であり、個別 session サブコマンドの実装詳細ではなく、利用者から観測できる一連の挙動を確認したい場合に読む。

## Read this when
- session fork・join・abandon の外部挙動や回帰テストを調査するとき
- session branch、session state、linked worktree のライフサイクルを追跡するとき
- session join の merge conflict 解消、対象外差分拒否、Codex 呼び出し境界を確認するとき
- dirty worktree 拒否や preprocess、失敗時の rollback・エラー出力を検証するとき

## Do not read this when
- session サブコマンドの内部実装や正本仕様だけを確認したいときは、対応する実装または oracle 仕様を直接読む
- session 以外の CLI コマンドの挙動や一般的な Git ヘルパーを調査するとき
- 単一の低レベル関数の実装詳細・単体テストだけを確認したいとき

## hash
- 747dcda058115e6a69200623c64489cefad1e9a9df623cf8b2c2b7fb020ea986

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
