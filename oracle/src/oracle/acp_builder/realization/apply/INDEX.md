# `fork`

## Summary
- `realization apply fork` 用の AgentCallParameter を構築し、追従対象の commit 範囲と oracle file の raw git diff を完全 prompt に組み込む実装。
- run worktree を作業ディレクトリとして、realization file 全体の追従に必要なアクセス権、oracle/realization・レビュー・routing policy、モデルおよび推論設定を指定する起動処理への入口。

## Read this when
- `realization apply fork` の追従 agent が受け取る prompt、作業範囲、完了条件を変更または確認するとき
- oracle file の差分を realization file 全体へ反映する agent call の起動パラメータや run worktree の指定を調査するとき
- commit 範囲や raw git diff の prompt への埋め込みと、関連する realization policy の連携を確認するとき

## Do not read this when
- `realization apply fork` 以外の apply 処理を調査するとき
- 完全 prompt の共通生成規則を調査するときは、まず共通 prompt builder の定義を読むとき
- AgentCallParameter の共通データ構造や列挙値だけを調査するときは、基礎定義を直接読むとき
- 個別の oracle file、realization implementation、realization test の仕様や挙動を確認するときは、対象ファイルを直接読むとき

## hash
- 2c10ec315de6d06cd62ce47371476a3f9dd9aa3b6895eeb863da7dfc8ad79374
