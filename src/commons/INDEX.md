# `__init__.py`

## Summary
- cmoc の実行時に複数箇所から共有される補助機能をまとめる領域の入口。
- 対象そのものは共有 runtime helper 群のパッケージ境界を示すだけで、個別 helper の責務は下位要素の本文で確認する。

## Read this when
- cmoc の実行時処理で、複数モジュールから使う共通 helper の配置場所や入口を確認したいとき。
- 共有 helper 群の下位要素へ進む前に、この領域が runtime helper 用のまとまりであることを確認したいとき。

## Do not read this when
- 特定の helper の実装、入出力、失敗時挙動を確認したいとき。この対象ではなく、該当する下位要素の本文を読む。
- CLI コマンド固有の処理やテスト固有の処理を調べたいとき。共有 runtime helper ではなく、より直接その責務を持つ対象へ進む。

## hash
- 7dba2bba25cf07b27346cef2bc3541a7faac13254b97577482a98e2046a63f45

# `cmoc_runtime.py`

## Summary
- `commons` 配下の実行時共通基盤を集約する入口。Codex 実行前後の環境準備、設定・状態・ログ・パス・Git・エラー処理・結果型を横断的に使うときに読む。

## Read this when
- サブコマンド実行の前処理や後処理、`codex` 呼び出しの準備、設定や状態ファイルの読み書き、作業ツリーやブランチの管理、ログやレポート出力、共通エラー整形を扱うとき。

## Do not read this when
- 個別サブコマンドの入出力や制御フローだけを見たいときは、そのサブコマンド側を直接読む。実行基盤ではなく業務ロジックの詳細を探す目的ではここを起点にしない。

## hash
- 555239502325c251dbb9f35d6e2bf255b5c273cdfe678a81366abb59f02df9b3

# `indexing.py`

## Summary
- `INDEX.md` の生成・更新と、そのための対象列挙、既存エントリの再利用判定、Codex 実行、Markdown への再整形をまとめる。
- `cmoc` の indexing 前処理を登録・直列化・コミットする入口であり、index 更新の排他、差分検出、失敗時の扱いを確認したいときに読む。
- index 対象の探索条件、対象内容の要約用入力、Structured Output の検証とレンダリングの境界を把握したいときに読む。

## Read this when
- INDEX.md を自動更新する処理、または indexing preflight の流れを変更したい。
- 対象ディレクトリや対象ファイルの選別条件、hash による再利用判定、生成結果の検証条件を確認したい。
- Codex の呼び出し条件、ログ/作業ディレクトリの固定、更新 commit の作成条件を確認したい。

## Do not read this when
- `INDEX.md` に書くべき具体的なエントリ文面そのものを編集したいなら、別の prompt/標準定義の本文を読む。
- `cmoc` 全体の CLI 解析や設定値の定義を見たいなら、ここではなくそれらを扱う実装を読む。
- index 生成以外の Git 操作や一般的なファイル入出力の実装を追いたいなら、より直接の処理箇所を読む。

## hash
- 46866024a115d65e3c91bb9b503e4d17fa725d906460ac326e88e17e97bd0e6b

# `runtime_apply.py`

## Summary
- `cmoc apply abandon` の cleanup と、そのために必要な worktree 解決・apply process ID 追跡・child process group 停止をまとめて扱う共通実装。`cmoc apply abandon` の挙動、停止対象の同一性確認、pidfile 生成/読取/削除、process group の終了確認を見たいときに読む。

## Read this when
- `cmoc apply abandon` の削除対象 worktree/branch を特定する処理を確認したい。
- apply 実行中 process の記録・読取・削除、または PID 再利用を避けた停止判定を変えたい。
- Codex subprocess を process group 単位で止める条件や、pidfd が使えない環境でのエラー扱いを確認したい。

## Do not read this when
- session state の読み書きや branch 遷移そのものを追いたいだけなら、より上位の session/apply コマンド実装を読む。
- 一般的な git worktree 操作や process 管理の共通基盤だけを見たいなら、この apply 専用実装ではなく該当する汎用モジュールを読む。
- `cmoc apply abandon` 以外のサブコマンドの入出力仕様だけを確認したいなら、このファイルは読まず各サブコマンド実装へ進む。

## hash
- 083122281aa88bc209cecf31e649d34eac38ce7b226a5b09ad220dba4158a400

# `runtime_cli.py`

