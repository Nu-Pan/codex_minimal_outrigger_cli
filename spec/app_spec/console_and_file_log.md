# コンソール・ファイル、ログ出力規則

本書は、最外側のサブコマンド実行の識別とサブコマンドログ、TUI の実行記録、および非対話サブコマンドの console、primary report、terminal result に関する共通契約の正本とする。primary report の構成・配置・可読性と共通掲載内容は本書が所有する。個別サブコマンド仕様は、サブコマンド固有の `result`、`completion_reason`、report の固有項目と意味・生成方法・掲載時点・保存先・再開時の扱い、次の操作、および終了コードを定義する。

## 共通規則

### 人間向け自然言語

- console、primary report、およびエラー説明の自然言語部分は、個別仕様に指定がない限り日本語とする。
- 識別子、path、command、JSON key、log 原文、および引用は元の表記を維持してよい。

### 実行 ID の開始表示

実行 ID `{{execution-id}}` は、ユーザーが起動した最外側の末端サブコマンドの invocation を識別する。console と保存記録を同じ値で対応付け、editor input のファイル名から対応するターミナル上の実行を直接照合できるようにする。書式と採番は、`{{cmoc-root}}/spec/app_spec/id.md` の「ID のフォーマット」「プレフィックス」「採番と順序保証」に従う。

- 最外側のサブコマンド開始処理で、doctor preprocess や editor input より前に一度確定し、終了まで維持する。この発行確定順を実行開始順とし、並行開始も同じ基準で順序を定める。
- 内部から呼び出すサブコマンド、処理関数、agent call、Codex call、retry、および回復待ちには、同じ実行 ID を引き継ぐ。自動 join と post-join、TUI 起動用の初回 exec から TUI への自動移行も含め、実際の最外側のサブコマンド名を維持する。
- 別の最外側のサブコマンド実行には別の値を割り当てる。同じ session や run を扱う場合も、複数ターミナルで並行実行する場合も重複させない。
- `cmoc resume` も新しい最外側の実行として採番する。指定された再開元の実行 ID は対応情報として保持し、今回の実行 ID やログ保存先に再利用しない。
- 同じ実行を表す console 表示、保存先の `{{execution-id}}`、および記録内の実行情報には同じ文字列を使う。

記録系の日時項目は維持し、実行 ID で置き換えない。

公開 CLI の command 表記と agent call 種別は区別する。apply/refactor の command 表記は、`{{cmoc-root}}/spec/app_spec/sub_command/editing_run.md` の「公開コマンド名」に従い、builder 名や内部処理名で置き換えない。

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
- Codex CLI の回復待ちでは、現在の待機理由、待機の継続、次回確認の目安、理由変更、復旧後の再開、および待機終了の理由を簡潔に示す。待機・再開の判断は、`{{cmoc-root}}/spec/app_spec/codex_exec_rule.md` の「回復待ちと再開」を正本とする
- 個別 probe の呼び出し情報や結果は、本書の「診断記録」に残す。probe ごとの詳細を進行通知へ列挙せず、probe の成功をサブコマンドの完了として表示しない

realization refactor の巡回・確定成果・比較可能なテスト時間は、人間が停止を判断するための進捗として表示する。項目と未完了結果の扱いは、`{{cmoc-root}}/spec/app_spec/sub_command/realization_refactor.md` の「実行中の進捗」に従い、個別サブステップの経過時間とは区別する。

## primary report

primary report は、冒頭だけで、何を依頼した実行か、どこまで終わったか、注意すべき点、および次に必要な操作を人間が読み取れるものとする。その invocation で確定した作業内容と終端結果を要約し、根拠となる詳細結果と実行記録を続ける。ユーザーが起動した最外側の非対話末端サブコマンドは、terminal result を確定する前に primary report を 1 件保存する。

feedback の immutable な publication artifact の掲載時点は、`{{cmoc-root}}/spec/app_spec/sub_command/feedback_report.md` の「publication report と終了時の記録」に従う。`cmoc feedback report` は、同文書の「invocation report」に従い最外側の終了結果を primary report に載せる。再開した実行の帰属は同文書の「再開時の report と実行記録」に従う。`cmoc feedback close` が publication report を primary report として使う場合の保存確認・掲載時点・保存後の記録先は、`{{cmoc-root}}/spec/app_spec/sub_command/feedback_close.md` の「primary report と終了結果」を維持する。

- `natural_completion`、`user_interruption`、および `error` のすべてを primary report の対象とする。個別サブコマンドで成立しない終端分類の report は要求しない。
- primary report を新規生成する際は、本書の「重要事項確認用 call」に従う確認工程を必須とする。それ以外の report 作成専用 call は、個別仕様が生成手順として明示する場合に限る。
- cmoc 内部から呼び出したサブコマンド、処理関数、agent call、および Codex call は、独立した primary report を保存しない。

