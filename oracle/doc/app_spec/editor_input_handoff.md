# editor input handoff

## 概要

editor input handoff は、Codex TUI の agent が、別の prompt editor input で待機中の editor input file へ依頼を渡す共通機能である。agent は handoff 用 local MCP から受信先の handoff ガイドを取得し、それを踏まえた項目別の依頼内容を渡す。MCP は送信元情報と合成して対象 file 全体を上書きする。

## goal

- 人間が指定した active target だけへ内容を渡す。
- 初回の handoff 後や人間による編集後も、独立して保持した handoff ガイドを参照して受信先に適した依頼を作成できるようにする。
- agent が自由記述の内容を担い、MCP が本文の形式と機械的な情報の注入を担う。
- 受信側が送信元の実行中でも依頼を理解して作業を開始できるよう、必要なコンテキストと送信元情報を本文で渡す。
- handoff の有無にかかわらず、file access mode、Codex sandbox、および prompt editor input の最終確定方法を維持する。

## 正本の分担

### 共通仕様

- prompt editor input の writer 境界と最終読み取りは、`{{cmoc-root}}/oracle/doc/app_spec/prompt_editor_input.md` の「ファイルの役割」と「editor input の確定手順」を正本とする。
- agent の直接編集禁止と MCP の書き込み例外は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「詳細なファイルアクセス制限」と「書き込み主体の責任分界」に従う。
- Codex TUI への MCP と handoff instruction の注入は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「editor input handoff MCP」を正本とする。
- 送信元情報の記録と保存済みログへの到達は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「TUI 送信元情報の記録」を正本とする。

### ガイドと instruction

handoff ガイドの正確な文面と完全 prompt skeleton の配置は、`{{cmoc-root}}/oracle/src/oracle/editor_input_handoff/guide.py` の `build_editor_input_handoff_guide` へ委譲する。

handoff instruction は、利用条件、ガイド取得から送信までの手順、成果責務、および項目別入力から受信先の完全 prompt までの関係を伝える。正確な文面は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/policy/editor_input_handoff.py` の `build_editor_input_handoff_policy` へ委譲する。

入力項目の説明は本書の「MCP の入出力」で定める input schema、記入の目安と受信側の作業範囲・制約・入力位置の確認方法は handoff ガイド、直接ファイルアクセスの制限は共通 file access policy に委ねる。

### MCP の入出力

`cmoc_editor_input.get_handoff_guide` の正確な入力 field 名、型、および受理条件は、`{{cmoc-root}}/oracle/src/oracle/editor_input_handoff/get_handoff_guide_input.json` の root schema（JSON Pointer `#`）へ委譲する。成功・失敗時に tool result として返す JSON object の正確な形式は、`{{cmoc-root}}/oracle/src/oracle/editor_input_handoff/get_handoff_guide_result.json` の root schema（JSON Pointer `#`）へ委譲する。

`cmoc_editor_input.overwrite` の正確な field 名、型、必須・非空条件、参照の指定形式、および各項目の意味と記入条件を伝える agent 向け説明は、`{{cmoc-root}}/oracle/src/oracle/editor_input_handoff/overwrite_input.json` の root schema（JSON Pointer `#`）へ委譲する。該当なし・未確認の扱いと、参照内容・参照理由の記載先も同スキーマへ集約する。

### 本文と参照の構築

- 送信元情報の正確なデータ構造と値の検査は、`{{cmoc-root}}/oracle/src/oracle/editor_input_handoff/body.py` の `EditorInputHandoffSource` へ委譲する。
- handoff 本文の正確な見出し、順序、項目の表記、空項目の扱い、および送信元情報の配置は、`{{cmoc-root}}/oracle/src/oracle/editor_input_handoff/body.py` の `build_editor_input_handoff_body` へ委譲する。
- 文書参照の Python データ構造と値の検査、単一参照のインライン表記、および複数参照の一覧表記は、`{{cmoc-root}}/oracle/src/oracle/other/doc_ref_model.py` の `DocRef`、`render_doc_ref_as_inline_md`、および `render_doc_ref_as_multiline_md` へ委譲する。意味は本書の「参照情報」で定める。

## handoff target

