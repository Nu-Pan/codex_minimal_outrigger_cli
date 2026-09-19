# `launch_tui.py`

## Summary
- `cmoc oracle investigation` の完全 prompt と read-only TUI 起動パラメータを構築する正本 builder。oracle 限定の読み取り範囲、パス情報、エディタ入力引き継ぎ、indexing preflight などを調査実行条件へまとめる。

## Read this when
- oracle investigation の agent 起動条件、調査 prompt の構成、oracle の読み取り専用境界を確認・変更するとき
- oracle investigation 用の TUI 起動パラメータが、入力指示や実行前処理をどう引き渡すか確認するとき

## Do not read this when
- oracle investigation の CLI 入力編集から builder 呼び出しまでの実行順序を確認したいときは、サブコマンド実装を直接読む
- 互換 import adapter の構成や移行状況を確認したいときは、acp 側の adapter を読む
- oracle investigation の具体的な調査内容や oracle 文書の仕様を確認したいときは、対象の oracle 文書を直接読む

## hash
- 28ed0f4a6ff3ec4c848e616c9693ca045c2b38d6144afc5e9a2634373d446ba2