自動 join を含む workload は、join と post-join、state、cleanup、失敗段階、および次の操作を最外側の primary report に含める。項目と保存順序は、`{{cmoc-root}}/spec/app_spec/sub_command/editing_run.md` の「merge と post-join」「workload の report」に従う。内部 join 用に report、表示用エディタ、terminal result、または完了通知を重複させない。

primary report の保存に失敗し、完了契約を確定できない場合は、`{{cmoc-root}}/spec/app_spec/error_handling.md` の「エラー終了の確定」に従って internal failure とする。この場合は、保存済みでない primary report の path を terminal result に表示しない。

### 完了時のエディタ表示

サブコマンド完了時に人間が結果を読めるよう、本書が primary report の対象とするすべての終了経路で、保存済みの primary report をエディタで自動的に 1 回開く。保存を確認できない report は開かない。

- エディタの選択は、`{{cmoc-root}}/spec/app_spec/prompt_editor_input.md` の「エディタの選択」に従う。
- 表示が目的であるため、エディタの終了やユーザーによるファイルのクローズを待たずに cmoc を終了する。`code` には `--wait` を付けない。
- cmoc の終了後も report を閲覧できるように起動する。エディタの表示や診断出力を cmoc の stdout または stderr へ混入させない。これらを満たす具体的な起動方法は実装に委ねる。
- エディタの選択または起動に失敗しても、サブコマンドの終端結果、終了コード、および成果物は変更しない。失敗は warning として、本書の「出力先の責務」「確定と表示の順序」「診断記録」に従って知らせる。

### 共通掲載内容

primary report は Markdown とし、「人間向けタイトルと冒頭の要約 → 重要事項の確認結果 → 元の指示 → 詳細結果・実行記録 → 実行情報」の順序で構成する。

ファイル先頭に YAML Front Matter を置かない。実行情報を YAML で表す場合は、その章内のコードブロックにする。見出しの正確な名前、抜粋の長さ、および細かな装飾は、上記の読み順と以下の要件を満たす範囲で実装に委ねる。

cmoc が生成する Markdown 見出しの前後には、少なくとも 1 行の空行を設ける。ただし、ファイル先頭の見出しの直前は例外とする。引用する指示原文や Structured Output の文字列には、この整形のための空行挿入や書き換えを行わず、report 側の見出しと区切りで読みやすくする。

構成・機械的な要約・表示加工は cmoc の report 生成が担う。確認用 agent は重要事項を抽出し、agent 向け prompt や Structured Output schema に表示責務を追加しない。

#### 実行の識別と入力

冒頭にコマンド名、実行目的、および対象を示す。ユーザー指示や理由などの自由記述入力を受け取る実行では、その実行で使用するものとして確定した入力の短い抜粋を冒頭に載せ、全文を重要事項の確認結果に続く「元の指示」へ加工せず掲載する。長い指示全文によって冒頭の結果要約を押し下げない。

editor input の掲載元は、`{{cmoc-root}}/spec/app_spec/prompt_editor_input.md` の「ファイルの役割」「editor input の確定手順」で確定したオリジナルプロンプトとする。同節の再読禁止は report 作成時にも適用し、保存ファイルから指示を復元しない。report 用に別の入力の正本を設けない。

入力確定後なら agent call 開始前の失敗でもその入力を掲載し、未開始の処理を区別する。入力確定前に失敗した場合は、冒頭の要約と「元の指示」に「入力未確定」と示し、編集中の本文を確定済み指示として掲載しない。自由記述入力を受け取らないコマンドでは、「元の指示」にも操作目的と対象の commit 範囲・案件 ID など、実際に確定した対象情報を示す。対象を特定できなかった場合も未確定と分かるようにする。

#### 冒頭の要約

冒頭の要約には、次の内容を含める。

| 項目 | 示す内容 |
|---|---|
| 実行結果 | 完了・中断完了・失敗の別と、確定した処理の範囲。掲載時点で未確定の終端結果や、未開始・未実行・未完了の処理を区別する |
| 要注意事項 | 確認できたエラー、warning、未解決事項、および未確認事項。注意事項がないと示す場合も、確認できた範囲を越えて問題なしと断定しない |
| 次の操作 | 必要な確認・操作。必要な操作がなければ、その旨 |

実行の成否と問題の有無は分ける。終了コード 0 を問題なしと読み替えず、未確認を確認済みとして扱わない。サブコマンド固有の結果分類と、その結果に応じた注意事項・次の操作は個別仕様に従う。

冒頭の要約は既存の確定情報から cmoc が機械的に作成する。本文に記された重要事項を補う専用 call は、本書の「重要事項確認用 call」で定め、機械的な要約の置換や一般的な変更要約には使わない。realization apply と realization refactor の変更要約の可否・生成方法は、それぞれ `{{cmoc-root}}/spec/app_spec/sub_command/realization_apply.md` の「report と終了コード」と `{{cmoc-root}}/spec/app_spec/sub_command/realization_refactor.md` の「変更要約」に従う。oracle edit の差分と成果の帰属は、`{{cmoc-root}}/spec/app_spec/sub_command/oracle_edit.md` の「終了と差分」に従う。

