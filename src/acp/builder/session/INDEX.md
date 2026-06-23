# `join`

## Summary
- `cmoc session join` で merge conflict marker 解消専用のエージェント呼び出しパラメータを組み立てる領域。解消対象パスを実パスへ解決して prompt に埋め込み、conflict marker 解消に限定した役割・目標・ファイルアクセス制約を complete prompt として構成する。
- join 処理から conflict marker 解消エージェントへ渡す parameter の入口であり、model、reasoning、realization write の扱いと生成 prompt の内容を確認するための読み先。

## Read this when
- `cmoc session join` の conflict marker 解消用エージェント呼び出し内容を確認または変更したいとき。
- conflict 対象ファイル一覧が prompt にどう埋め込まれるか、実パス解決や work root 表示の扱いを確認したいとき。
- merge conflict 解消だけを goal にする指示、git add/commit 禁止、oracle file の例外的な最小編集許可などの制約文を調整したいとき。
- session join の join 処理から conflict marker 解消用 parameter を生成する流れを追う入口が必要なとき。

## Do not read this when
- 通常の session join 実行フロー、merge 実行、conflict marker 検出、または join 後処理そのものを調べたいとき。
- complete prompt の共通組み立て仕様、markdown rendering、エージェント呼び出しパラメータの型定義を調べたいとき。
- conflict 解消プロンプトではなく、session join の別用途の prompt や他サブコマンド用のエージェント呼び出しパラメータを調べたいとき。
- real path や work root の定義、パスキーワードの意味、パス解決処理そのものを確認したいとき。

## hash
- 53f7c2a619ad1fe2dc649785825ad617a867006419881f90090b32ffe974c98a
