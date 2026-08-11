# プロンプトのエディタ入力

## 概要

- cmoc は、後続の AI Agent 呼び出しに渡す完全プロンプトの skeleton をエディタへ提示する。
- ユーザーは、HTML コメントブロックの外にオリジナルプロンプトを入力する。
- cmoc は、入力されたオリジナルプロンプトを skeleton の `{{original-prompt-here}}` へ挿入し、後続の AI Agent 呼び出しに渡す完全プロンプトを確定する。

## 初期コメントの責務

- 初期コメントは、editor 利用者へ入力方法を伝える補助文面とする。
- 初期コメントには、入力に必要な操作説明と有用な記入上の助言だけを含める。
- 初期コメントを、cmoc 開発者向けの prompt 設計仕様または正本仕様の代替にしてはならない。
- 初期コメントの正確な表示文面は、人間が所有してレビューする `{{cmoc-root}}/oracle/src/oracle/prompt_builder/editor_input.py` で管理する。
- 生成済み editor input は実行時生成物であり、表示文面または意味仕様の正本ではない。
- 初期コメントはオリジナルプロンプトの読み出し時に削除し、後続の AI Agent へ渡してはならない。

## 完全プロンプトの skeleton

- 呼び出し元は、対応する `build_*_parameter` 関数へオリジナルプロンプトの代わりに `{{original-prompt-here}}` を渡し、エディタ起動前に完全プロンプトの skeleton と起動パラメータを構築する。
- skeleton は、`{{original-prompt-here}}` だけが未確定であり、後続の AI Agent 呼び出しに渡す完全プロンプトと同じ構造および内容を持つ。
- skeleton 内の `{{original-prompt-here}}` は、ちょうど 1 箇所とする。
- 編集対象の初期値は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/editor_input.py` の `build_prompt_editor_input_initial_text` に、Markdown へレンダリングした skeleton を渡して構築する。
- `build_prompt_editor_input_initial_text` はサブコマンド固有の指示を組み立てない。サブコマンド固有の契約は、対応する `build_*_parameter` 関数が skeleton に含める。

## エディタの起動

- 起動するエディタは、優先度が高い順に `code`、`nano`、`vim`、`vi` とする。
- `code` で起動する場合は、必ず `--wait` を付ける。
- エディタの編集対象は、`{{repo-root}}/.cmoc/gu/ar/log/editor_input/{{time-stamp}}_orig.md` とする。
- エディタから cmoc に処理が戻ってきたら、ユーザー入力完了とみなす。

## オリジナルプロンプトの読み出し

- 編集対象からコメント `<!-- ... -->` を削除する。
- コメントを削除した結果の前後の空白文字を `strip` で除去する。

## 完全プロンプトの確定

- 読み出したオリジナルプロンプトで、skeleton 内の 1 箇所の `{{original-prompt-here}}` を置換する。
- 置換対象が 1 箇所でない場合は、後続の AI Agent を起動せずエラー終了する。
- 確定した完全プロンプトは、対応する `build_*_parameter` 関数が構築した起動パラメータから参照される `{{repo-root}}/.cmoc/gu/ar/log/editor_input/{{time-stamp}}_cmpl.md` に保存する。
- realization file 側で許容する完全プロンプトの加工は、この置換だけとする。
- 起動パラメータは再構築または変更せず、完全プロンプトを確定した後の AI Agent 呼び出しに使用する。
