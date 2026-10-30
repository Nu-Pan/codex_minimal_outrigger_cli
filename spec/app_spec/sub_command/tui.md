
# `cmoc tui` サブコマンド

## 概要

cmoc は、ユーザーから与えられたプロンプトへ cmoc 固有の契約を注入し、AI Agent CLI/TUI を起動する。注入する cmoc 基本規定は、適用条件を伴う固定の内容とし、installed skill の有無にかかわらず解釈できるものにする。実行パラメータまたは注入規定を選定するための agent call は行わない。

本コマンドは汎用 TUI の新規起動を行う。後日の Codex 会話の再開は、`{{cmoc-root}}/spec/app_spec/sub_command/resume.md` の「目的と公開入口」「対象の適格性と会話選択」「workload と起動環境の保持」に従う。

## 引数

- なし

## 事前条件

- git working tree と staging area が clean であることを事前条件にせず、いずれかに未コミット差分が存在しても実行する

## 実行手順

1. doctor preprocess を呼び出す
2. prompt editor input の lifecycle に従って、オリジナルプロンプトをユーザーから受け取る
3. `build_tui_request` で起動パラメータを構築する
4. 構築した起動パラメータで AI Agent CLI/TUI を起動する。Codex CLI では、下記の「Codex CLI の場合」に従い、初回 exec の成功・終了を確認して同じ会話の TUI へ自動移行する

## ユーザー指示の入力

- エディタ入力の仕組みは、`{{cmoc-root}}/spec/app_spec/prompt_editor_input.md` の「プロンプトのエディタ入力」を正本とする

## 「AI Agent CLI/TUI を起動」の詳細

### 全バックエンド共通

- `build_tui_request` が返したパラメータを変更せずに使う。具体的な起動経路はバックエンドの規約に従う
- 汎用 TUI の意味上の責務と新規起動条件は本書を正本とする。正確な prompt part の選択、文面、および workload 固有の新規起動・再開パラメータの構築は、`{{cmoc-root}}/reference/src/oracle/request_builder/tui/launch_tui.py` の `build_tui_request` へ委譲する
- cmoc の基本規定は、各規定が明示する適用条件に該当する場合だけ、オリジナルプロンプトの作業へ適用する
- TUI へ注入する基本規定の意味仕様は、次の文書を正本とする
    - oracle file と realization file の責務: `{{cmoc-root}}/spec/app_spec/cmoc_basic_instruction.md` の「oracle file と realization file の責務」
    - oracle file に対する realization file の適合性: `{{cmoc-root}}/spec/app_spec/cmoc_basic_instruction.md` の「oracle file に対する realization file の適合性」
- installed skill は任意の追加規定として利用してよいが、cmoc 固有契約と競合する場合は cmoc 固有契約を優先する
- 共通 feedback instruction、各 process の collector context、および accepted observation の保持は、`{{cmoc-root}}/spec/app_spec/feedback_observation.md` の「feedback observation の収集」に従う
- このサブコマンドの初回処理完了・応答完了と終了時の Windows toast 通知は、`{{cmoc-root}}/spec/app_spec/windows_toast_notification.md` の「TUI の通知境界」を正本とする

### Codex CLI の場合

- `{{cmoc-root}}/spec/app_spec/codex_tui_rule.md` の「新規起動の二段階実行」に従う。新規入力の builder が返す完全 prompt とパラメータは初回 exec に使い、成功後は同じ builder に検査済み再開入力を渡して、初期 prompt のない TUI 起動パラメータを構築する
- editor input handoff は初回 exec と TUI の両方で提供する。共通の意味は、`{{cmoc-root}}/spec/app_spec/editor_input_handoff.md` の「editor input handoff」を正本とする
- 送信元情報の確定と MCP への供給は、`{{cmoc-root}}/spec/app_spec/codex_common_rule.md` の「editor input handoff MCP」に従う
- 共通呼び出し規約は、`{{cmoc-root}}/spec/app_spec/codex_common_rule.md` の「Codex CLI 共通呼び出し規約」に従う
- 管理対象の会話 ID は、`{{cmoc-root}}/spec/app_spec/codex_tui_rule.md` の「TUI の固定 session ID」に従う
