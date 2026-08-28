# `launch_exec.py`

## Summary
- `cmoc realization apply fork` の差分追従用 AgentCallParameter と prompt を構築する定義。始点・終点 commit と oracle file の raw diff を追従対象として埋め込み、リポジトリ全体の realization file を調査・更新・検証する agent call の入口。

## Read this when
- fork 間の oracle file 差分を realization file へ反映する agent call の prompt、権限、作業ディレクトリ、起動時インデックス処理を確認・変更するとき。
- commit 範囲や raw oracle diff の構造化、realization write モード、realization 関連ポリシーの指定を確認するとき。

## Do not read this when
- 通常の realization 実装やテストの内容を直接変更・確認したいときは、該当する realization file またはその作業規定を読む。
- fork 差分追従ではなく、別の realization apply 起動経路や一般的な prompt 構築を調べるとき。

## hash
- 4d6b52e9d1bf7589e2765d00d925069ec7496b2fe906c647a574c3af1bbeb486