## Summary
- CLI サブコマンド共通の実行ライフサイクルをまとめる。work root 検査、doctor preprocess の呼び出し、サブコマンドログの初期化、step 通知、完了サマリー、例外時の終了コード化と stderr/stdout の振り分けを一箇所で扱う。
- 個別サブコマンドの業務処理ではなく、サブコマンド共通の実行順序や失敗時の見せ方を変えるときに読む。

## Read this when
- 新しいサブコマンドをこの共通実行経路に載せるとき。
- work root での実行制約や、runtime state を repo root に置くか work root に置くかの判断を変えるとき。
- doctor preprocess を挟む位置、step 開始通知、完了サマリー、returncode の扱いを調整するとき。
- 例外を標準出力と標準エラーのどちらに出すか、または `CliRunResult` の stdout 契約を変えるとき。

## Do not read this when
- 各サブコマンド固有のビジネスロジックだけを変更するとき。
- サブコマンドログの保存形式や詳細イベント仕様だけを変えたいときは、ログ実装側を読む。
- doctor preprocess の修復内容そのものを変えたいときは、doctor preprocess 側を読む。
- エラー文言の生成ルールだけを変えたいときは、エラー整形側を読む。

## hash
- b09cd25b8c1c7599ad0d0e6df775f89211c03a86f79447f78391cf884d7a2b88

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
- Codex exec の単一試行ループと再試行制御の入口。Structured Output 検証、capacity 再試行、quota 待機と代表 probe、resume token の継続、call log と subcommand event の記録をまとめて扱うため、この実行制御の流れを追うときに読む。
- TUI 起動や別サブコマンドの責務ではなく、Codex 呼び出しの argv/env/cwd/schema の組み立て、実行結果の判定、変更 worktree path の列挙だけを確認したいときに進む。

## Read this when
- Codex exec の失敗時挙動、再試行条件、quota 待機の継続条件、Structured Output の検証条件を確認したいとき。
- call log、prompt log、stdout/stderr、output の保存内容や、subcommand logger へ何を記録するかを追いたいとき。
- resume token の復元や quota 代表 probe の扱いを含む、実行制御の状態遷移を理解したいとき。
- worktree 上の変更 path を絶対 path で列挙する処理の入口を探しているとき。

## Do not read this when
- Codex exec 以外のサブコマンドの入出力変換や TUI 起動を見たいときは、より直接のモジュールを読む。
- 実行ログの保存先や runtime path の定義そのものを確認したいだけなら、関連する paths や logging 側の定義を先に読む。
- Codex CLI の内部実装全体を追う必要はなく、単に `codex exec` 呼び出しの結果だけ知りたい場合は、このファイルの周辺ロジックだけで足りる。

## hash
- 0e6bdc6c3cea02554413e903fcfc1cb4ff8b46d9a7f03487e62a197a1f20625c

# `runtime_codex_logging.py`

## Summary
- Codex CLI 呼び出しに関する console 出力と、起動失敗時の error 文面を共通化する補助をまとめた対象。呼び出し通知の表示形式を確認したいときや、失敗理由の整形を他の出力経路と揃えたいときの入口になる。
- console に出す時刻・経過時間・終了コードの組み立てを見たい場合と、`CmocError` を含む例外を利用者向けの短い error text に直したい場合に読む。

## Read this when
- Codex CLI 呼び出しの通知を console に出す処理を追加・修正したい。
- 起動失敗や例外の文面を、console 出力と event で同じ表現に揃えたい。
- 経過時間や時刻表示を含む呼び出しログの見え方を確認したい。

## Do not read this when
- 呼び出しの記録先そのものや永続化の責務を変えたいときは、保存・記録側の対象を先に読む。
- Codex 以外の CLI 表示や一般的な runtime エラー処理を変えたいだけなら、より上位の入出力処理を読む。
- `console_timestamp` や `format_duration` の表示仕様だけを追いたいときは、それらを定義している対象を直接読む。

## hash
- 3aa2c9b4388542920c4557bddf5901e75f441a15c053f019c7c9b9f20c90267d

# `runtime_codex_preflight.py`

## Summary
- Codex exec/TUI 実行の直前に登録済みの INDEX 更新 preflight を挟むための薄い委譲層。preflight の登録・解除、実行起点 root の決定、再入抑止と直列化を扱い、実際の Codex 実行は runtime 側へ渡す。

