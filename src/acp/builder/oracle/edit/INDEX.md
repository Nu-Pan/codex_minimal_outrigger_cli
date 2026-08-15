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
- oracle edit 用の exec builder 関数を、正本実装から再公開する互換 import 経路。main launch と reduction launch の実行パラメータ生成を扱い、これらの関数を既存の ACP builder 配下から利用したい場合の入口となる。

## Read this when
- oracle edit の main または reduction 用 launch exec パラメータ生成関数の import 経路を確認・変更するとき。
- 正本実装ではなく、既存利用者向けの互換的な公開位置を確認するとき。

## Do not read this when
- oracle edit の exec builder の実装内容や挙動を変更・確認するときは、参照先の正本実装を直接読む。
- oracle edit 以外の launch exec builder を扱うとき。

## hash
- 92823c1681fff7cd05fd0241fc6feaa1950be8b3ca563e2ed2d327d95fb8504f
