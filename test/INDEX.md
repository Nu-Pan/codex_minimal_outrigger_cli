# `_acp_builder_support.py`

## Summary
- テストから acp_builder の正本 schema を参照するための共有 helper。schema を複製せず、参照先の Path を返します。

## Read this when
- acp_builder の正本 schema を使うテストを追加・修正し、テスト側の参照先を確認するとき。

## Do not read this when
- 正本 schema の定義や仕様を確認・変更するときは、schema 自体を参照するとき。
- acp_builder の実装動作を調べるときや、schema を使わないテストを扱うとき。

## hash
- 6fd184bad0b16e6bce9c32dac57e2187a8272303ece3f3c8d350acaeacf5824b

# `_cli_support.py`

## Summary
- CLI テストで共有する呼び出しと出力解析の補助をまとめる。指定した worktree で doctor を実行して終了コードを確認し、CLI 出力から primary report のパスを取得する。
- CLI テストで使う共有の CliRunner も提供する。

## Read this when
- CLI テストで doctor を対象 worktree 上で実行したいとき。
- CLI の結果や出力から primary report のパスを取り出したいとき。
- 複数の CLI テストで共有している CliRunner を確認したいとき。

## Do not read this when
- コマンドの仕様や診断・レポート内容を調べるときは、該当する仕様またはコマンド実装へ直接進む。
- cwd の切り替えや排他制御の挙動が論点なら、ディレクトリ切り替えユーティリティへ直接進む。

## hash
- 77fc1a0c23afa228b0235135b24525d1823f6332923c8ea7c430c89dc6871020

# `_codex_support.py`

## Summary
- Codex runtime・CLI テストで共用する fake result と、テスト環境・parameter・CLI 引数の準備や解析を行う helper を提供する。
- 複数の Codex 関連テストが使う共通支援コードを変更・調査するときの入口。

## Read this when
- Codex runtime や CLI のテストで、隔離した Codex 環境、共通 parameter、fake result、固定 override 引数を使うとき。
- 複数のテストで共有する Codex 引数・設定の解析 helper を変更するとき。

## Do not read this when
- 個別テストの挙動を調べるだけで共通 helper が関係しない場合は、そのテストと対象の runtime 実装を直接確認する。

## hash
- 5d1587851c20ed65a62cf640cbbfa2b218412580743e9ac569d6227b722ef394

# `_command_support.py`

## Summary
- テストから起動する偽の外部コマンド用に、Python スクリプトを書き込み、実行可能にする共通ヘルパー。
- 個々の偽コマンドの処理や製品動作は定義せず、複数のテストが使うスクリプト生成処理を担う。

## Read this when
- テストで起動する偽の外部コマンドについて、スクリプトの作成方法や実行権限の付与方法を確認・変更するとき。
- 複数のテストで共有する偽コマンド生成処理の利用例を確認するとき。

## Do not read this when
- 製品コードの外部コマンド実行や、その動作を検証する個別テストの内容を調べるときは、それぞれの実装やテストを直接読む。
- テストで実行可能な Python スクリプトを生成しない場合。

## hash
- 37672f2473fdf889a2210635d4294e5f807fefd04034b00449f411bffcf86ae8

# `_git_support.py`

## Summary
- CLI テストで共有する一時 Git リポジトリ用ヘルパーを提供し、Git コマンドの実行、現在ブランチの取得、初期 commit 済みリポジトリの作成、ignore 対象だが追跡済みの oracle file の fixture 作成を担う。

## Read this when
- テスト用リポジトリの共通初期状態や、Git コマンド実行・ブランチ取得のヘルパー動作を調査または変更するとき。
- ignore 対象だが追跡済みの oracle file を使うテスト fixture の作成方法を確認するとき。

## Do not read this when
- 特定サブコマンドの挙動や個別テストケースを調べるときは、該当する実装やテストへ直接進む。
- 本番コードの Git 操作や ignore 判定の仕様・実装を調べるときは、その正本仕様や本番コードへ直接進む。

## hash
- 1ecaade4dee17221fe4bca8c1837bef8e9d28957fd6bee025a6b52c299aea9e1

# `_handoff_support.py`

## Summary
- handoff 関連テストで共有する入力値と、正本 builder を使った期待本文を作るテスト補助。

## Read this when
- editor input handoff の MCP、ライフサイクル、TUI 連携テストで共通の入力や期待本文の生成元を確認するとき。

## Do not read this when
- handoff 本文の仕様やレンダリングを確認するときは、正本仕様または body builder を直接読む。
- MCP 応答や target の動作を調べるときは、実装または個別のテストを直接読む。

## hash
- 0bf82cfbb81f22d3a0345534414f77b906a61181b469c36b8a9e3d8b260afc31

# `_real_path_integration`

## Summary
- 実経路統合テストの子プロセスで、AI 呼び出しパラメータのモデル設定を最小モデル・低い推論強度に固定するテスト用フックを担う。

## Read this when
- 実経路統合テストの子プロセスで適用されるモデル設定や、そのテスト用上書きを調べる・変更する場合。

## Do not read this when
- ACP の一般的な型や本番時のパラメータ構造を調べる・変更する場合は、テスト用上書きではなく正本の ACP 型定義を直接確認する。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `conftest.py`

## Summary
- pytest 全体で使う Windows toast の外部副作用隔離と、editor input handoff 用 MCP context を準備する共有 fixture を定義する。
- テスト共通の隔離設定や handoff 用 context の準備を変更するときの入口。

## Read this when
- 複数のテストに適用される Windows toast の隔離方法を変更するとき。
- editor input handoff のテストで共有する送信元 context や環境変数の準備を変更するとき。

## Do not read this when
- Windows toast の個別動作や handoff protocol の詳細を調べるときは、対応する実装・仕様・個別テストから確認を始める場合。

## hash
- 89282cf36f1b504ac55859e2268d465bac3bfaa45fff87a0b807fa3532ca791f

# `test_acp_builder_editing_run_parameters.py`

## Summary
- realization apply/refactor の編集 run 向け builder adapter が、正本 builder を再公開し、各フローの起動パラメータを設定する契約を検証する。
- apply では commit 範囲を使う追従 prompt と実行設定を、refactor では変更要約とファイルレビュー・修正それぞれの prompt、実行設定、正本 schema との対応を確認する。

## Read this when
- realization の apply run が commit 範囲や閲覧範囲をどう prompt に反映し、どの実行設定で起動するかを確認・変更するとき。
- refactor の変更要約またはファイルレビュー・修正 builder の起動設定や正本 schema との対応を確認・変更するとき。
- 編集 run 向け builder の互換入口と正本 builder の結び付きに関するテスト失敗を調べるとき。

