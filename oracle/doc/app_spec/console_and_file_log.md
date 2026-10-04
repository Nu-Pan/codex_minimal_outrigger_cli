# コンソール・ファイル、ログ出力規則

本書は、最外側のサブコマンド実行の識別、および非対話サブコマンドの console、primary report、サブコマンドログ、terminal result に関する共通契約の正本とする。個別サブコマンド仕様は、サブコマンド固有の `result`、`completion_reason`、primary report の形式・保存先・追加項目・要約方法、次の操作、および終了コードを定義する。

## 共通規則

### 人間向け自然言語

- console、primary report、およびエラー説明の自然言語部分は、個別仕様に指定がない限り日本語とする。
- 識別子、path、command、JSON key、log 原文、および引用は元の表記を維持してよい。

### 実行 ID の開始表示

実行 ID `{{execution-id}}` は、ユーザーが起動した最外側の末端サブコマンドの invocation を識別する。console と保存記録を同じ値で対応付け、editor input のファイル名から対応するターミナル上の実行を直接照合できるようにする。書式と採番は、`{{cmoc-root}}/oracle/doc/app_spec/id.md` の「ID のフォーマット」「プレフィックス」「採番と順序保証」に従う。

- 最外側のサブコマンド開始処理で、doctor preprocess や editor input より前に一度確定し、終了まで維持する。この発行確定順を実行開始順とし、並行開始も同じ基準で順序を定める。
- 内部から呼び出すサブコマンド、処理関数、agent call、Codex call、retry、および回復待ちには、同じ実行 ID を引き継ぐ。
- 別の最外側のサブコマンド実行には別の値を割り当てる。同じ session や run を扱う場合も、複数ターミナルで並行実行する場合も重複させない。
- 同じ実行を表す console 表示、保存先の `{{execution-id}}`、および記録内の実行情報には同じ文字列を使う。

記録系の日時項目は維持し、実行 ID で置き換えない。

agent call、Codex call、session、run、および handoff target の識別子は、それぞれの識別対象を維持する。これらの識別情報を使う記録には、関連する実行 ID との対応を残し、実行 ID で各識別子を置き換えない。

cmoc は、人間向け console ログの最初の出力として、確定した実行 ID を stderr に表示する。TUI と自動補完への適用は、本書の「TUI と自動補完の境界」に従う。

### 時間表示のフォーマット

- console に流す時間表示は、`{{month}} Mo {{day}} Day {{hour}} Hr {{minute}} Min {{sec}}.{{msec}} Sec` を最大構成とする
- `{{month}}`, `{{day}}`, `{{hour}}`, `{{minute}}`, `{{sec}}` は 2 桁・スペースパディング・右詰めとする
- `{{msec}}` は小数点以下 1 桁を表し、値が 0 の場合も表示する。小数点第 2 位以降は切り捨てる
- 値が 0 の上位単位は、`{{month}}` から順に、最初の 0 でない単位の直前まで省略する
- `{{sec}}.{{msec}} Sec` は常に表示する
- 例えば、経過時間が 10 時間の場合は `10 Hr  0 Min  0.0 Sec` と表示する

### パス表示のフォーマット

- ファイル・ディレクトリのパス文字列はフルパスで表現すること
- パスの前後は区切り文字で囲むこと（例：ダブルクォート、半角スペース、改行）
- 出力形式の区切り文字ですでに囲まれている場合は、その区切り文字を使ってよい（例：JSON の文字列を囲むダブルクォート）

## 非対話サブコマンドの console 出力

### 出力先の責務

- stdout は、`natural_completion` または `user_interruption` の terminal result だけを表示する
- stderr は、簡潔な進行通知、warning、および `error` の terminal result を表示する
- terminal result は、ユーザーが起動した最外側の末端サブコマンドについて 1 回だけ表示する
- cmoc 内部から呼び出したサブコマンド、処理関数、agent call、および Codex call は、独立した terminal result を表示しない

### 進行通知

- 進行通知は、cmoc が稼働中であることと、現在のトップレベルステップを人間が確認できる短い表示とする
- 階層化された全サブステップを console へ列挙してはならない
- サブステップ別の経過時間、個別 Codex call のログパス、および個別 Codex call の戻り値を、通常の進行通知へ列挙してはならない
- Codex CLI の回復待ちでは、現在の待機理由、待機の継続、次回確認の目安、理由変更、復旧後の再開、および待機終了の理由を簡潔に示す。待機・再開の判断は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「回復待ちと再開」を正本とする
- 個別 probe の呼び出し情報や結果は、本書の「診断記録」に残す。probe ごとの詳細を進行通知へ列挙せず、probe の成功をサブコマンドの完了として表示しない

