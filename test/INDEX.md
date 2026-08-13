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
- editing run workload の canonical builder adapter を検証するテスト。互換 import 経路の再公開、apply/refactor 用 prompt の実行設定・参照規則・差分埋め込み、canonical Structured Output schema の利用、および raw diff 内の境界風文字列を保持する prompt 境界を確認する。
- editing run の builder 実装や対応する oracle builder・schema を調査または変更する際の検証入口となる。

## Read this when
- editing run 用の apply または refactor builder の prompt 生成、互換 import、実行設定、Structured Output schema の経路を確認するとき
- raw git diff を prompt に埋め込む処理が、三連 backtick や prompt 境界風の見出しを安全に扱えるか確認するとき
- canonical builder と互換 builder の同一性、または refactor builder が要求された schema を参照することを検証するとき

## Do not read this when
- builder の実装仕様や oracle の正本内容そのものを確認する場合は、対応する oracle file または実装を直接読むとき
- editing run と無関係な builder、schema、prompt 生成、または一般的な git/worktree 処理を調査するとき
- テスト実行手順や共通 test fixture の詳細だけを確認するときは、該当する共通テスト支援または実行手順を直接読むとき

## hash
- 055af0750fadc7899921dcb6504e4035fd21ea29e3e9f478f6647007bdeafe92

# `test_acp_builder_indexing_parameters.py`

## Summary
- indexing の index entry builder に対するテストを定義する。builder が選択するモデル・推論強度・ファイルアクセス権・実行設定・プロンプト内容を検証し、oracle 実装との一致も確認する。
- builder が返す Structured Output schema の semantic 配列を空にできないこと、対象本文内の三連 backtick を含む場合も prompt の本文境界を安全に保てることを検証する。
- 互換公開 module が index entry builder のみを公開する契約を検証する。index entry builder の実装、対応する oracle、schema、prompt standard の変更時にテスト対象への入口となる。

## Read this when
- indexing の index entry builder の parameter、schema、prompt 生成、oracle との互換性を変更または検証するとき。
- 対象本文を prompt に埋め込む際のコードフェンス境界や、互換 module の公開面を確認するとき。

## Do not read this when
- index entry の routing 文書そのものを作成・変更するときは、既存の INDEX.md ではなく対象本文と指定された正本仕様を直接確認する。
- indexing 以外の builder の parameter や、一般的な test 実行方法だけを確認する場合。

## hash
- b4bfdd39456d23c22e6ffea5900c39fddc58f44832f110d92473f8508e581cd7

# `test_acp_builder_oracle_review_parameters.py`

## Summary
- oracle review ACP builder 群の parameter 選択、AgentCallParameter の公開面、Structured Output schema、canonical builder 互換性、および動的 prompt の code fence 境界保護を検証する回帰テスト。enumerate、judge、merge、validate advocate/challenger の各段階を横断する review builder 仕様の入口であり、関連する oracle builder 実装や schema の整合性を確認する際に読む。

## Read this when
- oracle review の builder を追加・変更・互換性確認するとき
- review builder の model、reasoning、file access、preflight、agent_call_cwd、公開 export の契約を検証するとき
- review builder が参照する Structured Output schema と oracle source の一致を確認するとき
- 動的に埋め込む finding や理由文に含まれる Markdown 見出し・三連 backtick が prompt section の境界を壊さないことを確認するとき

## Do not read this when
- oracle review builder や schema の挙動を変更せず、別領域の ACP builder だけを調査・変更するとき
- prompt の動的入力保護ではなく、個別 builder の詳細な実装ロジックを直接確認する必要があるときは、対応する canonical builder 実装へ進む
- Structured Output の形式そのものだけを確認したいときは、対応する oracle review schema を直接読む

## hash
- 682b5e2e0ba17ee71dfd7a9fb13db06f241da4479ed4c84921542ba62fb5f7c2

# `test_acp_builder_session_join_parameters.py`

## Summary
- session join の conflict resolution builder に対する契約テスト。互換モジュールの公開範囲と canonical builder との同一性、repo write 権限・モデル設定・作業ディレクトリ・prompt 内容・preflight 無効化を検証する。競合ファイルパスに三連 backtick が含まれる場合も、prompt 内のコードフェンスが正しく保護されることを確認する。

## Read this when
- session join の conflict resolution builder の実装や公開 API を変更するとき
- conflict resolution 用 agent parameter のモデル、権限、prompt、作業ディレクトリ、preflight 設定を変更するとき
- 競合ファイルパスを prompt に埋め込む処理やコードフェンスのエスケープを変更するとき

