# `conflict_resolution.py`

## Summary
- `cmoc session join` で検出された merge conflict marker を解消するための AI エージェント呼び出しパラメータを構築する実装。
- 解消対象のパスを実パスへ解決して prompt に埋め込み、conflict marker 解消に限定した役割・目標・追加ファイルアクセス規則を complete prompt として組み立てる。
- 返却するパラメータでは mainstream model、medium reasoning、realization write のファイルアクセスモードを指定し、生成した markdown prompt を渡す。

## Read this when
- `cmoc session join` の conflict marker 解消用エージェント呼び出し内容を確認または変更したいとき。
- conflict 対象ファイル一覧が prompt にどう渡されるか、実パス解決や work root 表示の扱いを確認したいとき。
- merge conflict 解消作業に限定する goal、git add/commit 禁止、oracle file の例外的な最小編集許可などの指示文を調整したいとき。
- session join の join 処理から conflict marker 解消用 parameter を生成する流れを追う入口が必要なとき。

## Do not read this when
- 通常の session join 実行フロー、merge 実行、conflict marker 検出、または join 後処理そのものを調べたいとき。
- complete prompt の共通組み立て仕様、StructDoc や StructCodeBlock の markdown rendering、AgentCallParameter の型定義を調べたいとき。
- conflict 解消プロンプトではなく、session join の別用途の prompt や他サブコマンド用のエージェント呼び出しパラメータを調べたいとき。
- real path や work root の定義、パスキーワードの意味、パス解決処理そのものを確認したいとき。

## hash
- 178b29ee724b5e7ba01760409af66a822e2463ff42db68de5125061b5a4138ab