## Read this when
- Codex exec/TUI 呼び出し前に indexing preflight が実行される条件や順序を確認したいとき。
- run_indexing_preflight、cwd、root、parameter.cwd から preflight の起点 root がどう決まるかを調べたいとき。
- indexing preflight の登録解除、再入防止、ロックによる直列実行の挙動を変更したいとき。

## Do not read this when
- Codex exec/TUI の実行本体、サブプロセス実行、戻り値の組み立てを調べたいときは runtime 実行側を読む。
- repo root や work root の判定規則そのものを調べたいときは path 解決を担う runtime path 側を読む。
- AgentCallParameter の項目定義や run_indexing_preflight の意味を確認したいときは basic 側の parameter 定義を読む。

## hash
- 21640496726fe5b154993e3215648edd155e6984b8fcb368ada7a22845c04670

# `runtime_codex_profile.py`

## Summary
- Codex CLI を起動する前後の境界処理をまとめる実装で、`argv` と permission profile、`CODEX_HOME`、schema 配置、子プロセス追跡、JSONL error 判定を一貫して扱う。Codex subprocess に渡す実行条件と、その戻り値を機械的に解釈する責務の中心である。
- 権限・read/write 境界を組み立てる部分と、Codex 出力の異常判定を行う部分が同居しているため、起動条件の変更、ファイルアクセス制御の調整、quota/capacity/error 判定の修正をするときに読む。
- 同じ subprocess 境界の不変条件を共有するため、呼び出し側が起動条件と失敗時挙動をまとめて理解したい場合の入口になる。

## Read this when
- Codex CLI の起動引数、sandbox/permission profile、`CODEX_HOME`、schema 配置、または child process tracking の扱いを変えたいとき。
- Codex から返る JSONL を見て capacity/quota/unexpected error をどう判定するか、あるいは resume token をどう抽出するかを確認したいとき。
- read/write 許可境界や oracle/realization の保護ルールを、Codex subprocess 側の起動条件として見直したいとき。

## Do not read this when
- Codex の一般的なコマンド実装や UI だけを確認したいときは、より上位のサブコマンド実装を先に読む。
- file access policy の正本定義そのものを確認したいだけなら、対応する oracle 側の仕様断片を読むべきで、このファイルは実装化の境界を見るためのものに留める。
- JSONL のプロトコルやエラー文言の仕様全体を確認したいだけなら、Codex 実行ルールや該当する oracle doc を先に読む。

## hash
- ab16fbf60aaaf0ad819ad6878f7249a43b64c472c899b2a540121d526c2c9427

# `runtime_codex_tui.py`

## Summary
- Codex TUI を起動する共通処理で、`AgentCallParameter` から呼び出し argv・`CODEX_HOME`・call log・サブコマンドログをまとめて準備し、実行結果を `CommandResult` か例外で返す。
- Codex の起動前後で記録内容や失敗時の扱いを揃えたいときに読む。特に、起動先の cwd 決定、`CODEX_HOME` の解決と検証、呼び出しログ出力、失敗イベント記録の責務を確認するときの入口になる。

## Read this when
- Codex TUI の起動方法や、起動時に残す call log とサブコマンドログの内容を変えたい。
- `CODEX_HOME` の解決・検証や、Codex 呼び出し前の argv 組み立てを見直したい。
- Codex 実行失敗時の例外変換や、起動失敗をイベントとして記録する経路を確認したい。

## Do not read this when
- Codex 以外の実行経路や、別サブコマンドの引数組み立てだけを見たい。
- 単に `CommandResult` の定義や一般的な設定読み込み処理だけを確認したい。
- call log の保存先だけを知りたい場合は、直接 `runtime_paths` 側を読む方が近い。

## hash
- 56354704e19d5e51bc279f550754fc1a964cd8fe3e3a1d66fa012c93f2a9af97

# `runtime_config.py`

## Summary
- cmoc の設定を正本 config 型と永続化 JSON の間で変換し、設定ファイルの読み込み、検証、既定値補完、書き戻しを担う。
- 利用者が編集する config JSON の型不正や構文不正を、利用者向けの CmocError 境界へ変換する。

## Read this when
- 設定ファイルの保存形式、既定値補完、読み込み時の検証、または sync 時の生成・正規化挙動を確認・変更したいとき。
- config の enum key map、Codex model spec、int 値、optional section の JSON 復元ルールを調べたいとき。
- 設定ファイル不在、JSON 構文不正、top-level 不正、値型不正に対する利用者向けエラーを確認したいとき。