## primary report

primary report は、その invocation で確定した作業内容と終端結果を人間向けに要約する。ユーザーが起動した最外側の非対話末端サブコマンドは、terminal result を確定する前に primary report を 1 件保存する。

ただし、feedback の publication または cleanup の再開で引き継ぐ正常 report と `incomplete` 診断 report の保存確認、掲載対象、および実行情報の帰属は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の「再開時の report と実行記録」に従う。

- `natural_completion`、`user_interruption`、および `error` のすべてを primary report の対象とする。個別サブコマンドで成立しない終端分類の report は要求しない。
- primary report 作成専用の追加 agent call は、個別仕様が report 生成手順として明示する場合に限る。
- cmoc 内部から呼び出したサブコマンド、処理関数、agent call、および Codex call は、独立した primary report を保存しない。

primary report の保存に失敗し、完了契約を確定できない場合は、`{{cmoc-root}}/oracle/doc/app_spec/error_handling.md` の「エラー終了の確定」に従って internal failure とする。この場合は、保存済みでない primary report の path を terminal result に表示しない。

### 完了時のエディタ表示

サブコマンド完了時に人間が結果を読めるよう、本書が primary report の対象とするすべての終了経路で、保存済みの primary report をエディタで自動的に 1 回開く。保存を確認できない report は開かない。

- エディタの選択は、`{{cmoc-root}}/oracle/doc/app_spec/prompt_editor_input.md` の「エディタの選択」に従う。
- 表示が目的であるため、エディタの終了やユーザーによるファイルのクローズを待たずに cmoc を終了する。`code` には `--wait` を付けない。
- cmoc の終了後も report を閲覧できるように起動する。エディタの表示や診断出力を cmoc の stdout または stderr へ混入させない。これらを満たす具体的な起動方法は実装に委ねる。
- エディタの選択または起動に失敗しても、サブコマンドの終端結果、終了コード、および成果物は変更しない。失敗は warning として、本書の「出力先の責務」「確定と表示の順序」「診断記録」に従って知らせる。

### 共通掲載内容

primary report には、内部処理を含むその invocation の実行記録として、次の内容を一覧で掲載する。

- 本書の「実行 ID の開始表示」で定める実行 ID と、対応する診断用サブコマンドログへの参照。
- 各 `codex exec`（`codex exec resume` による再開・補正を含む）で取得できた最終出力の本文と、元の出力ファイルへの参照。取得・保存先は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の `--output-last-message` を正本とする。
- 実行中に新規受理された feedback observation の問題内容。掲載対象は、`{{cmoc-root}}/oracle/doc/app_spec/feedback.md` の「用語と結果分類」における observation とする。

共通掲載対象の本文を、省略・要約または原本への参照だけで置き換えてはならない。

#### Structured Output の表示

共通掲載対象の各呼び出しで取得した Structured Output には、本書が primary report の対象とするすべての終了経路で、次の表示要件を適用する。表示加工は cmoc の primary report 生成が担い、report 内の表現だけを対象とする。agent 向け指示や schema に表示責務を追加せず、この加工のための追加 agent call は行わない。

JSON として解析できる場合は、次を満たす表示にする。

- オブジェクト・配列の階層とキー・値の対応を読み取れる整形表示にする。キー、値、型の区別、および配列順序を保持し、空文字列・`null`・空配列などを識別できるようにする。
- 文字列は、JSON の解釈に必要なデコードを一度だけ行い、Unicode エスケープは対応する文字として、文字列内の改行は実際の改行として読めるようにする。デコード後の文字列に含まれるリテラルのバックスラッシュと `n` の並びや JSON 風の文章を、追加でデコード・再解析してはならない。
- 引用符やバックスラッシュを含む文字列も、本文と表示上の区切りを取り違えない形で示す。

具体的なレイアウト、インデント幅、見出しの形は、上記の可読性と忠実性を満たす範囲で実装裁量とする。表示結果自体の JSON 構文への準拠や、文字列内の Markdown の装飾表示は要求しない。

JSON として解析できない場合は、その旨と取得できた原文を実行記録へ掲載する。解析できても、schema または宣言済みの決定論的事後条件の検証に不合格だった出力は、不合格であり正式な結果ではないと判別できるように表示する。

Structured Output の受理条件と不合格出力の保持は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「Structured Output > 機械的検証と正式な結果」を正本とする。表示できることを受理条件に加えたり、表示変換で出力補正や結果の受理を代替したりしてはならない。

## terminal result

### 定義と分類

terminal result は、最外側の末端サブコマンドについて確定した終端結果を、人間へ最後に示す 1 つの console 出力単位である。

共通分類は、次の 3 種類とする。