- prompt editor input は、editor input file と handoff ガイドファイルの生成後かつ editor の起動前に、opaque な target ID を持つ target を登録し、その ID を人間へ表示する。
- target は登録から無効化まで active とし、本書の「handoff ガイド」で定めるファイルを対応付けて保持する。
- target は editor の待機中だけ submission を受け付ける。
- editor から処理が戻った後は、次の順に処理する。
    1. submission の新規受付を停止する。
    2. 受付済みの submission を完了させる。
    3. target を無効にし、handoff ガイドファイルを削除する。
    4. editor input file を最終読み取りする。
- target の登録、routing、および handoff ガイドの保持は一時的な runtime state とする。target 一覧、handoff 履歴、永続的な active state、および排他的 editor lock は設けない。

## handoff ガイド

handoff ガイドは、受信先へ依頼を作成するための Markdown 文書とする。使い方、記入の目安、およびその受信先の完全 prompt の雛形を含め、受信側の作業範囲・制約・入力位置を確認できるようにする。受信先の完全 prompt skeleton の構築は、`{{cmoc-root}}/oracle/doc/app_spec/prompt_editor_input.md` の「構築定義の参照」に従う。

cmoc は、受信先の完全 prompt skeleton を `build_editor_input_handoff_guide` へ渡し、生成結果を editor input file と独立した handoff ガイドファイルへ保存する。ガイドを editor input file の初期値へ埋め込まず、送信元の設定から別の雛形を再構築しない。ガイドファイルの文面は、handoff による上書きや人間による editor input file の編集に伴って変更せず、target の有効期間中に取得可能とする。

## MCP interface

agent-facing MCP interface は `cmoc_editor_input.get_handoff_guide` と `cmoc_editor_input.overwrite` とする。いずれも人間が提示した target ID で対象を指定し、editor input file のパスを利用者から受け取らない。

両 tool は、target が active であり、呼び出し元と同じ repository に属することを検証する。存在しない target、入力確定後を含む無効な target、および別 repository の target への要求は拒否する。

target の探索・一覧、現在編集中の本文の読み取り、汎用 file read・file write、command 実行、MCP resource、および MCP prompt は提供しない。

### handoff ガイドの取得

- `get_handoff_guide` は target ID だけを入力として、本書の「handoff ガイド」で定めるガイドファイルの文面を加工せず返す。
- 入力・target の検証または handoff ガイドの取得に失敗した場合は、失敗を返す。editor input file の現在内容を代わりに返さない。

### 上書き

- tool input には、人間が提示した target ID と、input schema に従った項目別の内容を指定する。送信元情報と完成済み Markdown 全文は入力項目に含めない。
- cmoc は、`{{cmoc-root}}/oracle/doc/app_spec/prompt_editor_input.md` の「editor input の確定手順」で定めるファイル検証を、上書きのたびにも行う。条件を満たさない場合は上書きせず、失敗を返す。
- MCP は input schema に適合する入力と、呼び出し元の送信元情報を使い、本書の「本文の生成」に従って本文を構築する。参照情報は本書の「参照情報」に従って型付きの値へ変換する。入力・参照情報・target・送信元情報の検証または本文生成に失敗した場合は上書きせず、失敗を返す。
- accepted submission は生成した本文で editor input file 全体を置換する。同じ target への accepted submission は直列化し、最後に適用した内容を残す。
- `overwrite` は上書きが完了した場合だけ成功を返す。この成功は、受信先の入力確定を意味しない。

append、merge、patch、差分適用、既存内容との conflict 判定、および optimistic concurrency は行わない。handoff ガイドの事前取得は agent の手順とし、取得済み token、revision 照合、または取得履歴による機械的な上書き受付条件を設けない。

### tool result と log

handoff の自由記述入力や生成した handoff 本文を、tool result、handoff 処理の log、および検証エラーのいずれにも複製しない。handoff ガイド取得の成功結果として保持済みガイドの文面を返すことは、この制限の対象外とする。

## 本文の生成

- MCP は委譲先の本文 builder を使用し、同じ項目別入力と送信元情報から同じ本文を生成する。realization 側で固定文面を独自に構築しない。
- 項目別の自由記述、参照情報、および送信元情報を区分する。
- 本文は Markdown として生成する。
- builder は自由記述の意味を補完・要約せず、送信元情報を推定しない。