## Do not read this when
- prompt の本文や schema の定義自体を調べるときは、該当する正本 builder または schema から確認するとき。
- session join の競合解決や TUI 起動 builder のパラメータを調べるときは、それぞれの専用テストから確認するとき。
- 共有 repository fixture や schema 参照 helper の挙動を変更・調査するときは、その helper の実装から確認するとき。

## hash
- 13ddc8bad493aa0b3349a498210a3b93d269d9c4990b6016660b3ba606986fb7

# `test_acp_builder_session_join_parameters.py`

## Summary
- session join の競合解消パラメータ builder について、リポジトリ書き込み権限、作業ディレクトリ、閲覧範囲、構造化出力スキーマ、および prompt に渡す commit 参照の契約を検証する。
- 互換 import 経路が builder のみを公開し、正本の実装と同じ関数を参照することも検証する。

## Read this when
- session join 固有の競合解消 call の入出力契約や互換 import の公開範囲を確認・変更するとき。
- この builder の契約に対する回帰テストを追加・修正するとき。

## Do not read this when
- パラメータ構築自体の実装を変更するときは、正本の builder 実装を直接確認する。
- run join と session join に共通する競合解消 prompt の意味や Git からの情報取得方法を変更するときは、共通 prompt builder とその仕様を直接確認する。

## hash
- 9b26551fa0e7bf21887c2d2c2e84bc196539b246800f7d42f21492b910945bb1

# `test_acp_builder_tui_parameters.py`

## Summary
- TUI 起動 builder の固定 parameter、prompt の組み立て、互換 module の公開面を回帰検証する。editor input handoff の有効化と、起動時に handoff log が作られないことも確認する。

## Read this when
- TUI 起動 builder の parameter や prompt の構成・規定が変わった原因を調べるとき。
- 互換 module の公開範囲や、公開 builder が正規実装と同一であることを確認するとき。

## Do not read this when
- 起動 builder が組み込む規定の意味や正本上の期待動作を確認するときは、対応する正本の定義へ直接進む。
- 別の ACP builder の parameter や prompt の回帰を調べるときは、その builder に対応するテストへ進む。

## hash
- bc429d3796412f43d55e61dfc46b8a1c07cc95b9e99e50c6e3bca10197df331a

# `test_basic_runtime.py`

## Summary
- repo-root / work-root と root placeholder の解決を、Git repository・worktreeの違いや並行処理を含めて検証するruntime回帰テスト。
- cmoc管理run worktreeのbranchとpathの対応、作成・検索・削除時のsymlinkや無効なGit登録の拒否、およびテスト用repositoryのGit設定分離も確認する。

## Read this when
- root placeholderやagent-call path contextが、main・linked worktreeやnested repositoryなどでどう解決されるかを調べるとき。
- 管理run worktreeのpath対応や、安全な作成・検索・削除の回帰を調べるとき。

## Do not read this when
- root placeholderの正本実装やbranch・run worktreeの命名とlifecycle規約を確認・変更するときは、それぞれの正本へ直接進む。
- 時刻・ログ形式やrun processの停止など、このテストが扱わないruntime責務を調べるときは、その責務の実装へ直接進む。

## hash
- 9942c6dcd1ebb9875a3cacf18573018053cbbc306956d52ee8c53ef0dcfbc1b8

# `test_cli_command_tree.py`

## Summary
- 公開 CLI の末端コマンド構成、help の描画、Typer と Click の互換性、および feedback report の引数・option の有無を検証するテストです。
- CLI の公開構成や help の形を確認するときに、実行時のコマンド動作を扱うテスト群と区別して参照します。

## Read this when
- 公開 CLI コマンドの追加・削除・階層変更が期待される末端コマンド集合に反映されているか確認するとき。
- Typer と Click の help 互換性や feedback report のコマンド固有引数・option を変更するとき。

## Do not read this when
- 個別コマンドの登録や CLI 構成の定義を調べるときは、CLI の構成を定義する実装を直接確認してください。
- コマンドの実行処理、引数解析エラー、実行時の副作用を調べるときは、それらを扱う実装や実行時テストから確認してください。

## hash
- 77aebc373c15cf6692bb9c39a413565fdefa923862c1df11f90e805a52bf85e8

# `test_cli_tui.py`

## Summary
- `tui` と Oracle investigation/edit に共通するエディター入力の確定保存について、保存失敗時の入力保全と agent 呼び出しの抑止を検証する。
- `tui` CLI の前処理から Codex TUI 起動までの外部挙動を扱い、編集済みプロンプト、Git 差分の保持、linked worktree 利用時の作業コンテキストとログの配置を確認する。

## Read this when
- `tui` CLI の Doctor 前処理、プロンプト編集、起動パラメータ構築や起動順序を変更するとき。
- TUI 実行時の main worktree と linked worktree のコンテキスト、入力ログ、`.cmoc` の ignore 動作を変更するとき。
- TUI または Oracle investigation/edit から使う共通エディター入力の確定保存失敗時の挙動を変更するとき。

## Do not read this when
- 共通エディター入力の保存形式、編集処理、入力検証や handoff の内部動作を調べるときは、その処理を直接扱うテストを読む。
- Codex TUI プロセスの実行、呼び出しログ、通知や handoff の runtime 挙動を変更するときは、runtime 専用テストを読む。
- Doctor 前処理自体や Oracle investigation/edit 固有の CLI フローを変更するときは、それぞれを直接扱うテストを読む。

## hash
- f1f30ec5b2ece55508b0b88f4ad1cf6e84a3e800029bd9e4dc88984767d168cd

# `test_codex_runtime_errors.py`

## Summary
- Codex exec の JSONL 異常入力の失敗扱いと、Codex CLI 不在時の例外・失敗ログを確かめるテスト。
- Codex 実行の異常系のうち、破損した JSONL と CLI 起動時の不在を扱う。

## Read this when
- Codex exec が不正な JSONL を受け取った場合の失敗分類や、CLI 不在時の起動失敗とログを確認するとき。

## Do not read this when
- 有効な JSONL に対する quota・一時障害の分類、再開や再試行を調べるときは、Codex の回復・再試行テストへ進む。
- TUI 経由の Codex 呼び出しで CLI 不在時の挙動を調べるときは、TUI の実行テストへ進む。
- Codex 実行の規範的な挙動を確認・変更するときは、テストではなく正本仕様を読む。

