# サブコマンドのユーザー中断

## 用語

- ユーザー中断要求とは、実行中の cmoc に対して、以後の処理を打ち切るようユーザーが通知することである。
- 中断可能サブコマンドとは、ユーザー中断要求を受け、確定済みの部分結果で正常完了することが個別仕様に明示されたサブコマンドである。
- TUI 起動途中の取消とは、TUI 起動用の初回 exec を停止し、作業未完了のまま起動を打ち切ることを指す。部分結果による正常完了とは区別する。

## 対象

現在の中断可能サブコマンドは、次の 2 つとする。

- `cmoc realization refactor`
- `cmoc feedback report`

追加できるのは、長時間実行され、かつ処理済みの範囲だけでも一貫した結果として確定できるサブコマンドに限る。ただし、この条件を満たすだけでは中断可能サブコマンドとみなさず、個別仕様への明記を必須とする。

これとは別に、`cmoc tui` と `cmoc oracle investigation` の初回 exec 実行中には、本書の「TUI 起動途中の取消」を適用する。TUI へ制御を渡した後の操作を、cmoc の正常完了型の中断へ変更するものではない。

primary report の重要事項確認中には、本書の「重要事項確認の取消」を適用する。確認を取り消せることだけを理由に、元のサブコマンドを中断可能サブコマンドへ追加しない。

## 中断要求の通知

- 中断可能サブコマンドと TUI 起動用の初回 exec では、実行中の端末からの `Ctrl+C` をユーザー中断要求として受け付ける。
- cmoc はユーザー中断要求を自ら処理し、子 process の想定外エラーとしてだけ扱ってはいけない。
- 個別仕様が、state を破損させずには分割できない finalization 区間を定める場合は、区間の開始前に未処理の中断要求を確認する。開始後は、次の整合した境界に達するまで処理を途中で停止してはならない。
- `Ctrl+C` 以外の入力をユーザー中断要求として扱うかは未定義とする。

## 共通動作

本節は、確定済みの部分結果で正常完了する中断可能サブコマンドに適用する。TUI 起動途中の取消には、次の専用節を適用する。

ユーザー中断要求を受け付けた cmoc は、新しい処理単位の開始を止める。実行中だった処理単位を完了させるか rollback するかは個別仕様に従い、規定がない範囲だけ実装裁量とする。破損した部分結果や未確定の部分結果を完了済みとして残してはいけない。

