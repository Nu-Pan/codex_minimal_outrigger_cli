# `__init__.py`

## Summary
- cmoc 共通 runtime helper を提供する commons パッケージの初期化ファイル。commons 配下の共通実行時補助機能を確認・変更するときの入口。

## Read this when
- 共通 runtime helper の提供箇所や commons パッケージの初期化を確認するとき
- commons 配下の機能を利用・変更する前にパッケージの入口を確認するとき

## Do not read this when
- 特定の runtime helper の実装詳細を確認したいとき
- commons 配下に対象となる個別実装ファイルがある場合

## hash
- 8b50d22749d6fd880d430c393e14c6dcb919038e7b9c7ec76288c523c3d58b34

# `cmoc_runtime.py`

## Summary
- cmoc のランタイム共通 API を集約して再公開するモジュール。設定、Git、Codex 実行、プロセス管理、パス、状態、ログ、結果型など、CLI 実装が横断的に利用する関数・定数・型の入口となる。

## Read this when
- 複数の runtime commons 機能を利用する CLI 実装や、その公開 API の追加・変更・参照箇所を確認するとき。
- cmoc の共通ランタイム API の import 元や再公開対象を確認するとき。

## Do not read this when
- 特定のランタイム機能の内部実装を調査・変更するとき。その機能に対応する個別の runtime モジュールを直接読む。
- CLI コマンド固有の処理やテストだけを確認するとき。

## hash
- dc703041a3d3ddd031bd81f5153d7b230cf31a10617c2debfc6ce34e7f295a74

# `indexing.py`

## Summary
- INDEX.md の検査・生成・更新・commit を一貫して扱う共通実装。対象ディレクトリの列挙、既存 entry の hash による再利用、不足 entry の Codex 生成、Structured Output の検証、INDEX.md の安全な書き込み、更新 commit、排他制御を提供する。

## Read this when
- INDEX.md の自動生成や鮮度判定の挙動を変更・調査するとき
- 対象ファイル・ディレクトリの除外条件、hash 計算、entry の再利用条件を確認するとき
- Codex による entry 生成、並列実行、実行コンテキストや worktree の扱いを確認するとき
- INDEX.md の書き込み・symlink 対策・Git commit の失敗処理を確認するとき

## Do not read this when
- INDEX.md entry の正本 schema や文章上の要件だけを確認したいときは、対応する oracle の schema・standard 文書を読む
- INDEX.md 更新以外の CLI 処理、一般的な Git 操作、Codex 実行処理だけを調査するときは、各責務の直接実装を読む

## hash
- 6232c5928c0b90acf3a1bb16f99d9b24b57a35c6a6c84cc3e464a0dc9f1433f4

# `prompt_editor_input.py`

## Summary
- エディタまたはTUIからAI Agent用Markdownプロンプトを受け取り、テンプレート保存、エディタ選択・起動、入力読み込み、HTMLコメント除去、`.cmoc` ignore保証を担う共通境界。プロンプト編集フロー、エディタ選択仕様、入力完了時のエラー処理を確認する入口。

## Read this when
- プロンプト編集入力の保存・読み込み・コメント除去を変更または調査するとき
- code、nano、vim、viの選択順やエディタ起動失敗を確認するとき
- editor/TUI用ディレクトリの`.cmoc` ignore保証やtimestamp付きパス予約を確認するとき

## Do not read this when
- AI Agentへのプロンプト内容やテンプレート仕様だけを確認したいときは、対応するoracle文書を直接読む
- プロンプト編集後のCLI/TUI全体の実行フローや呼び出し元の責務を調査するときは、該当する上位実装を直接読む

## hash
- 5b4c8b92cfd723b9bd31e33b234cc9809fdc7e597e4129aa31e3007a5af482d1

# `runtime_cli.py`

## Summary
- CLI サブコマンドの共通実行ライフサイクルを提供する。work root 検査、doctor preprocess、サブコマンドログ、step 通知、完了サマリー、終了コード処理、例外のエラー表示を一元管理する。関連する CLI 実行フローや共通ログ・エラー処理を確認するときの入口。