## hash
- 07979859bab4cda55abd4b43e4dc967a660621050bc3eadf13c4875315480b73

# `test_codex_runtime_exec.py`

## Summary
- Codex exec の通常起動について、CLI 引数と設定上書き、作業ディレクトリ、prompt の stdin 渡し、結果の読込をテストする。
- 実行環境の分離、汎用 model provider の設定反映、CODEX_HOME に設定ファイルを作らないこと、schema なしの出力に不正 UTF-8 が含まれる場合の扱いも確認する。通常 exec の呼び出し契約を調べる入口となる。

## Read this when
- Codex exec に渡す引数や設定上書き、作業ディレクトリ、prompt の stdin 渡しを確認・変更するとき。
- model provider の設定反映や、Codex の設定ファイルを生成しない実行環境の扱いを調べるとき。
- Structured Output schema を使わない場合の出力読込、特に不正 UTF-8 の扱いを確認するとき。

## Do not read this when
- Structured Output の検証・補正、postcondition、容量回復や再開を調べるときは、出力補正や回復処理を扱うテストから確認する。
- Codex 子プロセスの追跡、停止、PID の同一性確認などを調べるときは、プロセス管理を扱うテストから確認する。

## hash
- ebc007d7ca7eab3f2ec012970839a4777a728997189f7af2426147b3219e6db8

# `test_codex_runtime_home.py`

## Summary
- Codex 実行時の home 選択、相対パス解決、および欠落・非ディレクトリ時の起動前検証を確認するテストです。
- auth.json の有無や種別を home 検証の前提にしないことも確認します。

## Read this when
- `run_codex_exec` の `CODEX_HOME` 未設定時の既定値、設定値の保持、相対パス解決、または起動前検証を変更・調査するとき。
- Codex home の検証が `auth.json` の有無や種別に依存しないことを変更・調査するとき。

## Do not read this when
- Codex 実行の引数、結果処理、その他の挙動を調べるときは、該当する実装・仕様・専用テストを直接確認してください。
- Codex home の検証実装自体を調べるときは、検証関数の定義を直接確認してください。

## hash
- e41bbb7111d976975c0749de36062985fad0ee0b5a84c1ea32bec9f2d77ea514

# `test_codex_runtime_paths.py`

## Summary
- Codex 実行時の作業ディレクトリ、sandbox 引数、linked worktree での schema 保存先を検証するテスト群。
- 同じ timestamp を使う並列実行でも、ログと出力のパスが衝突しないことを確認する。

## Read this when
- run_codex_exec の cwd 伝播や、linked worktree からの実行時に schema を保存する場所を変更・調査するとき。
- PURE_ORACLE_READ の sandbox 引数や、実在する .agents パスの扱いを変更・調査するとき。
- 並列実行時の timestamp 付きログパス予約を変更・調査するとき。

## Do not read this when
- Codex CLI の一般的な argv 構成や起動契約を調べるときは、実行契約を扱うテスト群を先に読む。
- subprocess の timeout、中断、停止や process group の扱いを調べるときは、subprocess のライフサイクルを扱うテスト群を読む。
- sandbox 設定 builder の API や permission profile への依存を調べるときは、その設定生成を直接扱うテスト群を読む。

## hash
- 436f37bdb11c13d255ce536ac29f7ec37de72db15896839e9088bb227f1a6ce5

# `test_codex_runtime_quota_retry.py`

## Summary
- Codex 実行で quota 枯渇を検出した後の回復確認 probe と、元の処理を再開または再実行する経路を検証するテスト群です。
- probe の失敗・中断・ログ記録や、並行呼び出しで probe を共有する動作も扱います。

## Read this when
- quota 待機後の回復確認、session 再開または prompt 再実行、並行呼び出し間の結果共有を調べるとき。
- quota probe の生成・実行条件、失敗時の伝播や記録、Codex の実行環境に関するテストを変更するとき。

## Do not read this when
- quota 待機に関係しない Codex CLI の一般的な起動や引数の動作を調べるときは、通常の実行・subprocess のテストから確認してください。
- Structured Output の補正や capacity retry、回復処理全般の状態遷移を調べるときは、それぞれに焦点を当てたテストから確認してください。

## hash
- 439773b70f92a3cdf91945bd7d039f272018d8715b0e72de384e8cbad3ef0e35

# `test_codex_runtime_recovery.py`

## Summary
- Codex exec の JSONL 終了結果の分類と、回復待ち・確認 probe 後の同一 session 再開を検証するテスト。
- 回復理由の切替、設定継承、Structured Output 補正中の回復、中断処理、条件が一致する並列 call の probe 共有も扱う。

## Read this when
- quota や capacity を含む JSONL 結果の分類、回復待ち・probe・session 再開の動作を変更または調査するとき。
- 設定継承、補正中の回復、中断の優先、並列 call 間の probe 共有を確認するとき。

## Do not read this when
- 回復後の呼び出しを対象とせず、Codex exec の通常起動時の引数や provider 設定だけを調べるときは、通常起動のテストを直接読む。
- 対話型 Codex TUI の起動・終了や通知フックを調べるときは、TUI 専用のテストを読む。

## hash
- aa87e4c68fe649e580f908cfeec3cb73d9adfb49051926facf48cd412a31d6f7

# `test_codex_runtime_retry.py`

## Summary
- Codex 呼び出しの Structured Output が欠落・不正・契約違反のときの補正、再試行上限、事後条件の検証、失敗時の成果物復元を確認する。
- capacity error の再試行と作業差分の保持に加え、stdout JSONL の error による retry 判定、call event や中断時の記録を扱う。

## Read this when
- Structured Output の補正、session の再開、補正上限、補正中に生じた成果物の変更の復旧を変更・調査するとき。
- capacity error の再試行ログや作業差分の保持、stdout JSONL の error を使う retry 判定、中断時の記録を変更・調査するとき。

## Do not read this when
- quota の probe・polling・共有や、回復理由の分類・設定継承・同時実行制御が対象なら、それらを直接扱うテストから読む。
- 不正な JSONL event の parser 分類や CLI 不在時の一般エラー、Codex の起動引数・home・subprocess が対象なら、それらを直接扱うテストから読む。

## hash
- 0ab648cf19afd959d506b4b245da468f2637a043a829e45ce0a6dd74d04215b9

# `test_codex_runtime_subprocess.py`

## Summary
- Codex subprocess の起動・追跡実行と、run 子プロセスの停止処理に関する回帰テスト。期限や割り込み、tracking の検証・更新、プロセス同一性の確認、process group の cleanup、起動 callback の境界を扱う。