realization refactor では、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md` の「不可分な確定区間」「ユーザー中断」が定める停止・rollback を適用する。共通の完了・rollback の選択肢を根拠に、長い agent 作業や全件テストの自然完了まで待ってはならない。

中断要求は、quota または一時障害による待機中と、回復確認 probe の実行中にも受け付ける。受け付けた後は待機を終了し、実行中の probe も終了処理へ移す。停止する本命処理のための新しい Codex CLI 呼び出し、probe、retry、回復待ち、および Codex CLI session の再開を行わない。probe の成功と競合した場合も、中断要求を優先する。

この優先関係は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「回復待ちと再開」に優先する。ただし、本書の「中断要求の通知」が定める不可分な finalization 区間の扱いは維持する。待機中の中断を理由に、個別 workload が要求する処理単位の commit・rollback または確定済み部分結果の保持を省略してはならない。

成立済み run では、子 process の停止確認と未確定処理単位の整合化を終えた後、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の「正常終了時の自動 join」へ進む。新しい本命作業、巡、wave、issue 処理、または変更要約用 call は開始しないが、この自動 join に必要な競合解消 call と検証は例外として許可する。join の事前検査、state 同期、結果保存、および cleanup も省略しない。run 成立前に終了した場合は、join を開始しない。

これらの停止・整合化と、その経路で必要な後処理を終えた後は、中断 report の重要事項確認用 call も例外として許可する。run 成立前に中断した report も対象とし、開始時点と確認入力は `{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「重要事項確認用 call」に従う。この例外によって、本命作業、要約、追加検証、または issue 探索を再開してはならない。

本命処理の停止要求と、自動 join 自体の取消・失敗を区別する。正常中断の terminal result は join と必要な後処理の成功後に確定し、自動 join の取消・失敗は `error` とする。不可分な finalization 内の停止境界は個別仕様に従い、途中の強制終了を正常中断へ変換しない。

確定済みの部分結果を保持したまま、次の順序で完了処理を行う。

1. 個別仕様が定める自動 join、state 更新、および後処理を行う。
2. 確定済みの部分作業と中断による終端結果を含む primary report の機械生成版を完成し、重要事項の確認結果と確認自身の記録を加えて、個別仕様が定める保存先へ保存する。生成・表示契約は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「primary report」に従う。
3. `user_interruption` の terminal result をサブコマンドログと console へ出力する。

共通の保存・出力規則は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「コンソール・ファイル、ログ出力規則」を正本とする。primary report、個別仕様が保存を認める再開 state、および terminal result を含むサブコマンド終了イベントから、自然完了ではなくユーザー中断要求によって完了したことを判別可能にする。

ユーザー中断要求による完了は正常系とし、エラー結果またはエラー終了として扱ってはいけない。ただし、primary report の保存を含む完了処理自体に失敗した場合は、個別仕様と、`{{cmoc-root}}/oracle/doc/app_spec/error_handling.md` の「エラーハンドリング規則」に従ってエラー処理を行う。重要事項確認の未完了については、本書の「重要事項確認の取消」が参照する共通規約の例外を適用する。

Windows toast による terminal result の通知は、`{{cmoc-root}}/oracle/doc/app_spec/windows_toast_notification.md` の「Windows toast 通知」を正本とする。

## 重要事項確認の取消

primary report の重要事項確認中に受けた `Ctrl+C` は、確認用 call に対する新しい取消要求とする。補正、回復待ち、および probe の間も受け付ける。本命処理の停止に使った要求は、終了工程として新たに始める確認を自動で取り消す要求にはしない。

確認の停止、確認未完了の記録、保存との関係、および終了結果への非波及は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「確認の停止・失敗と保存」「確認結果と終了結果の分離」に従う。確認を終えた後の state 確定・report 保存・publication などの処理へ、この call の取消契約を拡張しない。

## TUI 起動途中の取消

初回 exec の実行中に中断要求を受け付けた場合は、初回作業の自然完了を待たず、子 process の停止・終了処理へ移す。後続 TUI、prompt の再送、retry、回復待ち、および probe は開始しない。初回の成功確認と競合した場合も、受け付け済みの取消を優先する。

初回作業は未完了として記録し、起動の取消を作業の完了と混同させない。workload 固有の終了処理を保ち、一律の rollback や、途中の変更を完成済みの部分成果とする扱いは追加しない。作成済みの記録と accepted observation は、それぞれの保存契約に従って保持する。

process の停止確認、MCP 接続・capability・通知 context の終了処理、および会話の使用の解放は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「対話 resume の process」「会話の使用と排他」と各 MCP 節に従う。停止や保存を確認できない状態を、終了確認済みとして扱わない。

取消の表示とログは、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「定義と分類」「TUI 再開のための実行記録」「TUI と自動補完の境界」に従う。通知は、`{{cmoc-root}}/oracle/doc/app_spec/windows_toast_notification.md` の「TUI の通知境界」に従う。具体的なログ符号化と終了コードは、この取消と正常完了型の `user_interruption` を区別できる範囲で実装に委ねる。

## 中断後の扱い

- 中断後の refactor run の state と次の操作は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md` の「ユーザー中断」を正本とする。
- feedback report の issue 処理単位、run state、publication 禁止、observation retention、および次の操作は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の「ユーザー中断」を正本とする。
- 編集 run の中断位置を同じ run で再開する checkpoint を保存してはいけない。
- Codex CLI の障害からの自動再開は、ユーザー中断後に同じ編集 run の作業を再開する権限を与えない。
