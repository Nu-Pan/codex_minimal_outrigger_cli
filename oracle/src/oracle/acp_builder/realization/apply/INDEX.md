# `fork`

## Summary
- `cmoc realization apply fork` 用の完全な作業 prompt と AgentCallParameter を構築する入口。
- 指定 commit 範囲、linked worktree、realization 書き込み権限、実行前 indexing、oracle file 変更の差分追従条件を結び付ける。

## Read this when
- `cmoc realization apply fork` が差分追従 agent を起動する際の prompt と AgentCallParameter の構築経路を確認するとき。
- 指定 commit 範囲から oracle file の変更を判定し、rename・追加・削除・oracle 配下外への移動を含めて realization file へ反映する作業条件を確認するとき。
- realization 書き込み権限、linked worktree、実行前 indexing、差分取得失敗時の完了条件を確認するとき。

## Do not read this when
- `cmoc realization apply fork` の実行処理、Git 差分取得そのもの、または realization file への具体的な反映処理を調べるとき。
- 共通の prompt 構築処理や AgentCallParameter の一般仕様だけを確認するとき。

## hash
- e3625e501d3af9ba014ed26f875ed628355f29e89c30552980b479f818ff0044
