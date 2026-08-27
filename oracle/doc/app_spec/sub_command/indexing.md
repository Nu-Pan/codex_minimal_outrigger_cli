
# `cmoc indexing`

## 概要

- `cmoc indexing` は、`{{cmoc-root}}/oracle/doc/app_spec/indexing.md:2` の仕様に従って、現在の `{{work-root}}` を明示的にインデクシングする

## 引数

- 引数なし

## 事前条件

以下の場合はエラー終了する。

- git 未コミット差分が存在する

## 実行手順

1. doctor preprocess を呼び出す
2. インデクシングを明示的に実行する

## primary report

- `natural_completion` と `error` のすべての終了経路で、インデクシング実行要約を primary report として保存する。事前条件違反や doctor preprocess の失敗も対象とする。
- report は Markdown と YAML Front Matter で構成し、`{{repo-root}}/.cmoc/gu/ar/report/indexing/{{time-stamp}}.md` に保存する。
- front matter には、command、生成日時、repo root、terminal result の共通分類、終了コード、および作成した commit ID を含める。commit を作成していない場合は commit ID を `null` とする。
- 本文には、インデクシングの実行有無、処理結果、作成または更新した `INDEX.md`、commit の作成結果、warning またはエラー、必要な次の操作、および関連する診断用サブコマンドログを要約する。
