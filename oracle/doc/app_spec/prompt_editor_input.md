# プロンプトのエディタ入力

## 概要

- 本書は、オリジナルプロンプトを受け取る editor work file の lifecycle を定める。
- editor work file は依頼本文を受け取るために使い、人間向けの案内を入力に混入させない。
- editor の待機中は、共通の editor input handoff による editor work file 全体の上書きも受け付ける。
- cmoc は、人間の直接入力と handoff 入力を共通に扱い、検証済み editor work file の一回の最終読み取り結果を保存と入力確定に使う。

## 構築定義の参照

- 人間が直接記入する場合に向けた console 案内は、入力する内容を示す、長くても数行程度の簡単な説明とする。正確な文面は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/editor_input.py` の `build_prompt_editor_input_console_guidance` へ委譲する。
- editor input handoff の target lifecycle、handoff ガイドの生成・保持・取得、および上書きは、`{{cmoc-root}}/oracle/doc/app_spec/editor_input_handoff.md` の「handoff target」「handoff ガイド」「MCP interface」、失敗時の責務は同文書の「agent の責務と権限」を正本とする。
- 完全 prompt skeleton と入力確定後の完全 prompt は、各 agent call の正確な構築を所有する builder で構築する。oracle src への委譲は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/tui.md` の「全バックエンド共通」、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/oracle_investigation.md` の「TUI 起動パラメータ」、および `{{cmoc-root}}/oracle/doc/app_spec/sub_command/oracle_edit.md` の「ユーザー指示と prompt の構築」を正本とする。
- 生成済み editor input、handoff ガイド、および skeleton は実行時生成物であり、editor lifecycle または prompt 文面の正本ではない。

## ファイルの役割

editor input では、可変な作業ファイルと cmoc が保存する記録を分離する。

| 役割 | path | 書き込み主体 |
| --- | --- | --- |
| editor work file | `{{repo-root}}/.cmoc/gu/editor_input/{{time-stamp}}_orig.md` | cmoc が生成および削除する。人間は直接編集でき、cmoc は handoff submission に基づいて全面上書きできる。 |
| 入力結果の保存コピー | `{{repo-root}}/.cmoc/gu/log/editor_input/{{time-stamp}}_orig.md` | cmoc だけが書き込む。 |

- editor work file は未信頼かつ可変な作業ファイルとする。cmoc と後続 agent は、その内容を保存記録として参照してはならない。
- 入力確定後は、保存した最終読み取り結果と、そこから抽出したオリジナルプロンプトを使用する。送り元が handoff 後に会話を続けても、確定済み入力を再取得・更新しない。
- agent による直接編集の禁止と書き込み主体の責任分界は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「詳細なファイルアクセス制限」と「書き込み主体の責任分界」に従う。

## エディタの起動

- エディタの起動前に、人間向けの console 案内を stderr に表示する。出力先と TUI への通知境界は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「出力先の責務」と「TUI と自動補完の境界」に従う。
- 起動するエディタは、優先度が高い順に `code`、`nano`、`vim`、`vi` とする。
- `code` で起動する場合は、必ず `--wait` を付ける。
- エディタの編集対象は、editor work file とする。
- エディタから cmoc に処理が戻った時点で、ユーザー入力が完了したとみなす。

## editor input の確定手順

1. cmoc は、空の editor work file を作成する。
2. cmoc は、受信先の agent call に対応する完全 prompt skeleton から handoff ガイドを生成し、共通の handoff target lifecycle を適用する。
3. cmoc は、本書の「エディタの起動」に従ってエディタを起動し、処理が戻るまで待機する。
4. cmoc は最終読み取り時に editor work file を検証する。検証条件を次に示す。
    - 対象 path が `{{repo-root}}/.cmoc/gu/editor_input` ディレクトリ内に収まる。
    - 対象が regular file である。
    - 対象が symlink ではない。
5. 検証に成功した場合、cmoc は editor work file を一度だけ読み取る。この結果を最終読み取り結果とする。
6. cmoc は、最終読み取り結果を加工せず、入力結果の保存コピーへ保存する。
7. cmoc は、同じ最終読み取り結果の前後の空白文字だけを `strip` で除去し、オリジナルプロンプトとする。HTML コメントも本文として保持する。
8. 呼び出し元は、サブコマンド固有仕様に従ってオリジナルプロンプトを反映し、完全プロンプトを確定する。
9. 後続の AI Agent は、editor work file を参照してはならない。
10. cmoc は、この確定手順が成功した場合に editor work file を削除する。失敗した場合は復旧用に残す。

- skeleton 構築時と実行時のパラメータについて、全 field の比較は行わない。exec 専用の prompt 一致検査も行わない。