## Read this when
- Codex subprocess の起動、キャンセルや timeout、child tracking、起動 callback、終了時の cleanup の挙動を調べたり変更したりするとき。
- run の子プロセス tracking や、leader 終了後を含む process group の安全な停止・同一性確認を調べたり変更したりするとき。

## Do not read this when
- Codex の argv や profile 設定、retry、quota、TUI など subprocess の起動・追跡・停止に関係しない runtime 挙動を扱うとき。
- apply/refactor の CLI ワークフロー、run state、commit、rollback など呼び出し元の統合動作を扱うときは、そのワークフローを直接検証するテストから確認するとき。

## hash
- 2893f867c3ff571d08c7983f73b53027556ed0283114e3b25184cb32a5efa447

# `test_codex_runtime_tui.py`

## Summary
- Codex TUI の起動経路について、prompt と CLI 設定、通知フック、worktree のアクセス境界を検証する回帰テスト。
- TUI 呼び出しの成功・失敗ログと、並行する editor-input MCP handoff の送信元対応を検証する。

## Read this when
- Codex TUI の起動設定、バージョンに応じた通知フック、設定検証やシェル補完中の挙動を変更・調査するとき。
- TUI のログ記録、worktree での prompt・handoff、並行呼び出し時の送信元対応を変更・調査するとき。

## Do not read this when
- Codex exec の prompt stdin、出力処理、結果構築を調べるときは、exec 経路のテストを直接読む。

## hash
- f8c1590da9efbf22d28178bf61c08701a25070929beb1a1e15c3383032a045b8

# `test_doctor_cli.py`

## Summary
- doctor preprocess の CLI と直接呼び出しを通じ、Git ignore、`.agents`、config、refactor state の修復と reporter 利用不能時の挙動を統合的に検証する。
- repository と linked worktree にまたがる排他 lock、修復 commit の範囲、既存の staged・unmerged 変更や index 状態の保持を確認する。

## Read this when
- `cmoc doctor` の修復内容・処理順・CLI 報告や、reporter 利用不能時の継続と中断の扱いを確認・変更するとき。
- linked worktree を含む doctor の lock と修復範囲、修復失敗時も含む既存 Git index の保持を調べるとき。
- doctor が `.agents`、`.cmoc/gu`、config、refactor state を Git と同期する動作を確認するとき。

## Do not read this when
- doctor から独立した config の形式・読み込み・検証や、refactor state の inventory・hash 算出を調べるときは、それぞれの機能を直接検証するテストから読む。
- Git ignore の低水準な判定・パス検証、reporter の MCP protocol や probe 内部、doctor 以外の CLI 共通報告を調べるときは、それぞれの機能を直接検証するテストから読む。

## hash
- 8cf2da3ddbdce7f27a2236c4217f5f447279f31cade736c3ccf1f270189f15d9

# `test_document_search.py`

## Summary
- 文書検索の許可範囲、本文変更への同期、索引再利用、失敗の識別、stdio MCP と推論 worker の取消、および明示同期コマンドの回帰テストをまとめ、これらの挙動変更時の確認先となる。

## Read this when
- 検索対象の範囲制御、本文の追加・変更・削除・空白化、検索結果の鮮度や cache 再利用を変更するとき。
- stdio MCP の検索公開・失敗応答、または推論 worker の取消とプロセス回収を変更するとき。
- 明示同期コマンドの未コミット差分の扱いや、未準備時の失敗報告を変更するとき。

## Do not read this when
- 検索の正本要件や明示同期コマンドの仕様を確認・変更するときは、対応する仕様書を直接読む。
- editor input handoff の MCP 挙動だけを扱うときは、その機能専用のテストから確認する。

## hash
- ac591650ecc50ed5920f39e6d3fbe5edfd01770d510154ebd775394642908f27

# `test_editing_run_cli.py`

## Summary
- realization apply/refactor fork と共通 run join/abandon の統合テストを扱う。独立 worktree、state 遷移、差分の検査と merge、process 停止、report、rollback・cleanup・中断時の復旧をまたいで検証する。

## Read this when
- apply または refactor の fork 結果が run state や worktree にどう反映され、join 可能になるか確認するとき。
- run の join・abandon で、merge conflict、想定外差分、process tracking、cleanup 失敗が state や report とどう連動するか調べるとき。
- editing run の開始から完了・中断まで、複数コマンドにまたがる回帰を追うとき。

## Do not read this when
- 共通 CLI runner の error、log、preflight、completion だけを調べるときは、CLI lifecycle 全般を扱うテストから確認する。
- session branch 自体の fork・join・abandon と state の挙動だけを調べるときは、session CLI のテストから確認する。
- apply/refactor 用 agent parameter や prompt の builder 契約だけを調べるときは、builder 専用テストから確認する。

## hash
- 3625f308d392d69ad18d425cf3b5f85aed86701899c76aec614d4fb99cba73a5

# `test_editor_input_handoff.py`

## Summary
- エディターの待機中に MCP 経由で送られる入力の受け渡しを検証します。target の有効期間、リポジトリとの対応、接続認証、上書きの安全性と完了境界を確認する入口です。

## Read this when
- エディター待機中の入力受け渡しで、どの target が受理されるか、上書きがいつ確定するか、終了時や異常な接続で入力を保護できるかを確認するとき。

## Do not read this when
- MCP の JSON-RPC、公開ツール、入力検証やエラー応答の契約を確認するときは、MCP インターフェースを直接扱う項目へ進んでください。
- 入力ファイルの予約、エディター選択、終了後の読み取りや保存を確認するときは、エディター入力の外部挙動を扱う項目へ進んでください。

## hash
- 088bde51380894981f43f6047b770565f86fa008ea589eda7f25ed4cf3ea4fa9

# `test_editor_input_handoff_mcp.py`

## Summary
- Codex TUI から呼び出される editor input handoff の stdio MCP interface と、guide 取得・overwrite の応答契約を検証する。
- 入力と送信元の検証、正本の本文生成との連携、入力内容を漏らさない失敗応答、送信結果が不明な場合の扱いも確認する。

## Read this when
- MCP tool の公開、JSON-RPC request の検証、guide・overwrite の呼び出しや応答変換を変更・調査するとき。
- 入力内容の秘匿、受付結果と送信結果不明の区別、正本の本文生成へ渡す連携を確認するとき。

