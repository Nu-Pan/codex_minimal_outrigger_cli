# `join`

## Summary
- session join のマージ競合で使う agent call の prompt と起動条件を組み立てる定義。競合対象の指定や、適用する共通・マージ用の規定、事前処理の選択を確認する入口。

## Read this when
- session join の競合解消 agent call の指示内容や起動設定を変更・確認するとき。
- 競合対象の渡し方、適用する規定、indexing preflight の有無など、この call 固有の選択理由を確認するとき。

## Do not read this when
- session join 全体の手順や git merge 後の処理を確認するときは、session join の仕様またはコマンド実装を参照する。
- 競合解消で保持すべき意図や、解消結果の意味上の優先順位を確認するときは、session join 仕様の該当節を参照する。

## hash
- 9a895c2c67fed3d039706710c7e4a84cf716a5308c1cdc9e41dd1ff9c46e9ee3
