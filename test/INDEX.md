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
- 実経路統合テスト向けに、case-local Ollama の導入・設定・起動・GPU 推論確認・終了処理をまとめて提供するテスト支援モジュール。共有 cache の安全な検証、atomic publish、独立した working set、pytest runner も扱うため、Ollama を使う統合テストの入口となる。

## Read this when
- Ollama を使用する実経路統合テストの実行環境、cache、model 構築、GPU-only 推論、process group の teardown を調査・変更するとき
- test case から case-local Ollama provider を設定する方法や、専用 pytest runner の挙動を確認するとき

## Do not read this when
- Ollama を使わない通常のテストや、アプリケーション本体の model provider 実装を調査するとき
- テスト実行全体の選択・品質検査手順を確認したいときは、まず test execution の正本仕様を読む

## hash
- c96f1fa7b5a180f33e64ebf941c45a1711c31c3dd36a3fcedf848b04ec430003

# `test_acp_builder_editing_run_parameters.py`

## Summary
- editing run workload の canonical builder adapter を検証するテスト。apply 用 builder が commit 範囲・raw diff・実行規則を prompt に埋め込むこと、refactor 用 builder が canonical Structured Output schema と実行設定を使うことを確認する。

## Read this when
- editing run の realization apply/refactor builder の prompt 構成、実行設定、Structured Output schema、raw diff の境界処理を検証または変更するとき。

## Do not read this when
- builder 実装そのものの仕様や変更内容を確認したいときは、テストが対応する oracle file と各 realization builder 実装を直接読む。
- editing run と無関係な builder、または一般的な Git worktree fixture の挙動だけを扱うとき。

## hash
- a906168c8878b853cb6354fbb3f45b9e96e77a5b449e5aa151453cc129b80b5d

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
- Codex 実行ランナーとテスト用ローカル Ollama の統合契約を検証するテスト群。pytest の一時領域と Ollama cache の分離、cache 再利用・再構築、current worktree の import、Codex 環境分離、Codex CLI の argv・stdin・override・出力・schema 配置、汎用 provider 利用、実 Codex CLI と Ollama の結合動作を扱う。Codex 実行経路や Ollama テスト基盤の挙動を変更・調査する際の検証入口。

## Read this when
- Codex CLI 実行の argv、prompt の stdin 渡し、sandbox・approval・override 契約を変更または確認するとき
- テスト用ローカル Ollama の cache 選択、既存 model の再利用、install cache の再構築、実行環境分離を変更または確認するとき
- run_codex_exec、prepare_codex_override_args、共通 Codex/Ollama test helper の統合動作を検証するとき

## Do not read this when
- Codex 実行や Ollama の実装を直接理解・変更することが目的で、まず対象の realization implementation や oracle 仕様を読むべきとき
- このテスト群が対象としない一般的な pytest 実行、CLI 機能、または unrelated な provider の挙動を調べるとき

## hash
- 92e17c3771e48773696c4e0e3766ef299910d93f7d832755d8c6675d334bf331

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
- Codex exec の実運用呼び出しにおけるログ・出力パスの衝突回避、agent call の cwd、schema 保存先、sandbox 引数を検証する統合テスト。
- 同一 timestamp の並列実行、リンク済み worktree、PURE_ORACLE_READ と REPO_WRITE、.agents パスの扱いなど、Codex 実行境界の回帰検証への入口。

## Read this when
- run_codex_exec の cwd、sandbox モード、schema 出力先、ログ・出力パス予約の挙動を変更または検証するとき
- リンク済み worktree や並列実行時の Codex 呼び出しの回帰を調査するとき

## Do not read this when
- Codex 実行境界ではなく、プロンプト生成、ファイルアクセス規則そのもの、または個別のテスト支援関数を直接調べるとき
- run_codex_exec の外部挙動を変更しない一般的なテスト実行や別機能のテストを扱うとき

## hash
- bcb897854ccb08e5c616379e214cf6ece1ca038a49e06866de8ce7826f92fe06

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex quota exceeded 後の probe・待機・resume・再実行を検証する回帰テスト。代表 probe の共有、session ID 復元、quota/capacity retry、並行呼び出し、失敗伝播、call log・subcommand log、CODEX_HOME と cwd の扱いを同一の retry 状態機械として扱う。

## Read this when
- Codex exec の quota 復帰、probe、resume、再実行、quota polling の挙動を変更または検証するとき
- quota 待機中の並行呼び出し、probe 失敗、ログ記録、session ID 復元の回帰を調査するとき

