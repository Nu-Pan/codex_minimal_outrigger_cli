# editor input handoff

## 概要

editor input handoff は、Codex TUI の agent が、別の prompt editor input で待機中の editor work file へ依頼を渡す共通機能である。agent は `cmoc_editor_input.overwrite` に項目別の内容を渡し、handoff 用 local MCP が送信元情報と合成して対象 file 全体を上書きする。

## goal

- 人間が指定した active target だけへ内容を渡す。
- agent が自由記述の内容を担い、MCP が本文の形式と機械的な情報の注入を担う。
- editor work file 全体の単純な上書きだけを MCP 経由で行う。
- 受信側が送り元の実行中でも依頼を理解して作業を開始できるよう、必要なコンテキストと送信元情報を本文で渡す。
- handoff の有無にかかわらず、file access mode、Codex sandbox、および prompt editor input の最終確定方法を維持する。

## 正本の分担

- prompt editor input の writer 境界と最終読み取りは、`{{cmoc-root}}/oracle/doc/app_spec/prompt_editor_input.md` の「ファイルの役割」と「editor input の確定手順」を正本とする。
- agent の直接編集禁止と MCP の書き込み例外は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「詳細なファイルアクセス制限」と「書き込み主体の責任分界」に従う。
- Codex TUI への MCP と handoff instruction の注入は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「editor input handoff MCP」を正本とする。
- 送信元情報の記録と保存済みログへの到達は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「TUI 送信元情報の記録」を正本とする。
- `cmoc_editor_input.overwrite` の正確な field 名、型、必須条件、および空値・省略の受理条件は、`{{cmoc-root}}/oracle/src/oracle/editor_input_handoff/overwrite_input.json` の root schema（JSON Pointer `#`）へ委譲する。
- handoff instruction の正確な文面は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/policy/editor_input_handoff.py` の `build_editor_input_handoff_policy` へ委譲する。
- 送信元情報の正確なデータ構造と値の検査は、`{{cmoc-root}}/oracle/src/oracle/editor_input_handoff/body.py` の `EditorInputHandoffSource` へ委譲する。
- handoff 本文の正確な見出し、順序、項目の表記、空項目の扱い、および送信元情報の配置は、`{{cmoc-root}}/oracle/src/oracle/editor_input_handoff/body.py` の `build_editor_input_handoff_body` へ委譲する。
- 文書参照の Python データ構造と値の検査、単一参照のインライン表記、および複数参照の一覧表記は、`{{cmoc-root}}/oracle/src/oracle/other/doc_ref_model.py` の `DocRef`、`render_doc_ref_as_inline_md`、および `render_doc_ref_as_multiline_md` へ委譲する。意味は本書の「参照情報」で定める。

## handoff target

- prompt editor input は、editor work file の生成後かつ editor の起動前に、opaque な target ID を持つ target を登録し、その ID を人間へ表示する。
- target は editor の待機中だけ submission を受け付ける。
- editor から処理が戻った後は、次の順に処理する。
    1. submission の新規受付を停止する。
    2. 受付済みの submission を完了させる。
    3. target を無効にする。
    4. editor work file を最終読み取りする。
- target の登録と routing は一時的な runtime state とする。target 一覧、handoff 履歴、永続的な active state、および排他的 editor lock は設けない。

## MCP interface と上書き

agent-facing MCP interface は `cmoc_editor_input.overwrite` だけとする。target の探索、file read、汎用 file write、command 実行、MCP resource、および MCP prompt は提供しない。

- tool input には、人間が提示した target ID と、本書の「agent の責務と権限」で定める項目別の内容を指定する。送信元情報と完成済み Markdown 全文は入力項目に含めない。
- cmoc は target が active であり、呼び出し元と同じ repository に属することを検証する。
- cmoc は対象が所定の editor work directory 内にある regular file かつ非 symlink であることを、上書きのたびに検証する。
- MCP は input schema に適合する入力と、呼び出し元の送信元情報を使い、本書の「本文の生成」に従って本文を構築する。参照情報は本書の「参照情報」に従って型付きの値へ変換する。入力・参照情報・target・送信元情報の検証または本文生成に失敗した場合は上書きせず、失敗を返す。
- accepted submission は生成した本文で file 全体を単純に置換する。同じ target への accepted submission は直列化し、最後に適用した内容を残す。
- tool は上書きが完了した場合だけ成功を返す。tool result または handoff 処理の log に、自由記述の入力や生成した本文を複製しない。検証エラーにもこれらの内容を含めない。

append、merge、patch、差分適用、既存内容との conflict 判定、および optimistic concurrency は行わない。

## 本文の生成

- MCP は委譲先の本文 builder を使用し、同じ項目別入力と送信元情報から同じ本文を生成する。realization 側で固定文面を独自に構築しない。
- 項目別の自由記述、参照情報、および送信元情報を区分する。
- 本文は Markdown として生成し、コメント開始記号の置換は行わない。生成後の HTML コメントの扱いは、`{{cmoc-root}}/oracle/doc/app_spec/prompt_editor_input.md` の「editor input の確定手順」に従う。
- builder は自由記述の意味を補完・要約せず、送信元情報を推定しない。
- 本文の生成と機械的な注入は editor work file の上書き時に完結させる。その後は既存の editor input 確定手順へ渡し、確定した `AgentCallParameter.prompt` を加工しない。

## agent の責務と権限

- agent は、人間が active target への handoff を明示的に要求し、target ID を提示した場合だけ tool を使用する。
- agent は、依頼する目標状態、実行してほしい作業、意図・背景、決定事項とその理由、および未確定事項を、それぞれ空白だけではない自由記述として作成する。送り元の会話を読まなくても依頼を理解できる内容とする。
- 該当する内容がない場合や未確認の場合も、その状態を記述する。存在しない経緯や決定を補わない。
- 関連する oracle の選定と参照箇所の特定は agent が担い、本書の「参照情報」に従って渡す。参照先の簡潔な内容と参照理由は、依頼や背景の自由記述に含める。
- 引き渡す必要のある内容は HTML コメントの外に記述する。
- agent は本文全体の見出し・配置・参照表記を完成させる必要はなく、送信元情報の取得や転記も行わない。自由記述内部の文章量や表現の細部は固定しない。
- agent は editor work file へ直接書き込まない。
- handoff のために sandbox、network access、permission profile、または file access mode を変更してはならない。
- tool を利用できない場合や submission が拒否された場合に、handoff の代替として sandbox escalation を要求してはならない。
- tool の結果を正確に報告し、handoff の成否にかかわらず、agent call が要求する正式な回答または成果物を満たす。失敗時は、必要なら agent が作成した依頼・コンテキスト部分を手動利用できる形で回答へ残す。MCP が注入する送信元情報を含めた同一の完成済み全文の再構築は求めない。

## 参照情報

文書参照は、実行時の参照先ファイルと、そのファイル内の参照箇所を表す。参照箇所には、見出しや識別子など、検索で参照元を逆引きできる安定した locator を使い、行番号を使わない。ファイル全体を参照する場合は、箇所の指定がないことを表す。

handoff では、作業に必要な oracle の文書参照を配列で渡し、参照がなければ空配列とする。参照先は絶対パスで指定する。MCP は入力のパス文字列を `Path` に変換し、参照箇所とともに `DocRef` を構築して本文 builder に渡す。これは実行時の入力形式であり、oracle file 自体に記載する正本間参照の形式は、`{{cmoc-root}}/oracle/doc/app_spec/oracle_and_realization.md` の「oracle file を扱う判断基準」に従う。

## 送信元情報

送信元情報は、handoff を行う TUI process と、それを起動した cmoc の実行を識別する次の値とする。

- 送信元のサブコマンド名
- その invocation を識別する既存の実行 ID
- 送信元 TUI process に対応する既存の Codex call ID
- 対応する診断用サブコマンドログのフルパス

cmoc は実際の呼び出しに付与・保持する値を、送信側 TUI process に結び付いた MCP の呼び出し元コンテキストへ供給する。MCP はこの情報を本文 builder に渡す。送信元情報を転記用 prompt または tool input として agent に渡さず、handoff 専用の ID 体系は作らない。

並行する TUI process 間でコンテキストを取り違えず、同じ送信側 TUI process の各 turn では、その process に対応する実行情報を使用する。受信先 target の情報から送信元を推定せず、target ID と送信元の識別子を相互に代用しない。必要な送信元情報を取得できない場合は、推測・捏造で補わず handoff の失敗を返す。

起動・呼び出し管理経路からの供給と準備順序は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「editor input handoff MCP」に従う。内部 transport や module の分割は、本書の責務と lifecycle を満たす範囲で実装に委ねる。

## non-goal

- target の自動発見または自動選択
- editor の自動保存、終了、または排他的 writer 管理
- Codex TUI 以外への handoff MCP または handoff instruction の注入
