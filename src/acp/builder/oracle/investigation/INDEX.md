# `__init__.py`

## Summary
- `cmoc oracle investigation` 用 builder adapter パッケージの入口。oracle investigation 向け builder 機能へ進む際の参照先。

## Read this when
- oracle investigation 用 builder adapter の構成や入口を確認するとき
- 該当パッケージ内の下位実装へ進む前に責務を確認するとき

## Do not read this when
- builder adapter の具体的な実装詳細を確認したいとき
- oracle investigation 以外の builder や ACP 実装を調べるとき

## hash
- c4c41f07d0b59e430e93561b97dcc2321301abc3cedb93fdeb0ef16a0c9a9637

# `launch_tui.py`

## Summary
- oracle investigation の正本 builder を呼び出す realization adapter。リポジトリの editor input directory を作成したうえで、時刻とユーザー指示から AgentCallParameter を生成する。

## Read this when
- oracle investigation の launch TUI 用パラメータ生成 adapter の処理や、editor input directory の準備を確認するとき
- adapter が正本 builder に渡す引数や公開関数を変更するとき

## Do not read this when
- oracle investigation の prompt 内容や AgentCallParameter の組み立て規則そのものを確認するときは、正本 builder を直接読む
- launch TUI 以外の builder や runtime path の一般的な仕様だけを確認するとき

## hash
- d2a33a34b2d4a0aa7c8c9fab4e00610dfea789de5e256651669d71a797296919
