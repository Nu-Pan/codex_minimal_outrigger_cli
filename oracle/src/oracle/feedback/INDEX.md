# `reporter_input.json`

## Summary
- フィードバック observation の submission に使う version 2 入力契約を定義し、tool discovery と受け入れ検査で参照されます。
- workload limitation の説明など、入力内容の検証規則を確認する入口です。

## Read this when
- reporter に送る observation 入力の構造、制約、互換性を変更または確認するとき。
- tool discovery と受け入れ検査で使う入力契約を調べるとき。

## Do not read this when
- 何を報告すべきか、または agent へ渡す報告指示の意味を確認するとき。報告基準や prompt の仕様を参照してください。
- reporter の transport・tool result・raw 保存、または `cmoc feedback report` の処理を調べるとき。該当する interface や report 処理の仕様へ進んでください。

## hash
- 7b17a9d08b99bd759f347a6a613599ee6229b46e7765e2012afbfbc208f72dfe
