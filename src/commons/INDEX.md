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
- `commons` 配下の runtime 群を束ねる統合入口。Codex 実行・TUI 起動、設定と状態の読み書き、Git/作業ツリー操作、ログ・パス・出力処理をまたいで扱うときにここを起点に読む。
- 各低レベル helper の詳細ではなく、`cmoc` 全体の実行フローやサブコマンド横断の共通処理を追いたい場合に使う。個別の設定変換、Git 操作、状態管理だけを知りたいなら、それぞれの専用モジュールを直接読む。

## Read this when
- Codex 実行や TUI 起動の前後で、設定・状態・Git・ログをどう連携させるかを確認したいとき。
- 作業ディレクトリや worktree、branch、session、schema store などの共通パスや永続状態の扱いを横断的に把握したいとき。
- サブコマンド実行の周辺で、エラー整形や subprocess 実行、ハッシュ付き出力、実行結果の共通表現をまとめて追いたいとき。

## Do not read this when
- 特定の責務だけを調べたいときは、設定なら `runtime_config`、Git なら `runtime_git`、状態なら `runtime_state`、パスなら `runtime_paths` を直接読む。
- サブコマンド固有の振る舞いだけを確認したいときは、ここではなく各サブコマンド実装を読む。
- 個々の low-level helper の実装差だけを追う目的では、まずこの統合入口を読む必要はない。

## hash
- 612c735076091aea4798f3103ca3c336d1c4eb55da60bd7e3e0627a360ec7021

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
- apply 実行の pid / process group / worktree を扱い、`cmoc apply abandon` で安全に停止対象を特定・記録・削除するための基盤です。親 apply process と Codex child group の同一性確認、追跡用環境変数の切替、stale 判定、停止順序の制御をまとめて扱います。
- apply の停止や追跡に関する挙動を変更する時に読む対象です。特に、pid file の形式、child group の保存・読取、親終了後の再読取、worktree 復元、停止不能時のエラー条件を確認したい場合に進みます。
- apply abandon 以外のサブコマンド仕様、一般的な process 管理、表示文言の調整だけが目的なら、ここは優先対象ではありません。worktree 計算や process tracking を直接変更しない作業では、より上位の呼び出し元や CLI 側を先に読む方が適切です。

## Read this when
- `cmoc apply abandon` の停止対象判定、pid file 生成・読取・削除、child process group の追跡方式を変える必要があるとき。
- apply 実行中だけ Codex child を追跡する仕組みや、親 apply process 終了後に tracking を再読込する必要があるとき。
- branch から linked worktree を復元する処理や、`cmoc/apply/...` 形式の managed worktree path の解釈を確認したいとき。
- 停止対象が stale かどうか、同一 process かどうか、既に終了済みかどうかの判定条件を確認したいとき。

## Do not read this when
- apply 以外のサブコマンドの実装や CLI 引数の整理だけをしたいとき。
- process の一般論や OS レベルのシグナル仕様だけを確認したいとき。
- このモジュールを直接触らず、停止処理を呼ぶ上位コマンドの入出力やユーザー向けメッセージだけを変えたいとき。
- worktree 名や session state の保存形式を変えず、単なる呼び出し順や小さなリファクタだけを行うとき。

## hash
- 92dc35ad5fb186ce11086512e70eaac38531713aec7a930298e21c334f7cd765

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
- Codex exec の実行制御を担当する。Structured Output 検証、capacity retry、quota 待機と代表 probe、resume 継続、実行ログ生成、失敗時の要約を 1 つの状態機械としてまとめる。
- TUI 起動や別サブコマンドのルーティングではなく、`codex exec` 呼び出しそのものの組み立てと再試行条件を読むときに参照する。
- 変更中の worktree について、更新された path を git status から拾う補助関数もここにある。

## Read this when
- `codex exec` の呼び出し方、再試行条件、Structured Output の検証失敗時の扱い、quota 待機中の挙動、call log / stdout / stderr / output の記録方法を確認したいとき。
- resume token の引き継ぎ、quota 代表 probe の開始・終了条件、capacity retry と quota polling の関係を確認したいとき。
- worktree の変更 path を absolute path で列挙する補助が必要なとき。

## Do not read this when
- TUI の起動経路や画面制御を追いたいときは、別 module を読むべきでここは読まない。
- サブコマンド全体の入口や CLI ルーティングを見たいだけなら、より上位の実行層を読むべきでここは読まない。
- git status の一般的な取得方法だけを知りたい場合は、この実行制御モジュールではなく git 操作の共通部を読むべきでここは読まない。

