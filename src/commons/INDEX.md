# `__init__.py`

## Summary
- cmoc の共有ランタイム helper 群に属するパッケージ入口であることを示すだけの、ごく小さい初期化本文。現時点では公開 import や初期化処理を持たない。

## Read this when
- 共有ランタイム helper 群のパッケージ境界や、この階層が cmoc の共通実行時支援を扱う領域かを確認したいとき。

## Do not read this when
- 個別の helper 関数、クラス、定数、具体的な runtime 挙動を調べたいとき。その場合は同階層の責務別 runtime 実装本文へ進む。

## hash
- 7dba2bba25cf07b27346cef2bc3541a7faac13254b97577482a98e2046a63f45

# `cmoc_runtime.py`

## Summary
- cmoc の実行時共通機能を直接実装せず、Codex 実行、設定、内容ハッシュ、CLI 呼び出し、エラー描画、git 操作、ログ、パス、結果型、状態管理などの下位 runtime API をまとめて公開する集約入口。
- この対象自体の責務は、各 runtime 領域の具体処理を置くことではなく、呼び出し側が複数の共通機能へ一つの import 面から到達できるようにすることにある。

## Read this when
- runtime 系の共通 API がどの機能群から集約されているかを確認したいとき。
- 呼び出し側の import 面を整理する変更で、既存の共通 runtime API が集約入口から公開されているかを確認したいとき。
- Codex 実行、設定、git、パス、状態など複数領域をまたぐ処理を読む前に、利用可能な共通 API の入口を把握したいとき。

## Do not read this when
- 各 API の具体的な挙動、入出力、副作用、例外処理を知りたいとき。その場合は該当する責務を実装している下位の runtime 本体を読む。
- 新しい runtime 処理の実装場所を探しているとき。この対象は集約入口であり、処理本体を追加する場所ではない。
- 設定、内容ハッシュ、git 操作、パス解決、状態ファイル操作など単一領域だけを変更する場合。その領域を担当する下位対象へ直接進む。

## hash
- 2685ce534f01e5ce3f6f5191a1baeff4bd5e26e471f8610d4dc55ad3d2401846

# `indexing.py`

## Summary
- Codex 呼び出し前の preflight として各階層の目次を再生成し、変更された目次だけを専用 commit にまとめる処理を担う。
- 目次更新の排他制御、対象ディレクトリ・子要素の列挙、既存エントリーの鮮度判定、Codex によるエントリー生成、Markdown への描画までを一つの流れとして扱う。
- ルーティング文書の自動更新に関わる git 操作、hash 計算、除外対象判定、Structured Output 検証の入口になる。

## Read this when
- Codex 実行前に目次更新を走らせる preflight の登録・実行順序・排他 lock を確認したいとき。
- どのディレクトリや子要素が目次作成対象になり、memo・git ignored・binary・隠し要素がどう除外されるかを調べるとき。
- 既存エントリーの hash 検証、再生成要否の判定、Codex 呼び出し、生成結果の Markdown 化、目次更新 commit の挙動を変更するとき。

## Do not read this when
- 個々のエントリー生成 prompt や Structured Output parameter の中身だけを確認したい場合は、その builder 側を読む方が直接的である。
- Codex 実行前の一般的な preflight 登録機構だけを確認したい場合は、runtime preflight 側を読む方が直接的である。
- path token の定義、git ignored 判定、hash 計算、設定読み込み、git 実行 helper の詳細を調べたい場合は、runtime 側や対応する仕様・helper を読む方が直接的である。

## hash
- 9e99aca5414510a3b0eff4c29a82b8141b54ba19aa1fae98f5aca9b9775ab98d

# `runtime_cli.py`

## Summary
- CLI サブコマンドの共通実行ライフサイクルを扱う実装。work root 検査、サブコマンドログの作成と現在 logger の設定、開始・実行・完了の標準出力、戻り値の終了コード化、例外時のエラー表示と終了コード化を一箇所で管理する。
- 標準サマリー以外に追加の stdout を返すサブコマンド用の結果型、work root で実行されていることの検査、完了時の標準サマリー出力 helper も含む。