## Read this when
- CLI サブコマンドの実行前後処理、共通ログ、step 表示、完了表示、終了コード、例外処理を変更または調査するとき。
- work root の実行条件や doctor preprocess の共通適用範囲を確認するとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、runtime ログの永続化実装、エラー内容の定義だけを確認したいときは、それぞれの専用実装を直接読む。

## hash
- 0fdfe0cf2a299838bfd4b72f21b187a24772db84ad908b9b7c233ebe6feae934

# `runtime_codex.py`

## Summary
- Codex 実行系の公開入口をまとめる薄い再エクスポートモジュール。exec 実行と TUI 実行の起動関数を同じ import 元から参照できるようにする。

## Read this when
- Codex 実行ランタイムの利用側で、exec 実行または TUI 実行の起動関数をどこから import するか確認したいとき。
- 実行方式ごとの実装詳細ではなく、runtime_codex 系の公開 API 境界だけを確認したいとき。

## Do not read this when
- exec 実行の具体的な処理、引数処理、プロセス制御を確認したいときは、exec 実行側の実装を直接読む。
- TUI 実行の具体的な処理、端末制御、対話実行の挙動を確認したいときは、TUI 実行側の実装を直接読む。
- 新しい実行ロジックや分岐を追加する場所を探しているときは、この再エクスポートではなく各実行方式の実装へ進む。

## hash
- bce418fcd1f6bffaed81f3724333817408657aed46183fa20819ffc1b40a7993

# `runtime_codex_exec.py`

## Summary
- Codex exec の単一試行ループを統括する実行制御モジュール。Codex subprocess の起動、prompt・stdout・stderr・output・call log の保存、Structured Output の厳格な JSON/schema 検証、capacity retry、quota 待機と代表 probe、resume token による継続、console/subcommand event 記録、最終的な CodexExecResult の構築を扱う。exec 実行の再試行状態機械を確認するための入口。

## Read this when
- Codex exec の subprocess 起動条件、cwd・CODEX_HOME・設定上書き、output schema の適用を変更または調査するとき
- Structured Output の parse/schema 検証、semantic retry、capacity retry、quota 待機・probe・resume 継続の挙動を確認するとき
- Codex call log、prompt/stdout/stderr/output log、console 出力、subcommand event の記録内容や失敗時の診断を変更または調査するとき
- CodexExecResult の生成や、1 回の exec 呼び出しから成功・失敗結果が返るまでの制御フローを確認するとき

## Do not read this when
- TUI の起動・対話処理そのものを調査するときは、TUI 起動を担当する別 module を直接読む
- Codex subprocess の低レベル環境構築、エラー分類、resume token 抽出などの共通処理だけを調査するときは、commons.runtime_codex_profile を直接読む
- Codex exec が参照する正本仕様や retry・quota・ログ規則を確認することが目的なら、対応する oracle 文書を先に読む

## hash
- 0d4695446ef6c4b679967685b1e0d8617fdcdca4ab91765ccc02614e709e44de

# `runtime_codex_logging.py`

## Summary
- Codex CLI 呼び出しの利用者向け console 通知と、起動失敗時の共通エラーテキスト整形を担当する。呼び出し目的・ログパス・経過時間・終了状態を出力し、異常時は stderr へ通知する。

## Read this when
- Codex CLI 呼び出し時の console 通知、終了コードや起動失敗の表示、エラー文字列の整形を変更または確認するとき。

## Do not read this when
- Codex CLI の実行処理、呼び出しログの保存形式、runtime path や時間表示の仕様そのものを変更するとき。

## hash
- 1398891b8c46be913d7f8bdc8a255c0c8426012bb7f58d0afc2f44bb1b0bd350

# `runtime_codex_preflight.py`

