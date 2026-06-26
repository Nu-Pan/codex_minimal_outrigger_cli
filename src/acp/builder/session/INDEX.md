# `join`

## Summary
- `cmoc session join` における merge conflict marker 解消用のエージェント呼び出し構築を扱う領域。
- 解消対象ファイルの prompt 化、conflict marker 解消に限定する作業指示、oracle file を含むファイルアクセス制約、呼び出しモデル・reasoning・アクセスモードの固定条件を確認する入口となる。

## Read this when
- session join 中に検出された merge conflict marker を AI エージェントへ解消させるための呼び出し内容を確認または変更したいとき。
- conflict 解消タスクへ渡す role、summary、goal、追加ファイルアクセス規則、対象パス一覧の組み立てを調べたいとき。
- join 処理で conflict 対象ファイルがどのように prompt に埋め込まれ、どのファイルアクセス条件で実行されるかを確認したいとき。

## Do not read this when
- merge conflict marker の検出方法、join 全体の制御フロー、git 操作そのものを調べたいとき。
- 通常の session join 用 prompt や、conflict marker 解消以外のエージェント呼び出しパラメータを確認したいとき。
- prompt 部品の markdown レンダリング、構造化ドキュメント、パス解決 helper の詳細実装を調べたいとき。

## hash
- f3ebc8b4e31d2f112ede8674c70afa589034013385cad2d636477271686f8c18
