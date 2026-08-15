
# `cmoc doctor`

## 概要

- `{{repo-root}}` が cmoc を正常に実行可能な状態か検証し、可能な限り修復を試みる
- 実質的には doctor preprocess を明示的に呼び出すためだけのコマンド

## 引数

- 引数なし

## 事前条件

- `cmoc doctor` 固有の事前に満たすべき条件は無い

## 実行手順

1. doctor preprocess を呼び出す

## primary report

- `natural_completion` と `error` のすべての終了経路で、doctor 実行要約を primary report として保存する。doctor preprocess の開始前または途中で確定したエラーも対象とする。
- report は Markdown と YAML Front Matter で構成し、`{{repo-root}}/.cmoc/gu/ar/report/doctor/{{time-stamp}}.md` に保存する。
- front matter には、command、生成日時、repo root、terminal result の共通分類、および終了コードを含める。
- 本文には、検査と修復の実行有無および結果、残った warning またはエラー、必要な次の操作、および関連する診断用サブコマンドログを要約する。
