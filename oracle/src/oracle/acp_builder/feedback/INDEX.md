# `normalize_issue.json`

## Summary
- feedback issue の同一性判断を返す出力スキーマ。入力された既存 issue candidate と同一か新規かの判断結果を定義し、feedback 同一性判断処理の出力契約への入口となる。

## Read this when
- feedback issue が既存候補と同一か、新しい issue かを判定する agent call の出力形式を確認するとき
- 同一 issue の ID を返す場合と、新規 issue として null を返す場合の契約を確認するとき

## Do not read this when
- feedback issue の内容や同一性判定ロジック自体を確認したいとき
- agent call の入力形式や issue candidate の生成・保存処理を確認したいとき

## hash
- 2b30dfd42f9d1f751aca7b061bfe811dbe8d7fcfa85788fea6e1a1cfc647764f

# `normalize_issue.py`

## Summary
- feedback observation と絞り込み済みの既存 issue candidate の同一性だけを判定する agent call の prompt と起動パラメータを構築する入口。
- issue の内容や原因を生成せず、候補との比較結果を決定論的な条件付きで返す処理を扱う。

## Read this when
- feedback observation が既存 issue と同一か新規かを判定する prompt、入力範囲、Structured Output の事後条件を確認するとき
- normalize issue 用の agent call パラメータや readonly の実行条件を変更するとき

## Do not read this when
- observation の申告や構造化、候補 issue の絞り込み、issue の summary・impact・remediation の生成を確認するとき
- 同一性判定の実装ではなく、出力スキーマ自体の定義を直接確認すべきとき

## hash
- 2151f8aa221438f82a77b1613a61062bb03b2d1dae49e1e22814268b9b36245c

# `remediate_issue.json`

## Summary
- feedback issue remediation agent call の結果を表す JSON Schema。入力された feedback issue について、修正完了、既解決、報告対象外、人間対応が必要、判定不能のいずれかを分類し、issue ID、現在の根拠、変更ファイル、検証結果、理由、人間対応の要否を返す。
- 結果分類ごとに、realization file の変更差分の必須性、current evidence と verification の必須性、human action の扱いを制約する。

## Read this when
- feedback issue の remediation agent が返す構造化出力の形式や、結果分類ごとの必須フィールドと制約を確認するとき。
- 修正済み・既解決・報告対象外・人間対応必須・判定不能のどの結果を返すべきか、その出力契約を確認するとき。

## Do not read this when
- feedback issue の受付、正規化、収集、または observation の送信方法を確認したいとき。
- realization file 自体の実装や、remediation の診断・修正手順を確認したいとき。
- INDEX.md のルーティング情報だけを確認したいとき。

## hash
- 058852babba8588d1a91592f7b21cfd8d92bbe8e6d923185517c26704e5373c5

# `remediate_issue.py`

## Summary
- feedback issue 1件の存在確認、realization file に限定した安全な修正、検証、および remediation 結果を返す agent call parameter を構築する。

## Read this when
- 正規化済み feedback issue の remediation 用 prompt、realization 書き込み権限、対象範囲、結果分類、変更 path、検証条件を確認するとき。
- feedback issue remediation の agent call 起動パラメータや Structured Output schema の関連付けを変更・調査するとき。

## Do not read this when
- feedback issue の受付・正規化・報告処理を調べるとき。
- remediation 対象そのものの realization 実装や oracle file の内容を直接確認するとき。
- feedback remediation の結果 schema の定義だけを確認するとき。

## hash
- 44e4fd7e602d407b294b2e02359aa70f3841692e262d2b8d4b555cf2537fbc91