## Do not read this when
- session join 以外の builder の契約を確認するとき
- conflict resolution builder の実装・公開範囲・prompt 生成に関係しないテストや機能を変更するとき
- canonical builder 自体の正本仕様を確認する必要があり、対応する oracle 実装を直接読むべきとき

## hash
- 718b5e1422beec39954660be9ba80163e000e1f8254181a7d8e0bed3f142ff1d

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
- Codex quota 超過後の probe・待機・復帰・resume／再実行を検証する回帰テスト。代表 probe の共有、session ID 復元、失敗伝播、並行呼び出し、call log・subcommand log、Codex の cwd／CODEX_HOME まで、同一 retry 状態機械の観測点を一体として扱う。quota 待機からの復帰挙動を確認する際の入口となる。

## Read this when
- Codex exec の quota 超過後に、probe の実行条件、待機回数、resume または再実行の選択を確認するとき
- quota probe の失敗・不正な stdout・KeyboardInterrupt・並行呼び出しへの伝播を検証または変更するとき
- quota retry に関する call log、subcommand log、session ID、cwd、CODEX_HOME の外部挙動を確認するとき

## Do not read this when
- 通常の Codex exec 成功経路や quota と無関係な subprocess 実行を確認するとき
- quota probe の prompt 生成仕様そのものを確認するときは、正本の probe builder や Codex exec 仕様を直接読む
- quota retry 実装の内部構造や一般的なテスト実行方法だけを確認するとき

## hash
- eb94cd7a82986cb0906b8fc91d9e3229338afd5a95b83015686612c57e4054e1

# `test_codex_runtime_retry.py`

## Summary
- Codex exec の retry と失敗時ログを検証するテスト群。Structured Output の出力補正、capacity retry、JSONL error、中断、retry 上限、差分保持を、fake subprocess の最終結果・呼び出し回数・call log・subcommand event まで含む外部挙動として一続きに確認する。
- run_codex_exec の retry 状態と共有ログ schema を同じ読み取り文脈で検証するためのテスト入口であり、異常系を個別の責務へ分割せず扱う。

## Read this when
- run_codex_exec の Structured Output 検証失敗、出力補正、capacity retry、未知の JSONL error、中断、retry 上限、または補正時の成果物差分保持を変更・検証するとき
- Codex subprocess の呼び出し回数、session 継続、call log、codex_call event、subcommand event の対応を確認するとき
- fake Codex の応答から最終結果とログ列までを外部挙動として検証するテストを追加・変更するとき

## Do not read this when
- Codex exec の通常成功経路だけを確認するとき
- retry や失敗時ログに関係しない別の runtime 機能を調査するとき
- run_codex_exec の実装責務や正本仕様そのものを確認する必要があり、テスト本文ではなく実装・仕様を直接読むべきとき

## hash
- 173c657a24987edd03acd7527f1104695e6c1e2434795510050b6903618c0559

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
- Codex TUI 実行ラッパーの受け入れテスト。完成済み prompt の読み込み、agent call の作業ディレクトリ・sandbox・引数制約、linked worktree でのアクセス境界、成功時の call log／サブコマンドイベント／コンソール要約、timestamp 衝突時のログ保持、CLI 不在・KeyboardInterrupt・非 0 終了時の失敗記録と例外を検証する。TUI 実装やログ仕様の挙動を変更・確認する際のテスト入口である。

## Read this when
- Codex TUI の呼び出し引数、prompt 読み込み、作業ディレクトリ、sandbox 設定の適合性を確認するとき。
- Codex TUI の成功・失敗時に生成される call log、サブコマンドイベント、コンソール出力、例外の外部挙動を確認するとき。
- timestamp 衝突、CLI 不在、割り込み、非 0 終了など TUI 呼び出しの境界条件を変更・検証するとき。

## Do not read this when
- Codex TUI の内部実装の詳細を調べるだけで、外部挙動のテストケースを確認する必要がないとき。
- Codex の通常実行や別サブコマンドの挙動を確認するときは、対応する実装・テスト対象へ直接進む。

## hash
- 8edd0b6b2d44391c8b00815dd19357ae4a4e080a6128a0005fb940cd7afa20b7

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
- workload fork と共通 run join/abandon の統合 realization test。editing run の session state、run worktree、fork report、process tracking、INDEX 更新、rollback、join/abandon cleanup、refactor cycle を同じ lifecycle fixture で検証する。
- apply fork と refactor fork の正常完了・中断・失敗時の state 遷移、成果物、report、Codex child 停止、管理対象外差分の拒否を扱う。
- run join の merge、競合解決、session 側変更との統合、生成 INDEX の扱い、post-join 同期失敗時の rollback と cleanup 状態を検証する。
- run abandon の process tracking 検証、worktree・branch cleanup、破損 tracking や cleanup 失敗時の資源保持を検証する。

