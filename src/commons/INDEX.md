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
- 共通ランタイム機能を単一の入口から再エクスポートする集約モジュール。Codex 実行、プロファイル、設定、ファイル内容、CLI、エラー、Git、ログ、パス、結果、状態管理にまたがる runtime_* 系 API をまとめて参照できるようにする。

## Read this when
- 複数の共通ランタイム API をまとめて import している箇所の依存元を確認したいとき。
- runtime_codex_profile、runtime_git、runtime_state など複数の commons runtime モジュールにまたがる公開入口を把握したいとき。
- この集約モジュール経由で利用できる共通関数・型・定数の範囲を確認したいとき。

## Do not read this when
- 個別 API の実装、引数、失敗時挙動を確認したいとき。その場合は該当する runtime_* モジュールを直接読む。
- 新しい共通処理を実装・修正したいとき。このファイルではなく、責務を持つ個別モジュールを読む。
- CLI サブコマンド、Git 操作、状態管理など特定領域だけを調べたいとき。対象領域の専用モジュールを直接読む。

## hash
- 1f4b3c37a1e680ec77e3065cb3cd68676b0d79551bbc1f65b89c78719cfabf24

# `indexing.py`

## Summary
- Codex 呼び出し前の INDEX 更新 preflight、排他制御、差分 commit、ディレクトリ走査、既存エントリー再利用、エントリー生成、hash 鮮度判定、Structured Output 検証と Markdown 描画をまとめて担う実装。
- INDEX.md の自動最新化を、git 管理領域の lock、git ignore・memo・binary・symlink 除外、深い階層からの更新、同一深度の並列生成という制御で成立させる。
- エントリー本文の形式検証、対象内容の取り出し、対象 hash の再帰計算、Codex 実行関数への entry 生成依頼までを一連の indexing 実行経路として読む入口になる。

## Read this when
- Codex 実行前に INDEX.md を自動更新する preflight の登録・実行順序・commit 作成条件を確認または変更したいとき。
- INDEX.md 作成対象に含めるファイルやディレクトリ、除外する memo・git ignored・binary・symlink・隠し要素の判定を調べたいとき。
- 既存 INDEX.md エントリーの再利用条件、hash の抽出・検証、対象内容の hash 計算、再生成が必要になる条件を追いたいとき。
- Codex へ単一エントリー生成を依頼する引数、実行 root・cwd・config・purpose の扱い、生成結果の schema 検証と Markdown 変換を確認したいとき。
- INDEX.md 更新処理の並列化粒度、子孫を先に完了させる更新順序、排他 lock の配置や保持範囲を変更する必要があるとき。

## Do not read this when
- INDEX.md エントリーのプロンプト文面や標準文言そのものを変更したいだけなら、プロンプト構築側または正本仕様側を先に読む。
- git コマンド実行、設定読み込み、repo root 解決、hash 計算、binary 判定、git ignore 判定などの低レベル runtime helper の内部挙動を調べたいだけなら、それぞれの runtime 実装を直接読む。
- 個別 CLI コマンドの利用者向け挙動や通常のサブコマンド処理を調べたいだけなら、CLI command 実装側を読む。
- INDEX.md の仕様意図や oracle 上の正本要求を確認したいだけなら、対応する oracle doc を読む。

## hash
- 6ba17c4c80501d669fa28fcf2b4202f71ff6a7c45240909755758c3e971c5982

# `runtime_cli.py`

## Summary
- CLI サブコマンド共通の実行ライフサイクルをまとめる実装。work root 検査、pre-log 処理、サブコマンドログ作成、開始・実行・完了の標準出力、戻り値の終了コード化、例外時のエラー表示、現在のサブコマンド logger の設定と解除を扱う。
- 標準サマリー以外の stdout を返すサブコマンド向けの結果型と、cmoc が work root で実行されていることを検査する共通関数、完了時サマリー出力の helper も含む。

