# `launch_exec.py`

## Summary
- `cmoc realization apply fork` の realization 追従 AgentCallParameter を構築する定義。追従対象の commit 範囲と oracle file の raw git diff を prompt に組み込み、run worktree、ファイルアクセス権限、モデル設定、preflight などの起動条件をまとめる。apply fork の差分追従 prompt や AgentCall の起動設定を確認・変更するときの入口。

## Read this when
- `cmoc realization apply fork` の agent call が参照する prompt の構成や起動パラメータを変更するとき
- oracle file の差分を realization file へ追従させる agent call の作業範囲、権限、worktree、モデル、preflight 設定を確認するとき

## Do not read this when
- realization file の個別実装やテストの挙動を変更するとき
- apply fork の実行処理そのものや、別の agent call 種別の prompt・起動条件を調査するとき

## hash
- 92a0426a19d23be259f11928c04f3755b6445315788c0d531c01594970928fad
