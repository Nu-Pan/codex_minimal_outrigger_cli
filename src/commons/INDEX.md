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
- runtime 系 commons の主要 API を 1 か所から参照できるように集約する入口。Codex 実行・profile・config・content・CLI・error・git・logging・paths・results・state にまたがる既存 runtime 部品を再公開する役割を持つ。
- 実処理の実装本体ではなく、周辺モジュールに分散した runtime 機能への import 境界をまとめるための薄い集約層として読む。

## Read this when
- 複数の runtime commons 機能をまとめて利用している呼び出し側の import 元を確認したいとき。
- runtime 系 API の公開入口にどの関数・クラス・定数が含まれているかを確認したいとき。
- runtime commons の分割済みモジュールへ進む前に、Codex 実行、git、path、state、config などの横断的な参照関係を把握したいとき。

## Do not read this when
- 個別機能の挙動や副作用を調べたいとき。その場合は、対応する runtime commons の実装本体を直接読む。
- 新しい runtime 処理を実装・修正したいとき。この集約層ではなく、責務を持つ下位モジュールを読む。
- CLI サブコマンドの利用者向け挙動や出力仕様を確認したいとき。より直接の command 実装またはテストを読む。

## hash
- 8966f0d5a850e449686651c59834522e9dbbe9937161b01765fe8e2215085580

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

# `runtime_apply.py`

## Summary
- apply 実行に紐づく worktree 特定、pid file の読み書き、Codex subprocess 追跡、apply abandon 時の停止処理を扱う runtime 補助実装。
- PID reuse を避けるための process start time 照合、pidfd 経由の signal 送信、process group 停止、zombie を考慮した終了確認をまとめる。

## Read this when
- apply branch から managed worktree を復元する処理、または branch が checkout された linked worktree を探す処理を確認・変更したいとき。
- apply 実行中の pid file 保存、読込、削除、壊れた pid file の無視条件、Codex subprocess 追跡用 environment の扱いを確認・変更したいとき。
- apply abandon が実行中 apply process や Codex subprocess group を安全に停止する条件、警告、CmocError、SIGTERM/SIGKILL の順序を確認・変更したいとき。
- pidfd、process start time、Linux /proc、process group、zombie process を使った停止対象の同一性確認や終了待ちを調べるとき。

## Do not read this when
- apply の CLI 引数、session state の上位制御、または利用者向け出力だけを確認したいときは、command 層や state 管理の対象を読む。
- 通常の git command 実行 wrapper、worktree root の基本 path 規則、CmocError の共通定義を確認したいだけなら、runtime 共通処理の対象を読む。
- apply abandon 以外のサブコマンド仕様や、process 停止と関係しない apply 本体の作業手順を調べるときは、より直接その責務を持つ対象を読む。

## hash
- 25625f4e91acd37a8ef3835a54cfb3b03718bb4b8ecb56db40212f4f3f026937

# `runtime_cli.py`

## Summary
- CLI サブコマンドの共通実行ライフサイクルを扱う実装。work root 検査、pre-log 処理、サブコマンドログ作成、開始・実行・完了表示、戻り値の終了コード化、例外時のエラー表示、実行時間や quota 待機時間を含む完了サマリー出力を一箇所に集約する。
- 通常の標準サマリーとは別の stdout 契約を持つサブコマンド向けの結果型と、cmoc が work root で実行されている前提を検査する処理も含む。

## Read this when
- CLI サブコマンドの実行前後に共通して行うログ作成、進捗表示、完了サマリー、終了コード処理、例外表示を変更する。
- サブコマンド実装の戻り値を CLI 終了コードや stdout に変換する挙動を確認する。
- init など、runtime state の配置先や pre-log 検査のタイミングが重要なサブコマンドの実行ライフサイクルを調べる。
- cmoc が work root 以外で実行された場合のエラー内容や検査条件を変更する。

