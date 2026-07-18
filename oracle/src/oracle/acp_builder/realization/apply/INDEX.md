# `fork`

## Summary
- `cmoc realization apply fork` の TUI 起動パラメータを構築する oracle source。oracle 差分追従用の完全 prompt を生成・保存し、最高品質設定の AgentCallParameter を返す。

## Read this when
- `cmoc realization apply fork` の TUI 起動処理、差分追従 prompt、AgentCallParameter の設定を変更・検証するとき。
- 対象 commit 範囲や raw oracle diff を realization 追従 agent へ渡す流れを確認するとき。

## Do not read this when
- 通常の realization apply 処理や fork 以外の起動経路を調べるとき。
- 完全 prompt の構成要素や共通 prompt 処理を直接調べるときは、対象の prompt builder・構造化文書実装を先に読む。

## hash
- 8187f4a51b4d804c11fdf5cce7f3f82b45d28634375d8002b2764edac7dcabea