#### 重要事項の確認結果

既存の冒頭の要約の直後、元の指示より前に、確認状態と重要事項を載せる。重要事項には report 内の根拠位置と短い原文引用を添え、プロセスの正常終了と本文で報告された目標未達などを読み分けられるようにする。既存の機械的な結果分類、要約、詳細本文を変更・削除しない。

確認状態は、次の意味を判別可能にする。本節で定める確認未完了の固定文言を除き、正確な表示文言は実装に委ねる。

| 確認状態 | 意味 |
|---|---|
| 重要事項あり | 固定した機械生成版の全文を確認し、重要事項を抽出した。 |
| 全文を確認した範囲では該当なし | 同じ全文を確認したが、抽出すべき重要事項がなかった。実作業の正しさや、report 外も含む問題の不存在を保証しない。 |
| 確認未完了 | 全文の確認完了を得られなかった。 |

確認未完了として終える場合は、cmoc がこの欄に固定文言「エージェントによる重要事項の確認は完了していません。」を挿入し、未完了の理由と判明している確認範囲を併記する。固定文言の生成は agent の起動・応答に依存させない。

未確認、失敗、または不受理の出力を「該当なし」へ変換してはならない。受理した未完了の応答に部分的な抽出結果があれば、確認未完了のまま、その範囲の結果として載せる。schema 不合格などで受理できない出力は重要事項の根拠に採用せず、次の実行記録に残す。

#### 詳細結果と実行記録

個別仕様が定める詳細結果に加え、内部処理を含む掲載対象の実行記録として、次の内容を一覧で掲載する。

- 各 `codex exec`（`codex exec resume` による再開・補正を含む）で取得できた最終出力の本文と、元の出力ファイルへの参照。取得・保存先は、`{{cmoc-root}}/spec/app_spec/codex_exec_rule.md` の `--output-last-message` を正本とする。
- 実行中に新規受理された feedback observation の問題内容。掲載対象は、`{{cmoc-root}}/spec/app_spec/feedback.md` の「用語と結果分類」における observation とする。

重要事項確認用 call 自身も実行記録の対象とし、取得できた最終出力本文、出力ファイル・call log への参照、開始・終了状況、および受理結果を掲載する。確認入力の固定時点とその全文への参照を示し、確認自身の記録は確認対象外だったことを区別する。未開始なら call の実行や出力を作らない。これらの追記を理由に再確認を始めてはならない。

共通掲載対象の本文を、省略・要約または原本への参照だけで置き換えてはならない。冒頭の要約を設けても、個別仕様の必須情報と実行記録本文は省略しない。

#### 実行情報

末尾の実行情報には、本書の「実行 ID の開始表示」で定める実行 ID と対応する診断用サブコマンドログへの参照、および個別仕様が定める command、生成日時、root、branch、commit、state、終了コードなどの補足項目を掲載する。未確定値の表現は個別仕様に従い、存在しない値や実行していない処理の成功結果を補わない。

#### Structured Output の表示

共通掲載対象の各呼び出しで取得した Structured Output には、本書が primary report の対象とするすべての終了経路で、次の表示要件を適用する。表示加工は report 内の表現だけを対象とし、この加工のための追加 agent call は行わない。

JSON として解析できる場合は、次を満たす表示にする。

- オブジェクト・配列の階層とキー・値の対応を読み取れる整形表示にする。キー、値、型の区別、および配列順序を保持し、空文字列・`null`・空配列などを識別できるようにする。
- 文字列は、JSON の解釈に必要なデコードを一度だけ行い、Unicode エスケープは対応する文字として、文字列内の改行は実際の改行として読めるようにする。デコード後の文字列に含まれるリテラルのバックスラッシュと `n` の並びや JSON 風の文章を、追加でデコード・再解析してはならない。
- 引用符やバックスラッシュを含む文字列も、本文と表示上の区切りを取り違えない形で示す。

具体的なレイアウト、インデント幅、見出しの形は、上記の可読性と忠実性を満たす範囲で実装裁量とする。表示結果自体の JSON 構文への準拠や、文字列内の Markdown の装飾表示は要求しない。

JSON として解析できない場合は、その旨と取得できた原文を実行記録へ掲載する。解析できても、schema または宣言済みの決定論的事後条件の検証に不合格だった出力は、不合格であり正式な結果ではないと判別できるように表示する。

Structured Output の受理条件と不合格出力の保持は、`{{cmoc-root}}/spec/app_spec/codex_exec_rule.md` の「Structured Output > 機械的検証と正式な結果」を正本とする。表示できることを受理条件に加えたり、表示変換で出力補正や結果の受理を代替したりしてはならない。

### 重要事項確認用 call

機械的な冒頭要約だけでは拾えない、agent の出力本文に記された目標未達などを人間へ伝えるため、機械生成した primary report の全文を専用 agent が確認する。本節は、この確認の意味仕様を所有する。

#### 入力の固定と開始時点

