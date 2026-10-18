# Windows toast 通知

## 目的と適用範囲

- cmoc は、ユーザーが端末を見ていない場合に、処理の結果や応答の完了を Windows toast で知らせる。
- 対象環境は、`{{cmoc-root}}/oracle/doc/dev_rule/development_environment.md` の「基本環境」が定める Windows 11 上の WSL2 とする。
- 通知対象は、ユーザーが直接起動した最外側の末端サブコマンドの terminal result と、Codex CLI の TUI に関する初回処理完了・応答完了とする。TUI の発火条件と終了時の扱いは、本書の「TUI の通知境界」に従う。
- 最外側の末端サブコマンドとは、1 回の `cmoc` invocation でユーザーの argv が選択した、実処理を持つ最も深いサブコマンドを指す。
- cmoc の内部処理として呼び出す関数、agent call、または Codex call は、最外側の末端サブコマンドではない。

現在、TUI の通知境界を適用するサブコマンドは次のとおりとする。

- `cmoc tui`
- `cmoc oracle investigation`
- `cmoc resume`

## 非対話サブコマンドの通知境界

- TUI の通知境界を適用するサブコマンド以外の最外側の末端サブコマンドは、非対話サブコマンドとして扱う。
- 非対話サブコマンドの primary report と terminal result の確定条件は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「primary report」と「確定と表示の順序」を正本とする。確定した terminal result を 1 回だけ通知する。
- 通知の成否を、terminal result の確定条件に含めてはならない。

### terminal result の分類

terminal result の共通分類は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「定義と分類」を正本とする。Windows toast は、同仕様が定める全共通分類を区別可能にする。

`user_interruption` は、エラーとして通知してはならない。

ユーザー中断要求の成立条件と完了処理は、`{{cmoc-root}}/oracle/doc/app_spec/subcommand_interruption.md` の「サブコマンドのユーザー中断」を正本とする。

非対話サブコマンドの内部にある次の処理では、Windows toast を通知しない。

- 自動 join、post-join、およびその cleanup
- `codex exec`
- Structured Output の補正 turn
- retry、quota または一時障害の回復確認 probe、および回復待ち後の再開
- 並列 agent call

## TUI の通知境界

内部の自動移行では、実際の最外側のサブコマンド名を維持する。後日の公開 `cmoc resume` の通知に使うサブコマンド名は `resume` とする。再開元のコマンド名や解決した TUI 種別で置き換えず、callback と重複排除の context は新しい TUI process に対応させる。

### 初回処理完了

初回 exec が最終的に成功し、続く TUI process の生成に成功した時点で、「初回処理完了」を 1 回だけ通知する。起動管理側がこの境界を判定する。

初回 exec の成功だけでは通知しない。TUI process の生成前に失敗した場合は、本書の「終了と取消」に従う起動前エラーとする。生成後には TUI の内部準備が続いている可能性があり、この通知は入力可能状態や TUI 全体の成功を保証しない。

この通知は、新規起動の exec から TUI への自動移行に限る。初回 exec を行わない公開 `cmoc resume` では発火しない。

### 応答完了

Codex が通知専用処理を直接呼び出し、TUI の agent turn の完了を「応答完了」として通知する。TUI の入力可能状態を保証する「入力待ち」の通知にはしない。起動管理側の終了待ちから独立して通知し、その通知処理を会話の追跡、移行確認、または起動成功の認定に使わない。

通知専用処理は、`{{cmoc-root}}/oracle/doc/app_spec/codex_tui_rule.md` の「TUI の固定 session ID」で定める ID に対応する通知だけを対象とし、subagent の通知を除く。turn の識別と重複排除の範囲は、その TUI process invocation 内に限り、同じ turn の callback を複数回受け取っても通知は 1 回だけとする。

### 終了と取消

- TUI の正常終了時は、ユーザー自身が終了操作を行っているため、サブコマンドの terminal result を追加で通知しない。
- 初回 exec の失敗を含む TUI の起動前エラー、または TUI の異常終了は、失敗結果を確定した後に 1 回だけ通知する。生成後の異常終了は、通知済みの初回処理完了とは別の事実として扱う。
- TUI 起動途中の取消の意味は、`{{cmoc-root}}/oracle/doc/app_spec/subcommand_interruption.md` の「TUI 起動途中の取消」に従う。取消を、部分結果による正常完了、初回処理完了、または応答完了として通知しない。