## Do not read this when
- 個別サブコマンドの業務処理そのものを変更したいだけで、共通の実行ライフサイクルや表示契約に触れない。
- サブコマンドログの内部フォーマット、イベント記録の保存方法、現在の logger 管理の詳細だけを調べたい場合は、runtime logging 側を直接読む。
- repo root、work root、時刻表示、経過時間整形の解決方法だけを確認したい場合は、runtime paths 側を直接読む。

## hash
- fa9d69da666a38b9545a60975c7d3cd29db49c818a6e4db315962330424ee39e

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
- Codex exec の実行制御を担う。単一試行ループ内で Structured Output 検証、capacity retry、quota 待機と代表 probe、resume 継続、call log と subcommand event 記録、実行後の file access rule 違反検出・回復を一体で扱う。
- file access mode ごとの書き込み許可判定、agent call 後に残った差分の検査、cmoc が生成した log・schema・output と agent が残した変更の区別もここで扱う。
- 16,000 文字を超えるが、retry counter、resume token、subprocess 結果、log/event、post-check baseline を共有する状態機械として凝集しており、exec 実行制御の責務境界内に収めている。

## Read this when
- Codex exec 呼び出しの argv、cwd、profile、CODEX_HOME、Structured Output schema、stdin prompt log、output log の生成や記録を確認・変更するとき。
- Codex CLI の capacity error、quota error、quota availability probe、resume token による再開、semantic retry の挙動を確認・変更するとき。
- agent call 後の file access rule 違反検出、回復用 Codex call、禁止 root や git 差分の snapshot、生成済み log を検査対象から除外する条件を確認・変更するとき。
- FileAccessMode に応じて oracle、realization、readonly、一時生成物への書き込みを許すかどうかの判定を確認・変更するとき。
- Codex call の console 出力、subcommand log event、call log JSON、stdout/stderr/output path の扱いを調査するとき。

## Do not read this when
- TUI 起動や画面操作の責務だけを調べるとき。
- Codex profile の具体的な生成内容、CODEX_HOME 解決、schema 準備、subprocess 実行 wrapper、Codex stdout/stderr 解析そのものを変更したいだけのとき。
- AgentCallParameter の生成内容や quota probe/recovery 用 prompt の組み立てを変更したいとき。
- git コマンド wrapper、runtime path 定義、設定読み込み、結果 dataclass、subcommand logger の一般仕様だけを調べるとき。
- apply/requeue など特定サブコマンド固有の外部挙動を調べるだけで、Codex exec 呼び出し後の差分検査や retry 制御に触れないとき。

## hash
- 456a47d57d1e38c32aabb09157000acb79b97e1e0ad84073278d0b08bbdc48bd

# `runtime_codex_logging.py`

## Summary
- Codex CLI 呼び出し後に、目的・call log path・経過時間・終了コードを利用者の console へ通知するための小さな出力 helper を提供する。
- console 表示の時刻や経過時間の整形は runtime path 系 helper に委ね、この対象は oracle が定める通知ブロックの組み立てと標準出力への即時 flush に責務を絞る。

## Read this when
- Codex CLI call の console 通知内容や表示順を確認・変更したいとき。
- Codex CLI 呼び出しの目的、call log、経過時間、終了コードを利用者へどう出すかを追うとき。
- console log 仕様に対応する実装箇所を探しているとき。

## Do not read this when
- timestamp や duration の具体的な整形規則を確認したいだけのとき。
- call log file の作成、保存場所、書き込み内容を確認したいとき。
- Codex CLI 呼び出しそのものの実行制御や subprocess 処理を調べたいとき。

## hash
- d6c16807d74cfa4ef374c6062dcd9ce3fd7c9464c0d331fb11bf238d5d5d5f6b

# `runtime_codex_preflight.py`

## Summary
- Codex 実行前に indexing preflight を差し込むためのラッパー実装。preflight の設定・解除、再入防止、直列化、目的文字列によるスキップ判定を扱う。
- 通常の Codex exec / tui 呼び出しを runtime 実装へ委譲しつつ、呼び出し前に work root または repo root を起点とした indexing を必要に応じて実行する入口。

