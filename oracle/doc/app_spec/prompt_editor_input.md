# プロンプトのエディタ入力

## 概要

- cmoc は、オリジナルプロンプトの入力位置を示す完全プロンプトの skeleton をエディタへ提示する。
- ユーザーは、HTML コメントブロックの外にオリジナルプロンプトを入力する。
- cmoc は、検証済み editor work file の一回の最終読み取り結果を加工せず保存する。同じ結果から HTML コメントブロックを除去してオリジナルプロンプトを抽出する。
- 呼び出し元は、抽出したオリジナルプロンプトから後続呼び出し用の完全プロンプトを確定する。

## 初期コメントの責務

- 初期コメントは、editor 利用者へ入力方法を伝える補助文面とする。
- 初期コメントには、入力に必要な操作説明と有用な記入上の助言だけを含める。
- 初期コメントを、cmoc 開発者向けの prompt 設計仕様または正本仕様の代替にしてはならない。
- 初期コメントの正確な表示文面は、人間が所有してレビューする `{{cmoc-root}}/oracle/src/oracle/prompt_builder/editor_input.py` で管理する。
- 生成済み editor input は実行時生成物であり、表示文面または意味仕様の正本ではない。
- 初期コメントはオリジナルプロンプトの読み出し時に削除し、後続の AI Agent へ渡してはならない。

## 完全プロンプトの skeleton と確定

- 呼び出し元は、対応する `build_*_parameter` 関数へオリジナルプロンプトの代わりに `{{original-prompt-here}}` を渡し、エディタ起動前に完全プロンプトの skeleton を構築する。
- skeleton は、`{{original-prompt-here}}` だけが未確定であり、オリジナルプロンプトの入力位置と担当固有の prompt 構造を表示する。
- skeleton 内の `{{original-prompt-here}}` は、ちょうど 1 箇所とする。
- 編集対象の初期値は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/editor_input.py` の `build_prompt_editor_input_initial_text` に、Markdown へレンダリングした skeleton を渡して構築する。
- `build_prompt_editor_input_initial_text` はサブコマンド固有の指示を組み立てない。サブコマンド固有の契約は、対応する `build_*_parameter` 関数が skeleton に含める。

呼び出し元は、サブコマンド固有仕様に従って完全プロンプトを確定する。`AgentCallParameter.prompt` には、原則として完全プロンプト本文を直接設定する。

- 後続の AI Agent に渡す完全プロンプトに、skeleton 由来の `{{original-prompt-here}}` を残してはならない。

## ファイルの役割

editor input では、可変な作業ファイルと cmoc が保存する記録を分離する。

| 役割 | path | 書き込み主体 |
| --- | --- | --- |
| editor work file | `{{repo-root}}/.cmoc/gu/aw/editor_input/{{time-stamp}}_orig.md` | cmoc が生成および削除し、内容は人間または agent が編集する。 |
| 入力結果の保存コピー | `{{repo-root}}/.cmoc/gu/ar/log/editor_input/{{time-stamp}}_orig.md` | cmoc だけが書き込む。 |

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
7. 呼び出し元は、サブコマンド固有仕様に従ってオリジナルプロンプトを反映し、完全プロンプトを確定する。
8. 後続の AI Agent は、editor work file を参照してはならない。
9. cmoc は、この確定手順が成功した場合に editor work file を削除する。失敗した場合は復旧用に残す。

- skeleton 構築時と実行時のパラメータに対する全 field 比較、および exec 専用の prompt 一致検査は行わない。
