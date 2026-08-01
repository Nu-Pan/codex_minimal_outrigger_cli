# `fork`

## Summary
- Oracle の変更差分を埋め込んだ realization 追従用の完全 prompt と AgentCallParameter を構築する。linked worktree、commit 範囲、realization write 権限、モデル設定、事前 indexing を含む agent call の起動設定を担う。

## Read this when
- oracle file の変更を realization implementation・test・ancillary 全体へ反映する agent call の起動条件や prompt を変更するとき。
- realization apply fork の実行 cwd、差分情報、権限、モデル・推論設定を確認するとき。

## Do not read this when
- 通常の realization 実装やテストの内容を変更するとき。
- oracle の仕様や共通 prompt 構築処理を確認するときは、対応する oracle file や prompt builder を直接読む。

## hash
- 2f2df60b09b88d45b02e29970cd4304b79fedbe954701daf164b03a64414e47d