## hash
- 692027dd1c8a22888c06fc10447f3ffca97119670145ec4ed6badeb2fa489633

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
- Codex CLI を起動する前後の環境組み立てと、返ってきた実行結果を正規化・判定する境界を扱う。argv の上書き、sandbox/permission profile、CODEX_HOME、schema 配置、追跡用 pid file、JSONL エラー判定をまとめて確認したいときに読む。
- 呼び出し側が Codex 実行の権限制御や失敗時挙動を変える必要がある場合に読む。個別のサブコマンド実装や人間向け仕様文書ではなく、Codex subprocess の共通ルールを確認する入口として使う。

## Read this when
- Codex CLI に渡す `--sandbox` や permission profile、追加 read/write path の許可条件を確認したい。
- `CODEX_HOME` の解決・妥当性検査、または Codex subprocess に渡す環境変数の扱いを確認したい。
- apply 実行中の child process tracking、pidfd を使った停止、process group の終了待ちを確認したい。
- Structured Output schema の配置、実行結果 JSON の読み取り、JSONL stdout/stderr からの容量不足・quota・予期しない error 判定を確認したい。

## Do not read this when
- 単一のコマンド定義や UI からの入力変換だけを見たい場合は、そちらのサブコマンド実装を先に読む。
- Codex 実行前の一般的な設定値やドキュメントだけを確認したい場合は、実行境界ではなく対応する仕様文書を読む。
- ファイルアクセス方針そのものの正本を確認したい場合は、このファイルではなく `<work-root>/oracle/src/oracle/prompt_builder/parts/file_access_rule.py` の側を読む。

## hash
- 036629fcb2f8ddb5851ee6c9f0b8f8504b660cd46b04bdfd2f82477f2e04ec41

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
- Git の呼び出し境界と、その結果を cmoc の利用者向けエラー・判定値・worktree/branch 管理のための共通 helper に分けている。
- .cmoc/local の ignore 保証、managed branch/worktree の判定と作成・削除、tracked or ignored 判定、oracle/realization file 判定のように、Git 状態に依存する基盤ロジックをまとめて扱う。

## Read this when
- Git subprocess の失敗を cmoc の例外体系へそろえる経路を変えたいとき。
- managed branch の命名規則、linked worktree の作成・削除条件、symlink 経由の拒否条件を確認したいとき。
- .cmoc/local を ignore 対象に保つ条件や、tracked ファイルと ignore 判定の扱いを確認したいとき。
- oracle file / realization file の判定基準を変更したいとき。

## Do not read this when
- 具体的な CLI サブコマンドの入出力や引数仕様だけを追いたいときは、各 sub_commands 側を読む。
- worktree や branch の永続状態レイアウトそのものを知りたいだけなら、path model や branch model を読む。
- Git とは無関係な cmoc の設定値やプロンプト生成を見たいとき。

## hash
- 6e501bb2d7a7b4ff2793841cbf435faf5474e403bdd82f825f378be6ffc4685c

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
- cmoc 実行時の root 解決と、実行時刻・保存先・cwd 切替の共通基盤を持つ。`repo_root`/`work_root`/`cmoc_root` の解決方針、timestamp 生成、`pushd` の直列化、各種 local 保存先の決定が主な役割である。
- 上位のコマンド実行やログ保存、session/report/schema/working tree のパス組み立てがここに依存する。root 特定の失敗を runtime error に変換する契約も担う。

## Read this when
- root placeholder を絶対パスに解決する方法を確認したいとき
- `<repo-root>` / `<work-root>` / `<cmoc-root>` の失敗時エラーや cwd 起点の解決契約を確認したいとき
- cmoc が使う local 配置先や timestamp / duration 表示の共通ルールを確認したいとき
- cwd を一時的に切り替える処理の排他制御や復元条件を確認したいとき

## Do not read this when
- 特定サブコマンドの業務ロジックや入出力仕様を追いたいとき
- 個別の JSON 生成、CLI 引数、ログ本文形式の詳細を追いたいとき
- root 解決を使う側の実装ではなく、解決後のパス利用先を確認したいとき

## hash
- fe8c37e4a6e5c5e2c06413e2da70b1b136210eff258087e472adb3359fd75a3d

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