- `natural_completion`: サブコマンド固有の正常な処理結果を確定して自然完了した
- `user_interruption`: ユーザー中断要求に従い、個別仕様が認める確定済みの部分結果で正常に完了した
- `error`: エラー終了した

共通分類、サブコマンド固有の `result` または `completion_reason`、および終了コードは、それぞれ独立した意味とする。終了コードだけから、共通分類、サブコマンド固有結果、またはスタックトレースの要否を決めてはならない。

### 確定と表示の順序

terminal result は、次の処理をすべて完了した後に確定して表示する。

1. state、成果物、および終端結果に必要な情報を確定する
2. 並列処理、非同期処理、回復待ち・probe・再開の処理、および console へ出力し得る通知処理を停止または drain する
3. 非対話サブコマンドでは、確定した作業内容と終端結果を primary report に保存する
4. 非対話サブコマンドでは、本書の「完了時のエディタ表示」に従って表示用エディタの起動を試みる
5. terminal result を含むサブコマンド終了イベントをサブコマンドログへ書き込み、flush する

terminal result の表示後は、同じサブコマンドの stdout または stderr へ追加出力してはならない。

### 表示内容

terminal result は、該当する情報を次の優先順序で表示する。

1. 完了、中断完了、または失敗の別と、サブコマンド名
2. 非対話サブコマンドでは、primary report の役割とフルパス
3. サブコマンド固有の `result` または `completion_reason` が存在する場合は、その値
4. 次に必要な操作がある場合は、その操作
5. warning の要約と、repository-local な pending feedback observation 数
6. サブコマンド全体の経過時間と終了コード
7. 診断用サブコマンドログのフルパス

primary report は、そのサブコマンド結果について人間が読むべき report とする。primary report のフルパスは terminal result の見出し直後に表示し、同じパスを console の別の箇所へ重複表示してはならない。保存済みであることを確認した path だけを表示する。

report 本文、candidate、および finding の詳細を console へ複製してはならない。

pending feedback observation の件数と warning は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` の「durability と retention」が定める通知境界に従う。

Windows toast の対象、発火順序、通知内容、および失敗時の扱いは、`{{cmoc-root}}/oracle/doc/app_spec/windows_toast_notification.md` の「Windows toast 通知」を正本とする。

## サブコマンドログファイル

### 基本要件

- ログファイルは、本書の「実行 ID の開始表示」で定める最外側のサブコマンド実行と 1:1 で対応させ、内部処理もそのログへ記録すること
- ログファイルは JSON Lines 形式であること
- ログファイルは `{{repo-root}}/.cmoc/gu/log/sub_command/{{execution-id}}.jsonl` に出力すること
- ログファイルは `{{run-root}}` 側に出力してはいけない
- サブコマンド中に発生したイベント 1 つを、ログファイルの 1 行に記録すること
- イベントの追記はバッファリングせずに即時 flush すること

### 診断記録

サブコマンドログは、サブコマンド呼び出しから terminal result までを追跡できる完全な診断記録とする。少なくとも次の情報を記録する。

- サブコマンド呼び出しと、その実行 ID
- 作成した editor input と primary report の保存先、および関連する agent call、Codex call、session、run の識別情報との対応。agent call の開始前や入力中の失敗も含め、作成済み記録の所属実行を追跡可能にする
- 階層化されたサブステップを含む全ステップと、その時間
- 全 Codex call と、対応する Codex call ログ、経過時間、および戻り値
- 回復待ちの開始・継続、理由とその変更、個別 probe の結果、復旧、再開と再発、および待機終了の理由。停止した呼び出しと probe・再開を対応付け、確認した呼び出し条件と結果の適用範囲を追跡可能にする
- warning
- handled failure と internal failure の判別に必要なエラー詳細
- terminal result を含むサブコマンド終了イベント
- サブコマンド全体の経過時間、Codex CLI の quota と一時障害それぞれの回復待ち時間、および終了コード。待機理由が変わった場合も、各理由で待った時間を追跡可能にする

過去のサブコマンド実行で起きたことを追跡するための具体的な field は、realization の裁量で定めてよい。例外として、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` の「rule registry」の detector rule が参照する event は、同仕様が定める `event_schema_version`, `event_id`, `event_type`, context、および rule 固有 field を安定した契約として含める。

feedback detector は、安定契約として定義されていない自由文 field を判定に使用してはならない。

### 索引同期の診断記録

索引同期と MCP 検索要求について、所要時間、処理量、結果、および打切り理由を調べられるようにする。通常起動・明示 doctor の同期と、TUI 利用中も含む MCP 検索要求・自動同期・再同期を対象とする。呼出し元の最外側のサブコマンドログへ、本書の「基本要件」に従って保存する。

