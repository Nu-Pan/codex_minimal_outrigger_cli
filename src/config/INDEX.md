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
- oracle 側の設定定義クラスを realization 側の `config.cmoc_config` として再公開する互換ブリッジ。設定定義自体は複製せず、oracle の型を参照して利用者向け import 面を維持する。

## Read this when
- `config.cmoc_config` の設定クラス import や公開 API を変更・確認するとき。
- oracle 側の設定定義と realization 側の参照関係を確認するとき。

## Do not read this when
- 設定クラスの仕様や実装を確認したいときは、再公開元である oracle 側の設定定義を直接読む。
- 設定参照を利用する個別機能だけを変更するときは、この再公開モジュールではなく該当する利用側コードを読む。

## hash
- 9984eb91677d6d945b13c4d066cc6e2928fe2b933e4152300048b4ade9a9bcc3
