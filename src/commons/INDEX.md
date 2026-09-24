# `__init__.py`

## Summary
- commons パッケージを cmoc の共通 runtime helper 群として説明する docstring。パッケージ全体の位置づけを確認する入口です。

## Read this when
- commons パッケージが担う全体的な役割を確認するとき。

## Do not read this when
- 個々の helper の挙動や実行フローを調べるときは、該当する runtime モジュールを直接読んでください。

## hash
- 8b50d22749d6fd880d430c393e14c6dcb919038e7b9c7ec76288c523c3d58b34

# `cmoc_runtime.py`

## Summary
- 共通 runtime API の集約点として、責務別モジュールの関数・型・定数を再公開する。公開面を確認する場合はここが入口で、各機能の処理本体は個別の責務モジュールにある。

## Read this when
- 共通 import 経由で利用できる runtime API の公開範囲を確認・変更するとき。
- 複数の呼び出し元が使う API を集約する公開面を調べるとき。

## Do not read this when
- 特定の runtime 機能の動作や修正箇所を調べるときは、その処理を実装する責務別モジュールを直接読む。
- サブコマンド固有のフローや互換 import 経路の維持が論点なら、それぞれの呼び出し元や互換用の入口を直接読む。

## hash
- 1b38a5291744c19cf1b1de0fe1fd56b23c8b5065b5671840691461780d401ec9

# `indexing.py`

## Summary
- INDEX.md 更新の共通 lifecycle を実装し、対象の列挙、既存 entry の再利用と鮮度判定、必要な entry の生成・書き込みを担う。
- 深さ順の更新、失敗時の復元、排他制御、自動 preflight と INDEX.md 差分の commit をつなぐ実行経路である。

## Read this when
- 共通インデクシング処理の対象列挙、更新順序、entry 生成の並列制御を調べる・変更するとき。
- entry の再利用と鮮度判定、更新失敗時の復元、排他制御、commit、自動 preflight との接続を調べる・変更するとき。

## Do not read this when
- entry 生成 call に渡す prompt 文面や起動パラメータ自体を調べる・変更するときは、それらを構築する専用実装を直接読む。
- インデクシングの意味要件や実行条件を変更・解釈するときは正本仕様を直接読む。
- 明示的な indexing コマンドの入力条件や利用手順だけを確認するときは、そのサブコマンド仕様を直接読む。

## hash
- 4ba775165c440665c11e7e25f5005aeb4fd35e013cccda0e900ef6a2893f9c39

# `prompt_editor_input.py`

## Summary
- `cmoc tui`、`cmoc oracle edit`、`cmoc oracle investigation` の依頼文・指示をエディタから受け取る共通入口。入力用ファイルの予約、エディタ起動、handoff の開始、入力の確定保存と抽出を担う。
- プロンプト雛形の構築や Codex の起動設定は呼び出し側に委ね、ここではエディタ入力の受け渡しを扱う。

## Read this when
- これらのコマンドに共通するエディタの選択・起動、handoff 開始、入力の保存・抽出の挙動を変更または追跡するとき。
- エディタ入力の保存先の検証や、保存時のエラー処理との連携を確認するとき。

## Do not read this when
- 特定コマンドのプロンプト雛形や、入力後の Codex 起動設定だけを変更するときは、そのコマンドやプロンプト構築の担当箇所を確認する。
- handoff の通信認証・IPC・target のライフサイクルなどの実装だけを変更するときは、handoff のランタイム担当箇所を直接確認する。

## hash
- 5350b9e1fa5ac518ba0a30ef4b5390e8e5e6e9e2d53854d6a1f7fdbd0b748447

# `runtime_cli.py`

## Summary
- 最外側の CLI サブコマンドの共通実行ライフサイクルを統括します。起動前の検査や任意の前処理、実装の呼び出し、終了結果の確定、ログ・レポート・通知、エラー処理と実行コンテキストの後始末を扱います。
- サブコマンド共通の実行順序や終了時の振る舞いを調べる際の入口です。個別処理ではなく、各コマンドを包む実行境界の責務を確認できます。

## Read this when
- サブコマンドの起動前処理から終了処理までの順序、戻り値の扱い、成功・中断・失敗時の結果確定や表示を変更・調査するとき。
- 共通ログや feedback の開始・終了、主レポート保存、TUI の中断扱い、進行表示、作業ディレクトリ検査、終了通知との連携を確認するとき。

## Do not read this when
- 特定コマンドの業務処理や実装内容だけを変更・調査するときは、そのコマンドの実装へ直接進んでください。
- ログ形式、feedback の収集・保存、主レポート生成、doctor 前処理、エラー表現、通知の個別仕様だけを調べるときは、それぞれを担当する専用コンポーネントへ直接進んでください。

## hash
- 90502962f77e6933a57773773e9cc1c27634c194964c56afca4406d0faab6fbf

# `runtime_codex.py`

## Summary
- Codex の exec と対話 TUI の実装関数を共有ランタイム API として再公開する入口。個別の起動処理や実行制御は含まない。

## Read this when
- 共有ランタイムから利用する Codex 実行 API の公開範囲や import を変更・確認するとき。
- Codex exec と TUI の呼び出し関数が共有入口から公開されているか確認するとき。

