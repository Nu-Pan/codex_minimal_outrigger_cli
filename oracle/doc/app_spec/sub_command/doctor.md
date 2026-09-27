# `cmoc doctor`

## 概要

`cmoc doctor` は、各サブコマンドに必要な共通実行環境・設定・資材を準備・修復・検証する公開入口とする。処理内容と正常終了で保証する範囲は、`{{cmoc-root}}/oracle/doc/app_spec/doctor_preprocess.md` の「成功条件と保証範囲」「共通実行環境の検証」「実行手順」を正本とする。

## 引数

- 引数なし

## 事前条件

- `cmoc doctor` 固有の branch や clean 状態の事前条件はない。起動基盤の境界は、`{{cmoc-root}}/oracle/doc/app_spec/doctor_preprocess.md` の「共通実行環境の検証」に従う。

## 実行手順

1. doctor preprocess を明示 doctor の準備・修復経路で呼び出す。
2. 検証・修復の結果と保証範囲を primary report に保存し、終了結果を確定する。

## 終了結果

doctor preprocess の成功条件を満たし、終了処理を完了した場合に限り、`natural_completion`・終了コード 0 とする。未解決または未検証の必須条件が残る場合は、`error`・非ゼロの終了コードとし、完了した一部の準備だけを根拠に正常終了してはならない。

失敗の診断・終了処理は、`{{cmoc-root}}/oracle/doc/app_spec/error_handling.md` の「エラー終了の確定」「handled failure の表示」「internal failure の表示」に従う。primary report の保存を確認できない場合も、この共通規則を適用する。

## primary report

- `natural_completion` と `error` のすべての終了経路で、doctor 実行要約を primary report として保存する。doctor preprocess の開始前または途中で確定したエラーも対象とする。
- report は Markdown と YAML Front Matter で構成し、`{{repo-root}}/.cmoc/gu/report/doctor/{{time-stamp}}.md` に保存する。
- front matter には、command、生成日時、repo root、cmoc root、対象 work root、terminal result の共通分類、および終了コードを含める。確定できなかった root は未確定と分かるようにする。
- 本文には、共通実行環境・設定・管理領域・検索資材の検査と修復の実行有無および結果、残った warning またはエラー、必要な次の操作、および関連する診断用サブコマンドログを要約する。
- 検索設定については、対象ファイル、生成・補完した項目と値、検証結果、および保存の有無を含める。補完不要と、失敗して候補を保存しなかった場合を区別する。
- 検索資材については、所有する cmoc root と保存先、照合した資材 identity、再利用・取得・構築・修復の実績、および照合・runtime 互換検査・実モデルの embedding・rerank 検証の結果を含める。未開始・未完了・失敗を成功と区別し、取得済みでも検証未完了なら利用可能と記載しない。失敗後に残る資材の状態と、必要な手動対処または再実行方法も示す。
- 成功時は、検査した root・設定条件と保証範囲が分かるようにする。非必須機能の warning は必須条件の検証結果と区別し、索引同期・任意の実検索・製品受入条件まで完了したと誤認させない。
