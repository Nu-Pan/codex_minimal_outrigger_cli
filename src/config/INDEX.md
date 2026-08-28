# `__init__.py`

## Summary
- `config.*` 参照を受ける互換入口。設定の正本は `{{work-root}}/oracle/src/oracle/other/cmoc_config.py` 側にあり、ここは既存利用者の参照先を成立させるためだけに読む。

## Read this when
- `config` からの import を維持する必要があるとき。
- 設定の正本を変更せず、互換入口の有無だけを確認したいとき。

## Do not read this when
- 設定仕様そのものを確認したいときは、正本側の oracle src を読む。
- `config.*` 参照を新規に増やす実装判断をしたいだけなら、ここではなく利用側の参照経路を直接見る。

## hash
- 2df099916bfadae1547b9bb803be4606e032bc2d738c77e453dddf5756e2dece

# `cmoc_config.py`

## Summary
- oracle 側で定義された cmoc 設定型を realization 側で再公開する互換層。設定定義を複製せず、既存の config.cmoc_config 参照を維持する。

## Read this when
- realization 側や利用者向け公開面で CmocConfig などの設定型を参照する入口を確認したいとき。
- 設定型の定義元を確認し、参照先を oracle.other.cmoc_config に統一したいとき。

## Do not read this when
- 設定型の構造や値の定義そのものを確認したいときは、oracle.other.cmoc_config を直接読む。
- config.cmoc_config 参照が realization 側と利用者向け公開面からなくなり、互換層の削除条件だけを確認するとき。

## hash
- 349e327305182d50ab0a10cbdc9722d4e9acf663baeb3d28b6a3a6780d95b6a0