## Do not read this when
- exec の出力検証、回復、再試行などの実行時挙動を調べるときは、exec の実装を直接読む。
- TUI のプロセス起動、call log、通知 callback などを調べるときは、TUI の実装を直接読む。

## hash
- cc80041004f69b74468dbd703e186f058a367b85f21904b0b419d3a38cd687c2

# `runtime_codex_exec.py`

## Summary
- Codex exec の呼び出し全体を制御し、実行記録、回復待ち後の再開、Structured Output の検証と補正を連携させる。
- 個々の subprocess 準備や回復待ちの仕組みではなく、それらを組み合わせる呼び出し側の制御を調べる入口。

## Read this when
- Codex exec の呼び出し手順、実行記録、結果の組み立てを変更・調査するとき。
- Structured Output の検証、補正 turn、補正中の作業成果物の保護を変更・調査するとき。
- quota または一時障害からの回復確認後に、元の call を再開する流れを変更・調査するとき。

## Do not read this when
- Codex CLI の argv・環境・schema 準備、実行結果の分類など、subprocess 境界の個別処理を調べるときは、その処理を担う対象から確認する。
- 回復待ちの共有、probe の集約、中断伝播そのものを調べるときは、回復待ち機構を担う対象から確認する。
- Codex 呼び出し失敗の共通エラーテキスト変換だけを調べるときは、その変換を担う対象から確認する。

## hash
- e56520fc9aec386dc49fe79864bac60767bd87dd73a92e0deaf19985bc659eac

# `runtime_codex_logging.py`

## Summary
- Codex exec と TUI の呼び出し失敗例外を、共通のエラーテキストへ変換する。
- CmocError では概要と詳細をまとめ、それ以外の例外では文字列表現を使う。

## Read this when
- Codex exec または TUI の失敗 event に記録される例外文の扱いを変更・調査するとき。
- CmocError と通常の例外で Codex 呼び出しのエラー記録がどう変わるか確認するとき。

## Do not read this when
- Codex の起動、出力処理、再試行、回復処理、call log の作成方法を調べるときは、それぞれの実行制御側を確認する。
- 端末向け失敗 report の表示や復旧案を調べるときは、共通の例外描画処理を確認する。

## hash
- dbc22241cdd8af0da9bd7074e31f3617345bcf1035252f3a0ed0d40cce7b117e

# `runtime_codex_preflight.py`

## Summary
- Codex exec と TUI の呼び出し前に、設定された INDEX 更新 preflight を挟む共通実行境界を提供する。
- 再入抑止とロックの下で preflight を実行し、exec では本体起動直前の通知を呼び出してから実行処理へ委譲する。

## Read this when
- Codex exec／TUI 経路で INDEX 更新 preflight が起動する条件や実行 root、再入抑止・直列化の仕組みを調べたり変更したりするとき。
- preflight の登録・解除や、exec 本体の直前に呼び出し元へ通知する境界を調べたり変更したりするとき。

## Do not read this when
- INDEX 対象の探索、entry の生成・鮮度確認、更新内容の書き込みや commit を調べたり変更したりするときは、それらを担う indexing lifecycle の実装を読む。
- Codex subprocess の起動方法や exec／TUI 固有の実行動作を調べたり変更したりするときは、各実行処理の実装を読む。

## hash
- ea72c61aa6a3ec3477625e6e39c0cc470f0b56a61209f2d456784eea2045ba15

# `runtime_codex_profile.py`

## Summary
- Codex CLI の共通呼び出し境界として、sandbox・model/provider・MCP 設定と実行環境を組み立て、subprocess の追跡・停止、schema の配置、JSONL 結果の解釈を担う。
- exec と TUI の両方から使われるため、CLI の起動から結果分類までを調べる入口。

## Read this when
- Codex CLI に渡す引数、sandbox、model/provider、MCP 設定、CODEX_HOME や環境変数の挙動を変更・調査するとき。
- Codex subprocess の起動、中断・timeout、editing run の process tracking、process group の停止を追うとき。
- schema の配置や、stdout/JSONL からの error・resume token・成功／回復理由の判定を変更するとき。

## Do not read this when
- Codex exec の出力検証・補正、回復待ち、probe 後の再開制御を変更するときは、runtime_codex_exec.py と runtime_codex_recovery.py へ進む。
- TUI 固有の call lifecycle やログ記録を変更するときは runtime_codex_tui.py へ進む。共通の CLI 起動設定や subprocess 管理を変更するときはこのファイルを読む。
- feedback reporter の処理や editor input handoff の schema・transport を変更するときは、それぞれ runtime_feedback_reporter.py または runtime_editor_input_handoff_mcp.py と runtime_editor_input_handoff_protocol.py へ進む。このファイルは Codex CLI 側の MCP 設定を担う。

## hash
- 603fca718389c18e380cf5b33536e21b920c7f58d892de3f1a4dd35b7bb2fe4a

# `runtime_codex_recovery.py`

## Summary
- quota・一時障害からの回復待機を管理し、同じ条件の Codex call 間で probe と待機を共有します。
- 待機中の中断伝達、回復イベント記録、理由別の待ち時間集計も担います。

## Read this when
- 回復待機の集約条件や、quota・一時障害の待機中に起きる中断・ログ・時間集計を調べるとき。
- 回復待機へ入る前後の中断状態の伝達や、シグナル handler の設置・復元を調べるとき。