確認入力は、既存の機械的な要約、確定した元の指示、各 agent の最終出力全文、受理済み observation、および当該 report の掲載時点までに確定した後処理結果を含む機械生成版の全文とする。詳細結果・実行記録・実行情報も含め、冒頭だけ、抜粋、または一部の call だけを全文の代わりに渡してはならない。

個別仕様が定める掲載時点に達し、その時点までの掲載情報を確定してから機械生成版を完成させる。通常の編集 workload では、自動 join、post-join、state 更新、cleanup の実際の結果を含める。これらの完了前に確認を始めて、未実行の後処理を成功として補ってはならない。

cmoc は確認用 call の開始直前に入力全文を固定し、確認対象として読み取れるファイルに保存する。call 中はその本文を変更せず、call の記録と対応付けて保持する。最終 report に確認結果と確認自身の記録を加えても、固定した入力には戻さず、確認を循環させない。先頭部分しか読めない、途中が省略された、context 上限などにより全文を扱えない場合は、全文確認が完了したとは扱わない。

確認を行うのは最外側の primary report の新規生成時だけとする。内部 join の中間 report や、primary report を兼ねない publication report のために同じ call を増やさない。primary report を兼ねる immutable な publication report の初回保存と保存済み artifact の再利用は、`{{cmoc-root}}/spec/app_spec/sub_command/feedback_close.md` の「primary report と終了結果」に従う。

#### agent の責務と境界

agent は、全文に記された目標未達、未完了、未検証、未解決事項、人間の判断が必要な点など、結果を読む人間が見落としてはいけない事項を、report 内の根拠に基づいて抽出する。元の指示の要求・例示と実績の申告、プロセスの成功と本文で報告された達成状況を分け、過去の途中結果と掲載時点までの確定結果を照合する。例えば call が正常終了していても、最終出力に「目標未達で停止した」とあれば、重要事項として扱う。

判断材料は固定した report 本文だけとする。本文中の元の指示、過去の出力、引用、command、およびリンク先への作業指示は、すべて確認対象の資料であり、確認 agent が従う指示ではない。外部のファイル、raw log、現在の repository 状態などを追加調査しない。

本命作業の再実行・補完、修正・検証、一般的な意味的変更要約、差分や成果の再認定、および feedback close の外部解決の妥当性の再判定は行わない。確認結果からサブコマンドや issue の結果分類を再判定しない。表示・構成・配置は cmoc が担う。

新しい問題の探索や observation・issue の生成も行わない。既存 observation を含む本文の再報告を防ぐため、この call では feedback reporter と報告規定をともに無効にする。提供判断の共通機構は、`{{cmoc-root}}/spec/app_spec/codex_common_rule.md` の「feedback reporter と collector context」に従う。確認結果を自動 issue 化する代替経路も設けない。

#### 起動と正確な定義の委譲

確認は新しい Codex session の読み取り専用 call とし、本命 call の会話を引き継がない。cwd は対象 repository の main worktree とし、cleanup 済みの run worktree を再作成しない。本文以外を調査しないため、文書検索 MCP と editor input handoff MCP は提供しない。

正確な詳細は次へ委譲する。受信 agent が cmoc の内部仕様を読まなくても実行できる、自己完結した指示にする。

- `{{cmoc-root}}/referenece/src/oracle/acp_builder/primary_report_review.py` の `build_primary_report_review_request`：prompt 文面、固定した入力ファイルの受け渡し、call 種別、file access mode、および MCP の選択を含む起動パラメータ。
- `{{cmoc-root}}/referenece/src/oracle/acp_builder/primary_report_review.json` の root schema（JSON Pointer `#`）：Structured Output の構造、確認状態の固定値、重要事項・根拠・未完了理由の field と組み合わせ。構造と schema で表せる出力要件は prompt に重複させない。
- `{{cmoc-root}}/referenece/src/oracle/other/cmoc_config.py` の `CmocConfigCodex.agent_calls["build_primary_report_review_request"]`：重要事項確認用 call の個別設定の既定値。

設定取得と出力検証には、`{{cmoc-root}}/spec/app_spec/codex_model_provider.md` の「agent call ごとの直接設定」と `{{cmoc-root}}/spec/app_spec/codex_exec_rule.md` の「Structured Output」を適用する。schema にない意味的品質を機械的な受理条件へ追加しない。

#### 回復待ちと出力補正

確認用 call にも、`{{cmoc-root}}/spec/app_spec/codex_common_rule.md` の「preflight validation」と、`{{cmoc-root}}/spec/app_spec/codex_exec_rule.md` の「Structured Output」「`codex exec` が失敗した場合」を適用する。回復待ち・probe・再開、補正の条件と回数、同じ session の使用、補正上限の維持、および不受理出力の保持は、後者の exec 規約に従う。回復待ち中というだけで確認未完了として保存へ進まず、その待機・再開条件に従う。確認用 call 固有の時間上限や retry 方式は設けない。

`{{cmoc-root}}/referenece/src/oracle/acp_builder/primary_report_review.json` の `#/$defs/incomplete_result` に従う全文確認不能の応答を正式に受理した場合は、確認未完了として記録・保存へ進む。その status 自体を出力補正や再試行の理由にしない。

