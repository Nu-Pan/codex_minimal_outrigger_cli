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
- `cmoc oracle edit fork` の builder adapter を提供するディレクトリ。fork 編集処理の入口と、launch_exec 用 builder の realization 側再公開経路を扱う。

## Read this when
- `cmoc oracle edit fork` の builder adapter の責務や実装入口を確認するとき。
- launch_exec パラメータ builder の realization 側エントリーや再公開経路を確認するとき。

## Do not read this when
- `cmoc oracle edit fork` 以外のコマンドを確認するとき。
- builder adapter 以外の処理、builder の正本仕様・実装詳細、launch_exec 以外の builder や fork 処理を調べるとき。

## hash
- 68269ac1918c240cd4d2b95c70a62b0dbb5068d06824f52c0c325f8b7d987a9f