## 通知内容

### 必須情報

各通知には、次の情報を含める。

- サブコマンド名
- repository を識別できる短い情報
- 状態

### 内容の制限と裁量

- terminal result の通知には、経過時間を含めてよい。
- prompt、assistant の回答本文、秘密情報、フルパス、および Windows の通知履歴へ残す必要がない情報を含めてはならない。
- `{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「パス表示のフォーマット」は、Windows toast の通知内容には適用しない。

## 決定論的な発火と Codex CLI の設定境界

- 通知の要否は、prompt、assistant の回答、または installed skill に判断させてはならない。
- cmoc のサブコマンド lifecycle event と、cmoc が起動した Codex process の lifecycle event から決定論的に発火する。
- cmoc が起動する Codex CLI について、通知に関する effective configuration は呼び出し単位で cmoc が決定する。
- TUI 起動用の初回を含む `codex exec` では、agent turn 完了の通知 callback を無効にする。
- TUI では、Codex が応答完了時に通知専用処理を直接呼ぶ callback を、その TUI process にだけ設定する。固定した session ID と当該 invocation の通知 context を渡し、起動管理側で TUI の出力を監視して通知を中継する構成にしない。
- 通知を設定するために、`$CODEX_HOME/config.toml` を生成または変更してはならない。

## 実装前に検証する Codex CLI の外部契約

現行 oracle は、Codex CLI の通知 callback に関する具体的な interface を定義しない。

realization の実装前に、利用する Codex CLI 版のソースと、実行を明示的に指示された場合の実測で、次の外部契約を検証する。新規起動の自動移行と後日の公開 resume の両方を対象とする。

- callback を呼び出し単位で設定または無効化する設定 key
- 応答完了を表す callback event の種類、payload、および通知専用処理を直接起動する経路
- 固定した session ID に対応する通知を選び、subagent を除外し、同じ turn の重複を識別・排除するために利用できる情報
- 通知専用処理の起動失敗が Codex の turn 処理を失敗させないこと

これらの確認を、TUI が会話を開いたことや入力可能になったことの検証へ広げない。ソースで確認した挙動と実測した挙動を区別し、現在の内部実装を将来版の互換性保証にしない。

### 未検証 interface の扱い

- 検証結果を得る前に、特定の設定 key、event 名、payload 形式、または発火保証を正本仕様として断定してはならない。
- 必要な callback を利用できない場合も、TUI 出力の解析または agent や installed skill への委譲を fallback として追加してはならない。

## 通知処理と Windows toast transport

- 外部 PowerShell module または新しい Python package を必須依存にしてはならない。
- 通知内容は、shell 文字列の組み立てに依存せず、データとして安全に transport へ渡す。
- 通知処理には有限の上限時間を設け、本命処理を長時間待たせてはならない。
- 通知の準備・設定の失敗、callback の利用不能、transport の欠落・起動失敗、または toast の送信・表示失敗によって、TUI の起動・利用を止めたり、サブコマンドの終了コード、run state、成果物、retry、または成功判定を変更したりしてはならない。
- 通知失敗や通知の欠落を、Codex call またはサブコマンドの失敗や再実行の理由にしてはならない。

## 自動補完プローブ

- `_CMOC_COMPLETE` が環境変数として存在する呼び出しでは、通知処理を初期化または実行してはならない。
- 自動補完プローブでは、transport の利用可能性を検査してはならない。
- 自動補完プローブでは、通知に関する warning を stdout または stderr へ出力してはならない。

## non-goal

本書は、次の機能を要求しない。

- agent turn の途中にある tool approval または追加承認要求の通知
- toast のクリックによる terminal focus、action button、sound、または表示時間のカスタマイズ
- repository 設定から任意の host command を実行する仕組み
- 通知履歴または永続的な通知 state の新設
- Windows 以外の desktop notification 対応
