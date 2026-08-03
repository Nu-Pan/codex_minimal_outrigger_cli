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
- oracle edit 用の TUI 起動パラメータを生成する realization adapter。リポジトリ実パスを解決し、完全な prompt の保存先となる editor input directory を準備したうえで、oracle 側の builder を呼び出す。

## Read this when
- oracle edit の TUI 起動パラメータ生成や、その前提となる editor input directory の準備を確認・変更するとき
- realization 側から oracle edit の正本 builder を呼び出す経路を追跡するとき

## Do not read this when
- oracle 側の TUI builder の prompt 内容や本体ロジックを直接確認するとき
- oracle edit や TUI 起動パラメータと無関係な builder、パス解決、実行時処理を調べるとき

## hash
- 7ae5d0a9e77b7cc62a050f8eb6bba220dcc501423e1bbf47bb6361478ecfe557
