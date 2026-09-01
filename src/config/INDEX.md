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
- oracle 側で定義された cmoc 設定型を realization 側から再公開する互換用モジュール。
- 設定定義を複製せず、既存の config.cmoc_config 参照を維持する入口。

## Read this when
- cmoc 設定の公開型を realization 側の config.cmoc_config 経由で確認するとき。
- config.cmoc_config 参照の所在や、互換用の設定型再公開を調べるとき。

## Do not read this when
- 設定型の定義や設定値の仕様を確認したいときは、再公開元の oracle 側設定定義を直接読む。
- config.cmoc_config の参照が realization 側と利用者向け公開面からなくなり、モジュールの削除条件だけを確認するとき。

## hash
- e143f75a879b3dc46fb34ebbab3e7e3a0cf88bb6d8e061e1f98dfb2859e1aa87
