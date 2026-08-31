# `launch_exec.py`

## Summary
- `cmoc realization apply fork` の prompt 文面と AgentCallParameter の起動パラメータを構築する定義。
- 指定された commit 範囲と oracle file の raw git diff を追従対象変更として prompt に埋め込み、realization file への反映作業を起動する入口。

## Read this when
- `cmoc realization apply fork` の AgentCallParameter、prompt、作業範囲、完了条件、ファイルアクセスモードの構築を確認したいとき。
- commit 間の oracle file 差分を realization file 全体へ反映する Agent call の起動条件を確認したいとき。

## Do not read this when
- oracle file の変更内容そのものや realization file への具体的な反映方法を確認したいとき。
- 個別の prompt 部品や SD ノードの一般的な構築仕様を直接確認したいとき。

## hash
- 3b9f30483c05c09c9d0854875d9517c65052d4aa832d43485df882551b6f1b69
