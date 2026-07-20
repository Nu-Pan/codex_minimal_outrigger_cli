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
- oracle/src/oracle/other/cmoc_config.py の設定型を realization 側から再公開する互換用モジュール。設定定義自体は保持せず、既存の config.cmoc_config 参照を維持する。

## Read this when
- cmoc 設定型の import 経路や config.cmoc_config 参照を変更・確認するとき。

## Do not read this when
- 設定定義の内容や仕様そのものを確認するときは、再公開元の oracle/src/oracle/other/cmoc_config.py を直接読む。
- config.cmoc_config 参照が realization 側と利用者向け公開面からなくなっている場合。

## hash
- 46d78fa1d103a3d52db1f861d2187698122d2dde1940ff0b4c0d1a60ca7a87fa
