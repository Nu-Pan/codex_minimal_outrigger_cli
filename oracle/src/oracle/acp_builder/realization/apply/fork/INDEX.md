# `launch_exec.py`

## Summary
- `cmoc realization apply fork` 実行時に、差分追従用の `codex exec` 用 AgentCallParameter を構築する正本コード。oracle file の変更範囲・raw git diff・実行用 worktree を prompt に組み込み、realization file 全体への反映作業を委譲する。
- prompt の役割・依頼概要・完了条件、ファイルアクセス権、oracle/realization 関連標準、レビュー標準を設定し、最高品質のモデル・推論設定と linked worktree を指定する。

## Read this when
- `cmoc realization apply fork` の `codex exec` 起動条件、prompt 構成、差分追従範囲を確認するとき
- oracle file の変更を realization file 全体へ反映する AgentCallParameter の生成方法を変更・検証するとき
- 実行用 worktree、commit 範囲、raw oracle diff の prompt への渡し方を調査するとき

## Do not read this when
- 通常の realization 実装やテストの内容を調査するとき
- `cmoc realization apply fork` 以外の agent call prompt や起動処理を調査するとき
- oracle file と realization file の具体的な追従実装そのものを調査するときは、対象の realization file や関連する prompt 定義を直接読む

## hash
- 86d784805419faabd4cebe70061b25b40bcc2abf2d8cad19e8772098921b6ad8