## Do not read this when
- Codex CLI の起動、結果分類、probe の実行、回復後の再開処理を調べるときは、まず runtime_codex_exec.py を読む。
- サブコマンド全体の実行ライフサイクルや interruptible の設定箇所を調べるときは、まず runtime_cli.py を読む。

## hash
- d31ca3cfcce60d91b2449e9d4ff413d9f911650b03b59e2868243a0c8574519b

# `runtime_codex_tui.py`

## Summary
- Codex TUI 呼び出し固有の起動準備、プロセス実行、call log と結果記録をまとめた入口です。

## Read this when
- cmoc から Codex TUI を起動する際の設定検証、作業場所や環境の準備、通知 callback の設定、実行結果の記録やエラー処理を調べるとき。
- TUI 呼び出しに editor input handoff や feedback 用の環境情報を渡す流れを変更するとき。

## Do not read this when
- 共通の Codex CLI 環境、設定上書き、subprocess 起動の挙動を変更するときは、その共通処理を確認するとき。
- 非対話型 Codex exec の出力検証、補正、再開処理を変更するとき。
- TUI 起動前の INDEX 更新や subcommand 側の prompt・引数生成、通知 callback の内部動作を変更するとき。

## hash
- 62811e0fac78a60c799432f482ea88bcb59880589f1a73896fff0f978d61e428

# `runtime_config.py`

## Summary
- 設定オブジェクトと永続 JSON の変換、値の検証、不正設定の利用者向けエラー化を担う。
- 設定 JSON の読み書きと、既定設定の生成・既存設定の同期を調べる入口。

## Read this when
- 設定の保存・読み込み・同期の流れや、JSON と TOML の双方で扱える値、復元時の型検証を確認するとき。
- 設定を利用する runtime 処理で、設定 JSON と実行時オブジェクトの受け渡しを調べるとき。

## Do not read this when
- 設定項目の意味・型・既定値だけを確認または変更するときは、正本の設定定義を直接読む。
- 設定ファイルの保存先や root 解決だけを変更するときは path 解決の実装を、一般的な runtime error の描画だけを変更するときは error 処理の実装を直接読む。

## hash
- a457e807e76725701f62337ebeeb9a20f81ee490608cef1010c117ed9c3b9609

# `runtime_content.py`

## Summary
- ファイル内容・文字列の SHA-256 算出、内容由来の hash 名での保存、読み取り可否と NUL byte による粗い binary 判定を提供する共有 runtime helper 群です。
- symlink の hash ではリンク文字列を対象にし、hash 名での保存では同じ directory 内の一時 file を使って置換します。

## Read this when
- 内容 hash の対象や symlink の扱い、hash 名での保存時の既存 file・symlink の処理、binary 判定の共通動作を調べる、または変更する場合。
- 複数の runtime workflow で共有される hash・保存・binary 判定の primitive 自体を変更する場合。

## Do not read this when
- index 対象の選択、directory hash の組み立て、entry の更新判断だけを扱う場合は、indexing lifecycle の実装から確認してください。
- refactor 調査履歴の同期や Structured Output schema の取得・利用フローだけを扱う場合は、それぞれの workflow の実装から確認してください。

## hash
- 655ad0b996b073ecc238dbb4e924f6d0e8137ef4dbec086d3f7dcc9b36b4d7df

# `runtime_doctor.py`

## Summary
- doctor preprocess の lifecycle を担い、Git common directory 単位の排他、index の退避・復元、設定と refactor state の同期、修復差分だけの commit をまとめる。
- Git ignore 規則、.agents の追跡状態、不要な管理対象の除去、runtime state の追跡確認、feedback reporter の利用可否を修復処理に組み込む。

## Read this when
- doctor preprocess の並行実行、利用者の staged/unstaged 変更の保全、index の復元、修復 commit の範囲を調べる・変更する。
- doctor preprocess が行う worktree / Git 修復や、設定・refactor state の同期呼び出し、feedback reporter 利用不可時の扱いを調べる・変更する。

## Do not read this when
- doctor コマンドの起動方法、進捗表示、結果や共通 CLI 処理を調べる・変更する場合。コマンド入口や CLI runtime から確認する。
- 設定や refactor state の書式、読み書き、同期規則そのものを調べる・変更する場合。それぞれの同期実装から確認する。

## hash
- 47aa1a6d33f394de15f116746c342bff525e8b83b47332f7c35bf14b27b0498d

# `runtime_editor_input_handoff.py`

## Summary
- editor input file 一つを対象とする一時 handoff target のサーバー側ライフサイクルを担い、ガイドの保持・取得、送信内容の検証・上書き、終了時の target 無効化とガイド削除を行う。
- 入力 file の安全性と target 固有の受付・後処理を調べる際の入口。

## Read this when
- editor input file の regular file・symlink 検証や、handoff による本文置換の安全性を変更・調査するとき。
- 一時 target の起動、認証済み接続の受付、submission の直列処理、終了時の drain とガイド削除を変更・調査するとき。
- target が保持するガイドの作成・取得と、その期間中の扱いを確認するとき。