## Read this when
- CLI サブコマンドの共通実行順序、標準の進捗表示、完了サマリー、終了コード処理、例外表示の挙動を確認または変更したいとき。
- サブコマンドログの生成場所、runtime state の root 選択、init などでログ作成前に行う検査、現在のサブコマンド logger の扱いを追いたいとき。
- サブコマンド実装から独自 stdout と終了コードを返す契約、または work root 以外で実行された場合の共通エラーを調べたいとき。

## Do not read this when
- 個別サブコマンドの引数定義、CLI アプリへの command 登録、または各サブコマンド固有の処理内容だけを知りたいとき。
- サブコマンドログファイルの内部形式、step timing の記録方法、quota 待機時間の更新方法そのものを調べたいとき。
- repo root や work root の検出規則、タイムスタンプや経過時間の整形規則そのものを確認したいとき。

## hash
- add81e2cda35041a82bd78cd995edbaca0e6561e6da1438a9ee203063373515c

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
- Codex exec の単一試行ループと、その再試行・検証・ログ記録・file access rule 事後検査を扱う実行制御モジュール。
- Structured Output 検証、capacity retry、quota 待機の代表 probe、resume 継続、Codex call log と subcommand event の記録を、同じ subprocess 結果と retry 状態を共有する状態機械としてまとめている。
- agent call 後に残った file access rule 違反の検出・修復、変更 path の列挙、禁止 runtime 領域の filesystem 差分検査も扱う。

## Read this when
- Codex exec 呼び出しの argv、stdin prompt log、output schema、resume token、CODEX_HOME/profile/cwd の扱いを確認または変更したいとき。
- Codex CLI の capacity error、quota error、quota availability probe、semantic retry、Structured Output 検証失敗時の挙動を調べたいとき。
- Codex call の console 出力、call log、stdout/stderr/output log、subcommand event payload の生成条件や内容を確認したいとき。
- agent call 後の file access rule 違反検出、禁止領域の差分検査、違反回復用 Codex exec の呼び出しを変更したいとき。
- worktree の変更 path を git status から取得する処理や、FileAccessMode ごとの書き込み許可判定を確認したいとき。

## Do not read this when
- TUI 起動や exec 以外の Codex 実行入口を探しているとき。
- Codex profile、schema、CODEx_HOME、subprocess 実行、出力 JSON 読み取りなどの低レベル runtime helper の詳細だけを変更したいとき。
- AgentCallParameter の構造や file access mode の定義そのものを確認したいとき。
- quota availability probe 用 prompt の正本または builder の内容を変更したいとき。
- ログの保存先 path や work root/repo root の解決規則そのものを調べたいとき。

## hash
- 748df3cb6581450c7a97c3ec2d1a5041a20fed2f967e3821250272a2a1c0866b

# `runtime_codex_logging.py`

## Summary
- Codex CLI 呼び出し完了時に、目的、呼び出しログ位置、経過時間、終了コードを利用者向け console へ通知するための小さな出力 helper を定義する。
- 時刻表記と経過時間表記は共通の runtime path 系 helper に委ね、oracle が定める console 通知形式に沿った複数行メッセージを標準出力へ即時 flush する入口である。

## Read this when
- Codex CLI 呼び出し後に利用者の console へ出す通知内容、表示順、表示項目を確認または変更したいとき。
- Codex CLI 呼び出しログへの参照、経過時間、終了コードをどのように人間向け表示へ整形しているかを追いたいとき。
- console 用の時刻文字列や duration 文字列を使った Codex CLI 呼び出し通知の実装箇所を探しているとき。

## Do not read this when
- Codex CLI 呼び出しそのものの実行、プロセス起動、標準入出力の捕捉、戻り値制御を調べたいとき。
- ログファイルの生成、保存先決定、ファイルへの書き込み仕様を調べたいとき。
- 汎用的な runtime path の解決、時刻文字列や経過時間文字列の詳細な整形規則を調べたいとき。
- Codex 以外の CLI 通知や、利用者向け console 出力全般の設計を広く調べたいだけのとき。