## Read this when
- editing run の apply/refactor fork、run join、run abandon の lifecycle 挙動を変更または検証するとき。
- session state と run worktree の共有、fork report・lifecycle report、process tracking、Codex child cleanup の連携を確認するとき。
- INDEX refresh、oracle・realization 差分の許可範囲、agent commit・遅延変更・rollback の境界を確認するとき。
- refactor の unresolved target、rename、永続 state、cycle completion、中断時の確定済み進捗を検証するとき。

## Do not read this when
- INDEX 更新機構そのものの単体挙動だけを確認するときは、indexing 関連の直接の実装・テストを読む。
- session や run lifecycle の実装詳細を変更せず、単純な CLI 利用方法や仕様概要だけを確認するとき。
- apply fork、refactor fork、run join、run abandon の統合 lifecycle に関係しない機能のテストを探しているとき。

## hash
- 95a278f12d40e2e70dbfa53461b43ea4352e40f6c4b659c55a6734a65dbfcd80

# `test_feedback.py`

## Summary
- feedback observation の受理から raw 保存、report cut、verification、active state への atomic publication、cleanup までを repository fixture で検証する統合テスト群。
- agent-facing reporter の MCP 境界、正規化・verification 用 agent builder、path 境界と secret masking、重複・閾値・fingerprint 判定、破損検出を扱う。
- 中断、再開、checkpoint 再利用、部分 cleanup、publication 後の active state 検証など、feedback report の永続状態遷移を確認する入口。

## Read this when
- feedback observation の reporter、collector、store、report cut、verification、active state、publication、cleanup の挙動を変更または検証するとき。
- feedback report の中断・再開、Codex 呼出しの checkpoint、machine observation の再発閾値、raw artifact の検証を調査するとき。
- feedback 関連の oracle 仕様と実装の外部境界を、同一 repository fixture による実例から確認したいとき。

## Do not read this when
- feedback 領域と無関係な CLI やテストの変更を扱うとき。
- 個別の正本仕様や agent builder の実装内容を直接確認する場合は、それぞれの oracle file や実装対象を読むとき。
- テスト実行方法や一般的な fixture ユーティリティだけを確認したい場合。

## hash
- c58350b890633460954a5145ace5ca1d48cd575fbfdb4723c5fb5589cc749fad

# `test_file_inventory.py`

## Summary
- Git 管理下の work-root を対象に、oracle・realization ファイルの full-tree 列挙契約を検証するテスト。除外ルート、除外名、Git ignore、nested repository、Git metadata、symlink・FIFO・socket・device などの非通常ファイル、refactor state の同期と SHA 更新を扱う。runtime_git の列挙・単一パス分類および refactor state 同期処理の回帰検証への入口となる。

## Read this when
- oracle・realization ファイルの列挙範囲、Git ignore の適用、nested repository の境界、非通常ファイルの拒否動作を変更または検証するとき。
- refactor state のファイル集合・SHA・investigation 状態の同期動作を変更または検証するとき。
- 候補数増加時の Git 処理量や ignore source 検証回数など、列挙処理の性能特性を確認するとき。

## Do not read this when
- 列挙や refactor state 同期の外部挙動を扱わず、別の runtime 機能だけを変更・調査するとき。
- 単一の正本仕様や実装の詳細を確認することが目的で、テストの期待動作を確認する必要がないとき。

## hash
- 9f14e7c05f17bdd8b0e8600f12d4573af3bfbb57741f3e42abab68b89b646021

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
- `commons.indexing` の INDEX.md 生成・解析・更新とディレクトリ走査を、CLI lifecycle から分離して直接検証する回帰テスト群。入力検証、hash による entry 再利用、安定した走査・描画順、並列更新、logger 伝播、cwd lock、memo・symlink・特殊ファイルの扱い、linked worktree 間の lock 共有を確認する。indexing contract の変更や、これらの traversal・更新順・並列実行の挙動を調査するときのテスト側の入口である。

## Read this when
- INDEX.md entry の parse・render・hash 再利用・更新処理を変更または検証するとき
- directory traversal、symlink・特殊ファイル・memo directory の除外、空 directory の扱いを確認するとき
- INDEX 更新の並列実行、pushd 中の worker 制約、Codex event logger、linked worktree lock を確認するとき
- indexing contract に関する回帰テストの対象挙動を把握するとき