## Do not read this when
- editor input の予約、エディタ起動、終了後の本文読み取り・確定保存を調べる場合は、入力編集の呼び出し側から確認する。
- 共有 schema、環境変数、target ID の形式、共通認証・client transport を調べる場合は、handoff protocol の定義へ進む。
- MCP tool の公開、agent 入力の検証、handoff 本文の生成、target への送信を調べる場合は、MCP server 側を確認する。
- agent 向け指示文やガイドの正確な文面を調べる場合は、prompt builder とガイド生成の正本へ進む。

## hash
- 6de2f85902dfd93f0b0786fcafd25fee61571abc12fd1650b8021d3c79b3e93d

# `runtime_editor_input_handoff_mcp.py`

## Summary
- Codex TUI が起動する stdio MCP server の受付点として、ガイド取得と上書きの呼び出しを振り分け、結果を MCP 応答へ変換する。
- 上書きでは、入力と起動元情報から本文を組み立て、同じ repository の active target へ届ける。MCP の受付・中継を扱うときの入口であり、共有 transport や target の実装とは責務が異なる。

## Read this when
- stdio MCP の JSON-RPC 処理、tool の公開・振り分け、入力検証後の結果やエラーの扱いを変更・確認するとき。
- ガイド取得から上書きまでの中継、送信元情報の利用、本文 builder の呼び出し、target への要求送信を追うとき。

## Do not read this when
- 入力 schema、target ID の解釈、認証や socket transport の共通処理を変更するときは、共有 protocol と正本 schema を直接確認する。
- Codex が MCP server を起動する設定、tool の有効化、環境変数の受け渡しを変更するときは、Codex 実行設定を直接確認する。
- ガイドや生成本文の正確な文面・構成を変更するときは、それぞれを定義する正本の builder と仕様を直接確認する。

## hash
- 9f2add3e38e2d306ff499ae271e5f5d7624273e4f742f1862921fc347f00170f

# `runtime_editor_input_handoff_protocol.py`

## Summary
- editor input handoff の共有 protocol 層。正本 schema の読み込み・検証、呼び出し元情報の受け渡し、target の repository routing、認証 transport と応答 framing を担う。
- 複数の handoff runtime が共有する境界や通信仕様を調べる際の入口。target の lifecycle や MCP tool の個別処理ではなく、共通の routing・transport を確認するために読む。

## Read this when
- handoff の schema 読み込み・入力検証の挙動を変更または調査するとき。
- subprocess 環境を介した送信元情報や repository の受け渡しを追うとき。
- target ID の repository 対応、認証 handshake、protocol version、応答 framing を変更または調査するとき。

## Do not read this when
- target の開始・終了、ガイド保持、editor input file の検証や書き込みを調べる場合は、target lifecycle を担う実装から確認する。
- agent 向け MCP tool、tool 呼び出しの処理、項目別入力から本文を作る流れを調べる場合は、MCP interface と本文 builder の実装から確認する。

## hash
- 17d3c7257e2338323ead131a3d0f8beb583dbd014227078b8c17c2fbd1b7e5b3

# `runtime_errors.py`

## Summary
- 共通の実行時例外に利用者向けの説明と診断情報を保持し、診断値の安全な文字列化と簡潔なエラー表示を担う実装層です。
- 個別の失敗条件や通常の終端レポートを定義する場所ではなく、共通例外とログ未初期化時の表示処理を確認する入口です。

## Read this when
- 共通例外が保持する情報や診断値の文字列化・簡易表示の挙動を変更または調査するとき。
- ログ初期化前や CLI 引数解析時にエラーがどう表示されるかを調べるとき。

## Do not read this when
- 特定の操作がどの条件で失敗するか、どの復旧手順を示すかを調べるときは、その処理の実装を直接確認してください。
- 通常の終端レポートの形式やエラー分類の規範を確認するときは、レポート・ログの実装または正本仕様を直接確認してください。

## hash
- 7aebf501056b06c1339e7a20e20c997aec60001f55a492420dbdf02dc935e836

# `runtime_feedback.py`

## Summary
- サブコマンドごとの feedback collector と、Codex call ごとの capability 登録、並列受付、rate limit、終了時の drain を管理する。
- agent observation と許可された machine event の保存連携、利用不能時の非致命な degraded 動作、reporter/collector の doctor 検査を扱う。feedback の実行時ライフサイクルと event detector を確認する入口。

## Read this when
- feedback を invocation や Codex call に紐づける処理、並列受付や終了時の drain、accepted observation の連携を変更・調査するとき。
- reporter/collector の利用可能性検査や、stable event を machine observation に変換する detector の条件を確認するとき。

## Do not read this when
- agent に公開する MCP request handling や payload の転送契約を調べるだけなら、MCP reporter の担当箇所を直接読む。
- payload schema・検証、secret redaction、path evidence、immutable observation の生成や保存を調べるだけなら、observation storage の担当箇所を直接読む。

## hash
- 847c2b8a0b1acb62d7737dda1971470d944fe7685bbd2d0da83d02bb013f30d9

# `runtime_feedback_intake.py`

## Summary
- 保存済み feedback observation の受理順序と intake 境界を管理し、remediation wave へ渡す pending input を確定する。publication 後は、処理済み observation の受理記録の cleanup も担う。