## Do not read this when
- 待機中 target の開始・終了、server 側の上書き受理、書き込み先の検証や安全性だけが対象なら、target の lifecycle と上書き境界を扱うテストを読む。
- 正本の入力制約や guide・本文の生成規則そのものを確認するなら、仕様・schema・生成実装を直接読む。

## hash
- 02264d471c42f20fd659f91f36dc50f6670a9778acd46d586d7b8dd61b1baf82

# `test_feedback.py`

## Summary
- feedback の観測受付から issue 集約、修復、report と active state の公開、raw 観測の整理までを、repository fixture 上で横断して検証するテスト群。collector と report 処理の連携や、公開・復旧時の状態遷移を確認する入口。

## Read this when
- agent の観測受付から report 公開・整理までの一連の流れや、collector と report 処理の境界を変更・調査するとき。
- 観測の保存、候補の集約、修復 run、公開失敗からの復旧が連携する条件を確かめるとき。

## Do not read this when
- feedback の判定根拠に含める repository file の選定だけが対象なら、根拠収集に絞ったテストを読む。
- checkpoint、根拠の再確認、封印の単独動作が対象なら、その制御に絞ったテストを読む。
- 単一コンポーネントの内部動作だけが対象なら、その実装と焦点を絞ったテストから確認する。

## hash
- 3ec3547d4719d643cc1190d84d3c7416f54bed3ac3ed95ad0fe7dcc1403e119a

# `test_feedback_decision.py`

## Summary
- feedback 判定根拠に含める worktree 入力の収集とハッシュ化を検証する。入力の除外、安全なパス処理、Git mode の扱い、nested `.git` の判別に関する回帰テストが中心。

## Read this when
- 判定根拠の入力対象や除外対象を変えるとき、その変更が `worktree_inputs` の回帰条件に与える影響を確認する。
- 入力内容・実行 mode のハッシュ化、nested repository の metadata 判定、削除済みパスや worktree 外パスの扱いを調べる。

## Do not read this when
- feedback の報告・修復フローや生成物全般の振る舞いを調べるときは、統合テストを扱う `test_feedback.py` から確認する。
- checkpoint、再確認履歴、修復の収束判定を調べるときは、`test_feedback_reconfirmation.py` へ進む。

## hash
- d5bd58b9507279e39eada8a25463b14cfc95ca656eebd5c8d46bb2ce59c0eacf

# `test_feedback_reconfirmation.py`

## Summary
- feedback の依存入力や証拠が変わったとき、過去の判定結果を再確認し、修正 wave の循環診断と checkpoint 復旧が保たれることを検証する。
- 封印後の join・publication・recovery で判定根拠の整合性を確認し、検証済み merge 調整と active issue への根拠引き継ぎも扱う。

## Read this when
- feedback の再確認が起きる条件、過去の結果や証拠の扱い、修正サイクルの収束を調べるとき。
- checkpoint の復旧や、封印後に入力が変わった場合の join・recovery の可否を調べるとき。

## Do not read this when
- 判定根拠に含めるファイルの列挙や Git metadata の除外方法だけを調べるときは、根拠状態の構築を直接検証する項目へ進む。
- feedback の通常受付、MCP reporter、raw observation 保存や一般的な publication の挙動を調べるときは、それらの基本フローを扱う項目へ進む。

## hash
- aeb3d77952e7957097347c78946498908deca204c79d5b4ad021efacf4ba10a7

# `test_file_inventory.py`

## Summary
- oracle と realization の全ファイル列挙が Git 状態による分類と pruning の境界を守るかを、full-glob 基準と照合する回帰テスト群。
- 列挙結果の refactor state 同期への影響、nested repository 上の単一路分類、候補数に対する Git 処理量も確認する。

## Read this when
- 全ファイル列挙の結果や、root と nested repository での ignore 規則・metadata 境界に関する回帰を調べるとき。
- symlink や特殊ファイルの扱い、ignored directory の走査、linked worktree の metadata 処理を確認するとき。
- 列挙による refactor state の同期や変更検出、候補数増加時の Git 処理量、nested repository 内の単一路分類を調べるとき。

## Do not read this when
- 列挙・pruning の規範的な定義を確認するときは、回帰テストではなく正本仕様から読む。
- Git ignore helper の個別の判定や ignore 設定ファイルの更新・検証だけを調べるときは、その helper に対応するテストから読む。
- refactor state の保存形式や入力検証、対象選択だけを調べ、ファイル列挙との連携を扱わないときは、state 専用のテストから読む。

## hash
- f48c4eda1eb04c8261459deec0363f20848a47df141fd3a1287af1dc83adcd19

# `test_oracle_edit_cli.py`

## Summary
- `cmoc oracle edit` の CLI 実行制御を検証するテストです。2 回の agent call、入力・設定の共用、起動前提、失敗時の状態と差分、終了レポートをまとめて扱います。

## Read this when
- `oracle edit` の実行順序や成功・失敗時の制御、差分・session state・通知の保持に関するテスト範囲を調べるとき。

## Do not read this when
- コマンドの正規仕様を確認するときは oracle edit の仕様へ、prompt の構築内容を確認するときは編集パラメータ builder へ直接進むとき。
- `oracle edit` 以外の CLI コマンドのテストを探すとき。

## hash
- d8aff9820c2581f74b0f179a2cda40f267d51a94fd3b439cd080b3f2d2f2cc43

# `test_oracle_investigation_cli.py`

## Summary
- `cmoc oracle investigation` の CLI 統合テストを担い、session のない main worktree からの起動、入力確定から TUI 起動までの流れ、および read-only 呼び出しの主要条件を検証する。
- 併せて、investigation の互換 adapter が builder 関数だけを公開することを検証する。

## Read this when
- investigation の起動前提、editor input の受け渡し、閲覧範囲やアクセス mode、TUI 起動条件を変更・調査するとき。
- investigation builder の互換 adapter が公開する API を変更・調査するとき。

## Do not read this when
- 正確な prompt 文面や agent への指示、builder の選択条件が対象なら、builder 実装または正本仕様を直接読む。
- 共通の editor input lifecycle や document search の意味・実装が対象なら、それぞれの責務を持つ共通実装や正本仕様を直接読む。oracle edit の session 実行条件が対象なら、その専用 CLI テストから確認する。

## hash
- 4510ae2a2d71abe93425067c4e87922aaacb53dfa9362b0ab0a844cc02177496

# `test_packaged_import.py`

