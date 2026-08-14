# コンソール・ファイル、ログ出力規則

本書は、非対話サブコマンドの console、サブコマンドログ、および terminal result に関する共通契約の正本とする。console 出力について、個別サブコマンド仕様は、サブコマンド固有の `result`、`completion_reason`、primary report、次の操作、および終了コードだけを定義する。

## 共通規則

### 時間表示のフォーマット

- console に流す時間表示は、`{{month}} Mo {{day}} Day {{hour}} Hr {{minute}} Min {{sec}}.{{msec}} Sec` を最大構成とする
- `{{month}}`, `{{day}}`, `{{hour}}`, `{{minute}}`, `{{sec}}` は 2 桁・スペースパディング・右詰めとする
- `{{msec}}` は 1 桁・ゼロ表示・小数点第 2 位以降は切り捨てとする
- 値が 0 の上位単位は、`{{month}}` から順に、最初の 0 でない単位の直前まで省略する
- `{{sec}}.{{msec}} Sec` は常に表示する
- 例えば、経過時間が 10 時間の場合は `10 Hr  0 Min  0.0 Sec` と表示する

### パス表示のフォーマット

- ファイル・ディレクトリのパス文字列はフルパスで表現すること
- パスの前後は何らかの区切り文字 (e.g. ダブルクォート、半角スペース、改行、…) で囲うこと
- フォーマット的に元々囲われている場合 (e.g. JSON なら文字列はダブルクォートで囲われているはずである) は、元々の区切り文字にまかせて良い

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
- 進行通知の具体的な文面、記号、および形式は、本節の意味と出力先を守る範囲で realization の裁量とする

## terminal result

### 定義と分類

terminal result は、最外側の末端サブコマンドについて確定した終端結果を、人間へ最後に示す 1 つの console 出力単位である。

共通分類は、次の 3 種類とする。

- `natural_completion`: サブコマンド固有の正常な処理結果を確定して自然完了した
- `user_interruption`: ユーザー中断要求に従い、個別仕様が認める確定済みの部分結果で正常に完了した
- `error`: エラー終了した

共通分類、サブコマンド固有の `result` または `completion_reason`、および終了コードは、それぞれ独立した意味とする。終了コードだけから、共通分類、サブコマンド固有結果、またはスタックトレースの要否を決めてはならない。

### 確定と表示の順序

terminal result は、次の処理をすべて完了した後に表示する。

1. state、report、および成果物を確定する
2. 並列処理、非同期処理、および console へ出力し得る通知処理を停止または drain する
3. terminal result を含むサブコマンド終了イベントをサブコマンドログへ書き込み、flush する

terminal result の表示後は、同じサブコマンドの stdout または stderr へ追加出力してはならない。

### 表示内容

terminal result は、該当する情報を次の優先順序で表示する。

1. 完了、中断完了、または失敗の別と、サブコマンド名
2. primary report が存在する場合は、その役割とフルパス
3. サブコマンド固有の `result` または `completion_reason` が存在する場合は、その値
4. 次に必要な操作がある場合は、その操作
5. warning の要約と、repository-local な pending feedback observation 数
6. サブコマンド全体の経過時間と終了コード
7. 診断用サブコマンドログのフルパス

primary report は、そのサブコマンド結果について人間が読むべき report とする。primary report のフルパスは terminal result の見出し直後に表示し、同じパスを console の別の箇所へ重複表示してはならない。

report 本文、candidate、および finding の詳細を console へ複製してはならない。primary report が作成されなかった結果では、存在しない report path を表示してはならない。

pending feedback observation の件数と warning は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` の通知境界に従う。

Windows toast の対象、発火順序、通知内容、および失敗時の扱いは、`{{cmoc-root}}/oracle/doc/app_spec/windows_toast_notification.md` を正本とする。

## サブコマンドログファイル

### 基本要件

- ログファイルはサブコマンドと 1:1 で存在すること
- ログファイルは JSON Lines 形式であること
- ログファイルは `{{repo-root}}/.cmoc/gu/ar/log/sub_command/{{time-stamp}}.jsonl` に出力すること
- ログファイルは `{{run-root}}` 側に出力してはいけない
- サブコマンド中に発生したイベント 1 つ = ログファイルの 1 行とすること
- イベントの追記はバッファリングせずに即時 flush すること

### 診断記録

サブコマンドログは、サブコマンド呼び出しから terminal result までを追跡できる完全な診断記録とする。少なくとも次の情報を記録する。

- サブコマンド呼び出し
- 階層化されたサブステップを含む全ステップと、その時間
- 全 Codex call と、対応する Codex call ログ、経過時間、および戻り値
- warning
- handled failure と internal failure の判別に必要なエラー詳細
- terminal result を含むサブコマンド終了イベント
- サブコマンド全体の経過時間、Codex CLI quota 回復待ち時間、および終了コード

過去のサブコマンド実行で起きたことを追跡するための具体的な field は、realization の裁量で定めてよい。例外として、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` の detector rule が参照する event は、同仕様が定める `event_schema_version`, `event_id`, `event_type`, context、および rule 固有 field を安定した契約として含める。

feedback detector は、安定契約として定義されていない自由文 field を判定に使用してはならない。

## TUI と自動補完の境界

- `cmoc tui`、`cmoc oracle edit`、および `cmoc oracle investigation` の正常な TUI 終了後には、非対話サブコマンド用の terminal result を追加表示しない
- TUI の起動前エラーまたは異常終了には、本書と `{{cmoc-root}}/oracle/doc/app_spec/error_handling.md` のエラー表示規則を適用する
- TUI process へ制御を渡した後は、cmoc の進行通知を TUI の表示へ混入させない
- 自動補完プローブでは、CLI ライブラリの補完処理が必要とする出力以外を stdout または stderr へ混ぜない
- 自動補完プローブでは、通常のサブコマンドログ初期化、terminal result、および cmoc 形式のエラー表示を行わない

自動補完プローブの判定と処理境界は、`{{cmoc-root}}/oracle/doc/app_spec/cli_auto_completion.md` を正本とする。

## non-goal

本書は、次の機能を要求しない。

- ANSI color に依存する表示
- TTY と non-TTY で意味が変わる動的表示
- verbosity option または debug option
- 機械可読な stdout 用の新しい JSON schema
- report 本文の内容または判定基準の変更
- Windows toast 通知内容の拡張
- feedback detector が使用する安定した構造化 event 契約の変更