## Read this when
- CLI サブコマンド実行時の共通フロー、標準サマリー出力、終了コード、例外表示、typer.Exit への変換を確認または変更したいとき。
- サブコマンドログの生成場所、現在のサブコマンド logger の設定・解除、command_invoked や command_finished の記録内容を追うとき。
- init など、runtime state を通常の root ではなく初期化対象 root に置く挙動や、その前後の pre-log check の呼び出し位置を確認したいとき。
- サブコマンドが標準サマリーに加えて独自 stdout を返す契約を扱うとき。
- cmoc が work root 以外で実行された場合のエラー内容や検査条件を確認したいとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、引数定義、永続状態の具体的な読み書きを調べたいだけのとき。
- ログファイルの内部形式、step timing の記録実装、quota wait の加算処理そのものを確認したいとき。
- root path の検出規則、timestamp や duration の整形規則そのものを変更したいとき。
- CmocError の構造や render_error の詳細な表示形式を確認したいとき。

## hash
- a466afe8e6879cc65200f1014b108f67cebc42f41f437a41f34fc04250e0234d

# `runtime_codex.py`

## Summary
- Codex CLI 呼び出し runtime の互換 import 入口。exec 実行本体と TUI 起動本体を責務別 module から再 export し、既存の `commons.runtime_codex` import path を維持する。
- この file 自体は実行制御を持たず、分割後の公開面を小さく保つための橋渡しだけを担う。

## Read this when
- 旧来の `commons.runtime_codex` import path がどの実装 module へ接続されるか確認したいとき。
- Codex runtime の責務分割後も、公開 import 面として `run_codex_exec` と `run_codex_tui` を維持する必要があるか判断したいとき。

## Do not read this when
- Codex exec の retry、Structured Output 検証、quota/capacity 制御、call log 記録を調べたいときは `runtime_codex_exec.py` を読む。
- Codex TUI の起動準備、call log、subcommand event、失敗時例外化を調べたいときは `runtime_codex_tui.py` を読む。
- Codex profile 名、Codex home、schema file、resume token、quota/capacity error 判定、output JSON 読み取りなどの個別 helper 実装だけを確認したいときは、それらを定義する profile 周辺の runtime helper を直接読む。

## hash
- bce418fcd1f6bffaed81f3724333817408657aed46183fa20819ffc1b40a7993

# `runtime_codex_exec.py`

## Summary
- Codex CLI の exec 呼び出しを 1 回の状態機械として制御する実装。profile/schema 準備、prompt/call/stdout/stderr/output log の作成、subprocess 実行、Structured Output 検証、capacity retry、quota 待機と代表 probe、resume 継続、`.agents` 変更拒否、結果オブジェクト生成をまとめて扱う。
- TUI 起動や profile 生成そのものではなく、exec 分岐の実行制御と、その実行に伴う log/event/retry/resume の整合性を読む入口になる。

## Read this when
- Codex CLI exec の argv、cwd、CODEX_HOME、profile、schema、sandbox root の渡し方を確認または変更したいとき。
- Codex CLI 呼び出しごとの prompt/call/stdout/stderr/output log、console 出力、subcommand event の記録条件や内容を追いたいとき。
- Structured Output の検証失敗時 retry、capacity error の exponential backoff、quota error の待機・代表 probe・resume 継続の制御を確認または変更したいとき。
- Codex CLI 実行後に `.agents` 配下の変更を拒否する挙動や、その失敗時にも call event を残す理由を確認したいとき。
- Codex exec の成功時に返される実行結果、経過時間、quota 待機時間、log path 群の由来を追いたいとき。

