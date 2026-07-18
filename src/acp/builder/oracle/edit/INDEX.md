# `__init__.py`

## Summary
- `cmoc oracle edit` builder の realization adapter package。対象パッケージの入口として、oracle edit 用 builder 実装を扱う。

## Read this when
- `cmoc oracle edit` の builder adapter の責務や実装入口を確認するとき。

## Do not read this when
- oracle edit の具体的な編集処理や CLI 全体の動作を確認したいとき。対象の実装ファイルや上位の CLI 関連ファイルを直接読む。

## hash
- aceb2892c60c365c1ab63b37a6a8264fbaf18cc2d0e146e7f8d370741f78ac55

# `launch_tui.py`

## Summary
- oracle edit TUI 用の realization adapter。実行時の editor input 保存先ディレクトリを作成したうえで、正本 builder に完全な AgentCallParameter の生成を委譲する。

## Read this when
- oracle edit TUI の起動パラメータ生成や、editor input 保存先の準備処理を変更・確認するとき。

## Do not read this when
- 正本 builder の prompt 構築仕様そのものを確認するときは、対応する oracle builder を直接読む。
- editor input ディレクトリのパス定義を確認するときは、runtime path 定義を直接読む。

## hash
- 31d0d75fce702d13def856b79200196a9b7a355c4b5005759a219dfea26c3618
