# `cmoc oracle edit fork`

## 目的

- oracle file の最終状態に関するユーザー指示を受け取り、隔離された編集 run で oracle file へ反映する workload である。
- fork, join, abandon の共通 lifecycle は `{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` を正本とする。

## 引数

- 引数なし。

## ユーザー指示の入力

- エディタ入力の仕組みは `{{cmoc-root}}/oracle/doc/app_spec/prompt_editor_input.md` を正本とする。
- エディタ編集対象 file の初期値へ、以下の workload 固有コメントを追加注入する。

    ```markdown
    <!--
    以下の指示は cmoc が自動注入するため、この file に書いてはいけない。

    - realization file の読み書き禁止
    - oracle file の規約・規範
    - TODO
    -->
    ```

## agent call と file access

- `build_oracle_edit_fork_launch_exec_parameter` が、ユーザー指示を含む完全 prompt を `AgentCallParameter.prompt` として直接返す。
- `{{cmoc-run-worktree}}` を cwd とする `codex exec` を 1 回だけ本命 agent call として実行する。Codex CLI の TUI は起動しない。
- 実行パラメータ決定用の追加 agent call は行わない。
- file access mode は `PURE_ORACLE_WRITE` とし、agent は oracle file だけを変更する。
- Codex CLI の共通実行規則は `{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` を正本とする。

## 想定内差分

- agent が変更する oracle file。
- cmoc が生成する任意階層の `INDEX.md`。
- agent は `INDEX.md` を変更せず、cmoc が生成する。

## 実行手順

1. doctor preprocess と編集 run の共通事前条件検査を行う。
2. oracle file の最終状態に関するユーザー指示をエディタから受け取る。
3. 編集 run の共通 fork 開始処理を行う。
4. `build_oracle_edit_fork_launch_exec_parameter` で AgentCallParameter を構築する。
5. その AgentCallParameter を変更せず、`{{cmoc-run-worktree}}` を cwd とする `codex exec` で実行する。
6. agent の oracle file 差分と cmoc が生成した `INDEX.md` を検査し、run branch に commit する。
7. `run.state` を `joinable` にして結果を report する。

## エラー

- 本命 agent call を正常に開始または終了できない場合、差分を整合した単位へ commit または rollback できない場合、あるいは後処理に失敗した場合は `run.state` を `error` にする。
- エラー後は `cmoc run join` で確定済み成果物を取り込むか、`cmoc run abandon` で run を破棄する。

## fork report と終了コード

- report は Markdown + YAML Front Matter とする。
- 共通 run 項目に加え、Codex CLI の終了結果と変更 path を含める。
- AI による意味的な変更要約は生成しない。
- `{{repo-root}}/.cmoc/gu/ar/report/oracle/edit/fork/{{time-stamp}}.md` に保存する。report 本文は stdout に流さず、保存先のフル path を表示する。
- `joinable` での終了は終了コード 0、`error` での終了は非 0 とする。

## join 後 hook

- workload 固有の hook は持たない。
