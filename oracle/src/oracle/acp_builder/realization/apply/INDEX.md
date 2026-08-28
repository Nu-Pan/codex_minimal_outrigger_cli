# `fork`

## Summary
- `cmoc realization apply fork` における、oracle file の commit 差分を realization file へ追従させる AgentCallParameter と prompt の構築入口。
- commit 範囲と oracle file の raw git diff を追従対象として埋め込み、リポジトリ全体の関連ファイルを調査・更新・検証する起動条件を定義する。
- realization write モード、作業ディレクトリ、実行前インデックス処理など、差分追従 agent call の実行パラメータを確認する対象。

## Read this when
- fork 間の oracle file 差分を realization file へ反映する agent call の prompt や起動パラメータを確認・変更するとき。
- commit 範囲、raw oracle git diff、realization file 全体調査、realization implementation・test・ancillary の更新および検証方針を確認するとき。

## Do not read this when
- 通常の realization file の実装やテストの内容を直接確認・変更したいとき。
- 差分追従以外の realization apply 起動経路や、一般的な prompt 構築処理を調べたいとき。

## hash
- 8e48ff3082fa28872f6d11301d14a27333bab24c99f712e67876b623ee554e8f
