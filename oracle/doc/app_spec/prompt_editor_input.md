# プロンプトのエディタ入力

- cmoc がエディタを起動して、そこにユーザーがプロンプトを入力する
- 起動するエディタは (高優先度) `code` --> `nano` --> `vim` --> `vi` (低優先度) の順でフォールバックする
- `code` で起動する場合は必ず `--wait` を付けること
- エディタの編集対象は `{{repo-root}}/.cmoc/gu/ar/log/editor_input/{{time-stamp}}_orig.md` とする
- 編集対象の初期値は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/editor_input.py` の `build_prompt_editor_input_initial_text` で構築する
- 呼び出し元は、cmoc が自動注入するサブコマンド固有の指示を `automatically_injected_instruction` に渡す
- `automatically_injected_instruction` の具体的な文面と追加内容は realization file 側の実装裁量とする
- エディタから cmoc に処理が戻ってきたらユーザー入力完了とみなす
- 編集対象からのプロンプト読み出しは以下の挙動とする
    - コメント `<!-- ... -->` は削除
    - 前後の空白文字は除去 (`strip`)
