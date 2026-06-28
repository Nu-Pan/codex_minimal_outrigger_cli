# `__init__.py`

## Summary
- `oracle.acp_builder.apply.fork` と同じ import 経路を実装側に用意するための互換 package 初期化ファイル。本文は互換 package であることを示す docstring のみを持ち、具体的な処理や公開 API の定義は持たない。

## Read this when
- `oracle.acp_builder.apply.fork` 互換 package の存在理由を確認したいとき。
- この package 直下の実装を読む前に、package 自体が処理本体ではなく互換用の入口であることだけを確認したいとき。

## Do not read this when
- fork 適用処理の具体的な実装、関数、クラス、入出力を調べたいとき。
- 互換 package ではなく oracle 側の正本仕様断片を確認したいとき。
- package 初期化 docstring 以外の実行時挙動や副作用を探しているとき。

## hash
- c5707d270af058dc9b548e1d49ffefdd38c20a0785a67a293523f2be83ebc266

# `change_summary.py`

## Summary
- ACP builder の fork 適用処理における change summary 実装を、正本側実装から公開する薄い realization 実装。実体は正本側の同名モジュールにあり、このファイル自体はその API を realization 側の import 経路へ接続する入口である。

## Read this when
- realization 側から fork 適用処理の change summary API がどの正本実装へ委譲されているか確認したいとき。
- src 配下の import 経路で change summary 関連の名前解決や再エクスポートを確認したいとき。

## Do not read this when
- change summary の具体的な処理内容、データ構造、分岐条件を確認したいとき。その場合は委譲先の正本側実装を読む。
- fork 適用処理全体の流れや、change summary 以外の apply/builder 責務を調べたいとき。より上位または該当する別モジュールを読む。

## hash
- cbb76ca448c88775e7c984af9a60a2bbad476918df7c66b7a30ce457f934ea0f

# `file_finding_enumeration.py`

## Summary
- 対象は、実装側の同名モジュールを正本側の実装へ委譲する薄い再公開ファイルである。本文自体は独自ロジックを持たず、fork 適用時の file finding enumeration に関する実体は正本側モジュールに置かれている。

## Read this when
- 実装側の import 経路から、fork 適用時の file finding enumeration の定義がどこへ委譲されているかを確認したいとき。
- 同階層の実装ファイル群のうち、この概念の realization 側エントリーポイントだけを確認したいとき。

## Do not read this when
- file finding enumeration の具体的な仕様、関数、型、挙動を調べたいときは、委譲先の正本側モジュールを読む。
- fork 適用処理全体の流れや他の責務を調べたいときは、該当する上位または隣接モジュールを読む。

## hash
- b64c3193ab0469318fecebabc0c2e2ac9d2164d2bcbef9dd8d11362a205ab599

# `finding_application.py`

## Summary
- fork 適用処理で検出された finding の適用仕様を公開する薄い再エクスポート実装。実体は oracle 側の同名モジュールにあり、この realization 側ファイルは src ツリーからその定義を参照可能にする入口として位置づく。

## Read this when
- src ツリー側から fork finding application 関連の公開名がどこへ委譲されているか確認したいとき。
- 実装本体ではなく、realization implementation が oracle 側の正本実装断片を再利用している接続点を確認したいとき。

## Do not read this when
- fork finding application の具体的な関数・型・処理内容を確認したいとき。その場合は再エクスポート先の oracle 側本文を読む。
- fork 適用処理全体の設計や他の適用段階を調べたいとき。その場合は同じ責務領域のより上位または隣接する本文を読む。

## hash
- 055ee85cc2fab78164f4ef81a97d605ec0bc25162c4e7c098fffa72bb1e0eb84
