# `fork`

## Summary
- `cmoc apply fork` 向けに、差分要約、ファイル単位の所見列挙、検出所見への対応作業を行う AI エージェント呼び出しパラメータと、それらが返す Structured Output schema を扱う。
- git diff 由来の変更サマリー、人間へ渡すレビュー所見リスト、所見対応エージェント用 prompt など、apply fork のレビュー・報告段階で使う oracle src と出力契約への入口になる。

## Read this when
- `cmoc apply fork` で、fork 適用後の差分を要約したり、realization file の要修正点を列挙したり、所見対応作業を別エージェントへ渡したりする prompt や AgentCallParameter の正本仕様を確認したいとき。
- 差分要約やレビュー所見の Structured Output schema について、出力互換性、必須の根拠情報、空でない前提、主要変更箇所や修正方針の粒度を確認したいとき。
- apply fork のレビュー・報告系 agent call に渡す role、summary、goal、file access mode、model class、reasoning effort、placeholder、標準文書の組み込み方を変更または検証したいとき。

## Do not read this when
- `cmoc apply fork` の fork 作成、適用、branch 操作、git 操作、作業レポート保存など、レビュー・報告用 agent call より前後の実行フローを調べたいとき。
- 個別ファイルのパッチ内容、diff 生成手順、実際の realization file 修正結果、または所見の統合・実行結果処理を確認したいとき。
- apply fork 以外のサブコマンドの prompt、AgentCallParameter、共通部品の実装詳細、または一般的なルーティング文書の書き方を探しているとき。

## hash
- 28f66aa79cf3c48a0d66f247642a2aa7007c67983766b6344a9e0c304d6fd2ff
