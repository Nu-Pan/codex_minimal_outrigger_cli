# `cmoc indexing`

## 概要

`cmoc indexing` は、現在の work-root の文書検索索引を明示的に同期する。対象・同期・失敗・排他・解放は、`{{cmoc-root}}/oracle/doc/app_spec/document_search.md` の「対象と信頼境界」「同期と cache」「排他、期限、終了」を正本とし、通常検索前と同じ同期処理を使う。

## 引数と事前条件

- 引数なし。
- git working tree と staging area の未コミット差分を許容する。索引同期のために既存差分を commit、stash、revert、または破棄しない。
- この CLI の信頼された caller は、現在の work-root の閲覧可能な oracle/doc 全体を構造化した範囲として渡す。分類と検索対象条件は共通仕様を適用する。別 call の狭い scope に対する索引とは取り違えない。

## 実行手順

1. doctor preprocess を呼び出す。doctor 固有の修復と commit は、`{{cmoc-root}}/oracle/doc/app_spec/doctor_preprocess.md` の「実行手順」に従う。
2. work-root と実効閲覧範囲、資材・設定、および保存先の非追跡を確認し、共通の同期処理を実行する。
3. 同期結果を保存し、資源を解放して終了する。検索 query の embedding と rerank、および Codex agent による目次生成は行わない。

索引同期自体は Git commit を作らない。失敗時は完了した同期として報告せず、共通仕様の失敗識別と未完了世代の非公開を維持する。

## primary report

- `natural_completion` と `error` のすべての終了経路で同期実行要約を primary report として保存する。doctor preprocess の失敗や同期開始前の失敗も含む。
- report は Markdown と YAML Front Matter で構成し、`{{repo-root}}/.cmoc/gu/report/indexing/{{time-stamp}}.md` に保存する。
- front matter は command、生成日時、repo root、work root、実効閲覧範囲の識別情報、索引 identity、terminal result の共通分類、終了コード、および同期結果を含む。同期結果は未開始・更新済み・無変更・失敗を区別する。確定前の identity や件数は `null` とする。
- 本文には、許可文書・chunk の件数、追加・変更・削除・空白化と埋め込み再利用の実績、所要時間、失敗 code と理由、warning、必要な次の操作、および診断用サブコマンドログを要約する。未測定・未実行の件数をゼロとして報告しない。
- 生成した INDEX 名や索引生成 commit ID を結果項目にしない。doctor の修復があれば、その結果を索引同期と区別する。