## Do not read this when
- Codex exec の通常成功・一般的な subprocess 実行だけを調べるとき
- quota retry と無関係な prompt 構築、設定、または別の実行経路を直接調べるとき

## hash
- 114395fbebf31845ed23367f4e7d18e0648b6b6c9881569137745424a2eb1836

# `test_codex_runtime_retry.py`

## Summary
- Codex exec の Structured Output 補正、capacity retry、JSONL error、中断、retry 上限、差分保持を、最終結果・subprocess 呼び出し回数・call log・subcommand event の外部挙動として検証する異常系テスト。Codex 実行の retry 状態機械や共有ログ schema を確認する入口。

## Read this when
- Codex exec の retry、Structured Output 検証・補正、capacity failure、JSONL error、KeyboardInterrupt、成果物差分保持の挙動を変更または調査するとき。
- Codex call log と subcommand event の status、returncode、error、呼び出し順を検証するとき。

## Do not read this when
- 通常の Codex exec 成功経路や prompt 生成だけを確認するときは、実行実装または対応する正本仕様を直接読む。
- 他の CLI サブコマンドや Codex 以外のログ機能のテストを探すとき。

## hash
- 987b4a754eef73ebdc3d986b44868bd9b22af0f70d26a0509da9ecb351d1124d

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
- workload fork と共通 editing run lifecycle の統合テストを扱う。realization apply/refactor の fork、run join/abandon、session state、run worktree、Git 差分、INDEX 更新、process tracking、report、rollback、cleanup の連携と異常系を検証する。
- apply/refactor の各実装単体ではなく、共通 lifecycle fixture を介した状態遷移や成果物の統合挙動を確認するためのテスト入口である。

## Read this when
- realization apply または refactor の fork と run join/abandon の連携を変更・レビューするとき。
- run の state 遷移、worktree・branch の作成/削除、process tracking、Codex child の停止、INDEX refresh、report 生成、rollback の統合挙動を確認するとき。
- unexpected な oracle・INDEX・realization 差分、rename/delete、force-resolve、merge conflict、interrupt、cleanup failure などの境界条件を調査するとき。

## Do not read this when
- 単一の lifecycle helper や sub-command の内部実装だけを確認する場合は、対応する実装とより直接的な単体テストを読む。
- 一般的な INDEX 生成規則や正本仕様を確認する場合は、この統合テストではなく対応する oracle 文書を読む。
- fork と join/abandon を含まない通常の CLI 挙動や、無関係なテスト領域を調査する場合。

## hash
- cbe193eee16e612b6544b52a9321b63f01394f0fde4142afba4d1d66078f4038

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
- Codex exec／TUI 呼び出し直前の indexing preflight のテスト群。preflight の実行順序、対象 root／linked worktree の選択、repository lock 待機、パラメータによる無効化、および file access violation 後に recovery indexing を行わない制約を検証する。indexing と Codex 呼び出しの統合挙動を確認する realization test の入口。

## Read this when
- Codex 呼び出し前の indexing preflight の動作、実行順序、対象 worktree 選択を変更または検証するとき
- repository lock による preflight の待機や、preflight 無効化条件を変更するとき
- file access violation 発生時の recovery 方針や Codex 呼び出し回数を変更するとき

## Do not read this when
- INDEX.md の生成ロジック自体や indexing 実装の詳細を確認したいときは、indexing 実装側のテストまたは仕様を直接読む
- Codex CLI 呼び出し単体の引数・結果処理を確認したいときは、Codex runtime の実装・テストを直接読む
- preflight と無関係な CLI 経路や一般的な repository test fixture を扱うとき

## hash
- 7dd35c562ccb6e88dc06a7a73aee87930908a29cb85c44c0564a2abe2c14cb0f

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
- oracle review の finding loop 回帰テスト。finding の対象別引き継ぎ、main worktree のパス照合、challenger/advocate の同一周回理由、interrupt 時の部分結果復旧、merge の postcondition と失敗伝播を fake Codex call で検証する。oracle review のループ挙動や Structured Output 呼び出し契約を変更・調査するときの入口となる。

## Read this when
- oracle review の finding 列挙・検証・判定ループを変更またはレビューするとき
- finding の partial progress、retry、interrupt 復旧、merge 入力条件の回帰を確認するとき
- oracle review が Codex call の worktree、purpose、Structured Output 契約を満たすか検証するとき

## Do not read this when
- oracle review の実装詳細を直接調査する場合は、まず review loop 実装を読むとき
- oracle review 以外のサブコマンドや一般的なテスト規約だけを確認する場合