これらの呼び出し規約で確認を続行できない場合の保存と最外側の終了結果には、次の「確認の停止・失敗と保存」「確認結果と終了結果の分離」を適用する。

#### 確認の停止・失敗と保存

確認用 call のプロセスの成功、出力の受理、および全文の確認完了は分けて判断する。起動条件を満たせない場合、全文を渡せない場合、または本書の「回復待ちと出力補正」が参照する呼び出し規約に従っても確認を続行できない場合（回復対象外の失敗、再開不能、補正上限到達など）は、確認未完了として記録・保存へ進む。cmoc が検出した未開始・失敗の理由と、受理した agent の未完了応答を区別し、存在しない応答や確認済み範囲を補わない。未完了の表示は、本書の「重要事項の確認結果」に従う。

本命処理の中断後に確認を開始する例外と、確認に対する新しい取消要求の区別は、`{{cmoc-root}}/spec/app_spec/subcommand_interruption.md` の「共通動作」「重要事項確認の取消」に従う。取消を受け付けたら回復待ちを終了し、実行中の確認用 call または probe の自然完了を待たず子 process の停止・終了処理へ移る。同じ invocation では、取消後に新しい確認 call、補正、retry、probe、または回復待ちを開始しない。確認結果の受理と競合した場合も取消を優先し、確認未完了として記録する。

取消後に別の primary report を新規生成する必要が生じた場合も、確認は開始せず、取消により未開始であることをその report に示す。先の report に対する確認結果を、本文が異なる report の全文確認結果として流用してはならない。

確認自体を不可分な finalization に含めて停止要求を保留しない。停止確認と記録の保存は省略せず、停止を確認できない process を終了済みと表示しない。

確認を終えたら、機械生成版と取得済みの詳細本文を保持し、確認状態・結果と確認自身の記録を加えて、個別仕様が定める保存・終了処理へ進む。これらの追記によって、report の掲載時点や publication・cleanup・保存の順序を変更しない。

#### 確認結果と終了結果の分離

確認工程の完遂は、最外側の正常終了条件にしない。一般的な call failure や必須後処理の失敗・取消による終了規約に対する例外として、確認未完了だけを理由に、本命処理の `result`・`completion_reason`、最外側の終端分類、終了コード、確定済み成果、state、および成立済み publication を変更しない。本命処理の正常完了、`error`、正常な `user_interruption` のいずれにも適用する。

確認結果の重要事項やその件数も、本命処理の結果分類や終了コードの再判定に使わない。確認の取消を、本命処理の再開・rollback、成立済み publication の取消、または close の再判定の契機にしない。

この例外は確認未完了そのものに限る。primary report 自体や必要な記録の保存、process の停止確認、その他の必須後処理の失敗・取消には、`{{cmoc-root}}/spec/app_spec/error_handling.md` の「エラー終了の確定」と個別仕様のエラー規約を適用する。確認未完了を理由に、必要な保存・終了処理を省略したり、その失敗を成功へ変換したりしてはならない。

## terminal result

### 定義と分類

terminal result は、最外側の末端サブコマンドについて確定した終端結果を、人間へ最後に示す 1 つの console 出力単位である。

共通分類は、次の 3 種類とする。

- `natural_completion`: サブコマンド固有の正常な処理結果を確定して自然完了した
- `user_interruption`: ユーザー中断要求に従い、個別仕様が認める確定済みの部分結果で正常に完了した
- `error`: エラー終了した

TUI 起動途中の取消は、確定済み部分結果による正常完了を表す `user_interruption` には含めない。その意味は、`{{cmoc-root}}/spec/app_spec/subcommand_interruption.md` の「TUI 起動途中の取消」、表示の境界は本書の「TUI と自動補完の境界」に従う。取消のために共通分類へ新しい固定値を追加することは要求しない。

共通分類、サブコマンド固有の `result` または `completion_reason`、および終了コードは、それぞれ独立した意味とする。終了コードだけから、共通分類、サブコマンド固有結果、またはスタックトレースの要否を決めてはならない。

### 確定と表示の順序

terminal result は、次の処理をすべて完了した後に確定して表示する。

1. 個別仕様が定める report の掲載時点まで、state、成果物、および終端結果に必要な情報を確定する
2. 本命処理の並列処理、非同期処理、回復待ち・probe・再開の処理、および console へ出力し得る通知処理を停止または drain する
3. 非対話サブコマンドでは、機械生成版を完成・固定し、本書の「重要事項確認用 call」の工程を行う。確認の終了処理と取得できた出力の回収後、確認状態・結果と確認自身の記録を加えて primary report を保存する。個別仕様が保存済み artifact の再利用を定める場合は、再確認せず保存確認を行う
4. 個別仕様が report 保存後に publication・cleanup などを行う場合は、それらを完了し、実際の終端結果を確定する。immutable な report を書き換えず、個別仕様が定める記録先に結果を残す
5. 残る非同期処理と通知処理を停止または drain する。非対話サブコマンドでは、本書の「完了時のエディタ表示」に従って保存済み primary report の表示用エディタの起動を試みる
6. terminal result を含むサブコマンド終了イベントをサブコマンドログへ書き込み、flush する

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