## Do not read this when
- Codex profile の具体的な生成、Codex HOME の検証、resume token 抽出、quota/capacity error 判定、output JSON 読み取りなどの低位 helper の実装だけを確認したいときは、それらを定義する profile/runtime 補助側を読む。
- TUI 起動や exec 以外の Codex 実行形態を確認したいときは、TUI 側または呼び出し元の command 実装を読む。
- subcommand logger や console logging の汎用 API 自体を変更したいときは、logging 側の実装を読む。
- path model、work root、repo root、log directory、timestamp の一般的な解決規則を確認したいときは、path 関連の実装を読む。
- Codex exec を呼び出す上位 workflow の入力組み立てや、生成された結果の利用方法だけを知りたいときは、この制御本体ではなく呼び出し元を読む。

## hash
- c87a42d5fe22435d1afc2f7579cd76a81389ac6ef2b61924d07dac504490d8c5

# `runtime_codex_logging.py`

## Summary
- Codex exec/TUI 呼び出し単位の完了サマリーを利用者の console へ出力する小さな共有 helper を扱う。
- Codex call log path、purpose、elapsed、returncode を同じ表示形式にそろえるための補助であり、exec/TUI の起動制御や retry は持たない。

## Read this when
- Codex exec/TUI 共通の console 表示形式、表示項目、timestamp や duration の出し方を変更・確認したいとき。
- Codex runtime の呼び出し完了サマリーだけを調べたいとき。

## Do not read this when
- Codex exec の retry、Structured Output 検証、quota/capacity 制御を調べたいときは `runtime_codex_exec.py` を読む。
- Codex TUI の起動準備や失敗時例外化を調べたいときは `runtime_codex_tui.py` を読む。
- サブコマンド単位の JSON Lines event 保存や quota 待機時間の集計を調べたいときは logging 側の runtime helper を読む。

## hash
- 65cfde582382659dd394662fe73f4e8796945c7ad06a7f2d2240181e63abaab8

# `runtime_codex_preflight.py`

## Summary
- Codex 実行/TUI 起動の直前に、設定済みの indexing preflight を一度だけ走らせるための薄い実行ラッパーを定義している。
- preflight の登録・解除、実行対象 root の決定、再入防止、排他制御、indexing 用途や conflict resolution 用途では preflight を省略する判定を扱う。
- 実際の Codex 実行処理そのものは runtime 側へ委譲し、この対象は実行前フックの制御だけを担当する。

## Read this when
- Codex exec または Codex TUI を呼び出す前に、INDEX.md 生成などの indexing 処理を自動実行する経路を確認・変更したいとき。
- indexing preflight の登録、無効化、再入防止、スレッド間排他、skip 条件の挙動を調べたいとき。
- Codex 呼び出し時の cwd/root から、indexing 対象 root がどう決まるかを確認したいとき。
- indexing 自体がさらに Codex exec を呼ぶ場合の循環防止や、conflict resolution 時に preflight を避ける理由を追うとき。

## Do not read this when
- Codex CLI プロセスの実際の起動、コマンドライン構築、戻り値変換、標準入出力処理を調べたいだけのとき。
- repo root、work root、cwd 変換などの path model や runtime path 解決そのものを調べたいとき。
- Codex 実行結果やコマンド実行結果のデータ構造を確認したいだけのとき。
- INDEX.md の内容生成ロジック、エントリー生成プロンプト、ファイル探索ルールそのものを調べたいとき。

## hash
- 3878cafea4f3209a564a38a3ebe0f67ca85915e34f09112258511701c00f4c48

# `runtime_codex_profile.py`

## Summary
- Codex CLI を起動する subprocess 境界で共有される不変条件をまとめる実装。FileAccessMode から Codex sandbox/profile/cwd への変換、CODEX_HOME 検証、profile 生成、child process tracking、Structured Output schema 配置、Codex JSONL/stdout/stderr からの error・quota・capacity・resume 判定を扱う。
- sandbox/profile/cwd、CODEX_HOME、process tracking、schema 配置、JSONL error 判定は同じ実行境界の失敗時文脈を共有するため、個別 helper ではなく Codex profile 境界全体の挙動を確認する入口になる。