## Summary
- Codex exec/TUI 実行前に INDEX 更新 preflight を挟むランタイム連携を担当する。preflight の登録・解除、再入抑止と直列実行、実行対象からの indexing 起点 root 算出、実行本体への委譲を扱う。

## Read this when
- Codex exec または TUI の起動前処理、INDEX 更新 preflight、preflight の有効化・無効化を変更するとき。
- Codex 呼び出し設定から作業 root を決める処理や、preflight の再入・並列実行制御を確認するとき。

## Do not read this when
- Codex 実行本体の subprocess・TUI 実装を変更または調査するときは、runtime_codex の実装を直接読む。
- INDEX の生成規則や oracle 編集サブコマンド固有の仕様を確認するときは、対応する oracle 文書を直接読む。

## hash
- 9a17bb577fe0ed64e036ca1f99b85af81357514dd6f87db9bde3a1d7bbe25e19

# `runtime_codex_profile.py`

## Summary
- Codex CLI subprocess 境界の実装。file access policy、cwd、CODEX_HOME、argv の TOML/config override、schema 配置、subprocess 環境、実行時エラー変換を扱う。
- editing run 用の process tracking、pidfd による PID 再利用対策、process group の停止・待機・cleanup を提供する。
- Codex の JSONL 出力から thread/resume token、capacity/quota、unexpected error、利用者向け error detail を判定する。Codex CLI の起動条件や実行結果の解釈を変更・調査する際の入口。

## Read this when
- Codex CLI の sandbox、argv、cwd、CODEX_HOME、model/provider 設定、schema 配置を変更・調査するとき
- editing run の child process tracking、process group 停止、abandon 時の cleanup や PID 再利用対策を変更・調査するとき
- Codex subprocess の起動失敗、JSONL error、capacity/quota retry、resume token の判定を変更・調査するとき

## Do not read this when
- Codex CLI 以外の一般的な runtime config、path、content、error 型の責務だけを調べるときは、各専門モジュールを直接読む
- editing run の上位 command の状態遷移や利用者向け操作仕様だけを調べるときは、対応する app specification と command 実装を直接読む
- Codex の prompt 本文生成や agent call の orchestration を調べるときは、prompt builder または呼び出し側の実装を読む

## hash
- b020f139805ccf6d1f953b50402afbd6b8d1cbf7b34a4fd9a8b2bc2af1fa4d65

# `runtime_codex_tui.py`

## Summary
- Codex TUI 呼び出しの実行制御を担うモジュール。設定・作業ディレクトリ・CODEX_HOME・上書き引数を解決し、call log を保存して Codex subprocess を起動する。実行結果や起動失敗をコンソールおよびサブコマンド logger に記録し、失敗を CommandResult または CmocError として返す。

## Read this when
- Codex TUI の起動引数、作業ディレクトリ、環境変数、CODEX_HOME の検証を変更・調査するとき
- Codex 呼び出しの call log、実行時間、return code、logger event の記録処理を変更・調査するとき
- Codex subprocess の失敗処理や CmocError への変換を変更・調査するとき

## Do not read this when
- Codex の設定値や override argv の生成規則だけを確認したいときは、設定・profile 関連モジュールを直接読む
- Codex CLI の非 TUI 呼び出し固有の処理だけを確認したいときは、対応する呼び出しモジュールを直接読む

## hash
- 1bc74d53df01b76bf196b7f908cf3eec9628e8ab05571f0d6c5ed95f068711bd

# `runtime_config.py`

## Summary
- cmoc 設定を JSON へ変換・検証・保存し、JSON から実行時設定へ復元するモジュール。Codex のモデル・provider・reasoning effort、各種ループ回数、JSON/TOML 互換値の型検証を扱う。設定ファイルの symlink・特殊ファイル・不正 JSON を拒否し、既定値での復元や未作成時の生成も提供する。

## Read this when
- cmoc 設定の JSON 永続化形式、読み込み・書き込み、型検証、既定値補完を変更または調査するとき
- Codex model/provider や reasoning effort の設定復元、設定値の不正入力時のエラー境界を確認するとき
- 設定ファイルの path 安全性、symlink・特殊ファイル対策、初期生成や同期処理を確認するとき