## Do not read this when
- config 型そのものの項目定義や既定値を確認したいだけなら、config 定義側を読む。
- Codex model 名や reasoning effort 名の正本定義を確認したいだけなら、oracle 側の model config 定義を読む。
- 設定ファイルのパス解決だけを確認したいなら、runtime path 側を読む。

## hash
- 1120d55ea7a5a55ce14b73f76f472319f67fe3da04ee9717c70ebf73e14deeda

# `runtime_content.py`

## Summary
- ファイル内容または文字列内容から SHA-256 digest を計算し、digest をファイル名に含めた内容アドレス型ファイルを書き出す小さな runtime content helper 群。
- 出力先 directory の作成有無が異なる 2 種類の書き出し関数と、先頭 chunk の NUL byte と読み取り可否による簡易 binary 判定を扱う。

## Read this when
- 内容 hash を使った成果物ファイル名の生成、重複書き込み回避、または内容アドレス型の一時・補助ファイル保存を確認・変更するとき。
- ファイル内容や文字列内容の SHA-256 digest 計算処理を使う箇所を探すとき。
- テキスト対象と binary 対象を粗く分けるための簡易判定ロジックを確認・変更するとき。

## Do not read this when
- path model、run/work/root の意味、またはパス表記そのものの仕様を確認したいとき。
- CLI 引数、サブコマンド、標準出力、終了コードなど利用者向けの公開面を確認したいとき。
- hash 値を使わない通常のファイル読み書き、設定読み込み、永続状態管理の実装を探しているとき。

## hash
- d121b59cd941f68e101d0bf9b1eb0f0fdd2fe8c928d89dd6447b3079581fb905

# `runtime_doctor.py`

## Summary
- doctor 用の Git ロック、修復用一時 index、`.gitignore` 修復、`.agents/.gitkeep` の補完、修復コミット生成をまとめて扱う。doctor 実行時に共有 index を壊さず差分だけを反映したいときに読む。
- Git common directory 単位の排他と、一時 index へ HEAD や現在の index から修復を合成して戻す流れを担う。並行 doctor の競合回避や、linked worktree でも同じ修復をそろえたいときに読む。
- `.cmoc/local` を git 追跡外にする修復と、`.agents` を tracked に保つための placeholder 追加を含む。ignore 追加や placeholder の扱いを変えるときに読む。

## Read this when
- doctor 実行前後の Git state 復元や修復 commit の作り方を確認したい。
- `.gitignore` の cmoc 例外追加や `.agents/.gitkeep` の扱いを変えたい。
- linked worktree を含む並行実行時の排他や、一時 index を使った修復合成の責務を確認したい。

## Do not read this when
- doctor に関係しない通常の Git 操作や、他の runtime 補助処理を追いたい。
- 修復対象の具体的なコマンドや UI 挙動だけを見たい場合は、doctor_preprocess の上位呼び出し側を先に読む。
- ignore パターンや placeholder 方針そのものの正本仕様を探している場合は、対応する oracle 側を読む。

## hash
- f50f885e8ffc648f1b5c5fe95ac4122301ef4397800b010e148de20e73e6d8b9

# `runtime_errors.py`

## Summary
- cmoc の実行時例外と、任意の例外を利用者向け Markdown エラーレポートへ変換する共通処理を定義する。エラー概要、復旧案、詳細、呼び出しスタックを一貫した形式で出力するための入口となる。

## Read this when
- 利用者に表示する cmoc 共通エラーレポートの構成や文面を確認・変更したいとき。
- 実装内で発生させる利用者向け例外に、概要・復旧案・詳細を持たせる方法を確認したいとき。
- 例外ごとの復旧案が少ない場合に既定の Next actions がどう補われるかを確認したいとき。

## Do not read this when
- 個別コマンド固有のエラー判定条件や入力検証ロジックを調べたいとき。
- エラーレポートを出力する CLI エントリーポイント側の制御を調べたいとき。
- Markdown エラーレポート以外の通常出力や成功時出力の形式を調べたいとき。

## hash
- 51eb58dfc241cb76b6debfce4a06a3169cb6a2a29d0a6f123f7c5b6c0bd03e95

# `runtime_git.py`

