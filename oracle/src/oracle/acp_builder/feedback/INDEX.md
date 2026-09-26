# `normalize_issue.json`

## Summary
- feedback observation と既存 issue 候補の同一性判断を行う agent call の出力契約を定める。
- 同じ issue と判断した場合と新規 issue と判断した場合の結果を区別する。

## Read this when
- 同一性判断 agent call の出力契約や、返却値を受け取る側の適合性を確認・変更するとき。

## Do not read this when
- 一致判定の基準や候補の選び方、新規 issue の登録方法を調べるとき。この対象は出力契約のみを定めるため、それらを定義する仕様や実装へ進む。

## hash
- 2b30dfd42f9d1f751aca7b061bfe811dbe8d7fcfa85788fea6e1a1cfc647764f

# `normalize_issue.py`

## Summary
- agent observation と絞り込み済みの issue 候補の同一性判断を担う normalization call の prompt と起動 parameter を組み立てる。
- この call の判断範囲、参照境界、読み取り専用の実行条件を確認する入口。

## Read this when
- feedback observation を既存候補と照合する判断基準、追加参照の範囲、判断対象外を確認または変更するとき。
- この call の実行場所、文書検索範囲、アクセスモードなど、起動 parameter の構築を追うとき。

## Do not read this when
- intake 全体の validation、処理順序、wave、checkpoint の意味を確認するときは、feedback の正本仕様へ進む。
- issue の現在状態の診断、修正、検証結果を扱うときは、remediation call の定義へ進む。
- 出力の Structured Output schema だけを確認するときは、対応する schema 定義を直接読む。

## hash
- c9ce5cc9e6c570f99c5d809d29eb4982c9693b4c480395e73a3154b679099474

# `remediate_issue.json`

## Summary
- feedback issue の remediation agent call が返す結果契約を定義し、解決状態や判断根拠、修正・検証の結果を表す。

## Read this when
- feedback issue の remediation 結果の分類と、その結果を支える修正差分・現状確認・検証・人の対応要否の扱いを確認または変更するとき。

## Do not read this when
- remediation の指示文、対象範囲、権限、起動方法を調べるときは、prompt と起動処理の実装を読む。
- feedback issue の正規化や既存 issue との同一性判断を調べるときは、その処理の schema と実装を読む。

## hash
- 058852babba8588d1a91592f7b21cfd8d92bbe8e6d923185517c26704e5373c5

# `remediate_issue.py`

## Summary
- 正規化済みの単一 feedback issue について、現在状態の確認・安全な realization 修正・検証を指示する agent 向け prompt と起動パラメータを組み立てる。
- issue 固有の対象範囲、編集権限、結果分類の制約、検索範囲、実行場所を定める call 構築の入口。

## Read this when
- 単一 issue の remediation call の指示内容や対象範囲、編集権限、結果分類上の制約を確認・変更するとき。
- この call の検索範囲や実行場所など、起動条件を確認・変更するとき。

## Do not read this when
- 構造化出力の契約だけを確認・変更するときは、対応する schema を直接読む。
- feedback report 全体の issue 正規化、call の順序、commit・merge・結果公開の流れを調べるときは、report の処理仕様から読む。
- 結果分類の共通の意味や人間向け公開条件を調べるときは、feedback の意味仕様から読む。

## hash
- 31fcf1b7b9feec2c7f3b7275c77d375842b7af3f277cd9001665d32fcf17130b