## Summary
- 配布時の配置を模した隔離環境で、選択したパッケージの import 境界と公開面を検証します。コピーしたソースだけを使うため、開発用チェックアウトへの依存も確認できます。
- quota probe の正本 builder 参照、oracle 編集と prompt editor の import・入出力境界、ACP basic の定義再公開、config の公開名を確認します。実際の wheel のビルドやインストール内容全体を検証するテストではありません。

## Read this when
- 隔離した packaged layout で、対象パッケージが import できるか、正本定義の再公開や公開名が期待どおりかを確認するとき。複数の import 境界を横断して検証する入口です。
- 配布用 package 設定と、隔離環境からの import 成功が食い違う場合に、その設定確認を含む回帰テストを調べるとき。

## Do not read this when
- 個別 builder の prompt や parameter の生成内容を調べるときは、その処理を定義する実装と正本仕様を直接確認してください。
- prompt editor の編集手順や config の値・振る舞いなど、ここで確認する import と公開面を越えた機能を調べるときは、担当する実装や機能テストへ進んでください。
- 実際の wheel の構築結果や配布物の収録内容を確認するときは、その成果物を扱う検証と packaging 設定を直接確認してください。

## hash
- 8cdaba9c9023a0490e61b1b1bed4a78924d8d57d9dfd6814de6b1693f3b141c3

# `test_primary_report.py`

## Summary
- 非対話 CLI の primary report が、処理前エラーや中断を含む終了経路で保存され、Codex 出力と受理済み observation を実行記録に保持する契約を検証する。
- Structured Output の表示、artifact path の Markdown 表現、保存・読取・更新の失敗時の扱いも対象とする。

## Read this when
- 共通の primary report fallback や実行記録の生成・追記を調べるとき。
- doctor preprocess や事前条件の失敗、中断時の report、Codex 出力の整形、report 保存失敗時の挙動を確かめるとき。

## Do not read this when
- 個別サブコマンドの業務処理や Git・session・indexing の効果が対象で、共通 report 契約を調べる必要がないときは、各処理に対応するテストへ進む。
- terminal result・ログ・通知の共通制御だけが対象で、report の内容や保存が範囲外のときは、CLI 共通制御のテストへ進む。
- report の規範要件や描画・保存の実装詳細を確認するときは、正本仕様または共通 reporter 実装を直接読む。

## hash
- 12d3f1be1dda1880039bbb1a032e7206296bde75236cf79c78ed440ab5a60548

# `test_production_cli.py`

## Summary
- 利用者向け CLI の末端コマンドを、独立プロセス・実 Codex CLI・実推論で通す統合受け入れ試験。TUI 経路では PTY も使う。
- 回答品質ではなく、応答後の制御と外部から観測できる report・state・Git・call log、および TUI の editor handoff や通知を検証する。

## Read this when
- 公開末端コマンドの追加漏れや、実 CLI を使った本番起動経路を一括して確認するとき。
- 実推論を伴う oracle edit、feedback remediation、realization run、session/run の join・abandon などをまたぐ状態遷移や Git の結果を確認するとき。
- TUI の実応答完了、PTY 操作、editor handoff、通知、および実行前後の副作用を確認するとき。

## Do not read this when
- 特定コマンドの分岐・入力検証・失敗条件を fake Codex や CLI runner で調べるときは、そのコマンドに絞ったテストから確認する。
- Codex の回答内容や推論品質、生成結果が正本仕様を満たすかを調べるとき。この試験は回答後の cmoc の制御を対象とする。

## hash
- c3a17c41ce375ae83ac094acba13f9acefc8a8f14500ea582ee5f659f56fe6aa

# `test_production_cli_support.py`

## Summary
- 実経路統合テストで使う PTY 操作 helper のうち、信頼確認 prompt の描画後に Enter を送るタイミングを検証する。

## Read this when
- 信頼確認 prompt の描画中に入力が破棄されないことや、次の poll で Enter を一度だけ送る挙動を確認・変更するとき。

## Do not read this when
- 本番 CLI の起動から終了までの統合フローを調べるときは、そのフローを検証するテストへ進む。

## hash
- 67687d4517bc714cca1ab03754abb96c90a374dbc48b788c0eed9ca2e6d1e5d1

# `test_prompt_editor_input.py`

## Summary
- プロンプト編集入力の予約・エディタ起動・確定保存について、呼び出し側から見た挙動と入力保全を検証する。
- 編集入力の一連の処理を変更・調査する際、外部挙動の回帰境界を確認する入口となる。

## Read this when
- 編集入力を予約し、エディタで変更して確定する流れや、入力ファイルの検証・保存・失敗時の保持を変更または調査するとき。
- 編集処理から handoff target を開始・終了する連携や、その終了処理を確認するとき。

## Do not read this when
- handoff target のプロトコル、上書き規則、ガイド提供、MCP interface のみが対象なら、handoff 専用のテストを直接読む。
- 本番コードの内部構造を把握することが目的なら実装側から読み始め、外部挙動の確認が必要な場合にこのテストへ進む。

## hash
- 53dad9b8decf47c7c9ac6e7e002ac9caac68d5fba6fe9e3797bdb30cb582c379

# `test_prompt_parts.py`

## Summary
- 各 policy builder の出力と完全 prompt への組み込みを、共通の Markdown 描画経路で横断確認するテスト。
- policy の選択・順序・重複、objective と placeholder の扱い、アクセス mode ごとの規定出力を検証する。

## Read this when
- 複数の policy を完全 prompt に組み込む変更について、出力順、選択、重複や描画への影響を確認するとき。
- placeholder の統合・競合や、アクセス mode ごとの規定が prompt 出力に反映されるかを確認するとき。

## Do not read this when
- 構造化文書の Markdown 整形や tag block の描画自体を調べる場合は、renderer の単体検証から読む。
- エディタ入力の予約・編集・読み戻しといった実動作を調べる場合は、その処理を扱う検証から読む。この対象が扱うのは handoff policy の文面と prompt への組み込み。
- 単一 policy の生成実装や仕様だけを調べる場合は、その builder と対応する正本を直接読む。

## hash
- 55fbe8994ac9a3b649095ce8f0aae4eb048a39a97999059eb5bb58dd8901eefb

# `test_runtime_cli.py`

## Summary
- 共有 CLI runner の終了処理を検証し、成功・失敗・ユーザー中断時の表示、終了コード、診断ログ、通知の関係を扱う。
- 引数解析、補完 probe、doctor と pre-log の前処理、work root の扱いに加え、共通ログと時間表示も検証する。

