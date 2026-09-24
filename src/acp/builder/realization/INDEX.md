# `__init__.py`

## Summary
- realization workload の builder adapter 群をまとめる package marker。子 package は apply と refactor の adapter に分かれ、個別の builder 処理は正本の実装を再公開する。

## Read this when
- realization workload の builder adapter 層の役割を把握し、apply と refactor のどちらを確認するか決めるとき。

## Do not read this when
- 特定の apply または refactor builder の動作を調べるときは、対応する adapter と正本の実装を直接確認する。
- realization の CLI コマンドの動作を調べるときは、コマンド層を直接確認する。

## hash
- cd24953f9993d22add52453bee8a2c6dd9c2fc85ecd238c962f1cc82066eec92

# `apply`

## Summary
- realization apply fork 用の builder adapter を担い、既存の import 参照を保つため oracle 側の launch-exec parameter builder を再公開する。

## Read this when
- realization apply fork の launch-exec builder の互換 import 参照や、この adapter の追加・変更・削除を扱うとき。

## Do not read this when
- launch-exec parameter の正本の挙動を変更・確認するときは、対応する oracle builder を直接読む。
- realization refactor fork の builder を扱うときは、そちらの adapter を読む。

## hash
- 489bb960e219cb5547d82a3939183a15250f7f3053cb5244010addb81b6870c4

# `refactor`

## Summary
- realization の refactor 用 builder adapter をまとめ、fork の変更要約とファイル単位レビュー・修正の parameter builder を oracle の定義から再公開する入口です。

## Read this when
- realization refactor fork の builder 呼び出し口や、refactor 側の adapter の役割を確認するとき。

## Do not read this when
- prompt の内容や schema の定義を確認するときは、oracle 側の対応する定義を直接参照してください。
- realization apply の起動 parameter を調べるときは、隣接する apply 側を参照してください。

## hash
- 9967ee89fdb7e90dfd3488fbe7ed2698f1535924ffd79a69418eda3f742a629e