## Read this when
- FileAccessMode と Codex CLI の sandbox_mode、workspace writable_roots、追加 read/write path の許可判定、PURE_ORACLE_READ 時の cwd の対応を確認・変更したいとき。
- Codex 起動前の CODEX_HOME 解決、auth.json を含む home 検証、profile 本文生成、内容 hash 名の profile 配置、profile 名抽出に関わる挙動を確認したいとき。
- Codex subprocess 実行時の環境変数、Codex CLI 不在時の CmocError 化、apply abandon 用の child process tracking、pid file への記録・削除、Linux proc stat の starttime 読み取りを扱うとき。
- Structured Output schema を root 配下の hash store へ配置する処理、Codex output JSON の読み取り失敗を retry 判定へ渡す処理を確認したいとき。
- Codex JSONL/stdout/stderr から利用者向け error detail、resume token、capacity error、quota error を抽出・判定する制御を変更したいとき。

## Do not read this when
- AgentCallParameter や FileAccessMode 自体の型定義・意味を確認したいだけのときは、その定義側を読む。
- Codex model や reasoning effort の設定値の出所、設定ファイル全体の読み込み・既定値を確認したいだけのときは、設定管理側を読む。
- hash 付きファイルの書き込み方法や schema store directory の path 規則そのものを確認したいときは、runtime content/path 側を読む。
- CmocError の構造、表示形式、例外全体の扱いを確認したいだけのときは、runtime error 側を読む。
- Codex CLI へ渡す prompt 本文、ACP の prompt 組み立て、LLM 出力品質そのものの評価を調べたいときは、この subprocess/profile 境界ではなく prompt・呼び出し制御側を読む。

## hash
- bfa9071b4fa3102e4d5bea1bbf7c79cb9a0c9df1176339415d3554a57fb14d99

# `runtime_codex_tui.py`

## Summary
- Codex TUI 呼び出しを行うための実行時処理を提供する。設定読み込み、call log 作成、Codex profile 準備、作業ディレクトリと CODEX_HOME の解決、外部 Codex プロセス起動、結果ログ出力、失敗時の cmoc 用エラー化を一連で扱う。

## Read this when
- AgentCallParameter から Codex TUI を起動する制御フローを確認・変更したいとき。
- Codex 呼び出し時の profile 名、CODEX_HOME、作業ディレクトリ、file access mode に応じた cwd 解決、追加 read path の渡し方を追いたいとき。
- Codex TUI 呼び出しの call log に記録される項目、保存先、コンソール通知、subcommand logger へのイベント記録を確認したいとき。
- Codex CLI/TUI の subprocess 失敗を cmoc の CommandResult または CmocError として扱う境界を確認したいとき。

## Do not read this when
- Codex profile の具体的な生成内容、環境変数の組み立て、CODEX_HOME 検証、file access mode から cwd への変換そのものを変更したいだけのときは、それらを定義する profile 系の実行時処理を読む。
- 設定ファイルの読み込み規則そのものを確認したいときは、設定読み込みの実行時処理を読む。
- ログディレクトリ、repo root、work root、timestamp などの path 解決規則そのものを確認したいときは、path 系の実行時処理を読む。
- Codex 呼び出し結果のコンソール表示形式や共通ログ基盤だけを変更したいときは、それぞれの logging 系の実行時処理を読む。

## hash
- 33918fa90c10f7b7f68a377863266e3409df173636e6c0d539b01a2fceb71d86

# `runtime_config.py`

## Summary
- cmoc の設定データを、既定値付きの内部設定モデルと JSON 保存形式の間で変換し、設定ファイルの読み込み・書き込み・同期を行う実装。
- 設定値の型変換、enum キー付きマッピングの復元、不正な設定 JSON や未初期化状態を利用者向けエラーへ変換する入口を持つ。

