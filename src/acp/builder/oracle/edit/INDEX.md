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

# `launch_tui.py`

## Summary
- oracle edit の TUI 起動パラメータを生成する realization adapter。正本 builder の呼び出しに先立ち、完全 prompt の保存先となる editor input log directory を作成する。

## Read this when
- oracle edit の TUI 起動処理で、realization 側の directory 準備と正本 builder の接続責務を確認するとき

## Do not read this when
- 正本 builder の prompt 内容や TUI 起動パラメータ生成の詳細を確認するとき
- editor input log directory の管理だけを確認するとき

## hash
- 66998a41cec97f194635d83f36727e99cd286668e6c1190ffe51e99040f86a8c
