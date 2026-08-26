# `launch_exec.py`

## Summary
- `cmoc realization apply fork` 実行用の AgentCallParameter を構築する関数を定義する。コミット範囲と oracle file の raw git diff を構造化した追従対象変更として prompt に埋め込み、realization file の差分追従を依頼する。
- リンク済み worktree を agent call の作業ディレクトリに設定し、realization write 権限、flagship モデル、最大推論 effort、ルーティング事前処理などの起動パラメータをまとめて返す。

## Read this when
- `cmoc realization apply fork` の prompt 文面や AgentCallParameter の起動設定を変更・確認するとき
- oracle file の変更を realization file 全体へ反映する Agent call の作業範囲、権限、検証方針を確認するとき

## Do not read this when
- 通常の realization implementation や realization test の具体的な実装を変更するとき
- `cmoc realization apply fork` 以外の起動パラメータ構築を確認するときは、対象となる各 launch 定義を直接読む

## hash
- b10dda47869c60fff9a767d934f05080d39426d2e8427d88c30db4eff933f7e4
