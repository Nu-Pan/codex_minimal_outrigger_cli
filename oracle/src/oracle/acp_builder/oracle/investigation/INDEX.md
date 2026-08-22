# `launch_tui.py`

## Summary
- `cmoc oracle investigation` 用の完全プロンプトと Codex CLI TUI 起動パラメータを構築する実装。oracle file の読み取り専用調査に必要な作業範囲、目的、ユーザー指示の埋め込み、モデル・推論強度・作業ディレクトリ・索引事前処理などの固定条件をまとめて定義する。調査起動条件や prompt 構成の入口として読む。

## Read this when
- `cmoc oracle investigation` の TUI 起動パラメータを変更または確認するとき
- oracle file 調査用の完全プロンプトに、ユーザー指示や読み取り専用の作業範囲をどう組み込むか確認するとき
- 調査起動時のモデル、推論強度、作業ディレクトリ、indexing preflight などの固定条件を確認するとき

## Do not read this when
- oracle file 調査そのものの正本仕様や調査対象の内容を確認したいときは、関連する oracle file を直接読む
- 一般的な TUI 起動処理や `AgentCallParameter` の共通定義を確認したいときは、該当する共通実装を直接読む
- `cmoc oracle investigation` 以外のコマンドの prompt や起動パラメータを確認したいとき

## hash
- eb047c9da87829932af5ef6b666ab672b4d759240c85e9e18bece40bca3293ad
