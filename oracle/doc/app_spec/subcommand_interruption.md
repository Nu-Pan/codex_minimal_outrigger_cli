# サブコマンドのユーザー中断

## 用語

- ユーザー中断要求とは、実行中の cmoc に対して、以後の処理を打ち切り、確定済みの部分結果でそのサブコマンドを完了させるようユーザーが通知することである。
- 中断可能サブコマンドとは、ユーザー中断要求を正常系として処理することが個別仕様に明示されたサブコマンドである。

## 対象

- 現在の中断可能サブコマンドは以下とする。
    - `cmoc realization refactor fork`
    - `cmoc oracle review`
    - `cmoc feedback report`
- 中断可能サブコマンドとして追加できるのは、長時間実行され、かつ処理済みの範囲だけでも一貫した結果として確定できるサブコマンドに限る。
- この条件を満たすだけでは中断可能サブコマンドとみなさず、個別仕様への明記を必須とする。

## 中断要求の通知

- 中断可能サブコマンドでは、実行中の端末からの `Ctrl+C` をユーザー中断要求として受け付ける。
- cmoc はユーザー中断要求を自ら処理し、子 process の想定外エラーとしてだけ扱ってはいけない。
- `Ctrl+C` 以外の入力をユーザー中断要求として扱うかは未定義とする。

## 共通動作

- ユーザー中断要求を受け付けた cmoc は、新しい処理単位の開始を止める。
- 実行中だった処理単位を完了させるか rollback するかは個別仕様または実装裁量とする。ただし、破損した部分結果や未確定の部分結果を完了済みとして残してはいけない。
- 確定済みの部分結果を保持したまま、個別仕様が定める state 更新と後処理を行う。
- 確定済みの部分作業と中断による終端結果を要約した primary report を、個別仕様が定める形式と保存先へ保存する。その後に `user_interruption` の terminal result をサブコマンドログと console へ出力する。共通の保存・出力規則は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` を正本とする。
- ユーザー中断要求による完了は正常系とし、エラー結果またはエラー終了として扱ってはいけない。
- primary report、個別仕様が保存を認める再開 state、および terminal result を含むサブコマンド終了イベントから、自然完了ではなくユーザー中断要求によって完了したことを判別可能にする。
- ユーザー中断要求を受け付けた後は、そのサブコマンドのための新しい Codex CLI 呼び出し、retry、quota 回復待ち、および Codex CLI session の再開を行わない。この指示は `codex_exec_rule.md` の待機・再開規則より優先する。
- primary report の保存を含む完了処理自体に失敗した場合は、ユーザー中断要求による正常系ではなく、個別仕様と error handling 規則に従う。
- ユーザー中断要求による terminal result の Windows toast 通知は、`{{cmoc-root}}/oracle/doc/app_spec/windows_toast_notification.md` を正本とする。

## 中断後の扱い

- 中断後の refactor run の state と次の操作は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md` の「ユーザー中断」を正本とする。
- oracle review の部分結果と再開境界は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/oracle_review.md` の「ユーザー中断」を正本とする。
- feedback report の保存 state と再開方法は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/feedback_report.md` の「ユーザー中断と再開」を正本とする。
- 編集 run または oracle review の中断位置を再開する checkpoint を保存してはいけない。feedback report が保存する正式な agent call result は処理位置ではなく固定入力に対する確定結果であるため、この禁止の対象外とする。
