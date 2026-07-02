# `__init__.py`

## Summary
- oracle src の basic 互換 import 入口を示す。`basic.*` 参照を残す必要がある間、正本側の実体 module や ACP 基本型を複製せず参照互換性を保つための補助 module。

## Read this when
- `basic.*` import の互換維持、削除可否、または正本側・実体 module への移行状況を確認したいとき。
- oracle src の実体を複製せずに既存参照を保つための入口を確認したいとき。

## Do not read this when
- oracle src の実体定義や ACP 基本型そのものを確認したいとき。
- `basic.*` 参照の互換性や移行条件に関係しない実装詳細を調べたいとき。

## hash
- bd7e89dfb56983290190c9facb93f671f397b370fc9ea0fb32052b0bc819b591

# `acp.py`

## Summary
- ACP builder の正本型を再公開し、既存の `basic.acp` 参照を保つための互換入口を提供する。
- 正本型を realization 側へ複製せず、oracle 側の定義をそのまま参照するための薄い公開面である。

## Read this when
- `basic.acp` 経由で利用される ACP 関連型の公開面を確認したいとき。
- 正本型を複製せずに oracle 側の ACP 型を参照する互換経路を調べるとき。
- `basic.acp` 参照を削除できるかどうかを判断するため、残存理由と削除条件を確認したいとき。

## Do not read this when
- ACP 型そのものの定義や列挙値を確認したいとき。その場合は oracle 側の正本定義を読む。
- ACP builder の生成処理や呼び出しロジックを調べたいとき。
- `basic.acp` 互換公開面に関係しない realization 実装を変更するとき。

## hash
- de511dc6ae0bf66bbe04c2916d62b5268565b3e4ecdd7da73137fc3bb6174faa

# `path_model.py`

## Summary
- 公開 path model の互換用再公開モジュール。正本実装を複製せずに oracle 側の path model 定義を参照し、既存の `basic.path_model` 利用を維持するための入口。

## Read this when
- `basic.path_model` 経由で公開される path placeholder 解決 API の互換維持を確認したいとき。
- realization 側で oracle 側 path model を複製せず参照している箇所を確認したいとき。
- `basic.path_model` 参照を削除できるか、または公開面から外せるかを判断したいとき。

## Do not read this when
- path model の正本定義や具体的な解決ロジックを確認したいときは、oracle 側の公開 path model 実装を読む。
- 新しい path 解決仕様や挙動差を検討したいだけで、互換用再公開の要否に関係しないとき。

## hash
- 3ef925dfd0d7897d6364bb284d1591c7c6844ad7ea64df15894d9b69ecbca164

# `struct_doc.py`

## Summary
- 構造化文書の型・描画関数を、正本実装を複製せず既存の公開参照名から使えるように再公開する互換モジュール。
- 正本側の構造化文書実装への薄い入口であり、利用者向け公開面に残る参照を支えるためだけに存在する。

## Read this when
- 既存の公開参照名から構造化文書 API を利用する経路を確認したいとき。
- 構造化文書実装を複製せず正本側へ委譲している互換層の削除可否を判断したいとき。
- 構造化文書関連の公開シンボルがどこから再公開されているかを確認したいとき。

## Do not read this when
- 構造化文書 API の実装内容や markdown 描画ロジックを確認したいときは、正本側の実装を読む。
- 新しい構造化文書仕様や挙動を追加したいときは、この再公開層ではなく正本側の仕様・実装を確認する。
- 互換参照の有無ではなく、一般的な補助モジュール全体の構成を調べたいだけのとき。

## hash
- 30e7080d603dfe06e6a8b58c8be36b17cbf95965ac706da3291269a56c890772