## Do not read this when
- indexing の正本仕様や CLI subcommand の利用契約を確認する場合は、対応する app_spec を直接読む
- INDEX entry の生成プロンプト標準や Structured Output schema を確認する場合は、対応する oracle source を直接読む
- indexing と無関係な CLI lifecycle、一般的な runtime、または他機能のテストを調査するとき

## hash
- c5fef2ac6a7290435572c5051d1a8636143fad5de369866df36535f964841c7a

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
- oracle review の finding loop を検証する回帰テスト。finding の列挙、関連 finding の引き継ぎ、検証理由の統合、merge の postcondition、judgement、interrupt 時の部分結果保持、および隔離 worktree に対する agent call context を一つの review loop として確認する。

## Read this when
- oracle review の finding 列挙・merge・検証・judgement の連続処理を変更または調査するとき
- review worktree、agent call parameter、Structured Output、finding path の関連付けを変更するとき
- review loop の中断復旧や、完了済み finding・検証理由の保持を確認するとき
- merge 出力の postcondition や補正失敗の伝播を変更するとき

## Do not read this when
- oracle review loop の実装や契約に関係せず、他の sub-command の単独動作だけを調査するとき
- テスト実行方法だけを確認するときは、repository local の test execution 指示を直接読む

## hash
- 0f593f6750c3f5daf20d34f2113730e3c15db86849fa526ce3d083b7d635c85e

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
- review 用の隔離 worktree と branch の lifecycle、および review で生成された INDEX.md の検証・統合を回帰テストする。
- oracle review の対象 worktree 選択、snapshot からの fork、衝突回避、割り込み・例外時の cleanup、merge rollback、差分制約、preflight path context、report、notification を検証する。
- oracle review の review worktree lifecycle、INDEX 差分の許可範囲、merge conflict 復旧、cleanup 失敗を変更または検証するときの入口である。

## Read this when
- oracle review の隔離 run がどの branch・commit・worktree を使うか確認するとき
- review worktree の作成・cleanup、割り込みや予期しない例外、lifecycle lock の挙動を変更または検証するとき
- review branch から INDEX.md のみを session に統合する条件、差分検証、merge conflict の復旧を確認するとき
- oracle review の report や terminal notification の回帰挙動を確認するとき

## Do not read this when
- oracle review の実装そのものを調べるときは、対応する sub_commands の実装を直接読む
- 一般的な INDEX.md 生成規則だけを確認するときは、indexing の正本仕様を直接読む
- oracle review と無関係な worktree lifecycle、merge、またはテストを扱うとき

## hash
- 8bca1e26933ec2546d6724e29ae447897a85931569345c5d07b769df1d664054

# `test_packaged_import.py`

## Summary
- packaged layout にソースツリーを複製し、隔離環境で Python import を実行して、ACP builder、oracle edit、prompt editor 入力境界、設定再公開の検証を行うテスト。packaged 配布時の import 境界、正本定義の参照、公開 API の限定を確認する実行テストへの入口。

## Read this when
- packaged layout での import、配布後の Python package 構成、または oracle と realization の import 境界を検証・変更するとき。
- oracle review や quota probe の builder が schema と完全 prompt を参照することを確認するとき。
- oracle edit、prompt editor 入力境界、ACP basic の正本型再公開、cmoc config の公開面を packaged 環境で確認するとき。
- このテストの対象となる packaging 設定、canonical builder、prompt editor 入力処理、または設定再公開の実装を変更するとき。

## Do not read this when
- packaged layout や import 境界を扱わず、通常の builder ロジックや prompt 内容だけを検証するときは、該当する個別テストや正本実装を直接読む。
- 配布構成ではなく、oracle の review schema や edit の仕様そのものを確認するときは、対象の schema または仕様書を直接読む。
- 設定定義の値や enum の挙動だけを確認するときは、cmoc config の正本定義または専用テストを直接読む。

## hash
- 16ceb03627945fb0b23a57b255a8b1cadf694266ef02c424af0d83eb23d16312

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
- 標準 prompt parts の rendering と complete prompt の組み立てを検証する回帰テスト。各 standard の注入条件、内容、相互排他、placeholder 展開、file access mode、feedback 指示、INDEX entry standard の出力境界を扱う。prompt builder の標準規則や complete prompt の構成を確認する際のテスト入口である。

## Read this when
- prompt part または complete prompt の rendering を変更・検証するとき
- standard の注入条件、既定値、相互排他、placeholder 展開を変更・検証するとき
- file access mode ごとの prompt 内容や共通 feedback 指示を変更・検証するとき
- prompt builder の回帰テスト対象と検証される主要な構成を把握するとき