pending feedback observation の件数と warning は、`{{cmoc-root}}/spec/app_spec/feedback_observation.md` の「durability と retention」が定める通知境界に従う。

Windows toast の対象、発火順序、通知内容、および失敗時の扱いは、`{{cmoc-root}}/spec/app_spec/windows_toast_notification.md` の「Windows toast 通知」を正本とする。

## サブコマンドログファイル

### 基本要件

- ログファイルは、本書の「実行 ID の開始表示」で定める最外側のサブコマンド実行と 1:1 で対応させ、内部処理もそのログへ記録すること
- ログファイルは JSON Lines 形式であること
- ログファイルは `{{repo-root}}/.cmoc/gu/log/sub_command/{{execution-id}}.jsonl` に出力すること
- ログファイルは `{{run-root}}` 側に出力してはいけない
- サブコマンド中に発生したイベント 1 つを、ログファイルの 1 行に記録すること
- イベントの追記はバッファリングせずに即時 flush すること

### 診断記録

サブコマンドログは、サブコマンド呼び出しから終了までを追跡できる完全な診断記録とする。少なくとも次の情報を記録する。

- サブコマンド呼び出しと、その実行 ID。実際の最外側のサブコマンド名は、非 TUI の実行も含め、自由文の解析を要しない構造化された値で記録する
- 作成した editor input と primary report の保存先、および関連する agent call、Codex call、session、run の識別情報との対応。agent call の開始前や入力中の失敗も含め、作成済み記録の所属実行を追跡可能にする
- 階層化されたサブステップを含む全ステップと、その時間
- 全 Codex call と、対応する Codex call ログ、経過時間、および戻り値
- 回復待ちの開始・継続、理由とその変更、個別 probe の結果、復旧、再開と再発、および待機終了の理由。停止した呼び出しと probe・再開を対応付け、確認した呼び出し条件と結果の適用範囲を追跡可能にする
- warning
- handled failure と internal failure の判別に必要なエラー詳細
- サブコマンド終了イベント。terminal result を表示する経路では、その結果を含める。正常終了した TUI でも終了イベントは省略しない
- サブコマンド全体の経過時間、Codex CLI の quota と一時障害それぞれの回復待ち時間、および終了コード。待機理由が変わった場合も、各理由で待った時間を追跡可能にする

過去のサブコマンド実行で起きたことを追跡するための具体的な field は、realization の裁量で定めてよい。ただし、本書の「TUI 再開のための実行記録」は機械的な再開判断に使う安定契約とする。また、`{{cmoc-root}}/spec/app_spec/feedback_observation.md` の「rule registry」の detector rule が参照する event は、同仕様が定める `event_schema_version`, `event_id`, `event_type`, context、および rule 固有 field を安定した契約として含める。

feedback detector は、安定契約として定義されていない自由文 field を判定に使用してはならない。

### ダウンロードアセットの診断記録

明示 doctor のコンポーネント準備について、本書の「基本要件」に従ってサブコマンドログへ記録する。資材の有効性・再利用・取得の意味は、`{{cmoc-root}}/spec/app_spec/download_asset_cache.md` の「有効性と再利用」「取得と公開」に従う。記録から次を確認できるようにする。

- 実行 ID、使用する cmoc root、コンポーネント、および要求する資材の識別情報との対応。
- 再利用した準備済みコンポーネント、有効なキャッシュ、その他の正常なローカル資材と、その保存先。並行取得の待機後に完成品を再利用した場合も識別する。
- キャッシュを使わなかった理由。準備済みコンポーネントの再利用による確認不要・未確認と、欠落、識別不一致、完全性の確認不合格、読み書き失敗などを区別する。
- 取得した資材と、取得関連の通信の種類・試行回数・成否、資材ごとの取得回数、および有効なキャッシュとしての公開結果。

取得回数は、アセットごとに外部からの取得を試みた回数とし、重複取得・再試行・途中失敗も計測から除かない。一つの取得処理内の通信回数とは区別する。更新確認・存在確認・依存解決など、資材本体を取得しなかった通信の試行も記録し、遮断・失敗した通信を通信ゼロと扱わない。

途中で失敗した場合も確認済みの実績を残し、未確定の値をゼロや成功で埋めない。アセットの再利用・取得・公開と、コンポーネントの動作検証の結果を区別する。具体的な field・イベント構成は本書の「診断記録」の裁量に従う。

### 索引同期の診断記録

索引同期と MCP 検索要求について、所要時間、処理量、結果、および打切り理由を調べられるようにする。通常起動・明示 doctor の同期と、TUI 利用中も含む MCP 検索要求・自動同期・再同期を対象とする。呼出し元の最外側のサブコマンドログへ、本書の「基本要件」に従って保存する。