## Read this when
- observation の durable な受理順序、wave に含める入力境界、または publication 後の受理記録 cleanup を調べるとき。

## Do not read this when
- observation payload の検査・masking・raw 保存や collector の受付 lifecycle を調べるときは、それらを担う raw store・collector 側から確認する。
- wave の処理内容、run artifact、checkpoint、report cut、publication state を調べるときは、remediation・run state・feedback state 側から確認する。

## hash
- d730f6473bea9a4f073c847ff531d9441da323b88e7ab22bff7e38c078e740e6

# `runtime_feedback_reporter.py`

## Summary
- Codex call ごとの stdio MCP endpoint として `submit_observation` を公開し、JSON-RPC request を処理して loopback collector へ送信し、その応答を検証して返す。
- 担当範囲は reporter 側の MCP protocol と collector への通信境界。collector の call 管理や observation の検証・保存を調べる入口ではない。

## Read this when
- `cmoc_feedback.submit_observation` の初期化、tool 公開、call 処理、JSON-RPC response を調べるとき。
- reporter から collector への引き渡し、接続に必要な実行時 context、通信失敗や collector 応答の扱いを調べるとき。

## Do not read this when
- 入力項目や制約、observation の受理条件・redaction・保存形式を調べるときは、正本の入力 schema と feedback 仕様、collector/store 層を読む。
- reporter の起動、call ごとの環境設定、Codex MCP 設定への組み込みを調べるときは、実行時の invocation/profile 統合を読む。

## hash
- 0dd124d5c38a80dfd33af41625b587248d28cbfe98a57b1d9450903d751c0f26

# `runtime_feedback_run_state.py`

## Summary
- feedback report run の intake wave、seal、join に関する immutable artifact の保存・参照・整合性検証を担う。
- run manifest の追記・回復規則と、remediation checkpoint の監査記録・判定根拠の検証をまとめる。

## Read this when
- feedback run の wave や seal/join artifact の保存、参照、hash 検証、manifest との整合性を調べるとき。
- artifact 保存後に manifest 更新が中断した場合の回復や、run manifest の追記専用規則を確認するとき。
- remediation checkpoint の検証、issue の判定根拠、再確認履歴や監査記録の整合性を調べるとき。

## Do not read this when
- active generation、current pointer、publication 全体や cleanup の状態遷移を調べるときは、feedback state 全体を管理する実装から読む。
- feedback report の修復手順、commit・rollback、join・finalization の制御フローを調べるときは、その処理を調整する subcommand 実装から読む。
- 実装の挙動ではなく要求の正本を確認するときは、この実装が根拠としている feedback state の oracle 仕様を読む。

## hash
- 0404f94e892378154337bd1f7a78b743a2ad2a3013549ee94d88c531b1ea22cc

# `runtime_feedback_state.py`

## Summary
- Raw observation の envelope、issue と machine aggregate、report cut、active generation／current pointer の整合性を検証し、publication、cleanup、cut の破棄を扱う。
- report cut から generation の切替後まで、永続 state をまたぐ復旧と遷移の一貫性を追う入口。

## Read this when
- current pointer が選ぶ active state や issue・aggregate record の検証、破損調査をするとき。
- report cut の固定入力、checkpoint、incomplete 診断、再開・復旧の整合性を調べるとき。
- generation の公開、current pointer の切替、切替後の cleanup、未公開 cut の破棄を変更・調査するとき。
- feedback raw observation の envelope 検査規則を確認するとき。

## Do not read this when
- invocation collector、call-scoped reporter、detector の受付や停止だけを扱うときは、それらの lifecycle を担う対象へ進む。
- raw observation の受付 schema、secret masking、path fingerprint、immutable 保存だけを扱うときは raw store の対象へ、receipt の順序や high-watermark だけを扱うときは intake の対象へ進む。
- feedback run の wave、seal、join、run artifact の保存・検証だけを扱うときは run state の対象へ進む。
- CLI の操作手順や Markdown report の内容・表示だけを扱うときは、subcommand の orchestration または report 生成を担う対象へ進む。

## hash
- b9e12ba3380ce025ad0f63bc7b211b53e3cec0061e94c1787ad86db49932ac93

# `runtime_feedback_store.py`

## Summary
- agent と機械 rule の feedback observation を検証し、secret masking と evidence path の処理を経て immutable raw record として保存する。raw observation の列挙と未処理件数の計算も担う。

## Read this when
- observation の受理検査、secret masking、repo 内 evidence path の正規化や fingerprint、raw record の保存・回復を調べるとき。
- raw observation の列挙や、未処理件数と通知条件を調べるとき。

## Do not read this when
- MCP の JSON-RPC transport、agent-facing tool 結果、capability の受け渡し、Codex call の開始・終了が対象なら、reporter/client または collector lifecycle の担当箇所から読む。
- durable な受理順序と high-watermark の receipt 管理、または report cut・active state の検証や publication が対象なら、それぞれの担当箇所から読む。

## hash
- cd470dabdd57221f2964d0db231c6a7ddd75aa12302e26a85ca77bbbaf894062

# `runtime_git.py`

## Summary
- Git の状態確認、branch・worktree の管理、status path の解析、作業 tree の snapshot と復元を担う共通境界。
- Git ignore の検証・判定と、nested repository を考慮した oracle・realization file の列挙・分類をまとめ、複数の runtime から共有される。