## Read this when
- Codex 呼び出し前に INDEX 更新や indexing を自動実行する制御を確認・変更したいとき。
- indexing preflight の再入防止、ロック、スキップ条件、root 推定の挙動を調べたいとき。
- recovery 用の Codex 呼び出し前 hook がどこで渡されるかを確認したいとき。

## Do not read this when
- Codex プロセスの実際の起動、標準出力・終了コード・結果型への変換を調べたいときは、runtime 側の実装を読む。
- path placeholder や root 判定そのものの定義を調べたいときは、runtime path の責務を持つ実装を読む。
- 個別の INDEX.md エントリー生成内容や oracle / realization の分類仕様を調べたいときは、該当する仕様文書または indexing 実装を読む。

## hash
- 09f8d8853e45703b1101bf821fe1d9ecbc95dd4d29741f82338d6ac880813f86

# `runtime_codex_profile.py`

## Summary
- Codex CLI subprocess 境界で使う profile 生成、sandbox/cwd/write/read path 検査、CODEX_HOME 検証、apply child process tracking、Structured Output schema 配置、Codex JSONL の error/resume 判定をまとめる実装。
- FileAccessMode を Codex CLI が受け取れる実行環境へ変換し、cmoc 側の禁止領域や post-check 前提を保つための実行時境界を担う。

## Read this when
- Codex CLI 起動用 profile の内容、sandbox mode、writable_roots、cwd、追加 read/write path の許可判定を確認または変更したいとき。
- CODEX_HOME の解決・検証、profile ファイル生成、Codex subprocess へ渡す環境変数、Codex CLI 不在時のエラー化を扱うとき。
- apply abandon に関係する Codex child process の pid 記録、lock、process group 起動、pid 再利用検出を調べるとき。
- Structured Output schema の保存先配置、Codex output JSON の読み取り、JSONL stdout/stderr からの error detail、resume token、capacity/quota retry 判定を変更するとき。

## Do not read this when
- FileAccessMode そのものの正本定義や prompt 上のファイルアクセス規則を確認したいだけなら、oracle 側の file access rule を読む。
- Codex profile 境界ではなく、cmoc の CLI サブコマンド仕様、設定 schema、git 差分検査、runtime path 定義を調べたいときは、それぞれの担当ファイルへ進む。
- Codex subprocess の起動結果を使う上位フローや retry 全体の制御を追いたいだけなら、呼び出し側の実装を読む。

## hash
- 076a9629abb417a95c6eae9b708b6bacded4000c4203486316547c35b9151037

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
- cmoc config の永続化 JSON と runtime config 型の相互変換、既定値補完、読み書き、初期生成と正規化を担う。利用者向けの config 読み込みエラー境界もここで扱う。

## Read this when
- config JSON の保存形式、読み込み時の既定値補完、enum key map の復元、または config 不正時の利用者向けエラーを確認・変更したいとき。
- config の初期生成、既存 config の現在形式への書き戻し、または config 保存先 path を使った読み書きフローを追いたいとき。

## Do not read this when
- config 型そのものの項目定義や既定値を確認したいだけのときは、正本 config 型の定義を読む。
- config 保存先 path の決定規則だけを確認したいときは、runtime path 側の定義を読む。
- config を使う各機能の挙動や CLI command 側の処理を確認したいときは、その利用箇所を読む。

## hash
- 0e456ca44c87e3df2e1e44c788f8daa462cfeaad051b053e189371602b9651cf

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
- git コマンド実行を cmoc のエラー形式へ変換する境界と、branch・HEAD・worktree・ignore 状態に関する共通操作をまとめた runtime helper。
- cmoc 管理 branch/worktree の作成・削除制約、clean worktree 要求、.cmoc の ignore 初期化・検査、oracle file 判定など、git 状態に依存する実装の入口になる。

