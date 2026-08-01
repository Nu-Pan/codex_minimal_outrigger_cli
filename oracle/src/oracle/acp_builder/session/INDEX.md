# `join`

## Summary
- `cmoc session join` における merge conflict marker 解消用の AI エージェント呼び出し設定を扱う実装。対象パス、専用 prompt、書き込み権限、モデル、実行 cwd などの組み立てを確認する入口。

## Read this when
- `cmoc session join` の merge conflict 解消処理や、その agent call の prompt・モデル・権限・実行設定を変更または調査するとき。

## Do not read this when
- 通常の `session join` 処理や merge 操作そのものを調査するとき。
- 一般的な prompt 生成処理や共通の agent call パラメータ定義を確認するとき。

## hash
- c8f042a91557c1abddd59fc938d1fcb08cb718dcec3da6d616167dcd5a4cf4c3