## Read this when
- Git の共通処理や branch・worktree の安全な作成・削除を調べる、または変更するとき。
- Git ignore の設定・検証や、未追跡 file の ignore 判定を扱うとき。
- file の列挙・分類、nested repository の扱い、作業 tree の snapshot と復元を調べるとき。

## Do not read this when
- repository・worktree root や cmoc の保存先の解決だけが対象なら、path 解決を担う共通処理を読む。
- エラー表示やコマンド結果のデータ構造だけが対象なら、それぞれの共通定義を直接読む。
- サブコマンド固有の処理や復旧判断だけを調べる場合は、その判断を組み立てる処理を読む。

## hash
- 259518514122fe14c7657e049c409f288381405c4a12e2d72eafa2975b1f19e4

# `runtime_logging.py`

## Summary
- サブコマンド単位の JSON Lines イベント、警告、step 計測、待機時間を記録し、後続処理が参照するイベント記録を提供する。
- ネストした runtime helper から現在の logger を任意に参照・差し替えできるようにする。

## Read this when
- イベントの記録・flush 順序、並行書き込み、終端イベントの回復、警告処理を変更するとき。
- step 計測、待機時間の集計、または実行中 logger の共有方法を変更するとき。
- 診断ログとイベント記録がレポートや feedback 検出へ渡る流れを追うとき。

## Do not read this when
- ログ保存先、パス予約、時刻表記、経過時間の整形だけを変更するときは、それらを担う runtime の共通機能を読む。
- feedback の受付・収集・判定・保存の仕様や動作を変更するときは、その一連の処理を担う機能を直接読む。
- サブコマンドの起動・終了処理や終端結果の分類を変更するときは、実行ライフサイクルを統括する機能を読む。
- primary report の項目、描画、保存を変更するときは、レポートを担う機能を読む。
- Codex call の起動や再試行・回復の動作を変更するときは、その実行・回復を担う機能を読む。

## hash
- 17aa6c7d735a6dc9a11efaca54d933225621da3bb0f035f427af123401ad933f

# `runtime_merge_conflict.py`

## Summary
- session と editing run の join で共有される Git 競合解消処理を担い、内容競合に対する agent call と変更範囲を管理する。
- 生成 INDEX や refactor state の競合処理から、INDEX 更新、競合 marker の確認、merge commit の確定までを扱う。

## Read this when
- merge 失敗後の未統合 path の分類、agent の編集範囲検証、管理物の統合、解消後の commit 処理を追うとき。
- session join と editing run join で共有される競合解消の挙動を確認するとき。

## Do not read this when
- join の事前条件、差分検査、branch 切替、後始末など一連の流れを追うときは、該当する join 呼び出し元を読む。
- 競合解消 agent に渡す指示内容を調べるときは、join 種別ごとの parameter builder を読む。

## hash
- 7f449a1e49a259ee89a5d0fcbc993a7b19ce57b7d711b23771c03d169837223a

# `runtime_paths.py`

## Summary
- repository/worktree root の実行時解決を起点 path に対応させ、cmoc 管理データの保存先と memo 配下の判定を提供する。
- 実行時刻・経過時間の整形と、process-wide な cwd 切替の直列化・復元を担う。

## Read this when
- root 解決で起点 path がどう扱われ、解決失敗がどう実行時エラーになるかを確認するとき。
- cmoc 管理データの保存先の導出や、tracked / untracked の区分、memo 配下の判定を確認するとき。
- 時刻・経過時間の表記や、時刻付き path の重複予約を調べるとき。
- 一時的な cwd 切替の排他制御、復元、切替中かどうかの判定を調べるとき。

## Do not read this when
- root placeholder の定義や共通の path 解決規則そのものを調べる場合は、共有 path model の項目から確認する。
- 実行時エラーの保持形式や描画を調べる場合はエラー処理の項目を、個別コマンドの保存データ形式を調べる場合はそのコマンドや schema の項目を確認する。

## hash
- 8a017cb7f721c5291df27f535e8fb948d67d887ae9abd5b0a167fb4d91e5a0d3

# `runtime_primary_report.py`

## Summary
- 非対話サブコマンドの invocation ごとの report 項目を管理し、個別処理で report が作られなかった終了経路の fallback 保存と、作成済み report の検証・実行記録追記を担う。
- report の保存・置換と保存失敗の扱いをまとめる実行時層。コマンド別の項目定義や本文描画とは役割が異なる。

## Read this when
- 非対話サブコマンドの終了経路で primary report がどのように再利用または fallback 保存されるかを調べるとき。
- report 用の invocation 項目の収集や更新、保存確認、既存 report の安全な置換を変更するとき。

## Do not read this when
- report の本文構成やテンプレート、コマンドごとの保存先・必須項目を調べるだけなら、描画処理や個別仕様の定義を直接読む。
- 特定サブコマンドがどの値を確定して report に渡すかを調べるだけなら、そのサブコマンドの処理を直接読む。

## hash
- b9af89f7a318419a73703cefb4869c39e19347779f569cdaaea1fe0d708a5e9c

# `runtime_primary_report_render.py`