## Do not read this when
- prompt builder の実装責務や正本仕様そのものを確認する場合
- prompt builder と無関係なテストや機能を調査・変更する場合
- テスト対象の具体的な標準文面や実装詳細を直接確認する必要がある場合は、対応する prompt builder の実装または正本仕様を読む

## hash
- be22fb91be8530bf1eff6ac34c17b7b11b87b9867fbe5910106b6bd9219b2696

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
- Codex argv の model、sandbox、provider 上書き契約を検証するテスト。file access mode から sandbox への変換、approval・TOML override・MCP feedback 設定、provider 選択と欠落時の失敗を扱う。
- Codex subprocess への feedback context 継承防止、schema の元バイト保持と SHA256 保存、invalid UTF-8 出力の扱いも検証する。Codex override 構築や runtime profile の挙動を確認する際のテスト入口となる。

## Read this when
- Codex argv の sandbox、model、reasoning effort、provider override の契約を変更または検証するとき
- MCP feedback の call context が Codex argv や subprocess environment に漏れないことを確認するとき
- schema の保存時ハッシュや Codex 出力 JSON のエラー処理を変更または検証するとき

## Do not read this when
- Codex override の実装詳細そのものを調査するときは、対応する runtime profile 実装と正本仕様を直接読む
- 他の runtime 機能や一般的な test 実行手順だけを確認するとき

## hash
- 2ed948eb91813f84cb0a95bf97e507b6f41cb328ce715f467409f57ea5bb5e09

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
- bin/cmoc の起動時に仮想環境の Python が利用できない場合のエラーレポートを検証するテスト。missing venv、通常ファイルでない venv パス、Python として起動できない実行ファイルを対象に、終了コード・stdout の report 構造・call stack の root token path・次のアクションを確認する。

## Read this when
- bin/cmoc の仮想環境検査、起動失敗時のエラーレポート、wrapper の call stack 表示を変更または検証するとき。

## Do not read this when
- 通常の CLI 機能や補完プローブの挙動だけを変更・調査するとき。仮想環境検査と wrapper の失敗 report に直接関係しないテストを扱うとき。

## hash
- 777dd4f6844721c51f36f16bb80f4c7d61c30c4c8853372891e7c4e3874c7335

# `test_session_cli.py`

## Summary
- session fork・join・abandon の CLI 外部挙動を、branch と永続 session state のライフサイクルとして一体的に検証する回帰テスト群。
- session branch の作成・衝突・保存失敗時の rollback、home branch への復帰、state 更新・cleanup・復元を扱う。
- linked worktree、dirty worktree、preprocess、home branch 不在、state 不正、conflict 解消、差分検査、エラー報告、session branch 削除警告など、session 操作の境界条件を検証する。
- session コマンドの挙動、session state の遷移、branch/worktree 操作、join 時の conflict resolution を確認したい場合の回帰テスト入口。

## Read this when
- session fork・join・abandon の仕様変更や不具合調査を行うとき。
- session branch、session state、linked worktree のライフサイクルや rollback を変更するとき。
- join の conflict resolution、変更範囲検査、Codex 呼び出し境界、エラー出力を確認するとき。
- doctor preprocess と session 操作の前後関係、dirty worktree や home branch 不在時の挙動を検証するとき。

## Do not read this when
- session CLI の実装詳細だけを確認したい場合は、対応する session サブコマンド実装を直接読む。
- session state の正本形式や遷移規則だけを確認したい場合は、session state 仕様を直接読む。
- conflict resolution のプロンプト生成規則だけを確認したい場合は、conflict resolution の実装・仕様を直接読む。
- session と無関係な CLI、Git 操作、一般的なテスト支援機能を調べる場合。

## hash
- 46f4688370451d46da3b01ab09b6e39e3fe7f0895ea8a39ff5bf72aa7e1246d7

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
- StructDoc の Markdown renderer に対する単体テスト。空行の縮約、code block の fence 処理、StructBlock の互換 re-export、描画済み Markdown の透過埋め込み、cmoc_ref の検証エラーを確認する。renderer の外部挙動を確認する際の入口であり、実装詳細や Oracle 原典そのものを読む対象ではない。

## Read this when
- Markdown renderer の空行処理や code block の fence 生成を確認・変更するとき
- StructBlock の互換公開や描画済み Markdown の埋め込み挙動を確認するとき
- cmoc_ref の欠落・重複・不正記法に対するエラー挙動を確認するとき

## Do not read this when
- renderer の実装詳細を直接調査するとき
- Oracle の StructDoc 定義や prompt standard の仕様を直接確認するとき
- 対象挙動と無関係なテストや機能を調査するとき

## hash
- 47d5a4c7a1dd53b0987d65acbc89ee232459d35a49eeca8c34d150fd5760a8a5

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