## Do not read this when
- 設定型そのものの既定値や enum 定義だけを確認したいときは、参照先の config 定義を直接読む
- 設定を利用する各 CLI コマンドの振る舞いだけを調査し、設定の保存・復元処理を扱わないとき
- 一般的な runtime path の生成規則だけを確認したいときは、runtime paths の実装を直接読む

## hash
- 02f81011c489d1b5ee1bd2de47dd22908c41cd26bcc135a1c9650ca63b5586ef

# `runtime_content.py`

## Summary
- ファイル内容の SHA-256 ハッシュ計算、UTF-8 文字列のハッシュ計算、内容ハッシュを含む一時ファイルの安全な保存、バイナリ判定を提供する共通ランタイム処理。symlink や dangling symlink、既存ファイルとの整合性、原子的な置換を扱う。

## Read this when
- ファイル分類や状態同期で、通常ファイルと symlink のハッシュ方法を確認するとき
- 内容ハッシュ付きファイルの生成・再利用・原子的な保存処理を変更するとき
- ファイルのバイナリ判定ロジックを変更または利用するとき

## Do not read this when
- 特定のプロンプト生成処理や oracle/realization の仕様を確認したいとき
- この共通ランタイム処理を利用する上位機能の挙動だけを調査するとき

## hash
- ddf0f66390f4aaf71281fa12bd36f060b80ff0d272148ee758ccd73e2714c1c6

# `runtime_doctor.py`

## Summary
- doctor preprocess における Git 共通ディレクトリ単位の排他ロック、修復対象の同期、一時 index の退避・合成・復元、修復 commit の lifecycle を扱う。current worktree と main worktree の修復差分を、利用者の staged 状態と分離して commit するための内部実装。

## Read this when
- doctor preprocess の修復処理、Git index の退避・復元、一時 index の操作、.gitignore や .agents の追跡修復、修復 commit、linked worktree 間の排他制御を調査・変更するとき。

## Do not read this when
- doctor の設定同期や refactor state 同期の仕様だけを確認したいときは、対応する同期モジュールを直接読む。
- doctor preprocess の利用者向け仕様やエラー条件の正本を確認したいときは、参照されている oracle doc を直接読む。

## hash
- 9a652882dfc53495fc8596c47b181fcb17256c905f8b27bfb935f1ef62e1604a

# `runtime_errors.py`

## Summary
- cmoc の実行時エラーを共通 Markdown レポートへ変換する実装。
- CmocError にエラー概要・復旧案・詳細を保持させ、通常例外には既定の案内を適用する。
- Next actions を最低 2 件に補完し、Summary、Detail、Call stack を含む利用者向けエラー出力を組み立てる。

## Read this when
- cmoc の実行時例外、利用者向けエラーレポート、復旧案、スタックトレースの出力を確認・変更するとき。

## Do not read this when
- 特定のサブコマンド固有のエラー発生条件や、エラー原因となる個別機能の実装だけを調査するとき。

## hash
- 19293509934218345593f574c4afed40ab4c72ae4d921b9864a95b3fa9f8cf66

# `runtime_git.py`

## Summary
- Git コマンド実行とエラー変換、branch・commit・worktree の管理、Git ignore 状態の操作・検証、oracle/realization file の分類を担う共通境界。Git repository path、index、linked worktree の安全性検証を共有するため、これらの処理を追跡する際の入口となる。

## Read this when
- Git subprocess の呼び出し、Git 状態や branch・commit の取得、clean worktree の検証を変更・調査するとき
- cmoc 管理下の branch・linked worktree の作成、削除、path 安全性検証を変更・調査するとき
- `.cmoc/gu` の ignore 設定や `.gitignore`・Git exclude の更新・検査を変更・調査するとき
- oracle file と realization file の path 分類、Git tracking・ignore 判定を変更・調査するとき