## Summary
- 確定済みの実行情報から fallback primary report を描画し、共通の YAML 値・実行段階・関連ログ・実行記録の整形も担う。
- 実行記録は Codex の最終出力と受理済み feedback observation を表示し、別の report や manifest からも利用される。

## Read this when
- fallback primary report の本文や、確定済み情報の Markdown 表示を確認・変更するとき。
- Codex の最終出力や feedback observation を含む共通の実行記録、または複数の report で使う YAML 値・実行段階・関連ログの整形を変更するとき。

## Do not read this when
- 対応コマンドやテンプレートの定義が対象なら定義元へ、report 項目の収集や保存・fallback の制御が対象なら report 管理元へ進む。このファイルは渡された情報の描画を担う。
- feedback publication report や remediation manifest の本体が対象なら、それぞれの生成元へ進む。このファイルが描画するのは feedback invocation の fallback 要約と、共有の実行記録である。
- editing run report 固有の本文や変更パスの表示が対象なら、その report の生成元へ進む。このファイルは共通の値・実行段階・ログ整形を提供する。

## hash
- a07333f44f58cb864e181a4adb74a83661069825983aec59bbcc81e01a357217

# `runtime_primary_report_specs.py`

## Summary
- 非対話サブコマンド用 fallback primary report の個別設定をまとめ、コマンド名から適用する設定を引く入口。
- doctor、indexing、session の fork/join/abandon、oracle edit、realization の apply/refactor fork、run の join/abandon、feedback report を扱う。

## Read this when
- 非対話サブコマンドが fallback primary report の対象か、どの個別設定を使うか確認・変更するとき。
- 対象コマンドの fallback report の保存先、役割、見出し、必須情報、描画テンプレートの割当を調べるとき。

## Do not read this when
- 既存 report の再利用・保存確認や、report がまだ作られていない終了経路の処理を調べるときは、fallback report の保存・制御処理へ進む。
- report 本文の組み立てや個別テンプレートの出力を調べるときは、report 描画処理へ進む。
- 個別サブコマンドが定める report 内容や終了条件、または TUI の通知境界を確認するときは、該当するサブコマンド仕様や通知仕様へ進む。

## hash
- 65ca5fc4c11b5cba1fbf37529e57f05ec073d09bc90569b39c1607b75bbc6ed1

# `runtime_refactor.py`

## Summary
- oracle／realization file ごとの refactor 調査 state を検証・読み込み・保存し、ファイル集合と内容ハッシュに応じて調査要否を同期する。
- 調査対象の選択と、新しい調査サイクルで全対象を調査必須にする処理を担う。

## Read this when
- refactor の調査履歴 state の検証・永続化や、変更された file を再調査対象にする条件を確認・変更するとき。
- 次に調査する対象の選択順や、調査サイクルの開始時に対象を再設定する処理を確認・変更するとき。

## Do not read this when
- oracle／realization file の列挙や分類の動作だけを確認・変更するときは、Git による file 分類を担う境界を読む。
- state の保存先だけを確認・変更するときは、path を定義する境界を読む。

## hash
- ce6d02c55f306b2ef28ece6045424dd668556d9e5a880211f5224de89953f27d

# `runtime_results.py`

## Summary
- CLI・外部コマンド・Codex exec が共有する結果データのモデルを定義する。最外側サブコマンドの終端情報、コマンド実行結果、Codex exec の出力と実行情報、Structured Output の検証エラーを扱う。
- Codex exec の Structured Output を呼び出し側が参照するための最小契約も提供する。

## Read this when
- 共有する結果データの構造や整合性条件を変更するとき。
- Codex exec または外部コマンドの結果をどの形で保持し、利用側へ渡すかを追うとき。

## Do not read this when
- コンソール表示、report、ログ、terminal result の意味や規則を確認・変更するときは、出力規則の正本を直接読む。
- Codex exec の呼び出し、Structured Output の補正、再実行などの規則を確認・変更するときは、Codex exec の正本仕様を直接読む。
- 特定サブコマンドの処理手順や結果値の設定方法を変更するときは、そのサブコマンドの実装へ進む。

## hash
- 0e0e254cc674e01b2d54a82f64802d073e4e04634d506c59efc79455c25330b8

# `runtime_run.py`

## Summary
- editing run で共有する worktree の解決、lifecycle lock、process tracking と停止・cleanup を担う共通 runtime の入口。
- 個々の run command の手順ではなく、複数の経路が使う worktree と process cleanup の振る舞いを調べる対象。

## Read this when
- session branch や run branch から worktree を安全に特定する条件、または managed run worktree の検証を調べる・変更するとき。
- editing run 本体や追跡中の Codex child の identity、tracking file、停止、残存 process group の cleanup を調べる・変更するとき。
- session 操作と editing run の開始・終了で共有する lifecycle lock を調べる・変更するとき。

## Do not read this when
- run の開始、状態遷移、差分検査、commit、join・abandon の実行順や cleanup 方針だけを調べる・変更するときは、lifecycle orchestration や該当 command の処理へ進む。
- OS process identity、signal、process group 操作、Codex subprocess の起動・追跡といった下位 primitive だけが対象なら、その Codex runtime helper へ進む。この対象はそれらを run 単位の tracking と cleanup に組み合わせる。
- 利用者向け command semantics を確認するときは command 定義と該当する正本仕様へ進む。ここは共通 runtime の実装を扱う。

