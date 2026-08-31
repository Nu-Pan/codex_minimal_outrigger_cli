# `fork`

## Summary
- realization apply fork 用 AgentCallParameter の prompt と起動設定を構築する定義。
- commit 範囲と oracle file の raw git diff を追従対象変更として埋め込み、リポジトリ全体の realization file への反映作業へ接続する入口。

## Read this when
- `cmoc realization apply fork` がどのように作業範囲、完了条件、ファイルアクセスモード、linked worktree を Agent call に設定するか確認したいとき。
- oracle file の差分をもとに realization file 全体の追従作業を起動する条件と prompt 構成を確認したいとき。

## Do not read this when
- oracle file の差分内容や realization file の具体的な修正内容を確認したいとき。
- 共通の prompt 生成処理、構造化文書ノード、AgentCallParameter の一般仕様を直接確認したいとき。

## hash
- 9b5bb7c1d15a15a2f1e6b01ebd7bc5600ac931eda6040b7ddd8381a22b81b8a2
