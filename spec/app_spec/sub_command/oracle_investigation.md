# `cmoc oracle investigation`

## 概要

cmoc は、oracle file に関するユーザーの調査指示をエディタから受け取り、初回 exec で調査を実行し、成功後に同じ会話の Codex CLI の TUI を起動する。agent は oracle file を根拠に調査し、初回の回答を含む調査結果は TUI でユーザーが確認できるようにする。

本コマンドは oracle 調査 TUI の新規起動を行う。後日の会話の再開は、`{{cmoc-root}}/spec/app_spec/sub_command/resume.md` の「目的と公開入口」「対象の適格性と会話選択」「workload と起動環境の保持」に従う。

## 引数

- なし

## 事前条件

- このサブコマンド固有の事前条件はない

## 実行手順

1. doctor preprocess を呼び出す
2. prompt editor input の lifecycle に従って、oracle file に関するユーザーの調査指示を受け取る
3. `build_oracle_investigation_request` で完全 prompt と初回 exec 用のパラメータを構築する
4. 下記の「Codex CLI の起動」に従い、初回 exec の成功・終了を確認して同じ会話の TUI へ自動移行する

## ユーザー指示の入力

- エディタ入力の仕組みは、`{{cmoc-root}}/spec/app_spec/prompt_editor_input.md` の「プロンプトのエディタ入力」を正本とする

## TUI 起動パラメータ

- oracle 調査 TUI の意味上の責務と調査境界は本書を正本とする。正確な prompt 文面、prompt part の選択、および workload 固有の新規起動・再開パラメータの構築は、`{{cmoc-root}}/reference/src/oracle/acp_builder/oracle/investigation/launch_tui.py` の `build_oracle_investigation_request` へ委譲する
- 初回 exec と TUI の両方で editor input handoff を提供する。共通の意味は、`{{cmoc-root}}/spec/app_spec/editor_input_handoff.md` の「editor input handoff」を正本とする
- 送信元情報の確定と MCP への供給は、`{{cmoc-root}}/spec/app_spec/codex_common_rule.md` の「editor input handoff MCP」に従う
- `build_oracle_investigation_request` が返したパラメータを変更せずに使う。新規入力は初回 exec 用とし、成功後は同じ builder に検査済み再開入力を渡して、初期 prompt のない TUI 起動パラメータを構築する
- oracle file を扱う判断基準は `{{cmoc-root}}/spec/app_spec/cmoc_basic_instruction.md` の「oracle file を扱う判断基準」を正本とする。正確な agent 向け文面は前述の builder を参照する
- 実行パラメータ決定用の agent call は行わない

## Codex CLI の起動

- `{{cmoc-root}}/spec/app_spec/codex_tui_rule.md` の「新規起動の二段階実行」に従う
- 共通呼び出し規約は、`{{cmoc-root}}/spec/app_spec/codex_common_rule.md` の「Codex CLI 共通呼び出し規約」に従う
- 管理対象の会話 ID は、`{{cmoc-root}}/spec/app_spec/codex_tui_rule.md` の「TUI の固定 session ID」に従う
- このサブコマンドの初回処理完了・応答完了と終了時の Windows toast 通知は、`{{cmoc-root}}/spec/app_spec/windows_toast_notification.md` の「TUI の通知境界」を正本とする

## 調査結果と変更の扱い

- 調査結果は Codex CLI の TUI でユーザーへ回答する
- 人間が editor input handoff を要求した場合の本文と回答の責務は、`{{cmoc-root}}/spec/app_spec/editor_input_handoff.md` の「agent の責務と権限」に従う
- 調査結果の根拠となる oracle file を、回答から特定できるようにする
- 調査結果の自然言語部分は原則として日本語とする。識別子、path、command、log 原文、および引用は元の表記を維持してよい
- 初回 exec と TUI のどちらの agent も、oracle file を変更せず、realization file を読み書きしない
- 一時作業領域の利用は、`{{cmoc-root}}/spec/app_spec/codex_common_rule.md` の「一時作業領域」に従う
- Codex CLI の TUI は oracle file の変更結果を自動 commit しない
- 文書検索の提供は、`{{cmoc-root}}/spec/app_spec/codex_common_rule.md` の「文書検索 MCP」に従う
