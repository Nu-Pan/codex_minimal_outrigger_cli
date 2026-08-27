
# `cmoc doctor`

## 概要

- doctor preprocess を明示的に呼び出すコマンドである。検証・修復の内容は、`{{cmoc-root}}/oracle/doc/app_spec/doctor_preprocess.md` の「Doctor Preprocess」を正本とする

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
