# `launch_tui.py`

## Summary
- `cmoc realization apply fork` 用 TUI 起動パラメータを構築する oracle source。oracle 差分追従の完全 prompt を生成してログへ保存し、最高品質設定の AgentCallParameter を返す。

## Read this when
- `cmoc realization apply fork` の TUI 起動処理、差分追従 prompt、AgentCallParameter の設定を変更・検証するとき。
- 対象 commit 範囲や raw oracle diff を realization 追従 agent へ渡す流れを確認するとき。

## Do not read this when
- 通常の realization apply 処理や fork 以外の起動経路を調べるとき。
- 完全 prompt の各構成要素や prompt 共通処理を直接調べる場合は、対象の prompt builder・構造化文書実装を先に読むとき。

## hash
- 444724c9d11124d39d74254cedb12a34e5b3527646ec50bc629cc80f4279bdf4