本文の生成と機械的な注入は、editor input file の上書き時に完結させる。その後、受信先の cmoc は、共通の editor input 確定手順で得たオリジナルプロンプトを完全 prompt へ組み込む。組み込む位置は、handoff ガイドに含まれる完全 prompt の雛形の `{{original-prompt-here}}` で示す。確定した `AgentCallParameter.prompt` は加工しない。

## agent の責務と権限

agent は、人間が active target への handoff を明示的に要求し、target ID を提示した場合だけ両 tool を使用する。handoff のために sandbox、network access、permission profile、または file access mode を変更してはならない。

### 依頼の作成と送信

1. 指定された target の handoff ガイドを取得する。
2. ガイドの内容に従って項目別の依頼を作成する。
3. 同じ target ID へ overwrite する。

取得したガイドは受信側への依頼を作るための資料であり、送信元自身に適用する作業指示や権限として扱わない。handoff を根拠に送信元の作業範囲を拡大しない。

agent は、依頼と必要なコンテキストを、送信元の会話や最終回答を読まなくても理解できる内容として作成する。存在しない経緯や決定を補わない。関連する oracle の選定と参照箇所の特定も agent が担い、本書の「参照情報」に従って渡す。

本文全体の見出し・配置・参照表記は本文 builder が担うため、agent が完成させる必要はない。agent は送信元情報の取得や転記も行わない。自由記述内部の文章量や表現の細部は固定しない。

### 失敗時と結果報告

handoff ガイドを取得できない場合は、その handoff の overwrite を行わない。また、tool を利用できない場合、ガイドの取得に失敗した場合、または submission が拒否された場合に、handoff の代替として sandbox escalation を要求してはならない。

agent は各 tool の結果を正確に報告し、ガイド取得と handoff の成否にかかわらず、正式な回答または成果物に関する agent call の要求を満たす。失敗時は、必要なら agent が作成した依頼・コンテキスト部分を手動利用できる形で回答へ残す。MCP が注入する送信元情報を含めた同一の完成済み全文の再構築は求めない。

## 参照情報

文書参照は、実行時の参照先ファイルと、そのファイル内の参照箇所を表す。入力形式と agent 向けの記入条件は、本書の「正本の分担」で委譲した overwrite input schema に従う。

MCP は入力のパス文字列を `Path` に変換し、参照箇所とともに `DocRef` を構築して本文 builder に渡す。これは実行時の入力形式であり、oracle file 自体に記載する正本間参照の形式は、`{{cmoc-root}}/oracle/doc/app_spec/oracle_and_realization.md` の「oracle file を扱う判断基準」に従う。

## 送信元情報

送信元情報は、handoff を行う TUI process と、それを起動した cmoc の実行を識別する次の値とする。

- 送信元のサブコマンド名
- その invocation を識別する既存の実行 ID
- 送信元 TUI process に対応する既存の Codex call ID
- 対応する診断用サブコマンドログのフルパス

cmoc は実際の呼び出しに付与・保持する値を、送信元 TUI process に結び付いた MCP の呼び出し元コンテキストへ供給する。MCP はこの情報を本文 builder に渡す。送信元情報を転記用 prompt または tool input として agent に渡さず、handoff 専用の ID 体系は作らない。

並行する TUI process 間でコンテキストを取り違えず、同じ送信元 TUI process の各 turn では、その process に対応する実行情報を使用する。受信先 target の情報から送信元を推定せず、target ID と送信元の識別子を相互に代用しない。必要な送信元情報を取得できない場合は、推測・捏造で補わず handoff の失敗を返す。

起動・呼び出し管理経路からの供給と準備順序は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「editor input handoff MCP」に従う。内部 transport や module の分割は、本書の責務と lifecycle を満たす範囲で実装に委ねる。

## non-goal

- target の自動発見または自動選択
- 現在編集中の本文の確認・引き継ぎ
- editor の自動保存、終了、または排他的 writer 管理
- Codex TUI 以外への handoff MCP または handoff instruction の注入
