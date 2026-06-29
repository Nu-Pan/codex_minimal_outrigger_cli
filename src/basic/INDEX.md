# `__init__.py`

## Summary
- oracle src 側の basic 互換 import を realization 側で受けるための入口。ACP 基本型などを複製せず、既存の `basic.*` 参照を維持する互換層として位置づけられる。
- 互換目的で残されており、削除可否は realization 側と利用者向け公開面から `basic.*` 参照がなくなり、正本側または実体 module への移行が済んでいるかで判断する。

## Read this when
- `basic.*` 参照の互換維持、移行、削除条件を確認したいとき。
- oracle src 側の basic 互換 import 入口と、realization 側または利用者向け公開面との関係を確認したいとき。
- ACP 基本型や関連する基本 module を複製せず既存参照を保つ理由を確認したいとき。

## Do not read this when
- 個別の ACP 基本型や実体 module の定義・挙動を確認したいとき。
- 正本仕様断片そのものや oracle src 配下の具体的な実装内容を確認したいとき。
- `basic.*` 互換参照の有無や削除条件ではなく、一般的な path model、CLI 挙動、テスト挙動を調べたいとき。

## hash
- bd7e89dfb56983290190c9facb93f671f397b370fc9ea0fb32052b0bc819b591

# `acp.py`

## Summary
- 正本側で定義された ACP 関連型を realization 側の既存公開面へ再公開する互換用モジュール。
- 正本型を複製せず、既存の参照を維持するための薄い入口であり、利用者向け公開面や realization 側からその参照がなくなれば削除可能な位置づけを持つ。

## Read this when
- 既存コードや利用者が参照している ACP 関連型の import 経路を維持・整理する必要があるとき。
- realization 側で ACP 型を独自定義せず、正本側の型を再公開している互換境界を確認したいとき。
- この互換入口を削除できるか判断するために、残す理由と削除条件を確認したいとき。

## Do not read this when
- ACP 関連型そのものの定義内容、列挙値、データ構造を確認したいとき。その場合は正本側の型定義を直接読む。
- ACP の生成ロジック、変換処理、CLI 挙動、テスト観点を調べたいとき。この対象は再公開だけを担い、それらの実装責務を持たない。
- 新しい ACP 型や挙動を追加する場所を探しているとき。この対象は互換用の公開入口であり、正本型の追加・変更場所ではない。

## hash
- de511dc6ae0bf66bbe04c2916d62b5268565b3e4ecdd7da73137fc3bb6174faa

# `path_model.py`

## Summary
- 公開 path model の実体を持たず、正本側の path model API を realization 側の既存公開面として再公開する互換モジュール。
- 既存利用者が参照する path placeholder と path 解決関数を、重複実装せず正本側実装へ委譲する入口として位置づけられている。

## Read this when
- realization 側で公開されている path model API の import 経路や再公開内容を確認したいとき。
- 正本側の path model 実装と既存の公開参照とのつながりを調べたいとき。
- 互換用の再公開を残す理由、または削除できる条件を確認したいとき。

## Do not read this when
- path placeholder や path 解決処理そのものの仕様・実装詳細を確認したいとき。その場合は再公開先の正本側実装を読む。
- path model 以外の basic 領域の機能や責務を調べたいとき。
- 新しい path 変換仕様を検討しているだけで、既存公開参照の互換性に関わらないとき。

## hash
- 3ef925dfd0d7897d6364bb284d1591c7c6844ad7ea64df15894d9b69ecbca164

# `struct_doc.py`

## Summary
- 構造化文書の正本実装を realization 側で再実装せず、既存の公開参照を維持するための互換再公開モジュール。
- 構造化文書本体、コードブロック表現、Markdown 描画、補助関数を正本側実装から import し、同じ公開面として提供する。
- 互換層として残す対象であり、削除できる条件は realization 側と利用者向け公開面から `basic.struct_doc` 参照がなくなること。

## Read this when
- `basic.struct_doc` 経由で構造化文書 API を参照している既存実装や公開面の互換性を確認する。
- 構造化文書 API の import 経路、再公開対象、または `__all__` の公開名を調整する。
- 正本側の構造化文書実装を realization 側へ複製せず参照する方針や、その互換層の削除条件を確認する。

## Do not read this when
- 構造化文書のデータ構造、Markdown 変換、補助関数の実処理を変更したい場合。正本側の実装を読む。
- `basic.struct_doc` 参照の互換維持や公開名に関係しない構造化文書利用箇所を調べる場合。利用元を直接読む。
- realization 側と利用者向け公開面から `basic.struct_doc` 参照が既になく、互換再公開の内容確認が不要な場合。

## hash
- 30e7080d603dfe06e6a8b58c8be36b17cbf95965ac706da3291269a56c890772