## hash
- 1d68a2d1286f19d8fc2e7fcc7f3e4f39ca02afc02e7129c36128c98f78818422

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
- prompt parts と complete prompt の回帰テストを集約し、各標準 prompt の rendering、選択的な注入、placeholder 展開、file access mode ごとの内容を検証する。
- prompt builder の実装や標準規則を変更・検証する際の realization test の入口であり、個別の prompt part の詳細は対応する実装ファイルを読む。

## Read this when
- prompt part の rendering や complete prompt の組み立て挙動を変更・調査するとき
- standard の注入条件、placeholder の統合・競合、file access mode の差異を検証するとき
- prompt builder 回帰テストの対象範囲を確認するとき

## Do not read this when
- prompt builder の実装詳細だけを確認したいときは、対応する src の prompt part または complete prompt 実装を直接読む
- prompt の正本仕様や標準規則そのものを確認したいときは、oracle 側の仕様ファイルを読む
- prompt builder と無関係なテストや機能を調査するとき

## hash
- fbd8c486f527e613515e9633ca2bf1eddc6724bed295a5d9c19247422f8737aa

# `test_runtime_cli.py`

## Summary
- CLI の共通 runner と終了処理を通じた error report、console log、preflight、shell completion の外部契約を検証するテスト。
- duration 表示、サブコマンドログの衝突・並列書き込み、doctor preflight、CLI 解析エラー、work root 制約、completion probe、KeyboardInterrupt、終了コードを扱う。
- CLI lifecycle の複数境界を横断して確認するため、個別の error・log・preflight・completion テストではなく、共通 runner の挙動を調査・変更するときの入口となる。

## Read this when
- CLI の error report や終了コード、stdout/stderr 出力を変更・調査するとき
- サブコマンドログ、runner、doctor preflight、work root 判定の挙動を変更・調査するとき
- shell completion probe が通常の CLI 初期化や副作用を回避する境界を変更・調査するとき
- duration 表示または並列 logger の挙動を変更・調査するとき

## Do not read this when
- CLI の業務処理そのものや、特定サブコマンドの実装だけを変更・調査するとき
- error report の仕様、ログ形式、completion、doctor preprocess の正本仕様を確認するときは、対応する oracle 文書を直接読む
- CLI と無関係なテストや、共通 runner・終了処理を通らない単体処理を調査するとき

## hash
- 7520ad8a76eaed8d8e9ab20ef600e2f6f72e12ed4d77742a4b6ca64a90ddfadc

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
- 対象は、Codex CLI に渡す sandbox argv が permission profile に依存しないことを検証するテストです。permission mode ごとの sandbox 引数受理と、path-based permission 入力を builder API が受け付けない契約を扱います。runtime Codex permission argv 実装のテスト入口として読みます。

## Read this when
- Codex override argv の生成仕様や permission mode 別の CLI 引数受理を変更・調査するとき
- path 別の read/write 例外を builder API に渡す入口が残っていないことを検証するとき
- Codex CLI の sandbox 引数互換性に関する realization test を確認するとき

## Do not read this when
- Codex permission argv の実装詳細そのものを確認したいときは、runtime Codex profile の実装を直接読む
- Codex CLI 以外の permission、sandbox、または一般的な subprocess テストを扱うとき
- このテストの実行方法だけを確認したいときは、リポジトリのテスト実行手順を直接読む

## hash
- 5c5b1bcc7012fea9d7929919ca98cf8bb9cb85e61003e1a66d0ba4015af5bfe8

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
- session fork・join・abandon の CLI 外部挙動を、実 Git リポジトリと session state を用いて回帰検証するテスト群。
- session branch/state の生成、衝突、rollback、cleanup、linked worktree、dirty worktree 拒否、merge/conflict 解消、不要差分検出、エラー出力を扱う。
- session ライフサイクルと branch/state 遷移に関するテスト実装へ進む入口であり、個別サブコマンドの実装詳細や正本仕様そのものの入口ではない。

## Read this when
- session fork、join、abandon の外部挙動や回帰テストを確認・変更するとき
- session state、managed branch、linked worktree のライフサイクル検証を調べるとき
- session join の conflict resolution、sandbox、不要差分、エラー出力のテストを確認するとき

## Do not read this when
- session CLI の実装挙動そのものを変更・調査する場合は、対応するサブコマンド実装や正本仕様を先に読むとき
- session state のスキーマやライフサイクル契約を確認する場合は、session state の正本仕様を直接読むとき
- 一般的な CLI、Git helper、Codex 実行規則だけを調べる場合

## hash
- fbdc8ebef81bda8d2b01754401be6f53de065f1b6faf335b986974f93dd573c4

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
