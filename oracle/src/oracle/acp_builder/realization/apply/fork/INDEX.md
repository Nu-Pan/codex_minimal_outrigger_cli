# `launch_exec.py`

## Summary
- `cmoc realization apply fork` における追従用 AgentCallParameter の構築を担う。差分対象の commit 範囲と oracle file の raw git diff を prompt に組み込み、realization file への反映を依頼する完全 prompt と、実行に必要なモデル・推論強度・ファイルアクセス・作業ディレクトリなどの起動設定をまとめる。realization の差分追従起動条件や、oracle file の変更を realization 全体へ反映する処理を確認・変更するときの入口となる。

## Read this when
- `cmoc realization apply fork` の起動時に、差分追従用 prompt の内容や AgentCallParameter の設定を確認するとき
- 追従対象の commit 範囲、oracle diff、linked worktree が agent call にどう渡されるかを調査するとき
- realization file の差分追従に必要なモデル、アクセスモード、実行前 indexing の設定を変更するとき

## Do not read this when
- 通常の realization 実装・テストの挙動を確認する場合は、対象の realization file や test file を直接読む
- 一般的な prompt 生成や共通の AgentCallParameter 構築規則を確認する場合は、対応する共通 builder や oracle file を直接読む
- `cmoc realization apply fork` 以外の起動経路を調査する場合は、その経路の launch 定義を読む

## hash
- 0c7d5b02b5b7cb35f6298307c1e4272087f21c04d4ca0ba2b5c5b4a5b7a37ad4
