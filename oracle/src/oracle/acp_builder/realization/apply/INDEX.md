# `fork`

## Summary
- realization の差分追従用 agent call の prompt と AgentCallParameter を構築し、指定された commit 範囲、作業用 worktree、文書検索範囲、書き込み条件を反映する。
- oracle file の変更をリポジトリ全体の realization file に反映するタスクと、追従対象差分の取得・判定方法を agent に指示する。

## Read this when
- realization apply fork の agent に渡す作業内容や、commit 範囲・worktree・検索範囲の指定を調べたり変更したりするとき。
- oracle file の追加・削除、rename、oracle 領域内外の移動を差分追従でどう扱うか確認するとき。

## Do not read this when
- agent call の実際の起動や commit 範囲・worktree の決定を調べるとき。この対象は prompt と起動パラメータの構築を担うため、起動側や範囲決定側を読む。
- 特定の差分や現在の realization 実装の内容を調べるだけなら、対象となる commit 範囲のファイルを直接読む。

## hash
- fe522fe3ce2e68c68cbdcf51805a70ce642c1cbbb697d232d10b089e4d272593
