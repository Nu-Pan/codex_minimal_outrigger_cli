# プロンプトのエディタ入力

## 概要

本書は、オリジナルプロンプトを受け取る本文ファイル（editor input file）の lifecycle を定める。editor input file は依頼本文を受け取るために使い、人間向けの案内を入力に混入させない。

editor の待機中は、人間の直接入力に加え、共通の editor input handoff による editor input file 全体の上書きも受け付ける。どちらの入力も、本書の「editor input の確定手順」に従って保存・確定する。

## 構築定義の参照

- 人間が直接記入する場合に向けた console 案内は、入力する内容を示す、長くても数行程度の簡単な説明とする。正確な文面は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/editor_input.py` の `build_prompt_editor_input_console_guidance` へ委譲する。
- editor input handoff の target lifecycle、handoff ガイドの生成・保持・取得、および上書きは、`{{cmoc-root}}/oracle/doc/app_spec/editor_input_handoff.md` の「handoff target」「handoff ガイド」「MCP interface」、失敗時の責務は同文書の「agent の責務と権限」を正本とする。
- 完全 prompt skeleton と入力確定後の完全 prompt は、各 agent call の正確な構築を所有する builder で構築する。oracle src への委譲は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/tui.md` の「全バックエンド共通」、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/oracle_investigation.md` の「TUI 起動パラメータ」、および `{{cmoc-root}}/oracle/doc/app_spec/sub_command/oracle_edit.md` の「ユーザー指示と prompt の構築」を正本とする。
- 生成済み editor input、handoff ガイド、および skeleton は実行時生成物であり、editor lifecycle または prompt 文面の正本ではない。

skeleton 構築時と実行時のパラメータについて、全 field の比較は行わない。exec 専用の prompt 一致検査も行わない。

## ファイルの役割

editor input 1 回につき、`{{repo-root}}/.cmoc/gu/log/editor_input/{{time-stamp}}_orig.md` を本文ファイルとして 1 つ使用し、編集開始から入力確定後の保存まで共用する。編集対象と保存記録を別ファイルに分けない。

| 段階 | 本文ファイルの役割 | 書き込み主体 |
| --- | --- | --- |
| 編集待機中 | 未信頼かつ可変な依頼本文 | 人間が直接編集する。cmoc は handoff submission に基づいて全面上書きする。 |
| 確定保存時 | 最終読み取り結果の保存原文 | cmoc が書き込む。 |
| 確定後 | 入力の保存記録 | cmoc による入力更新は終了する。人間による再編集は可能。 |

- 編集待機中の内容を保存記録として扱ってはならない。
- 入力確定後の cmoc と後続 agent は、固定した最終読み取り結果と、そこから抽出したオリジナルプロンプトを使用する。editor input file を入力の取得元として再読せず、確定済み入力を更新しない。送信元が handoff 後に会話を続けても、この扱いは変わらない。
- 保存記録は編集対象から独立していない。確定後に人間が同じパスを再編集すれば、残した記録も変わり得るため、本文ファイル自体の不変性は保証しない。
- agent による直接編集の禁止と書き込み主体の責任分界は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「詳細なファイルアクセス制限」と「書き込み主体の責任分界」に従う。

## エディタの起動

- エディタの起動前に、人間向けの console 案内を stderr に表示する。出力先と TUI への通知境界は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「出力先の責務」と「TUI と自動補完の境界」に従う。
- 起動するエディタは、優先度が高い順に `code`、`nano`、`vim`、`vi` とする。
- `code` で起動する場合は、必ず `--wait` を付ける。
- エディタの編集対象は、editor input file とする。
- エディタから cmoc に処理が戻った時点で、ユーザー入力が完了したとみなす。

## editor input の確定手順

1. cmoc は、本書の「ファイルの役割」で定める path に、空の editor input file を作成する。
2. cmoc は、受信先の agent call に対応する完全 prompt skeleton から handoff ガイドを生成し、共通の handoff target lifecycle を適用する。
3. cmoc は、本書の「エディタの起動」に従ってエディタを起動し、処理が戻るまで待機する。
4. cmoc は、`{{cmoc-root}}/oracle/doc/app_spec/editor_input_handoff.md` の「handoff target」に従い、target の無効化と handoff ガイドファイルの削除までを完了させる。
5. cmoc は最終読み取り時に editor input file を検証する。次の条件を満たさない対象は、読み取り・上書きをせず、入力として受け付けない。
    - 対象 path が `{{repo-root}}/.cmoc/gu/log/editor_input` ディレクトリ内に収まる。
    - 対象が regular file である。
    - 対象が symlink ではない。
6. 検証に成功した場合、cmoc は editor input file を一度だけ読み取り、その結果を最終読み取り結果として固定する。
7. cmoc は、固定した最終読み取り結果を加工せず、同じ editor input file の path へ確定保存する。
8. cmoc は、同じ最終読み取り結果の前後の空白文字だけを `strip` で除去し、オリジナルプロンプトとする。HTML コメントも本文として保持する。
9. 呼び出し元は、サブコマンド固有仕様に従ってオリジナルプロンプトを反映し、完全プロンプトを確定する。

cmoc は、この確定手順が成功した場合も editor input file を削除せず、記録として残す。失敗した場合は後続の実行へ進まず、作成済みの本文ファイルを復旧用に残す。確定保存の失敗によって入力を失わず、復旧できる状態を保つことを要求する。保存原文と固定した最終読み取り結果の一致、および失敗時の入力保持を満たす具体的な保存方式は、実装に委ねる。

## 既存データの扱い

この配置は新規入力から適用する。既存の保存ログはそのまま残し、旧 `{{repo-root}}/.cmoc/gu/editor_input` に残る復旧用ファイルを自動移動・削除しない。