## hash
- e4b79dd7896358d8e93f2bde8bb0c9e1a3698c3d4ac4aee8d1405cb328391624

# `runtime_run_join.py`

## Summary
- editing run の join で共有される前処理・差分検査・merge 処理を担い、doctor による修復差分を区別し、想定外差分の扱い、競合解決、失敗時の session 復元を行う。
- merge 後の INDEX 更新と refactor state 同期、join 済み run の worktree・branch cleanup までを扱う。コマンドごとの手順ではなく、明示的な run join と remediation workload の self-join が共有する処理を追う入口。

## Read this when
- 明示的な run join や remediation workload の self-join で、clean・差分検査、force-resolve、merge と競合解決、merge 後の同期、失敗時の復元を変更・調査するとき。
- doctor が追加した差分を join の検査対象からどう区別するか、または join 済み run の worktree・branch cleanup の成否条件を確認するとき。

## Do not read this when
- editing run の context 作成、state 遷移、lifecycle lock、差分分類の規則を調べる場合は、run lifecycle の共通処理を確認する。
- worktree の特定、process identity、Codex child の追跡・停止を調べる場合は、run process と worktree 管理の共通処理を確認する。
- ユーザー向け join コマンドや remediation の引数処理、個別の手順・report 発行を調べる場合は、該当するコマンドの調整処理を確認する。

## hash
- b1a70730bc31ae1448af435040dc48ca62cb445e6e4863a402fc0242df23d538

# `runtime_run_lifecycle.py`

## Summary
- editing run 共通のライフサイクルを担い、開始条件の検査、run の開始・解決・回復、state 遷移を扱う。
- work unit の commit／rollback、差分の列挙と許可範囲の判定、run 内の INDEX 更新を呼び出す共通処理も提供する。

## Read this when
- editing run の開始条件、run context の解決・回復、state 遷移の条件を調べる・変更するとき。
- work unit の差分処理や、agent／run が変更できる path の判定を調べる・変更するとき。

## Do not read this when
- worktree の探索や追跡 process の停止・cleanup が対象なら、process lifecycle を担う実装から読む。
- join／abandon の merge、report、cleanup の実行順が対象なら、それらを調整する lifecycle 実装から読む。
- INDEX.md の探索、entry 生成、鮮度検査、復元、lock、commit が対象なら、indexing lifecycle の実装から読む。

## hash
- 8d81f261e3896261ed4ef33194a55083e3173a3049af31ceaa136a7ca7575947

# `runtime_run_report.py`

## Summary
- 編集 run の fork・join・abandon report を Markdown と YAML Front Matter で組み立て、保存する共通処理。
- 実行段階や関連ログ、変更 path の描画も担うため、個別コマンドの処理ではなく共有 report の形式や保存を確認するときの入口。

## Read this when
- realization apply/refactor の fork report の構成や保存を調べる、または変更するとき。
- run join/abandon report の共通項目、詳細、ログ、変更 path の表示を調べる、または変更するとき。

## Do not read this when
- run の state 遷移、branch/worktree 操作、merge、cleanup 自体を変更するとき。該当する lifecycle の処理から確認する。
- 他のサブコマンド向け fallback report の生成や汎用 rendering を調べるとき。fallback report の実装から確認する。

## hash
- 8bd3e53a80b180d5efe443146380e27977953c9217da1758b3cc7bb411e15793

# `runtime_state.py`

## Summary
- session と編集 run の永続状態モデルを定義し、JSON の構造や値を検証して読み書きする。
- branch 名から session state を特定する共通処理、home branch に紐づく active session の検索、session lifecycle 用の排他 lock を提供する。

## Read this when
- session/run state のスキーマ、読み書き、妥当性検証、branch に基づく state 解決を調査・変更する場合。
- active session の検索や session lifecycle で共有する排他 lock の役割を確認する場合。

## Do not read this when
- 個別の session コマンドの事前条件、branch 操作、状態遷移、終了報告を調べる場合は、該当コマンドの仕様と実装から読む。
- 編集 run の開始から join または abandon までの処理順や workload 固有の挙動を追う場合は、run lifecycle 共通処理または対象 workload の仕様と実装へ進む。

## hash
- 5ea0c7423ab0802ad641c4ab0261df8daafb98ae165de6a3cd56223766a955b0

# `runtime_windows_toast.py`

## Summary
- Windows toast の送信と Codex TUI 完了通知 callback の実行を担い、通知に含める情報、対象 session の判定、turn の重複排除、一時 state の管理を行う。
- 通知処理の失敗を呼び出し元の処理結果へ波及させない境界でもある。

## Read this when
- Windows toast の transport や表示文面、通知失敗時の扱いを変更・調査するとき。
- Codex TUI callback の root session 判定、turn の重複排除、callback state の作成・破棄を変更・調査するとき。

## Do not read this when
- TUI 起動時に callback を登録する条件や hook command の渡し方を調べるときは、TUI process の起動を組み立てる側から確認する。
- サブコマンドの terminal state を決めて通知を呼び出すタイミングを調べるときは、サブコマンド実行を管理する側から確認する。

## hash
- ec2ff9d13fb19e614e1d22b439fa0d5470ba01bdaeddf51c7c37a9bba7130fde
