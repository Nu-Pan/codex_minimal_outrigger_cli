# Codex TUI 呼び出し規約

本書は、汎用 TUI と oracle 調査 TUI の新規起動、自動移行先の TUI、および後日の公開 `cmoc resume` の対話起動を対象とする。各段階には、`{{cmoc-root}}/oracle/doc/app_spec/codex_common_rule.md` の「Codex CLI 共通呼び出し規約」を適用する。

公開 resume の入口・適格性・workload の保持は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/resume.md` の「目的と公開入口」「対象の適格性と会話選択」「workload と起動環境の保持」を正本とする。各 workload の目的と権限は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/tui.md` の「全バックエンド共通」と、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/oracle_investigation.md` の「TUI 起動パラメータ」「調査結果と変更の扱い」に従う。

## TUI の新規起動と対話 resume

新規の汎用 TUI と oracle 調査 TUI は、初回の 1 ターンを `codex exec` で実行し、その会話を TUI で続ける。長い完全 prompt を argv に載せず、入力確定後の貼り付けや送信操作を人間に要求しないことを目的とする。初回 exec は元の依頼を実行する本命ターンであり、準備や要約だけを行う call ではない。

### TUI 起動と再開の call ID

汎用 TUI と oracle 調査 TUI の新規起動では、初回 exec と自動移行先の TUI を別々の agent call・Codex call とする。両段階は同じ既存 workload の `agent_call_kind` を使い、agent call ID と Codex call ID はそれぞれ新たに発行する。最外側の実行 ID と実際のサブコマンド名は共通とし、内部移行を新しい `cmoc resume` invocation として扱わない。

後日の公開入口 `cmoc resume` は、新しい最外側の実行・agent call・Codex call とする。元の workload と同じ `agent_call_kind` を使い、Codex session ID の引継ぎを cmoc の各 ID の再利用と混同しない。

同じ TUI process の各 turn では同じ Codex call ID を使う。

### 新規起動の二段階実行

1. editor input を確定し、workload の builder で完全 prompt を確定する。
2. `{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「prompt の保存と stdin 入力」に従って初回 Codex call 用の完全 prompt を保存し、その保存本文を stdin 入力として初回 exec を開始する。
3. `{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「非対話 call の会話 ID の取得」に従って ID を取得し、同文書の「最終的な成功と失敗の判断」に従って CLI の正常終了と当該 call の最終成功を確認する。ID の取得だけでは初回完了としない。
4. 初回 process の終了と必要な記録の保存を確認し、以下の検査済み再開入力を構築する。新しい TUI process 用の設定・MCP・通知を準備する。
5. 初回に取得した同じ Codex session UUID を明示し、初期 prompt のない対話 resume へ自動移行する。初回回答は再開した TUI で確認できるようにする。

初回 exec の出力と記録の保存は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「非対話 call の記録」「stdout, stderr の扱い」「`--output-last-message`」に従う。Structured Output は要求しない。初回の進行表示は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「TUI と自動補完の境界」、初回処理完了の通知は、`{{cmoc-root}}/oracle/doc/app_spec/windows_toast_notification.md` の「TUI の通知境界」に従う。

初回失敗には `{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「TUI 起動用の初回 exec の回復例外」、初回実行中の取消には `{{cmoc-root}}/oracle/doc/app_spec/subcommand_interruption.md` の「TUI 起動途中の取消」を適用する。初回成功後に TUI 起動が失敗した場合も、初回作業と TUI 起動のどちらも自動 retry せず、記録を保存して終了処理へ移る。後日の公開再開の適格性は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/resume.md` の「対象の適格性と会話選択」に従う。

### 検査済みの再開入力

起動管理側は、対話 resume の前に次の検査を完了する。正確な入力構造と新規入力との排他条件は、`{{cmoc-root}}/oracle/doc/app_spec/codex_common_rule.md` の「呼び出し単位と ID」で委譲した `TuiResumeTarget` と workload の builder に従う。

- 内部の自動移行では、初回 exec の成功・終了、保存済み UUID と必要なログを確認する。最外側の cmoc 実行は継続中であり、公開 resume の「最外側の実行が終了済み」という条件は適用しない。
- 後日の公開 resume では、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/resume.md` の「ログからの種別解決」「対象の適格性と会話選択」を満たす。
- 両経路とも、同文書の「workload と起動環境の保持」に従って、元の workload、file access mode、保存 cwd とそこから導出した path context、および実際の `$CODEX_HOME` の場所を照合する。二段階で共用するモデル設定値と、後日の公開 resume の設定取得時点は、`{{cmoc-root}}/oracle/doc/app_spec/codex_model_provider.md` の「TUI 起動での設定の確定」に従う。

### 対話 resume の process

TUI process は対話型の Codex を起動し、端末の入出力を使用する。`--json` による stdout 収集、`--output-last-message`、Structured Output とその補正、および非対話 call の回復待ちを TUI process に適用しない。

起動管理側は、TUI process の生成後はその終了を待つ。実際に会話を開いたか、入力可能になったか、終了時にどの会話を開いていたかという TUI の内部状態を監視・確認しない。管理する会話の識別は、本書の「TUI の固定 session ID」に従う。

- 検査済みの Codex session ID を明示して同じ会話を開く。初期 prompt は不在とし、過去の prompt、再構築した prompt、skeleton、空文字列、または再開を促す補助指示を送らない。prompt ファイルを捏造せず、prompt 用の stdin リダイレクトも行わない。
- 再開パラメータは、元の workload の `agent_call_kind`、file access mode、および MCP の提供判断を維持する。保存された会話内の workload の規定を継続し、cmoc が規定を再送して新しい turn を開始する方式にしない。

対話 resume の具体的な argv 配列・入力経路を、未検証の Codex interface に基づいて固定しない。必要な検証は、本書の「実装前に検証する TUI の外部契約」に従う。内部の起動制御や設計理由を agent 向け prompt に追加しない。

### process ごとの資源準備

共用するモデル設定値と、process ごとに準備する資源を区別する。起動管理側は、新しい TUI process の argv override、feedback・handoff・文書検索 MCP の接続・capability・診断 context、および通知設定を準備する。`{{cmoc-root}}/oracle/doc/app_spec/codex_common_rule.md` の「feedback reporter と collector context」「editor input handoff MCP」「文書検索 MCP」と、`{{cmoc-root}}/oracle/doc/app_spec/windows_toast_notification.md` の「決定論的な発火と Codex CLI の設定境界」「通知処理と Windows toast transport」に従って準備・終了処理を行い、終了済み process のものを再使用しない。初回失敗・取消・TUI 起動失敗でも、作成済み資源を回収する。

#### editor input handoff MCP の準備

汎用 TUI と oracle 調査 TUI の builder は、TUI 起動用の初回 exec と対話 resume の両方で MCP を有効にし、初回 exec の完全 prompt に handoff instruction を含める。

接続と送信元情報の供給・記録・flush は、`{{cmoc-root}}/oracle/doc/app_spec/codex_common_rule.md` の「editor input handoff MCP」に従う。この準備を skeleton 構築の前提にはしない。送信元情報は、skeleton と入力確定後の完全 prompt のいずれの builder 引数にも含めず、転記用の情報を prompt へ注入しない。

#### 文書検索 MCP の準備

対話 resume では、検査済みの保存 cwd から導出した work-root と、今回の process に属する実行 ID・Codex call ID・サブコマンドログ保存先を使って接続を準備する。内部移行と公開 resume の ID の区別は本書の「TUI 起動と再開の call ID」に従う。検索索引の再利用と、終了済み process の接続・診断 context の再使用を混同しない。

### 会話の使用と排他

排他対象は、本書の「TUI の固定 session ID」で定める Codex session ID とする。cmoc 管理下で、同じ `$CODEX_HOME` の同じ ID を複数の process が同時使用しないようにする。その ID を指定する process の起動前に使用を確保し、初回 exec で取得した ID の使用の確保を TUI への移行中も引き継ぐ。公開 resume の対象検査と起動の間に、別の実行が同じ ID を使用する競合も防ぐ。TUI 内でユーザーが切り替えた先の会話に対する排他は要求しない。

会話の使用は、その process の停止を確認するまで解放しない。終了が不明な process の使用状態を推測で解除しない。具体的な排他手法は実装に委ねる。

## TUI の固定 session ID

cmoc は、ユーザーが TUI 内でセッションを切り替えない前提で振る舞う。TUI の管理対象は、起動時に指定する Codex session ID に固定する。新規起動では、成功した初回 exec で取得した ID を使う。後日の公開 resume では、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/resume.md` の「対象の適格性と会話選択」に従い、再開元の記録から解決した同じ ID を使う。

セッション切り替えの検出・追跡・禁止も、切り替えなかったことの確認も行わない。この前提を TUI の操作監視や agent 向け prompt による強制へ置き換えない。実際にユーザーが切り替えても管理対象の ID は変えず、切り替え先や終了時に画面に表示されていた会話を `cmoc resume` で再開できる保証は持たない。

## TUI の呼び出し記録

TUI の call 記録には、`{{cmoc-root}}/oracle/doc/app_spec/codex_common_rule.md` の「Codex CLI 呼び出し情報の保存」が定める ID と保存先の対応を使う。記録対象は本書の「対話 resume の process」に従い、初期入力のない対話 resume の prompt ファイルや、非対話専用の stdout JSONL・最終出力ファイルを要求しない。再開判断に必要な情報は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「TUI 再開のための実行記録」に従い、サブコマンドログから取得可能にする。

## 実装前に検証する TUI の外部契約

次の外部契約は、実装前に、利用する Codex CLI 版のソースと、実行を明示的に指示された場合の実測で確認する。本書は特定の API、event 名、payload、または対話 resume の具体的な引数形式を確定しない。

- 保存本文の stdin 入力、初回 call の最終成功を識別する終端情報、process 終了と会話保存の成立時点、および取得した UUID による対話 resume がつながること。初回回答が TUI に表示され、prompt 再送や追加 turn の自動開始なしに会話を続けられること。
- TUI process の生成・終了と終了コードを確認でき、初回 exec から TUI への移行中と公開 resume の検査から起動までを含め、固定した session ID の同時使用を防げること。
- 明示した会話を初期 prompt の再送なしで対話再開でき、存在しない会話を新規会話や最新会話で代替しないこと。
- 保存された cwd と `$CODEX_HOME` の使用場所、起動時の model provider・Model・Reasoning Effort・provider-local 設定・sandbox・承認設定の override が対話 resume に適用され、元の workload の規定を保てること。
- 再開した process が新しい feedback・handoff・文書検索 MCP の設定と context を使用し、初回 exec を含む終了済み process の接続へ戻らないこと。失敗・取消時も含め、接続・capability・子 process を回収できること。

通知専用処理との連携の検証項目は、`{{cmoc-root}}/oracle/doc/app_spec/windows_toast_notification.md` の「実装前に検証する Codex CLI の外部契約」に従う。必要な契約を確認できない場合は未検証事項として残し、推測や Fake の挙動を確定済みの外部契約に置き換えない。
