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
- oracle 側で定義された cmoc 設定クラス群を realization 側から再公開する薄い互換モジュール。設定定義自体は保持せず、既存の `config.cmoc_config` 参照を維持するための入口である。

## Read this when
- cmoc 設定クラスの realization 側での公開名や import 入口を確認するとき
- `config.cmoc_config` 参照の削除可否や互換モジュールの整理条件を検討するとき

## Do not read this when
- 設定項目の具体的な定義や仕様を確認したいときは、oracle 側の設定定義を直接読む
- 設定を利用する各機能の挙動を確認したいときは、利用側の実装やテストを直接読む

## hash
- 6128860f37625e59c3ec35de62e161cb9b697d7bc25b4b8e4f251fb13608ce42