## Read this when
- 設定ファイルの JSON schema 相当の保存形、既定値の埋め戻し、モデル名や reasoning effort の文字列マッピングを確認・変更したいとき。
- 設定ファイルが存在しない、JSON として読めない、top-level が object でない、不正な値を含む場合のエラー文言や失敗条件を確認・変更したいとき。
- 初期化済み設定を読み込む処理、未存在時に既定設定を書き出す処理、設定ファイルの保存先 path を使う処理を追いたいとき。

## Do not read this when
- 設定モデルそのもののフィールド定義や既定値を確認したいだけなら、設定モデル定義を直接読む。
- 設定ファイルの保存先 path の規則だけを確認したいなら、runtime path を扱う実装を直接読む。
- CLI サブコマンドの引数、表示、呼び出し順を確認したいだけなら、コマンド層の実装を読む。

## hash
- 7e04d56621b72d05a69e78c781408143eb3810dcb5fd7e2d21dc666b4683665e

# `runtime_content.py`

## Summary
- ファイル内容または文字列内容から SHA-256 digest を計算し、その digest を名前に含めた内容ベースのファイル保存を行う小さな共通 helper 群を扱う。
- 出力先 directory を必要に応じて作成する保存処理と、既存 directory へ保存する処理を分け、同一内容なら既存ファイルを再利用する責務を持つ。
- 先頭 chunk の NUL byte と読み取り可否を使って、ファイルが binary かどうかを粗く判定する補助処理も含む。

## Read this when
- ファイル内容や文字列内容の SHA-256 digest 計算方法を確認・変更したいとき。
- 内容 hash をファイル名に含めて保存する runtime 生成物やキャッシュ的な出力の保存処理を確認・変更したいとき。
- 保存先 directory を自動作成する場合と、既存 directory 前提で保存する場合の挙動差を確認したいとき。
- ファイルが binary かどうかを判定する簡易 heuristic や、読み取り失敗時の扱いを確認・変更したいとき。

## Do not read this when
- パス概念そのものや `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` の定義を確認したいだけのとき。
- CLI command、出力 schema、状態遷移、実行 workflow の仕様や制御ロジックを確認したいとき。
- INDEX.md の生成・更新・ルーティング文書そのものの仕様を確認したいとき。
- 特定の利用箇所で、どの prefix・suffix・content を渡すかという上位ロジックだけを確認したいとき。
- 構造化テキストの解析、markdown 処理、oracle/realization の分類判断を確認したいとき。

## hash
- 327f8182b1ab2047a3f5f70e49d2feb4fba2029da38769d649f9ed82f4175106

# `runtime_errors.py`

## Summary
- cmoc 共通の実行時例外と、任意の例外を利用者向け Markdown エラーレポートへ変換する処理を扱う。
- エラー概要、復旧・調査手順、詳細、Call stack を含む共通エラー表示の責務を持ち、独自例外と通常例外の両方を同じ出力構造へ寄せる入口になる。

## Read this when
- 利用者向けエラーレポートの出力内容、見出し、復旧案、詳細情報、Call stack の扱いを確認または変更したいとき。
- cmoc 内で投げる実行時例外に、Summary、Next actions、Detail として表示される情報を持たせたいとき。
- 通常例外が共通エラーレポートへ変換される際の既定メッセージや detail 表現を確認したいとき。
- Next actions が不足している場合に既定案内を補う挙動を確認または変更したいとき。

## Do not read this when
- 個別コマンドや個別入力検証で、どの条件をエラーにするかだけを調べたいとき。この対象はエラーの表示形式と共通例外の器を扱う。
- 設定、作業ツリー、path、git 操作など特定ドメインの失敗原因を調べたいとき。まずその責務を持つ実装を読む。
- エラー以外の通常出力、成功時の Markdown、JSON schema、永続状態の形式を確認したいとき。
- スタックトレース生成そのものや Python 標準例外機構の詳細を調べたいとき。