## hash
- f958a19df4363d9585a17c45b2fee6d85d6cd968c79555d33f83707bdfbf8aca

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
- Codex CLI を起動する subprocess 境界で必要な profile 生成、sandbox/cwd/writable/read path 判定、CODEX_HOME 検査、child process tracking、schema 配置、出力 JSON/JSONL の error 判定をまとめる実装。
- FileAccessMode から Codex CLI が理解する sandbox profile と実行環境へ変換し、cmoc 側の読み書き許可境界を Codex profile と実行前後の検査で保つ責務を持つ。

## Read this when
- Codex CLI 呼び出し前に渡す profile、sandbox mode、writable_roots、cwd、CODEX_HOME、subprocess env の挙動を確認・変更したいとき。
- FileAccessMode ごとの追加 read path / writable path の許可判定、oracle conflict 解消時の例外的な書き込み許可、git ignored path の扱いを確認したいとき。
- apply 実行中の Codex child process を pid file に記録・削除する処理や、abandon との競合を避ける lock の挙動を確認したいとき。
- Structured Output schema の配置、schema なし出力 JSON の読み取り、Codex JSONL stdout/stderr から利用者向け error detail、resume token、capacity/quota error を判定する処理を確認したいとき。

## Do not read this when
- prompt 本文に載せる file access rule や oracle/realization の定義そのものを確認したいだけなら、対応する oracle 側の仕様断片を読む。
- Codex subprocess 境界ではなく、上位の agent call orchestration、CLI subcommand の流れ、設定値の正本定義を確認したいだけなら、それぞれの呼び出し元や設定定義を読む。
- 一般的な git 操作、runtime path の組み立て、hashed file store の実装だけを確認したい場合は、それぞれの専用実装を読む。

## hash
- 01b2fef23152c749c3e249f32817547a6c20c65aa84f1d7c278055887e5e03e8

# `runtime_codex_tui.py`

## Summary
- Codex TUI 呼び出しを、実行プロファイル作成、作業ディレクトリ決定、call log 記録、実行結果の console/log event 出力、失敗時の cmoc エラー化まで含めて扱う実行入口。
- agent call parameter と runtime config から Codex CLI/TUI 用の profile、CODEX_HOME、実行 cwd、環境変数を組み立て、TUI サブコマンド相当の外部プロセス起動を担う。
- Codex TUI 実行時の call log に残す metadata、実行時間、returncode、logger event payload の生成責務を持つ。

## Read this when
- Codex TUI を起動する実装、引数、cwd、CODEX_HOME、profile 名、file access mode に応じた実行位置を確認または変更したいとき。
- TUI 呼び出しの call log JSON、console 出力、subcommand logger の event 内容、失敗時のエラーメッセージを調べたいとき。
- linked worktree や追加 read path を含む TUI 実行 profile の準備経路を追いたいとき。

## Do not read this when
- Codex exec や非 TUI の agent call 実行経路を調べたいだけのとき。
- profile 作成、CODEX_HOME 解決、file access mode から cwd を決める詳細実装そのものを確認したいとき。
- cmoc の設定読み込み、runtime path 計算、CommandResult、CmocError の一般的な仕様や実装を確認したいとき。

## hash
- 282709994a710f28c42883f934e94c9c2d1ae4a36a91fefc1f755598a316f5e9

# `runtime_config.py`

## Summary
- cmoc の設定ファイルを `CmocConfig` と JSON object の間で変換し、設定ファイルの読み込み・書き込み・存在しない場合の同期生成を行う runtime 設定処理。設定値の既定値補完、enum key の復元、不正 JSON や不正な値に対する `CmocError` への変換を担う。