記録から、実行 ID、サブコマンド、対象 work-root、索引 identity、および MCP 経路の Codex call・検索要求・各同期の対応を追えるようにする。並行要求や再同期を混同させない。接続側の context 供給と記録の搬送は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「文書検索 MCP」に従う。

検索要求と各同期について、次を記録する。

- 開始、終了処理を含む実測の総所要時間、結果。同期の更新あり・変更なし・失敗・取消・期限超過を区別し、親の検索要求やサブコマンドの結果と混同しない。
- 確認できた文書の処理状況と、embedding の新規計算・保存・再利用の処理量。
- 失敗・取消・期限超過の理由と、資源待ち・処理の停滞・停止と回収の状況。期限超過では適用した期限と判定時の実測値を残し、その後の終了処理と区別する。

開始と打切り理由は終端を待たずに記録する。途中で終了した場合も確認できた実績を残し、未確定値をゼロや成功で埋めない。終端を記録できない強制終了は、完了した結果と区別する。

期限・進捗・再利用・回収の意味と MCP stdout の境界は、`{{cmoc-root}}/oracle/doc/app_spec/document_search.md` の「同期と cache」「排他、期限、終了」「stdio MCP と失敗の公開」に従う。詳細な計測区間、件数の集計単位、イベント構成、相関方式は実装に委ねるが、測定対象・単位と途中値／確定値の区別が分かる記録にする。console の表示には本書の「進行通知」「TUI と自動補完の境界」を適用する。

### TUI 送信元情報の記録

editor input handoff を有効にする `cmoc tui` と `cmoc oracle investigation` では、TUI process を起動する前に、次の対応を既存のサブコマンドログへ記録し、flush を完了する。

- 本書の「実行 ID の開始表示」で定める実行 ID と、送信元のサブコマンド名
- 起動する TUI process の Codex call ID と、対応するログ保存先
- その実行の診断用サブコマンドログのフルパス

Codex call ID は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「基本」で定める識別子を使い、記録する送信元情報は同文書の「editor input handoff MCP」に従って MCP の呼び出し元コンテキストへ供給する実際の値と一致させる。送信元が実行中でも、この対応から既に保存された記録へ到達できるようにする。終了時にだけ保存される戻り値や最終結果を、対応の特定に必要としてはならない。

この記録は送信元の識別と保存済み記録への到達を保証する。TUI 会話全文や最終回答の保存・取得保証は追加しない。本文の受け渡しと tool result・log の境界は、`{{cmoc-root}}/oracle/doc/app_spec/editor_input_handoff.md` の「agent の責務と権限」と「tool result と log」に従う。

## TUI と自動補完の境界

TUI の通知境界を適用するサブコマンドと非対話サブコマンドの分類は、`{{cmoc-root}}/oracle/doc/app_spec/windows_toast_notification.md` の「目的と適用範囲」と「非対話サブコマンドの通知境界」を正本とする。本書の primary report 契約は、その分類を変更しない。

- `cmoc tui` および `cmoc oracle investigation` の正常な TUI 終了後には、非対話サブコマンド用の primary report または terminal result を追加しない
- `cmoc oracle edit` は非対話サブコマンドとして本書を適用する。内部の各 `codex exec` は独立した terminal result を表示せず、最外側のサブコマンドが終了状態の確定後に 1 回だけ表示する
- TUI の起動前エラーまたは異常終了には、本書と `{{cmoc-root}}/oracle/doc/app_spec/error_handling.md` の「エラーハンドリング規則」のエラー表示規則を適用する。非対話サブコマンド用の primary report は要求しない
- TUI process へ制御を渡した後は、cmoc の進行通知を TUI の表示へ混入させない
- 制御を渡した後も、文書検索 MCP の検索要求と自動同期は本書の「索引同期の診断記録」に従ってサブコマンドログへ記録する。この記録を TUI への進行通知の追加理由にしない
- TUI の起動前には実行 ID の開始表示を行い、サブコマンドログの記録規則を適用する。handoff を有効にする経路は、本書の「TUI 送信元情報の記録」も満たす
- 自動補完プローブの判定、console 出力、および通常処理の抑止は、`{{cmoc-root}}/oracle/doc/app_spec/cli_auto_completion.md` の「CLI 自動補完規則」を正本とする

## non-goal

本書は、次の機能を要求しない。

- ANSI color に依存する表示
- TTY と non-TTY で意味が変わる動的表示
- verbosity option または debug option
- 機械可読な stdout 用の新しい JSON schema
- 個別サブコマンド仕様が定める正常経路の report 本文の意味または判定基準の変更
- Windows toast 通知内容の拡張
- feedback detector が使用する安定した構造化 event 契約の変更