## Read this when
- 共通 runner の結果分類やエラー表示、診断ログ、終了通知のタイミングを変更するとき。
- doctor や pre-log の前処理、work root と linked worktree の選択、補完 probe の副作用境界を見直すとき。
- 共通サブコマンドログの記録方法、timestamp、duration 表示を変更するとき。

## Do not read this when
- 特定サブコマンド固有の引数、処理結果、レポートを調べるときは、そのコマンドのテストから読む。
- Windows toast の payload・transport や Codex TUI の prompt・subprocess の詳細を調べるときは、それぞれの専用テストから読む。

## hash
- f07e289f6592e907070c242eb85d114d70a1e548926337745a91ac7e905f6eb7

# `test_runtime_codex_conflicts.py`

## Summary
- session join の conflict resolution パラメータから Codex の起動引数への受け渡しを検証する。commit 参照は prompt に残り起動引数には含まれず、参照の順序で sandbox 設定や引数が変わらないことを確認する。

## Read this when
- session join の conflict resolution 呼び出しで、commit 参照の prompt と起動引数への振り分けや、sandbox 設定の不変性を確認するとき。

## Do not read this when
- Codex の model、provider、hook、出力処理を含む全般的な起動引数の契約を調べるときは、Codex profile 全体を扱うテストへ進む。
- Codex sandbox 設定 API が path 別の permission 入力を拒否する契約を調べるときは、その API に絞ったテストへ進む。
- session join builder の prompt 内容や公開契約を調べるときは、builder の契約を扱うテストへ進む。

## hash
- 677c33890f496bff233b3922c44863bbfa9556d5c2e86da26c7dc9fa4632c6dd

# `test_runtime_codex_permissions.py`

## Summary
- Codex argv 構築 API が path 別の権限入力を受け付けないことを、構築・準備の両経路で確認する回帰テスト。

## Read this when
- Codex argv 構築 API の引数契約を変更する時や、path 別の権限入力が再導入されていないか確認する時。

## Do not read this when
- FileAccessMode から sandbox への変換や、生成 argv の設定内容全体を調べる時。その場合は変換や Codex profile の構築契約を扱うテストを読む。

## hash
- 6d7ae696c6cd3cceca152c9ec0dbbc83566f5aad324dc9b36796fe32a22fa79e

# `test_runtime_codex_profile.py`

## Summary
- Codex CLI に渡す argv と環境の構築契約を検証します。sandbox の選択、model/provider 設定、call ごとの MCP・hook 設定、通知 hook の対応判定、別 call の環境変数を引き継がないことが対象です。
- schema source の配置と、schema を使わない場合の JSON 出力読み取りも扱います。

## Read this when
- Codex CLI の起動引数や環境の生成、provider の設定、MCP・通知 hook の有効条件を変更・調査するとき。
- schema source の配置方法や、通常の JSON 出力を読み取る処理を変更・調査するとき。

## Do not read this when
- プロセスの起動後の終了・追跡・中断処理が対象なら、process lifecycle を扱うテストから確認してください。
- CODEX_HOME の検証、JSONL event のエラーや回復分類、path 別の権限制約や session join の競合が対象なら、それぞれに特化したテストへ進んでください。

## hash
- 1c93eeda3b572505905eab1d0e80d637a7f8abd7191501b7cc7bd38b8b2ec22e

# `test_runtime_config.py`

## Summary
- CmocConfig の既定値と Codex の agent call・model provider 設定について、JSON 変換とファイル経由の保存・復元を確認する回帰テスト。
- 設定入力の検証、壊れた JSON や扱えないパスの拒否、利用者向けエラー出力も扱う。

## Read this when
- 既定値補完、agent call ごとの設定、provider-local 設定値、または設定の保存・復元を変更するとき。
- 設定入力の型や値の受理条件、壊れた設定ファイルや不正なパスの扱いを変更するとき。

## Do not read this when
- Codex CLI の引数生成や実際の呼び出しへの適用が主題なら、その境界を扱うテストから確認するとよい。
- 設定項目の意味や要求を確定・変更する場合は、正本仕様を先に確認するとよい。

## hash
- c5d71fd28b760c4ad4a59f5e1b5dcec2fc0c9d0a54288ac93dc0a4835a08002c

# `test_runtime_content.py`

## Summary
- runtime content helper の binary 判定と、内容ハッシュ名で保存する際の安全性を検証するテストです。NUL byte の判定と、保存先が symlink の場合にリンク先を変更せず保存する動作を扱います。

## Read this when
- NUL byte を含む内容の binary 判定を確認・変更するとき。
- 内容ハッシュで保存する処理について、保存先が symlink の場合にリンク先を保護する動作を確認・変更するとき。

## Do not read this when
- runtime content helper の実装や処理の詳細を調べる・変更するときは、実装を直接確認してください。
- 索引付けや Codex 実行規則の仕様全体を調べるときは、正本仕様を確認してください。このテストは helper の限定的な動作だけを扱います。

## hash
- 1d7cd925d0b731ec53366c6eb796bed8c9be466df205b88ae5f6b9f8f07ad5c3

# `test_runtime_file_access.py`

## Summary
- FileAccessMode の永続化値と、既知の論理モードから Codex sandbox mode への変換契約を検証するテスト。
- Codex 実行時の sandbox 変換境界を確認する入口。

## Read this when
- FileAccessMode の永続化値が保たれるか確認するとき。
- 既知の file access mode と sandbox mode の対応を変更・調査するとき。

## Do not read this when
- mode ごとの詳細なファイルアクセス制限や prompt 文面を調べるときは、policy の構築・適用条件を扱うテストを読む。
- sandbox を含む Codex argv の組み立てや未知 mode の失敗条件を調べるときは、Codex 実行プロファイルの統合テストを読む。

## hash
- da671493f26abe84c50a963e608fef2af59ab84a099bb946321c5c38401ad4a2

# `test_runtime_git_ignore.py`

## Summary
- Git ignore 判定と cmoc 用 ignore 設定のランタイム挙動を検証するテスト。追跡状態やパス名の解釈、既存設定の保持、安全でない ignore ファイルの拒否、判定失敗時のエラーを扱う。

## Read this when
- Git ignore 判定の変更や、追跡済み・未追跡のファイルの扱いを確認するとき。
- cmoc 用 ignore 設定を追加・更新するとき、既存ルールの保持や ignore ファイルの安全性を確認するとき。
- ignore 判定の失敗や、無視された symlink の扱いを調査するとき。

## Do not read this when
- ファイル分類全体の正本ルールを確認するときは、該当する仕様文書を直接読む。
- Git ignore 以外のランタイム機能を変更・調査するときは、その機能を担当するテストから確認する。

