# `conflict_resolution.py`

## Summary
- `cmoc session join` で検出された merge conflict marker を解消するための AI エージェント呼び出しパラメータを構築する実装。
- 解消対象ファイルの実パス一覧を prompt に埋め込み、作業範囲を conflict marker 解消に限定し、oracle file も必要最小限だけ編集可能とする制約を含めた完了 prompt を生成する。
- 返却する呼び出し条件は mainstream model、medium reasoning、realization write のファイルアクセスで固定されている。

## Read this when
- `cmoc session join` の中で merge conflict marker 解消用のエージェント呼び出し内容を確認または変更したいとき。
- conflict marker 解消タスクに渡す role、summary、goal、追加ファイルアクセス規則、対象パス一覧の構成を調べたいとき。
- join 処理で conflict 対象ファイルがどのように prompt 化され、どのファイルアクセスモードで呼び出されるかを確認したいとき。

## Do not read this when
- merge conflict の検出方法、join 全体の制御フロー、git 操作そのものを調べたいとき。
- 通常の session join prompt や conflict marker 解消以外のエージェント呼び出しパラメータを確認したいとき。
- prompt 部品の markdown レンダリング、構造化ドキュメント、パス解決 helper の詳細実装を調べたいとき。

## hash
- caceb7b108026650c89706b5a14843849da1f7f4c861170455ee863feab7f786
