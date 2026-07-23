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
- oracle investigation 用の完全な AgentCallParameter を正本 builder に委譲する realization adapter。実行前にリポジトリを解決し、editor input 用ディレクトリを作成する。investigation launch TUI のパラメータ生成処理への入口。

## Read this when
- oracle investigation の launch TUI 用 builder や AgentCallParameter 生成の呼び出し経路を確認するとき
- editor input ディレクトリの準備を含む investigation 起動処理を変更・調査するとき

## Do not read this when
- 正本 builder の prompt 内容や investigation 起動仕様そのものを確認したいとき
- investigation 以外の builder、TUI 実装、または共通パス解決処理だけを調査するとき

## hash
- 07ca68e21555887974b0773ecaf88d5e8e751de8df8ad6f5bb2839a7ce6d86a6