## Summary
- `src/commons/runtime_git.py` は、cmoc が Git へ依存する基盤処理をまとめた境界です。branch/HEAD/worktree の判定、`.cmoc/local` の ignore 管理、Git 由来のエラー整形、oracle/realization 判定に使う path 判定を扱います。
- この対象を読むのは、Git コマンド実行の失敗扱い、managed branch や managed worktree の判定、`.cmoc/local` の ignore 保障、oracle file の判定ルールを変更・確認したいときです。
- この対象だけでは、各サブコマンドの振る舞い本体や UI は分かりません。Git 基盤の利用箇所を追う必要があるときに読む入口です。

## Read this when
- Git subprocess の例外整形や `CmocError` への変換を変えたいとき.
- current branch / HEAD commit / clean worktree / managed branch の判定条件を確認したいとき.
- `.cmoc/local` を ignore する条件や、tracked かつ ignore 対象の扱いを確認したいとき.
- oracle file 判定や managed worktree の削除条件など、path ベースの安全判定を確認したいとき.

## Do not read this when
- 各 CLI コマンドの入出力や実行フローそのものを知りたいだけのとき.
- Git 以外の状態管理や session / branch の上位制御を見たいとき.
- 単なる UI 文言や report 生成の詳細を追いたいとき.

## hash
- a407f29b7d0fb422e34396a9759e1cfb22f37c69d0b63fe904bd0cf75bf93ca9

# `runtime_logging.py`

## Summary
- サブコマンドごとの JSON Lines ログと経過時間をまとめる共有 logger を定義する。`ContextVar` で現在の logger を深い runtime helper から参照できるようにし、step timing と quota 待機時間も保持する。
- コンソール出力やファイル出力の連携で、イベント記録の単位、step 開始・終了の扱い、現在 logger の受け渡し方法を変えるときの入口になる。

## Read this when
- サブコマンド実行中に残すイベント記録の追加・変更をするとき。
- step の開始時刻、経過時間、quota 待機時間など、サブコマンド全体の実測値の集計方法を変えるとき。
- 深い runtime helper から現在のサブコマンド logger を参照・差し替え・復元する流れを確認したいとき。

## Do not read this when
- 個別サブコマンドの実処理や引数処理だけを変えるときで、共有 logger の記録方式に触れない場合。
- Codex CLI 呼び出しの詳細な記録形式だけを扱いたい場合は、`runtime_codex_logging.py` を先に読む。
- タイムスタンプ付き path の予約やログ保存先の決定だけを確認したい場合は、`runtime_paths.py` を先に読む。

## hash
- f4eb36e9d2b4bb2881b61820de8725a8b750ddb8c0118b57ba999d1bf7d9e241

# `runtime_ollama.py`

## Summary
- cmoc が管理する Ollama の導入、systemd user service の同期、`127.0.0.1:11434` での提供確認、モデルの取得・load・GPU 推論確認を一連で担う単一 preflight の入口。
- config から cmoc provider の model 名を集め、重複排除したうえで必要な model だけを対象にする。
- 実処理は install/service/procfs/HTTP/model 検証に分かれるが、外部からは `ensure_ollama_serves_local_slm` を起点に読むべき対象。

## Read this when
- cmoc provider の local SLM を Ollama で serve 可能にする流れを追いたいとき。
- Ollama の archive install、user service 設定、`/proc` による listener と MainPID の突合、`/api/generate` による load、`/api/ps` による GPU 使用確認の境界を確認したいとき。
- どの model を対象にするかの決定と、失敗時にどの段階で止まるかを知りたいとき。

## Do not read this when
- Ollama の provider 選択や model 仕様そのものを確認したいときは、config 側や app_spec 側を先に読む。
- systemd や procfs、HTTP クライアントの一般的な使い方だけを知りたいときは、この対象よりも各責務の実装や標準ライブラリ側を読む。
- 単独の helper 再利用先を探しているだけなら、まずはこのファイルの外で同責務の入口がないかを確認する。

## hash
- 7a29c53f3a4a68e3b958bdfda14d9390cf26f6c1e9dee953e868d8c88ecc32eb

# `runtime_paths.py`

## Summary
- 実行時に `<repo-root>` / `<work-root>` を解決し、失敗時は `CmocError` に変換する root 解決ユーティリティをまとめる。cwd 指定時の解決補助、`pushd` を使った一時的な cwd 切替、`cmoc-root` 解決もここで扱う。
- 時刻文字列の生成と、セッション・レポート・ログ・worktree・schema・config の保存先パス決定を扱う。`memo` 配下判定のような、保存先やルート判定に関わる周辺ロジックも含む。