記録から、実行 ID、サブコマンド、対象 work-root、索引 identity、および MCP 経路の Codex call・検索要求・各同期の対応を追えるようにする。並行要求や再同期を混同させない。接続側の context 供給と記録の搬送は、`{{cmoc-root}}/spec/app_spec/codex_common_rule.md` の「文書検索 MCP」に従う。

検索要求と各同期について、次を記録する。

- 開始、終了処理を含む実測の総所要時間、結果。同期の更新あり・変更なし・失敗・取消・期限超過を区別し、親の検索要求やサブコマンドの結果と混同しない。
- 確認できた文書の処理状況と、文書埋め込みの新規生成数・保存数・同一 worktree 内での再利用数・別 worktree 由来の再利用数。再利用の内訳は、保存結果を生成した worktree と同期先 worktree との関係で区別し、cache の配置先だけで判定しない。
- 失敗・取消・期限超過の理由と、資源待ち・処理の停滞・停止と回収の状況。期限超過では適用した期限と判定時の実測値を残し、その後の終了処理と区別する。

文書埋め込みの新規生成数は、文書入力片ごとに実際に生成した件数とし、同じ入力を重複生成した場合も計測から除かない。入力片数、文書数、および推論呼び出し回数を区別し、一度の呼び出しで複数の入力片を処理した場合も混同しない。文書埋め込み、query の埋め込み、およびコンポーネント検証の推論は分けて計測する。

開始と打切り理由は終端を待たずに記録する。途中で終了した場合も確認できた実績を残し、未確定値をゼロや成功で埋めない。終端を記録できない強制終了は、完了した結果と区別する。

文書入力片・再利用・回収・期限・進捗の意味と MCP stdout の境界は、`{{cmoc-root}}/spec/app_spec/document_search.md` の「同期と cache」「identity と保存先」「排他、期限、終了」「stdio MCP と失敗の公開」に従う。詳細な計測区間、イベント構成、相関方式は実装に委ねるが、測定対象・単位、再利用数等での重複入力の集計方法、および途中値／確定値の区別が分かる記録にする。console の表示には本書の「進行通知」「TUI と自動補完の境界」を適用する。

### handoff 送信元情報の記録

editor input handoff を有効にする初回 exec と対話 resume では、各 Codex process を起動する前に、次の対応を既存のサブコマンドログへ記録し、flush を完了する。

- 本書の「実行 ID の開始表示」で定める実行 ID と、送信元のサブコマンド名
- 起動する Codex process の Codex call ID と、対応するログ保存先
- その実行の診断用サブコマンドログのフルパス

Codex call ID は、`{{cmoc-root}}/spec/app_spec/codex_common_rule.md` の「呼び出し単位と ID」で定める識別子を使い、記録する送信元情報は同文書の「editor input handoff MCP」に従って MCP の呼び出し元コンテキストへ供給する実際の値と一致させる。送信元が実行中でも、この対応から既に保存された記録へ到達できるようにする。終了時にだけ保存される戻り値や最終結果を、対応の特定に必要としてはならない。

この記録は送信元の識別と保存済み記録への到達を保証する。TUI 会話全文や最終回答の保存・取得保証は追加しない。本文の受け渡しと tool result・log の境界は、`{{cmoc-root}}/spec/app_spec/editor_input_handoff.md` の「agent の責務と権限」と「tool result と log」に従う。

### TUI 再開のための実行記録

`{{cmoc-root}}/spec/app_spec/sub_command/resume.md` の「ログからの種別解決」「対象の適格性と会話選択」を、既存のサブコマンド JSONL から機械的に判断できるようにする。新規起動の初回 exec・自動移行先 TUI と後日の公開 resume を対象とし、本書の「handoff 送信元情報の記録」と同じ実行・call に対応付ける。

| 記録する情報 | 区別する意味 |
|---|---|
| 実行 ID、実際の最外側のサブコマンド、再開元実行 ID | 今回の invocation と、`resume` が指定した直接の再開元。新規起動には再開元がない |
| 解決した TUI 種別、agent call 種別、file access mode | 呼び出し元のコマンド名と、実際に続ける workload とその制約 |
| 各段階の agent call ID、Codex call ID、各保存ログへの対応 | 初回 exec と TUI の別々の call、および内部移行の対応。初期 prompt を持つ call と prompt 不在の call を区別し、会話の識別子で代用しない |
| 実際の cwd、そこから導出した work-root・repo-root、使用した `$CODEX_HOME` の場所 | その process が使用する環境。相対表記や symlink に依存せず照合できる絶対パスで記録する |
| 最外側の cmoc 実行、初回 exec、TUI process の開始・終了と結果 | 起動準備、process の生成成功・生成失敗、終了確認済み・未確認を区別し、開始・終了と終了コードを記録する。子 process の終了だけで最外側の実行終了を代用しない |
| 初回 exec の最終成功・失敗・取消と、その確認結果 | UUID の取得、CLI の正常終了、および call の最終成功を区別する。取消時は作業未完了を保持し、初回成功後の TUI 起動失敗と混同させない |
| 初回 exec で取得した Codex session ID、TUI 起動時に指定する固定した ID とその取得元 | 初回 exec の取得結果と、公開 resume の再開元記録から引き継いだ値を区別し、今回の process に指定する ID へ対応付ける |