## Read this when
- git subprocess の呼び出し結果を利用者向けエラーへそろえる処理を確認・変更したいとき。
- 現在 branch、HEAD commit、未コミット差分、branch 存在確認など、repository 状態の取得・検査に関わる実装を扱うとき。
- cmoc 管理 worktree の作成・削除、管理外 worktree 削除防止、管理 branch namespace の判定を確認したいとき。
- .cmoc を git ignore 対象にする初期化・検査、または tracked file と ignored file の扱いを変更したいとき。
- oracle file 判定や git ignore 判定を使うアクセス制御・diff 分類の挙動を追うとき。

## Do not read this when
- CLI 引数定義、表示文言の組み立て、コマンドごとの上位制御だけを確認したいとき。
- git を介さない path model の正本仕様や、path 用語そのものの定義を確認したいとき。
- Codex や LLM への prompt 構築ロジックを確認したいとき。ただし oracle file 判定 helper の利用箇所を追う場合は読む。
- 永続 state file の schema や読み書き形式だけを確認したいとき。

## hash
- 3d23d9153ada9e6575be7247b7a3504f952d987f22cdf5811c0d29517aeb393d

# `runtime_logging.py`

## Summary
- サブコマンド実行単位のログファイルを初期化し、JSON Lines event、経過時間、quota 待機時間、step 実測値を集約する runtime logging 実装。
- 現在の制御文脈から任意参照できるサブコマンド logger を ContextVar で保持し、深い runtime helper からログ記録へ接続する入口を提供する。
- console summary と file log の共有 timing 情報、および console 表示名と JSON Lines 用 step 名を分ける制約を扱う。

## Read this when
- サブコマンド単位のログファイル生成、JSON Lines event の出力、ログレコードの共通 payload、timestamp 付与を確認または変更するとき。
- step 開始・終了、経過秒、quota 待機秒、完了サマリー向け timing 集計の挙動を確認または変更するとき。
- runtime helper から現在のサブコマンド logger を参照する仕組み、または logger の一時差し替えと復元を確認または変更するとき。
- console 表示用の step description と log event 用の step description を分ける必要がある処理を扱うとき。

## Do not read this when
- ログ保存先ディレクトリや時刻文字列の生成規則だけを確認したい場合は、それらを定義する runtime path 側を読む。
- CLI サブコマンドの呼び出し構造、ユーザー向け console 出力文面、または個別サブコマンドの業務処理を確認したいだけの場合。
- 生成済みログファイルの内容調査や実行履歴の確認が目的で、logging 実装自体を変更しない場合。

## hash
- 435c34b19e2277edd8f95d4456eadef464c857b66fc7bca81fa0646e1a77a4f8

# `runtime_paths.py`

## Summary
- 実行時に必要な root 解決、時刻・duration 表示、cmoc 管理領域の保存先 path、memo 判定、短時間の cwd 切替をまとめる共通 utility。
- oracle 側の path model で内部扱いの root resolver を、実行時エラーへ変換して runtime から使える形にする入口でもある。

## Read this when
- 実行中の repository root、worktree root、cmoc root を取得する処理を確認・変更したいとき。
- session、report、log、worktree、schema store、config などの cmoc 管理ファイル・ディレクトリの保存先を確認・変更したいとき。
- console や log に出す timestamp、duration 表示の形式を確認・変更したいとき。
- `<work-root>/memo` 判定や、一時的に cwd を変更して外部 API を呼ぶ処理を確認したいとき。

## Do not read this when
- path placeholder の定義や root path 解決仕様そのものを確認したいときは、oracle 側の path model を読む。
- CmocError の構造や表示仕様を確認したいだけのときは、runtime error を扱う定義を読む。
- 各 sub command 固有の report 内容、session state 内容、log 内容を確認したいときは、それぞれの生成・利用箇所を読む。

## hash
- f3704d5a8acf92715269020e9e67e1c714c6ea31eefd7958f4776a03e660ac3e

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