## Read this when
- `.cmoc/config.json` の読み書き、初期生成、既定値補完、または JSON schema 相当の実装挙動を確認・変更したいとき。
- `CmocConfig` と永続化 JSON の対応、model や reasoning effort の enum key 変換、設定値の数値変換エラー処理を調べたいとき。
- 設定ファイルが存在しない、JSON として読めない、top-level が object でない、不正な型を含む場合の利用者向けエラーを確認したいとき。

## Do not read this when
- 設定データクラスそのものの定義や既定値を確認したいだけなら、設定型を定義している対象を読む。
- 設定ファイルの配置パスの決定だけを確認したいなら、runtime path の対象を読む。
- ACP の model class や reasoning effort の enum 定義だけを確認したいなら、ACP 基本型の対象を読む。

## hash
- 9bc797d6ae683de03d7f73ecba67078ac5048aba263a064e4a99e34b0b5aead5

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
- Git コマンド実行を cmoc の結果型・利用者向けエラーへ変換し、branch、HEAD、clean worktree、linked worktree、branch 削除、ignore 判定を扱う共通実装。
- .cmoc 管理領域の worktree 作成・削除を、branch namespace と管理下 path の対応確認に基づいて制限する。
- .cmoc を git 追跡対象外に保つための .gitignore、git exclude、index 状態の更新・検査と、oracle/realization 判定で使う ignore helper を提供する。

## Read this when
- git subprocess の呼び出し、失敗時の CmocError 変換、CommandResult の扱いを確認・変更したいとき。
- cmoc 管理 branch の判定、run/apply 用 linked worktree の作成・削除、worktree path の安全確認に関わる挙動を調べるとき。
- .cmoc の ignore 初期化、clean worktree を保つための exclude 更新、git check-ignore による対象判定を扱うとき。
- detached HEAD、未コミット差分、branch 存在確認、HEAD commit 取得など git repository 前提条件の共通処理を変更するとき。

## Do not read this when
- CLI 引数定義、サブコマンドの利用者向け制御フロー、表示文言だけを調べたいとき。
- git を使わない path model、prompt 組み立て、状態ファイルの schema だけを確認したいとき。
- oracle file や realization file の概念定義そのものを確認したいとき。
- 特定サブコマンドの仕様根拠やユーザー操作単位の挙動を読みたいだけで、git 共通処理の実装詳細を変更しないとき。

## hash
- 15cb165e66243e3f32378864165e42984718c8920ba2978b0ff521353cf57366

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
- 実行時に必要なルート解決、時刻文字列、実行状態を置くディレクトリや設定ファイルのパス、memo 配下判定、作業ディレクトリ一時変更をまとめる共通 helper。
- repository/worktree の位置特定失敗を CmocError に変換し、CLI 実行場所に依存する処理が共通の失敗時挙動を使うための入口になる。

## Read this when
- 実行時の repository root、worktree root、cmoc root の解決方法や、解決失敗時のエラーメッセージを確認・変更したいとき。
- sessions、reports、logs、worktrees、codex log、schema store、config など、`.cmoc` 配下の保存先パスを作る処理を確認・変更したいとき。
- timestamp や console 表示用 timestamp、経過時間表示の形式を確認・変更したいとき。
- memo 自体またはその配下を判定する処理や、処理中だけ cwd を切り替えて必ず戻す文脈管理を使う・修正するとき。

## Do not read this when
- path placeholder の種類、抽象的な path model、実パス解決の正本仕様を確認したいだけなら、path model 側の仕様・実装を読む。
- 個別サブコマンドがどの保存先をいつ作成・更新・削除するかを知りたいときは、そのサブコマンド側の実装を読む。
- CmocError の構造、表示形式、例外の共通扱いを変更したいときは、runtime error 定義側を読む。
- ファイルシステム操作全般、Git 操作、設定 JSON の読み書き内容を確認したいだけなら、それぞれの責務を持つ別の実装を読む。

## hash
- 7415276735049b6804964a29f6671212540142e6dec612218466b2617747e2fc

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
