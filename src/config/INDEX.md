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
- `oracle.other.cmoc_config` の設定定義を `config.cmoc_config` から再公開するための入口。実体の設定定義をここで複製せず、既存の公開参照を維持したいときに読む。

## Read this when
- `config.cmoc_config` から Cmoc 系の設定型を参照したい。
- 設定定義の実体を別に持たず、既存の公開面をそのまま使う構成を確認したい。

## Do not read this when
- 設定定義そのものの内容や項目の意味を確認したい。
- `config.cmoc_config` 以外の設定公開や新規設定追加を扱いたい。

## hash
- 8c04baeba97ac2c81cf42b9327a888a80d36f05b205fce45afa59f603dd35675
