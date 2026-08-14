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
- oracle investigation の launch TUI 用 agent-call parameter を生成する realization adapter。正本 builder を呼び出す前に、完全な prompt の保存先となる editor input log directory を repository 上に作成し、生成結果をそのまま返す。正本 builder の実装へ進む前段の入口として読む。

## Read this when
- oracle investigation の launch TUI 呼び出し用 parameter 生成処理を確認・変更するとき
- 正本 builder の呼び出し前に必要な runtime directory 準備の責務を確認するとき

## Do not read this when
- launch TUI 用 parameter の具体的な prompt 構築仕様を確認したいときは、直接正本 builder を読む
- editor input log のパス解決や runtime path の詳細だけを確認したいときは、対応する path/runtime 定義を直接読む

## hash
- 84f29eabc6b8a1cc25b3b31cba1fde159625cc294e42370a7ffd79129000e482