## hash
- 51eb58dfc241cb76b6debfce4a06a3169cb6a2a29d0a6f123f7c5b6c0bd03e95

# `runtime_git.py`

## Summary
- git subprocess 実行と worktree/branch 操作を cmoc の共通エラー・戻り値表現へそろえる実装。detached HEAD や未コミット差分の事前条件検査、cmoc 管理 branch 判定、linked worktree 作成・削除、branch 削除を扱う。
- .cmoc を git 追跡対象外にするための ignore 判定・更新処理を担う。通常の ignore 初期化、clean worktree を保つための exclude 更新、初期化済み repository の検査、任意 path の ignore 判定への入口になる。

## Read this when
- git コマンド実行失敗を cmoc 利用者向けエラーへ変換する境界処理を確認・変更したいとき。
- 現在 branch、HEAD commit、clean worktree 必須条件、cmoc 管理 branch namespace の扱いを確認・変更したいとき。
- run/apply/session などで使う linked worktree の作成・削除や一時 branch 削除の挙動を確認・変更したいとき。
- .cmoc の git ignore 初期化、git exclude による ignore 保証、追跡対象外検査、または path が ignore されるかの判定を確認・変更したいとき。

## Do not read this when
- git 操作を呼び出す個別サブコマンドの CLI 入出力、引数解析、レポート生成だけを調べたいとき。
- cmoc の永続状態ファイルの schema や読み書き処理そのものを調べたいとき。
- git 以外の runtime error 型や command result 型の定義だけを確認したいとき。
- oracle の path keyword 定義や repository/worktree path model の仕様を確認したいとき。

## hash
- 025c1d2a729bdb9d9943161c3426f9b67ae8bd8268f74c27d8d4979c1b16ff20

# `runtime_logging.py`

## Summary
- サブコマンド実行中のイベント記録、step の開始・経過時間、quota 待機時間を集約する実行時 logger を定義する。
- 実行ごとに logs 配下へ JSON Lines の log file を確保し、event record を追記する責務を持つ。
- 深い runtime helper から現在のサブコマンド logger を参照できるよう、context ごとの current logger の設定・復元・取得を提供する。

## Read this when
- サブコマンド単位の実行 log、JSON Lines event、step_started event、完了サマリー用の step timing を調べるとき。
- Codex quota 待機時間を実行全体の待機時間として集計する処理を確認・変更するとき。
- 実行中の制御文脈に紐づく current logger を設定、リセット、参照する runtime helper の挙動を確認するとき。
- log file の生成場所、timestamp 名による排他的な確保、event record の基本項目を確認するとき。

## Do not read this when
- CLI の表示文言や利用者向けの console 出力仕様だけを確認したいとき。
- logs 配下のパス解決や timestamp 文字列の生成規則そのものを確認したいとき。
- 個別サブコマンドの業務処理、引数解析、状態更新の実装を探しているとき。
- 生成済み log を解析・集計する読み取り側の処理を探しているとき。

## hash
- 6c9b4a4c583c28c18afd061c8230290bf642e6b5004f5889d6039988207fbd45

# `runtime_paths.py`

## Summary
- 実行中の cmoc が扱うルートパス、時刻文字列、実行状態保存先、ログ・レポート・設定ファイルの配置、memo 判定、作業ディレクトリ一時変更をまとめた共通 helper 群。
- 基本層のパス解決に失敗した場合は利用者向けの共通エラーへ変換し、上位コマンドが `<repo-root>`、`<work-root>`、`<cmoc-root>` や `.cmoc` 配下の標準配置を一貫して参照するための入口になる。