各意味を構造化された値とイベントの順序で表し、記録形式の識別、状態遷移、および未確定値の扱いを安定させる。未起動・未発行・未取得を区別し、存在しない値を作らない。読み手が解釈できない記録や矛盾した対応を、再開可能な状態として扱わない。具体的な field 名・符号化・イベント分割は実装に委ねるが、自由文、ファイル時刻、ID の発行順、または最後に見つかった会話 ID から状態を推測する形式にしてはならない。

起動前に確定できる情報は、それぞれの process の起動前に記録する。初回 exec から得た ID は取得でき次第記録し、初回成功と終了の確認結果は TUI 移行前に保存する。TUI に指定する固定した ID と process の対応は、TUI process の起動前に記録し、即時 flush する。ID の決定は、`{{cmoc-root}}/spec/app_spec/codex_tui_rule.md` の「TUI の固定 session ID」に従う。

TUI が実際に開いた会話、切り替え履歴、終了時の主会話、および入力待ち状態の確認・記録は要求しない。起動時に指定した ID を、観測済みの実会話や終了時の主会話として記録してはならない。

終了時は、初回 exec と TUI process のそれぞれの終了確認結果・終了コードと、最外側の cmoc 実行の終了を記録する。初回失敗・取消、初回成功後の TUI 未起動・生成失敗、および生成後の正常・異常終了を区別する。強制終了などで終了記録を保存できなかった場合、記録の途切れを終了確認として扱わない。必要な保存・flush の失敗は診断可能にし、再開可能な記録が完成したと報告しない。

再開後の対応は新しい実行のログへ保存し、再開元のログや Codex call 記録を上書きしない。そのログには、直接の再開元との対応、引き継いだ初回成功の根拠と固定した session ID、および今回確認した workload・環境・process の生成と終了を残す。過去に確認された初回の事実と今回の観測結果を区別し、そのログだけで次の適格性を判断できるようにする。再開専用の ID 体系や会話本文の独自保存は追加しない。

## TUI と自動補完の境界

TUI の通知境界を適用するサブコマンドと非対話サブコマンドの分類は、`{{cmoc-root}}/spec/app_spec/windows_toast_notification.md` の「目的と適用範囲」と「非対話サブコマンドの通知境界」を正本とする。本書の primary report 契約は、その分類を変更しない。

- TUI の通知境界を適用するサブコマンドでは、正常な TUI 終了後に非対話サブコマンド用の primary report または terminal result を追加しない。`cmoc resume` の場合も同じ境界とする
- primary report を生成しない TUI 経路には、重要事項確認用 call も追加しない
- `cmoc oracle edit` は非対話サブコマンドとして本書を適用する。内部の各 `codex exec` は独立した terminal result を表示せず、最外側のサブコマンドが終了状態の確定後に 1 回だけ表示する
- TUI の起動前エラーまたは異常終了には、本書と `{{cmoc-root}}/spec/app_spec/error_handling.md` の「エラーハンドリング規則」のエラー表示規則を適用する。非対話サブコマンド用の primary report は要求しない
- 初回 exec 中は、「初回応答を生成中」など、稼働中と分かる短い進行表示を stderr へ出す。生成途中の回答本文を独自にストリーミング表示しない。初回 exec を含むことだけを理由に非対話サブコマンドへ再分類せず、独立した primary report や完了表示を追加しない
- TUI 起動途中の取消では、起動を取り消し、初回作業が未完了であることを短く表示し、終了イベントへ記録する。部分結果による正常完了表示や非対話サブコマンド用の primary report は要求しない
- TUI process へ制御を渡した後は、cmoc の進行通知を TUI の表示へ混入させない
- 制御を渡した後も、文書検索 MCP の検索要求と自動同期は本書の「索引同期の診断記録」に従ってサブコマンドログへ記録する。この記録を TUI への進行通知の追加理由にしない
- TUI 用の初回 exec より前にも実行 ID の開始表示とサブコマンドログの記録規則を適用する。handoff を有効にする経路は、本書の「handoff 送信元情報の記録」も満たす
- 自動補完プローブの判定、console 出力、および通常処理の抑止は、`{{cmoc-root}}/spec/app_spec/cli_auto_completion.md` の「CLI 自動補完規則」を正本とする

## non-goal

本書は、次の機能を要求しない。

- ANSI color に依存する表示
- TTY と non-TTY で意味が変わる動的表示
- verbosity option または debug option
- 機械可読な stdout 用の新しい JSON schema
- 個別サブコマンド仕様が定める正常経路の report 本文の意味または判定基準の変更
- Windows toast 通知内容の拡張
- feedback detector が使用する安定した構造化 event 契約の変更