## hash
- cd4002d7f6293b03a9d07d5d099490cc545f8643d83156258709df390981e93f

# `test_runtime_refactor.py`

## Summary
- realization refactor の調査 state と対象選択に関する runtime 回帰テストの入口。
- 対象集合の同期、履歴保持と変更時の再調査、state の検証・保存、選択優先度に加え、oracle/realization 分類が調査対象へ反映される境界を確認する。

## Read this when
- realization refactor の state 同期、履歴保持、変更時の再調査、state の拒否条件、候補選択の優先順を変更または調査するとき。
- 対象ファイルの分類や branch 上の file 判定が refactor state に与える影響を、nested repository や symlink・非通常 file の境界に沿って調べるとき。

## Do not read this when
- コマンド全体の処理手順、完了・中断、所見判定など workload の正本仕様を確認するときは、realization refactor の仕様本文を直接読む。
- 列挙や Git ignore の契約・性能要件そのもの、または refactor と無関係な Git/worktree 動作を調べるときは、列挙仕様か該当する Git runtime の実装・テストへ進む。

## hash
- 0785f76765f3a591a9ac1a41891bbf1ffa0371bd036cb7251804aea58e820d63

# `test_runtime_state.py`

## Summary
- session/run の永続状態を扱う runtime のテスト。state schema と managed branch 解析、state file の読み書きに関する境界条件、session fork lock の process 間排他を確認する。

## Read this when
- session/run state の schema 検証や branch からの state 解決、state file の入出力エラー処理を確認・変更するとき。
- session fork lock が process 間で排他されることを確認するとき。

## Do not read this when
- session/run の field や状態遷移の正本仕様を定めるときは、仕様文書を直接読む。
- 個別コマンドの fork・join・abandon の workflow や CLI 振る舞いを調べるときは、そのコマンドのテストを直接読む。

## hash
- 32811ae0b83c739ed0c9b39d68097f7c1070c6b84ba11da5216b054ca0ba8c48

# `test_runtime_wrapper.py`

## Summary
- 起動 wrapper の回帰テストとして、仮想環境 Python の検査、失敗時のエラー報告、利用可能な場合の CLI 本体への引数転送を確認する。
- 補完プローブ時の出力抑制も扱い、起動 wrapper の挙動を調べる入口となる。

## Read this when
- 仮想環境 Python の検出や起動確認、失敗報告を変更・調査するとき。
- 補完プローブ時の経路や、wrapper から CLI 本体への引数・環境変数の転送を変更・調査するとき。

## Do not read this when
- 仮想環境の作成・インストール手順を調べるときは、開発環境の仕様を確認する。
- CLI 本体のコマンドや内部動作を調べるときは、該当機能の実装・テストを確認する。

## hash
- 707b3f26990edb78254d6b4a9b15a2b50f704cf7f8afd6c89b609f3ce72be6d5

# `test_session_cli.py`

## Summary
- session fork・join・abandon の CLI 統合テストとして、branch と永続 state の遷移、事前条件、失敗時の復旧、利用者向け結果を検証する。
- linked worktree を含む session 操作や、join の merge・conflict 解消・cleanup を一連の CLI 動作として確かめる。

## Read this when
- session コマンドの状態遷移や失敗時の復旧を、CLI を通した回帰テストで確認するとき。
- linked worktree 上の session 操作や、join の merge と conflict 解消の連携を調べるとき。

## Do not read this when
- join conflict resolver の prompt や呼び出し parameter の契約だけを調べるときは、その builder 専用テストを読む。
- 公開 CLI の command 登録や help 表示だけを調べるときは、CLI command tree のテストを読む。
- session state の形式や遷移規約そのものを確認するときは、対応する正本仕様を読む。

## hash
- 82cbac50361105fd17836d262e329841c5f85be8526ab61a193dc14006ca2bdc

# `test_skill_metadata.py`

## Summary
- リポジトリ内ローカルスキル定義の YAML frontmatter に関する共通条件を検査し、新しいスキルも対象に含めるテスト。

## Read this when
- ローカルスキルの追加・移動や frontmatter の登録情報を変更し、この検査への影響を確認するとき。
- この検査の対象範囲や検出条件を変更するとき。

## Do not read this when
- 個別スキルの用途や指示内容を確認・編集するときは、該当するスキル文書を直接読む。
- frontmatter の登録情報に関係しないテストや実装を扱うとき。

## hash
- bf735875997b038795c375af2a689094f308e7a286145efe3996c3ce9cd796d8

# `test_struct_doc_rendering.py`

## Summary
- 構造化文書ノードの Markdown 描画と `basic.struct_doc` 互換 API の挙動を検証するテスト。空行の縮約、コードフェンス、参照ブロック、規定カテゴリ、互換 re-export、子要素の型エラーを扱う。

## Read this when
- Markdown 描画の整形や参照ブロック、SDPolicy の表示を変更・調査するとき。
- `basic.struct_doc` から公開する型や renderer の互換性を変更・調査するとき。
- SDHeader または SDTagBlock の不正な単一子要素に対する型エラーを変更・調査するとき。

## Do not read this when
- 正本 renderer の実装詳細や構造化文書ノードの仕様を確認するときは、正本の `oracle/src/oracle/other/struct_doc.py` を直接読む。
- このテストが扱う Markdown 描画・互換 API と関係しない、構造化文書の利用側だけの挙動を調べるとき。

## hash
- 59777795fc220c56f39c46ca4ee6aa2b3d9cb6b4f47edec071c540bc15734205

# `test_windows_toast.py`

## Summary
- Windows toast の表示内容と安全な PowerShell transport、通知失敗の非伝播、自動補完中の無効化を検証するテストです。
- Codex TUI callback の root session 判定、turn ごとの重複抑止、入力内容の秘匿、呼び出し単位の state 管理と cleanup も扱います。

## Read this when
- toast の内容・transport・失敗時の挙動や、自動補完中の通知境界を変更または調査するとき。
- TUI の通知 callback が root session の turn 完了を一度だけ扱う条件や、一時 state の並行実行・cleanup を調査するとき。

## Do not read this when
- CLI が terminal result 確定時に通知を呼ぶ条件や回数を調べるときは、CLI runtime の統合テストを確認してください。
- Codex TUI 起動時に通知設定や session-start hook を渡す構成を調べるときは、Codex TUI runtime の統合テストを確認してください。

## hash
- 89f0cf57ba1d258d5355d60731bd03d20be0b8aaf008deeb38e0494173394cfb
