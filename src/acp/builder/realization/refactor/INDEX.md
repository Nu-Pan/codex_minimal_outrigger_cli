# `__init__.py`

## Summary
- realization refactor 用の builder adapter パッケージ。refactor 処理の builder 関連実装へ進む入口。

## Read this when
- realization refactor の builder adapter の責務や実装入口を確認するとき。

## Do not read this when
- builder adapter 以外の refactor 処理を確認するとき。

## hash
- 4c331bccb54a9842893b30e509c994292dd25afbf1159ad4b7929ebffb3a311d

# `fork`

## Summary
- cmoc realization refactor fork 向けの builder adapter 群をまとめるパッケージ。change summary と file review/fix の agent call parameter 生成入口を提供し、具体的な生成処理は oracle 側実装へ委譲する。

## Read this when
- realization refactor の fork 処理における builder adapter の公開入口や、change summary・file review/fix の parameter 生成経路を変更・調査するとき。

## Do not read this when
- fork 以外の builder 実装を調査するとき。
- builder の正本仕様や具体的な生成ロジックを確認したいときは、対応する oracle 側実装を直接読む。

## hash
- 53f3caf3dbae55590b444010c031761dafa68c2d1596ebac139c9495ebf37af6