## Read this when
- コマンド実行時に現在位置から `<repo-root>`、`<work-root>`、`<cmoc-root>` を取得する処理や、その失敗時メッセージを確認・変更したいとき。
- セッション、レポート、ログ、worktree、schema store、設定ファイルなど `.cmoc` 配下の標準保存先を使う実装の参照先を探しているとき。
- 内部保存用 timestamp、コンソール表示用 timestamp、経過時間表示の形式を確認・変更したいとき。
- `<work-root>/memo` 自体または配下かどうかを判定する境界、または一時的にカレントディレクトリを変更して必ず戻す処理を確認したいとき。

## Do not read this when
- パス概念そのものの定義や `<cmoc-root>`、`<repo-root>`、`<work-root>` の解決規則を確認したいだけの場合は、基本層のパスモデルを直接読む。
- 共通エラー型の構造、表示形式、終了コードなどを確認したい場合は、エラー定義側を読む。
- 特定サブコマンドがどの保存先をいつ作成・更新・削除するかを知りたい場合は、そのサブコマンド実装や状態操作の本文を読む。
- 実際のファイル入出力、JSON schema の内容、ログ本文の生成規則を調べたい場合は、この helper ではなく各機能の実装を読む。

## hash
- 6a1e0d848764448e62ddac9e8c77a56e3b35314bd0239761d7d1643cc73f4da8

# `runtime_results.py`

## Summary
- 外部コマンド実行結果と Codex exec 実行結果を受け渡すための、不変なデータ保持クラスを定義する。
- 終了コード、標準出力・標準エラー、生成テキスト・JSON、各種ログや出力先、使用 profile/schema、実行時間や quota 待機状況をまとめる共有の結果モデルである。

## Read this when
- 外部コマンドの実行結果を戻り値として扱うコードの型や保持項目を確認したいとき。
- Codex exec 呼び出し後に、生成物、ログパス、profile 情報、schema 情報、実行時間、quota 待機情報をどのデータ構造で運ぶか確認したいとき。
- 実行結果を返す関数、結果を受け取る処理、テスト fixture の期待値を変更するとき。

## Do not read this when
- 実際に外部コマンドや Codex exec を起動する制御フロー、subprocess 呼び出し、リトライ処理を調べたいとき。
- ログファイルや出力ファイルの生成・保存・削除条件そのものを調べたいとき。
- profile や schema の読み込み、検証、選択ルールを調べたいとき。
- CLI の利用者向け出力形式や JSON schema の仕様を確認したいとき。

## hash
- 149af60f60abfd4347d39a62b9b27d873af9cb1148cba531f191e860be3a9e8b

# `runtime_state.py`

## Summary
- session state file の永続化モデルと読み書き操作を扱う実装。session/apply の state 断片、JSON schema 検証、cmoc 管理 branch 名からの session_id 抽出、現在 branch に対応する state 読み込み、canonical JSON 書き戻し、home branch に紐づく active session 探索をまとめている。
- session state file の不正構造や不正な state 値、cmoc 管理外 branch、欠落した state file を CmocError として扱う境界もここにある。

## Read this when
- session state file の JSON 構造、必須 field、許容される session/apply state 値を確認または変更したいとき。
- cmoc session branch や cmoc apply branch の命名から session_id を取り出す処理、または branch 種別ごとの state file 解決を扱うとき。
- session state file の読み込み、検証、書き戻し、保存先 path、active session 探索に関する挙動を調べるとき。
- session/apply の進行状態を更新する上位処理から、永続 state の表現やエラー条件を確認したいとき。

## Do not read this when
- CLI subcommand の引数定義、画面出力、コマンド全体の制御フローを調べたいだけのとき。
- session state file の仕様意図そのものを確認したいときは、対応する oracle doc を直接読む方がよい。
- runtime path の基準ディレクトリ定義や sessions directory の組み立てだけを調べたいとき。
- CmocError の表示形式や例外クラス自体の責務を調べたいとき。

## hash
- 639a3107fd6c4d1ad5208798d2042e7bdaa8b70ba12f3984bd72b4432b5dab30
