# editor input handoff

## 概要

editor input handoff は、Codex TUI の agent が、別の prompt editor input で待機中の editor work file へ完成済み内容を渡す共通機能である。agent は `cmoc_editor_input.overwrite` を呼び出し、cmoc が対象 file 全体を上書きする。

この機能は、agent による `aw` ツリーへの通常の直接書き込みを禁止しない。

## goal

- 人間が指定した active target だけへ内容を渡す。
- editor work file 全体の単純な上書きだけを MCP 経由で行う。
- handoff の有無にかかわらず、file access mode、Codex sandbox、および prompt editor input の最終確定方法を維持する。

## 正本の分担

- prompt editor input の writer 境界と最終読み取りは、`{{cmoc-root}}/oracle/doc/app_spec/prompt_editor_input.md` を正本とする。
- Codex TUI への MCP と handoff instruction の注入は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「editor input handoff MCP」を正本とする。
- `cmoc_editor_input.overwrite` の正確な input schema は、`{{cmoc-root}}/oracle/src/oracle/editor_input_handoff/overwrite_input.json` の root schema（JSON Pointer `#`）へ委譲する。
- handoff instruction の正確な文面は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/policy/editor_input_handoff.py` の `build_editor_input_handoff_policy` へ委譲する。

## handoff target

- prompt editor input は、editor work file の生成後かつ editor の起動前に、opaque な target ID を持つ target を登録し、その ID を人間へ表示する。
- target は editor の待機中だけ submission を受け付ける。
- editor から処理が戻った後は、新規受付を停止し、受付済みの submission を完了させて target を無効にしてから、editor work file を最終読み取りする。
- target の登録と routing は一時的な runtime state とする。target 一覧、handoff 履歴、永続的な active state、および排他的 editor lock は設けない。

## MCP interface と上書き

agent-facing MCP interface は `cmoc_editor_input.overwrite` だけとする。target の探索、file read、汎用 file write、command 実行、MCP resource、および MCP prompt は提供しない。

- tool input は target ID と editor work file 全体の新しい内容を指定する。
- cmoc は target が active であり、呼び出し元と同じ repository に属することを検証する。
- cmoc は対象が所定の editor work directory 内にある regular file かつ非 symlink であることを、上書きのたびに検証する。
- accepted submission は file 全体を単純に置換する。同じ target への accepted submission は直列化し、最後に適用した内容を残す。
- accepted 後も人間または agent が直接編集できる。editor 終了後の最終読み取り結果を確定入力とする。
- tool は submission の成否を返し、result または log に content 本文を複製しない。

append、merge、patch、差分適用、既存内容との conflict 判定、および optimistic concurrency は行わない。

## agent の責務と権限

- agent は、人間が active target への handoff を明示的に要求し、target ID を提示した場合だけ tool を使用する。
- handoff のために sandbox、network access、permission profile、または file access mode を変更してはならない。
- tool を利用できない場合や submission が拒否された場合に、handoff の代替として editor work file へ直接書き込んだり、sandbox escalation を要求したりしてはならない。この禁止は handoff の代替手段だけに適用し、`aw` ツリーへの通常の agent write を制限しない。
- handoff の成否にかかわらず、agent call が要求する正式な回答または成果物を満たす。handoff に失敗した場合は成功と報告せず、必要なら手動で利用できる完成済み内容を回答へ残す。

## non-goal

- target の自動発見または自動選択
- editor の自動保存、終了、または排他的 writer 管理
- `aw` ツリーへの一般的な agent write の禁止
- Codex TUI 以外への handoff MCP または handoff instruction の注入