## Do not read this when
- Git 境界の実装を変更せず、個別の CLI command や上位 workflow の仕様だけを調査するとき
- worktree や ignore の安全性検証を使う呼び出し側の挙動だけを確認し、共通 helper 自体を追跡する必要がないとき

## hash
- f3f4a193a40d1d38a86f14bbc2e73636f8bb65c3ca0aadef366d6ce8f632a185

# `runtime_logging.py`

## Summary
- サブコマンド単位の JSON Lines ログ出力と step/quota 待機時間の計測を担当する runtime logging モジュール。ContextVar による現在の logger の設定・復元・参照も提供し、ログ記録や実行時間集計を行う実装の入口となる。

## Read this when
- サブコマンドのイベントログ、step timing、quota 待機時間の集計を変更・調査するとき
- runtime helper から現在のサブコマンド logger を取得する処理を変更・調査するとき
- 並列実行時のログ追記や集計の同期を確認するとき

## Do not read this when
- コンソール表示形式やログ仕様そのものを確認したいときは、対応する oracle 文書を先に読む
- ログ保存先や timestamped path の生成だけを変更・調査するときは、runtime paths の実装を直接読む
- サブコマンド固有の処理や Codex event の生成を変更・調査するときは、その呼び出し元を直接読む

## hash
- 6242674523c98429906ea81fe6ab017cb54110f18d1b979ca099099f831630bb

# `runtime_paths.py`

## Summary
- リポジトリ、worktree、cmoc ルートの解決と、実行時の timestamp・duration 表示、各種 session/report/log/schema/config/state 保存先 path の構築を担う共通 runtime path モジュール。cwd の一時切替を process-wide に直列化する `pushd` と、memo 配下判定も提供する。

## Read this when
- runtime path の解決、root placeholder の扱い、cmoc 管理ディレクトリの保存先を確認・変更するとき
- timestamp、console timestamp、duration の書式や予約処理を確認・変更するとき
- cwd 切替の並行実行制御、context 単位の切替状態、root・memo 判定を確認・変更するとき

## Do not read this when
- 特定サブコマンドの処理内容、report・log の出力形式、設定 JSON の schema 自体を確認したいとき
- root placeholder の解決ロジックそのものを変更・確認したいときは、path model 側の実装を直接読む

## hash
- 731c950d030dd27d68799c7bc70603ddde37f79b668f94142de0bbbd159459c5

# `runtime_refactor.py`

## Summary
- oracle/realization file の調査状態を表す state を読み込み、schema 検証・対象 file との同期・保存を行う共通 runtime helper。調査対象の列挙、次対象の選択、未調査状態の生成、全対象の再調査要求化も提供する。

## Read this when
- refactor state の読み込み・保存・schema 検証・同期処理を変更または調査するとき
- oracle file と realization file の列挙や、refactor 調査対象の選択規則を確認するとき
- state path の symlink 拒否、相対 path、SHA256、調査日時などの入力検証を確認するとき

## Do not read this when
- 特定の subcommand の refactor 実行処理や利用者向け仕様だけを調査するとき
- refactor state を利用しない一般的な git、path、JSON helper の実装を調査するとき
- この共通 state 管理の挙動ではなく、oracle file または realization file 本体の内容を調査するとき

## hash
- 4be6657bb580f6d0f5eedf9f8ed7eadcb27908fd8f626ada39bbbc1af6735146

# `runtime_results.py`

## Summary
- Codex exec の構造化出力契約、外部コマンド結果、および exec 実行に伴う生成物・ログ・設定パスを表す型を定義する。runtime 結果の型や呼び出し側契約を確認する必要がある場合の入口となる。

## Read this when
- Codex exec の戻り値契約や構造化出力へのアクセス方法を変更・確認するとき
- 外部コマンドの終了コード、標準入出力、実行ログや生成物のパスを保持する結果型を利用するとき

