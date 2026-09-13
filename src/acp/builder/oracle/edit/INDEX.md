# `__init__.py`

## Summary
- `cmoc oracle edit` builder の realization adapter package。対象パッケージの入口として、oracle edit 用 builder 実装を扱う。

## Read this when
- `cmoc oracle edit` の builder adapter の責務や実装入口を確認するとき。

## Do not read this when
- oracle edit の具体的な編集処理や CLI 全体の動作を確認したいとき。対象の実装ファイルや上位の CLI 関連ファイルを直接読む。

## hash
- aceb2892c60c365c1ab63b37a6a8264fbaf18cc2d0e146e7f8d370741f78ac55

# `fork`

## Summary
- 内容がない空ディレクトリで、現時点では案内対象となる実装・テスト・補助ファイルを含まない。

## Read this when
- このディレクトリにファイルが追加されたか確認するとき。

## Do not read this when
- 既存の実装やテストを調査するとき。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `launch_exec.py`

## Summary
- oracle edit の正本 exec builder へ到達する互換 import 経路を提供する。

## Read this when
- oracle edit の起動 exec parameter builder を、この互換経路から import する必要があるとき。

## Do not read this when
- 正本 builder の実装や挙動を確認・変更するときは、参照先の正本モジュールを直接読む。

## hash
- bee79dd76db49ad009b73aec73e6fb73843ea6fb66e8dde551e967d1019e7195
