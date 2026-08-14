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

## ファイルの役割

editor input では、可変な作業ファイルと cmoc が保存する記録を分離する。

| 役割 | path | 書き込み主体 |
| --- | --- | --- |
| editor work file | `{{repo-root}}/.cmoc/gu/aw/editor_input/{{time-stamp}}_orig.md` | cmoc が生成および削除し、内容は人間または agent が編集する。 |
| 入力結果の保存コピー | `{{repo-root}}/.cmoc/gu/ar/log/editor_input/{{time-stamp}}_orig.md` | cmoc だけが書き込む。 |
| 確定した完全プロンプト | `{{repo-root}}/.cmoc/gu/ar/log/editor_input/{{time-stamp}}_cmpl.md` | cmoc だけが書き込む。 |

- `ar` は agent-readable かつ agent-write-prohibited な保存領域とする。
- `aw` は未信頼かつ可変な作業領域とする。cmoc と後続 agent は、`aw` の内容を保存記録として参照してはならない。

## エディタの起動

- 起動するエディタは、優先度が高い順に `code`、`nano`、`vim`、`vi` とする。
- `code` で起動する場合は、必ず `--wait` を付ける。
- エディタの編集対象は、editor work file とする。
- エディタから cmoc に処理が戻ってきたら、ユーザー入力完了とみなす。

## editor input の確定手順

1. cmoc は、`build_prompt_editor_input_initial_text` の結果を初期値とする editor work file を作成する。
2. 人間または agent が、editor work file を編集する。
3. エディタから処理が戻った後、cmoc は最終読み取り時に editor work file を検証する。検証条件を次に示す。
    - 対象 path が `{{repo-root}}/.cmoc/gu/aw/editor_input` ディレクトリ内に収まる。
    - 対象が regular file である。
    - 対象が symlink ではない。
4. 検証に成功した場合、cmoc は editor work file を一度だけ読み取る。この結果を最終読み取り結果とする。
5. cmoc は、最終読み取り結果を加工せず、入力結果の保存コピーへ保存する。
6. cmoc は、同じ最終読み取り結果からコメント `<!-- ... -->` を削除する。削除結果の前後の空白文字を `strip` で除去し、オリジナルプロンプトとする。
7. cmoc は、オリジナルプロンプトで skeleton 内の 1 箇所の `{{original-prompt-here}}` を置換し、確定した完全プロンプトを保存する。置換対象が 1 箇所でない場合は、後続の AI Agent を起動せずエラー終了する。
8. 後続の AI Agent は、確定した完全プロンプトを読み取る。editor work file を参照してはならない。
9. cmoc は、この確定手順が成功した場合に editor work file を削除する。失敗した場合は復旧用に残す。

- realization file 側で許容する完全プロンプトの加工は、手順 7 の置換だけとする。
- 起動パラメータは再構築または変更せず、完全プロンプトを確定した後の AI Agent 呼び出しに使用する。