## Do not read this when
- Codex exec の実行処理そのものを変更・確認するとき
- CLI 入出力やログ保存処理の具体的な挙動だけを調べるとき

## hash
- 9f6e365d5335be51796785b3abc187d63c1d32111ecb9b0ad30308780df063e4

# `runtime_run.py`

## Summary
- editing run の worktree 解決、プロセス追跡、ライフサイクル排他、プロセスおよび Codex 子プロセス群の安全な停止を担うランタイム共通処理。run の abandon・error cleanup や stale PID 検出に関わる入口。

## Read this when
- editing run の process tracking、abandon、error cleanup、子プロセス停止、worktree 解決の挙動を変更・調査するとき
- PID 再利用、プロセスグループ、pidfd、tracking file の破損・stale 状態に関する処理を確認するとき

## Do not read this when
- 通常の git 操作やパス計算だけを変更・調査するときは、対応する runtime_git または runtime_paths の実装を直接読む
- editing run の CLI 入出力や状態遷移の仕様を確認したいだけのときは、先に oracle の editing run 仕様を読む

## hash
- ff4587be210dd7d12e46e6c39f21b57af5e6607acf278939291a51299b4c800f

# `runtime_run_lifecycle.py`

## Summary
- editing run の開始から state 遷移、commit、差分分類、INDEX 更新、cleanup 判定までを担う共通 lifecycle 実装。EditingRunContext と lifecycle lock を共有し、run branch/worktree、session state、許可された変更範囲の整合性を管理する。

## Read this when
- editing run の開始・復旧・終了状態、run/session の state 整合性を変更または調査するとき
- run worktree の commit、rollback、差分分類、oracle 差分、許可外 path 判定を変更または調査するとき
- run worktree での INDEX 更新や branch/worktree cleanup の挙動を確認するとき

## Do not read this when
- editing run lifecycle ではなく、個別の CLI サブコマンド仕様や agent workload の実装だけを確認するとき
- state schema、git 操作、path 判定の詳細実装を直接確認する必要があり、対応する commons モジュールへ進む方が適切なとき

## hash
- f806a46699cf98cf89b62796e20a0ac2e79447db0a88849df57f17ee3035221f

# `runtime_run_report.py`

## Summary
- editing run の fork report と lifecycle report を Markdown + YAML Front Matter 形式で保存する共通処理を提供する。実行コンテキスト、状態遷移、完了理由、変更パス、警告、詳細情報を記録し、timestamped path の予約によって report の上書きを防ぐ。YAML scalar の安全な文字列表現も担当する。

## Read this when
- editing run の fork report または run の join/abandon lifecycle report の生成・保存処理を変更するとき
- report の Front Matter 項目、本文構成、timestamped path の予約、YAML scalar 変換を確認するとき

## Do not read this when
- report の正本仕様や編集 run の状態遷移仕様を確認したいときは、記載された oracle document を直接読む
- runtime path の構築や EditingRunContext の定義自体を変更・調査するとき

## hash
- 37b70b344bbdcff0b02251e6fa3eb6eb63b0f1b6e46fa48aa9d4b10494fc97bf

# `runtime_state.py`

## Summary
- session の永続 state を表す dataclass、JSON schema 検証、読み書き、branch からの session 特定、active session 検索を提供する共通 runtime モジュール。session fork の排他 lock も扱い、session/run 操作から state 管理を参照する入口となる。

## Read this when
- session state の schema、状態値、不変条件、JSON 保存形式を変更または確認するとき
- session branch・run branch と state file の対応付けや、state の読み書き・検証を調査するとき
- session fork の排他制御や active session の検索処理を変更するとき

## Do not read this when
- CLI サブコマンド固有の session 操作仕様や lifecycle を確認したいときは、対応する oracle 文書またはサブコマンド実装を直接読む
- session state と無関係な git 操作、path 解決、エラー型の一般仕様だけを調べるとき

## hash
- e0b35333320120922fa7b0dc327f3f8e884f62a884378b435bbef5e550647fff
