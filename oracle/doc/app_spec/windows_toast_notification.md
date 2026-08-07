# Windows toast 通知

## 目的と適用範囲

- cmoc は、ユーザーが端末を見ていない場合に、処理の完了または人間の入力が必要になったことを Windows toast で知らせる。
- 対象環境は、`{{cmoc-root}}/oracle/doc/dev_rule/development_environment.md` が基本環境とする Windows 11 上の WSL2 とする。
- 通知対象は、ユーザーが直接起動した最外側の末端サブコマンドの terminal result と、Codex CLI の TUI における agent turn の完了とする。
- 最外側の末端サブコマンドとは、1 回の `cmoc` invocation でユーザーの argv が選択した、実処理を持つ最も深いサブコマンドを指す。
- cmoc の内部処理として呼び出す関数、agent call、または Codex call は、最外側の末端サブコマンドではない。

現在、TUI の通知境界を適用するサブコマンドは次のとおりとする。

- `cmoc tui`
- `cmoc oracle edit`
- `cmoc oracle investigation`

## 非対話サブコマンドの通知境界

- TUI の通知境界を適用するサブコマンド以外の最外側の末端サブコマンドは、非対話サブコマンドとして扱う。
- 非対話サブコマンドは、そのサブコマンドが要求する state、report、成果物、および終了 log を確定した後に、terminal result を 1 回だけ通知する。
- 通知の成否を、terminal result の確定条件に含めてはならない。

### terminal result の分類

terminal result の通知は、少なくとも次の状態を区別可能にする。

- 自然完了
- エラー終了
- ユーザー中断要求による正常な中断完了

ユーザー中断要求による正常な中断完了は、エラーとして通知してはならない。

ユーザー中断要求の成立条件と完了処理は、`{{cmoc-root}}/oracle/doc/app_spec/subcommand_interruption.md` を正本とする。

非対話サブコマンドの内部にある次の処理では、Windows toast を通知しない。

- `codex exec`
- Structured Output の補正 turn
- retry、および quota 回復待ち後の再開
- 並列 agent call

## TUI の通知境界

- TUI は、agent turn が完了し、人間の入力待ちになった時点で、turn ごとに 1 回だけ通知する。
- agent turn 完了の状態は、サブコマンド完了ではなく「入力待ち」として通知する。
- TUI の正常終了時は、ユーザー自身が終了操作を行っているため、サブコマンドの terminal result を追加で通知しない。
- TUI の起動前エラーまたは異常終了は、失敗結果を確定した後に 1 回だけ通知する。
- 1 つの TUI process 内の各 turn を区別する。
- 同じ turn の callback を複数回受け取った場合も、同じ Windows toast を重複表示しない。
- turn の識別と重複排除は、その TUI process invocation 内に閉じる。

## 通知内容

### 必須情報

各通知には、次の情報を含める。

- サブコマンド名
- repository を識別できる短い情報
- 状態

### 内容の制限と裁量

- terminal result の通知には、経過時間を含めてよい。
- prompt、assistant の回答本文、秘密情報、フルパス、および Windows の通知履歴へ残す必要がない情報を含めてはならない。
- `{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` のパス表示規則は、Windows toast の通知内容には適用しない。
- 具体的な文面、表示形式、および repository を識別する短い情報の導出方法は、この節の境界を守る範囲で realization の裁量とする。

## 決定論的な発火と Codex CLI の設定境界

- 通知の要否は、prompt、assistant の回答、または installed skill に判断させてはならない。
- cmoc のサブコマンド lifecycle event と、cmoc が起動した Codex process の lifecycle event から決定論的に発火する。
- cmoc が起動する Codex CLI について、通知に関する effective configuration は呼び出し単位で cmoc が決定する。
- `codex exec` では、agent turn 完了の通知 callback を無効にする。
- TUI では、agent turn 完了を検出する callback を、その TUI process にだけ設定する。
- 通知を設定するために、`$CODEX_HOME/config.toml` を生成または変更してはならない。

## 実装前に検証する Codex CLI の外部契約

現行 oracle は、Codex CLI の通知 callback に関する具体的な interface を定義しない。

realization の実装前に、利用中の Codex CLI で次の外部契約を検証する。

- callback を呼び出し単位で設定または無効化する設定 key
- callback event の種類、payload、および同じ turn の重複を識別するために利用できる情報
- 対話型 TUI の各 agent turn が完了し、人間の入力待ちになった時点で callback が発火する保証

### 未検証 interface の扱い

- 検証結果を得る前に、特定の設定 key、event 名、payload 形式、または発火保証を正本仕様として断定してはならない。
- 必要な callback を利用できない場合も、TUI 出力の解析または agent や installed skill への委譲を fallback として追加してはならない。

## Windows toast transport

- Windows 11 上の WSL2 から Windows toast を表示する。
- 外部 PowerShell module または新しい Python package を必須依存にしてはならない。
- 通知内容は、shell 文字列の組み立てに依存せず、データとして安全に transport へ渡す。
- 通知処理には有限の上限時間を設け、本命処理を長時間待たせてはならない。
- transport の欠落、起動失敗、または toast 表示失敗によって、サブコマンドの終了コード、run state、成果物、retry、または成功判定を変更してはならない。
- 通知失敗を理由に、Codex call またはサブコマンドを再実行してはならない。
- transport の具体方式と上限時間は、この節の境界を守る範囲で realization の裁量とする。

## 自動補完プローブ

- `_CMOC_COMPLETE` が環境変数として存在する呼び出しでは、通知処理を初期化または実行してはならない。
- 自動補完プローブでは、transport の利用可能性を検査してはならない。
- 自動補完プローブでは、通知に関する warning を stdout または stderr へ出力してはならない。

## non-goal

今回の仕様では、次の機能を要求しない。

- agent turn の途中にある tool approval または追加承認要求の通知
- toast のクリックによる terminal focus、action button、sound、または表示時間のカスタマイズ
- prompt または assistant の回答本文の toast 表示
- repository 設定から任意の host command を実行する仕組み
- 通知履歴または永続的な通知 state の新設
- Windows 以外の desktop notification 対応