## Read this when
- root placeholder から実パスを解決する処理や、その失敗をユーザー向けエラーに変換する挙動を変えるとき。
- 実行時刻表記、ファイル名向けの timestamp、または `.cmoc/local` 配下の各種保存先ルールを変えるとき。
- cwd を一時的に切り替えて外部 API の前提に合わせる必要がある処理を確認するとき。

## Do not read this when
- 個別サブコマンドの業務ロジックや、セッション・ログ・レポートの中身を扱う実装を追うとき。
- `INDEX.md` のルーティングや他モジュールの責務境界だけを確認したいとき。
- path 解決や保存先決定と無関係な CLI 解析、出力整形、状態遷移を見たいとき。

## hash
- 44eb6c915159efffe5354bd1bfa12c771b7f1e9dc6d838f6860733fd18564cee

# `runtime_preprocess_command.py`

## Summary
- `cmoc` の前処理コマンド群をまとめて読むための入口。実行開始時のラッパーと、前処理本体の順序、設定同期後に差分をコミットする流れを追いたいときに読む。

## Read this when
- `cmoc` の前処理コマンドの実行順や、前処理・設定同期・設定コミットのつながりを確認したい。
- 設定を人間編集対象として扱いつつ、前処理で現在形へ戻す扱いを確認したい。
- 設定ファイルの差分を明示的に追跡対象へ戻して commit する判断を確認したい。

## Do not read this when
- 各前処理ステップの具体的な処理内容や失敗時の細部を追いたいときは、各ステップの実装へ直接進む。
- `cmoc` 以外のサブコマンドの手順を知りたいときは、そちらのコマンド実装を読む。
- 設定データの中身そのものを知りたいときは、設定定義側を読む。

## hash
- 96b19ba19c1d2faade9ee3c7903b53a6a8ff5e8883f65ffd6f7e342ef240c434

# `runtime_results.py`

## Summary
- 外部コマンド実行結果と Codex exec 実行結果を保持する不変 dataclass を定義する。
- コマンド終了コード、標準出力・標準エラー、生成物パス、Codex home、schema、実行時間、quota 待機情報など、runtime 実行後に他処理へ渡す結果コンテナを扱う。

## Read this when
- 外部コマンドや Codex exec の実行結果を受け渡す型のフィールドを確認・変更したいとき。
- call log、prompt log、stdout/stderr log、output、schema などの実行成果物パスを保持する結果オブジェクトを扱うコードを読むとき。
- quota 待機時間や poll 回数など、Codex exec 実行結果に付随する計測値の保持場所を確認したいとき。

## Do not read this when
- 実際に外部コマンドや Codex exec を起動する処理、ログファイルを書き出す処理、quota 待機制御の実装を探しているとき。
- CLI 引数、設定読み込み、argv 上書き生成、schema 生成など、実行結果コンテナへ渡される値の作成元を調べたいとき。
- runtime 結果型ではなく、ユーザー向け出力形式やテスト期待値の仕様を確認したいとき。

## hash
- c9bf5b582e21beadd3ab372c424bc794a332ddbfd657f47369776b0109590f13

# `runtime_state.py`

## Summary
- cmoc の session/apply 用 state file を読み書きする共通基盤。branch 名から session_id を取り出し、対応する JSON state を検証付きで読み込み、canonical JSON で書き戻す。
- active な home branch 対応 state の探索や、session fork の排他 lock もここで扱う。branch/state の整合性確認や state schema の修復が必要なときの入口。
- state の型検証、必須 field の欠落検出、不正 state への一貫したエラー生成をまとめている。上位の session/apply コマンド側で個別の state 仕様を読む前の基礎層。

## Read this when
- session state file の保存先・読み込み・書き戻し方を確認したいとき。
- cmoc session branch / cmoc apply branch から session_id を復元する規則を確認したいとき。
- active session の探索、fork 時の排他制御、state JSON の妥当性検証やエラーメッセージの方針を確認したいとき。

## Do not read this when
- session/apply の高レベルなコマンド手順だけを知りたいときは、各 sub command 側の文書を先に読む。
- branch 命名や state schema の人間向け正本仕様を確認したいだけなら、ここではなく対応する oracle doc を読む。
- git 操作、worktree 操作、CLI 出力整形だけを見たい場合は、この共通 state モジュールではなくそれぞれの担当モジュールを読む。

## hash
- 88b98bb5b7d4d1932a1bfc8018b216a473b64515a37e1492daa87bf8c7e40be8
