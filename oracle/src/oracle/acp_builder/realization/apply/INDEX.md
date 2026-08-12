# `fork`

## Summary
- `cmoc realization apply fork` の差分追従処理に使う AgentCallParameter を構築する。commit 範囲と oracle file の raw git diff を完全 prompt に組み込み、realization file への反映条件と起動設定をまとめる。
- 差分追従用 prompt、realization 書き込み権限、作業ディレクトリ、モデル・推論強度、実行前 indexing など、単一の agent call に必要な設定を定義する。

## Read this when
- `cmoc realization apply fork` で oracle file の変更を realization file 全体へ反映する処理を確認・変更するとき
- 追従対象の commit 範囲や oracle diff が prompt にどう組み込まれるかを調査するとき
- 差分追従 agent call のモデル、推論強度、ファイルアクセス、linked worktree、実行前 indexing の設定を変更するとき

## Do not read this when
- 通常の realization 実装やテストの挙動を確認する場合
- 一般的な prompt 生成や共通の AgentCallParameter 構築規則を確認する場合
- `cmoc realization apply fork` 以外の起動経路を調査する場合

## hash
- 351c5c5cbbd098c245b8773c5ececd42660c1882595d726d826ac8c268357c57
