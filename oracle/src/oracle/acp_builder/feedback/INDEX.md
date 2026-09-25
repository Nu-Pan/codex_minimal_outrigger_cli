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
- 構造化 observation と絞り込み済みの既存候補を照合し、同一 issue か新規 issue かを判断させる agent call の prompt と起動 parameter を構築する。
- 読み取り専用の参照境界と、判断に必要な関連情報への routing を含む。原因診断や remediation は担当しない。

## Read this when
- normalization agent の prompt、起動条件や参照境界を変更・確認するとき。
- 観測と既存候補の同一性判断に渡す情報や、同一 issue の判定条件を確認するとき。

## Do not read this when
- intake 内の validation、候補形成、処理順序など全体の仕様を確認するときは、feedback intake の仕様を読む。
- agent call の出力構造を確認・変更するときは、対応する Structured Output schema を読む。
- issue の現在状態の確認、修正、検証を扱うときは、remediation 用の構築定義を読む。

## hash
- a8c3a072f819f3c0c845bb1d0975325ae9dc16163c79355e7c944c5b9aee9217

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
- 正規化済み feedback issue 1 件について、現在状態の確認から realization 修正・検証までを行う agent 向け prompt と起動条件を組み立てる。remediation call 固有の指示、アクセス境界、実行設定を確認・変更するときの入口。

## Read this when
- issue remediation call が、現在状態の確認、安全な realization 修正、修正後の検証をどう指示するか確認・変更するとき。
- 結果分類の判断制約、許可する変更範囲、差分の扱いなど、この call 固有の制約を確認するとき。
- call の cwd、アクセスモード、schema の指定、indexing preflight など起動 parameter の設定を確認・変更するとき。

## Do not read this when
- feedback observation と既存候補の同一性判断や issue identity の確定を調べるときは、normalization の実装と仕様を読む。
- 出力契約の構造や値の形式を調べるときは Structured Output schema を、結果分類の意味を調べるときは feedback の意味仕様を直接読む。
- wave 処理、再確認の順序、issue 単位の commit、join、publication、recovery など全体の orchestration を調べるときは feedback report の workload 仕様を読む。

## hash
- c0dc67720f11b6e82d2194eae634fa966f761541da56f47dfdcc90c090ac3f31
