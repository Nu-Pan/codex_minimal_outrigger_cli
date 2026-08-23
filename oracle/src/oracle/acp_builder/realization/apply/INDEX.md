# `fork`

## Summary
- oracle の変更を realization へ反映する差分追従 Agent の起動定義。始点・終点 commit 間の raw git diff と対象 oracle file を prompt に組み込み、対象 worktree、書き込み権限、モデル・推論設定、起動時 indexing を指定する。この配下で差分追従 Agent の起動条件や prompt 連携を確認・変更する際の入口。

## Read this when
- oracle file の変更を realization file へ反映する Agent の prompt や起動パラメータを調査・変更するとき
- realization_apply_change の commit 範囲や oracle file の差分を Agent prompt に渡す処理を確認するとき

## Do not read this when
- 個別の oracle file または realization file の実装内容を直接調査するとき
- AgentCallParameter の共通仕様や prompt の共通生成処理だけを確認するときは、それぞれの定義元を直接読む

## hash
- deb03c9451e82a8ca399fd18b9807b8d40bd3d1c141843c9c518f68aa4c18719
