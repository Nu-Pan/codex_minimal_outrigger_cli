# `fork`

## Summary
- `cmoc apply fork` におけるレビュー所見の列挙・精査・適用と、適用後差分の人間向け要約生成に関する正本仕様断片をまとめる領域。
- realization file を調査するための agent 呼び出し、所見リストの schema、所見を修正へ反映する agent 呼び出し、作業レポート用の変更要約 schema と生成 prompt への入口になる。
- fork の作成や git 操作そのものではなく、fork 適用フロー内で AI agent に渡す prompt・アクセス制約・Structured Output schema を確認するための下位要素を案内する。

## Read this when
- `cmoc apply fork` で、実装調査から所見リストを作り、精査し、修正担当 agent へ渡すまでの prompt や AI 呼び出し条件を確認したいとき。
- fork 適用後の作業レポートに載せる変更要約について、差分入力、要約生成 prompt、出力 schema、カテゴリ別サマリーの契約を確認したいとき。
- apply fork 系の処理で、所見リストまたは変更要約の Structured Output schema がどの agent 呼び出しに接続されるかを追いたいとき。
- 所見本文の扱い、読み取り専用または realization write のファイルアクセス制約、git 操作禁止、参照 standard の組み合わせを確認したいとき。

## Do not read this when
- `cmoc apply fork` の CLI 解析、fork 作成、ブランチ操作、diff 取得、git コマンド実行など、agent prompt 生成や出力 schema 以外の実行フローを調べたいとき。
- oracle file、realization file、path keyword、standard、complete prompt 構築などの共通概念や共通 helper の定義を調べたいとき。
- 個別ファイルの実際の修正方法、パッチ内容そのもの、または実装差分をどう生成するかを調べたいとき。
- `cmoc apply fork` 以外のサブコマンドにおけるレビュー、要約、レポート生成の仕様を探しているとき。

## hash
- ea05cfbc23201018185e49dde1bbcbe3915cb79faca29c736ee99d43fa0094a2
