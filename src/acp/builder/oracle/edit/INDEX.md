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
- oracle edit 用の TUI 起動パラメータを生成する realization adapter。リポジトリの実パスを解決し、完全な prompt の保存先ディレクトリを作成したうえで、oracle 側の正本 builder に処理を委譲する。

## Read this when
- oracle edit の TUI 起動パラメータ生成、prompt 保存先の準備、または oracle builder への委譲経路を変更・調査するとき。

## Do not read this when
- oracle 側の prompt 構築仕様そのものを確認するときは、対応する oracle builder を直接読む。
- 他の ACP builder や TUI 以外の起動処理を調査するとき。

## hash
- 4ad26bd2026388f9bea1d1dc78e071bd09e3cf13e602472c5dc92d5e91803506
